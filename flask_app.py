from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import sqlite3

# On importe ton fichier run_test.py
from run_test import run_test, init_db, save_result

app = Flask(__name__)


# ===============================
# DASHBOARD
# ===============================
@app.route("/")
def dashboard():

    init_db()

    conn = sqlite3.connect("results.db")
    c = conn.cursor()
    c.execute("SELECT * FROM results ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()

    results = []

    for row in rows:
        timestamp, success, latency = row

        results.append({
            "name": f"Test à {timestamp}",
            "category": "Contrat",
            "status": "PASS" if success else "FAIL",
            "latency": round(latency * 1000, 2),  # conversion en ms
            "details": "OK" if success else "Erreur API"
        })

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")

    availability = round((passed / total) * 100, 2) if total > 0 else 0
    avg_latency = round(sum(r["latency"] for r in results) / total, 2) if total > 0 else 0

    sorted_latencies = sorted(r["latency"] for r in results)
    p95_latency = sorted_latencies[int(0.95 * (total - 1))] if total > 0 else 0

    last_run = rows[0][0] if rows else "Aucun test"

    return render_template(
        "dashboard.html",
        results=results,
        availability=availability,
        passed=passed,
        total=total,
        avg_latency=avg_latency,
        p95_latency=p95_latency,
        last_run=last_run
    )


# ===============================
# LANCER UN TEST
# ===============================
@app.route("/run-tests")
def run_tests():

    init_db()

    success, latency = run_test()
    timestamp = datetime.now().isoformat()

    save_result(timestamp, success, latency)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
