import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "vizagbus.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(SCHEMA_PATH, "r") as f:
    cursor.executescript(f.read())

# 1. All Visakhapatnam Bus Stops from Friend's DB
bus_stops = [
    ("RTC Complex (Dwaraka Nagar)", 17.7244, 83.3063, "Central Vizag", "APSRTC Central Bus Terminal"),
    ("Siripuram Junction", 17.7205, 83.3182, "Central Vizag", "Near RTIH & AU Ingate"),
    ("Maddilapalem", 17.7368, 83.3205, "Central Vizag", "BRTS Terminal & AU Engineering"),
    ("MVP Colony Circle", 17.7447, 83.3340, "Central Vizag", "Sector 3 MVP Circle"),
    ("Ushodaya Junction", 17.7412, 83.3310, "Central Vizag", "MVP Main Road"),
    ("Jagadamba Junction", 17.7121, 83.3025, "Old City & Commercial", "Cinema & Shopping Center"),
    ("Visakhapatnam Railway Station", 17.7222, 83.2901, "Central Vizag", "Main Junction Railway Station"),
    ("Town Kotharoad", 17.6980, 83.2945, "Old City", "Old Post Office & Port Area"),
    ("Collector Office", 17.7095, 83.3095, "Central Vizag", "District Collectorate & Police Barracks"),
    ("Waltair Uplands", 17.7235, 83.3210, "Central Vizag", "AU North Gate & Medical Area"),
    ("Andhra University", 17.7285, 83.3230, "Central Vizag", "AU North Campus Main Gate"),
    ("Gurudwara Junction", 17.7348, 83.3015, "Central Vizag", "City Central Junction"),
    ("Satyam Junction", 17.7355, 83.3125, "Central Vizag", "Near Rama Talkies & Maddilapalem"),
    ("Seethammadhara", 17.7420, 83.3110, "Central Vizag", "North Central Residential Area"),
    ("Venkojipalem", 17.7485, 83.3260, "North Corridor", "NH16 Zoo Road Junction"),
    ("Hanumanthawaka Junction", 17.7556, 83.3315, "North Corridor", "Major BRTS Transit Hub"),
    ("Arilova / Health City", 17.7640, 83.3180, "North Suburbs", "VIMS & Apollo Health City"),
    ("Zoo Park Stop", 17.7685, 83.3445, "North Corridor", "Indira Gandhi Zoological Park"),
    ("Pothinamallayya Palem", 17.7860, 83.3540, "North Suburbs", "PM Palem Terminal"),
    ("ACA-VDCA Cricket Stadium", 17.7965, 83.3525, "North Suburbs", "PM Palem International Stadium"),
    ("Car Shed Junction", 17.8045, 83.3560, "North Suburbs", "Madhurawada Entrance"),
    ("Madhurawada", 17.8165, 83.3585, "North Suburbs", "IT & Educational Hub"),
    ("Kommadi Junction", 17.8285, 83.3610, "North Suburbs", "Gayatri College Junction"),
    ("Marikavalasa", 17.8480, 83.3680, "North Suburbs", "NH16 North Suburb"),
    ("Anandapuram Junction", 17.8820, 83.3790, "Suburban North", "Highway Intersection"),
    ("Tagarapuvalasa", 17.9260, 83.4240, "Suburban North", "Vizag-Vizianagaram Highway"),
    ("RK Beach", 17.7143, 83.3236, "Beach Road", "Submarine Museum & Beach Front"),
    ("Pandurangapuram", 17.7180, 83.3285, "Beach Road", "Near Coastal Battery"),
    ("Sagar Nagar", 17.7610, 83.3590, "Beach Road", "Beach Road Scenic Junction"),
    ("Rushikonda Beach Stop", 17.7819, 83.3852, "Beach Road", "Rushikonda Blue Flag Beach"),
    ("GITAM University", 17.7835, 83.3785, "Beach Road", "Main Campus Entrance"),
    ("IT SEZ (Rushikonda Hills)", 17.7940, 83.3830, "Beach Road", "Millennium Tower IT Park"),
    ("Mangamaripeta", 17.8210, 83.4090, "Beach Road", "Thotlakonda Beach Road"),
    ("INS Kalinga", 17.8510, 83.4280, "Beach Road", "Naval Base & Coastal Road"),
    ("Bheemunipatnam Bus Stand", 17.8905, 83.4520, "Bheemili Suburb", "Historic Bheemili Terminal"),
    ("Kancharapalem", 17.7315, 83.2790, "South Corridor", "Urdu Junior College / Kancharapalem"),
    ("Urvasi Junction", 17.7365, 83.2680, "South Corridor", "Kancharapalem Highway Junction"),
    ("Marripalem", 17.7410, 83.2530, "South Corridor", "Railway Quarters & NH16"),
    ("NAD Junction", 17.7442, 83.2328, "Major Transit Hub", "NAD Double Flyover Hub"),
    ("Visakhapatnam Airport", 17.7285, 83.2245, "South Corridor", "International Airport Terminal"),
    ("Sheela Nagar", 17.7120, 83.2180, "Industrial South", "Near Port Connectivity Road"),
    ("BHPV Junction", 17.7040, 83.2130, "Industrial South", "Heavy Plates Engineering Unit"),
    ("Autonagar Gate", 17.6960, 83.2110, "Industrial South", "Industrial Estate Gate"),
    ("Gajuwaka Junction", 17.6868, 83.2185, "Industrial South", "Gajuwaka Commercial Center"),
    ("Old Gajuwaka", 17.6820, 83.2150, "Industrial South", "Market Road Bus Stop"),
    ("New Gajuwaka", 17.6850, 83.2040, "Industrial South", "Gajuwaka RTC Depot Hub"),
    ("Sriharipuram", 17.6810, 83.2410, "Port Corridor", "Industrial Suburb"),
    ("Coromandel Gate", 17.6835, 83.2520, "Port Corridor", "Coromandel Plant"),
    ("Malkapuram", 17.6860, 83.2650, "Port Corridor", "HPCL Refinery Gate"),
    ("Scindia Junction", 17.6910, 83.2780, "Port Corridor", "Hindustan Shipyard Entrance"),
    ("Naval Dockyard", 17.7010, 83.2880, "Port Corridor", "INHS Kalyani & Port Gate"),
    ("Kurmannapalem Junction", 17.6745, 83.1852, "Industrial South", "Steel Plant Highway Junction"),
    ("Steel Plant Main Gate", 17.6610, 83.1680, "Ukkunagaram", "RINL Visakhapatnam Steel Plant"),
    ("Steel Plant Township Sector 6", 17.6480, 83.1550, "Ukkunagaram", "Ukkunagaram Central Township"),
    ("Duvvada Railway Station", 17.7020, 83.1510, "South Suburb", "Major Express Train Station"),
    ("Desapatrunipalem", 17.6590, 83.1380, "South Suburb", "Steel Plant Outskirts"),
    ("Parawada Junction", 17.6320, 83.0950, "Industrial South", "Pharma City Entrance"),
    ("NTPC Simhadri Gate", 17.5980, 83.0890, "Industrial South", "NTPC Thermal Power Station"),
    ("Atchutapuram", 17.5620, 82.9890, "Industrial SEZ", "APSEZ & Multi-Product SEZ"),
    ("Lankelapalem Junction", 17.6790, 83.1120, "South Highway", "NH16 Junction to Anakapalle"),
    ("Anakapalle RTC Complex", 17.6896, 83.0039, "Anakapalle Suburb", "Anakapalle Major Transit Hub"),
    ("Gopalapatnam", 17.7524, 83.2188, "West Transit Hub", "Gopalapatnam Petrol Bunk"),
    ("Simhachalam Foothills", 17.7665, 83.2505, "Simhachalam", "Varaha Narasimha Temple Foothills"),
    ("Simhachalam Temple", 17.7663, 83.2505, "Simhachalam", "Hill Top Temple Complex"),
    ("Vepagunta Junction", 17.7680, 83.2110, "West Suburbs", "BRTS West Hub"),
    ("Sujatha Nagar", 17.7790, 83.2080, "West Suburbs", "Residential Suburb Stop"),
    ("Chintalagraharam", 17.7890, 83.2040, "West Suburbs", "Pendurthi Highway Stop"),
    ("Pendurthi Junction", 17.8040, 83.2010, "West Transit Hub", "Pendurthi Railway & Market Hub"),
    ("Sabbavaram Junction", 17.7910, 83.1250, "West Suburbs", "DSNLU & Maritime University"),
    ("Kothavalasa", 17.8920, 83.1890, "Suburban West", "Kothavalasa Junction Terminal")
]
cursor.executemany("INSERT OR REPLACE INTO bus_stops (stop_name, lat, lng, area, landmark) VALUES (?, ?, ?, ?, ?)", bus_stops)

# 2. All 29 APSRTC Bus Routes from Friend's DB
bus_routes = [
    ("400K", "Gajuwaka to Maddilapalem Express", "Gajuwaka Junction", "Maddilapalem", "Via Airport, NAD Junction, RTC Complex, Siripuram", "Metro Express", 12, "05:00 AM", "11:30 PM", 15, 35, 11),
    ("400", "Kurmannapalem to Maddilapalem", "Kurmannapalem Junction", "Maddilapalem", "Via Gajuwaka, NAD Junction, Gurudwara, Siripuram", "City Ordinary", 15, "05:30 AM", "10:45 PM", 10, 30, 10),
    ("400H", "Steel Plant to Maddilapalem", "Steel Plant Main Gate", "Maddilapalem", "Via Kurmannapalem, Gajuwaka, Airport, Railway Station, RTC Complex", "Metro Express", 20, "06:00 AM", "10:15 PM", 15, 40, 9),
    ("400Y", "Anakapalle to RTC Complex Express", "Anakapalle RTC Complex", "RTC Complex (Dwaraka Nagar)", "Via Lankelapalem, Kurmannapalem, Gajuwaka, NAD, Kancharapalem", "Metro Express", 15, "05:00 AM", "11:00 PM", 20, 50, 10),
    ("900K", "RTC Complex to Bheemili Beach Road", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand", "Via Siripuram, Maddilapalem, MVP Colony, Rushikonda, GITAM, IT SEZ", "Metro Express", 15, "05:30 AM", "10:30 PM", 15, 45, 11),
    ("900T", "RTC Complex to Rushikonda IT SEZ", "RTC Complex (Dwaraka Nagar)", "IT SEZ (Rushikonda Hills)", "Via Siripuram, Maddilapalem, MVP Colony, Sagar Nagar, Rushikonda Beach", "City Sheetal AC", 20, "06:00 AM", "09:45 PM", 25, 50, 9),
    ("900", "Railway Station to Bheemunipatnam", "Visakhapatnam Railway Station", "Bheemunipatnam Bus Stand", "Via Jagadamba, RTC Complex, Siripuram, Maddilapalem, Rushikonda", "City Ordinary", 20, "06:15 AM", "09:30 PM", 10, 40, 9),
    ("28A", "RK Beach to Simhachalam Foothills", "RK Beach", "Simhachalam Foothills", "Via Jagadamba, RTC Complex, Gurudwara, NAD Junction, Gopalapatnam", "Metro Express", 12, "05:15 AM", "11:00 PM", 15, 35, 11),
    ("28", "RK Beach to Pendurthi Junction", "RK Beach", "Pendurthi Junction", "Via Jagadamba, RTC Complex, NAD, Gopalapatnam, Vepagunta, Sujatha Nagar", "City Ordinary", 15, "05:30 AM", "10:30 PM", 10, 35, 9),
    ("28K", "Town Kotharoad to Kothavalasa", "Town Kotharoad", "Kothavalasa", "Via Jagadamba, RTC Complex, NAD, Simhachalam, Pendurthi", "City Ordinary", 25, "05:45 AM", "09:30 PM", 10, 45, 9),
    ("38", "Kurmannapalem to Siripuram Junction", "Kurmannapalem Junction", "Siripuram Junction", "Via Gajuwaka, Airport, NAD Junction, Urvasi, Railway Station, RTC Complex", "Metro Express", 10, "05:30 AM", "11:00 PM", 15, 35, 11),
    ("38K", "Duvvada Railway Station to RTC Complex", "Duvvada Railway Station", "RTC Complex (Dwaraka Nagar)", "Via Kurmannapalem, Gajuwaka, Airport, NAD, Gurudwara", "Metro Express", 15, "05:00 AM", "11:15 PM", 15, 40, 8),
    ("38A", "Steel Plant Sector 6 to Siripuram", "Steel Plant Township Sector 6", "Siripuram Junction", "Via Steel Plant Main Gate, Kurmannapalem, Gajuwaka, NAD, RTC Complex", "Metro Express", 20, "06:00 AM", "10:00 PM", 15, 40, 8),
    ("38H", "Gajuwaka to Maddilapalem via Scindia", "Gajuwaka Junction", "Maddilapalem", "Via Sriharipuram, Malkapuram, Scindia, Dockyard, Kotharoad, Jagadamba, RTC Complex", "City Ordinary", 20, "05:30 AM", "10:00 PM", 10, 30, 9),
    ("500", "RTC Complex to Anandapuram via Pendurthi", "RTC Complex (Dwaraka Nagar)", "Anandapuram Junction", "Via Gurudwara, NAD Junction, Gopalapatnam, Vepagunta, Pendurthi", "Metro Express", 20, "05:30 AM", "10:00 PM", 15, 40, 7),
    ("500A", "Railway Station to Pendurthi Junction", "Visakhapatnam Railway Station", "Pendurthi Junction", "Via RTC Complex, Kancharapalem, NAD, Gopalapatnam, Vepagunta", "City Ordinary", 20, "06:00 AM", "10:00 PM", 10, 35, 7),
    ("500D", "Maddilapalem to Pendurthi BRTS", "Maddilapalem", "Pendurthi Junction", "Via Satyam Junction, Gurudwara, NAD, Gopalapatnam, Sujatha Nagar", "Metro Express", 15, "05:45 AM", "10:15 PM", 15, 35, 8),
    ("60", "Simhachalam Foothills to Town Kotharoad", "Simhachalam Foothills", "Town Kotharoad", "Via Gopalapatnam, NAD, Urvasi, Kancharapalem, Railway Station, Jagadamba", "City Ordinary", 15, "05:30 AM", "10:30 PM", 10, 30, 9),
    ("60C", "Simhachalam Foothills to RK Beach", "Simhachalam Foothills", "RK Beach", "Via Gopalapatnam, NAD Junction, Kancharapalem, RTC Complex, Jagadamba", "Metro Express", 18, "06:00 AM", "10:00 PM", 15, 35, 8),
    ("10K", "Town Kotharoad to Gopalapatnam", "Town Kotharoad", "Gopalapatnam", "Via Jagadamba, RTC Complex, Gurudwara, Marripalem, NAD Junction", "City Ordinary", 15, "05:30 AM", "10:45 PM", 10, 25, 7),
    ("222", "RTC Complex to Tagarapuvalasa Highway", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Via Maddilapalem, Hanumanthawaka, PM Palem, Madhurawada, Kommadi, Anandapuram", "Metro Express", 12, "05:00 AM", "11:00 PM", 15, 45, 12),
    ("222V", "Railway Station to Tagarapuvalasa", "Visakhapatnam Railway Station", "Tagarapuvalasa", "Via RTC Complex, Maddilapalem, Hanumanthawaka, Madhurawada, Anandapuram", "City Ordinary", 20, "06:00 AM", "09:30 PM", 10, 40, 8),
    ("55", "Scindia to Simhachalam Foothills", "Scindia Junction", "Simhachalam Foothills", "Via Malkapuram, Sriharipuram, Gajuwaka, Sheela Nagar, NAD, Gopalapatnam", "Metro Express", 15, "05:45 AM", "10:00 PM", 15, 35, 10),
    ("55K", "Scindia to Kothavalasa", "Scindia Junction", "Kothavalasa", "Via Sriharipuram, Gajuwaka, NAD, Gopalapatnam, Vepagunta, Pendurthi", "City Ordinary", 25, "06:00 AM", "09:00 PM", 10, 45, 8),
    ("68", "RTC Complex to Sabbavaram Junction", "RTC Complex (Dwaraka Nagar)", "Sabbavaram Junction", "Via NAD, Gopalapatnam, Vepagunta, Pendurthi Junction, Sabbavaram", "City Ordinary", 25, "06:30 AM", "09:15 PM", 10, 40, 6),
    ("88K", "Maddilapalem to Atchutapuram SEZ", "Maddilapalem", "Atchutapuram", "Via Siripuram, RTC Complex, NAD, Gajuwaka, Kurmannapalem, Parawada, NTPC", "Metro Express", 30, "05:30 AM", "10:00 PM", 20, 55, 10),
    ("99K", "Town Kotharoad to Bheemili Coastal Route", "Town Kotharoad", "Bheemunipatnam Bus Stand", "Via Collector Office, RK Beach, Sagar Nagar, Rushikonda, GITAM", "City Ordinary", 20, "06:00 AM", "09:30 PM", 10, 40, 8),
    ("111", "Kurmannapalem to Madhurawada Car Shed", "Kurmannapalem Junction", "Car Shed Junction", "Via Gajuwaka, Airport, NAD, Gurudwara, Maddilapalem, Hanumanthawaka, PM Palem, Madhurawada", "Metro Express", 12, "05:30 AM", "10:30 PM", 15, 45, 10),
    ("211", "Railway Station to Health City / VIMS", "Visakhapatnam Railway Station", "Arilova / Health City", "Via RTC Complex, Gurudwara, Seethammadhara, Hanumanthawaka", "City Ordinary", 18, "06:15 AM", "10:00 PM", 10, 25, 6),
    ("541", "Maddilapalem to Kothavalasa Express", "Maddilapalem", "Kothavalasa", "Via Gurudwara, NAD Junction, Gopalapatnam, Vepagunta, Pendurthi", "Metro Express", 20, "06:00 AM", "09:30 PM", 15, 45, 7)
]
cursor.executemany("""
    INSERT OR REPLACE INTO bus_routes
    (bus_number, route_name, source, destination, via, bus_type, frequency_mins, first_bus_time, last_bus_time, fare_min, fare_max, total_stops)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", bus_routes)

# 2b. Complete Route Stops Mapping for All 30 Routes
cursor.execute("DELETE FROM route_stops")
routes_stops_dict = {
    '400K': ['Gajuwaka Junction', 'BHPV Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Marripalem', 'Urvasi Junction', 'Kancharapalem', 'Gurudwara Junction', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Andhra University', 'Maddilapalem'],
    '400': ['Kurmannapalem Junction', 'Old Gajuwaka', 'Gajuwaka Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Urvasi Junction', 'Gurudwara Junction', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Maddilapalem'],
    '400H': ['Steel Plant Main Gate', 'Kurmannapalem Junction', 'Old Gajuwaka', 'Gajuwaka Junction', 'Visakhapatnam Airport', 'NAD Junction', 'Kancharapalem', 'Visakhapatnam Railway Station', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Maddilapalem'],
    '400Y': ['Anakapalle RTC Complex', 'Lankelapalem Junction', 'Kurmannapalem Junction', 'Gajuwaka Junction', 'Visakhapatnam Airport', 'NAD Junction', 'Marripalem', 'Kancharapalem', 'RTC Complex (Dwaraka Nagar)'],
    '900K': ['RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Andhra University', 'Maddilapalem', 'Ushodaya Junction', 'MVP Colony Circle', 'Venkojipalem', 'Sagar Nagar', 'Rushikonda Beach Stop', 'GITAM University', 'IT SEZ (Rushikonda Hills)', 'Mangamaripeta', 'INS Kalinga', 'Bheemunipatnam Bus Stand'],
    '900T': ['RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Andhra University', 'Maddilapalem', 'Ushodaya Junction', 'MVP Colony Circle', 'Venkojipalem', 'Sagar Nagar', 'Rushikonda Beach Stop', 'GITAM University', 'IT SEZ (Rushikonda Hills)'],
    '900': ['Visakhapatnam Railway Station', 'Jagadamba Junction', 'Collector Office', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Maddilapalem', 'MVP Colony Circle', 'Sagar Nagar', 'Rushikonda Beach Stop', 'GITAM University', 'Mangamaripeta', 'Bheemunipatnam Bus Stand'],
    '28A': ['RK Beach', 'Pandurangapuram', 'Collector Office', 'Jagadamba Junction', 'RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'Kancharapalem', 'Marripalem', 'NAD Junction', 'Gopalapatnam', 'Simhachalam Foothills'],
    '28': ['RK Beach', 'Jagadamba Junction', 'RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'Kancharapalem', 'NAD Junction', 'Gopalapatnam', 'Vepagunta Junction', 'Sujatha Nagar', 'Chintalagraharam', 'Pendurthi Junction'],
    '28K': ['Town Kotharoad', 'Jagadamba Junction', 'RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'NAD Junction', 'Gopalapatnam', 'Simhachalam Foothills', 'Vepagunta Junction', 'Pendurthi Junction', 'Kothavalasa'],
    '38': ['Kurmannapalem Junction', 'Old Gajuwaka', 'Gajuwaka Junction', 'BHPV Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Marripalem', 'Urvasi Junction', 'Kancharapalem', 'Visakhapatnam Railway Station', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction'],
    '38K': ['Duvvada Railway Station', 'Kurmannapalem Junction', 'Old Gajuwaka', 'Gajuwaka Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Urvasi Junction', 'Gurudwara Junction', 'RTC Complex (Dwaraka Nagar)'],
    '38A': ['Steel Plant Township Sector 6', 'Steel Plant Main Gate', 'Kurmannapalem Junction', 'Gajuwaka Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Kancharapalem', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction'],
    '38H': ['Gajuwaka Junction', 'Sriharipuram', 'Coromandel Gate', 'Malkapuram', 'Scindia Junction', 'Naval Dockyard', 'Town Kotharoad', 'Jagadamba Junction', 'Collector Office', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Maddilapalem'],
    '500': ['RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'Kancharapalem', 'NAD Junction', 'Gopalapatnam', 'Vepagunta Junction', 'Sujatha Nagar', 'Pendurthi Junction', 'Anandapuram Junction'],
    '500A': ['Visakhapatnam Railway Station', 'RTC Complex (Dwaraka Nagar)', 'Kancharapalem', 'Urvasi Junction', 'NAD Junction', 'Gopalapatnam', 'Vepagunta Junction', 'Pendurthi Junction'],
    '500D': ['Maddilapalem', 'Satyam Junction', 'Gurudwara Junction', 'Kancharapalem', 'NAD Junction', 'Gopalapatnam', 'Vepagunta Junction', 'Sujatha Nagar', 'Pendurthi Junction'],
    '60': ['Simhachalam Foothills', 'Gopalapatnam', 'NAD Junction', 'Marripalem', 'Urvasi Junction', 'Kancharapalem', 'Visakhapatnam Railway Station', 'Collector Office', 'Jagadamba Junction', 'Town Kotharoad'],
    '60C': ['Simhachalam Foothills', 'Gopalapatnam', 'NAD Junction', 'Marripalem', 'Urvasi Junction', 'Kancharapalem', 'RTC Complex (Dwaraka Nagar)', 'Jagadamba Junction', 'Collector Office', 'RK Beach'],
    '10K': ['Town Kotharoad', 'Jagadamba Junction', 'Collector Office', 'RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'Marripalem', 'NAD Junction', 'Gopalapatnam'],
    '222': ['RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Maddilapalem', 'Venkojipalem', 'Hanumanthawaka Junction', 'Zoo Park Stop', 'Pothinamallayya Palem', 'ACA-VDCA Cricket Stadium', 'Car Shed Junction', 'Madhurawada', 'Kommadi Junction', 'Marikavalasa', 'Anandapuram Junction', 'Tagarapuvalasa'],
    '222V': ['Visakhapatnam Railway Station', 'RTC Complex (Dwaraka Nagar)', 'Siripuram Junction', 'Maddilapalem', 'Hanumanthawaka Junction', 'Pothinamallayya Palem', 'Car Shed Junction', 'Madhurawada', 'Kommadi Junction', 'Anandapuram Junction', 'Tagarapuvalasa'],
    '55': ['Scindia Junction', 'Malkapuram', 'Coromandel Gate', 'Sriharipuram', 'Gajuwaka Junction', 'Autonagar Gate', 'BHPV Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Gopalapatnam', 'Simhachalam Foothills'],
    '55K': ['Scindia Junction', 'Sriharipuram', 'Gajuwaka Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Gopalapatnam', 'Vepagunta Junction', 'Pendurthi Junction', 'Kothavalasa'],
    '68': ['RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'NAD Junction', 'Gopalapatnam', 'Vepagunta Junction', 'Pendurthi Junction', 'Sabbavaram Junction'],
    '88K': ['Maddilapalem', 'Siripuram Junction', 'RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'Kancharapalem', 'NAD Junction', 'Visakhapatnam Airport', 'Sheela Nagar', 'Gajuwaka Junction', 'Kurmannapalem Junction', 'Desapatrunipalem', 'Parawada Junction', 'NTPC Simhadri Gate', 'Atchutapuram'],
    '99K': ['Town Kotharoad', 'Jagadamba Junction', 'Collector Office', 'RK Beach', 'Pandurangapuram', 'Sagar Nagar', 'Rushikonda Beach Stop', 'GITAM University', 'IT SEZ (Rushikonda Hills)', 'Mangamaripeta', 'INS Kalinga', 'Bheemunipatnam Bus Stand'],
    '111': ['Kurmannapalem Junction', 'Old Gajuwaka', 'Gajuwaka Junction', 'Sheela Nagar', 'Visakhapatnam Airport', 'NAD Junction', 'Marripalem', 'Urvasi Junction', 'Gurudwara Junction', 'Satyam Junction', 'Maddilapalem', 'Venkojipalem', 'Hanumanthawaka Junction', 'Pothinamallayya Palem', 'ACA-VDCA Cricket Stadium', 'Car Shed Junction'],
    '211': ['Visakhapatnam Railway Station', 'RTC Complex (Dwaraka Nagar)', 'Gurudwara Junction', 'Satyam Junction', 'Seethammadhara', 'Venkojipalem', 'Hanumanthawaka Junction', 'Arilova / Health City'],
    '541': ['Maddilapalem', 'Satyam Junction', 'Gurudwara Junction', 'Marripalem', 'NAD Junction', 'Gopalapatnam', 'Vepagunta Junction', 'Sujatha Nagar', 'Chintalagraharam', 'Pendurthi Junction', 'Kothavalasa']
}

route_stops_data = []
for b_num, s_list in routes_stops_dict.items():
    for seq, s_name in enumerate(s_list, start=1):
        route_stops_data.append((b_num, seq, s_name, round(seq * 2.2, 1), seq * 4))

cursor.executemany("""
    INSERT INTO route_stops (bus_number, stop_sequence, stop_name, distance_km, eta_from_start_mins)
    VALUES (?, ?, ?, ?, ?)
""", route_stops_data)

# 3. Active Fleet Buses from Friend's DB
cursor.execute("DELETE FROM buses")
buses = [
    ("400K", "Gajuwaka Junction", "Maddilapalem", "NAD Junction", 17.7442, 83.2328, 3, 88, "Overcrowded", 12, 28, "Metro Express"),
    ("400K", "Gajuwaka Junction", "Maddilapalem", "Visakhapatnam Airport", 17.7285, 83.2245, 8, 42, "Comfortable", 15, 36, "Metro Express"),
    ("400K", "Gajuwaka Junction", "Maddilapalem", "Kancharapalem", 17.7315, 83.2790, 5, 76, "Overcrowded", 10, 30, "Metro Express"),
    ("400K", "Maddilapalem", "Gajuwaka Junction", "Siripuram Junction", 17.7205, 83.3182, 4, 35, "Comfortable", 14, 34, "Metro Express"),
    ("400K", "Maddilapalem", "Gajuwaka Junction", "Gurudwara Junction", 17.7348, 83.3015, 7, 60, "Moderate", 18, 31, "Metro Express"),
    ("400", "Kurmannapalem Junction", "Maddilapalem", "Gajuwaka Junction", 17.6868, 83.2185, 6, 30, "Comfortable", 15, 30, "City Ordinary"),
    ("400", "Kurmannapalem Junction", "Maddilapalem", "Sheela Nagar", 17.7120, 83.2180, 9, 52, "Moderate", 19, 29, "City Ordinary"),
    ("400H", "Steel Plant Main Gate", "Maddilapalem", "Kurmannapalem Junction", 17.6745, 83.1852, 5, 72, "Moderate", 20, 35, "Metro Express"),
    ("400H", "Steel Plant Main Gate", "Maddilapalem", "Visakhapatnam Railway Station", 17.7222, 83.2901, 4, 85, "Overcrowded", 16, 26, "Metro Express"),
    ("400Y", "Anakapalle RTC Complex", "RTC Complex (Dwaraka Nagar)", "Lankelapalem Junction", 17.6790, 83.1120, 9, 65, "Moderate", 22, 42, "Metro Express"),
    ("400Y", "Anakapalle RTC Complex", "RTC Complex (Dwaraka Nagar)", "NAD Junction", 17.7442, 83.2328, 3, 91, "Overcrowded", 15, 32, "Metro Express"),
    ("900K", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand", "Siripuram Junction", 17.7205, 83.3182, 4, 90, "Overcrowded", 12, 30, "Metro Express"),
    ("900K", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand", "Maddilapalem", 17.7368, 83.3205, 6, 62, "Moderate", 15, 35, "Metro Express"),
    ("900K", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand", "Rushikonda Beach Stop", 17.7819, 83.3852, 5, 38, "Comfortable", 18, 40, "Metro Express"),
    ("900K", "Bheemunipatnam Bus Stand", "RTC Complex (Dwaraka Nagar)", "Mangamaripeta", 17.8210, 83.4090, 8, 40, "Comfortable", 20, 38, "Metro Express"),
    ("900T", "RTC Complex (Dwaraka Nagar)", "IT SEZ (Rushikonda Hills)", "MVP Colony Circle", 17.7447, 83.3340, 5, 28, "Comfortable", 18, 34, "City Sheetal AC"),
    ("900T", "RTC Complex (Dwaraka Nagar)", "IT SEZ (Rushikonda Hills)", "Sagar Nagar", 17.7610, 83.3590, 7, 45, "Moderate", 22, 36, "City Sheetal AC"),
    ("900", "Visakhapatnam Railway Station", "Bheemunipatnam Bus Stand", "Jagadamba Junction", 17.7121, 83.3025, 4, 78, "Overcrowded", 16, 25, "City Ordinary"),
    ("28A", "RK Beach", "Simhachalam Foothills", "Jagadamba Junction", 17.7121, 83.3025, 3, 82, "Overcrowded", 12, 28, "Metro Express"),
    ("28A", "RK Beach", "Simhachalam Foothills", "NAD Junction", 17.7442, 83.2328, 6, 38, "Comfortable", 14, 34, "Metro Express"),
    ("28A", "Simhachalam Foothills", "RK Beach", "Gopalapatnam", 17.7524, 83.2188, 5, 48, "Moderate", 15, 32, "Metro Express"),
    ("28", "RK Beach", "Pendurthi Junction", "RTC Complex (Dwaraka Nagar)", 17.7244, 83.3063, 4, 79, "Overcrowded", 12, 26, "City Ordinary"),
    ("28", "Pendurthi Junction", "RK Beach", "Vepagunta Junction", 17.7680, 83.2110, 10, 50, "Moderate", 20, 35, "City Ordinary"),
    ("28K", "Town Kotharoad", "Kothavalasa", "Town Kotharoad", 17.6980, 83.2945, 6, 25, "Comfortable", 25, 28, "City Ordinary"),
    ("28K", "Town Kotharoad", "Kothavalasa", "Simhachalam Foothills", 17.7665, 83.2505, 8, 68, "Moderate", 25, 34, "City Ordinary"),
    ("38", "Kurmannapalem Junction", "Siripuram Junction", "Sheela Nagar", 17.7120, 83.2180, 5, 58, "Moderate", 12, 36, "Metro Express"),
    ("38", "Kurmannapalem Junction", "Siripuram Junction", "BHPV Junction", 17.7040, 83.2130, 7, 32, "Comfortable", 14, 38, "Metro Express"),
    ("38", "Siripuram Junction", "Kurmannapalem Junction", "Visakhapatnam Railway Station", 17.7222, 83.2901, 4, 84, "Overcrowded", 10, 27, "Metro Express"),
    ("38K", "Duvvada Railway Station", "RTC Complex (Dwaraka Nagar)", "Kurmannapalem Junction", 17.6745, 83.1852, 6, 40, "Comfortable", 15, 38, "Metro Express"),
    ("38K", "Duvvada Railway Station", "RTC Complex (Dwaraka Nagar)", "Gajuwaka Junction", 17.6868, 83.2185, 4, 75, "Overcrowded", 12, 30, "Metro Express"),
    ("38A", "Steel Plant Township Sector 6", "Siripuram Junction", "Steel Plant Main Gate", 17.6610, 83.1680, 5, 22, "Comfortable", 20, 35, "Metro Express"),
    ("38H", "Gajuwaka Junction", "Maddilapalem", "Scindia Junction", 17.6910, 83.2780, 7, 64, "Moderate", 18, 29, "City Ordinary"),
    ("38H", "Gajuwaka Junction", "Maddilapalem", "Town Kotharoad", 17.6980, 83.2945, 4, 86, "Overcrowded", 15, 24, "City Ordinary"),
    ("500", "RTC Complex (Dwaraka Nagar)", "Anandapuram Junction", "Gurudwara Junction", 17.7348, 83.3015, 6, 55, "Moderate", 18, 33, "Metro Express"),
    ("500", "RTC Complex (Dwaraka Nagar)", "Anandapuram Junction", "Pendurthi Junction", 17.8040, 83.2010, 8, 34, "Comfortable", 20, 40, "Metro Express"),
    ("500A", "Visakhapatnam Railway Station", "Pendurthi Junction", "Kancharapalem", 17.7315, 83.2790, 5, 70, "Moderate", 16, 30, "City Ordinary"),
    ("500D", "Maddilapalem", "Pendurthi Junction", "Satyam Junction", 17.7355, 83.3125, 4, 48, "Moderate", 15, 34, "Metro Express"),
    ("60", "Simhachalam Foothills", "Town Kotharoad", "Gopalapatnam", 17.7524, 83.2188, 3, 85, "Overcrowded", 12, 28, "City Ordinary"),
    ("60", "Simhachalam Foothills", "Town Kotharoad", "NAD Junction", 17.7442, 83.2328, 7, 38, "Comfortable", 15, 32, "City Ordinary"),
    ("60C", "Simhachalam Foothills", "RK Beach", "Marripalem", 17.7410, 83.2530, 6, 62, "Moderate", 18, 34, "Metro Express"),
    ("10K", "Town Kotharoad", "Gopalapatnam", "RTC Complex (Dwaraka Nagar)", 17.7244, 83.3063, 5, 68, "Moderate", 14, 28, "City Ordinary"),
    ("222", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Maddilapalem", 17.7368, 83.3205, 3, 84, "Overcrowded", 10, 32, "Metro Express"),
    ("222", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Hanumanthawaka Junction", 17.7556, 83.3315, 6, 50, "Moderate", 14, 38, "Metro Express"),
    ("222", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Madhurawada", 17.8165, 83.3585, 8, 28, "Comfortable", 18, 45, "Metro Express"),
    ("222V", "Visakhapatnam Railway Station", "Tagarapuvalasa", "RTC Complex (Dwaraka Nagar)", 17.7244, 83.3063, 5, 75, "Overcrowded", 20, 30, "City Ordinary"),
    ("55", "Scindia Junction", "Simhachalam Foothills", "Sriharipuram", 17.6810, 83.2410, 6, 60, "Moderate", 15, 32, "Metro Express"),
    ("55", "Scindia Junction", "Simhachalam Foothills", "NAD Junction", 17.7442, 83.2328, 4, 42, "Comfortable", 16, 35, "Metro Express"),
    ("55K", "Scindia Junction", "Kothavalasa", "Gajuwaka Junction", 17.6868, 83.2185, 10, 52, "Moderate", 25, 35, "City Ordinary"),
    ("68", "RTC Complex (Dwaraka Nagar)", "Sabbavaram Junction", "NAD Junction", 17.7442, 83.2328, 7, 72, "Moderate", 22, 34, "City Ordinary"),
    ("88K", "Maddilapalem", "Atchutapuram", "Gajuwaka Junction", 17.6868, 83.2185, 5, 89, "Overcrowded", 25, 38, "Metro Express"),
    ("88K", "Maddilapalem", "Atchutapuram", "Kurmannapalem Junction", 17.6745, 83.1852, 9, 45, "Moderate", 30, 42, "Metro Express"),
    ("99K", "Town Kotharoad", "Bheemunipatnam Bus Stand", "RK Beach", 17.7143, 83.3236, 6, 56, "Moderate", 18, 32, "City Ordinary"),
    ("99K", "Town Kotharoad", "Bheemunipatnam Bus Stand", "Rushikonda Beach Stop", 17.7819, 83.3852, 8, 35, "Comfortable", 22, 38, "City Ordinary"),
    ("111", "Kurmannapalem Junction", "Car Shed Junction", "Visakhapatnam Airport", 17.7285, 83.2245, 5, 66, "Moderate", 12, 36, "Metro Express"),
    ("111", "Kurmannapalem Junction", "Car Shed Junction", "Maddilapalem", 17.7368, 83.3205, 4, 80, "Overcrowded", 14, 32, "Metro Express"),
    ("211", "Visakhapatnam Railway Station", "Arilova / Health City", "Seethammadhara", 17.7420, 83.3110, 6, 44, "Comfortable", 16, 30, "City Ordinary"),
    ("541", "Maddilapalem", "Kothavalasa", "Gopalapatnam", 17.7524, 83.2188, 7, 58, "Moderate", 20, 36, "Metro Express")
]
cursor.executemany("""
    INSERT INTO buses
    (bus_number, source, destination, current_location, lat, lng, eta_minutes, crowd_percentage, crowd_status, next_bus_eta, speed_kmh, bus_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", buses)

# 4. Alternative Routes from Friend's DB
cursor.execute("DELETE FROM alternative_routes")
alt_routes = [
    ("Gajuwaka Junction", "Maddilapalem", "Connecting Bus", "Board Bus 38 to NAD Junction (5 mins away), then transfer to Metro Express 500D or 111 to Maddilapalem.", 35),
    ("Gajuwaka Junction", "Maddilapalem", "Shared Auto + Bus Combo", "Take Auto from Gajuwaka to Scindia (8 mins), board less-crowded Beach Bus 38H to Maddilapalem via Kotharoad.", 42),
    ("RTC Complex (Dwaraka Nagar)", "Rushikonda Beach Stop", "Auto + Bus Combo", "Take Shared Auto to MVP Colony (8 mins), then hop on Beach Bus 900T (AC / Less Crowded).", 25),
    ("RTC Complex (Dwaraka Nagar)", "Rushikonda Beach Stop", "Direct Metro Express", "Wait 10 mins for next Metro Express 900K departing Platform 4 directly along coastal road.", 28),
    ("Simhachalam Foothills", "RK Beach", "Connecting Bus", "Board Bus 55 or 60 to NAD Junction, transfer to City Direct 10K or 60C to RK Beach.", 40),
    ("Simhachalam Foothills", "RK Beach", "Fast Direct Metro", "Take Express 28A via Jagadamba directly to Submarine Museum (estimated 38 mins).", 38),
    ("Kurmannapalem Junction", "Siripuram Junction", "Cab + Express Bus", "Take Rapido / Auto to Gajuwaka Depot (5 mins), board Express 400K direct to Siripuram.", 36),
    ("NAD Junction", "Madhurawada", "Connecting BRTS", "Board Bus 400K or 38 to Maddilapalem BRTS, switch to 222 or 111 Express to Madhurawada.", 38),
    ("RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Express Bypass", "Take Bus 222 Non-Stop to Anandapuram, transfer to local auto to Tagarapuvalasa.", 45),
    ("Visakhapatnam Railway Station", "Rushikonda Beach Stop", "City Connection", "Board Bus 900 or take Auto to RTC Complex (6 mins), transfer to 900T Sheetal AC Bus.", 32)
]
cursor.executemany("""
    INSERT INTO alternative_routes (source, destination, option_type, route_details, total_time_mins)
    VALUES (?, ?, ?, ?, ?)
""", alt_routes)

# 5. Complaints from Friend's DB
complaints = [
    ("TICK-INIT01", "400K", "Bus skipped the NAD Junction stop during peak evening hours due to heavy crowd.", "Route / Stop Violation", "High", "Resolved"),
    ("TICK-INIT02", "900K", "AC was not functioning properly on Rushikonda Beach route bus during afternoon.", "Vehicle Maintenance", "Medium", "Open"),
    ("TICK-728D58", "400K", "Heavy rush and overcrowding at morning hours", "Overcrowding & Frequency", "Medium", "Open")
]
cursor.executemany("""
    INSERT OR IGNORE INTO complaints (ticket_id, bus_number, complaint_text, ai_category, ai_priority, status)
    VALUES (?, ?, ?, ?, ?, ?)
""", complaints)

conn.commit()
conn.close()
print("✓ Friend's database (69 stops, 29 routes, 57 active buses, 10 alternative routes) seeded into database/vizagbus.db!")
