import VMtranslator
import sys
import os


def main():
    # Terminate if not given exactly 1 input
    if len(sys.argv) != 2:
        print("Error: exactly one (1) .vm file or directory as input expected")
        sys.exit()

    file_name = sys.argv[1]

    # When receiving a file as input
    if os.path.isfile(file_name):

        # Terminate if given input is not .vm
        if os.path.splitext(file_name)[1] != '.vm':
            print("Error: input file should have the extension \".vm\"")
            sys.exit()

        # If output file exists, overwrite it (as CodeWriter uses append)
        if os.path.isfile(os.path.abspath(file_name)[:-2]+'asm'):
            os.remove(os.path.abspath(file_name)[:-2]+'asm')

        VMtranslator.translate(file_name, file_name)
        print("Translation completed!")

    # When receiving a directory of .vm files as input
    elif os.path.isdir(file_name):
        files = os.listdir(file_name)
        files = [os.path.join(file_name, f)
                 for f in files if os.path.splitext(f)[1] == '.vm']

        raw_name = os.path.dirname(file_name)[2:] if os.path.dirname(
            file_name)[:2] in ['./', '.\\'] else os.path.dirname(file_name)
        output = os.path.join(os.path.abspath(file_name), raw_name + '.vm')
        # If output file exists, overwrite it (as CodeWriter uses append)
        if os.path.isfile(output[:-2] + 'asm'):
            os.remove(output[:-2] + 'asm')

        for count, f in enumerate(files):
            if count == 0:
                VMtranslator.bootstrap(f, output)
            VMtranslator.translate(f, output)
        print("Translation completed!")

    # Terminate if given input is not an existing file or directory
    else:
        print("Error: given input file doesn't exist")
        sys.exit()


if __name__ == '__main__':
    main()
