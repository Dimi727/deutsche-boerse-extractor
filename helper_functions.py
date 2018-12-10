import glob


def yes_no_input(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def create_list_of_files(data_dirs):
    files = []
    for data_dir in data_dirs:
        files.extend(glob.glob(data_dir+'/*.csv'))
        files.sort()
    return files
