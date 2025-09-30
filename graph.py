from typing import List, Any, Dict
from ppm import PPM

class EdgeAlreadyExistsException(Exception):
    pass

class NodeAlreadyExistsException(Exception):
    pass

class IllegalWeightException(Exception):
    pass

class NodeDoesNotExistException(Exception):
    pass

class Node:
    def __init__(self, label : Any):
        self.label = label

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return isinstance(other, Node) and self.label == other.label


class Edge:
    def __init__(self, v : Node, w : Node, weight : float):
        self.v = v
        self.w = w
        self.weight = weight


class Graph:
    def __init__(self):
        self.adj : Dict[Node, List[Edge]] = {}

    def add_node(self, node : Node) -> None:
        if not self.node_exists(node):
            self.adj[node] = []
        else:
            raise NodeAlreadyExistsException(f"Node {node.label} already exists.")

    def node_exists(self, node : Node) -> bool:
        return node in self.adj

    def add_edge(self, v : Node, w : Node, weight : float) -> None:
        """
        Adds an edge between two given vertices if none already exists and if the weight is valid.
        :param v: first node
        :param w: second node
        :param weight: weight ranging from 0 to 1 (gaussian similarity function)
        :return: None
        """
        if weight < 0 or weight > 1:
            raise IllegalWeightException("Cannot add weight smaller than 0 or bigger than 1")

        if not self.node_exists(v):
            raise NodeDoesNotExistException(f"Cannot add edge to unexisting node {v.label}")
        if not self.node_exists(w):
            raise NodeDoesNotExistException(f"Cannot add edge to unexisting node {w.label}")

        edge_vw = Edge(v, w, weight)
        edge_wv = Edge(w, v, weight)

        if edge_vw in self.adj.get(v):
            raise EdgeAlreadyExistsException(f"Edge between {v.label} and {w.label} already exists")

        self.adj[v].append(edge_vw)
        self.adj[w].append(edge_wv)

    def edge_exists(self, v : Node, w : Node) -> bool:
        for edge in self.adj.get(v, []):
            if edge.w == w:
                return True
        return False

    def get_neighbors(self, node : Node) -> List[Edge]:
        """
        Returns a list of neighbors of a given
        :param node:
        :return:
        """
        return self.adj.get(node, [])

    def print_graph(self):
        for node in self.adj:
            print(f"Node {node.label} ->", end=" ")
            for neighbor in self.adj.get(node):
                print(f"{neighbor.w.label}", end=" ")

    def from_ppm_image(self, ppm_image_object : PPM, sigma : float):
        cols = ppm_image_object.header.columns
        rows = ppm_image_object.header.rows
        pixel_grid = ppm_image_object.body.pixel_grid

        for r in range(rows):
            print(r)
            for c in range(cols):
                current_pixel = pixel_grid[r][c]
                coordinate = (r, c)
                current_node = Node(coordinate)
                self.adj[current_node] = []

                coordinates_list = {
                    'n' : (r - 1, c),
                    'w' : (r, c - 1),
                    'nw': (r - 1, c - 1),
                    'ne': (r - 1, c + 1)
                }

                if not c - 1 < 0:
                    w_pixel = pixel_grid[r][c - 1]
                    edge_weight = PPM.calculate_similarity(current_pixel, w_pixel, sigma)

                    w_node = Node(coordinates_list['w'])
                    self.add_edge(current_node, w_node, edge_weight)

                    if not r - 1 < 0:
                        nw_pixel = pixel_grid[r - 1][c - 1]
                        edge_weight = PPM.calculate_similarity(current_pixel, nw_pixel, sigma)

                        nw_node = Node(coordinates_list['nw'])
                        self.add_edge(current_node, nw_node, edge_weight)

                if not r - 1 < 0:
                    n_pixel = pixel_grid[r - 1][c]
                    edge_weight = PPM.calculate_similarity(current_pixel, n_pixel, sigma)

                    n_node = Node(coordinates_list['n'])
                    self.add_edge(current_node, n_node, edge_weight)

                    if not c + 1 >= cols:
                        ne_pixel = pixel_grid[r - 1][c + 1]
                        edge_weight = PPM.calculate_similarity(current_pixel, ne_pixel, sigma)

                        ne_node = Node(coordinates_list['ne'])
                        self.add_edge(current_node, ne_node, edge_weight)


if __name__ == '__main__':
    graph = Graph()
    ppm_image = PPM("./slipknot.ppm")
    graph.from_ppm_image(ppm_image, 0.05)
    graph.print_graph()

