"""
Copyright 2018 ThoughtSpot

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
import argparse
import json
import sys

from tsut.model import UsersAndGroups


def run_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="file containing data to load.")
    args = parser.parse_args()

    json_data = ""
    if args.filename:
        print(f"Validating JSON format and content from {args.filename}")
        with open(args.filename, "r") as infile:
            json_data = infile.read()
    else:
        print(f"Validating JSON format and content from stdin")
        for line in sys.stdin:
            json_data += line

    json.loads(json_data)
    print("JSON format appears valid.")  # only prints if valid.

    ugs = UsersAndGroups()
    ugs.load_from_json(json_str=json_data)
    if ugs.is_valid()[0]:
        print(f"JSON content appears valid.  There are {ugs.number_groups()} groups and {ugs.number_users()} users.")
    else:
        print(f"JSON content does not appear valid.")


if __name__ == "__main__":
    run_app()
