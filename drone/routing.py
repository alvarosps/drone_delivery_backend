import heapq

def calculate_shortest_path(graph, start, end):
    # Check if start and end are valid nodes in the graph
    if start not in graph or end not in graph:
        return None, float('inf')  # Invalid start or end

    # Create a dictionary to store the shortest path to each node
    shortest_paths = {start: (None, 0)}
    # Create a priority queue to store the nodes to be visited
    queue = [(0, start)]

    while queue:
        # Get the node with the smallest weight
        current_weight, current_node = heapq.heappop(queue)

        # If the current node is the end node, we have found the shortest path
        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                next_node = shortest_paths[current_node][0]
                current_node = next_node
            # Reverse the path
            path = path[::-1]
            return path, current_weight

        # If the current node has not been visited yet
        if current_weight <= shortest_paths[current_node][1]:
            # Visit each neighbor of the current node
            for neighbor, weight in graph[current_node].items():
                # Calculate the weight to the neighbor
                total_weight = current_weight + weight
                # If the neighbor has not been visited yet or if we have found a shorter path to the neighbor
                if neighbor not in shortest_paths or total_weight < shortest_paths[neighbor][1]:
                    # Update the shortest path to the neighbor
                    shortest_paths[neighbor] = (current_node, total_weight)
                    # Add the neighbor to the queue
                    heapq.heappush(queue, (total_weight, neighbor))

    return None, float('inf')  # No path found
