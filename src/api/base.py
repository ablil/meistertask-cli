from typing import Dict

RED = "\33[31m"
END = "\33[0m"

class API:
    def __init__(self, token: str):
        self.token = token
        self.headers: Dict = {"Authorization": f"Bearer {self.token}"}
