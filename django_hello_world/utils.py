from os.path import abspath, dirname


def get_project_path():
    return dirname(abspath(__file__))

if __name__ == '__main__':
    print get_project_path()
