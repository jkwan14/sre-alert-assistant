from ai_helper import ai_helper
from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///alerts.db")


@app.route("/", methods=["GET", "POST"])
def home():
    """Show home page"""
    alert = None

    if request.method == "POST":
        alert = request.form.get("alert")
        if not alert:
            return render_template("index.html", alert="", error="Please enter an alert.")

        matches = db.execute("SELECT * FROM alerts WHERE alert = ?", alert)

        if not matches:
            ai_results = ai_helper(alert)
            if ai_results is None:
                return render_template("index.html", alert=alert, error="Alert not found in knowledge base and AI is unavailable.")
            source = "AI-generated"
            explanation = ai_results["explanation"]
            severity = ai_results["severity"]
            possible_causes = ai_results["possible_causes"]
            next_steps = ai_results["next_steps"]

            if isinstance(possible_causes, list):
                possible_causes = "\n".join(possible_causes)
            if isinstance(next_steps, list):
                next_steps = "\n".join(next_steps)

            db.execute("INSERT INTO alerts (alert, explanation, severity, possible_causes, next_steps, source) VALUES (?, ?, ?, ?, ?, ?)", alert, explanation, severity, possible_causes, next_steps, source)

            return render_template("index.html", alert=alert, explanation=explanation, severity=severity, possible_causes=possible_causes, next_steps=next_steps, source=source)

        explanation = matches[0]["explanation"]
        severity = matches[0]["severity"]
        possible_causes = matches[0]["possible_causes"]
        next_steps = matches[0]["next_steps"]
        source = f"Knowledge Base ({matches[0]['source']})"

        return render_template("index.html", alert=alert, explanation=explanation, severity=severity, possible_causes=possible_causes, next_steps=next_steps, source=source)

    return render_template("index.html", alert="")


@app.route("/add", methods=["GET", "POST"])
def add():
    """Add to knowledge base"""

    if request.method == "POST":
        source = "Manual"
        alert = request.form.get("alert")
        explanation = request.form.get("explanation")
        severity = request.form.get("severity")
        possible_causes = request.form.get("possible_causes")
        next_steps = request.form.get("next_steps")

        if not severity:
            return render_template("add.html", severity=severity, alert=alert, explanation=explanation, possible_causes=possible_causes, next_steps=next_steps, error="Please select the level of severity.")

        if not alert:
            return render_template("add.html", severity=severity, alert=alert, explanation=explanation, possible_causes=possible_causes, next_steps=next_steps, error="Please enter an alert.")

        if not explanation:
            return render_template("add.html", severity=severity, alert=alert, explanation=explanation, possible_causes=possible_causes, next_steps=next_steps, error="Please enter an explanation.")

        if not possible_causes:
            return render_template("add.html", severity=severity, alert=alert, explanation=explanation, possible_causes=possible_causes, next_steps=next_steps, error="Please enter possible causes.")
        if not next_steps:
            return render_template("add.html", severity=severity, alert=alert, explanation=explanation, possible_causes=possible_causes, next_steps=next_steps, error="Please enter next steps.")

        existing = db.execute("SELECT * FROM alerts WHERE alert = ?", alert)

        if existing:
            return render_template("add.html", severity=severity, alert=alert, explanation=explanation, possible_causes=possible_causes, next_steps=next_steps, error="Alert already exists in knowledge base.")

        db.execute("INSERT INTO alerts (alert, explanation, severity, possible_causes, next_steps, source) VALUES (?, ?, ?, ?, ?, ?)", alert, explanation, severity, possible_causes, next_steps, source)

        return redirect("/")

    return render_template("add.html")


@app.route("/knowledge_base", methods=["GET"])
def saved_alerts():
    """View alerts from knowledge base"""
    alerts = db.execute("SELECT * FROM alerts ORDER BY date_created DESC")
    return render_template("knowledge_base.html", alerts=alerts)
