#!/usr/bin/env python

import argparse
import csv

from tsut.apps import TSUserGroupSyncApp, TSUGReader, TSUGWriter
from tsut.model import UsersAndGroups, User, Group

"""
Copyright 2019 ThoughtSpot
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


class CSVReader(TSUGReader):
    """
    Reads uses and groups from a delimited file.
    You can also extend from some other reader if it's close to what you want.
    """

    def __init__(self):
        """
        Creates a new reader.
        Replace the required arguments with your own and add any other initialization code.
        """
        super(CSVReader, self).__init__(
            required_arguments=["input_filename"]
        )

    def add_parser_arguments(self, parser):
        """
        Adds command line arguments that can be handled by this reader.  Note that name checking is *not* handled, so
        make sure your argument names are unique between the reader and writers.
        :param parser: The parser to add arguments to.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument("--input_filename", help="Name of file to read from from.")

    def get_users_and_groups(self, args):
        """
        Called by the app to get users and groups.
        :param args: Passed in arguments.
        :type args: argparse.Namespace
        :return: Users and groups that were read.
        :rtype: UsersAndGroups
        """
        ugs = UsersAndGroups()

        with open(args.input_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # create user and add to groups.
                ugs.add_user(User(name=row['name'], password=row['password'], mail=row['mail'],
                                  visibility=row['visibility'], group_names=row['groups']))
                # add the groups
                ugs.add_group(Group(name=row['groups'], description=row['groups'], visibility=row['visibility']))

        return ugs


class CSVWriter(TSUGWriter):
    """
    Writes users and groups to Excel.
    """

    def __init__(self):
        """
        Creates a new writer.
        Replace the required arguments with your own and add any other initialization code.
        """
        super(CSVWriter, self).__init__(
            required_arguments=["output_filename"])

    def add_parser_arguments(self, parser):
        """
        Adds command line arguments that can be handled by this writer.  Note that name checking is *not* handled, so
        make sure your argument names are unique between the reader and writers.
        :param parser: The parser to add arguments to.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument("--output_filename", help="Name of the file to write to.")

    def write_user_and_groups(self, args, ugs):
        """
        Writes the users and groups to a delimited.
        :param args: Command line arguments for writing.  Expects the "filename" argument.
        :type args: argparse.Namespace
        :param ugs: Users and groups to write.
        :type ugs: UsersAndGroups
        :return:  None
        """

        fieldnames = ['name', 'password', 'mail', 'groups', 'visibility']
        with open(args.output_filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for user in ugs.users:
                writer.writerow({'name': user.name, 'password': user.password, 'mail': user.mail,
                                'groups': user.groups, 'visibility': user.visibility})


def run_app():
    reader = CSVReader()
    writer = CSVWriter()
    sync_app = TSUserGroupSyncApp(reader=reader, writers=writer)
    sync_app.run()


if __name__ == "__main__":
    run_app()
