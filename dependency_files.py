import os.path


def get_file_name_from_dependency_file_line(line):
    path = os.path.basename(line)
    path = path.split(".")
    return path[0]


def get_dependecies_from_d_file_content(d_file_content):
    paths = []
    lines = d_file_content.split("\\")
    [paths.extend(line.split()) for line in lines]
    file_names = [get_file_name_from_dependency_file_line(name) for name in paths]
    dependant = file_names[0]
    dependencies = set(file_names)
    dependencies.remove(dependant)  # no dependency on self
    return {dependant: dependencies}
