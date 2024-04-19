import getopt
import sys


def parse_arguments():
    """
    Parse the command line for arguments.

    @return: txt_file_path
    """
    # Initialize variables
    txt_file_path, title, task, offset = "", "", None, None
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments, 'f:t:g:o:')

    if len(opts) == 0:
        sys.exit("[+] ERROR: No arguments were provided!")

    for opt, argument in opts:
        if opt == '-f':  # For .txt file path
            try:
                with open(argument, "r"):
                    txt_file_path = argument
            except FileNotFoundError:
                sys.exit("[+] ERROR: File not found in path provided ({})".format(argument))

        if opt == '-t':  # For title of the text
            title = argument

        if opt == '-g':  # For task number
            if int(argument) in {1, 2}:
                task = int(argument)
            else:
                sys.exit("[+] ERROR: A task number must be either 1 or 2 (-g option)")

        if opt == '-o':  # For offset (used in task 2)
            offset = int(argument)
            if offset < 0:
                sys.exit("[+] ERROR: The offset (-o option) must be a positive integer!")

    # Check if parameters are provided
    if len(txt_file_path) == 0:
        sys.exit("[+] ERROR: The text file path was not provided! (-f option)")
    if len(title) == 0:
        sys.exit("[+] ERROR: The title of the text was not provided! (-t option)")
    if task is None:
        sys.exit("[+] ERROR: The task number was provided! (-g option)")

    return txt_file_path, title, task, offset
