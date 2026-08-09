from enum import IntEnum


class HttpStatusClass(IntEnum):
    SUCCESS = 2
    REDIRECT = 3
    CLIENT_ERROR = 4
    SERVER_ERROR = 5


def classify_status(status_code: int) -> HttpStatusClass:
    status_class = status_code // 100

    try:
        return HttpStatusClass(status_class)
    except ValueError:
        raise ValueError(f"Unsupported HTTP status code: {status_code}")


def is_success(status_code: int) -> bool:
    return classify_status(status_code) == HttpStatusClass.SUCCESS


def is_server_error(status_code: int) -> bool:
    return classify_status(status_code) == HttpStatusClass.SERVER_ERROR


def is_client_error(status_code: int) -> bool:
    return classify_status(status_code) == HttpStatusClass.CLIENT_ERROR
