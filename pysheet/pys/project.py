import os
from meta_project import MetaProject

class Project(object):
    """Represents a Project with all its tables"""

    __metaclass__ = MetaProject

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.name)

    @property
    def name(self):
        """Return the project name"""
        name, _, _ = self.package_name.split('_')
        return name

    @property
    def package_name(self):
        """Return the python-package name of the project"""
        _, package_name = os.path.split(self.path)
        return package_name

    @property
    def serialized(self):
        """Return json representation of project"""
        return self.name

    @property
    def tables(self):
        """Return all table-classes"""
        # import all tables of a module
        import table
        tables = table.Table.import_tables(package_name=self.package_name)
        return tables
