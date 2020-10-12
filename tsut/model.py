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
from collections import OrderedDict, namedtuple
import copy
import json

from .util import eprint, public_props, obj_to_json

# -------------------------------------------------------------------------------------------------------------------


class Visibility:
    DEFAULT = "DEFAULT"
    NON_SHAREABLE = "NON_SHARABLE"


class User:
    """
    Represents a user to TS.
    """

    def __init__(
        self,
        name,
        password=None,
        mail=None,
        display_name=None,
        group_names=None,
        visibility=Visibility.DEFAULT,
        created=None,
        user_id=None
    ):
        """
        Creates a new user object.
        :param name: The name of the user.  This is the login name.
        :type name: str
        :param password: The password for the user.  Not sent if there is no password.
        :type password: str
        :param mail: The user's email.
        :type mail: str
        :param display_name: The name to display in the UI.  Set to name if not provided.
        :type display_name: str
        :param group_names: Set of groups the user belongs to.
        :type group_names: list of str
        :param visibility: Visibility for sharing.
        :type visibility: str
        :param created: Epoch time when the user was created.
        :type created: str
        :param user_id: GUID from TS for the user.  Optional and not used for syncing.
        :type created: str
        :return: Returns a new user object populated with the passed in values.
        :rtype: User
        """
        self.principalTypeEnum = "LOCAL_USER"
        self.name = name.strip()
        self.displayName = display_name if not None else name
        self.password = password
        self.mail = mail
        self.created = created
        self.groupNames = list()
        if group_names:
            for gn in group_names:
                self.groupNames.append(gn)
        self.visibility = visibility
        self.id = user_id

    @staticmethod
    def create_from_json(json_obj):
        """
        Creates a new user from JSON.
        :param json_obj: The JSON object (parsed JSON).
        :type json_obj: dict
        :return: A new user.
        """
        name = json_obj.get("name", None)
        display_name = json_obj.get("displayName", None)
        mail = json_obj.get("mail", None)
        password = json_obj.get("password", None)
        visibility = json_obj.get("visibility", None)
        group_names = json_obj.get("groupNames", None)

        return User(name=name, display_name=display_name, password=password,
                    mail=mail, visibility=visibility, group_names=group_names )

    def add_group(self, group_name):
        """
        Adds a parent group for the user.
        :param group_name: Name of the group to add.  Only one of any group is added.
        """

        if group_name not in self.groupNames:
            self.groupNames.append(group_name)

    def to_json(self):
        """
        Returns a JSON string representing this user.
        :return: A JSON string representing this user.
        :rtype: str
        """
        return obj_to_json(self)

    def __repr__(self):
        """
        Provides a string representation of the object.
        :return: A string representation of a user.
        :type: str
        """
        return self.to_json()


class Group:
    """
    Represents a group to TS.
    """

    def __init__(
        self,
        name,
        display_name=None,
        description=None,
        group_names=None,
        visibility=Visibility.DEFAULT,
        privileges=None,
        created=None,
    ):
        """
        Creates a new group object.
        :param name: The name of the group.
        :type name: str
        :param display_name: The name to display in the UI.  Set to name if not provided.
        :type display_name: str
        :param description: The optional description of the group.
        :type description: str
        :param group_names: Set of groups the group belongs to.
        :type group_names: list of str
        :param visibility: Indicates if the group is visibility or default.
        :type visibility: str
        :param privileges: The privileges for the group.
        :type privileges: list of str
        :param created: The epoch date when the group was created.
        :type created: str
        :return: Returns a new group object populated with the passed in values.
        :rtype: Group
        """
        self.principalTypeEnum = "LOCAL_GROUP"
        self.name = name.strip()
        self.displayName = display_name if not None else name
        self.description = description
        self.visibility = visibility
        self.privileges = copy.copy(privileges) if not None else []
        self.created = created
        self.groupNames = list()
        if group_names:
            for gn in group_names:
                self.groupNames.append(gn)

    @staticmethod
    def create_from_json(json_obj):
        """
        Creates a new user from JSON.
        :param json_obj: The JSON object (parsed JSON).
        :type json_obj: dict
        :return: A new user.
        """
        name = json_obj.get("name", None)
        display_name = json_obj.get("displayName", None)
        description = json_obj.get("description", None)
        visibility = json_obj.get("visibility", None)
        group_names = json_obj.get("groupNames", None)

        return Group(name=name, display_name=display_name, description=description,
                     visibility=visibility, group_names=group_names )

    def add_group(self, group_name):
        """
        Adds a parent group for the user.
        :param group_name: Name of the group to add.  Only one of any group is added.
        """

        if group_name not in self.groupNames:
            self.groupNames.append(group_name)

    def to_json(self):
        """
        Returns a JSON string representing this group.
        :return: A JSON string representing this group.
        :rtype: str
        """
        return obj_to_json(self)

    def __repr__(self):
        """
        Provides a string representation of the object.
        :return: A string representation of a group.
        :rtype: str
        """
        return self.to_json()


# Global list of users and groups. ----------------------------------------------------------------------

ValidationResults = namedtuple("ValidationResults", ["result", "issues"])


class UsersAndGroups:
    """
    Container for created users and groups.  Can be converted to JSON and sent to the TS API.
    """

    # Flags to say what to do when adding duplicates for users or groups.  Default is RAISE_ERROR_ON_DUPLICATE.
    RAISE_ERROR_ON_DUPLICATE = 0
    IGNORE_ON_DUPLICATE = 1
    OVERWRITE_ON_DUPLICATE = 2
    UPDATE_ON_DUPLICATE = 3

    def __init__(self):
        """
        Creates a new container for users and groups.
        """
        self.users = OrderedDict()
        self.groups = OrderedDict()

    def add_user(self, u, duplicate=RAISE_ERROR_ON_DUPLICATE):
        """
        Adds a user to the container.  Note that this does not make a copy of the user.
        :param u: User object to add to the container.
        :param duplicate: Flag to indicate how to handle duplicates.
        """
        l_username = u.name.lower()  # keys are stored in lower case to avoid duplicates.
        user = self.get_user(l_username)
        if not user:
            self.users[l_username] = u
        else:
            print(f"WARNING:  Duplicate user {user.name} already exists.")

            if duplicate == UsersAndGroups.RAISE_ERROR_ON_DUPLICATE:
                raise Exception(f"Duplicate user {u}")
            elif duplicate == UsersAndGroups.IGNORE_ON_DUPLICATE:
                pass  # keep the old one.
            elif duplicate == UsersAndGroups.OVERWRITE_ON_DUPLICATE:
                self.users[l_username] = u
            elif duplicate == UsersAndGroups.UPDATE_ON_DUPLICATE:
                u.groupNames.extend(user.groupNames)
                self.users[l_username] = u
            else:
                raise Exception(f"Unknown duplication rule {duplicate}")

    def has_user(self, user_name):
        """
        Returns true if the user is in the collection.
        :param user_name: Name of the user to check for.
        :return: True if the user is in the set, else false.
        :rtype: bool
        """
        return user_name.lower() in self.users

    def get_user(self, user_name):
        """
        Returns the user with the given name or None.
        :param user_name: Name of the user to get.
        :return: The user object or None.
        :rtype: User
        """
        return self.users.get(user_name.lower(), None)

    def remove_user(self, user_name):
        """
        Removes the user with the given name if it is in the collection..
        :param user_name: Name of the user to remove.
        """
        return self.users.pop(user_name.lower(), None)

    def number_users(self):
        """
        Returns the number of users in the list.
        :return: The number of users in the list.
        :rtype: int
        """
        return len(self.users)

    def get_users(self):
        """
        Returns a list with all the users.  This is a copy so the users here won't be changed.
        :return:  The list of users.
        :rtype: list
        """
        return list(self.users.values())

    def add_group(self, g, duplicate=RAISE_ERROR_ON_DUPLICATE):
        """
        Adds a group to the container.  Note that this does not make a copy of the group.
        :param g: Group object to add to the container.
        :param duplicate: Flag for what to do if there is a duplicate entry.
        """
        group = self.get_group(g.name)
        if not group:
            if g.groupNames:
                assert(isinstance(g.groupNames, list))
                groups_to_add = list(g.groupNames)  # making a copy in case the original is modified.
                g.groupNames = groups_to_add
            self.groups[g.name] = g
        else:
            if duplicate == UsersAndGroups.RAISE_ERROR_ON_DUPLICATE:
                raise Exception(f"Duplicate group {g}")
            elif duplicate == UsersAndGroups.IGNORE_ON_DUPLICATE:
                pass
            elif duplicate == UsersAndGroups.OVERWRITE_ON_DUPLICATE:
                self.groups[g.name] = g
            elif duplicate == UsersAndGroups.UPDATE_ON_DUPLICATE:
                group.groupNames.extend(g.groupNames)
            else:
                raise Exception(f"Unknown duplication rule {duplicate}")

    def has_group(self, group_name):
        """
        Returns true if the group is in the collection.
        :param group_name: Name of the group to check for.
        :return: True if the group is in the set, else false.
        :rtype: bool
        """
        # print self.groups
        return group_name in self.groups

    def get_group(self, group_name):
        """
        Returns the group with the given name or None.
        param group_name: Name of the group to get.
        :return: The group object or None.
        :rtype: Group
        """
        return self.groups.get(group_name, None)

    def remove_group(self, group_name):
        """
        Removes the group with the given name if it is in the collection..
        :param group_name: Name of the group to remove.
        """
        return self.groups.pop(group_name, None)

    def number_groups(self):
        """
        Returns the number of groups in the list.
        :return: The number of groups in the list.
        :rtype: int
        """
        return len(self.groups)

    def get_groups(self):
        """
        Returns a list with all the groups.  This is a copy so the groups here won't be changed.
        :return:  The list of groups.
        :rtype: list
        """
        return list(self.groups.values())

    def to_json(self):
        """
        Adds a group to the container.
        :return: A JSON string representation the users and groups.
        :rtype: str
        """
        json_str = "["
        first = True
        for g in self.groups.values():
            if first:
                first = False
            else:
                json_str += ","
            json_str += g.to_json()

        for u in self.users.values():
            if first:
                first = False
            else:
                json_str += ","
            json_str += u.to_json()

        json_str += "]"

        return json_str

    def load_from_json(self, json_str):
        """
        Loads the users and groups from a properly formatted JSON string.  This can add additional users and groups.
        :param json_str: The json string to load from.
        :type json_str: str
        :return: Nothing
        """
        ug_json = json.loads(json_str)
        for obj in ug_json:
            type = obj.get("principalTypeEnum", None)
            if type.endswith("_GROUP"):
                group = Group.create_from_json(obj)
                self.add_group(group)
            elif type.endswith("_USER"):
                user = User.create_from_json(obj)
                self.add_user(user)
            else:
                eprint(f"Unable to load {obj} as a user or group.  Missing or unknown 'principalTypeEnum' value {type}")

    def __repr__(self):
        """
        Retruns a string representation of the list.
        :return: A string representation of the list.
        :rtype: str
        """
        return self.to_json()

    def is_valid(self):
        """
        This method checks to see if the users and groups line up.  It makes sure that groups users belong to exist
        and that groups other groups belong to also exist.
        :return: Tuple with true or false if valid and list of errors if not.
        :rtype: (bool, issues)
        """
        issues = []
        valid = True  # true by default until an issue is found.

        for user in self.users.values():
            # 5.3+ will require emails, but it's not clear if always.  Leaving this commented out for now.
            # if not user.mail:
            #    issue = "user %s doesn't have a required email address." % user.name
            #    print(issue)
            #    issues.append(issue)
            #    valid = False

            for parent_group in user.groupNames:
                if parent_group not in self.groups:
                    issue = f"user group {parent_group} for user {user.name} does not exist"
                    print(issue)
                    issues.append(issue)
                    valid = False

        for group in self.groups.values():
            for parent_group in group.groupNames:
                if parent_group not in self.groups:
                    issue = f"parent group {parent_group} for group {group.name} does not exist"
                    print(issue)
                    issues.append(issue)
                    valid = False

        return ValidationResults(result=valid, issues=issues)
