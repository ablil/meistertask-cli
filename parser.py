#!/usr/bin/python3

import argparse
from typing import List, Dict
from helpers import RED, YELLOW, END, print_error_and_exit


class Parser:
    """Wrapper around the command line parser"""

    def __init__(self):
        self.github_link = "https://github.com/ablil/meistertask-cli"

        self.parser = argparse.ArgumentParser(
            prog="meistertask-cli",
            description="Meistertask command line tool",
            epilog="For more information check: {}".format(self.github_link),
        )

        # subparsers
        self.project_parser: argparse.ArgumentParser = None
        self.task_parser: argparse.ArgumentParser = None

        self.__configure_parser()

    def __configure_parser(self):
        """Add necessary options to argument parser"""

        subparsers = self.parser.add_subparsers(
            title="meistertask-cli",
            description="The following are the supported sub-options: ",
        )

        self.__configure_projects_parser(subparsers)
        self.__configure_tasks_parser(subparsers)

    def __configure_projects_parser(self, subparsers):
        """Add projects options"""

        self.project_parser = subparsers.add_parser(
            "projects",
            description="Manage meistertask projects",
            epilog="For more information check: {}".format(self.github_link),
        )
        project_group = self.project_parser.add_mutually_exclusive_group()

        project_list = project_group.add_mutually_exclusive_group()
        project_list.add_argument(
            "-l",
            "--active",
            "--list-active",
            action="store_true",
            help="List active projects",
            dest="active_projects",
        )
        project_list.add_argument(
            "--archived",
            "--list-archived",
            action="store_true",
            help="List archived projects",
            dest="archived_projects",
        )
        project_list.add_argument(
            "--all",
            "--list-all",
            action="store_true",
            help="List all projects",
            dest="all_projects",
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
            "-u",
            "--update",
            "--update-project",
            nargs=1,
            type=str,
            help="Update project name/description",
            metavar="name",
            dest="update_project",
        )
        project_group.add_argument(
            "-d",
            "--delete",
            "--delete-project",
            nargs=1,
            type=str,
            help="Delete a project",
            metavar="name",
            dest="delete_project",
        )
        project_group.add_argument(
            "-a",
            "--archive",
            "--archive-project",
            nargs=1,
            type=str,
            help="Archive a project",
            metavar="name",
            dest="archive_project",
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

    def __configure_tasks_parser(self, subparsers):
        """ add task options"""

        self.task_parser = subparsers.add_parser(
            "tasks",
            description="Manage project tasks",
            epilog="For more information check: {}".format(self.github_link),
        )
        # Positionnal arguments
        self.task_parser.add_argument(
            "project_name",
            type=str,
            help="select a project for task operations",
            metavar="project_name",
        )

        # Optional arguments
        task_group = self.task_parser.add_mutually_exclusive_group(required=True)
        task_group.add_argument(
            "-a",
            "--add",
            "--add-task",
            type=str,
            nargs=1,
            help="Add task to project",
            metavar="task_name",
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
            "-m",
            "--move",
            "--move-task",
            type=str,
            nargs=1,
            metavar="task_name",
            help="Move task from one section to another",
            dest="move_task",
        )

        # listing taskk group
        list_tasks = task_group.add_mutually_exclusive_group()
        list_tasks.add_argument(
            "-l",
            "--list",
            "--list-all",
            action="store_true",
            help="List all tasks",
            dest="list_all",
        )
        list_tasks.add_argument(
            "--open", action="store_true", help="List open tasks", dest="list_open"
        )
        list_tasks.add_argument(
            "--inprogress",
            action="store_true",
            help="List in progress tasks",
            dest="list_inprogress",
        )
        list_tasks.add_argument(
            "--done", action="store_true", help="list done tasks", dest="list_done"
        )

    def parse_args(self):
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

        isProject = self.__parse_projects_args(args, user_input)
        isTask = self.__parse_tasks_args(args, user_input)

        # check if no options is specified
        if not any([isProject, isTask]):
            self.parser.print_help()

        return user_input

    def __parse_projects_args(self, args, user_input: Dict):
        """Parse project aguments

        Parameters:
        args: parsed args from command line (argsparse.parse_args())
        user_input: dictionary which store the parsed arguement

        Return:
        bool: true if projects arguemtn are parsed, else False
        """

        try:
            project_args = (
                args.active_projects,
                args.archived_projects,
                args.all_projects,
                args.create_project,
                args.update_project,
                args.delete_project,
                args.archive_project,
                args.read_project,
            )

            if any(project_args):
                user_input["project"] = True

                # Listing projects
                if any(
                    [args.active_projects, args.archived_projects, args.all_projects]
                ):
                    user_input["operation"] = "list"
                    user_input["data"]["list_filter"] = "active"

                    if args.archived_projects:
                        user_input["data"]["list_filter"] = "archived"
                    if args.all_projects:
                        user_input["data"]["list_filter"] = "all"

                if args.create_project:
                    user_input["operation"] = "create"
                    user_input["data"]["project_name"] = str(args.create_project[0])
                if args.update_project:
                    user_input["operation"] = "update"
                    user_input["data"]["project_name"] = str(args.update_project)
                if args.delete_project:
                    user_input["operation"] = "delete"
                    user_input["data"]["project_name"] = str(args.delete_project)
                if args.archive_project:
                    user_input["operation"] = "archive"
                    user_input["data"]["project_name"] = str(args.archive_project)
                if args.read_project:
                    user_input["operation"] = "read"
                    user_input["data"]["project_name"] = str(args.read_project[0])

                    # check if section is specified
                    if args.open:
                        user_input["data"]["section"] = "open"
                    if args.inprogress:
                        user_input["data"]["section"] = "in progress"
                    if args.done:
                        user_input["data"]["section"] = "done"

                return True
            else:
                self.project_parser.print_help()
                exit(1)
        except AttributeError:
            return False

    def __parse_tasks_args(self, args, user_input):
        """Parse project aguments

        Parameters:
        args: parsed args from command line (argsparse.parse_args())
        user_input: dictionary which store the parsed arguement

        Return:
        bool: true if arguemtn are parsed, else False
        """
        try:

            task_args = (
                args.project_name,
                args.create_task,
                args.delete_task,
                args.move_task,
                args.list_all,
                args.list_open,
                args.list_inprogress,
                args.list_done,
            )

            if any(task_args):
                user_input["task"] = True
                if not len(args.project_name):
                    print(
                        f"{RED}Project name must be specified for task management{END}"
                    )
                    exit(1)
                else:
                    user_input["data"]["project_name"] = str(args.project_name)

                if args.create_task:
                    user_input["operation"] = "create"
                    user_input["data"]["task_name"] = str(args.create_task[0])
                if args.delete_task:
                    user_input["operation"] = "delete"
                if args.move_task:
                    user_input["operation"] = "move"
                    user_input["data"]["task_name"] = str(args.move_task[0])

                # listing args
                if any(
                    [
                        args.list_all,
                        args.list_open,
                        args.list_done,
                        args.list_inprogress,
                    ]
                ):
                    user_input["operation"] = "list"
                if args.list_all:
                    user_input["data"]["list"] = "all"
                if args.list_open:
                    user_input["data"]["list"] = "open"
                if args.list_inprogress:
                    user_input["data"]["list"] = "in progress"
                if args.list_done:
                    user_input["data"]["list"] = "done"

                return True
            else:
                self.task_parser.print_help()
                exit(1)
        except AttributeError:
            return False


if __name__ == "__main__":
    print("This moodule is intended to be included only")
