import requests
import time
import sqlite3
from datetime import datetime

URL = "https://api.agify.io?name=michael"

def init_db():
    conn = sqlite3.connect("results.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            timestamp TEXT,
            success INTEGER,
            latency REAL
        )
    """)
    conn.commit()
    conn.close()

def save_result(timestamp, success, latency):
    conn = sqlite3.connect("results.db")
    c = conn.cursor()
    c.execute("INSERT INTO results VALUES (?, ?, ?)",
              (timestamp, int(success), latency))
    conn.commit()
    conn.close()

def run_test():
    retries = 3

    for attempt in range(retries):
        try:
            start = time.time()
            response = requests.get(URL, timeout=5)
            latency = time.time() - start

            if response.status_code != 200:
                continue

            data = response.json()

            # Tests de contrat
            assert "name" in data
            assert "age" in data
            assert isinstance(data["age"], int)

            return True, latency

        except:
            time.sleep(1)

    return False, 0

if __name__ == "__main__":
    init_db()
    success, latency = run_test()
    timestamp = datetime.now().isoformat()
    save_result(timestamp, success, latency)
