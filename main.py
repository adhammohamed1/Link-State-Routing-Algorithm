from link_state_routing import *


if __name__ == '__main__':
    # Take in the topology from the user
    topology = input_topology()

    # Create graph objects from the topology
    directed_graph = create_graph(topology, type='directed')
    undirected_graph = create_graph(topology, type='undirected')

    ##############################################################################################################
    print(tf.bold("\nDirected Graph"))

    # Find the forwarding table for each node in the directed graph
    forwarding_table_dir = link_state_routing(directed_graph)
    dijkstra_forwarding_table_dir = link_state_routing_with_dijkstra(directed_graph)

    print("Forwarding table for each node (using built-in function):")
    print_forwarding_table(forwarding_table_dir)
    print("Forwarding table for each node (using dijkstra):")
    print_forwarding_table(dijkstra_forwarding_table_dir)

    # Visualize the directed topology
    print("Generating the directed graph visualization...")
    visualize_topology(directed_graph, title="Directed Graph")

    ##############################################################################################################
    print(tf.bold("\nUndirected Graph"))

    # Find the forwarding table for each node in the undirected graph
    forwarding_table_undir = link_state_routing(undirected_graph)
    dijkstra_forwarding_table_undir = link_state_routing_with_dijkstra(undirected_graph)

    print("Forwarding table for each node (using built-in function):")
    print_forwarding_table(forwarding_table_undir)
    print("Forwarding table for each node (using dijkstra):")
    print_forwarding_table(dijkstra_forwarding_table_undir)

    # Visualize the undirected topology
    print("Generating the undirected graph visualization...")
    visualize_topology(undirected_graph, title="Undirected Graph")