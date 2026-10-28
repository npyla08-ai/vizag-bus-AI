import sqlite3
import os

# Points directly to vizag-bus-AI/database/vizag_bus.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "vizag_bus.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Converts rows into easy Python dictionaries
    return conn

def fetch_buses(source=None, destination=None):
    """Get all buses, or filter by source and destination."""
    conn = get_connection()
    cursor = conn.cursor()
    if source and destination:
        cursor.execute(
            "SELECT * FROM buses WHERE LOWER(source) = LOWER(?) AND LOWER(destination) = LOWER(?)",
            (source, destination)
        )
    else:
        cursor.execute("SELECT * FROM buses")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def fetch_alternatives(source, destination):
    """Get multimodal/connecting route options for a route."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM alternative_routes WHERE LOWER(source) = LOWER(?) AND LOWER(destination) = LOWER(?)",
        (source, destination)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def update_crowd_level(bus_number, crowd_percentage):
    """Update bus occupancy (used for Computer Vision crowd simulation)."""
    if crowd_percentage >= 75:
        status = "Overcrowded"
    elif crowd_percentage >= 45:
        status = "Moderate"
    else:
        status = "Comfortable"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE buses SET crowd_percentage = ?, crowd_status = ? WHERE bus_number = ?",
        (crowd_percentage, status, bus_number)
    )
    conn.commit()
    conn.close()
    return {"bus_number": bus_number, "crowd_percentage": crowd_percentage, "crowd_status": status}

def save_complaint(bus_number, complaint_text, ai_category="Pending", ai_priority="Medium"):
    """Save a commuter complaint with AI-assigned category and priority."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO complaints (bus_number, complaint_text, ai_category, ai_priority) VALUES (?, ?, ?, ?)",
        (bus_number, complaint_text, ai_category, ai_priority)
    )
    conn.commit()
    conn.close()

def fetch_complaints():
    """Get all complaints ordered by newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
