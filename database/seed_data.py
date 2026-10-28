import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "vizag_bus.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Run schema.sql to create tables
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # 2. Insert Fake Vizag Buses
    buses_data = [
        # Route 1: Gajuwaka -> Maddilapalem
        ("400K", "Gajuwaka", "Maddilapalem", "NAD Junction", 5, 92, "Overcrowded", 15),
        ("400", "Gajuwaka", "Maddilapalem", "Airport", 15, 30, "Comfortable", 30),

        # Route 2: RTC Complex -> Rushikonda
        ("900K", "RTC Complex", "Rushikonda", "Siripuram", 4, 88, "Overcrowded", 14),
        ("900T", "RTC Complex", "Rushikonda", "MVP Colony", 14, 25, "Comfortable", 28),

        # Route 3: Simhachalam -> RK Beach
        ("28", "Simhachalam", "RK Beach", "Gopalapatnam", 6, 85, "Overcrowded", 16),
        ("28A", "Simhachalam", "RK Beach", "NAD Junction", 16, 40, "Comfortable", 30),

        # Route 4: Kurmannapalem -> Siripuram
        ("38", "Kurmannapalem", "Siripuram", "Sheela Nagar", 8, 55, "Moderate", 20),
        ("38K", "Kurmannapalem", "Siripuram", "BHPV", 18, 20, "Comfortable", 35)
    ]

    cursor.executemany("""
        INSERT INTO buses (bus_number, source, destination, current_location, eta_minutes, crowd_percentage, crowd_status, next_bus_eta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, buses_data)

    # 3. Insert Multimodal / Alternative Routes
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

    # 4. Insert 1 Sample Complaint for the Demo
    cursor.execute("""
        INSERT INTO complaints (bus_number, complaint_text, ai_category, ai_priority)
        VALUES ('400K', 'Bus skipped the NAD Junction stop during peak hours due to heavy crowd.', 'Route / Stop Violation', 'High')
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized and seeded successfully at: {DB_PATH}")

if __name__ == "__main__":
    seed_database()
