
def sweep_and_prune_algorithm(points, axis='x'):
    if axis == 'x':
        sorted_by_x = sorted(points, key=lambda pointa: pointa.position.x)
    elif axis == 'y':
        sorted_by_x = sorted(points, key=lambda pointa: pointa.position.y)
    else:
        raise

    possible_intersections = []
    active_interval = []
    if axis == 'x':
        sorted_plus_interval = [(point, point.position.x - point.c_perception/2,
                                point.position.x + point.c_perception/2) for point in sorted_by_x]
    elif axis == 'y':
        sorted_plus_interval = [(point, point.position.x - point.c_perception/2,
                                point.position.x + point.c_perception/2) for point in sorted_by_x]
    else:
        raise
    new_active = []
    for point in sorted_plus_interval:

        if not active_interval:
            active_interval = [point, ]
        else:
            i = 0
            for j in active_interval:

                if point[1] < j[2]:
                    i += 1
                    if abs(point[0].position.y - j[0].position.y) <= j[0].c_perception:
                        possible_intersections.append([point[0], j[0]])
                        possible_intersections.append([j[0], point[0]])
                if point[1] > j[2]:
                    i = 0
                    break
            if i == 0:
                new_active = [point, ]
            if i > 0:
                new_active.append(point)
            active_interval = new_active

    possible_intersections.sort(key=lambda x: x[0].position.x)
    return possible_intersections


def intersect(a, b):
    c = [tuple(i) for i in a]
    g = [tuple(i) for i in b]
    c = set(c)
    g = set(g)
    return list(c & g)



