def is_success(response):
    return response.status_code == 200


def has_json_content(response):
    return response.headers.get(
        "Content-Type",
        ""
    ).startswith("application/json")
