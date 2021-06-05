"""
    Invoke Tasks
"""
import os
from invoke import task


def find_files(ext=None, exclude=None):
    """
    Helper to return file paths in root project dir given an extension.
    """
    cur_dir = os.getcwd()
    ext_files = []
    for file in os.listdir(cur_dir):
        if os.path.splitext(file)[1].lower() in ext and file not in exclude:
            file_path = os.path.join(cur_dir, file)
            ext_files.append(file_path)
    return ext_files


@task
def lint(ctx):
    """
    Task to run PyLint over all python files within the project.
    """
    print('Invoking :: PyLint :')
    py_files = find_files(ext=['.py'], exclude=[])
    ctx.run('python -m pylint ' + ' '.join(py_files))


@task
def check_flake(ctx):
    """
    Task to run Flak8 over all python files within the project.
    """
    print('Invoking :: Check Flake :')
    py_files = find_files(ext=['.py'], exclude=[])
    print('Checking : ' + ' '.join(py_files))
    ctx.run('python -m flake8 ' + ' '.join(py_files))


@task
def check_style(ctx):
    """
    Task to run PEP8 over all the python files within the project.
    """
    print('Invoking :: Check Style :')
    py_files = find_files(ext=['.py'], exclude=[])
    print('Checking : ' + ' '.join(py_files))
    ctx.run('python -m pycodestyle ' + ' '.join(py_files))


@task(check_style, check_flake)
def check(_):
    """
    Task to preform all check Tasks.
    """
    print('Invoking :: Check :')


@task()
def test(ctx):
    """
    Task to perform pytest executions.
    """
    print('Invoking :: PyTest :')
    ctx.run('python -m pytest')
