def get_intersection_1d(a, b):
    ax1, ax2 = a
    bx1, bx2 = b

    assert ax1 < ax2
    assert bx1 < bx2

    if ax1 > bx2 or ax2 < bx1:
        intersection = []
    elif ax2 == bx1 or ax1 == bx2:
        intersection = [round(max(ax1, bx1), 12)]
    else:
        intersection = [round(max(ax1, bx1), 12), round(min(ax2, bx2), 12)]

    status = len(intersection) - 1

    if status == -1:
        if ax1 < bx1:
            positioning = "A_BEFORE_B"
        else:
            positioning = "B_BEFORE_A"
    elif status == 0:
        if ax1 < bx1:
            positioning = "A_BEFORE_B"
        else:
            positioning = "B_BEFORE_A"
    elif status == 1:
        if ax1 == bx1 and ax2 == bx2:
            positioning = "A_EQUALS_B"
        elif ax1 < bx1 < bx2 < ax2:
            positioning = "A_CONTAINS_B"
        elif bx1 < ax1 < ax2 < bx2:
            positioning = "B_CONTAINS_A"
        elif ax1 < bx1 < ax2 < bx2:
            positioning = "A_BEFORE_B"
        elif bx1 < ax1 < bx2 < ax2:
            positioning = "B_BEFORE_A"
        elif ax1 == bx1:
            if ax2 < bx2:
                positioning = "B_STARTS_WITH_A"
            else:
                positioning = "A_STARTS_WITH_B"
        elif ax2 == bx2:
            if ax1 < bx1:
                positioning = "A_ENDS_WITH_B"
            else:
                positioning = "B_ENDS_WITH_A"
        else:
            positioning = "OVERLAP"
    else:
        positioning = "ERROR"

    return intersection, status, positioning


if __name__ == "__main__":
    from itertools import permutations


    def draw_line(x1: int, x2: int):
        line_str = ""
        for i in range(max(x1, x2) + 1):
            if i == x1 or i == x2:
                line_str += "|"
            elif i > x1 and i < x2:
                line_str += "-"
            else:
                line_str += " "
        return line_str


    done = []
    for (ax1, ax2, bx1, bx2) in permutations([0, 0, 5, 5, 10, 10, 15, 15, 20, 20], 4):
        if ax1 >= ax2 or bx1 >= bx2:
            continue
        if (ax1, ax2, bx1, bx2) in done:
            continue
        done.append((ax1, ax2, bx1, bx2))
        # print(ax1, ax2, bx1, bx2)
        print("A:", draw_line(ax1, ax2))
        print("B:", draw_line(bx1, bx2))
        print(get_intersection_1d((ax1, ax2), (bx1, bx2)))
        print()
