from graph import find_include_full_path


def test_find_complete_relative_path():
    all_pathes = ["./a/b/c/bla.h",
                  "./a/b/c/x/y/z/bla.h",
                  "./a/b/a/bla.h"]
    header_to_search = "c/bla.h"
    dependent_file = "./a/b/c/foo.c"

    assert "./a/b/c/bla.h" ==  find_include_full_path(header_to_search, dependent_file, all_pathes)


