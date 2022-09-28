from typing import Optional, Union

from Reference import Reference


class OnYCalculations(object):
    def __init__(self):
        super(OnYCalculations, self).__init__()
        self._depth: Optional[Union[int, float, Reference]] = None
        self._back: Optional[Union[int, float, Reference]] = None
        self._front: Optional[Union[int, float, Reference]] = None
        self._center_y: Optional[Union[int, float, Reference]] = None
        self._offset_y: Union[int, float, Reference] = 0

        self._thickness: Optional[Union[int, float, Reference]] = None
        self._face: Optional[str] = None

    @property
    def values_on_y(self):
        return [
            self._front,
            self._center_y,
            self._back,
            self._depth if self._face != 'front' else self._thickness,
        ]

    @staticmethod
    def get_prop_names_on_y():
        return [
            'front',
            'center_y',
            'back',
            'depth',
        ]

    @property
    def count_defined_on_y(self):
        return sum(1 for value in self.values_on_y if value is not None)

    @property
    def is_over_defined_on_y(self):
        return self.count_defined_on_y > 2

    @property
    def is_under_defined_on_y(self):
        return self.count_defined_on_y < 2

    @property
    def is_well_defined_on_y(self):
        return self.count_defined_on_y == 2

    @property
    def calculated_values_on_y(self):
        # TODO: need to make sure that back <= front

        values = [v.value if isinstance(v, Reference) else v for v in self.values_on_y]
        if not self.is_well_defined_on_y:
            return values

        v_dict = dict(zip(self.get_prop_names_on_y(), values))

        if v_dict['back'] is None:
            if v_dict['front'] is None:
                v_dict['back'] = v_dict['center_y'] + v_dict['depth'] / 2
                v_dict['front'] = v_dict['center_y'] - v_dict['depth'] / 2
            elif v_dict['depth'] is None:
                v_dict['depth'] = (v_dict['front'] - v_dict['center_y']) * 2
                v_dict['back'] = v_dict['front'] - v_dict['depth']
            else:
                v_dict['back'] = v_dict['front'] - v_dict['depth']
                v_dict['center_y'] = v_dict['back'] + v_dict['depth'] / 2
        elif v_dict['front'] is None:
            if v_dict['depth'] is None:
                v_dict['front'] = v_dict['back'] + v_dict['center_y']
                v_dict['depth'] = v_dict['front'] - v_dict['back']
            else:
                v_dict['front'] = v_dict['back'] - v_dict['depth']
                v_dict['center_y'] = v_dict['back'] - v_dict['depth'] / 2
        elif v_dict['depth'] is None:
            v_dict['depth'] = v_dict['back'] - v_dict['front']
            v_dict['center_y'] = v_dict['front'] + v_dict['depth'] / 2
        ret_values = [v_dict[k] for k in self.get_prop_names_on_y()]
        ret_values[0] += self._offset_y
        ret_values[1] += self._offset_y
        ret_values[2] += self._offset_y
        return ret_values

    @property
    def back(self) -> Reference:
        return Reference(owner=self, prop='back')

    @back.setter
    def back(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert back <= center_y <= front

        # If None, set to None
        if value is None:
            self._back = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._back = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_y, "Can't set more than 2 constraints on the same axis"

    @property
    def back_value(self):
        if self._back is None and self.is_under_defined_on_y:
            return None
        return self.calculated_values_on_y[2]

    @property
    def front(self) -> Reference:
        return Reference(owner=self, prop='front')

    @front.setter
    def front(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert back <= center_y <= front

        # If None, set to None
        if value is None:
            self._front = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._front = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_y, "Can't set more than 2 constraints on the same axis"

    @property
    def front_value(self):
        if self._front is None and self.is_under_defined_on_y:
            return None
        return self.calculated_values_on_y[0]

    @property
    def center_y(self) -> Reference:
        return Reference(owner=self, prop='center_y')

    @center_y.setter
    def center_y(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert back <= center_y <= front

        # If None, set to None
        if value is None:
            self._center_y = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._center_y = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_y, "Can't set more than 2 constraints on the same axis"

    @property
    def center_y_value(self):
        if self._center_y is None and self.is_under_defined_on_y:
            return None
        return self.calculated_values_on_y[1]

    @property
    def depth(self) -> Reference:
        return Reference(owner=self, prop='depth')

    @depth.setter
    def depth(self, value: Optional[Union[int, float, Reference]]):
        if self._face == 'front':
            raise NotImplementedError("Can't set depth on back face")

        # If None, set to None
        if value is None:
            self._depth = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._depth = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_y, "Can't set more than 2 constraints on the same axis"

    @property
    def depth_value(self):
        if self._depth is None and self.is_under_defined_on_y:
            return None
        return self.calculated_values_on_y[3]

    def move_forward(self, value: Union[int, float, Reference]):
        self._offset_y -= value

    def move_backward(self, value: Union[int, float, Reference]):
        self._offset_y += value

    def grow_front(self, value: Union[int, float, Reference]):
        if self._front is None:
            raise ValueError("Can't grow front if front is not set")
        self._front -= value

    def grow_back(self, value: Union[int, float, Reference]):
        if self._back is None:
            raise ValueError("Can't grow back if back is not set")
        self._back += value

    def shrink_front(self, value: Union[int, float, Reference]):
        if self._front is None:
            raise ValueError("Can't shrink front if front is not set")
        self._front += value

    def shrink_back(self, value: Union[int, float, Reference]):
        if self._back is None:
            raise ValueError("Can't shrink back if back is not set")
        self._back -= value