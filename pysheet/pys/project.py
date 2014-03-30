import os
from meta_project import MetaProject

class Project(object):
    """Represents a Project with all its tables"""

    __metaclass__ = MetaProject

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '<{0}: {1}>'.format(self.path)

    @property
    def name(self):
        """Return the project name"""
        _, filename = os.path.split(self.path)
        name, _, _ = filename.split('.')
        return name

    @property
    def serialized(self):
        """Return json representation of project"""
        return self.name
