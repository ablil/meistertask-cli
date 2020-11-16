import argparse
from src.usage import PROJECT_USAGE, ROOT_USAGE, TASK_USAGE
from .project import ProjectParser
from .task import TaskParser


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="meistertask",
            description="A CLI tools for Meistertask",
            epilog=f"For more info: https://github.com/ablil/meistertaks-cli",
        )
        self.subparsers = self.parser.add_subparsers(
            title="Meistertask core commands",
            dest="command",
            metavar="command",
            help="[project, task]",
        )

        self.configure()

    def configure(self):
        self.projet_parser = ProjectParser(self.subparsers)
        self.projet_parser.configure()

        self.task_parser = TaskParser(self.subparsers)
        self.task_parser.configure()

    def parse_args(self):
        args = self.parser.parse_args()
        if not args.command:
            print(ROOT_USAGE)
            exit(1)

        if args.command.startswith("p") and not args.option:
            print(PROJECT_USAGE)
            exit(2)

        if args.command.startswith("t") and not args.option:
            print(TASK_USAGE)
            exit(3)
        return args