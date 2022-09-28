from typing import Union, Optional

from Reference import Reference


class Component(object):
    __axis_names = [['left', 'center_x', 'right', 'width'],
                    ['front', 'center_y', 'back', 'depth'],
                    ['bottom', 'center_z', 'top', 'height']]

    __axes = ["x", "y", "z"]

    __faces = ["side", "front", "top"]

    def __init__(self, /, label: str, thickness: Union[int, float], face: str,
                 width: Optional[Union[int, float, Reference]] = None,
                 height: Optional[Union[int, float, Reference]] = None,
                 depth: Optional[Union[int, float, Reference]] = None,
                 left: Optional[Union[int, float, Reference]] = None,
                 top: Optional[Union[int, float, Reference]] = None,
                 right: Optional[Union[int, float, Reference]] = None,
                 bottom: Optional[Union[int, float, Reference]] = None,
                 front: Optional[Union[int, float, Reference]] = None,
                 back: Optional[Union[int, float, Reference]] = None,
                 center_x: Optional[Union[int, float, Reference]] = None,
                 center_y: Optional[Union[int, float, Reference]] = None,
                 center_z: Optional[Union[int, float, Reference]] = None):
        super(Component, self).__init__()

        self.__user_values = [[left, center_x, right, width],
                              [front, center_y, back, depth],
                              [bottom, center_z, top, height]]

        assert thickness > 0, 'Thickness must be positive'
        self._thickness = thickness

        self._label = label

        assert face in ("side", "top", "front"), 'Face must be side, top or front'
        self._face = face

        self.__offset = [0, 0, 0]

        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if depth is not None:
            self.depth = depth

        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.front = front
        self.back = back
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z

    @property
    def label(self):
        return self._label

    @property
    def thickness(self):
        return self._thickness

    @property
    def face(self):
        return self._face

    def __repr__(self):
        return f'Piece<{self._label}>'

    def __get_reference(self, i: int, j: int):
        return Reference(self, self.__class__.__axis_names[i][j])

    def get_user_value(self, i: int, j: int):
        return self.__user_values[i][j]

    def get_conceptual_value(self, i: int, j: int):
        if self.__class__.__faces[i] == self._face and j == 3:
            return self._thickness
        return self.__user_values[i][j]

    def get_real_value(self, i: int, j: int):
        user_value = self.get_conceptual_value(i, j)
        if isinstance(user_value, Reference):
            return user_value.value
        return user_value

    def __set_user_value(self, i: int, j: int, value: Union[int, float, Reference]):
        if j == 3 and self._face == self.__faces[i]:
            raise NotImplementedError("Unable to set this value on the selected component face")

        # If None, set to None
        if value is None:
            self.__user_values[i][j] = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self.__user_values[i][j] = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_conceptually_over_defined_on_axis(i), "Can't set more than 2 constraints on the same axis"

    def conceptual_values_on_axis(self, axis: int):
        values = [*self.__user_values[axis]]
        if self._face == self.__faces[axis]:
            values[-1] = self._thickness
        return values

    def real_values_on_axis(self, axis: int):
        values = self.conceptual_values_on_axis(axis)
        return [v.value if isinstance(v, Reference) else v for v in values]

    def count_conceptual_defined_on_axis(self, axis: int):
        return sum(1 for value in self.conceptual_values_on_axis(axis) if value is not None)

    def count_real_defined_on_axis(self, axis: int):
        return sum(1 for value in self.real_values_on_axis(axis) if value is not None)

    def is_conceptually_over_defined_on_axis(self, axis: int):
        return self.count_conceptual_defined_on_axis(axis) > 2

    def is_really_over_defined_on_axis(self, axis: int):
        return self.count_real_defined_on_axis(axis) > 2

    def is_conceptually_under_defined_on_axis(self, axis: int):
        return self.count_conceptual_defined_on_axis(axis) < 2

    def is_really_under_defined_on_axis(self, axis: int):
        return self.count_real_defined_on_axis(axis) < 2

    def is_conceptually_well_defined_on_axis(self, axis: int):
        return self.count_conceptual_defined_on_axis(axis) == 2

    def is_really_well_defined_on_axis(self, axis: int):
        return self.count_real_defined_on_axis(axis) == 2

    def __get_calculated_value(self, axis: int, index: int):
        return self.calculated_values_on_axis(axis)[index]

    def calculated_values_on_axis(self, axis: int):
        values = [self.get_real_value(axis, i) for i in range(4)]
        count_values = sum(1 for value in values if value is not None)
        if count_values < 2:
            return values
        elif count_values > 2:
            raise ValueError("More than 2 values defined on axis")

        # values = [left, center, right, width]
        if values[0] is None:
            if values[1] is None:
                values[0] = values[2] - values[3]
                values[1] = values[2] - values[3] / 2
            elif values[2] is None:
                values[0] = values[1] - values[3] / 2
                values[2] = values[1] + values[3] / 2
            else:
                values[3] = (values[2] - values[1]) * 2
                values[0] = values[2] - values[3]
        elif values[1] is None:
            if values[2] is None:
                values[1] = values[0] + values[3] / 2
                values[2] = values[0] + values[3]
            else:
                values[1] = (values[2] + values[0]) / 2
                values[3] = values[2] - values[0]
        else:
            values[3] = (values[1] - values[0]) * 2
            values[2] = values[0] + values[3]

        if values[0] > values[2]:
            values[0], values[2] = values[2], values[0]
            values[1] = (values[0] + values[2]) / 2
            values[3] = values[2] - values[0]

        values[0] += self.__offset[axis]
        values[1] += self.__offset[axis]
        values[2] += self.__offset[axis]

        return values

    @property
    def is_conceptually_over_defined(self):
        return any(self.is_conceptually_over_defined_on_axis(i) for i in range(3))

    @property
    def is_really_over_defined(self):
        return any(self.is_really_over_defined_on_axis(i) for i in range(3))

    @property
    def is_conceptually_under_defined(self):
        return any(self.is_conceptually_under_defined_on_axis(i) for i in range(3))

    @property
    def is_really_under_defined(self):
        return any(self.is_really_under_defined_on_axis(i) for i in range(3))

    @property
    def is_conceptually_well_defined(self):
        return all(self.is_conceptually_well_defined_on_axis(i) for i in range(3))

    @property
    def is_really_well_defined(self):
        return all(self.is_really_well_defined_on_axis(i) for i in range(3))

    @property
    def conceptual_values(self):
        return [self.conceptual_values_on_axis(i) for i in range(3)]

    @property
    def real_values(self):
        return [self.real_values_on_axis(i) for i in range(3)]

    @property
    def calculated_values(self):
        return [self.calculated_values_on_axis(i) for i in range(3)]

    def to_scad(self):
        return f'translate([{self.center_x_value}, {self.center_y_value}, {self.center_z_value}])\n' \
               f'   cube([{self.width_value}, {self.depth_value}, {self.height_value}], center=true);'

    def bounds_on_axis(self, axis: int):
        values = self.calculated_values_on_axis(axis)
        return values[0], values[2]

    @property
    def full_bounds(self):
        return [self.bounds_on_axis(i) for i in range(3)]

    def bounds_on_face(self, from_face: str = None):
        assert from_face is None or from_face in ("side", "top", "front"), 'Face must be side, top or front'
        selected_face = from_face if from_face is not None else self._face
        if selected_face == "side":
            return self.bounds_on_axis(1), self.bounds_on_axis(2)
        elif selected_face == "top":
            return self.bounds_on_axis(0), self.bounds_on_axis(1)
        elif selected_face == "front":
            return self.bounds_on_axis(0), self.bounds_on_axis(2)
        else:
            raise NotImplementedError(f'Unknown face "{self._face}"')

    @property
    def left(self):
        return self.__get_reference(0, 0)

    @left.setter
    def left(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(0, 0, value)

    @property
    def left_value(self):
        if self.__user_values[0][0] is None and self.is_conceptually_under_defined_on_axis(0):
            return None
        return self.__get_calculated_value(0, 0)

    @property
    def center_x(self):
        return self.__get_reference(0, 1)

    @center_x.setter
    def center_x(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(0, 1, value)

    @property
    def center_x_value(self):
        if self.__user_values[0][1] is None and self.is_conceptually_under_defined_on_axis(0):
            return None
        return self.__get_calculated_value(0, 1)

    @property
    def right(self):
        return self.__get_reference(0, 2)

    @right.setter
    def right(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(0, 2, value)

    @property
    def right_value(self):
        if self.__user_values[0][2] is None and self.is_conceptually_under_defined_on_axis(0):
            return None
        return self.__get_calculated_value(0, 2)

    @property
    def width(self):
        return self.__get_reference(0, 3)

    @width.setter
    def width(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(0, 3, value)

    @property
    def width_value(self):
        if self.__user_values[0][3] is None and self.is_conceptually_under_defined_on_axis(0):
            return None
        return self.__get_calculated_value(0, 3)

    @property
    def front(self):
        return self.__get_reference(1, 0)

    @front.setter
    def front(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(1, 0, value)

    @property
    def front_value(self):
        if self.__user_values[1][0] is None and self.is_conceptually_under_defined_on_axis(1):
            return None
        return self.__get_calculated_value(1, 0)

    @property
    def center_y(self):
        return self.__get_reference(1, 1)

    @center_y.setter
    def center_y(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(1, 1, value)

    @property
    def center_y_value(self):
        if self.__user_values[1][1] is None and self.is_conceptually_under_defined_on_axis(1):
            return None
        return self.__get_calculated_value(1, 1)

    @property
    def back(self):
        return self.__get_reference(1, 2)

    @back.setter
    def back(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(1, 2, value)

    @property
    def back_value(self):
        if self.__user_values[1][2] is None and self.is_conceptually_under_defined_on_axis(1):
            return None
        return self.__get_calculated_value(1, 2)

    @property
    def depth(self):
        return self.__get_reference(1, 3)

    @depth.setter
    def depth(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(1, 3, value)

    @property
    def depth_value(self):
        if self.__user_values[1][3] is None and self.is_conceptually_under_defined_on_axis(1):
            return None
        return self.__get_calculated_value(1, 3)

    @property
    def bottom(self):
        return self.__get_reference(2, 0)

    @bottom.setter
    def bottom(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(2, 0, value)

    @property
    def bottom_value(self):
        if self.__user_values[2][0] is None and self.is_conceptually_under_defined_on_axis(2):
            return None
        return self.__get_calculated_value(2, 0)

    @property
    def center_z(self):
        return self.__get_reference(2, 1)

    @center_z.setter
    def center_z(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(2, 1, value)

    @property
    def center_z_value(self):
        if self.__user_values[2][1] is None and self.is_conceptually_under_defined_on_axis(2):
            return None
        return self.__get_calculated_value(2, 1)

    @property
    def top(self):
        return self.__get_reference(2, 2)

    @top.setter
    def top(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(2, 2, value)

    @property
    def top_value(self):
        if self.__user_values[2][2] is None and self.is_conceptually_under_defined_on_axis(2):
            return None
        return self.__get_calculated_value(2, 2)

    @property
    def height(self):
        return self.__get_reference(2, 3)

    @height.setter
    def height(self, value: Optional[Union[int, float, Reference]]):
        self.__set_user_value(2, 3, value)

    @property
    def height_value(self):
        if self.__user_values[2][3] is None and self.is_conceptually_under_defined_on_axis(2):
            return None
        return self.__get_calculated_value(2, 3)

    def move_left(self, value: Union[int, float, Reference]):
        self.__offset[0] -= value

    def move_right(self, value: Union[int, float, Reference]):
        self.__offset[0] += value

    def grow_left(self, value: Union[int, float, Reference]):
        if self.__user_values[0][0] is None:
            raise ValueError("Can't grow left if left is not set")
        self.__user_values[0][0] -= value

    def shrink_left(self, value: Union[int, float, Reference]):
        if self.__user_values[0][0] is None:
            raise ValueError("Can't shrink left if left is not set")
        self.__user_values[0][0] += value

    def grow_right(self, value: Union[int, float, Reference]):
        if self.__user_values[0][2] is None:
            raise ValueError("Can't grow right if right is not set")
        self.__user_values[0][2] += value

    def shrink_right(self, value: Union[int, float, Reference]):
        if self.__user_values[0][2] is None:
            raise ValueError("Can't shrink right if right is not set")
        self.__user_values[0][2] -= value

    def move_forward(self, value: Union[int, float, Reference]):
        self.__offset[1] -= value

    def move_backward(self, value: Union[int, float, Reference]):
        self.__offset[1] += value

    def grow_front(self, value: Union[int, float, Reference]):
        if self.__user_values[1][0] is None:
            raise ValueError("Can't grow front if front is not set")
        self.__user_values[1][0] -= value

    def shrink_front(self, value: Union[int, float, Reference]):
        if self.__user_values[1][0] is None:
            raise ValueError("Can't shrink front if front is not set")
        self.__user_values[1][0] += value

    def grow_back(self, value: Union[int, float, Reference]):
        if self.__user_values[1][2] is None:
            raise ValueError("Can't grow back if back is not set")
        self.__user_values[1][2] += value

    def shrink_back(self, value: Union[int, float, Reference]):
        if self.__user_values[1][2] is None:
            raise ValueError("Can't shrink back if back is not set")
        self.__user_values[1][2] -= value

    def move_down(self, value: Union[int, float, Reference]):
        self.__offset[2] -= value

    def move_up(self, value: Union[int, float, Reference]):
        self.__offset[2] += value

    def grow_bottom(self, value: Union[int, float, Reference]):
        if self.__user_values[2][0] is None:
            raise ValueError("Can't grow bottom if bottom is not set")
        self.__user_values[2][0] -= value

    def shrink_bottom(self, value: Union[int, float, Reference]):
        if self.__user_values[2][0] is None:
            raise ValueError("Can't shrink bottom if bottom is not set")
        self.__user_values[2][0] += value

    def grow_top(self, value: Union[int, float, Reference]):
        if self.__user_values[2][2] is None:
            raise ValueError("Can't grow top if top is not set")
        self.__user_values[2][2] += value

    def shrink_top(self, value: Union[int, float, Reference]):
        if self.__user_values[2][2] is None:
            raise ValueError("Can't shrink top if top is not set")
        self.__user_values[2][2] -= value
