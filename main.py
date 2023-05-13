# use the networkx package to simulate the link state routing algorithm

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import text_formatting as tf


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


def create_graph( adjacency_list: dict ) -> nx.Graph:
    """
    This function returns a networkx graph object corresponding to the given adjacency list
    """
    graph = nx.DiGraph()
    # nodes_set = set( list(adjacency_list.keys()) )
    # for node in adjacency_list:
    #     for dst_node, _ in adjacency_list[node]:
    #         nodes_set.add(dst_node)

    # for node in nodes_set:
    #     graph.add_node(node)

    for src_node in adjacency_list:
        for dst_node, edge_weight in adjacency_list[src_node]:
            graph.add_edge(src_node, dst_node, weight=edge_weight)
    
    return graph


def visualize_topology( graph: nx.Graph ):
    """
    This function creates and displays a visualization of a given weighted graph
    """
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
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
        print(f'\nshortest_path for src_node={src_node}={shortest_path}')

        # Add the next hop to the forwarding table
        for dst_node in shortest_path[1]:
            if dst_node != src_node:
                forwarding_table[src_node].append( (dst_node, shortest_path[1][dst_node][1]) )

    return forwarding_table


def dijkstra( graph: nx.Graph, src_node: str ):
    """
    This function implements the dijkstra algorithm and returns the shortest path from a source node to every other node
    """
    # Initialize the shortest path to each node
    shortest_path = { node:(None, np.inf) for node in graph.nodes() }
    shortest_path[src_node] = (src_node, 0)

    # Initialize the set of visited nodes
    visited_nodes = set()

    # Loop until all the nodes have been visited
    # Here, a for loop is used to ensure that the loop terminates even if the graph is disconnected
    for _ in range(len(graph.nodes())):
        # Find the unvisited node with the shortest path
        min_node, min_dist = None, np.inf
        for node in shortest_path:
            if node not in visited_nodes and shortest_path[node][1] < min_dist:
                min_node, min_dist = node, shortest_path[node][1]

        if min_node is None: break
        
        # Add the min node to the visited nodes
        visited_nodes.add(min_node)

        # Update the shortest path to each node
        for node in graph.neighbors(min_node):
            if node not in visited_nodes:
                dist = min_dist + graph[min_node][node]['weight']
                if dist < shortest_path[node][1]:
                    shortest_path[node] = (min_node, dist)

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
        print(f'\nshortest_path for src_node={src_node}={shortest_path}')

        # Add the next hop to the forwarding table
        for dst_node in shortest_path:
            if dst_node != src_node:
                forwarding_table[src_node].append( (dst_node, shortest_path[dst_node][1]) )

    return forwarding_table

def print_forwarding_table( forwarding_table: dict ):
    """
    This function prints the forwarding table for each node in the topology
    """
    print("Forwarding table for each node:")
    for node in forwarding_table:
        print(f'Node {node}: {forwarding_table[node]}')
    print()


if __name__ == '__main__':
    # Take in the topology from the user
    topology = input_topology()

    # Create a graph object from the topology
    graph = create_graph(topology)

    # Find the forwarding table for each node
    forwarding_table = link_state_routing(graph)
    dijkstra_forwarding_table = link_state_routing_with_dijkstra(graph)

    # Print the forwarding table for each node
    print("Forwarding table for each node:")
    print_forwarding_table(forwarding_table)
    print()
    print("Forwarding table for each node (using dijkstra):")
    print_forwarding_table(dijkstra_forwarding_table)

    # Visualize the topology
    visualize_topology(graph)