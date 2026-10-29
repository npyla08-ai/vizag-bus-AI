CREATE TABLE IF NOT EXISTS stops (
    stop_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS route_stops (
    route_no TEXT NOT NULL,
    stop_id TEXT NOT NULL,
    PRIMARY KEY (route_no, stop_id),
    FOREIGN KEY(stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS buses (
    bus_id TEXT PRIMARY KEY,
    route_no TEXT NOT NULL,
    route_name TEXT NOT NULL,
    total_seats INTEGER DEFAULT 50,
    current_passengers INTEGER DEFAULT 0,
    current_lat REAL NOT NULL,
    current_lng REAL NOT NULL,
    next_stop_id TEXT,
    eta_minutes INTEGER DEFAULT 5,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(next_stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_id TEXT NOT NULL,
    stop_name TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    description TEXT,
    has_video BOOLEAN DEFAULT 0,
    media_data TEXT,
    media_type TEXT,
    status TEXT DEFAULT 'Pending',
    logged_occupancy_pct INTEGER,
    ai_verified BOOLEAN DEFAULT 0,
    ai_severity TEXT,
    ai_fine_inr INTEGER,
    ai_action_summary TEXT,
    ai_depot_order TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
