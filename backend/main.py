from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from db import get_db

app = FastAPI(title="VizagBus AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stops")
def get_stops():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stops")
    stops_rows = cursor.fetchall()

    cursor.execute("SELECT route_no, stop_id FROM route_stops")
    rs_rows = cursor.fetchall()

    stop_routes_map = {}
    for r in rs_rows:
        sid = r["stop_id"]
        if sid not in stop_routes_map:
            stop_routes_map[sid] = []
        if r["route_no"] not in stop_routes_map[sid]:
            stop_routes_map[sid].append(r["route_no"])

    result = []
    for s in stops_rows:
        sid = s["stop_id"]
        result.append({
            "stop_id": sid,
            "name": s["name"],
            "lat": s["latitude"],
            "lng": s["longitude"],
            "routes": stop_routes_map.get(sid, [])
        })
    conn.close()
    return result

@app.get("/api/buses")
def get_buses(route_no: Optional[str] = None):
    conn = get_db()
    cursor = conn.cursor()
    if route_no:
        cursor.execute("""
            SELECT b.*, s.name as next_stop_name 
            FROM buses b 
            LEFT JOIN stops s ON b.next_stop_id = s.stop_id
            WHERE b.route_no = ?
        """, (route_no,))
    else:
        cursor.execute("""
            SELECT b.*, s.name as next_stop_name 
            FROM buses b 
            LEFT JOIN stops s ON b.next_stop_id = s.stop_id
        """)
    rows = cursor.fetchall()

    cursor.execute("SELECT route_no, stop_id FROM route_stops")
    rs_rows = cursor.fetchall()
    route_stops_map = {}
    for r in rs_rows:
        rn = r["route_no"]
        if rn not in route_stops_map:
            route_stops_map[rn] = []
        route_stops_map[rn].append(r["stop_id"])

    buses = []
    for r in rows:
        occ_pct = int((r["current_passengers"] / r["total_seats"]) * 100)
        status = "Available" if occ_pct < 50 else ("Moderate" if occ_pct <= 85 else "Crowded")
        buses.append({
            "id": r["bus_id"],
            "route_no": r["route_no"],
            "route_name": r["route_name"],
            "total_seats": r["total_seats"],
            "current_passengers": r["current_passengers"],
            "current_lat": r["current_lat"],
            "current_lng": r["current_lng"],
            "next_stop_id": r["next_stop_id"],
            "next_stop": r["next_stop_name"] or r["next_stop_id"],
            "eta_minutes": r["eta_minutes"],
            "occupancy_pct": occ_pct,
            "occupancy_status": status,
            "served_stops": route_stops_map.get(r["route_no"], [])
        })
    conn.close()
    return buses

class ConductorUpdate(BaseModel):
    bus_id: str
    delta_passengers: int

@app.post("/api/conductor/update")
def update_headcount(payload: ConductorUpdate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT current_passengers, total_seats FROM buses WHERE bus_id = ?", (payload.bus_id,))
    bus = cursor.fetchone()
    if not bus:
        conn.close()
        raise HTTPException(status_code=404, detail="Bus not found")
    
    new_count = max(0, min(bus["total_seats"] + 15, bus["current_passengers"] + payload.delta_passengers))
    cursor.execute("UPDATE buses SET current_passengers = ? WHERE bus_id = ?", (new_count, payload.bus_id))
    conn.commit()
    conn.close()
    return {"bus_id": payload.bus_id, "current_passengers": new_count}

class NewStopRequest(BaseModel):
    stop_id: str
    name: str
    latitude: float
    longitude: float

@app.post("/api/admin/stops")
def add_stop(payload: NewStopRequest):
    conn = get_db()
    cursor = conn.cursor()
    stop_id_clean = payload.stop_id.strip().upper().replace(" ", "_")
    cursor.execute(
        "INSERT OR REPLACE INTO stops (stop_id, name, latitude, longitude) VALUES (?, ?, ?, ?)",
        (stop_id_clean, payload.name.strip(), payload.latitude, payload.longitude)
    )
    conn.commit()
    conn.close()
    return {"status": "success", "stop_id": stop_id_clean}

class NewBusRequest(BaseModel):
    bus_id: str
    route_no: str
    route_name: str
    total_seats: int = 50
    current_passengers: int = 10
    next_stop_id: str
    eta_minutes: int = 5
    served_stop_ids: List[str] = []

@app.post("/api/admin/buses")
def add_bus(payload: NewBusRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM stops WHERE stop_id = ?", (payload.next_stop_id,))
    stop = cursor.fetchone()
    lat = stop["latitude"] + 0.002 if stop else 17.7289
    lng = stop["longitude"] + 0.002 if stop else 83.3032

    cursor.execute("""
        INSERT OR REPLACE INTO buses 
        (bus_id, route_no, route_name, total_seats, current_passengers, current_lat, current_lng, next_stop_id, eta_minutes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        payload.bus_id.strip().upper(),
        payload.route_no.strip().upper(),
        payload.route_name.strip(),
        payload.total_seats,
        payload.current_passengers,
        lat,
        lng,
        payload.next_stop_id,
        payload.eta_minutes
    ))

    stops_to_link = set(payload.served_stop_ids)
    stops_to_link.add(payload.next_stop_id)
    for sid in stops_to_link:
        cursor.execute("INSERT OR IGNORE INTO route_stops (route_no, stop_id) VALUES (?, ?)", (payload.route_no.strip().upper(), sid))

    conn.commit()
    conn.close()
    return {"status": "success", "bus_id": payload.bus_id}

# ----------------- COMPLAINTS WITH MEDIA & RESOLVE BUTTON -----------------

class GrievanceSubmission(BaseModel):
    bus_id: str
    stop_name: str
    issue_type: str
    description: str
    has_video: bool = False
    media_data: Optional[str] = None
    media_type: Optional[str] = None

@app.post("/api/complaints/triage")
def triage_complaint(payload: GrievanceSubmission):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT current_passengers, total_seats FROM buses WHERE bus_id = ?", (payload.bus_id,))
    bus = cursor.fetchone()
    logged_occ = int((bus["current_passengers"] / bus["total_seats"]) * 100) if bus else 0
    
    # --- GEMMA 4 HOOK AREA (IMPLEMENT AT EVENT) ---
    is_verified = True if (logged_occ < 50 and "empty" in payload.issue_type.lower()) or "rash" in payload.issue_type.lower() else False
    severity = "Critical" if "rash" in payload.issue_type.lower() else ("High" if is_verified else "Medium")
    fine = 1500 if "rash" in payload.issue_type.lower() else 500

    action_summary = (
        f"Gemma 4 Verification: Bus {payload.bus_id} was recorded at {logged_occ}% occupancy near {payload.stop_name}. "
        f"{'Telemetry confirms empty seats were available when stop was skipped.' if logged_occ < 50 else 'Logged for safety review.'}"
    )
    depot_order = f"Issue Action Notice to Driver of {payload.bus_id} under APSRTC Rule 14B. Penalty: ₹{fine}."

    cursor.execute("""
        INSERT INTO complaints 
        (bus_id, stop_name, issue_type, description, has_video, media_data, media_type, status, logged_occupancy_pct, ai_verified, ai_severity, ai_fine_inr, ai_action_summary, ai_depot_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?, ?, ?, ?, ?, ?)
    """, (
        payload.bus_id,
        payload.stop_name,
        payload.issue_type,
        payload.description,
        payload.has_video,
        payload.media_data,
        payload.media_type,
        logged_occ,
        is_verified,
        severity,
        fine,
        action_summary,
        depot_order
    ))
    conn.commit()
    complaint_id = cursor.lastrowid
    conn.close()

    return {
        "status": "submitted",
        "complaint_id": complaint_id,
        "message": "Complaint registered with media and forwarded to APSRTC Management."
    }

@app.post("/api/complaints/{complaint_id}/resolve")
def resolve_complaint(complaint_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = 'Resolved' WHERE id = ?", (complaint_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "complaint_id": complaint_id, "new_status": "Resolved"}

@app.get("/api/complaints")
def get_complaints():
    conn = get_db()
    cursor = conn.cursor()
    # Sort Pending first, then by newest ID
    cursor.execute("SELECT * FROM complaints ORDER BY CASE WHEN status = 'Pending' THEN 0 ELSE 1 END, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

class CommuterQuery(BaseModel):
    query: str
    user_location: str

@app.post("/api/ai/commuter-agent")
def commuter_agent(payload: CommuterQuery):
    # --- GEMMA 4 HOOK AREA (IMPLEMENT AT EVENT) ---
    mock_reply = (
        f"[Gemma 4 Agent]: Near {payload.user_location}, check the filtered route pills on your left. "
        f"Wait for a green (<50% occupancy) bus if the incoming one is marked overcrowded (>85%)."
    )
    return {"reply": mock_reply}
