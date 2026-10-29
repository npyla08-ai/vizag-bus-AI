import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "vizagbus.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS route_stops")
cursor.execute("DROP TABLE IF EXISTS complaints")

with open(SCHEMA_PATH, "r") as f:
    cursor.executescript(f.read())

stops = [
    ("RTC_COMPLEX", "Dwaraka Bus Station (RTC Complex)", 17.7289, 83.3032),
    ("GURUDWARA", "Gurudwara Junction", 17.7348, 83.3015),
    ("MADDILAPALEM", "Maddilapalem Bus Station", 17.7394, 83.3284),
    ("SIRIPURAM", "Siripuram Circle", 17.7231, 83.3175),
    ("RK_BEACH", "RK Beach Road", 17.7126, 83.3228),
    ("NAD_JUNCTION", "NAD Kotha Road Junction", 17.7472, 83.2201),
    ("GAJUWAKA", "Gajuwaka Bus Depot", 17.6908, 83.2120),
    ("SIMHACHALAM", "Simhachalam Hill Base", 17.7663, 83.2505),
    ("HANUMANTHAWAKA", "Hanumanthawaka Junction", 17.7670, 83.3421),
    ("BHEEMILI", "Bheemili Beach Stand", 17.8920, 83.4542),
    ("JAGADAMBA", "Jagadamba Centre", 17.7150, 83.3040),
    ("KURMANNAPALEM", "Kurmannapalem Junction", 17.6845, 83.1750)
]
cursor.executemany("INSERT OR REPLACE INTO stops VALUES (?, ?, ?, ?)", stops)

# Map each route to the exact stops it serves
route_stops = [
    # Route 28: RK Beach <-> Simhachalam
    ("28", "RK_BEACH"), ("28", "SIRIPURAM"), ("28", "JAGADAMBA"), ("28", "RTC_COMPLEX"), ("28", "GURUDWARA"), ("28", "NAD_JUNCTION"), ("28", "SIMHACHALAM"),
    # Route 38: RTC Complex <-> Gajuwaka
    ("38", "RTC_COMPLEX"), ("38", "GURUDWARA"), ("38", "NAD_JUNCTION"), ("38", "GAJUWAKA"), ("38", "KURMANNAPALEM"),
    # Route 900K: Maddilapalem <-> Bheemili
    ("900K", "RTC_COMPLEX"), ("900K", "MADDILAPALEM"), ("900K", "HANUMANTHAWAKA"), ("900K", "BHEEMILI"),
    # Route 400: Simhachalam <-> Kurmannapalem
    ("400", "SIMHACHALAM"), ("400", "NAD_JUNCTION"), ("400", "GAJUWAKA"), ("400", "KURMANNAPALEM"),
    # Route 60: Simhachalam <-> Jagadamba
    ("60", "SIMHACHALAM"), ("60", "GURUDWARA"), ("60", "MADDILAPALEM"), ("60", "RTC_COMPLEX"), ("60", "JAGADAMBA")
]
cursor.executemany("INSERT OR REPLACE INTO route_stops VALUES (?, ?)", route_stops)

cursor.execute("DELETE FROM buses")
buses = [
    ("AP31Z-2801", "28", "RK Beach ⇄ Simhachalam", 50, 45, 17.7290, 83.3010, "GURUDWARA", 3),
    ("AP31Z-2802", "28", "RK Beach ⇄ Simhachalam", 50, 19, 17.7210, 83.3150, "RTC_COMPLEX", 9),
    ("AP31Z-2803", "28", "RK Beach ⇄ Simhachalam", 50, 10, 17.7135, 83.3220, "SIRIPURAM", 16),
    ("AP31Z-3801", "38", "RTC Complex ⇄ Gajuwaka", 50, 47, 17.7410, 83.2350, "NAD_JUNCTION", 2),
    ("AP31Z-3802", "38", "RTC Complex ⇄ Gajuwaka", 50, 22, 17.7330, 83.2750, "NAD_JUNCTION", 8),
    ("AP31Z-3803", "38", "RTC Complex ⇄ Gajuwaka", 50, 12, 17.7289, 83.3032, "GURUDWARA", 15),
    ("AP31Z-9001", "900K", "Maddilapalem ⇄ Bheemili", 50, 44, 17.7620, 83.3390, "HANUMANTHAWAKA", 4),
    ("AP31Z-9002", "900K", "Maddilapalem ⇄ Bheemili", 50, 18, 17.7450, 83.3310, "HANUMANTHAWAKA", 11),
    ("AP31Z-9003", "900K", "Maddilapalem ⇄ Bheemili", 50, 8,  17.7394, 83.3284, "MADDILAPALEM", 19),
    ("AP31Z-4001", "400", "Simhachalam ⇄ Kurmannapalem", 50, 42, 17.7100, 83.2150, "GAJUWAKA", 5),
    ("AP31Z-4002", "400", "Simhachalam ⇄ Kurmannapalem", 50, 16, 17.7480, 83.2250, "NAD_JUNCTION", 13),
    ("AP31Z-6001", "60", "Simhachalam ⇄ Jagadamba", 50, 39, 17.7360, 83.3050, "RTC_COMPLEX", 6),
    ("AP31Z-6002", "60", "Simhachalam ⇄ Jagadamba", 50, 14, 17.7550, 83.2700, "GURUDWARA", 14)
]
cursor.executemany("""
    INSERT OR REPLACE INTO buses 
    (bus_id, route_no, route_name, total_seats, current_passengers, current_lat, current_lng, next_stop_id, eta_minutes) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", buses)

conn.commit()
conn.close()
print("✓ Database updated with route-stop mappings and seeded!")
