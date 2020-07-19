#!/usr/bin/python3

from typing import Dict, List
import os


def format_datetime(datetime: str):
    date, time = datetime.split("T")

    return f"{date} {time.split('.')[0]}"


def display_project(project: Dict):
    print("")
    print("> Project Name: ", project["name"])
    print("> Project Description: ", project["notes"])
    print("> Created at: ", format_datetime(project["created_at"]))
    print("> Updated at: ", format_datetime(project["updated_at"]))


def display_task(task: Dict):
    print("")
    print("> Task: ", task["name"])
    print("> Description: ", task["notes"])
    print("> Section: ", task["section_name"])
    print("> Created: ", format_datetime(task["created_at"]))


def display_detailed_project(project: Dict, sections: List[Dict], tasks: List[Dict]):
    """Given a project, it's sections and tasks,
        group tasks by section and display them
    """

    # display project summary
    print("> Project Name: ", project["name"])
    print("> Project Description: ", project["notes"])

    # display tasks grouped by sections
    for section in sections:
        tasks_by_section: List[Dict] = list(
            filter(lambda task: task["section_id"] == section["id"], tasks)
        )

        print("\t> Section: ", section["name"])
        for task in tasks_by_section:
            print("\t\t> Task: ", task["name"])
            print("\t\t> Description: ", task["notes"])
            print("")
        else:
            print("")
            print("")


def get_auth_key():
    """Read auth key from environment variable.
        Variable name: MEISTERTASK
    """
    try:
        return str(os.environ["MEISTERTASK"])
    except KeyError:
        print("Authentication key is required")
        print("For more info check: https://github.com/ablil/meistertask-cli")
        exit(1)


if __name__ == "__main__":
    print("This module is indented to be incluced only")
