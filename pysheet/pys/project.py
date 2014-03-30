import os
from meta_project import MetaProject

class Project(object):
    """Represents a Project with all its tables"""

    __metaclass__ = MetaProject

    # { name : instance } - to enforce Singleton on per package basis
    __instances__ = {} 

    def __new__(cls, *args, **kwargs):
        """Enforce singleton on per-package basis"""
        _, package_name = os.path.split(kwargs.get('path'))
        if package_name not in cls.__instances__:
            cls.__instances__[package_name] = super(Project, cls).__new__(cls, *args, **kwargs)
        return cls.__instances__[package_name]

    def __init__(self, path):
        self.__tables__ = {} # { table-name: table-class}
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

    def register_table(self, table, name):
        """Register table with this project-instance"""
        self.__tables__[name] = table

    @property
    def serialized(self):
        """Return json representation of project"""
        return self.name

    @property
    def tables(self):
        """Return all table-classes"""
        # import all tables of a module
        import table
        table.Table.import_tables(package_name=self.package_name)
        return self.__tables__.values()
