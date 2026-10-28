DROP TABLE IF EXISTS buses;
DROP TABLE IF EXISTS alternative_routes;
DROP TABLE IF EXISTS complaints;

-- 1. Real-Time Bus Tracking & Crowd Detection Table
CREATE TABLE buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    current_location TEXT NOT NULL,
    eta_minutes INTEGER NOT NULL,
    crowd_percentage INTEGER NOT NULL,
    crowd_status TEXT NOT NULL,
    next_bus_eta INTEGER NOT NULL
);

-- 2. Smart Route Planning (Multimodal / Connecting Buses) Table
CREATE TABLE alternative_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    option_type TEXT NOT NULL,
    route_details TEXT NOT NULL,
    total_time_mins INTEGER NOT NULL
);

-- 3. AI Complaint Management Table
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT NOT NULL,
    complaint_text TEXT NOT NULL,
    ai_category TEXT DEFAULT 'Pending',
    ai_priority TEXT DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
