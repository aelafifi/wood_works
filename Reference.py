from typing import Union


class Reference:
    def __init__(self, /, owner, prop: str):
        self.owner = owner
        self.prop = prop
        self.ops = []

    @property
    def value(self):
        value = self.owner_value
        if value is None:
            return None
        for op, other in self.ops:
            other_value = other.value if isinstance(other, Reference) else other
            if op == '+':
                value = value + other_value
            elif op == '-':
                value = other_value - value
            elif op == '*':
                value = value * other_value
            elif op == '_':
                value = other_value / value
        return value

    @property
    def owner_value(self):
        return getattr(self.owner, f'{self.prop}_value')

    def __add__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('+', other))
        return self

    def __radd__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('+', other))
        return self

    def __sub__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('+', -other))
        return self

    def __rsub__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('-', other))
        return self

    def __neg__(self) -> 'Reference':
        self.ops.append(('*', -1))
        return self

    def __mul__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('*', other))
        return self

    def __rmul__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('*', other))
        return self

    def __truediv__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('*', 1 / other))
        return self

    def __rtruediv__(self, other: Union[int, float, 'Reference']) -> 'Reference':
        self.ops.append(('_', other))
        return self

    def get_owners(self):
        owners = set()
        for op, other in self.ops:
            if isinstance(other, Reference):
                owners.update(other.get_owners())
        owners.add(self.owner)
        return owners

    def __repr__(self):
        return f'Ref<{self.owner.label}.{self.prop}>'
