from flask import Flask, jsonify, render_template, request
import requests

class BackendAPIClient:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def get_tables(self):
        """Fetch the list of tables from the backend API."""
        try:
            response = requests.get(f"{self.backend_url}/api/tables")
            response.raise_for_status()
            return response.json()["message"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tables: {e}")
            return {"error": f"Error fetching tables: {e}"}

    def get_data(self, table_name):
        """Fetch data from the backend API for a specific table."""
        try:
            response = requests.post(f"{self.backend_url}/api/data", json={"table": table_name})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return {"error": f"Error fetching data: {e}"}