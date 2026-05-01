import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_BASE = os.environ.get("API_BASE", "http://localhost:5000").rstrip("/")
_token = None


def request_json(method, path, data=None, token_required=False):
    body = None
    headers = {"Content-Type": "application/json"}

    if token_required and _token:
        headers["Authorization"] = f"Bearer {_token}"

    if data is not None:
        body = json.dumps(data).encode()

    request = Request(f"{API_BASE}{path}", data=body, headers=headers, method=method)

    try:
        with urlopen(request, timeout=10) as response:
            response_body = response.read().decode()
            return response.status, json.loads(response_body) if response_body else None
    except HTTPError as error:
        response_body = error.read().decode()
        try:
            return error.code, json.loads(response_body) if response_body else None
        except json.JSONDecodeError:
            return error.code, None
    except URLError:
        return 0, None


def login(email, password):
    global _token
    status, data = request_json("POST", "/login", {"email": email, "password": password})

    if status != 200 or not data:
        return None

    _token = data["token"]
    return data


def health_check():
    status, data = request_json("GET", "/health")
    return status == 200 and data == {"status": "ok"}


def get_students():
    status, data = request_json("GET", "/students", token_required=True)
    return data if status == 200 else None


def get_student(student_id):
    status, data = request_json("GET", f"/students/{student_id}", token_required=True)
    return data if status == 200 else None


def create_student(student_data):
    status, data = request_json("POST", "/students", student_data, token_required=True)
    return data if status == 201 else None


def update_student(student_id, updated_data):
    status, data = request_json("PUT", f"/students/{student_id}", updated_data, token_required=True)
    return data if status == 200 else None


def delete_student(student_id):
    status, data = request_json("DELETE", f"/students/{student_id}", token_required=True)
    return status == 200
