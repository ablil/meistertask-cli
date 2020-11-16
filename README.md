# Meistertask CLI

[![PyPI version](https://badge.fury.io/py/meistertask-cli.svg)](https://badge.fury.io/py/meistertask-cli)

## What is meistertask-cli

Meistertask is a cloud-based project management tool, based on Kanban-style.
If you are familiar with Trello, then think of it the same way

**Recent changelog**:
  * new arguement paser (easy to use).

## Why I build this ?

Once I discoved this platfrom from my tutor during an internship, I basically started using
it on every project project I'm working on.

My problem was the Terminal, most of the time Im working on a terminal / IDE, so it became a pain in the ass for me to open a browser window, authenticate, make a chagne, add a task, create a project ...
So I thought why not build a terminal-based tool to save me time.
And here it is :smiely:

> **warning**: *Some of the features are not available because the official meistertask api does not support them yet.*

## Overview 

[![asciicast](https://asciinema.org/a/373205.svg)](https://asciinema.org/a/373205)


## Requirement
First thing you need is python (obvious).

### GET Key
Second thing you need is an access token key, you can aquire one from the official link here:

[official api](https://www.mindmeister.com/api)

Scrool down to **Personal access tokens** and add new one.

Make sure to **select** all options, and **de-select** these two:

    * mindmeister.readonly
    * meistertask.readonly

### Add key to env variables

Third thing is adding your key to environment variable using the following command:

```> export MEISTERTASK='you auth key here'```

You can also that line to .bashrc to save you time.

## How to use ?

Install using pip
```
# install
pip install meistertask-cli

# Set authentication key
export MEISTERTASK=your-key-here

# Start using
meistertask --help
```

### Project help
```
USAGE:
    meistertask project <subcommand> [flags]

SUBCOMMANDS
    create:     Create project
    view:       View project
    update:     Update project name and description
    delete:     Delete project
    list:       List projects (active, deleted, archived)

SUBCOMMANDS ALIASES:
    create:     c
    view:       v, show, display
    update:     u, e, edit
    delete:     d, rm, del, remove
    list:       l, ls
```
### Tasks help
```
USAGE:
    meistertask task <subcommand> [flags] <project name>

SUBCOMMANDS
    create:     Create taks
    list:       List tasks by section
    update:     Update task name and description
    move:       Move task to another section

SUBCOMMANDS ALIASES:
    create:     c
    list:       l, ls
    update:     u, e, edit
    move:       m, mv
```

## Contribution
Building this app is very easy, if you are familiar with the basic of python3 and API.

You can even build it from scratch yourself, or just fork this project and build on top of.

There are multiple features that need to be included, feel free to contribute, in fact I would love if you take a look and give me some feedback, open some issue/pull request.

Or contact me: ablil@pm.me

## Todo
- [x] Colorful output
- [ ] Checklist support
- [ ] Comment tasks
- [ ] Edit project details
- [ ] Allow usage of project/task id insted if name