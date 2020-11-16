

class ProjectParser:

    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.parser = self.subparsers.add_parser(
            "project",
            aliases=["p"],
            description="Manage projects",
        )

    def configure(self):

        project_subparsers = self.parser.add_subparsers(
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