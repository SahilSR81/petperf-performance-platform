from enum import Enum


class RequestName(str, Enum):
    GET_AVAILABLE_PETS = "GET Available Pets"
    GET_PET_BY_ID = "GET Pet By Id"
    CREATE_PET = "POST Create Pet"
    UPDATE_PET = "PUT Update Pet"
    DELETE_PET = "DELETE Pet"


def get_request_name(name: RequestName) -> str:
    return name.value


def build_dynamic_name(method: str, resource: str) -> str:
    return f"{method.upper()} {resource.title()}"


def is_valid_request_name(name: str) -> bool:
    return bool(name.strip())
