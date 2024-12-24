import os


class CodeWriter:
    comp_index = 0  # index to label comparison operations, since they need labeling
    call_index = 0  # index for return address labels in call operations

    def __init__(self, f_name, vm_file_output):
        """Creates a CodeWriter object, that will write to the specified file.

        Args:
            dest_file (path): Path to create the output file.
        """
        self.path = os.path.abspath(vm_file_output)[:-2]+'asm'
        self.file = open(self.path, 'a+')
        self.file_name = os.path.basename(os.path.abspath(f_name))
        self.push_pop_dict = {'local': 'LCL',
                              'argument': 'ARG',
                              'this': 'THIS',
                              'that': 'THAT',
                              'temp': 5,
                              'pointer': 3}
        self.op_dict = {'add': '+',
                        'sub': '-',
                        'neg': '-',
                        'eq': 'EQ',
                        'gt': 'GT',
                        'lt': 'LT',
                        'and': '&',
                        'or': '|',
                        'not': '!'}

    def write_arithmetic(self, operator):
        """Writes to output the appropriate arithmetic or logical commands.

        Args:
            operator (str): The operator of current command
        """
        asm_command = ''
        if operator == 'neg' or operator == 'not':
            asm_command = self.one_operand(operator)
        elif operator == 'eq' or operator == 'gt' or operator == 'lt':
            asm_command = self.comparison_op(operator)
        else:
            asm_command = self.two_operands(operator)
        self.file.write(asm_command)

    def write_push_pop(self, command_type, segment, index):
        """Writes to output the appropriate push or pop commands.

        Args:
            command_type (str): C_PUSH or C_POP
            segment (str): Which segment to push/pop into
            index (int): Index within segment.
        """
        asm_command = ''
        if command_type == 'C_PUSH':
            if segment == 'constant':
                asm_command = self.push_constant(index)
            elif segment == 'static':
                asm_command = self.push_static(index)
            elif segment == 'temp' or segment == 'pointer':
                asm_command = self.push_temp_pointer(segment, index)
            else:
                asm_command = self.push(segment, index)
        else:
            if segment == 'static':
                asm_command = self.pop_static(index)
            elif segment == 'temp' or segment == 'pointer':
                asm_command = self.pop_temp_pointer(segment, index)
            else:
                asm_command = self.pop(segment, index)
        self.file.write(asm_command)

    def comment(self, command):
        """Writes the current VM line as a comment on the output file.

        Args:
            command: Current VM command.
        """
        line = '// '+str(command)+'\n'
        self.file.write('\n')
        self.file.write(line)

    def push_constant(self, index):
        """Writes appropriate ASM commands that implement pushing a constant.

        Args:
            index (int): The constant value to push.
        """
        lines = '''    // D = {n}
    @{n}
    D=A
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
    '''.format(n=index)
        return lines

    def push(self, segment, index):
        """Writes appropriate ASM commands that implement pushing from local, argument, this, or that.

        Args:
            segment (str): The segment to push from.
            index (int): The offset index in specified segment.
        """
        lines = '''    // D = RAM[{seg} + {i}]
    @{i}
    D=A
    @{seg}
    D=D+M
    A=D
    D=M
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
    '''.format(seg=self.push_pop_dict[segment], i=str(index))
        return lines

    def pop(self, segment, index):
        """Writes appropriate ASM commands that implement popping to local, argument, this or that.

        Args:
            segment (str): The segment to pop into.
            index (int): The offset index in specified segment.
        """
        lines = '''    // RAM[13] = {seg} + {i}
    @{seg}
    D=M
    @{i}
    D=D+A
    @R13
    M=D
    // SP--
    @SP
    M=M-1
    // RAM[R13] = RAM[SP]
    A=M
    D=M
    @R13
    A=M
    M=D
    '''.format(seg=self.push_pop_dict[segment], i=index)
        return lines

    def push_static(self, index):
        """Implements pushing from static segment.

        Args:
            index (int): The offset within the segment to push from.
        """
        lines = '''    @{label}
    D=M
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
    '''.format(label=self.file_name.split('.')[0]+'.'+str(index))
        return lines

    def pop_static(self, index):
        """Implement popping into static segment.

        Args:
            index (int): The offset within the segment to pop into.
        """
        lines = '''    @SP
    M=M-1
    A=M
    D=M
    @{label}
    M=D
    '''.format(label=self.file_name.split('.')[0]+'.'+str(index))
        return lines

    def one_operand(self, op):
        """Template for one-operand operation.

        Args:
            op (str): Which operation to slot.
        """
        lines = '''    @SP
    M=M-1
    A=M
    M={}M
    @SP
    M=M+1
    '''.format(self.op_dict[op])
        return lines

    def push_temp_pointer(self, segment, index):
        """Push template for pushing from temp and pointer segments.

        Args:
            segment (str): temp or pointer
            index (int): Index within segment.
        """
        lines = '''    // D = RAM[{seg} + {i}]
    @{i}
    D=M
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1
    '''.format(seg=self.push_pop_dict[segment], i=str(index+self.push_pop_dict[segment]))
        return lines

    def pop_temp_pointer(self, segment, index):
        """Pop template for popping into temp and pointer segments.

        Args:
            segment (str): temp or pointer
            index (int): Index within segment.
        """
        lines = '''    // SP--
    @SP
    M=M-1
    // RAM[{0}] = RAM[SP]
    A=M
    D=M
    @R{0}
    M=D
    '''.format(str(self.push_pop_dict[segment]+index))
        return lines

    def two_operands(self, op):
        """Template for operation with 2 operands.

        Args:
            op (str): Which operator to slot.
        """
        lines = '''    @SP
    M=M-1
    A=M
    D=M
    @SP
    M=M-1
    A=M
    M=D{}M
    @SP
    M=M+1
    '''.format(self.op_dict[op])
        if 'D-M' in lines:
            lines = lines.replace('D-M', 'M-D')
        return lines

    def comparison_op(self, op):
        """Template for comparison operation.

        Args:
            op (str): eq, gt, lt.
        """
        lines = '''    @SP
    M=M-1
    A=M
    D=M
    @SP
    M=M-1
    A=M
    D=M-D
    @TRUE{c}
    D;J{o}
    D=0
    @FINISHCOMP{c}
    0;JMP
(TRUE{c})
    D=-1
(FINISHCOMP{c})
    @SP
    A=M
    M=D
    @SP
    M=M+1
    '''.format(o=self.op_dict[op], c=CodeWriter.comp_index)
        CodeWriter.comp_index += 1
        return lines

    def close(self):
        """Closes this instance's output stream, effectively ending the usability of this instance.
        """
        self.file.close()

    def write_label(self, label):
        asm_command = '(' + label + ')\n'
        self.file.write(asm_command)

    def write_goto(self, label):
        asm_command = '''    @{}
    0;JMP
    '''.format(label)
        self.file.write(asm_command)

    def write_if(self, label):
        asm_command = '''    @SP
    M=M-1
    A=M
    D=M
    @{}
    D;JNE
    '''.format(label)
        self.file.write(asm_command)

    def write_function(self, f_name, n_vars):
        # TODO
        pass

    def write_call(self, f_name, n_args):
        asm_command = '''    @{name}$ret{num}
    D=A
    '''.format(name=f_name, num=str(self.call_index)) + self.write_internal_push() +\
            '''@LCL
    D=M
    ''' + self.write_internal_push() +\
            '''@ARG
    D=M
    ''' + self.write_internal_push() +\
            '''@THIS
    D=M
    ''' + self.write_internal_push() +\
            '''@THAT
    D=M
    ''' + self.write_internal_push() +\
            '''@{}
    D=A
    @SP
    D=M-D
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    '''.format(str(n_args + 5))

        self.file.write(asm_command)
        self.write_goto(f_name)
        self.write_label(f_name+'$ret'+str(self.call_index))
        self.call_index += 1

    def write_internal_push(self):
        lines = '''@SP
    A=M
    M=D
    @SP
    M=M+1
    '''
        return lines

    def write_return(self):
        # TODO
        pass
