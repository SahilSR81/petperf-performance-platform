from locust.clients import ResponseContextManager

from .retry import get_retry_policy


class ApiClient:
    def __init__(self, client):
        self.client = client

    def get(
        self,
        endpoint: str,
        *,
        params=None,
        name=None,
        catch_response=True,
    ) -> ResponseContextManager:
        policy = get_retry_policy()  # noqa: F841

        return self.client.get(
            endpoint,
            params=params,
            name=name,
            catch_response=catch_response,
        )
