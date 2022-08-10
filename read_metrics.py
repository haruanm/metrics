import json
import os

import jedi
from py2neo import Graph, Node, Relationship

BASE_PATH = "/home/haruan/Projects/django/"


def read_metrics(path=".metrics"):
    metrics = {}
    with open(path) as metrics_file:
        metrics = json.loads(metrics_file.read())
    return metrics


def get_file_attributes(node, absolute_path, relative_path):
    if "block_positions" in node:
        del node["block_positions"]

    node["absolute_path"] = absolute_path
    node["relative_path"] = relative_path
    node["filename"] = os.path.basename(absolute_path)

    return node


def get_file_relations(code_path):
    with open(code_path) as code_file:
        code = code_file.read()

    script = jedi.Script(code, path=code_path)
    names = script.get_names()

    paths = []
    for name in names:
        name_paths = name.goto(follow_imports=True)
        if len(name_paths) > 0 and str(name_paths[0].module_path) != str(code_path):
            paths.append(str(name_paths[0].module_path))

    return paths


def create_method_nodes(methods, tx, class_path):
    nodes = {}
    for method in methods:
        method_path = class_path + "->" + method["name"]
        node = Node("Method", method_path=method_path, class_path=class_path, **method)
        tx.create(node)
        nodes[method_path] = node

    return nodes


def create_class_node(block_position, tx, file_path):
    nodes = {}
    class_path = file_path + "::" + block_position["name"]
    if "methods" in block_position:
        method_nodes = create_method_nodes(block_position["methods"], tx, class_path)
        nodes.update(method_nodes)
        del block_position["methods"]

    node = Node("Class", file_path=file_path, class_path=class_path, **block_position)
    tx.create(node)
    nodes[class_path] = node

    return nodes


def create_block_nodes(block_positions, tx, file_path):
    blocks = {}
    for block_position in block_positions:
        if block_position["type"] == "Class":
            blocks.update(create_class_node(block_position, tx, file_path))
        if block_position["type"] == "Function":
            function_path = file_path + "::->" + block_position["name"]
            node = Node("Function", file_path=file_path, function_path=function_path, **block_position)
            blocks[function_path] = node
            tx.create(node)

    return blocks


def create_nodes(files, tx):
    nodes = {}
    for file in files:
        file_path = BASE_PATH + file
        print("reading file" + file_path + "\n")

        # if "block_positions" in files[file] and len(files[file]["block_positions"]):
        #     block_positions = files[file]["block_positions"]
        #     block_nodes = create_block_nodes(block_positions, tx, file_path)
        #     nodes.update(block_nodes)

        node = Node("File", **get_file_attributes(files[file], file_path, file))
        tx.create(node)

        nodes[file_path] = node

    return nodes


def create_relations(nodes, tx):
    for key in nodes:
        if nodes[key].has_label("File") and nodes[key]["language"] == "Python":
            relations = get_file_relations(nodes[key]["absolute_path"])
            for relation in relations:
                if relation in nodes:
                    tx.create(Relationship(nodes[key], "DEPENDS_ON_FILE", nodes[relation]))
        if nodes[key].has_label("Class") or nodes[key].has_label("Function"):
            tx.create(Relationship(nodes[key], "IS_IN_FILE", nodes[nodes[key]["file_path"]]))
        if nodes[key].has_label("Method"):
            tx.create(Relationship(nodes[key], "IS_IN_CLASS", nodes[nodes[key]["class_path"]]))


def save_metrics():
    graph = Graph("bolt://neo4j:neo4jj@localhost:7687")
    graph.delete_all()
    tx = graph.begin()

    metrics = read_metrics("./metrics")

    nodes = create_nodes(metrics["files"], tx)
    create_relations(nodes, tx)

    tx.commit()


save_metrics()
