#!/usr/bin/python3

import requests
import json
import re
from typing import List, Dict
from helpers import RED, END


class API:
    def __init__(self, auth_key: str):
        self.auth_key = auth_key
        self.headers: Dict = {"Authorization": f"Bearer {self.auth_key}"}

    def get_projects(self, filter_keyword="active") -> List[Dict]:
        r = requests.get(
            "https://www.meistertask.com/api/projects",
            headers=self.headers,
            params={"status": str(filter_keyword).strip().lower()},
        )

        return r.json()

    def get_project(self, id: int) -> Dict:
        r = requests.get(
            f"https://www.meistertask.com/api/projects/{id}", headers=self.headers
        )

        return r.json()

    def create_project(self, name: str, description: str):
        r = requests.post(
            "https://www.meistertask.com/api/projects",
            headers=self.headers,
            data={"name": name, "notes": description},
        )

        return r.json()

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

        return r.json()

    def delete_project(self, id: int) -> Dict:
        r = requests.put(
            f"https://www.meistertask.com/api/projects/{id}",
            headers=self.headers,
            data={"status": 4},
        )

        return r.json()

    def archive_project(self, id: int) -> Dict:
        r = requests.put(
            f"https://www.meistertask.com/api/projects/{id}",
            headers=self.headers,
            data={"status": 5},
        )

        return r.json()

    def create_section(self, project_id: int, name: str) -> Dict:
        r = requests.post(
            f"https://www.meistertask.com/api/projects/{project_id}/sections",
            headers=self.headers,
            data={"name": str(name)},
        )

        return r.json()

    def get_tasks(self, project_id: int) -> List[Dict]:
        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/tasks",
            headers=self.headers,
        )

        return r.json()

    def add_task(self, section_id: int, name: str, description: str = ""):
        r = requests.post(
            f"https://www.meistertask.com/api/sections/{section_id}/tasks",
            headers=self.headers,
            data={"name": str(name), "notes": str(description)},
        )

        return r.json()

    def alter_task(self, task_id: int, section_id: int) -> Dict:

        r = requests.put(
            f"https://www.meistertask.com/api/tasks/{task_id}",
            headers=self.headers,
            data={"section_id": section_id},
        )

        return r.json()

    def _get_project_by_name(self, name: str) -> List:

        projects = self.get_projects()

        filtered_project: List[Dict] = list(
            filter(
                lambda project: re.match(
                    name.strip().lower(), project["name"].strip().lower()
                ),
                projects,
            )
        )

        return filtered_project

    def _get_section_by_project(self, project_id: int) -> List[Dict]:

        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/sections",
            headers=self.headers,
        )

        return r.json()

    def _get_task_by_name(self, project_id: int, name: str) -> List[Dict]:

        r = requests.get(
            f"https://www.meistertask.com/api/projects/{project_id}/tasks",
            headers=self.headers,
        )

        tasks: List[Dict] = r.json()

        filterd_tasks: List[Dict] = list(
            filter(
                lambda task: re.match(
                    name.strip().lower(), task["name"].strip().lower()
                ),
                tasks,
            )
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
