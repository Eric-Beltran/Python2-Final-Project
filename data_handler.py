"""
Data access layer for users and student records.

When the CLI is running normally, this module forwards operations to the
remote API. When the API server is running, it talks directly to DynamoDB.
The rest of the project calls these functions instead of touching either
storage option directly.
"""

import random
import os
from student import StudentRecord

LAST_ERROR = None


def using_remote_api():
    return (
        os.environ.get("RUNNING_API_SERVER") != "1"
        and os.environ.get("USE_REMOTE_API", "1") == "1"
    )


def clear_last_error():
    global LAST_ERROR
    LAST_ERROR = None


def set_last_error(message):
    global LAST_ERROR
    LAST_ERROR = message


def get_last_error():
    return LAST_ERROR


if not using_remote_api():
    import boto3
    from boto3.dynamodb.conditions import Attr

    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-2"))
    users_table = dynamodb.Table("Users")
    students_table = dynamodb.Table("Students")


def error_message(error):
    if hasattr(error, "response"):
        return error.response.get("Error", {}).get("Message", str(error))
    return str(error)


def scan_all(table, **kwargs):
    items = []
    response = table.scan(**kwargs)
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            **kwargs
        )
        items.extend(response.get("Items", []))

    return items


def add_user(user):
    if using_remote_api():
        import api_client
        return api_client.add_user(user)

    clear_last_error()
    try:
        users_table.put_item(Item=user)
        return True
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error adding user: {message}")
        return False


def find_user_by(field, value):
    if using_remote_api():
        import api_client
        return api_client.find_user_by(field, value)

    clear_last_error()
    try:
        if field == "email":
            # Email is the partition key, so we can do a fast direct lookup
            response = users_table.get_item(Key={"email": value})
            return response.get("Item")
        else:
            # For any other field, we have to scan the whole table
            items = scan_all(
                users_table,
                FilterExpression=Attr(field).eq(value)
            )
            return items[0] if items else None
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error finding user: {message}")
        return None


def update_user(email, updated_data):
    if using_remote_api():
        import api_client
        return api_client.update_user(email, updated_data)

    if not updated_data:
        return True

    clear_last_error()
    try:
        # Build the UpdateExpression dynamically from whatever fields are passed in
        expr = "SET " + ", ".join(f"#k{i} = :v{i}" for i in range(len(updated_data)))
        names = {f"#k{i}": k for i, k in enumerate(updated_data.keys())}
        values = {f":v{i}": v for i, v in enumerate(updated_data.values())}

        users_table.update_item(
            Key={"email": email},
            UpdateExpression=expr,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
        )
        return True
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error updating user: {message}")
        return False


# ── Students ─────────────────────────────────────────────────────────────────

def delete_user(email):
    if using_remote_api():
        import api_client
        return api_client.delete_user(email)

    if not find_user_by("email", email):
        return False

    clear_last_error()
    try:
        users_table.delete_item(Key={"email": email})
        return True
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error deleting user: {message}")
        return False


def find_student_by(field, value):
    if using_remote_api():
        import api_client
        return api_client.find_student_by(field, value)

    clear_last_error()
    try:
        if field == "id":
            response = students_table.get_item(Key={"id": value})
            return response.get("Item")
        else:
            items = scan_all(
                students_table,
                FilterExpression=Attr(field).eq(value)
            )
            return items[0] if items else None
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error finding student: {message}")
        return None


def get_existing_student_ids():
    if using_remote_api():
        import api_client
        return api_client.get_existing_student_ids()

    clear_last_error()
    try:
        return {item["id"] for item in scan_all(students_table, ProjectionExpression="id")}
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error fetching IDs: {message}")
        return set()


def generate_student_id():
    existing_ids = get_existing_student_ids()
    while True:
        student_id = "700" + str(random.randint(100000, 999999))
        if student_id not in existing_ids:
            return student_id


def create_student_record(first_name, last_name, age, gender, phone, major="", grades=None, student_id=None):
    if student_id is None:
        student_id = generate_student_id()
    student = StudentRecord(
        student_id, first_name, last_name, int(age), gender, phone, major,
        grades if grades is not None else []
    )
    return student.to_dict()


def add_student(student):
    if using_remote_api():
        import api_client
        return api_client.add_student(student)

    if not student.get("id"):
        student["id"] = generate_student_id()

    if find_student_by("id", student["id"]):
        print("Error: A student with this ID already exists.")
        return False

    clear_last_error()
    try:
        students_table.put_item(Item=student)
        return True
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error adding student: {message}")
        return False


def update_student(student_id, updated_data):
    if using_remote_api():
        import api_client
        return api_client.update_student_direct(student_id, updated_data)

    if not updated_data:
        return True

    clear_last_error()
    try:
        expr = "SET " + ", ".join(f"#k{i} = :v{i}" for i in range(len(updated_data)))
        names = {f"#k{i}": k for i, k in enumerate(updated_data.keys())}
        values = {f":v{i}": v for i, v in enumerate(updated_data.values())}

        students_table.update_item(
            Key={"id": student_id},
            UpdateExpression=expr,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
        )
        return True
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error updating student: {message}")
        return False


def get_all_students():
    if using_remote_api():
        import api_client
        return api_client.get_all_students()

    clear_last_error()
    try:
        return scan_all(students_table)
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error fetching students: {message}")
        return []


def delete_student(student_id):
    if using_remote_api():
        import api_client
        return api_client.delete_student_direct(student_id)

    if not find_student_by("id", student_id):
        return False
    clear_last_error()
    try:
        students_table.delete_item(Key={"id": student_id})

        # Unlink any user connected to this student
        users = scan_all(users_table, FilterExpression=Attr("student_id").eq(student_id))
        for user in users:
            update_user(user["email"], {"student_id": None})

        return True
    except Exception as e:
        message = error_message(e)
        set_last_error(message)
        print(f"Error deleting student: {message}")
        return False


def link_user_to_student(email, student_id):
    if using_remote_api():
        import api_client
        return api_client.link_user_to_student(email, student_id)

    return update_user(email, {"student_id": student_id})
