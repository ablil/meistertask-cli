#!/usr/bin/python

ROOT_USAGE = """
USAGE:
    meistertask <command> <subcommand> [args/flags...]

CORE COMMANDS
    project:    Manage project
    task:       Manage tasks of specific project

CORE COMMANDS ALIASES:
    project:    p
    task:       t
"""


PROJECT_USAGE = """
USAGE:
    meistertask project <subcommand> [flags]

SUBCOMMANDS
    create:     Create project
    view:       View project
    delete:     Delete project
    list:       List projects (active, deleted, archived)

SUBCOMMANDS ALIASES:
    create:     c
    view:       v, show, display
    delete:     d, rm, del, remove
    list:       l, ls
"""

TASK_USAGE = """
USAGE:
    meistertask task <subcommand> [flags] <project name>

SUBCOMMANDS
    create:     Create taks
    list:       List tasks by section
    update:     Update task details
    move:       Move task to another section

SUBCOMMANDS ALIASES:
    create:     c
    list:       l, ls
    update:     u, e, edit
    move:       m, mv
"""
