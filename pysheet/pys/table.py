from meta_table import MetaTable

class Table(object):
    
    __metaclass__ = MetaTable

    def execute(self):
        """Encapsulate run method"""
        return self.run()

    def run(self):
        """Stub, needs to be implemented by its sub-classes"""
        raise NotImplementedError
