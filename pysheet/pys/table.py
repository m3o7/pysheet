from meta_table import MetaTable
import inspect

class Table(object):
    
    __metaclass__ = MetaTable

    def execute(self):
        """Encapsulate run method"""
        return self.run()

    def get_run_source(self):
        """Return the source-code of the run-method and remove the indentation"""
        # load source code
        lines, _ = inspect.getsourcelines(self.run)

        # remove indentation
        header_spaces = len(lines[0].split('def')[0])
        lines = [l[header_spaces:] for l in lines]
        return lines

    def get_full_source(self):
        """Return the source-code of the entire table-file"""
        full_path = inspect.getsourcefile(self.__class__)
        with open(full_path, 'r') as _file:
            source = _file.readlines()
        return source

    def run(self):
        """Stub, needs to be implemented by its sub-classes"""
        raise NotImplementedError

    def update_source(self, new_source):
        """Upate the class-file with the new source-code"""
        old_source, first_line = inspect.getsourcelines(self.run)
        first_line -= 1
        class_source = self.get_full_source()
        full_path = inspect.getsourcefile(self.__class__)
        header_spaces = old_source[0].split('def')[0]
        new_source = ['{0}{1}'.format(header_spaces, l) for l in new_source.split('\n')]

        part_1 = ''.join(class_source[:first_line])
        part_2 = ''.join(class_source[first_line+len(old_source):])

        content = '{0}{1}\n{2}'.format(part_1, '\n'.join(new_source), part_2)

        with open(full_path, 'w') as table_file:
            table_file.write(content)

