#!/usr/bin/python3

from typing import Dict, List
from .api import API
from .parser import CustomParser
import requests

from .utils import select_one_project, select_one_section, select_one_task
from .utils import CYAN, GREEN, SUCCESS, ERROR, YELLOW, RED, PURPLE, YELLOW, END
from .utils import (
    display_project,
    display_task,
    match_names,
    display_detailed_project,
    filter_sections_by_name,
    get_auth_key,
    filter_tasks_by_section,
    filter_sections_by_name,
)


class Meistertask:
    """Core logic of app"""

    def __init__(self, token: str):
        self.token = token
        self.api = API(self.token)

    def project_create(self, name: str, description=""):
        """create new project

        Params:
        name: project name
        description: project description
        """
        if len(name) < 5:
            print(f"{RED}Project name must be at least 05 charcters{END}")
            exit(1)

        response: Dict = self.api.create_project(name, description)

        API.check_errors("Failed to create project", response)

        # add default sections: Open, In Progress, Done
        project_id: int = response["id"]
        self.api.create_section(project_id, "Open")
        self.api.create_section(project_id, "In Progress")
        self.api.create_section(project_id, "Done")

        display_project(response)
        print(f"[+] {SUCCESS}Project created Successfully{END}")

    def project_update(self, id: int, name: str, description=""):
        """update project name and description"""

        response: Dict = self.api.update_project(id, name, description)
        API.check_errors("failed to update project", response)

        display_project(response)
        print(f"{SUCCESS}[+] Project updated successfully{END}")

    def project_delete(self, id: int):
        """Delete project

        Params:
        id: project id
        """

        while True:
            try:
                choice = str(input("Do you want to delete this project [y/n]?"))
                if choice.lower() in ["y", "yes", "n", "no"]:
                    break
            except:
                print(f"{RED} Choose from [y, yes/n, no]{END}")

        if choice.lower() in ["y", "yes"]:
            response: Dict = self.api.delete_project(id)

            # check errors
            API.check_errors("failed to delete the project", response)

            # parse repsonse
            display_project(response)
            print(f"{SUCCESS} [+] Project is deleted successfully{END}")
        else:
            print(f"{RED}No project is deleted{END}")

    def project_archive(self, id: int):
        """Archive project

        Params
        id(int): project id
        """
        while True:
            try:
                choice = str(input("Do you want to archive this project [y/n] ?"))
                if choice.lower() in ["y", "yes", "no", "n"]:
                    break
                else:
                    raise ValueError("Invalid choice")
            except:
                print(f"{RED}Valid choices: [y, yes / n, no]{END}")

        if choice.lower() in ["y", "yes"]:

            response: Dict = self.api.archive_project(id)

            # check errors
            API.check_errors("failed to archive the project", response)

            # parse repsonse
            display_project(response)
            print(f"{SUCCESS} [+] Project is archived successfully{END}")
        else:
            print(f"{RED}No project is archvied !{END}")

    def project_view(self, id: int):
        """View project

        Parameters:
        id(int) project id
        """

        project: Dict = self.api.get_project(id)
        display_project(project)

    def project_fetch_all(self, type="active") -> List[Dict]:
        """Project all projects"""

        if type not in ("active", "archived", "all"):
            raise ValueError(f"Project type is invalid: {type}")

        projects: List[Dict] = self.api.get_projects(type)
        if not projects or not len(projects):
            print(f"{RED}No project is found{END}")
            exit(1)

        return projects

    def project_fetch(self, name: str) -> Dict:
        """Fetch project by name"""

        projects: List[Dict] = self.api.get_projects()
        if not projects or not len(projects):
            print(f"{RED}No project is found with name: {name}{END}")
            exit(1)

        matched: List = [p for p in projects if match_names(p["name"], name)]
        return select_one_project(matched)

    def task_create(self, name: str, project_id: int, description=""):
        """Create new task on specific project

        Params:
        name(str) task name
        project_id: project id
        description(str) task description
        """

        if len(name) < 5:
            print(f"{RED}Task name must be at least 05 characters{END}")
            exit(1)

        # choose a section from the project for the task(default: open)
        sections: List[Dict] = self.api._get_section_by_project(project_id)
        section: Dict = select_one_section(sections)

        response: Dict = self.api.add_task(section["id"], name, description)
        API.check_errors("failed to add task", response)
        display_task(response)
        print(f"[+] {SUCCESS}Task addedd successfully{END}")

    def task_update(self, id: int, name: str, description: str):
        """Update task name and description

        Params:
        id(int) task id
        name(str) new task name
        description(str) new task description
        """

        response: Dict = self.api.update_task(id, name, description)
        API.check_errors("failed to update project", response)
        display_task(response)
        print(f"{SUCCESS}[+] Task updated successfully{END}")

    def task_move(self, id: int, section_id: int):
        """Move task from one section to another

        Parameters:
        id(int) task id
        section_id(int) section id
        """

        response: Dict = self.api.move_task(id, section_id)
        API.check_errors("failed to move task", response)
        display_task(response)
        print(f"[+] {SUCCESS}Task moved successfully{END}")

    def task_fetch(self, name: str, project_id: str):
        """Fetch task from project by name"""

        tasks: List[Dict] = self.api.get_tasks(project_id)
        if not tasks or not len(tasks):
            print(f"{RED}No task is found in project{END}")
            exit(1)

        matched: List = [t for t in tasks if match_names(t["name"], name)]
        return select_one_task(matched)

    def task_fetch_all(self, project_id: int) -> List[Dict]:
        """Fetch all task in project"""

        tasks: List[Dict] = self.api.get_tasks(project_id)
        if not tasks or not len(tasks):
            print(f"{RED}No task is found in this project{END}")

        return tasks

    def section_fetch_all(self, id: int):
        """Fetch sections of projec

        Params:
        id(int) project id
        """

        sections: List[Dict] = self.api._get_section_by_project(id)
        if not sections or not len(sections):
            print(f"{RED}No section is found in this project{END}")
            exit(1)

        return sections


def main():
    token: str = get_auth_key()
    meistertask: Meistertask = Meistertask(token)

    parser: CustomParser = CustomParser()
    args = parser.parse_args()

    if args.command.startswith("p"):
        print(f"{CYAN}Project management{END}")

        if args.option in ("c", "create"):
            meistertask.project_create(args.name, args.description)

        if args.option in ("v", "show", "display", "view"):
            project: Dict = meistertask.project_fetch(args.name)
            display_project(project)

        if args.option in ("u", "update", "e", "edit"):
            project: Dict = meistertask.project_fetch(args.name)

            display_project(project)
            new_name = str(input("[?] Type new name (Enter to skip):"))
            new_description = str(input("[?] Type new description (Enter to skip):"))

            name = new_name if (new_name and len(new_name)) else project["name"]
            description = (
                new_description
                if (new_description and len(new_description))
                else project["description"]
            )

            meistertask.project_update(project['id'], name, description)

        if args.option in ("d", "delete", "r", "remove", "rm"):
            project: Dict = meistertask.project_fetch(args.name)
            display_project(project)
            meistertask.project_delete(project["id"])

        if args.option in ("l", "ls", "list"):
            projects: List[Dict] = meistertask.project_fetch_all(args.type)
            for p in projects:
                display_project(p)

    if args.command.startswith("t"):
        print(f"{CYAN}Task management{END}")

        if args.option in ("c", "create"):
            project: Dict = meistertask.project_fetch(args.project)

            description: str = args.description if args.description else ""
            meistertask.task_create(args.name, project["id"], description)

        if args.option in ("u", "update", "e", "edit"):
            project: Dict = meistertask.project_fetch(args.project)
            task: Dict = meistertask.task_fetch(args.name, project["id"])

            display_task(task)
            name: str = str(input("[?] Type name (Enter to skip):"))
            description: str = str(input("[?] Type description (Enter to skip): "))

            new_name = name if (name and len(name)) else task["name"]
            new_description = (
                description
                if (description and len(description))
                else task["description"]
            )

            meistertask.task_update(task["id"], new_name, new_description)

        if args.option in ("ls", "l", "list"):
            project: Dict = meistertask.project_fetch(args.project)
            tasks: List[Dict] = meistertask.task_fetch_all(project["id"])

            filtered = filter_tasks_by_section(tasks, args.type)
            for t in filtered:
                display_task(t)

        if args.option in ("m", "move", "mv"):
            project: Dict = meistertask.project_fetch(args.project)
            task: Dict = meistertask.task_fetch(args.name, project["id"])
            sections: List[Dict] = meistertask.section_fetch_all(project["id"])
            section: Dict = filter_sections_by_name(sections, args.section)
            meistertask.task_move(task["id"], section["id"])


if __name__ == "__main__":
    main()
