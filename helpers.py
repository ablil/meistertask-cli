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

        if len(tasks_by_section):
            print(
                "\t>{}Section:{}: {} ({}{} tasks{})".format(
                    PURPLE, END, section["name"], YELLOW, len(tasks_by_section), END
                )
            )
            for task in tasks_by_section:
                print(f"\t\t> {YELLOW}Task{END}: ", task["name"])
                print(f"\t\t> {YELLOW}Description{END}: ", task["notes"])
                print("")
            else:
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
            lambda section: re.match(
                section["name"].lower().strip(), name.lower().strip()
            ),
            sections,
        )
    )


def print_error_and_exit(*messages):

    for msg in messages:
        print(f"{RED} [-] {msg.capitalize()}{END}")

    exit(1)


def yes_or_no(message: str) -> bool:
    """Prompt use for confirmation"""
    while True:
        choice = str(input(f"{YELLOW}{message} [y/N]: {END}"))

        if choice.lower() in ("y", "yes"):
            return True
        if choice.lower() in ("n", "no"):
            return False


def match_names(name1: str, name2: str) -> bool:
    """Given two name, typically a project or task name. check if they are the same.
    First step: lowercase all letter and strip any leading whitespace then check equality.
    Second step: splits names by whitespace into two sets, and check if there is an intersection.
    Third step: chech matching using regular express wich has a low quality.

    Parameter:
        name1: First name to match
        name2: Second name to match
    Return:
        True if names matchs, otherwise False
    """
    name1 = name1.strip().lower()
    name2 = name2.strip().lower()

    if name1 == name2:
        return True

    words1: Set = set(name1.split(" "))
    words2: Set = set(name2.split(" "))

    if len(words1.intersection(words2)):
        return True

    if re.match(name1, name2):
        return True

    return False


if __name__ == "__main__":
    print("This module is indented to be incluced only")
