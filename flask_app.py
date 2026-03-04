from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    status = "OK"
    error_rate = 0.02
    avg_latency = 0.35
    p95_latency = 0.60
    results = [
        ("10:00", True, 0.30),
        ("10:05", True, 0.40),
        ("10:10", False, 0.90),
    ]

    return render_template(
        "dashboard.html",
        status=status,
        error_rate=error_rate,
        avg_latency=avg_latency,
        p95_latency=p95_latency,
        results=results
    )

if __name__ == "__main__":
    app.run()
