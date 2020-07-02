"""
Copyright 2020 ThoughtSpot
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
import json
import sys


def eprint(*args, **kwargs):
    """
    Prints to standard error similar to regular print.
    :param args:  Positional arguments.
    :param kwargs:  Keyword arguments.
    """
    print(*args, file=sys.stderr, **kwargs)


def public_props(obj):
    """
    Returns any property that doesn't start with an _
    """
    return (name for name in vars(obj).keys() if not name.startswith("_"))


def obj_to_json(obj):
    """
    Returns a json string with all of the objects public properties as attributes
    This function only goes one level deep and does not convert contents of lists,
    dict, etc.
    :returns: A JSONS string representation of the object.
    :rtype: str
    """
    json_str = "{ "

    first = True
    for name in public_props(obj):
        value = getattr(obj, name)  # don't print empty values
        if not value:
            continue

        if first:
            first = False
        else:
            json_str += ","

        if value:
            json_str += f'"{name}":{json.dumps(value)}'

    json_str += "}"

    return json_str
