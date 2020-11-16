import requests
from typing import List, Dict

from .base import API
from .utils import catch_http_errors


class APISection(API):

    def __init__(self, token:str):
        super().__init__(token)

    @catch_http_errors
    def section_create(self, project_id: int, name: str) -> Dict:
        r = requests.post(
            f"https://www.meistertask.com/api/projects/{project_id}/sections",
            headers=self.headers,
            data={"name": str(name)},
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()




    @catch_http_errors
    def section_fetch_all(self, project_id: int) -> List[Dict]:

        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/sections",
            headers=self.headers,
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()
