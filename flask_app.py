from flask import Flask, render_template
import sqlite3
import statistics

app = Flask(__name__)

def get_results():
    conn = sqlite3.connect("results.db")
    c = conn.cursor()
    c.execute("SELECT * FROM results ORDER BY timestamp DESC LIMIT 50")
    results = c.fetchall()
    conn.close()
    return results

@app.route("/")
def dashboard():
    results = get_results()

    total = len(results)
    successes = sum(r[1] for r in results)
    latencies = [r[2] for r in results if r[2] > 0]

    error_rate = (total - successes) / total if total else 0
    avg_latency = statistics.mean(latencies) if latencies else 0
    p95_latency = statistics.quantiles(latencies, n=20)[-1] if len(latencies) > 1 else 0

    status = "OK" if error_rate < 0.2 else "FAIL"

    return render_template(
        "dashboard.html",
        results=results,
        error_rate=round(error_rate, 2),
        avg_latency=round(avg_latency, 3),
        p95_latency=round(p95_latency, 3),
        status=status
    )

@app.route("/health")
def health():
    return {"status": "healthy"}
