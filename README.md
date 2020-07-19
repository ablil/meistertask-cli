# Meistertask CLI

## What is meistertask-cli

Meistertask is a cloud-based project management tool, based on Kanban-style.
If you are familiar with Trello, then think of it the same way


## Why I build this ?

Once I discoved this platfrom from my tutor during an internship, I basically started using 
it on every project project I'm working on.

My problem was the Terminal, most of the time Im working on a terminal / IDE, so it became a pain in the ass for me to open a browser window, authenticate, make a chagne, add a task, create a project ...
So I thought why not build a terminal-based tool to save me time.
And here it is :smiely:

> **warning**: *Some of the features are not available because the official meistertask api does not support them yet.*

## Overview (demo)

[![asciicast](https://asciinema.org/a/348623.svg)](https://asciinema.org/a/348623)


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

Clone the project from github and run your meistertask-cli
```
> git clone https://github.com/ablil/meistertask-cli
> cd meistertask-cli
> python3 meistertask-cli --help
```
```
usage: meistertask-cli [-h]
                       [--list-projects | --create-project name | --delete-project | --show-project name]
                       [--select-project name]
                       [--add-task name | --remove-task | --update-task name]

Meistertask command line tool

optional arguments:
  -h, --help            show this help message and exit
  --list-projects       list all projects
  --create-project name
                        create new project
  --delete-project      delete existing project
  --show-project name   show detailed information about project
  --select-project name
                        select a project
  --add-task name       add new task to project
  --remove-task         remove task from project
  --update-task name    update task status

For more information check: https://github.com/ablil/meistertask-cli
```
You can typically perfom the following operations

* Create new project
    ```
    user@box#: python3 meistertask-cli.py --create-project 'my new project'
    Type project description (default: empty): lorem ipsum random text

    > Project Name:  my new project
    > Project Description:  lorem ipsum random text
    > Created at:  2020-07-20 16:11:11
    > Updated at:  2020-07-20 16:11:11
    [+] Project created Successfully
    ```

* Show a project in Details
    ```
    user@box#: python3 meistertask-cli --show-project 'bug-tracker'
    > Project Name:  bug-tracker
    > Project Description:  bug tracker for web developper and project managers
        > Section:  Open
            > Task:  registration ui
            > Description:  design and translate to html/css

            > Task:  reset password ui
            > Description:  design and translate to html/css

            > Task:  project structure
            > Description:  create project and setup dependencies

            > Task:  authentication
            > Description:  None

            > Task:  replace bootstrap with angular material
            > Description:  check attached link

            > Task:  make list of styles to use
            > Description:  fonts, color, overriding default angular material
    ....
    ```

* List all your projects:
    ```
    user@box#: python3 meistertask-cli.py --list-projects

    > Project Name:  College Attendance App
    > Project Description:  Android Project for School
    > Created at:  2020-03-20 01:26:13
    > Updated at:  2020-05-11 02:45:18

    > Project Name:  bug-tracker
    > Project Description:  bug tracker for web developper and project managers
    > Created at:  2020-07-08 10:46:22
    > Updated at:  2020-07-12 13:33:04

    > Project Name:  test project
    > Project Description:  descriton
    > Created at:  2020-07-19 19:59:23
    > Updated at:  2020-07-19 19:59:23
    ```

* Add new task
    ```
    user@box#: python3 meistertask-cli.py --select-project 'my new project' --add-task 'my first task'
    Type task description (default: empty): do some operation here
    [0] Open
    [1] In Progress
    [2] Done
    [?] Choose a section for your task (default: open): 

    > Task:  my first task
    > Description:  do some operation here
    > Section:  Open
    > Created:  2020-07-20 16:40:11
    [+] Task addedd successfully
    ```

* Move task to a new sections
    ```
    user@box#: python3 meistertask-cli.py --select-project 'my new project' --update-task 'my first task'
        [0] my first task (None)
        [1] my first task (this is the descriptions)
        [2] my first task (do some operation here)

    [?] Multiple tasks with the same name are found
    [?] Select a task: 2
    [0] Open
    [1] In Progress
    [2] Done
    [?] Choose a section for your task (default: open): 1

    > Task:  my first task
    > Description:  do some operation here
    > Section:  In Progress
    > Created:  2020-07-20 16:40:11
    [+] Task updated successfully
    ```

## Limitation

The following operation, even thougth they are included in the programm, but they are not yet suported the offical api.
The offcial api is in beta version, once a new feature is added, the meistertrask-cli will be updated as soon as possible.

    * delete project
    * delete task

## Contribution
Building this app is very easy, if you are familiar with the basic of python3 and API.

You can even build it from scratch yourself, or just fork this project and build on top of.

There are multiple features that need to be included, feel free to contribute, in fact I would love if you take a look and give me some feedback, open some issue/pull request.

Or contact me: ablil@pm.me

## Todo
- [ ] Colorful output
- [ ] Checklist support
- [ ] Comment tasks