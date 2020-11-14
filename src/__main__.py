from .meistertask import Meistertask
from typing import List, Dict, Set  

from typing import Dict, List
from .parser import CustomParser
from .api import *

from .utils import CYAN, END
from .utils import (
    display_project,
    display_task,
    filter_sections_by_name,
    get_auth_key,
    filter_tasks_by_section,
    filter_sections_by_name,
)

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
            if len(filtered):
                for t in filtered:
                    display_task(t)
            else:
                print(f'{CYAN}No task with section {args.type} is found{END}')

        if args.option in ("m", "move", "mv"):
            project: Dict = meistertask.project_fetch(args.project)
            task: Dict = meistertask.task_fetch(args.name, project["id"])
            sections: List[Dict] = meistertask.section_fetch_all(project["id"])
            section: Dict = filter_sections_by_name(sections, args.section)
            meistertask.task_move(task["id"], section["id"])


if __name__ == "__main__":
    main()
