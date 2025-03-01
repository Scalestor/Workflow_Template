from flask import Flask, jsonify, render_template, request
import os

from source.frontend.BackendAPIClient import  BackendAPIClient
from source.config.backend import backend_url
from source.config.webserver import frontend_host,frontend_port

class FrontendApp:
    def __init__(self, app_name, backend_url):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # This feels wrong
        template_folder = os.path.join(project_root, 'source','frontend','templates')
        static_folder = os.path.join(project_root, 'source','frontend','static')
        print(f"Template folder {template_folder}")
        print(f"Static folder {static_folder}")
        self.app = Flask(
            app_name,
            template_folder=template_folder,  # Set the correct path to templates
            static_folder=static_folder       # Set the correct path to static files
        )
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
            print(f"Initial home")
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

    def run(self, host=frontend_host, port=frontend_port):
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=True)


if __name__ == "__main__":   
    # Initialize the frontend Flask app
    app = FrontendApp("FrontendApp", backend_url)
    
    # Run the application
    app.run()
