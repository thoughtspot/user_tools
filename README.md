# ThoughtSpot User Tool

ThoughtSpot user tools are a collection of tools for managing users and groups in ThoughtSpot as well as working with 
the ThoughtSpot Web APIs that manage users and groups.  The tools and Web APIs are all written in Python and 
require a Python environment in which to run.  The remainder of this document will describe how to deploy and use 
the tools and how to write your own custom applications based on the API wrappers.

## Packages and scripts

The tools can be split into two broad categories.  The first are the scripts that you can run to directly do things.  
For example, the `get_usersy` script will let you get all of the users and groups from a running ThoughtSpot cluster.

The second category are the ThoughtSpot Web API Python wrappers.  These are all contained in the tsut package and 
categorized into modules based on functionality, such as writing sync applications, modeling users and groups and 
calling the APIs from Python scripts.

## Setup

This section will walk you through how to set up the environment to get started with the user tools.

### Environment

These tools have all been written in Python 3.7 and expect to be run in a 3.6 environment at a minimum.

You can either install directly into an existing Python environment, but it's better to run in an virtual environment 
to avoid conflicts with dependencies.  user_tools relies on other packages to run.  Note that this installation 
process requires external access to install packages and get the user_tools code from GitHub.

To create a virtual environment, you can run the following from the command prompt:

`$ virtualenv -p python3 ./venv`

Note that the `venv` folder can be whatever name and location you like (preferably external to a code repository).

Next, you need to activate the environment with the command: 

`$ source ./venv/bin/activate`

Note that you will need to reactivate the environment whenever you want to use it.  

You should see your prompt change to (venv) plus whatever it was before.  To verify the python version run:

`$ python --version`  You want to be on version 3.6 or higher.

If you want to leave the virtual environment, simple enter `$ deactivate` or close the terminal you are using.

See https://virtualenv.pypa.io/en/latest/ for more details on using virtualenv.

## Downloading and installing the user tools

Now that you have an environment for installing into you can install directly from GitHub with the command:

`$ pip install git+https://github.com/thoughtspot/user_tools`.  

You should see output as the user_tools and dependencies are installed.  

If you want or need to update to a newer version of the user tools, use the command:

`$ pip install --upgrade git+https://github.com/thoughtspot/user_tools`.  

## Running the pre-built tools

All of the pre-built tools are run using the general format: 

`python -m user_tools.<tool-name>`

Note there is no `.py` at the end and you *must* use `python -m`.  So for example to run `get_users` and see the 
options, you would enter `python -m user_tools.get_users --help`  Try it now and verify your environment is all set.

The user tools currently consist of four scripts:
1. `delete_ugs`, which deletes users and groups from a ThoughtSpot cluster.
2. `get_users` that can get users and groups from a ThoughtSpot cluster in multiple formats.
3. `sync_from_excel` that syncs ThoughtSpot from a properly formatted Excel document.  The format for the 
Excel document is the same as the one created by `get_users`.
4. `transfer_ownership` that transfers all of the objects owned by one one user to another.  Partial transfer of
ownership is not currently supported.

You might also notice a validate_json file that is a simple, command line validator or JSON.  Use if 
you like.

### delete_ugs

Deletes users and/or groups specified in either the flags or a file from a ThoughtSpot cluster.

~~~
usage: delete_ugs [-h] [--ts_url TS_URL] [--username USERNAME]
                     [--password PASSWORD] [--disable_ssl] [--users USERS]
                     [--groups GROUPS] [--user_file USER_FILE]
                     [--group_file GROUP_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --ts_url TS_URL       URL to ThoughtSpot, e.g. https://myserver
  --username USERNAME   Name of the user to log in as.
  --password PASSWORD   Password for login of the user to log in as.
  --disable_ssl         Will ignore SSL errors.
  --users USERS         List of user ids to delete.
  --groups GROUPS       List of group ids to delete.
  --user_file USER_FILE
                        File with list of user ids to delete.
  --group_file GROUP_FILE
                        File with list of group ids to delete.
~~~

### get_users

Retrieves all of the users and groups from a ThoughtSpot cluster and writes them to the output, a JSON file or Excel.

~~~
usage: get_users [-h] [--ts_url TS_URL] [--username USERNAME]
                    [--password PASSWORD] [--disable_ssl]
                    [--output_type OUTPUT_TYPE] [--filename FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  --ts_url TS_URL       URL to ThoughtSpot, e.g. https://myserver
  --username USERNAME   Name of the user to log in as.
  --password PASSWORD   Password for login of the user to log in as.
  --disable_ssl         Will ignore SSL errors.
  --output_type OUTPUT_TYPE
                        One of stdout, xls, excel, or json.
  --filename FILENAME   Name of file to write to if not stdout. Required for
                        Excel and JSON.
~~~

### sync_from_excel

Synchronized users and groups from an Excel document in the format created by `get_users` to a ThoughtSpot cluster.

~~~
usage: sync_from_excel [-h] [--filename FILENAME] [--ts_url TS_URL]
                          [--username USERNAME] [--password PASSWORD]
                          [--disable_ssl] [--remove_deleted] [--apply_changes]
                          [--batch_size BATCH_SIZE] [--merge_groups]

optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME   Name of file to write to.
  --ts_url TS_URL       URL to ThoughtSpot, e.g. https://myserver
  --username USERNAME   Name of the user to log in as.
  --password PASSWORD   Password for login of the user to log in as.
  --disable_ssl         Will ignore SSL errors.
  --remove_deleted      Will remove users not in the load. Cannot be used with
                        batch_size.
  --apply_changes       Will apply changes. Default is False for testing.
  --batch_size BATCH_SIZE
                        Loads the users in batches. Needed to avoid timeouts
                        for large groups of users.
  --merge_groups        Merge new groups with groups in ThoughtSpot.
~~~


### transfer_ownership

Transfers the ownership of all objects from one user to another in a ThoughtSpot cluster.

~~~
usage: transfer_ownership [-h] [--ts_url TS_URL] [--username USERNAME]
                             [--password PASSWORD] [--disable_ssl]
                             [--from_user FROM_USER] [--to_user TO_USER]

optional arguments:
  -h, --help            show this help message and exit
  --ts_url TS_URL       URL to ThoughtSpot, e.g. https://myserver
  --username USERNAME   Name of the user to log in as.
  --password PASSWORD   Password for login of the user to log in as.
  --disable_ssl         Will ignore SSL errors.
  --from_user FROM_USER
                        User to transfer ownership from.
  --to_user TO_USER     User to transfer ownership to.
~~~

## Writing Custom Scripts

While the pre-defined tools are convenient, they don't cover all possible scenarios.
See the [custom folder]("./custom/README.md") for details on how to write your own
sync script.
