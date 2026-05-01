import base64
import datetime
import hashlib
import hmac
import json
import os
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from data_handler import (
    add_student,
    create_student_record,
    delete_student,
    find_student_by,
    get_all_students,
    update_student,
)
from user import login_user


SECRET = os.environ.get("API_SECRET", "dev-secret-change-me")


def to_jsonable(value):
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    return value


def make_token(user):
    payload = {
        "email": user["email"],
        "role": user["role"],
        "student_id": user.get("student_id"),
        "exp": int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2)).timestamp()),
    }
    payload_json = json.dumps(payload, separators=(",", ":")).encode()
    encoded_payload = base64.urlsafe_b64encode(payload_json).decode().rstrip("=")
    signature = hmac.new(SECRET.encode(), encoded_payload.encode(), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{encoded_payload}.{encoded_signature}"


def decode_token(token):
    if not token:
        return None

    try:
        encoded_payload, encoded_signature = token.split(".", 1)
        expected_signature = hmac.new(SECRET.encode(), encoded_payload.encode(), hashlib.sha256).digest()
        actual_signature = base64.urlsafe_b64decode(encoded_signature + "=" * (-len(encoded_signature) % 4))

        if not hmac.compare_digest(expected_signature, actual_signature):
            return None

        payload_json = base64.urlsafe_b64decode(encoded_payload + "=" * (-len(encoded_payload) % 4))
        payload = json.loads(payload_json)

        if payload.get("exp", 0) < int(datetime.datetime.now(datetime.UTC).timestamp()):
            return None

        return payload
    except (ValueError, json.JSONDecodeError, TypeError):
        return None


class ApiHandler(BaseHTTPRequestHandler):
    def send_json(self, status, body):
        response = json.dumps(to_jsonable(body)).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}

        try:
            return json.loads(self.rfile.read(length).decode())
        except json.JSONDecodeError:
            return None

    def current_user(self):
        auth_header = self.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        return decode_token(auth_header.removeprefix("Bearer ").strip())

    def require_admin(self):
        user = self.current_user()
        if not user:
            self.send_json(401, {"error": "Unauthorized"})
            return None
        if user.get("role") != "admin":
            self.send_json(403, {"error": "Admins only"})
            return None
        return user

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            self.send_json(200, {"status": "ok"})
            return

        if path == "/students":
            if not self.require_admin():
                return
            self.send_json(200, get_all_students())
            return

        if path.startswith("/students/"):
            student_id = path.split("/", 2)[2]
            user = self.current_user()
            if not user:
                self.send_json(401, {"error": "Unauthorized"})
                return
            if user.get("role") != "admin" and user.get("student_id") != student_id:
                self.send_json(403, {"error": "Forbidden"})
                return

            student = find_student_by("id", student_id)
            if not student:
                self.send_json(404, {"error": "Student not found"})
                return

            self.send_json(200, student)
            return

        self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        body = self.read_json()
        if body is None:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        if path == "/login":
            email = body.get("email", "").strip()
            password = body.get("password", "")
            if not email or not password:
                self.send_json(400, {"error": "Email and password are required"})
                return

            user = login_user(email, password)
            if not user:
                self.send_json(401, {"error": "Invalid credentials"})
                return

            self.send_json(200, {
                "token": make_token(user),
                "role": user["role"],
                "student_id": user.get("student_id"),
            })
            return

        if path == "/students":
            if not self.require_admin():
                return

            required_fields = ["first_name", "last_name", "age", "gender", "phone"]
            missing = [field for field in required_fields if not body.get(field)]
            if missing:
                self.send_json(400, {"error": f"Missing required fields: {', '.join(missing)}"})
                return

            try:
                student = create_student_record(
                    body["first_name"],
                    body["last_name"],
                    body["age"],
                    body["gender"],
                    body["phone"],
                    body.get("major", ""),
                    body.get("grades", []),
                )
            except (TypeError, ValueError):
                self.send_json(400, {"error": "Invalid student data"})
                return

            if not add_student(student):
                self.send_json(500, {"error": "Student could not be created"})
                return

            self.send_json(201, student)
            return

        self.send_json(404, {"error": "Not found"})

    def do_PUT(self):
        path = urlparse(self.path).path
        body = self.read_json()
        if body is None:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        if not path.startswith("/students/"):
            self.send_json(404, {"error": "Not found"})
            return

        if not self.require_admin():
            return

        student_id = path.split("/", 2)[2]
        if not find_student_by("id", student_id):
            self.send_json(404, {"error": "Student not found"})
            return

        allowed_fields = {"first_name", "last_name", "age", "gender", "phone", "major", "grades"}
        updates = {key: value for key, value in body.items() if key in allowed_fields}

        if "age" in updates:
            try:
                updates["age"] = int(updates["age"])
            except (TypeError, ValueError):
                self.send_json(400, {"error": "Age must be a number"})
                return

        if not updates:
            self.send_json(400, {"error": "No valid fields to update"})
            return

        if not update_student(student_id, updates):
            self.send_json(500, {"error": "Student could not be updated"})
            return

        self.send_json(200, find_student_by("id", student_id))

    def do_DELETE(self):
        path = urlparse(self.path).path
        if not path.startswith("/students/"):
            self.send_json(404, {"error": "Not found"})
            return

        if not self.require_admin():
            return

        student_id = path.split("/", 2)[2]
        if not delete_student(student_id):
            self.send_json(404, {"error": "Student not found or could not be deleted"})
            return

        self.send_json(200, {"status": "deleted"})


def run():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    server = HTTPServer((host, port), ApiHandler)
    print(f"API server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
