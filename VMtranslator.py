import VMParser
import CodeWriter


def translate(vm_input, asm_output):
    """Drives the translation proccess of a single .vm file.

    Args:
        vm_input (str): Path (either  relative or absolute) of the .vm file to be translated.
        asm_output (str) : Path of the output .asm file to be created.
    """
    parser = VMParser.Parser(vm_input)
    writer = CodeWriter.CodeWriter(asm_output)

    while parser.has_more_lines():
        parser.advance()
        writer.comment(parser.current_command)
        if parser.command_type() == 'C_ARITHMETIC':
            writer.write_arithmetic(parser.arg1())
        else:
            writer.write_push_pop(parser.command_type(),
                                  parser.arg1(), parser.arg2())

    writer.close()
