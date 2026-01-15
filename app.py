import os
import subprocess
import webbrowser
from flask import Flask, jsonify

app = Flask(__name__)

ADK_WEB_PORT = 8000

# ------------------------
# Health check endpoint
# ------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ------------------------
# Launch ADK Web interface
# ------------------------
def launch_adk_web():
    """
    Launch the ADK Web interface on ADK_WEB_PORT.
    This runs in the background.
    """
    # Run 'adk web --port 8000' from the my_agent folder
    my_agent_dir = os.path.dirname(__file__)
    print(f"🚀 Launching ADK Web from {my_agent_dir} on port {ADK_WEB_PORT}...")

    # Start ADK Web in background
    process = subprocess.Popen(
        ["adk", "web", f"--port={ADK_WEB_PORT}"],
        cwd=my_agent_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Optionally open browser automatically
    try:
        webbrowser.open(f"http://localhost:{ADK_WEB_PORT}")
        print(f"🌐 ADK Web should open in your browser at http://localhost:{ADK_WEB_PORT}")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")

    return process

# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    # Launch ADK Web
    adk_process = launch_adk_web()

    # Start Flask app
    print("🔥 Starting Flask server on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

    # If Flask stops, terminate ADK Web
    adk_process.terminate()
    print("🛑 ADK Web stopped.")
