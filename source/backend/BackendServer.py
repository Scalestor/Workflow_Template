from flask import Flask, request, jsonify
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import DatabaseRequestHandler,RequestHandler
from source.config import database

class BackendServer:
    def __init__(self, app_name, db_handler, request_handler):
        self.app = Flask(app_name)
        self.db_handler = db_handler
        self.request_handler = request_handler
        self.allowed_resources = ["data", "tables"]
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes."""
        @self.app.before_request
        def log_request():
            print(f"Incoming request: {request.method} {request.url} 'Args' {request.args} 'Data' {request.data}")

        @self.app.route('/api/<resource>', methods=["GET", "POST"])
        def handle_request(resource):
            if resource not in self.allowed_resources:
                return jsonify({"error": "Resource not found"}), 404

            if resource == "tables":
                return self.request_handler.handle_tables_request()

            if resource == "data":
                if request.method == "POST":
                    look_for_table = request.json.get("table")
                    if not look_for_table:
                        return jsonify({"error": "No table name provided in request."}), 400
                    return self.request_handler.handle_data_request(look_for_table)

            return jsonify({"error": "Method not allowed"}), 405

    def run(self, host="127.0.0.1", port=5001):
        """Run the Flask application."""
        self.app.run(host=host, port=port)


if __name__ == '__main__':
    # Initialize database handler with the connection string
    database_engine_string = database.database_engine_string
    db_handler = DatabaseRequestHandler(database_engine_string)

    # Initialize request handler with the database handler
    request_handler = RequestHandler(db_handler)

    # Initialize Flask app with handlers
    app = BackendServer("BackendApp", db_handler, request_handler)

    # Run the application
    app.run()        