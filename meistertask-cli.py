#!/usr/bin/python3

from typing import Dict, List
from api import API
from parser import Parser
from helpers import *
import requests


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
            project: Dict = None

            if self.user_input["operation"] == "list":
                filter_keyword: str = self.user_input["data"]["list_filter"]
                projects = self.api.get_projects(filter_keyword)
                for project in projects:
                    display_project(project)
                else:
                    print(f"\n[+]{GREEN} Total projects: {END} {len(projects)}")
            else:
                # exract project
                project_name: str = self.user_input["data"]["project_name"]
                if not len(project_name):
                    print_error_and_exit("you must specify a project name")

                projects: Dict = self.api._get_project_by_name(project_name)
                project: Dict = self.__select_project_if_multiple(projects)

                # check if project is found
                if not project:
                    print_error_and_exit("project not found")

            if self.user_input["operation"] == "create":
                self._create_project(project)

            if self.user_input["operation"] == "update":
                self._update_project(project)

            if self.user_input["operation"] == "delete":
                self._delete_project(project)

            if self.user_input["operation"] == "archive":
                self._archive_project(project)

            if self.user_input["operation"] == "read":

                # check if filter option is passed
                filter_keyword: str = None
                if "section" in self.user_input["data"].keys():
                    filter_keyword = str(self.user_input["data"]["section"])

                self._show_project(project, filter_keyword)

        ###############################
        # Task management
        ##############################
        if self.user_input["task"]:

            # extract project first
            projects: List[Dict] = self.api._get_project_by_name(
                self.user_input["data"]["project_name"]
            )
            project: Dict = self.__select_project_if_multiple(projects)
            if not project:
                print_error_and_exit("project not found")

            if self.user_input["operation"] == "create":
                task_name: str = str(self.user_input["data"]["task_name"])
                self._add_task(task_name, project)

            if self.user_input["operation"] == "delete":
                print_error_and_exit(
                    "delete operation is not available for the moment",
                    "for mor info: https://github.com/ablil/meistertask-cli",
                )

            if self.user_input["operation"] == "move":
                task_name: str = self.user_input["data"]["task_name"]
                self._move_task(task_name, project)

            if self.user_input["operation"] == "list":
                self._show_project(project, self.user_input["data"]["list"])

    def _create_project(self, name: str):

        if len(name) < 5:
            print_error_and_exit(
                "you must specify a valid project name",
                "project name must be at least 05 characters",
            )

        description = str(input("Type project description (default: empty): "))

        response: Dict = self.api.create_project(name, description)

        API.check_errors("failed to create project", response)

        # add default sections: Open, In Progress, Done
        project_id: int = response["id"]
        self.api.create_section(project_id, "Open")
        self.api.create_section(project_id, "In Progress")
        self.api.create_section(project_id, "Done")

        display_project(response)
        print(f"[+] {GREEN}Project created Successfully{END}")

    def _update_project(self, project: Dict):
        """update project name and description"""

        if not project:
            print_error_and_exit("not project is found")
        else:
            display_project(project)

            new_name: str = str(
                input("Type project name (Leave empty to save previous name) : ")
            ).strip()
            new_description: str = str(
                input(
                    "Type project description (Leave empty to save privious description):\n"
                )
            ).strip()

            if not len(new_name) and not len(new_description):
                print(f"{CYAN} Nothing is updated{END}")
                exit(0)
            else:
                confirmation: bool = yes_or_no(
                    "are you sure you want to update the project"
                )

                if confirmation:
                    response: Dict = self.api.update_project(
                        project["id"], new_name, new_description
                    )
                    API.check_errors("failed to update project", response)

                    # display updated project
                    display_project(response)
                    print(f"{GREEN}[+] Project updated successfully{END}")

    def _delete_project(self, project: Dict):

        if not yes_or_no("do you want to delete this project"):
            print(f"{CYAN} No project is deleted{END}")
            return

        response: Dict = self.api.delete_project(project["id"])

        # check errors
        API.check_errors("failed to delete the project", response)

        # parse repsonse
        display_project(response)
        print(f"{GREEN} [+] Project is deleted successfully{END}")

    def _archive_project(self, project: Dict):

        if not project:
            print_error_and_exit("you must specify a project name")

        if not yes_or_no("do you want to archive this project"):
            print(f"{CYAN} No project is deleted{END}")
            return

        response: Dict = self.api.archive_project(project["id"])

        # check errors
        API.check_errors("failed to archive the project", response)

        # parse repsonse
        display_project(response)
        print(f"{GREEN} [+] Project is archived successfully{END}")

    def _show_project(self, project: None, keyword=None):
        """Show a proejct by name.
            Filter sections if keyword is passed

        Parameters:
        keyword: section filter keyword
        """

        if not project:
            print_error_and_exit("you must specify a project")

        if keyword == "all":
            # do not apply any filter
            keyword = None

        # get sections and tasks
        sections: List[Dict] = self.api._get_section_by_project(project["id"])
        tasks: List[Dict] = self.api.get_tasks(project["id"])

        # if section filter is applied from the command args, apply it
        if keyword:
            sections = filter_sections_by_name(sections, keyword)

        # display project
        display_detailed_project(project, sections, tasks)

    def _add_task(self, name: str, project: Dict):

        if len(name) < 5:
            print_error_and_exit(
                "please specify a valid task name",
                "task name must be at least 05 characters",
            )

        description: str = str(input("Type task description (default: empty): "))

        # choose a section from the project for the task(default: open)
        sections: List[Dict] = self.api._get_section_by_project(project["id"])
        section: Dict = self.__select_section_if_multipe(sections)

        response: Dict = self.api.add_task(section["id"], name, description)

        API.check_errors("failed to add task", response)

        display_task(response)
        print(f"[+] {GREEN}Task addedd successfully{END}")

    def _move_task(self, name: str, project: Dict):
        """Move task from one section to another

        Parameters:
        name: task name
        project: the project which the task belong to
        """

        # get task
        tasks: List[Dict] = self.api._get_task_by_name(project["id"], name)
        task: Dict = self.__select_task_if_multiple(tasks)

        # get section of choice
        sections: List[Dict] = self.api._get_section_by_project(project["id"])
        section: Dict = self.__select_section_if_multipe(sections)

        # update
        response: Dict = self.api.alter_task(task["id"], section["id"])

        API.check_errors("failed to update task", response)

        display_task(response)
        print(f"[+] {GREEN}Task updated successfully{END}")

    def __select_project_if_multiple(self, projects: List[Dict]) -> Dict:
        """Given a list of mulitple project, prompt the use to choose one
            Return: project
        """

        project: Dict = None

        if len(projects) == 0:
            return None
        elif len(projects) == 1:
            project = projects[0]
        else:

            # get selected project from user
            for i in range(len(projects)):
                project: Dict = projects[i]
                print("\t[{}] {}".format(i, project["name"]))

            print(f"\n[?] {YELLOW}Multiple project with the same name are found{END}")

            while True:
                try:
                    choice = int(input("[?] Select a project: "))
                    if choice < len(projects) and choice >= 0:
                        break
                except Exception:
                    print(f"{YELLOW}Select a valid project number{END}")

            project = projects[choice]

        return project

    def __select_section_if_multipe(self, sections: List[Dict], default=0) -> Dict:
        """Given a list of mulitple project, prompt the use to choose one
        if not section is select, the default value is choosed

        Parameters:
        sections: list of sections
        default: default section if no one is selected

        Return: section
        """

        choice: int = default

        for i in range(len(sections)):
            print("\t[{}] {}".format(i, sections[i]["name"]))

        while True:
            try:
                choice = str(
                    input("[?] Choose a section for your task (default: open): ")
                )

                choice = default if not len(choice) else int(choice)
                break
            except Exception:
                print("Please select a valid choice")

        return sections[choice]

    def __select_task_if_multiple(self, tasks: List[Dict]) -> Dict:
        """Given a list of tasks, prompt the use to choose one

        Returns:
        task choosed by the users
        """

        task: Dict = None

        if len(tasks) == 0:
            print_error_and_exit("no task is found, type the right name")
        elif len(tasks) == 1:
            task = tasks[0]
        else:
            for i in range(len(tasks)):
                task: Dict = tasks[i]
                print(
                    "\t[{}] {}: {}".format(
                        i,
                        task["name"],
                        task["notes"] if task["notes"] else "No Description",
                    )
                )
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

        return task


def main():

    parser = Parser()
    user_input: Dict = parser.parse_args()

    auth_key: str = get_auth_key()

    meistertask = Meistertask(user_input, auth_key)
    try:
        meistertask.run()
    except requests.exceptions.ConnectionError:
        print_error_and_exit("no internet connection")


if __name__ == "__main__":
    main()
