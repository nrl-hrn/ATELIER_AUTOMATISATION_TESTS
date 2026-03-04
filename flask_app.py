from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def dashboard():

    # Données simulées
    results = [
        {
            "name": "GET /latest - Status 200",
            "category": "Contrat",
            "status": "PASS",
            "latency": 78,
            "details": "OK"
        },
        {
            "name": "Content-Type JSON",
            "category": "Contrat",
            "status": "PASS",
            "latency": 67,
            "details": "application/json"
        },
        {
            "name": "Devise invalide",
            "category": "Robustesse",
            "status": "PASS",
            "latency": 120,
            "details": "404 attendu"
        }
    ]

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")

    availability = round((passed / total) * 100, 2)

    avg_latency = round(sum(r["latency"] for r in results) / total, 2)

    sorted_latencies = sorted(r["latency"] for r in results)
    p95_latency = sorted_latencies[int(0.95 * (total - 1))]

    last_run = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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


if __name__ == "__main__":
    app.run(debug=True)
