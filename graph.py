import os
from collections import defaultdict

import networkx as nx

from dependency_files import get_dependecies_from_d_file_content


def generate_graph(dependencies_list):
    g = nx.MultiDiGraph()
    for dependent, dependencies in dependencies_list.items():
        for dependency in dependencies:
            g.add_edge(dependent, dependency)
    return g


def is_dep_file(file_name):
    return file_name.endswith(".d")


# add -MMD to gcc to create dependency files
# add -d keepdepfile to ninja (otherwise the *.d files will be deleted)
# https://discourse.cmake.org/t/dependency-file-d-file-generation-in-cmake/2680
def find_dependency_files(path):
    dep_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if is_dep_file(file):
                dep_files.append(os.path.join(root, file))
    return dep_files


def generate_dependecy_list_from_d_files(dep_files):
    dependencies = defaultdict(set)
    for dep_file in dep_files:
        with open(dep_file, 'r') as dep_f:
            deps = get_dependecies_from_d_file_content(dep_f.read())
            for k, v in deps.items():
                dependencies[k].update(v)
    return dependencies


if __name__ == "__main__":

    path = "builddir"
    dep_files = find_dependency_files(path)
    dependencies = generate_dependecy_list_from_d_files(dep_files)

    g = generate_graph(dependencies)
    groups = nx.algorithms.components.strongly_connected_components(g)
    for group in groups:
        print(group)
    #nx.draw(g)
    #plt.savefig("graph.svg")




