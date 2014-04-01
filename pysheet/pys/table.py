from meta_table import MetaTable
import inspect
import os

class Table(object):
    
    __metaclass__ = MetaTable

    def execute(self):
        """Encapsulate run method"""
        return self.run()

    def __get_class_source__(self):
        """Return the source-code of the entire table-file"""
        full_path = inspect.getsourcefile(self.__class__)
        with open(full_path, 'r') as _file:
            source = _file.readlines()
        return source

    def __get_method_source__(self, method):
        """Return source code of a method"""
        # load source code
        func = getattr(self, method)
        lines, _ = inspect.getsourcelines(func)

        # remove indentation
        header_spaces = len(lines[0].split('def')[0])
        lines = [l[header_spaces:] for l in lines]
        return lines

    def get_source(self, method=None):
        """Return the source-code of the run-method and remove the indentation"""
        if method is None:
            source = self.__get_class_source__()
        else:
            source = self.__get_method_source__(method=method)
        return source

    def run(self):
        """Stub, needs to be implemented by its sub-classes"""
        raise NotImplementedError

    def __write_content_to_file__(self, filename, content):
        """Write the contents into the given file"""
        with open(filename, 'w') as _file:
            _file.write(content)
        # remove *.pyc file
        try:
            os.remove("{0}c".format(filename))
        except OSError:
            pass

    def __update_table_methode_source__(self, new_source, method):
        """Upate a method in a class-file with the new source-code"""
        # retrieving the method-source, class-source and isolate the method-code
        func = getattr(self, method)
        old_source, first_line = inspect.getsourcelines(func)
        first_line -= 1
        class_source = self.get_source()
        filename = inspect.getsourcefile(self.__class__)
        header_spaces = old_source[0].split('def')[0]
        new_source = ['{0}{1}'.format(header_spaces, l) for l in new_source.split('\n')]

        # construct the new source for the entire file
        part_1 = ''.join(class_source[:first_line])
        part_2 = ''.join(class_source[first_line+len(old_source):])
        content = '{0}{1}{2}'.format(part_1, '\n'.join(new_source), part_2)

        # write to disk
        self.__write_content_to_file__(filename=filename, content=content)

    def __update_table_source__(self, new_source):
        """Update the source-code for the entire file"""
        filename = inspect.getsourcefile(self.__class__)
        self.__write_content_to_file__(filename=filename, content=new_source)

    def update_source(self, new_source, method=None):
        """Forward the source-code update"""
        if method is None:
            self.__update_table_source__(new_source=new_source)
        else:
            self.__update_table_methode_source__(   new_source=new_source, 
                                                    method=method)

