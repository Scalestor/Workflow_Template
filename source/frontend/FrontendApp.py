from flask import Flask, jsonify, render_template, request
import requests

import BackendAPIClient



class FrontendApp:
    def __init__(self, app_name, backend_url):
        self.app = Flask(app_name)
        self.backend_api_client = BackendAPIClient(backend_url)
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes."""
        @self.app.before_request
        def log_request():
            print(f"Incoming request: {request.method} {request.url}")

        @self.app.route("/")
        def home():
            # Fetch data from the backend API (GET request)
            tables = self.backend_api_client.get_tables()
            return render_template('index.html', data=tables)

        @self.app.route("/get-tables", methods=['GET'])
        def get_tables():
            tables = self.backend_api_client.get_tables()
            return jsonify(tables)

        @self.app.route("/get-data", methods=['POST'])
        def get_data():
            if request.method == "POST":
                request_payload = request.get_json()  # Get JSON data from request body
                table_name = request_payload.get('table')  # Extract 'table' field
                data_from_backend = self.backend_api_client.get_data(table_name)
                return jsonify(data_from_backend)

            return jsonify({"error": "This endpoint only accepts POST requests"}), 405

    def run(self, host="127.0.0.1", port=5000):
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    # Define the backend server URL (assumed to be running on localhost:5001)
    backend_url = 'http://localhost:5001'
    
    # Initialize the frontend Flask app
    app = FrontendApp("FrontendApp", backend_url)
    
    # Run the application
    app.run()
