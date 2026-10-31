import sqlite3
import os

def resolve_db_path() -> str:
    # 1. Check if DB_PATH environment variable is provided
    if os.environ.get("DB_PATH"):
        return os.path.abspath(os.environ["DB_PATH"])
    
    # 2. Check if database exists in database/ directory (monorepo local dev)
    repo_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/vizagbus.db"))
    if os.path.exists(repo_db):
        return repo_db
    
    # 3. Default to backend/vizagbus.db (production / Render container)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "vizagbus.db"))

DB_PATH = resolve_db_path()

def get_db():
    from seed import init_db
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
