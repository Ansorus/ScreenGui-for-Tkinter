import colorsys

# -- VALUE TYPES --
class Color3:
    def __init__(self, r=0, g=0, b=0, rgb: tuple = None, hsv: tuple = None, hex_: str = None):
        self.rgb = (255*r, 255*g, 255*b)
        if rgb is not None:
            self.rgb = rgb
        if hsv is not None:
            self.hsv = hsv
        if hex_ is not None:
            self._hex = hex_
    def fromRGB(self, red, green, blue):
        self.__init__(rgb=(red, green, blue))
        return self
    def fromHSV(self, hue,saturation,value):
        self.__init__(hsv=(hue,saturation,value))
        return self
    def fromHex(self, hex_):
        self.__init__(hex_=hex_)
        return self
    def __setattr__(self, key, value: tuple):
        if key == 'rgb':
            rgb_gen = (int(v/255) for v in value)
            rgb_1 = tuple(rgb_gen)
            hsv = colorsys.rgb_to_hsv(rgb_1[0], rgb_1[1], rgb_1[2])
            _hex = "#%02x%02x%02x" % value
            super().__setattr__('rgb',value)
            super().__setattr__('hsv',hsv)
            super().__setattr__('_hex',_hex)
        elif key == 'hsv':
            rgb = colorsys.hsv_to_rgb(value[0], value[1], value[2])
            rgb_gen =(int(v*255) for v in rgb)
            rgb_255 = tuple(rgb_gen)
            _hex = "#%02x%02x%02x" % rgb_255
            super().__setattr__('rgb', rgb_255)
            super().__setattr__('hsv', value)
            super().__setattr__('_hex', _hex)
        elif key == '_hex':
            value: str
            value = value.lstrip("#")
            if len(value) == 3:
                value = ''.join([c * 2 for c in value])

            rgb = (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))
            rgb_gen = (int(v / 255) for v in rgb)
            rgb_1 = tuple(rgb_gen)
            hsv = colorsys.rgb_to_hsv(rgb_1[0], rgb_1[1], rgb_1[2])
            super().__setattr__('rgb', rgb)
            super().__setattr__('hsv', hsv)
            super().__setattr__('_hex', "#"+value)
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