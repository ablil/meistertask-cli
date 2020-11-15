class TaskParser:
    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.parser = self.subparsers.add_parser(
            "task",
            aliases=["t"],
            description="Manage tasks of a specific project",
        )

    def configure(self):
        task_subparsers = self.parser.add_subparsers(
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
            "update", aliases=["u", "e", "edit"], description="Update task details"
        )
        update_task.add_argument("name", help="task name")
        update_task.add_argument("project", help="project name")

        move_task = task_subparsers.add_parser(
            "move", aliases=["m", "mv"], description="Move task to new section"
        )
        move_task.add_argument("name", help="task name")
        move_task.add_argument("section", choices=["open", "inprogess", "done"])
        move_task.add_argument("project", help="project name")