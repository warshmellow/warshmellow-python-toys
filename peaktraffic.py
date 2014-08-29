"""
Author: warshmellow

Implements a solution to the Facebook Engineering Peak Traffic Challenge
using the Bron-Kerbosch algorithm (no pivotting, with degeneracy ordering)
for finding maximal cliques of a graph. The goal was to find the maximum
clusters, (read: maximal cliques, or maximal connected subgraphs, of a graph)
of size >= 3 of an undirected graph whose vertices are email addresses and
where there is an edge between two addresses iff there is a message sent from
one to the other and vice versa. The data is given as a series of lines:
timestamp sender recipient.

The solution:
File data is parsed and filtered into a set of sets {sender, recipient},
where both sender and recipient have sent and received messages from each
other. This data is read into a undirected graph, which is implemented
in class Graph as an adjacency map using Python sets. This graph is held
in a Graph object, and we can run the Bron-Kerbosch algorithm on the graph
by calling max_cliques() on the Graph, which returns cliques as sets
of vertices.
"""


import sys


class Graph(object):
    """
    Undirected graph implemented as an adjacency-map, with a set
    _adjacency_map holding the vertices as keys, with incidence sets holding
    vertices, as values. Edges are implicit and double counted.
    """
    def __init__(self):
        self._adjacency_map = {}

    def add_pair(self, u, v):
        if u in self._adjacency_map:
            self._adjacency_map[u].add(v)
        else:
            self._adjacency_map[u] = {v}

        if v in self._adjacency_map:
            self._adjacency_map[v].add(u)
        else:
            self._adjacency_map[v] = {u}

        return u, v

    def neighbors(self, key):
        return frozenset(self._adjacency_map[key])

    def degree(self, key):
        return len(self.neighbors(key))

    def degeneracy_ordering(self):
        """
        Returns a list of the vertices in ascending degeneracy ordering.
        From wikipedia: "The degeneracy of a graph G is the smallest number
        d such that every subgraph of G has a vertex with degree d or less.
        Every graph has a degeneracy ordering, an ordering of the vertices
        such that each vertex has d or fewer neighbors that come later in
        the ordering; a degeneracy ordering may be found in linear time
        by repeatedly selecting the vertex of minimum degree among the
        remaining vertices."

        This is to minimize the number of recursive calls made to
        _bron_kerbosch().
        """
        return sorted(self._adjacency_map, key=self.degree)

    def vertices(self):
        return self._adjacency_map.keys()

    def max_cliques(self):
        """
        Returns a list of all maximal cliques, each clique a frozenset.
        Top-level of Bron-Kerbosch, with recusive step in _bron_kerbosch().
        """
        possible = frozenset(self.vertices())
        acc = frozenset()
        excluded = frozenset()
        cliques = []
        degeneracy_ordered_vertices = self.degeneracy_ordering()
        for v in degeneracy_ordered_vertices:
            neighbors_of_v = self.neighbors(v)
            self._bron_kerbosch(
                acc.union({v}),
                possible.intersection(neighbors_of_v),
                excluded.intersection(neighbors_of_v),
                cliques)
            possible = possible.difference({v})
            excluded = excluded.union({v})
        return cliques

    def _bron_kerbosch(self, acc, possible, excluded, cliques):
        """
        Recursive step of Bron-Kerbosch, called in max_cliques().
        Appends maximum clique (as a set of vertices) to cliques.
        Returns None.
        """
        if len(possible) == 0 and len(excluded) == 0:
            cliques.append(acc)
        for v in iter(possible):
            neighbors_of_v = self.neighbors(v)
            self._bron_kerbosch(
                acc.union({v}),
                possible.intersection(neighbors_of_v),
                excluded.intersection(neighbors_of_v),
                cliques)
            possible = possible.difference({v})
            excluded = excluded.union({v})


def main():
    """
    Parses data from file, loads into graph, runs Bron-Kerbosch,
    and pretty prints the maximal cliques, sorted
    """
    with open(sys.argv[1], 'r') as test_cases:

        # Initialize possible pairs, pairs, and social graph Graph
        possible_pairs = set()
        pairs = set()
        social_graph = Graph()

        # Find true pairs of sender, recipient and vice versa for graph
        for test in test_cases:
            # Parse line into sender, recipient
            parsed_line = test.rstrip().split('\t')
            sender, recipient = parsed_line[1], parsed_line[2]

            # Determine which sender, recipient reciprocal pairs exist
            # Candidates are tested against possible pairs
            # True pairs are stored in pairs
            if (recipient, sender) in possible_pairs:
                pairs.add(frozenset({x for x in (sender, recipient)}))
            else:
                possible_pairs.add((sender, recipient))

        # From pairs, add to social graph
        for pair in pairs:
            u, v = pair
            social_graph.add_pair(u, v)

        # Compute maximal cliques of size >= 3 only
        max_cliques_gt_3 = [
            clique
            for clique in social_graph.max_cliques()
            if len(clique) >= 3]

        # Sort maximal cliques, ascending, and pretty print
        for cluster in sorted(map(
                lambda x: ", ".join(sorted(x)),
                max_cliques_gt_3)):
            print cluster


if __name__ == '__main__':
    main()
