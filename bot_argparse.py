import argparse


class ArgumentParser(argparse.ArgumentParser): 
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True,
                 exit_on_error=True):
        super().__init__(prog, usage, description, epilog, parents, formatter_class, prefix_chars,
            fromfile_prefix_chars, argument_default, conflict_handler, add_help, allow_abbrev, exit_on_error)
        self.help_info = ''
        self.error_info = ''
    
    def print_help(self, file=None):
        self.help_info = self.format_help()

    def error(self, message):
        self.error_info = f'{self.prog}: 错误: {message}'

    def exit(self, status=0, message=None):
        pass