from flask import Flask, request, jsonify
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

class RequestHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def handle_tables_request(self):
        """Handle request for fetching available tables."""
        tables = self.db_handler.get_tables()
        if "error" in tables:
            return jsonify({"error": tables["error"]}), 500
        return jsonify({"message": tables})

    def handle_data_request(self, table_name):
        """Handle request for fetching data (e.g., row count) from a table."""
        # Check if the table exists
        tables = self.db_handler.get_tables()
        if table_name not in tables:
            return jsonify({"error": f"Table {table_name} not found."}), 404
        
        data_count = self.db_handler.get_table_data_count(table_name)
        if "error" in data_count:
            return jsonify({"error": data_count["error"]}), 500

        response = {
            "message": f"Data from query SELECT COUNT(*) FROM {table_name}",
            "data": data_count
        }
        return jsonify(response)