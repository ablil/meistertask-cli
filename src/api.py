#!/usr/bin/python3

import requests
import json
import re
from typing import List, Dict, Set
from .utils import RED, END, match_names


def catch_http_errors(func):
    def wrapper(*args):
        try:
            return func(*args)
        except requests.exceptions.ConnectionError as e:
            print(f'{RED}It seems there is not internet connection{END}')
            exit()
        except Exception as e:
            print(e)
            exit()
    return wrapper

class API:
    def __init__(self, auth_key: str):
        self.auth_key = auth_key
        self.headers: Dict = {"Authorization": f"Bearer {self.auth_key}"}

    @catch_http_errors
    def get_projects(self, filter_keyword="active") -> List[Dict]:
        r = requests.get(
            "https://www.meistertask.com/api/projects",
            headers=self.headers,
            params={"status": str(filter_keyword).strip().lower()},
        )
        
        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def get_project(self, id: int) -> Dict:
        r = requests.get(
            f"https://www.meistertask.com/api/projects/{id}", headers=self.headers
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def create_project(self, name: str, description: str):
        r = requests.post(
            "https://www.meistertask.com/api/projects",
            headers=self.headers,
            data={"name": name, "notes": description},
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def update_project(self, id: int, name: str = "", description: str = ""):

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
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def delete_project(self, id: int) -> Dict:
        r = requests.put(
            f"https://www.meistertask.com/api/projects/{id}",
            headers=self.headers,
            data={"status": 4},
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def archive_project(self, id: int) -> Dict:
        r = requests.put(
            f"https://www.meistertask.com/api/projects/{id}",
            headers=self.headers,
            data={"status": 5},
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def create_section(self, project_id: int, name: str) -> Dict:
        r = requests.post(
            f"https://www.meistertask.com/api/projects/{project_id}/sections",
            headers=self.headers,
            data={"name": str(name)},
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def get_tasks(self, project_id: int) -> List[Dict]:
        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/tasks",
            headers=self.headers,
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def add_task(self, section_id: int, name: str, description: str = ""):
        r = requests.post(
            f"https://www.meistertask.com/api/sections/{section_id}/tasks",
            headers=self.headers,
            data={"name": str(name), "notes": str(description)},
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def update_task(self, id: int, name: str, description: str = ""):
        r = requests.put(
            f"https://www.meistertask.com/api/tasks/{id}",
            headers=self.headers,
            data={"name": str(name), "notes": str(description)},
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def move_task(self, task_id: int, section_id: int) -> Dict:

        r = requests.put(
            f"https://www.meistertask.com/api/tasks/{task_id}",
            headers=self.headers,
            data={"section_id": section_id},
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def _get_project_by_name(self, name: str) -> List:

        projects = self.get_projects()

        filtered_project: List[Dict] = list(
            filter(lambda project: match_names(name, project["name"]), projects,)
        )

        return filtered_project

    @catch_http_errors
    def _get_section_by_project(self, project_id: int) -> List[Dict]:

        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/sections",
            headers=self.headers,
        )

        if r.status_code != 200:
            raise Exception("Failed to connect to API")
        return r.json()

    @catch_http_errors
    def _get_task_by_name(self, project_id: int, name: str) -> List[Dict]:

        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/tasks",
            headers=self.headers,
        )

        tasks: List[Dict] = r.json()

        filterd_tasks: List[Dict] = list(
            filter(lambda task: match_names(name, task["name"]), tasks,)
        )

        return filterd_tasks

    @staticmethod
    def check_errors(msg: str, response: Dict):
        """Check if the reponse contains an errors.
            Exit when found.

        Parameters:
        msg: message to display if an error is found
        response: response object from the request call

        """

        if "errors" in response.keys():
            print(f"{RED} [-] {msg.capitalize()}{END}")
            print(f"{RED} Error: {END}", response["errors"][0]["message"])
            exit(1)


if __name__ == "__main__":

    print("This module is intended to be imported only")
