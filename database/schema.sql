CREATE TABLE IF NOT EXISTS bus_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stop_name TEXT NOT NULL UNIQUE,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    area TEXT,
    landmark TEXT
);

CREATE TABLE IF NOT EXISTS bus_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL UNIQUE,
    route_name TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    via TEXT NOT NULL,
    bus_type TEXT DEFAULT 'Metro Express',
    frequency_mins INTEGER DEFAULT 15,
    first_bus_time TEXT DEFAULT '05:30 AM',
    last_bus_time TEXT DEFAULT '10:30 PM',
    fare_min INTEGER DEFAULT 10,
    fare_max INTEGER DEFAULT 35,
    total_stops INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS route_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL,
    stop_sequence INTEGER NOT NULL,
    stop_name TEXT NOT NULL,
    distance_km REAL DEFAULT 0.0,
    eta_from_start_mins INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    current_location TEXT NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    eta_minutes INTEGER NOT NULL,
    crowd_percentage INTEGER NOT NULL,
    crowd_status TEXT NOT NULL,
    next_bus_eta INTEGER NOT NULL,
    speed_kmh INTEGER DEFAULT 32,
    bus_type TEXT DEFAULT 'Metro Express'
);

CREATE TABLE IF NOT EXISTS alternative_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    option_type TEXT NOT NULL,
    route_details TEXT NOT NULL,
    total_time_mins INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL UNIQUE,
    bus_number TEXT NOT NULL,
    complaint_text TEXT NOT NULL,
    ai_category TEXT DEFAULT 'Pending',
    ai_priority TEXT DEFAULT 'Medium',
    status TEXT DEFAULT 'Open',
    media_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
