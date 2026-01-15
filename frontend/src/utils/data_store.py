

from frontend.src.pydantic_classes.api.type_hierarchy import APIClient


class DataStore:
    def __init__(self, client):
        self.client: APIClient = client
        self.conversations = {}
        self.loaded_conversations = None
        self.friends = []
        self.friend_requests = []

