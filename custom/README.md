# Writing Custom Sync Scripts

# Overview

This file covers how to create new, custom syncronizations if none of the existing tools meet your needs.  

Most synchronizations require reading user/group information from a location and then writing the users
and groups to some other location.  For example, you might read the information from a database and then
write to ThoughtSpot.  Or you might read from ThoughtSpot and write to a file.  All of these scenarios 
are supported with a couple simple classes.  

An example is provided called `user_tools_example.py` that you can reference along with the instructions below.

## Parts of a custom sync script

To write a sync script, you need three things:

1. A reader class that is derived from `tsut.apps.TSUGReader` or one of it's subclasses.
2. One or more writer classes that are derived from `tsut.apps.TSUGWriter` or one of it's subclasses.
3. A `tsut.apps.TSUserGroupSyncApp` class.  You should rarely need to create a new application class.

### Readers

The primary goal of a reader is to read users and groups from some location and then return a 
`tsut.model.UsersAndGroups` object.  The reader has three methods:

1. An `__init__` method that does instance initialization, identifies required command line arguments and
calls `__init__` on the parent class.
2. An `add_parser_args` method that adds the required and any additional arguments to the parser (based on 
argparse).  These arguments will be passed to the `get_users_and_groups` method.
3. A `get_users_and_groups` method that gets any users and groups, returning a `tsut.model.UsersAndGroups` object.### Readers

Note that some readers already exist and more are being added.  These can be simply reused instead of 
creating a new one.  See the `tsut.app` module.

### Writers

The primary goal of a writer is to write users and groups defined in a `tsut.model.UsersAndGroups` object 
to some location.  Note that you can have multiple writers that do different things with the same users
and groups.  The writers also have three methods:

1. An `__init__` method that does instance initialization, identifies required command line arguments and
calls `__init__` on the parent class.
2. An `add_parser_args` method that adds the required and any additional arguments to the parser (based on 
argparse).  These arguments will be passed to the `write_users_and_groups` method.
3. A `write_users_and_groups` method that writes users and groups base on a `tsut.model.UsersAndGroups` object.

Note that some writers already exist and more are being added.  These can be simply reused instead of 
creating a new one.  See the `tsut.app` module.

### Application

The application object is responsible for workflow of the application.  It takes a reader and one or more writers.  
Then you run the application and it does the following:

1. Check command line arguments based on those specified in the reader and writer(s).
2. Validates the arguments to make sure any that are required are included.
3. Calls the reader to get users and groups.
4. Calls the writers to write users and groups.

### Example

The `user_tools_example.py` file contains an example of a trivial, custom sync application.  It reads from a 
delimited text file and writes to a delimited text file.  The details of the method are not that important, so 
much as the structure.  You can use this example both as a reference and as a template for creating your own custom 
sync applications.

