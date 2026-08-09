from contextlib import contextmanager
from typing import Iterator

from locust.clients import ResponseContextManager

from .http_status import is_client_error, is_server_error
from .request_context import RequestContext
from .retry import get_retry_policy


class ApiClient:
    def __init__(self, client):
        self.client = client
        self.context = RequestContext()

    @contextmanager
    def get(
        self,
        endpoint: str,
        *,
        params=None,
        name=None,
        catch_response=True,
    ) -> Iterator[ResponseContextManager]:
        policy = get_retry_policy()  # noqa: F841

        with self.client.get(
            endpoint,
            params=params,
            name=name,
            headers=self.context.build_headers(),
            catch_response=catch_response,
        ) as response:
            if is_server_error(response.status_code):
                response.failure("Server error")
            elif is_client_error(response.status_code):
                response.failure("Client error")

            yield response
