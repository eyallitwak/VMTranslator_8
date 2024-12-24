import VMParser
import CodeWriter


def translate(vm_input, asm_output):
    """Drives the translation proccess of a single .vm file.

    Args:
        vm_input (str): Path (either  relative or absolute) of the .vm file to be translated.
        asm_output (str) : Path of the output .asm file to be created.
    """
    parser = VMParser.Parser(vm_input)
    writer = CodeWriter.CodeWriter(vm_input, asm_output)

    while parser.has_more_lines():
        parser.advance()
        writer.comment(parser.current_command)
        if parser.command_type() == 'C_ARITHMETIC':
            writer.write_arithmetic(parser.arg1())
        elif parser.command_type() == 'C_PUSH' or parser.command_type() == 'C_POP':
            writer.write_push_pop(parser.command_type(),
                                  parser.arg1(), parser.arg2())
        elif parser.command_type() == 'C_LABEL':
            writer.write_label(parser.arg1())
        elif parser.command_type() == 'C_GOTO':
            writer.write_goto(parser.arg1())
        elif parser.command_type() == 'C_IF':
            writer.write_if(parser.arg1())
        elif parser.command_type() == 'C_CALL':
            writer.write_call(parser.arg1(), parser.arg2())
        elif parser.command_type() == 'C_FUNCTION':
            writer.write_function(parser.arg1(), parser.arg2())
        elif parser.command_type() == 'C_RETURN':
            writer.write_return()

    writer.close()
