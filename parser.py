#!/usr/bin/python3

import argparse
from typing import List, Dict
from helpers import RED, YELLOW, END


class Parser:
    def __init__(self):
        self.github_link = "https://github.com/ablil/meistertask-cli"

        self.parser = argparse.ArgumentParser(
            prog="meistertask-cli",
            description="Meistertask command line tool",
            epilog="For more information check: {}".format(self.github_link),
        )

        self.__configure_parser()

    def __configure_parser(self):
        """Add necessary options to argument parser
        """

        # Project management args
        project_parser_group = self.parser.add_mutually_exclusive_group()

        project_parser_group.add_argument(
            "--list-projects",
            action="store_true",
            help="list all projects",
            dest="list_projects",
        )
        project_parser_group.add_argument(
            "--create-project",
            nargs=1,
            type=str,
            help="create new project",
            metavar="name",
            dest="create_project",
        )
        project_parser_group.add_argument(
            "--delete-project",
            action="store_true",
            help="delete existing project",
            dest="delete_project",
        )
        project_parser_group.add_argument(
            "--show-project",
            nargs=1,
            type=str,
            help="show detailed information about project",
            metavar="name",
            dest="read_project",
        )

        sections_group = self.parser.add_mutually_exclusive_group()
        sections_group.add_argument(
            "--open",
            action="store_true",
            help="show only open tasks (works with --show-project)",
            dest="open",
        )
        sections_group.add_argument(
            "--inprogress",
            action="store_true",
            help="show only tasks in progress (works with --show-project)",
            dest="inprogress",
        )
        sections_group.add_argument(
            "--done",
            action="store_true",
            help="show only tasks which are done (works with --show-project)",
            dest="done",
        )

        # task management
        tasks_parser_group = self.parser.add_mutually_exclusive_group()

        self.parser.add_argument(
            "--select-project",
            type=str,
            help="select a project",
            metavar="name",
            dest="project_name",
        )
        tasks_parser_group.add_argument(
            "--add-task",
            type=str,
            nargs=1,
            help="add new task to project",
            metavar="name",
            dest="create_task",
        )
        tasks_parser_group.add_argument(
            "--remove-task",
            action="store_true",
            help="remove task from project",
            dest="delete_task",
        )
        tasks_parser_group.add_argument(
            "--update-task",
            type=str,
            nargs=1,
            metavar="name",
            help="update task status",
            dest="update_task",
        )

    def get_user_input(self):
        """Parse arguments and return the user desired operation

        Return: 
            Dictionnary representing the project name, the task name, the operation,
            and andy addional data
        """

        user_input: Dict = {
            "project": False,
            "task": False,
            "operation": None,
            "data": dict(),
        }
        args = self.parser.parse_args()

        project_args = (
            args.list_projects,
            args.create_project,
            args.delete_project,
            args.read_project,
        )
        task_args = (
            args.project_name,
            args.create_task,
            args.delete_task,
            args.update_task,
        )

        if any(project_args) and any(task_args):
            self.parser.print_help()
            print(f"{RED}Project and Task operations can NOT be combined togother{END}")
            exit(1)

        elif any(project_args):
            user_input["project"] = True
            if args.list_projects:
                user_input["operation"] = "list"
            if args.create_project:
                user_input["operation"] = "create"
                user_input["data"]["project_name"] = str(args.create_project[0])
            if args.delete_project:
                user_input["operation"] = "delete"
            if args.read_project:
                user_input["operation"] = "read"
                user_input["data"]["project_name"] = str(args.read_project[0])

                # check if section is specified
                if args.open:
                    user_input["data"]["section"] = "open"
                if args.inprogress:
                    user_input["data"]["section"] = "inprogress"
                if args.done:
                    user_input["data"]["section"] = "done"

        elif any(task_args):
            user_input["task"] = True
            if not len(args.project_name):
                print(f"{RED}Project name must be specified for task management{END}")
                exit(1)
            else:
                user_input["data"]["project_name"] = str(args.project_name[0])

            if args.create_task:
                user_input["operation"] = "create"
                user_input["data"]["task_name"] = str(args.create_task[0])
            if args.delete_task:
                user_input["operation"] = "delete"
            if args.update_task:
                user_input["operation"] = "update"
                user_input["data"]["task_name"] = str(args.update_task[0])

        else:
            self.parser.print_help()
            exit(1)

        return user_input


if __name__ == "__main__":
    print("This moodule is intended to be included only")
