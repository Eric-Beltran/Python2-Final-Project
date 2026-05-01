import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode


API_BASE = os.environ.get("API_BASE", "http://3.131.90.50:5000").rstrip("/")
_token = None
LAST_ERROR = None


def set_last_error(message):
    global LAST_ERROR
    LAST_ERROR = message


def get_last_error():
    return LAST_ERROR


def request_json(method, path, data=None, token_required=False):
    body = None
    headers = {"Content-Type": "application/json"}
    set_last_error(None)

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
            data = json.loads(response_body) if response_body else None
        except json.JSONDecodeError:
            data = None

        if isinstance(data, dict) and data.get("error"):
            set_last_error(data["error"])
            print(f"API error: {data['error']}")
        else:
            set_last_error(f"API returned HTTP {error.code}")
            print(f"API returned HTTP {error.code}")

        return error.code, data
    except URLError as error:
        set_last_error(f"Could not reach API server at {API_BASE}: {error.reason}")
        print(f"Could not reach API server at {API_BASE}: {error.reason}")
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


def database_health_check():
    status, data = request_json("GET", "/health/db")
    return status == 200, data


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


def find_user_by(field, value):
    query = urlencode({"field": field, "value": value})
    status, data = request_json("GET", f"/data/users/find?{query}")
    return data.get("item") if status == 200 and data else None


def add_user(user):
    status, data = request_json("POST", "/data/users", user)
    return status == 201


def update_user(email, updated_data):
    status, data = request_json("PUT", f"/data/users/{quote(email, safe='')}", updated_data)
    return status == 200


def find_student_by(field, value):
    query = urlencode({"field": field, "value": value})
    status, data = request_json("GET", f"/data/students/find?{query}")
    return data.get("item") if status == 200 and data else None


def get_existing_student_ids():
    status, data = request_json("GET", "/data/students/ids")
    return set(data) if status == 200 and data else set()


def add_student(student):
    status, data = request_json("POST", "/data/students", student)
    return status == 201


def update_student_direct(student_id, updated_data):
    status, data = request_json("PUT", f"/data/students/{student_id}", updated_data)
    return status == 200


def get_all_students():
    status, data = request_json("GET", "/data/students")
    return data if status == 200 and data else []


def delete_student_direct(student_id):
    status, data = request_json("DELETE", f"/data/students/{student_id}")
    return status == 200


def link_user_to_student(email, student_id):
    return update_user(email, {"student_id": student_id})
