def is_success(response):
    return response.status_code == 200


def has_json_content(response):
    return response.headers.get("Content-Type", "").startswith("application/json")


def validate_status_code(response, expected):
    if response.status_code != expected:
        response.failure(f"Expected {expected}, got {response.status_code}")
    return response.status_code == expected
