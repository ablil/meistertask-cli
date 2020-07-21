#!/usr/bin/python3

from typing import Dict, List
import os
import re

GREEN = "\33[32m"
RED = "\33[31m"
YELLOW = "\33[33m"
CYAN = "\33[96m"
PURPLE = "\33[95m"
END = "\33[0m"


def format_datetime(datetime: str):
    date, time = datetime.split("T")

    return f"{date} {time.split('.')[0]}"


def display_project(project: Dict):
    print("")
    print(f"> {CYAN}Project Name{END}: ", project["name"])
    print(f"> {CYAN}Project Description{END}: ", project["notes"])
    print(f"> {CYAN}Created at{END}: ", format_datetime(project["created_at"]))
    print(f"> {CYAN}Updated at{END}: ", format_datetime(project["updated_at"]))


def display_task(task: Dict):
    print("")
    print(f"> {CYAN}Task{END}: ", task["name"])
    print(f"> {CYAN}Description{END}: ", task["notes"])
    print(f"> {CYAN}Section{END}: ", task["section_name"])
    print(f"> {CYAN}Created{END}: ", format_datetime(task["created_at"]))


def display_detailed_project(project: Dict, sections: List[Dict], tasks: List[Dict]):
    """Given a project, it's sections and tasks,
        group tasks by section and display them
    """

    # display project summary
    print(f"> {CYAN}Project Name{END}: ", project["name"])
    print(f"> {CYAN}Project Description{END}: ", project["notes"])

    # display tasks grouped by sections
    for section in sections:
        tasks_by_section: List[Dict] = list(
            filter(lambda task: task["section_id"] == section["id"], tasks)
        )

        print(f"\t> {PURPLE}Section{END}: ", section["name"])
        for task in tasks_by_section:
            print(f"\t\t> {YELLOW}Task{END}: ", task["name"])
            print(f"\t\t> {YELLOW}Description{END}: ", task["notes"])
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
        print(f"{RED}Authentication key is required{END}")
        print("For more info check: https://github.com/ablil/meistertask-cli")
        exit(1)


def filter_sections_by_name(sections: List[Dict], name: str) -> List:
    return list(
        filter(
            lambda section: re.match(section["name"].lower(), name.lower()), sections
        )
    )


if __name__ == "__main__":
    print("This module is indented to be incluced only")
