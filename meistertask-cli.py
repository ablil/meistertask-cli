#!/usr/bin/python3

from typing import Dict, List
from api import API
from parser import Parser
from helpers import *


class Meistertask:
    """ Core logic for meistertask-cli """

    def __init__(self, user_input: Dict, key: str):
        self.user_input = user_input
        self.auth_key = key
        self.api = API(self.auth_key)

    def run(self):

        ###############################
        # Project management
        ##############################
        if self.user_input["project"]:
            if self.user_input["operation"] == "list":
                projects = self.api.get_projects()
                for project in projects:
                    display_project(project)

            if self.user_input["operation"] == "create":

                project_name: str = self.user_input["data"]["project_name"]
                if len(project_name) < 5:
                    print(
                        f"[?] {RED}You must specifiy a valid project name (mandatory){END}"
                    )
                    print("[?] {RED}Project name must be at least 05 characters{END}")
                    exit(1)

                project_description = str(
                    input("Type project description (default: empty): ")
                )

                project: Dict = self.api.create_project(
                    project_name, project_description
                )

                if not "errors" in project.keys():
                    # add default sections: Open, In Progress, Done
                    self.api.create_section(project["id"], "Open")
                    self.api.create_section(project["id"], "In Progress")
                    self.api.create_section(project["id"], "Done")

                    display_project(project)
                    print(f"[+] {GREEN}Project created Successfully{END}")
                else:
                    print(f"[-] {RED}Failed to create project ,try again{END}")
                    print(f"[-] {RED}Error{END}: ", project["errors"][0]["message"])

            if self.user_input["operation"] == "delete":

                print(
                    f"[?] {YELLOW}Sorry this options is not available for the momemt{END}"
                )
                print(
                    f"[?] {YELLOW}You need to delete projects manually from the platform{END}"
                )
                exit(1)

            if self.user_input["operation"] == "read":

                project_name: str = self.user_input["data"]["project_name"]
                if not len(project_name):
                    print(f"[-] {RED}You must specify a project name{END}")
                    exit(1)

                projects: List[dict] = self.api._get_project_by_name(project_name)

                # select a project if multiple are found
                if len(projects) == 0:
                    print(f"[-] {YELLOW}No project is found{END}")
                elif len(projects) == 1:
                    project = projects[0]

                    sections: List[Dict] = self.api._get_section_by_project(
                        project["id"]
                    )

                    # if section filter is applied from the command args, apply
                    if "section" in self.user_input["data"].keys():
                        sections = filter_sections_by_name(
                            sections, self.user_input["data"]["section"]
                        )

                    tasks: List[Dict] = self.api.get_tasks(project["id"])

                    display_detailed_project(project, sections, tasks)
                else:

                    for i in range(len(projects)):
                        project: Dict = projects[i]
                        print("\t[{}] {}".format(i, project["name"]))
                    else:
                        print(
                            f"\n[?] {YELLOW}Multiple project with the same name are found{END}"
                        )

                    while True:
                        try:
                            choice = int(input("[?] Select a project: "))
                            if choice < len(projects) and choice >= 0:
                                break
                        except Exception:
                            print(f"{YELLOW}Select a valid project number{END}")

                    project: Dict = projects[choice]

                    sections: List[Dict] = self.api._get_section_by_project(
                        project["id"]
                    )
                    tasks: List[Dict] = self.api.get_tasks(project["id"])

                    display_detailed_project(project, sections, tasks)

        ###############################
        # Task management
        ##############################
        if self.user_input["task"]:

            projects: List[Dict] = self.api._get_project_by_name(
                self.user_input["data"]["project_name"]
            )
            project: Dict = None

            # select a project if multiple are found with the same name
            if len(projects) == 0:
                print(
                    f"[-] {RED}Not project is found, make sure to write the right name{END}"
                )
            elif len(projects) == 1:
                project = projects[0]
            else:
                for i in range(len(projects)):
                    project: Dict = projects[i]
                    print("\t[{}] {}".format(i, project["name"]))
                else:
                    print(
                        f"\n[?] {YELLOW}Multiple project with the same name are found{END}"
                    )

                while True:
                    try:
                        choice = int(input("[?] Select a project: "))
                        if choice < len(projects) and choice >= 0:
                            break
                    except Exception:
                        print(f"{YELLOW}Select a valid project number{END}")

                project: Dict = projects[choice]

            if self.user_input["operation"] == "create":
                task_name: str = str(self.user_input["data"]["task_name"])

                if len(task_name) < 5:
                    print(f"[?] {RED}Please spicify a valid task name{END}")
                    print(f"[?] {RED}Task name must be at least 5 characters long{END}")
                    exit(1)

                task_description: str = str(
                    input("Type task description (default: empty): ")
                )

                # choose a section from the project for the task(default: open)
                sections: List[Dict] = self.api._get_section_by_project(project["id"])

                for i in range(len(sections)):
                    print("[{}] {}".format(i, sections[i]["name"]))

                while True:
                    try:
                        choice = str(
                            input(
                                "[?] Choose a section for your task (default: open): "
                            )
                        )

                        choice = 0 if not len(choice) else int(choice)
                        break
                    except Exception:
                        print("Please select a valid choice")

                # add task
                section: Dict = sections[choice]

                task: Dict = self.api.add_task(
                    section["id"], task_name, task_description
                )

                if "errors" in task.keys():
                    print(f"[-] {RED}Failed to add task, Try again{END}")
                    print(
                        "[-] {}Error: {}{}".format(
                            RED, task["errors"][0]["message"], END
                        )
                    )
                    exit(1)
                else:
                    display_task(task)
                    print(f"[+] {GREEN}Task addedd successfully{END}")

            if self.user_input["operation"] == "delete":
                print(
                    f"{YELLOW}[?] Delete operation is not available for the moment{END}"
                )
                print("[?] For more info: https://github.com/ablil/meistertask-cli")
                exit(1)

            if self.user_input["operation"] == "update":
                task_name: str = self.user_input["data"]["task_name"]

                tasks: List[Dict] = self.api._get_task_by_name(project["id"], task_name)
                task: Dict = None

                # choice a task if multiple are found
                if len(tasks) == 0:
                    print(
                        f"[-] {RED}No Task is found, make sure to write the right name{END}"
                    )
                    exit(1)
                elif len(tasks) == 1:
                    task = tasks[0]
                else:
                    for i in range(len(tasks)):
                        task: Dict = tasks[i]
                        print("\t[{}] {} ({})".format(i, task["name"], task["notes"]))
                    else:
                        print("\n[?] Multiple tasks with the same name are found")

                    while True:
                        try:
                            choice = int(input("[?] Select a task: "))
                            if choice < len(tasks) and choice >= 0:
                                break
                        except Exception:
                            print("Select a valid task number")

                    task = tasks[choice]

                # move task to a specific section
                sections: List[Dict] = self.api._get_section_by_project(project["id"])
                section: Dict = None

                for i in range(len(sections)):
                    print("[{}] {}".format(i, sections[i]["name"]))

                while True:
                    try:
                        choice = str(
                            input(
                                "[?] Choose a section for your task (default: open): "
                            )
                        )

                        choice = 0 if not len(choice) else int(choice)
                        break
                    except Exception:
                        print("Please select a valid choice")

                section = sections[choice]

                task: Dict = self.api.alter_task(task["id"], section["id"])

                if "errors" in task.keys():
                    print(f"[-] {RED}Failed to update task{END}")
                    print(
                        "[-] {}Error: {}{}".format(
                            RED, task["errors"][0]["message"], END
                        )
                    )
                    exit(1)
                else:
                    display_task(task)
                    print(f"[+] {GREEN}Task updated successfully{END}")


def main():

    parser = Parser()
    user_input: Dict = parser.get_user_input()

    auth_key: str = get_auth_key()

    meistertask = Meistertask(user_input, auth_key)
    meistertask.run()


if __name__ == "__main__":
    main()
