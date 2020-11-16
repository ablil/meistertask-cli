import requests
from typing import List, Dict

from .base import API
from .utils import catch_http_errors

class APITask(API):

    def __init__(self, token: str):
        super().__init__(token)


    @catch_http_errors
    def task_fetch_all(self, project_id: int) -> List[Dict]:
        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/tasks",
            headers=self.headers,
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def task_create(self, section_id: int, name: str, description: str = ""):
        r = requests.post(
            f"https://www.meistertask.com/api/sections/{section_id}/tasks",
            headers=self.headers,
            data={"name": str(name), "notes": str(description)},
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def task_update(self, id: int, name: str, description: str = ""):
        r = requests.put(
            f"https://www.meistertask.com/api/tasks/{id}",
            headers=self.headers,
            data={"name": str(name), "notes": str(description)},
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def task_move(self, task_id: int, section_id: int) -> Dict:

        r = requests.put(
            f"https://www.meistertask.com/api/tasks/{task_id}",
            headers=self.headers,
            data={"section_id": section_id},
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()