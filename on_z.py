from typing import Optional, Union

from Reference import Reference


class OnZCalculations(object):
    def __init__(self):
        super(OnZCalculations, self).__init__()
        self._height: Optional[Union[int, float, Reference]] = None
        self._bottom: Optional[Union[int, float, Reference]] = None
        self._top: Optional[Union[int, float, Reference]] = None
        self._center_z: Optional[Union[int, float, Reference]] = None
        self._offset_z: Union[int, float, Reference] = 0

        self._thickness: Optional[Union[int, float, Reference]] = None
        self._face: Optional[str] = None

    @property
    def values_on_z(self):
        return [
            self._bottom,
            self._center_z,
            self._top,
            self._height if self._face != 'top' else self._thickness,
        ]

    @staticmethod
    def get_prop_names_on_z():
        return [
            'bottom',
            'center_z',
            'top',
            'height',
        ]

    @property
    def count_defined_on_z(self):
        return sum(1 for value in self.values_on_z if value is not None)

    @property
    def is_over_defined_on_z(self):
        return self.count_defined_on_z > 2

    @property
    def is_under_defined_on_z(self):
        return self.count_defined_on_z < 2

    @property
    def is_well_defined_on_z(self):
        return self.count_defined_on_z == 2

    @property
    def calculated_values_on_z(self):
        # TODO: need to make sure that bottom <= top

        values = [v.value if isinstance(v, Reference) else v for v in self.values_on_z]
        if not self.is_well_defined_on_z:
            return values

        v_dict = dict(zip(self.get_prop_names_on_z(), values))

        if v_dict['bottom'] is None:
            if v_dict['top'] is None:
                v_dict['bottom'] = v_dict['center_z'] - v_dict['height'] / 2
                v_dict['top'] = v_dict['center_z'] + v_dict['height'] / 2
            elif v_dict['height'] is None:
                v_dict['height'] = (v_dict['top'] - v_dict['center_z']) * 2
                v_dict['bottom'] = v_dict['top'] - v_dict['height']
            else:
                v_dict['bottom'] = v_dict['top'] - v_dict['height']
                v_dict['center_z'] = v_dict['bottom'] + v_dict['height'] / 2
        elif v_dict['top'] is None:
            if v_dict['height'] is None:
                v_dict['top'] = v_dict['bottom'] + v_dict['center_z']
                v_dict['height'] = v_dict['top'] - v_dict['bottom']
            else:
                v_dict['top'] = v_dict['bottom'] + v_dict['height']
                v_dict['center_z'] = v_dict['bottom'] + v_dict['height'] / 2
        elif v_dict['height'] is None:
            v_dict['height'] = v_dict['top'] - v_dict['bottom']
            v_dict['center_z'] = v_dict['bottom'] + v_dict['height'] / 2
        ret_values = [v_dict[k] for k in self.get_prop_names_on_z()]
        ret_values[0] += self._offset_z
        ret_values[1] += self._offset_z
        ret_values[2] += self._offset_z
        return ret_values

    @property
    def bottom(self) -> Reference:
        return Reference(owner=self, prop='bottom')

    @bottom.setter
    def bottom(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert bottom <= center_z <= top

        # If None, set to None
        if value is None:
            self._bottom = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._bottom = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_z, "Can't set more than 2 constraints on the same axis"

    @property
    def bottom_value(self):
        if self._bottom is None and self.is_under_defined_on_z:
            return None
        return self.calculated_values_on_z[0]

    @property
    def top(self) -> Reference:
        return Reference(owner=self, prop='top')

    @top.setter
    def top(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert bottom <= center_z <= top

        # If None, set to None
        if value is None:
            self._top = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._top = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_z, "Can't set more than 2 constraints on the same axis"

    @property
    def top_value(self):
        if self._top is None and self.is_under_defined_on_z:
            return None
        return self.calculated_values_on_z[2]

    @property
    def center_z(self) -> Reference:
        return Reference(owner=self, prop='center_z')

    @center_z.setter
    def center_z(self, value: Optional[Union[int, float, Reference]]):
        # TODO: assert bottom <= center_z <= top

        # If None, set to None
        if value is None:
            self._center_z = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._center_z = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_z, "Can't set more than 2 constraints on the same axis"

    @property
    def center_z_value(self):
        if self._center_z is None and self.is_under_defined_on_z:
            return None
        return self.calculated_values_on_z[1]

    @property
    def height(self) -> Reference:
        return Reference(owner=self, prop='height')

    @height.setter
    def height(self, value: Optional[Union[int, float, Reference]]):
        if self._face == 'top':
            raise NotImplementedError("Can't set height on top face")

        # If None, set to None
        if value is None:
            self._height = None
            return

        # assert value is valid
        assert isinstance(value, (int, float, Reference)), "Expected value to be int, float, or Reference"
        if isinstance(value, (int, float)):
            assert value >= 0, 'Value must be positive'
        else:
            pass  # TODO: check valid reference / circular reference

        self._height = value

        # assert 2 values at max could be set on the same axis
        assert not self.is_over_defined_on_z, "Can't set more than 2 constraints on the same axis"

    @property
    def height_value(self):
        if self._height is None and self.is_under_defined_on_z:
            return None
        return self.calculated_values_on_z[3]

    def move_down(self, value: Union[int, float, Reference]):
        self._offset_z -= value

    def move_up(self, value: Union[int, float, Reference]):
        self._offset_z += value

    def grow_bottom(self, value: Union[int, float, Reference]):
        if self._bottom is None:
            raise ValueError("Can't grow bottom if bottom is not set")
        self._bottom -= value

    def grow_top(self, value: Union[int, float, Reference]):
        if self._top is None:
            raise ValueError("Can't grow top if top is not set")
        self._top += value

    def shrink_bottom(self, value: Union[int, float, Reference]):
        if self._bottom is None:
            raise ValueError("Can't shrink bottom if bottom is not set")
        self._bottom += value

    def shrink_top(self, value: Union[int, float, Reference]):
        if self._top is None:
            raise ValueError("Can't shrink top if top is not set")
        self._top -= value
