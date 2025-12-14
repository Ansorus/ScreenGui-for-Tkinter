import colorsys

# -- VALUE TYPES --
class Color3:
    def __init__(self, rgb: tuple = None, hsv: tuple = None, _hex: str = None):
        if rgb is not None:
            self.rgb = rgb
        if hsv is not None:
            self.hsv = hsv
        if _hex is not None:
            self._hex = _hex
    def __setattr__(self, key, value: tuple):
        if key == 'rgb':
            hsv = colorsys.rgb_to_hsv(value[0], value[1], value[2])
            _hex = "#%02x%02x%02x" % value
            super().__setattr__('rgb',value)
            super().__setattr__('hsv',hsv)
            super().__setattr__('_hex',_hex)
        elif key == 'hsv':
            rgb = colorsys.hsv_to_rgb(value[0], value[1], value[2])
            _hex = "#%02x%02x%02x" % value
            super().__setattr__('rgb', rgb)
            super().__setattr__('hsv', value)
            super().__setattr__('_hex', _hex)
        elif key == '_hex':
            value: str
            rgb = (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))
            hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            super().__setattr__('rgb', rgb)
            super().__setattr__('hsv', hsv)
            super().__setattr__('_hex', value)
    def __str__(self):
        return self._hex

class UDim2:
    def __init__(self, offset: tuple = (0,0), scale: tuple = (0,0)):
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.scale_x = scale[0]
        self.scale_y = scale[1]
    def from_scale_only(self, x,y):
        self.__init__(scale=(x,y))
        return self
    def from_offset_only(self, x, y):
        self.__init__(offset=(x,y))
        return self

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y