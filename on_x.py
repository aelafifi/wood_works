from typing import Optional, Union

from Reference import Reference


class OnXCalculations(object):
    def __init__(self):
        super(OnXCalculations, self).__init__()
        self._width: Optional[Union[int, float, Reference]] = None
        self._left: Optional[Union[int, float, Reference]] = None
        self._right: Optional[Union[int, float, Reference]] = None
        self._center_x: Optional[Union[int, float, Reference]] = None
        self._offset_x: Union[int, float, Reference] = 0

        self._thickness: Optional[Union[int, float, Reference]] = None
        self._face: Optional[str] = None

    @property
    def values_on_x(self):
        # TODO: if one of these is a reference of None, then it will affect the status of being over/under/well defined
        return [
            self._left,
            self._center_x,
            self._right,
            self._width if self._face != 'side' else self._thickness,
        ]

    @staticmethod
    def get_prop_names_on_x():
        return [
            'left',
            'center_x',
            'right',
            'width',
        ]

    @property
    def count_defined_on_x(self):
        return sum(1 for value in self.values_on_x if value is not None)

    @property
    def is_over_defined_on_x(self):
        return self.count_defined_on_x > 2

    @property
    def is_under_defined_on_x(self):
        return self.count_defined_on_x < 2

    @property
    def is_well_defined_on_x(self):
        return self.count_defined_on_x == 2

    @property
    def calculated_values_on_x(self):
        # TODO: need to make sure that left <= right

        values = [v.value if isinstance(v, Reference) else v for v in self.values_on_x]
        if not self.is_well_defined_on_x:
            return values

        v_dict = dict(zip(self.get_prop_names_on_x(), values))

        if v_dict['left'] is None:
            if v_dict['right'] is None:
                v_dict['left'] = v_dict['center_x'] - v_dict['width'] / 2
                v_dict['right'] = v_dict['center_x'] + v_dict['width'] / 2
            elif v_dict['width'] is None:
                v_dict['width'] = (v_dict['right'] - v_dict['center_x']) * 2
                v_dict['left'] = v_dict['right'] - v_dict['width']
            else:
                v_dict['left'] = v_dict['right'] - v_dict['width']
                v_dict['center_x'] = v_dict['left'] + v_dict['width'] / 2
        elif v_dict['right'] is None:
            if v_dict['width'] is None:
                v_dict['right'] = v_dict['left'] + v_dict['center_x']
                v_dict['width'] = v_dict['right'] - v_dict['left']
            else:
                v_dict['right'] = v_dict['left'] + v_dict['width']
                v_dict['center_x'] = v_dict['left'] + v_dict['width'] / 2
        elif v_dict['width'] is None:
            v_dict['width'] = v_dict['right'] - v_dict['left']
            v_dict['center_x'] = v_dict['left'] + v_dict['width'] / 2
        ret_values = [v_dict[k] for k in self.get_prop_names_on_x()]
        ret_values[0] += self._offset_x
        ret_values[1] += self._offset_x
        ret_values[2] += self._offset_x
        return ret_values

    @property
    def left(self) -> Reference:
        return Reference(owner=self, prop='left')

    @left.setter
    def left(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert left <= center_x <= right

        # If None, set to None
        if value is None:
            self._left = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._left = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_x, "Can't set more than 2 constraints on the same axis"

    @property
    def left_value(self):
        if self._left is None and self.is_under_defined_on_x:
            return None
        return self.calculated_values_on_x[0]

    @property
    def right(self) -> Reference:
        return Reference(owner=self, prop='right')

    @right.setter
    def right(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert left <= center_x <= right

        # If None, set to None
        if value is None:
            self._right = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._right = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_x, "Can't set more than 2 constraints on the same axis"

    @property
    def right_value(self):
        if self._right is None and self.is_under_defined_on_x:
            return None
        return self.calculated_values_on_x[2]

    @property
    def center_x(self) -> Reference:
        return Reference(owner=self, prop='center_x')

    @center_x.setter
    def center_x(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert left <= center_x <= right

        # If None, set to None
        if value is None:
            self._center_x = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._center_x = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_x, "Can't set more than 2 constraints on the same axis"

    @property
    def center_x_value(self):
        if self._center_x is None and self.is_under_defined_on_x:
            return None
        return self.calculated_values_on_x[1]

    @property
    def width(self) -> Reference:
        return Reference(owner=self, prop='width')

    @width.setter
    def width(self, value: Optional[Union[int, float, Reference]]):
        if self._face == 'side':
            raise NotImplementedError("Can't set width on side face")

        # If None, set to None
        if value is None:
            self._width = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._width = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_x, "Can't set more than 2 constraints on the same axis"

    @property
    def width_value(self):
        if self._width is None and self.is_under_defined_on_x:
            return None
        return self.calculated_values_on_x[3]

    def move_left(self, value: Union[int, float, Reference]):
        self._offset_x += value

    def move_right(self, value: Union[int, float, Reference]):
        self._offset_x -= value

    def grow_left(self, value: Union[int, float, Reference]):
        if self._left is None:
            # TODO: this one could be calculated if left not set
            # TODO: it's buggy that way if not exactly left and right are defined
            raise ValueError("Can't grow left if left is not set")
        self._left -= value

    def grow_right(self, value: Union[int, float, Reference]):
        if self._right is None:
            raise ValueError("Can't grow right if right is not set")
        self._right += value

    def shrink_left(self, value: Union[int, float, Reference]):
        if self._left is None:
            raise ValueError("Can't shrink left if left is not set")
        self._left += value

    def shrink_right(self, value: Union[int, float, Reference]):
        if self._right is None:
            raise ValueError("Can't shrink right if right is not set")
        self._right -= value
