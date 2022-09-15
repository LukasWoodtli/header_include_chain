
# This file is not used. Currently the dependency information is collected from *.d files

RELEVANT_FILE_ENDINGS = [".h", ".hpp", ".c", ".cpp"]


def relevant_file(filename):
    _, ext = os.path.splitext(filename)
    return ext in RELEVANT_FILE_ENDINGS


def find_source_files(paths):
    source_files = []
    for path in paths:
        for root, _, files in os.walk(path):
            for file in files:
                if relevant_file(file):
                    source_files.append(os.path.join(root, file))
    return source_files


INCLUDE_DIRECTIVE = re.compile(r'^\s*#\s*include\s+"([^"]*.h(pp)?)"')


def extract_includes(file):
    includes = []
    with open(file, "r") as in_file:
        for line in in_file.readlines():
            match = re.match(INCLUDE_DIRECTIVE, line)
            if match:
                includes.append(match.group(1))
    return includes


def split_path_components(path):
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break

    folders.reverse()
    return folders


def find_include_full_path(include_file, dependend_source_file, all_source_files):
    include_parts = split_path_components(include_file)
    source_files_parts = [split_path_components(source_file) for source_file in all_source_files]

    match = []
    for src_file_part in source_files_parts:
        length = len(include_parts)
        if src_file_part[-length:] == include_parts:
            match.append(src_file_part)

    if len(match) > 1:
        source_file_parts = split_path_components(dependend_source_file)
        length = len(source_file_parts)
        tmp_match = []
        for i in range(1, length):
            for m in match:
                try_path = source_file_parts[:-i]
                try_path.extend(include_file)
                if try_path == m:
                    tmp_match.append(m)

    if len(match) == 1:
        return "/".join(match[0]).replace("//", "/")
    else:
        return include_file


class SourceFile:
    def __init__(self, path, dependencies):
        self.path = path
        self.dependencies = dependencies



def generate_dependecy_list(sources):
    all_source_files = []
    for source in sources:
        includes = extract_includes(source)
        full_path_includes = [find_include_full_path(include, source, sources) for include in includes]
        all_source_files.append(SourceFile(source, full_path_includes))
    return all_source_files
