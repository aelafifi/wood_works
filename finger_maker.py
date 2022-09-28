from math import ceil, floor
from typing import List


class StartEndOptions:
    FINGER = "finger"
    SPACE = "space"
    HALF_FINGER = "half_finger"
    HALF_SPACE = "half_space"

    @classmethod
    def get_options(cls):
        print({v for k, v in cls.__dict__.items() if not k.startswith('_')})


class RoundingOptions:
    GROW_FINGER = "grow_finger"
    GROW_SPACE = "grow_space"
    GROW_BOTH = "grow_both"
    SHRINK_FINGER = "shrink_finger"
    SHRINK_SPACE = "shrink_space"
    SHRINK_BOTH = "shrink_both"

    @classmethod
    def get_options(cls):
        print({v for k, v in cls.__dict__.items() if not k.startswith('_')})


def generate_finger_joints(total_length, finger_length, space_length, start_with, end_with, rounding):
    start_type = "finger" if start_with in ["finger", "half_finger"] else "space"
    end_type = "finger" if end_with in ["finger", "half_finger"] else "space"
    rounding_type = "grow" if rounding in ["grow_finger", "grow_space", "grow_both"] else "shrink"
    total_finger_count = 0
    total_fingers_length = 0
    total_space_count = 0
    total_spaces_length = 0
    couple_length = finger_length + space_length

    if start_with == "finger":
        total_fingers_length += finger_length
        total_finger_count += 1
    elif start_with == "space":
        total_spaces_length += space_length
        total_space_count += 1
    elif start_with == "half_finger":
        total_fingers_length += finger_length / 2
        total_finger_count += 0.5
    elif start_with == "half_space":
        total_spaces_length += space_length / 2
        total_space_count += 0.5
    else:
        raise ValueError(f'Invalid start_with: {start_with}')

    if end_with == "finger":
        total_fingers_length += finger_length
        total_finger_count += 1
    elif end_with == "space":
        total_spaces_length += space_length
        total_space_count += 1
    elif end_with == "half_finger":
        total_fingers_length += finger_length / 2
        total_finger_count += 0.5
    elif end_with == "half_space":
        total_spaces_length += space_length / 2
        total_space_count += 0.5
    else:
        raise ValueError(f'Invalid end_with: {end_with}')

    if start_type == end_type:
        if start_type == "finger":
            total_spaces_length += space_length
            total_space_count += 1
        else:
            total_fingers_length += finger_length
            total_finger_count += 1

    total_added_length = total_fingers_length + total_spaces_length
    remaining_length = total_length - total_added_length

    if remaining_length < 0:
        raise ValueError(f'Not enough space for the given finger and space lengths')

    real_count_of_couples = remaining_length / couple_length
    num_of_couples = floor(real_count_of_couples) if rounding_type == "grow" else ceil(real_count_of_couples)

    total_fingers_length += num_of_couples * finger_length
    total_spaces_length += num_of_couples * space_length

    total_finger_count += num_of_couples
    total_space_count += num_of_couples

    total_length_diff = abs(total_length - (total_fingers_length + total_spaces_length))
    total_consumed_length = total_fingers_length + total_spaces_length
    if rounding == "grow_finger":
        finger_length += total_length_diff / total_finger_count
        total_fingers_length += total_length_diff
    elif rounding == "grow_space":
        space_length += total_length_diff / total_space_count
        total_spaces_length += total_length_diff
    elif rounding == "grow_both":  # TODO: add options for even/relative growth
        grow_for_fingers = total_length_diff / total_consumed_length * total_fingers_length / total_finger_count
        grow_for_spaces = total_length_diff / total_consumed_length * total_spaces_length / total_space_count
        finger_length += grow_for_fingers
        space_length += grow_for_spaces
        total_fingers_length += grow_for_fingers * total_finger_count
        total_spaces_length += grow_for_spaces * total_space_count
    elif rounding == "shrink_finger":
        finger_length -= total_length_diff / total_finger_count
        total_fingers_length -= total_length_diff
    elif rounding == "shrink_space":
        space_length -= total_length_diff / total_space_count
        total_spaces_length -= total_length_diff
    elif rounding == "shrink_both":
        grow_for_fingers = total_length_diff / total_consumed_length * total_fingers_length / total_finger_count
        grow_for_spaces = total_length_diff / total_consumed_length * total_spaces_length / total_space_count
        finger_length -= grow_for_fingers
        space_length -= grow_for_spaces
        total_fingers_length -= grow_for_fingers * total_finger_count
        total_spaces_length -= grow_for_spaces * total_space_count
    else:
        raise ValueError(f'Invalid rounding: {rounding}')

    parts = []

    position = 0
    if start_with == "finger":
        parts.append(("FINGER", finger_length, position, position + finger_length))
        position += finger_length
    elif start_with == "space":
        parts.append(("SPACE", space_length, position, position + space_length))
        position += space_length
    elif start_with == "half_finger":
        parts.append(("FINGER", finger_length / 2, position, position + finger_length / 2))
        position += finger_length / 2
    elif start_with == "half_space":
        parts.append(("SPACE", space_length / 2, position, position + space_length / 2))
        position += space_length / 2

    if start_type == end_type:
        if start_type == "finger":
            parts.append(("SPACE", space_length, position, position + space_length))
            position += space_length
        else:
            parts.append(("FINGER", finger_length, position, position + finger_length))
            position += finger_length

    for i in range(num_of_couples):
        if parts[-1][0] == "FINGER":
            parts.append(("SPACE", space_length, position, position + space_length))
            position += space_length
            parts.append(("FINGER", finger_length, position, position + finger_length))
            position += finger_length
        else:
            parts.append(("FINGER", finger_length, position, position + finger_length))
            position += finger_length
            parts.append(("SPACE", space_length, position, position + space_length))
            position += space_length

    if end_with == "finger":
        parts.append(("FINGER", finger_length, position, position + finger_length))
        position += finger_length
    elif end_with == "space":
        parts.append(("SPACE", space_length, position, position + space_length))
        position += space_length
    elif end_with == "half_finger":
        parts.append(("FINGER", finger_length / 2, position, position + finger_length / 2))
        position += finger_length / 2
    elif end_with == "half_space":
        parts.append(("SPACE", space_length / 2, position, position + space_length / 2))
        position += space_length / 2

    return [{
        'type': p[0],
        'length': round(p[1], 12),
        'start': round(p[2], 12),
        'end': round(p[3], 12),
        'portion': round(p[1] / total_length, 12),
        'start_time': round(p[2] / total_length, 12),
        'end_time': round(p[3] / total_length, 12),
    } for p in parts]


def flip_finger_joints(finger_joints: List[dict]):
    total_length = finger_joints[-1]['end']
    for joint in finger_joints:
        joint['start'], joint['end'] = total_length - joint['end'], total_length - joint['start']
        joint['start_time'], joint['end_time'] = 1 - joint['end_time'], 1 - joint['start_time']
    return finger_joints[::-1]


def swap_finger_joints(finger_joints: List[dict]):
    for joint in finger_joints:
        joint['type'] = 'SPACE' if joint['type'] == 'FINGER' else 'FINGER'
    return finger_joints
