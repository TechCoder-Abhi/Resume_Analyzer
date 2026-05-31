import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv('ANALYSES_DB') or os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'analyses.db')
)


def init_db():
    # ensure the directory for the DB exists (useful when moving DB to backend/data/)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS analyses
                 (id INTEGER PRIMARY KEY, match_percentage REAL, matched TEXT, missing TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()


def save_analysis(match, matched_list, missing_list):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO analyses (match_percentage, matched, missing, timestamp) VALUES (?, ?, ?, ?)",
              (match, ','.join(matched_list), ','.join(missing_list), datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_all_analyses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM analyses ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    analyses = []
    for row in rows:
        analyses.append({
            'id': row[0],
            'match': row[1],
            'matched': row[2].split(',') if row[2] else [],
            'missing': row[3].split(',') if row[3] else [],
            'timestamp': row[4]
        })
    return analyses


def clear_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM analyses")
    conn.commit()
    conn.close()


def delete_analysis(analysis_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    conn.commit()
    conn.close()
