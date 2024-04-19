from utilities.init import parse_arguments
from utilities.utility import perform_task_1, perform_task_2

if __name__ == '__main__':
    txt_file_path, title, task, offset = parse_arguments()

    if task == 1:
        perform_task_1(txt_file_path, title)

    if task == 2:
        perform_task_2(txt_file_path, title, offset)
