from Component import Component
from finger_maker import generate_finger_joints
from intersection_2d_3d import get_intersection_3d

# TODO: cannot set piece1.left = piece2.width
#  references should be related logically

# TODO: handle thickness assertions

c1 = Component(label='c1', thickness=4.3, face='front', center_x=0, center_y=0, center_z=0, width=800, height=600)
c2 = Component(label='c2', thickness=4.3, face='side', left=c1.left, back=c1.back, top=c1.top, bottom=c1.bottom)
c3 = Component(label='c3', thickness=4.3, face='side', right=c1.right, back=c1.back, top=c1.top, bottom=c1.bottom)

c4 = Component(label='c4', thickness=4.3, face='front', left=c1.left, right=c1.right, height=60, back=c1.front,
               bottom=c1.bottom)
c5 = Component('c5', thickness=4.3, face='top', left=c2.left, right=c3.right, bottom=c4.bottom, front=c4.front,
               back=c1.back)

c4.move_up(10)
c4.move_forward(130)

c2.front = c4.front
c3.front = c4.front

# TODO: cannot do (component.left += 10) because it create a self referenc

c2.grow_back(5)
c3.grow_back(5)

c2.grow_front(5)
c3.grow_front(5)

c5.move_up(10)

# c2 = Piece2(label='c2', thickness=1, face='front', right=2, center_x=c1.left)

# c2.move_left(c1._thickness)

# TODO: Strict components to be parts of a group, and references could be made only from the same group

# print(c1.calculated_values, c1.is_well_defined)
# print(c2.calculated_values, c2.is_well_defined)
# print(c3.calculated_values, c3.is_well_defined)
# print(c4.calculated_values, c4.is_well_defined)

items = [c1, c2, c3, c4, c5]


def twos(items):
    for i, item1 in enumerate(items):
        for j, item2 in enumerate(items[i + 1:], start=i + 1):
            yield item1, item2


def threes(items):
    for i, item1 in enumerate(items):
        for j, item2 in enumerate(items[i + 1:], start=i + 1):
            for k, item3 in enumerate(items[j + 1:], start=j + 1):
                yield item1, item2, item3


for i1, i2 in twos(items):
    if i1.face != i2.face:
        continue
    x_intersection, y_intersection, z_intersection = get_intersection_3d(i1.full_bounds, i2.full_bounds)
    if len(x_intersection[0]) == 2 and len(y_intersection[0]) == 2 and len(z_intersection[0]) == 2:
        raise Exception(f'Collision between {i1.label} and {i2.label}')

for i1, i2, i3 in threes(items):
    if i1.face == i2.face or i2.face == i3.face or i3.face == i1.face:
        continue

    x12_intersection, y12_intersection, z12_intersection = get_intersection_3d(i1.full_bounds, i2.full_bounds)
    x23_intersection, y23_intersection, z23_intersection = get_intersection_3d(i2.full_bounds, i3.full_bounds)
    x31_intersection, y31_intersection, z31_intersection = get_intersection_3d(i3.full_bounds, i1.full_bounds)

    pass  # TODO: check if invalid intersection

fingers = []


def detect_fingers_type(i1, i2, i3):
    if ('_WITH_' in i1[2] or '_BEFORE_' in i1[2]) and \
            ('_WITH_' in i2[2] or '_BEFORE_' in i2[2]):
        return 'OUTER', 'INNER'
    if '_WITH_' in i1[2] or '_BEFORE_' in i1[2]:
        return 'OUTER', 'INNER'
    if '_WITH_' in i2[2] or '_BEFORE_' in i2[2]:
        return 'INNER', 'OUTER'
    if '_CONTAINS_' in i3[2]:
        raise Exception(f'Invalid intersection between {i1.label} and {i2.label}')
    if i3[2] in ('A_BEFORE_B', 'B_STARTS_WITH_A', 'A_ENDS_WITH_B'):
        return 'HALF_BOTTOM', 'HALF_UP'
    return 'HALF_UP', 'HALF_BOTTOM'


for i1, i2 in twos(items):
    if i1.face == i2.face:
        continue

    if (i1.face in 'side' and i2.face == 'front') or \
            (i1.face in 'top' and i2.face == 'front') or \
            (i1.face in 'top' and i2.face == 'side'):
        i1, i2 = i2, i1

    i1_full_bounds = i1.full_bounds
    i2_full_bounds = i2.full_bounds

    x_intersection, y_intersection, z_intersection = get_intersection_3d(i1_full_bounds, i2_full_bounds)
    if len(x_intersection[0]) != 2 or len(y_intersection[0]) != 2 or len(z_intersection[0]) != 2:
        continue

    fingers_ = []

    if i1.face == 'front' and i2.face == 'side':
        # print(i1.label, i2.label, "XY", x_intersection, y_intersection, z_intersection)
        finger_type1, finger_type2 = detect_fingers_type(x_intersection, y_intersection, z_intersection)
        fingers_ = [[i1, x_intersection[0], z_intersection[0], 'V', finger_type1],
                    [i2, y_intersection[0], z_intersection[0], 'V', finger_type2]]
    elif i1.face == 'front' and i2.face == 'top':
        # print(i1.label, i2.label, "XZ", x_intersection, y_intersection, z_intersection)
        finger_type1, finger_type2 = detect_fingers_type(z_intersection, y_intersection, x_intersection)
        fingers_ = [[i1, x_intersection[0], z_intersection[0], 'H', finger_type1],
                    [i2, x_intersection[0], y_intersection[0], 'H', finger_type2]]
    elif i1.face == 'side' and i2.face == 'top':
        # print(i1.label, i2.label, "YZ", x_intersection, y_intersection, z_intersection)
        finger_type1, finger_type2 = detect_fingers_type(z_intersection, x_intersection, y_intersection)
        fingers_ = [[i1, y_intersection[0], z_intersection[0], 'H', finger_type1],
                    [i2, x_intersection[0], y_intersection[0], 'V', finger_type2]]

    fingers.extend(fingers_)

# TODO: check how many connected component groups are there

print('<svg xmlns="http://www.w3.org/2000/svg">')
for item in items:
    (x1, x2), (y1, y2) = item.bounds_on_face()
    print('<g>')
    print(f'  <rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" fill="none" stroke="black" />')
    for item_, x_bounds, y_bounds, fingers_direction, finger_config in fingers:
        if item is not item_:
            continue
        if finger_config not in ('INNER', 'OUTER'):
            continue  # TODO: to be removed!
        width = x_bounds[1] - x_bounds[0]
        height = y_bounds[1] - y_bounds[0]
        fingers_total_length = width if fingers_direction == 'H' else height
        finger_data = generate_finger_joints(fingers_total_length, 4.3 * 2, 4.3 * 2,
                                             'space' if finger_config == 'OUTER' else 'finger',
                                             'space' if finger_config == 'OUTER' else 'finger',
                                             "grow_both")
        print('  <g>')
        for finger in finger_data:
            if finger['type'] == 'FINGER':
                continue
            if fingers_direction == 'H':
                print(f'    <rect x="{x_bounds[0] + finger["start"]}" y="{y_bounds[0]}" '
                      f'width="{finger["length"]}" height="{height}" fill="nore" stroke="red" />')
            else:
                print(f'    <rect x="{x_bounds[0]}" y="{y_bounds[0] + finger["start"]}" '
                      f'width="{width}" height="{finger["length"]}" fill="nore" stroke="red" />')
        print('  </g>')

    print(f'</g>')
print("</svg>")
