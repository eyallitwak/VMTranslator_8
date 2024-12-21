class Parser:

    def __init__(self, source_file):
        """Initializes a parser that reads the given .vm file.\n
        Each file requires a new parser.

        Args:
            source_file (str): Path (either relative or absolute) of the .vm file to be translated.
        """
        self.current_command = ''  # initially there is no current command
        self.command_index = 0
        self.all_commands = []

        # reads entire file into a list line-by-line
        # while removing comments and whitespace
        with open(source_file, 'r') as file:
            self.all_commands = file.read().splitlines()
            self.all_commands = [line.strip().split('//')[0]
                                 for line in self.all_commands]
            self.all_commands = [
                line for line in self.all_commands if line != '']

    def has_more_lines(self):
        """Returns whether or not current file has more lines left to parse.

        Returns:
            bool: does current file has more lines left to parse.
        """
        return self.command_index < len(self.all_commands)

    def advance(self):
        """Advances the current command by one.\n
        Should only be used if your'e certain there are more lines left.
        """
        self.current_command = self.all_commands[self.command_index]
        self.command_index += 1

    def command_type(self):
        """Returns the type of the current command, in this format:\n
        C_ARITHMETIC for logical/arithmetic command,\n
        C_PUSH for push command,\n
        C_POP for pop command,\n
        C_LABEL,\n
        C_GOTO,\n
        C_IF,\n
        C_FUNCTION,\n
        C_RETURN,\n
        C_CALL

        Returns:
            const str: The type of the current command as C_<TYPE>
        """
        cmd = self.current_command.split(' ')[0]
        types = {'add': 'C_ARITHMETIC', 'sub': 'C_ARITHMETIC',
                 'neg': 'C_ARITHMETIC', 'eq': 'C_ARITHMETIC',
                 'gt': 'C_ARITHMETIC', 'lt': 'C_ARITHMETIC',
                 'and': 'C_ARITHMETIC', 'or': 'C_ARITHMETIC',
                 'not': 'C_ARITHMETIC', 'push': 'C_PUSH',
                 'pop': 'C_POP', 'goto': 'C_GOTO',
                 'if-goto': 'C_IF', 'label': 'C_LABEL',
                 'call': 'C_CALL', 'function': 'C_FUNCTION',
                 'return': 'C_RETURN'}
        return types[cmd]

    def arg1(self) -> str:
        """Returns the first argument of the current command.\n
        In the case of C_ARITHMETIC the command itself (add, sub, etc.) is returned.\n
        Should not be called if current command is C_RETURN

        Returns:
            str: The first argument of current command.
        """
        if self.command_type() == 'C_ARITHMETIC':
            return self.current_command.split(' ')[0]
        else:
            return self.current_command.split(' ')[1]

    def arg2(self) -> int:
        """Return the second argument of the current command.\n
        Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION or C_CALL.

        Returns:
            int: The second argument of the current command.
        """
        return int(self.current_command.split(' ')[2])
