import requests
from typing import List, Dict

from .base import API
from .utils import catch_http_errors

class APIProject(API):
    def __init__(self, token: str):
        super().__init__(token)

    @catch_http_errors
    def project_fetch_all(self, filter_keyword="active") -> List[Dict]:
        r = requests.get(
            "https://www.meistertask.com/api/projects",
            headers=self.headers,
            params={"status": str(filter_keyword).strip().lower()},
        )
        
        if r.status_code != 200:
            print
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def project_fetch(self, id: int) -> Dict:
        r = requests.get(
            f"https://www.meistertask.com/api/projects/{id}", headers=self.headers
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def project_create(self, name: str, description: str):
        r = requests.post(
            "https://www.meistertask.com/api/projects",
            headers=self.headers,
            data={"name": name, "notes": description},
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def project_update(self, id: int, name: str = "", description: str = ""):

        data = dict()
        if len(name):
            data["name"] = name
        if len(description):
            data["notes"] = description

        r = requests.put(
            f"https://www.meistertask.com/api/projects/{id}",
            headers=self.headers,
            data=data,
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def project_delete(self, id: int) -> Dict:
        r = requests.put(
            f"https://www.meistertask.com/api/projects/{id}",
            headers=self.headers,
            data={"status": 4},
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()

    @catch_http_errors
    def project_archive(self, id: int) -> Dict:
        r = requests.put(
            f"https://www.meistertask.com/api/projects/{id}",
            headers=self.headers,
            data={"status": 5},
        )

        if r.status_code != 200:
            raise Exception(f'Failed to connect to API ({r.status_code})')
        return r.json()