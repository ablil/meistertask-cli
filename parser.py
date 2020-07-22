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

        # subparser
        self.project_parser: argparse.ArgumentParser = None
        self.task_parser: argparse.ArgumentParser = None

        self.__configure_parser()

    def __configure_parser(self):
        """Add necessary options to argument parser
        """

        subparsers = self.parser.add_subparsers(
            title="meistertask-cli",
            description="The following are the supported sub-options: ",
        )

        # Project management args
        self.project_parser = subparsers.add_parser(
            "projects",
            description="Manage meistertask projects",
            epilog="For more information check: {}".format(self.github_link),
        )
        project_group = self.project_parser.add_mutually_exclusive_group()

        project_group.add_argument(
            "-l",
            "--list",
            "--list-projects",
            action="store_true",
            help="List all active projects",
            dest="list_projects",
        )
        project_group.add_argument(
            "-c",
            "--create",
            "--create-project,",
            nargs=1,
            type=str,
            help="Create new project",
            metavar="name",
            dest="create_project",
        )
        project_group.add_argument(
            "-d",
            "--delete",
            "--delete-project",
            nargs=1,
            type=str,
            help="Delete a project",
            metavar='name',
            dest="delete_project",
        )
        self.project_parser.add_argument(
            "-s",
            "--show",
            "--show-project",
            nargs=1,
            type=str,
            help="Show project in details",
            metavar="name",
            dest="read_project",
        )

        sections_group = project_group.add_mutually_exclusive_group()
        sections_group.add_argument(
            "--open",
            action="store_true",
            help="Show only open tasks (works with --show)",
            dest="open",
        )
        sections_group.add_argument(
            "--inprogress",
            action="store_true",
            help="Show only tasks in progress (works with --show)",
            dest="inprogress",
        )
        sections_group.add_argument(
            "--done",
            action="store_true",
            help="Show only tasks which are done (works with --show)",
            dest="done",
        )

        # task management
        self.task_parser = subparsers.add_parser(
            "tasks",
            description="Manage project tasks",
            epilog="For more information check: {}".format(self.github_link),
        )
        task_group = self.task_parser.add_mutually_exclusive_group()

        self.task_parser.add_argument(
            "-s",
            "--select",
            "--select-project",
            type=str,
            help="Select project (For tasks operations, project is needed)",
            metavar="name",
            dest="project_name",
            required=True,
        )
        task_group.add_argument(
            "-a",
            "--add",
            "--add-task",
            type=str,
            nargs=1,
            help="Add task to project",
            metavar="name",
            dest="create_task",
        )
        task_group.add_argument(
            "-r",
            "--remove",
            "--remove-task",
            action="store_true",
            help="Remove task from project",
            dest="delete_task",
        )
        task_group.add_argument(
            "-u",
            "--update",
            "--update-task",
            type=str,
            nargs=1,
            metavar="name",
            help="Update task",
            dest="update_task",
        )

    def get_user_input(self):
        """Parse arguments and return the user desired operation

        Return: 
            Dictionnary representing the project name, the task name, the operation,
            and andy addional data
        """
        isProjectArgs = False
        isTaskArgs = False

        user_input: Dict = {
            "project": False,
            "task": False,
            "operation": None,
            "data": dict(),
        }
        args = self.parser.parse_args()

        # parse projects arguments if present
        try:
            project_args = (
                args.list_projects,
                args.create_project,
                args.delete_project,
                args.read_project,
            )

            if any(project_args):
                user_input["project"] = True

                if args.list_projects:
                    user_input["operation"] = "list"
                if args.create_project:
                    user_input["operation"] = "create"
                    user_input["data"]["project_name"] = str(args.create_project[0])
                if args.delete_project:
                    user_input["operation"] = "delete"
                    user_input["data"]["project_name"] = str(args.delete_project)
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

                isProjectArgs = True
            else:
                self.project_parser.print_help()
                exit(1)
        except AttributeError:
            pass

        # parse task arguments if present
        try:

            task_args = (
                args.project_name,
                args.create_task,
                args.delete_task,
                args.update_task,
            )

            if any(task_args):
                user_input["task"] = True
                if not len(args.project_name):
                    print(
                        f"{RED}Project name must be specified for task management{END}"
                    )
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

                isTaskArgs = True
            else:
                self.task_parser.print_help()
                exit(1)
        except AttributeError:
            pass

        # check if no options is specified
        if (not isProjectArgs) and (not isTaskArgs):
            self.parser.print_help()

        return user_input


if __name__ == "__main__":
    print("This moodule is intended to be included only")
