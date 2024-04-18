from utilities.init import parse_arguments
from utilities.utility import perform_task_1

if __name__ == '__main__':
    txt_file_path, title = parse_arguments()
    perform_task_1(txt_file_path, title)
