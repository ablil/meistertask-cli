#!/usr/bin/python

import argparse

from .usage import ROOT_USAGE, PROJECT_USAGE, TASK_USAGE

class CustomParser:
    def __init__(self):
        self.parser = None 
        self.__configure_parser()

    def parse_args(self):
        args = self.parser.parse_args()
        if not args.command:
            print(ROOT_USAGE)
            exit(1)
        
        if args.command.startswith('p') and not args.option:
            print(PROJECT_USAGE)
            exit(2)

        if args.command.startswith('t') and not args.option:
            print(TASK_USAGE)
            exit(3)
        return args

    def __configure_parser(self):

        self.parser = argparse.ArgumentParser(
            prog='meistertask',
            description="A CLI tools for Meistertask",
            epilog=f"For more info check: https://github.com/ablil/meistertask-cli",
        )

        root_subparesers = self.parser.add_subparsers(
            title="Meistertask core commands",
            dest="command",
            metavar="command",
            help="[project, task]",
        )

        project_parser = root_subparesers.add_parser(
            "project",
            aliases=["p"],
            description="Manage projects",
        )
        task_parser = root_subparesers.add_parser(
            "task",
            aliases=["t"],
            description="Manage tasks of a specific project",
        )

        project_subparsers = project_parser.add_subparsers(
            title="Project commands",
            dest="option",
            metavar="[create, view, delete, archive, list]",
        )
        list_parser = project_subparsers.add_parser(
            "list", aliases=["l", "ls"], description="List project by their type"
        )
        list_group = list_parser.add_mutually_exclusive_group()
        list_group.add_argument(
            "-a",
            "--active",
            help="list active project",
            action="store_const",
            const="active",
            dest="type",
            default='active'
        )
        list_group.add_argument(
            "--all", help="list all project", action="store_const", const="all", dest="type"
        )
        list_group.add_argument(
            "--archived",
            help="list arvhied project",
            action="store_const",
            const="archived",
            dest="type",
        )

        create_parser = project_subparsers.add_parser(
            "create", aliases=["c"], description="Create new project"
        )
        create_parser.add_argument("name", help="project name")
        create_parser.add_argument("-d", "--description", help="project description")

        view_parser = project_subparsers.add_parser(
            "view", aliases=["v", "show", "display"], description="View project details"
        )
        view_parser.add_argument("name", help="project name")

        update_project = project_subparsers.add_parser(
            "update", aliases=['u', 'e', "edit"], description="Update project name or description"
        )
        update_project.add_argument("name", help="project name")
        

        delete_parser = project_subparsers.add_parser(
            "delete", aliases=["d", "rm", "del", "remove"], description="Delete a project"
        )
        delete_parser.add_argument("name", help="project name")

        archive_parser = project_subparsers.add_parser(
            "archive", description="Archive a projet"
        )
        archive_parser.add_argument("name", help="project name")

        task_subparsers = task_parser.add_subparsers(
            title="Task commands",
            dest="option",
            metavar="[create, list, update, delete, move]",
        )
        create_task = task_subparsers.add_parser(
            "create", aliases=["c"], description="Create new task"
        )
        create_task.add_argument("name", help="task name")
        create_task.add_argument("-d", "--description", help="task description")
        create_task.add_argument("project", help="project name")
        list_tasks = task_subparsers.add_parser(
            "list", aliases=["l", "ls"], description="List tasks by section"
        )
        list_tasks.add_argument("project", help="project name")
        list_task_group = list_tasks.add_mutually_exclusive_group(required=True)
        list_task_group.add_argument(
            "-a",
            "--all",
            action="store_const",
            const="all",
            dest="type",
            help="list all tasks",
        )
        list_task_group.add_argument(
            "-o",
            "--open",
            action="store_const",
            const="open",
            dest="type",
            help="list open tasks",
        )
        list_task_group.add_argument(
            "-i",
            "--inprogess",
            action="store_const",
            const="inprogess",
            dest="type",
            help="list inprogress tasks",
        )
        list_task_group.add_argument(
            "-d",
            "--done",
            action="store_const",
            const="done",
            dest="type",
            help="list cone tasks",
        )
        update_task = task_subparsers.add_parser(
            "update", aliases=['u', 'e', "edit"], description="Update task details"
        )
        update_task.add_argument("name", help="task name")
        update_task.add_argument("project", help="project name")
        
        move_task = task_subparsers.add_parser(
            "move", aliases=['m', "mv"], description="Move task to new section"
        )
        move_task.add_argument("name", help="task name")
        move_task.add_argument("section", choices=["open", "inprogess", "done"])
        move_task.add_argument("project", help="project name")


if __name__ == "__main__":
    
    parser = CustomParser()
    args = parser.parse_args()
    print(args)