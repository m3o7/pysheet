import project as p
import pkgutil

class MetaTable(type):

    def __new__(meta, name, bases, dct):
        """Create a new table class instance and register it"""
        module, _ = dct['__module__'].split('.')
        # create new table-class instance
        klass = super(MetaTable, meta).__new__(meta, name, bases, dct)
        # register the new table-(class) with its project-instance
        project = p.Project.get_project_klass(module)
        try:
            project.register_table(klass, name)
        except AttributeError as err:
            # Table class has no corresponding project
            pass
        return klass

    def import_tables(cls, package_name):
        """Return all tables of a module"""
        package = __import__( package_name )
        prefix = "{0}.".format( package.__name__ )
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__( modname )

    @property
    def name(cls):
        return cls.__name__

    @property
    def serialized(cls):
        return cls.name