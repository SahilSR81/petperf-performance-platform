from locust.clients import ResponseContextManager

from .request_context import RequestContext
from .retry import get_retry_policy


class ApiClient:
    def __init__(self, client):
        self.client = client
        self.context = RequestContext()

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
            headers=self.context.build_headers(),
            catch_response=catch_response,
        )
