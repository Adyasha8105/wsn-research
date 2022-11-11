import matplotlib.pyplot as plt

def node_simulation(coord, s, d, r, chosen_path, population, forward_zone):
    """
    Simulate the nodes in the network
    """
    
    def each_line_plot(path):
        x_path = []
        y_path = []
        for i in path:
            x_path.append(i[0])
            y_path.append(i[1])
        return x_path, y_path
        
    plt.xlim = max(s[0], d[0])
    plt.ylim = max(s[1], d[1])

    x_axis = [s[0]]
    y_axis = [s[1]]
    axes = plt.subplot()
    for i in coord:
        x_axis.append(i[0])
        y_axis.append(i[1])
    x_axis.append(d[0])
    y_axis.append(d[1])

    x_path, y_path = each_line_plot(chosen_path)

    fig = plt.figure(1)
    
    # plotting the position of nodes
    axes = fig.add_subplot(111)
    axes.scatter(x_axis, y_axis, s=10)

    # plotting the optimal path
    axes = fig.add_subplot(111)
    axes.plot(x_path, y_path, color='red', linewidth=2.0)

    # plotting the remaining paths
    for pop in population:
        pop_x_path, pop_y_path = each_line_plot(pop)
        plt.plot(pop_x_path, pop_y_path, linewidth=0.2)

    axes = fig.add_subplot(111)
    source = plt.Circle(s, r, fill=False)
    destination = plt.Circle(d, r, fill=False)
    axes.set_aspect(1)
    axes.add_artist(source)
    axes.add_artist(destination)
    forward_zone_simulation(coord, s, d, r, forward_zone)
    plt.show()

def forward_zone_simulation(coord, s, d, r, forward_zone):
    # Arranging coordinates in the right order
    temp = forward_zone[1], forward_zone[3]
    forward_zone[3], forward_zone[1] = temp

    temp = forward_zone[1], forward_zone[2]
    forward_zone[2], forward_zone[1] = temp

    # Appending the first element to create a closed loop
    forward_zone.append(forward_zone[0])
    print(forward_zone)

    fig = plt.figure(2)

    # Plotting the source and destination nodes
    axes = fig.add_subplot(111)
    temp_list = [s, d]
    node_x, node_y = zip(*temp_list)
    axes.scatter(node_x, node_y, color='red', s=20)

    # Plotting the range of source and destination nodes
    axes = fig.add_subplot(111)
    source = plt.Circle(s, r, fill=False)
    destination = plt.Circle(d, r, fill=False)
    axes.set_aspect(1)
    axes.add_artist(source)
    axes.add_artist(destination)

    # Plotting the nodes 
    axes = fig.add_subplot(111)
    nodes_x, nodes_y = zip(*coord)
    axes.scatter(nodes_x, nodes_y, s=10)

    # Plotting forward zone
    axes = fig.add_subplot(111)
    xs, ys = zip(*forward_zone)
    axes.plot(xs, ys)
