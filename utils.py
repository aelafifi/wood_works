def intersect_1d(a, b):
    ax1, ax2 = a
    assert ax1 <= ax2
    bx1, bx2 = b
    assert bx1 <= bx2
    if ax1 > bx2 or ax2 < bx1:
        return "SEPARATE"
    if ax2 == bx1 or ax1 == bx2:
        return "TOUCH"
    return "INTERSECT"


def intersect_2d(a, b):
    ax, ay = a
    bx, by = b
    x_intersect = intersect_1d(ax, bx)
    y_intersect = intersect_1d(ay, by)
    if x_intersect == "SEPARATE" or y_intersect == "SEPARATE":
        return "SEPARATE"
    count_intersect = sum([x_intersect == "INTERSECT", y_intersect == "INTERSECT"])
    return ["TOUCH_POINT", "TOUCH_LINE", "INTERSECT"][count_intersect]


def intersect_3d(a, b):
    ax, ay, az = a
    bx, by, bz = b
    x_intersect = intersect_1d(ax, bx)
    y_intersect = intersect_1d(ay, by)
    z_intersect = intersect_1d(az, bz)
    if x_intersect == "SEPARATE" or y_intersect == "SEPARATE" or z_intersect == "SEPARATE":
        return "SEPARATE"
    count_intersect = sum([x_intersect == "INTERSECT", y_intersect == "INTERSECT", z_intersect == "INTERSECT"])
    return ["TOUCH_POINT", "TOUCH_LINE", "TOUCH_AREA", "INTERSECT"][count_intersect]


def get_intersection_1d(a, b):
    ax1, ax2 = a
    assert ax1 <= ax2
    bx1, bx2 = b
    assert bx1 <= bx2
    if ax1 > bx2 or ax2 < bx1:
        return []
    if ax2 == bx1 or ax1 == bx2:
        return [max(ax1, bx1)]
    return [max(ax1, bx1), min(ax2, bx2)]


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


def detailed_intersect_1d(a, b):
    ax1, ax2 = a
    bx1, bx2 = b
    if ax1 > bx2 or ax2 < bx1:
        return "SEPARATE"
    if ax2 == bx1 or ax1 == bx2:
        return "TOUCHING_SURFACE"
    if ax1 == bx1:
        if ax2 < bx2:
            return "B_CONTAINS_A"
        elif ax2 > bx2:
            return "A_CONTAINS_B"
        return "IDENTICAL"
