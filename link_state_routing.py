import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import text_formatting as tf
import heapq


def input_topology() -> dict:
    """
    This function takes in the number of nodes and edges in the topology and returns the topology as a dictionary
    """
    print(tf.bold( "Enter the number of nodes and edges in the topology in the format: <number of nodes> <number of edges>:" ))
     # Loop until the user enters a valid input
    while True:
        print("-> ", end="")
        n_nodes, n_edges = input().split(sep=' ')
        
        # Attempt cast
        try:
            n_nodes, n_edges = int(n_nodes), int(n_edges)
            print(tf.color_green( f'Topology initialized with {n_nodes} nodes and {n_edges} edges.\n' ))
            break # If the input is valid, break out of the loop
        except: 
            print(tf.color_red( "Invalid input. Please re-enter the number of nodes and edges." ))
    
    topology = {}
    
    print(tf.bold( "Enter the edges in the format: <source node> <destination node> <weight>:" ))
    for i in range(n_edges):
        # Loop until the user enters a valid input
        while True:
            print(f'[Edge {i+1}/{n_edges}] -> ', end="")
            src_node, dst_node, weight = input().split(sep=' ')
            
            # Attempt cast
            try:
                weight = int(weight)
                print(tf.color_green( f'Edge added successfully. [{src_node} -> {dst_node} : {weight}]' ))
                break # If the input is valid, break out of the loop
            except:
                print(tf.color_red( "Invalid weight. Please re-enter the edge." ))
        
        if src_node not in topology:
            topology[src_node] = []
        topology[src_node].append( (dst_node, weight) )

    return topology


def create_graph( adjacency_list: dict, type: str='directed' ) -> nx.Graph:
    """
    This function returns a networkx graph object corresponding to the given adjacency list
    """
    if type == 'directed':
        graph = nx.DiGraph()
    elif type == 'undirected':
        graph = nx.Graph()
    else:
        raise ValueError("Invalid graph type. Valid graph types are 'directed' and 'undirected'.")

    for src_node in adjacency_list:
        for dst_node, edge_weight in adjacency_list[src_node]:
            graph.add_edge(src_node, dst_node, weight=edge_weight)
    
    return graph


def visualize_topology( graph: nx.Graph, title: str='' ):
    """
    This function creates and displays a visualization of a given weighted graph
    """
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()


def link_state_routing( graph: nx.Graph ) -> dict:
    """
    This function implements the link state routing algorithm and returns the forwarding table for each node
    """
    # Initialize the forwarding table for each node
    forwarding_table = { node:[] for node in graph.nodes() }

    # Find the shortest path from each node to every other node in directed graph
    for src_node in graph.nodes():
        shortest_path = nx.single_source_dijkstra(graph, src_node)

        # Add the next hop to the forwarding table
        for dst_node in shortest_path[1]:
            if dst_node != src_node:
                forwarding_table[src_node].append( (dst_node, shortest_path[1][dst_node][1]) )

    return forwarding_table


def dijkstra(graph: nx.Graph, src_node: str) -> dict:
    """
    This function implements the dijkstra algorithm to find the shortest path from a source node to every other node in the graph.
    @return: A dictionary containing the shortest path from the source node to every other node in the graph
    """
    # Initialize the shortest path dictionary
    shortest_path = { node: [np.inf, []] for node in graph.nodes() }
    shortest_path[src_node] = [0, []]

    visited = set()

    # Initialize the priority queue
    priority_queue = []
    heapq.heappush(priority_queue, (0, src_node))

    # Loop until the priority queue is empty
    while priority_queue:
        # Pop the node with the smallest distance from the priority queue
        _, node = heapq.heappop(priority_queue)
        visited.add(node)

        neighbors = graph.neighbors(node)
        # Loop through all the neighbors of the node
        for neighbor in neighbors:
            # Calculate the distance to the neighbor
            distance = shortest_path[node][0] + graph[node][neighbor]['weight']

            # If the distance to the neighbor is smaller than the current distance, update the shortest path
            if distance < shortest_path[neighbor][0]:
                shortest_path[neighbor][0] = distance
                shortest_path[neighbor][1] = shortest_path[node][1] + [neighbor]
                heapq.heappush(priority_queue, (distance, neighbor))

    return shortest_path

def link_state_routing_with_dijkstra( graph: nx.Graph ) -> dict:
    """
    This function implements the link state routing algorithm using the dijkstra algorithm and returns the forwarding table for each node
    """
    # Initialize the forwarding table for each node
    forwarding_table = { node:[] for node in graph.nodes() }

    # Find the shortest path from each node to every other node in directed graph
    for src_node in graph.nodes():
        shortest_path = dijkstra(graph, src_node)

        # Add the next hop to the forwarding table
        for dst_node in shortest_path:
            if dst_node != src_node and shortest_path[dst_node][0] != np.inf:
                forwarding_table[src_node].append( (dst_node, shortest_path[dst_node][1][0]) )

    return forwarding_table

def print_forwarding_table( forwarding_table: dict ):
    """
    This function prints the forwarding table for each node in the topology
    """
    for node in forwarding_table:
        print(f'Node {node}: {forwarding_table[node]}')
    print()