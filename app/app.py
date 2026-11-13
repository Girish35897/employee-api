import os
from flask import Flask, jsonify

app = Flask(__name__)

# Dynamic configuration supporting environment variables and default fallbacks
PORT = int(os.getenv("PORT", 5000))
ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "development")
PLATFORM_TEAM = os.getenv("PLATFORM_TEAM", "Platform Engineering")
RELEASE_VERSION = os.getenv("RELEASE_VERSION","1.0.0")

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "application": "Enterprise Employee Management API",
        "version": RELEASE_VERSION,
        "environment": ENVIRONMENT_NAME,
        "status": "Running"
    })

@app.route("/employees", methods=["GET"])
def get_employees():
    dummy_employees = [
        {"employeeID": "EMP001", "employee_name": "Alice Smith", "department": "Data Science & AI"},
        {"employeeID": "EMP002", "employee_name": "Bob Jones", "department": "Platform Engineering"},
        {"employeeID": "EMP003", "employee_name": "Charlie Davis", "department": "Cloud Infrastructure"}
    ]
    return jsonify(dummy_employees)

@app.route("/health", methods=["GET"])
def health_check():
    # Kubernetes readiness and liveness probe endpoint
    return jsonify({"status": "healthy"}), 200

@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "environment name": ENVIRONMENT_NAME,
        "platform team details": PLATFORM_TEAM
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)