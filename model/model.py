import copy

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.lista_rifugi = []
        self.rifugi_map = {}
        self.lista_sentieri = []
        self.sentieri_map = {}

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        self.G.clear()

        self.lista_rifugi = DAO.get_rifugi(year)
        self.rifugi_map = {r.id: r for r in self.lista_rifugi}
        for id, r in self.rifugi_map.items():
            self.G.add_node(r)

        self.lista_sentieri = DAO.read_sentieri(year)
        self.sentieri_map = {s.idSentiero: (s.id1, s.id2) for s in self.lista_sentieri}
        for s in self.lista_sentieri:
            self.G.add_edge(self.rifugi_map[s.id1], self.rifugi_map[s.id2])

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        return self.lista_rifugi

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        return len(list(self.G.neighbors(node)))

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO

        #DFS_TREE()
        dfs = nx.dfs_tree(self.G, start)
        lista_dfs = [n for n in dfs.nodes if n != start]

        #BFS_TREE()
        bfs = nx.bfs_tree(self.G, start)
        lista_bfs = [n for n in bfs.nodes if n != start]

        #ALGORITMO ITERATIVO
        visited_iter = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited_iter:
                visited_iter.add(node)
                for neigh in self.G.neighbors(node):
                    if neigh not in visited_iter:
                        stack.append(neigh)

        visited_iter.discard(start)
        visited_iter = list(visited_iter)

        #ALGORITMO RICORSIVO
        visited_set_ric = set()

        def dfs(node):
            visited_set_ric.add(node)
            for neigh in self.G.neighbors(node):
                if neigh not in visited_set_ric:
                    dfs(neigh)
        dfs(start)
        visited_ric = list(visited_set_ric)
        visited_ric.remove(start)

        '''
        Ora possimamo scegliere quello che vogliamo tra:
        lista_dfs, lista_bfs, visited_iter, visited_ric
        '''
        return visited_ric
