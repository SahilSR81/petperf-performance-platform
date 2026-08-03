from locust.clients import ResponseContextManager


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
        return self.client.get(
            endpoint,
            params=params,
            name=name,
            catch_response=catch_response,
        )
