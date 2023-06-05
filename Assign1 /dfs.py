def find_path(neighbour_fn,
              start,
              goal,
              visited=None,
              reachable=lambda pos: True,
              depth=100000):
    """
    Returns the path between two nodes as a list of nodes using depth first search.
    If no path can be found, an empty list is returned.
    """
    # Initialize the stack with the start node
    storage_place = [[start]]

    # Loop until the stack is empty
    while storage_place:
        # Pop the last element from the stack
        cur_path = storage_place.pop(-1)
        cur_node = cur_path[-1]

        # Mark the current node as visited
        visited.append(cur_node)

        # Check if the current node is the goal node
        if cur_node == goal:
            return cur_path

        # Check if the maximum depth has been reached
        if len(cur_path) >= depth:
            continue

        # Loop over the neighbours of the current node
        for neighbour in neighbour_fn(cur_node):
            # Check if the neighbour has not been visited and is reachable
            if neighbour not in visited and reachable(neighbour):
                # Add the neighbour to the path and push it to the stack
                update_path = cur_path + [neighbour]
                storage_place.append(update_path)

    # If no path is found, return an empty list
    return []




    # if visited is None:
    #     visited = []

    # # Check if the start node is the goal node
    # if start == goal:
    #     return [start]

    # # Check if the maximum depth has been reached
    # if depth <= 0:
    #     return []

    # # Mark the start node as visited
    # visited.append(start)

    # # Loop over the neighbours of the start node
    # for neighbour in neighbour_fn(start):
    #     # Check if the neighbour has not been visited and is reachable
    #     if neighbour not in visited and reachable(neighbour):
    #         # Recursively search for a path from the neighbour to the goal
    #         path = find_path(neighbour_fn, neighbour, goal, visited, reachable, depth - 1)
    #         # If a path is found, add the start node to the beginning of the path and return it
    #         if path:
    #             return [start] + path
    # # If no path is found, return None
    # return []
