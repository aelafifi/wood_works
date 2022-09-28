from intersection_1d import get_intersection_1d


def get_intersection_2d(a, b):
    ax, ay = a
    bx, by = b
    x_intersect = get_intersection_1d(ax, bx)
    y_intersect = get_intersection_1d(ay, by)
    return [x_intersect, y_intersect]


def get_intersection_3d(a, b):
    ax, ay, az = a
    bx, by, bz = b
    x_intersect = get_intersection_1d(ax, bx)
    y_intersect = get_intersection_1d(ay, by)
    z_intersect = get_intersection_1d(az, bz)
    return [x_intersect, y_intersect, z_intersect]
