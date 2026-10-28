import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "vizag_bus.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # Real Vizag GPS coordinates (lat, lng) for Leaflet Map pins
    buses_data = [
        # Route 1: Gajuwaka -> Maddilapalem
        ("400K", "Gajuwaka", "Maddilapalem", "NAD Junction", 17.7447, 83.2319, 5, 92, "Overcrowded", 15),
        ("400", "Gajuwaka", "Maddilapalem", "Visakhapatnam Airport", 17.7225, 83.2245, 15, 30, "Comfortable", 30),

        # Route 2: RTC Complex -> Rushikonda
        ("900K", "RTC Complex", "Rushikonda", "Siripuram Junction", 17.7205, 83.3168, 4, 88, "Overcrowded", 14),
        ("900T", "RTC Complex", "Rushikonda", "MVP Colony", 17.7412, 83.3375, 14, 25, "Comfortable", 28),

        # Route 3: Simhachalam -> RK Beach
        ("28", "Simhachalam", "RK Beach", "Gopalapatnam", 17.7563, 83.2185, 6, 85, "Overcrowded", 16),
        ("28A", "Simhachalam", "RK Beach", "NAD Junction", 17.7447, 83.2319, 16, 40, "Comfortable", 30),

        # Route 4: Kurmannapalem -> Siripuram
        ("38", "Kurmannapalem", "Siripuram", "Sheela Nagar", 17.7095, 83.2045, 8, 55, "Moderate", 20),
        ("38K", "Kurmannapalem", "Siripuram", "BHPV Junction", 17.7032, 83.1950, 18, 20, "Comfortable", 35)
    ]

    cursor.executemany("""
        INSERT INTO buses (bus_number, source, destination, current_location, lat, lng, eta_minutes, crowd_percentage, crowd_status, next_bus_eta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, buses_data)

    alternatives_data = [
        ("Gajuwaka", "Maddilapalem", "Connecting Bus", "Take Bus 38 to NAD Junction (5 mins away), then switch to Metro Express 555 to Maddilapalem.", 32),
        ("RTC Complex", "Rushikonda", "Auto + Bus Combo", "Take Shared Auto to MVP Colony (8 mins), then board less-crowded Beach Bus 900T.", 24),
        ("Simhachalam", "RK Beach", "Connecting Bus", "Board Bus 55 to NAD Junction, then transfer to City Direct 10K to RK Beach.", 38),
        ("Kurmannapalem", "Siripuram", "Cab + Bus Combo", "Take Rapido/Auto to Gajuwaka Depot (6 mins), then board Express Bus 400 to Siripuram.", 28)
    ]

    cursor.executemany("""
        INSERT INTO alternative_routes (source, destination, option_type, route_details, total_time_mins)
        VALUES (?, ?, ?, ?, ?)
    """, alternatives_data)

    cursor.execute("""
        INSERT INTO complaints (bus_number, complaint_text, ai_category, ai_priority)
        VALUES ('400K', 'Bus skipped the NAD Junction stop during peak hours due to heavy crowd.', 'Route / Stop Violation', 'High')
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database updated with Vizag Map coordinates at: {DB_PATH}")

if __name__ == "__main__":
    seed_database()