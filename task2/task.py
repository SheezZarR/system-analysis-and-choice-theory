from __future__ import annotations

import os
from typing import List, Set

from csver.reader import CSVReader


class Node:

    def __init__(self, node_id: int, parent: Node | None):
        self.identifier: int = node_id
        self.children: List[Node] = []
        self.parent: Node = parent

    def add_child(self, node: Node) -> None:
        self.children.append(node)

    def __str__(self) -> str:
        return f'{self.identifier}: {[x.identifier for x in self.children]}, parent: {self.parent.identifier if self.parent else None}'


class Graph(CSVReader):

    with_children = set()
    with_parent = set()
    with_grandparent = set()
    with_grandchildren = set()
    with_siblings = set()

    def __init__(self):
        super().__init__(
            os.path.join(os.getcwd(), "sample.csv")
        )
        print(self.csv)
        self.nodes = {}

        for i in range(self.csv.shape[0]):
            from_node, to_node = self.get_at(i, 0), self.get_at(i, 1)

            if from_node not in self.nodes:
                self.nodes[from_node] = Node(int(from_node), None)

            if to_node not in self.nodes:
                self.nodes[to_node] = Node(int(to_node), self.nodes[from_node])

            self.nodes[from_node].add_child(self.nodes[to_node])

        for identifier, node in self.nodes.items():
            print(f"{identifier} -> {node}")

    def gather_nodes_with_children(self) -> Set[Node]:
        self.with_children.clear()

        for node in self.nodes.values():
            if node.children:
                self.with_children.add(node.identifier)

        return self.with_children

    def gather_nodes_with_parent(self) -> Set[Node]:
        self.with_parent.clear()

        for identifier, node in self.nodes.items():
            if node.parent:
                self.with_parent.add(node.identifier)

        return self.with_parent

    def gather_nodes_with_siblings(self) -> Set[Node]:
        self.with_siblings.clear()

        for identifier, node in self.nodes.items():
            if not node.parent:
                continue

            self.with_siblings.update([x.identifier for x in node.parent.children])

        return self.with_siblings

    def gather_nodes_with_grandparents(self) -> Set[Node]:
        self.with_grandparent.clear()

        for identifier, node in self.nodes.items():
            if not node.parent:
                continue

            if node.parent and node.parent.parent:
                self.with_grandparent.add(node.identifier)

        return self.with_grandparent

    def gather_nodes_with_grandchildren(self) -> Set[Node]:
        self.with_grandchildren.clear()

        for identifier, node in self.nodes.items():
            for child in node.children:
                if child.children:
                    self.with_grandchildren.add(node.identifier)
                    break

        return self.with_grandchildren


def main(*args, **kwargs):
    topG = Graph()
    print(
        "\n",
        f"С родителем {topG.gather_nodes_with_parent()}\n",
        f"С детьми {topG.gather_nodes_with_children()}\n",
        f"С сиблингами {topG.gather_nodes_with_siblings()}\n",
        f"С правнуками {topG.gather_nodes_with_grandchildren()}\n",
        f"Cо старшими предками {topG.gather_nodes_with_grandparents()}\n",
    )


if __name__ == "__main__":
    main()
