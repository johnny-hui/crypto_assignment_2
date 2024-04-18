import getopt
import sys


def parse_arguments():
    """
    Parse the command line for arguments.

    @return: txt_file_path
    """
    # Initialize variables
    txt_file_path, title = "", ""
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments, 'f:t:')

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

    # Check if parameters are provided
    if len(txt_file_path) == 0:
        sys.exit("[+] ERROR: The text file path was not provided! (-f option)")
    if len(title) == 0:
        sys.exit("[+] ERROR: The title of the text was not provided! (-t option)")

    return txt_file_path, title
