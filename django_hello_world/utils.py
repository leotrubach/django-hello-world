from os.path import abspath, dirname, join


def get_project_path(subdir=''):
    return join(dirname(abspath(__file__)), subdir)

if __name__ == '__main__':
    print get_project_path()
