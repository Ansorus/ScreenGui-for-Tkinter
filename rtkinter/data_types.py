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
    @classmethod
    def new(cls, r,g,b): # CHANGE LATER TO MATCH STUDIo
        return cls(r=r,g=g,b=b)

    @classmethod
    def fromRGB(cls, red, green, blue):
        return cls(rgb=(red, green, blue))

    @classmethod
    def fromHSV(cls, hue,saturation,value):
        return cls(hsv=(hue,saturation,value))

    @classmethod
    def fromHex(cls, hex_):
        return cls(hex_=hex_)
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

    @classmethod
    def new(cls, scale_x, offset_x, scale_y, offset_y): #CHANGE LATER TO MATCH STUDIO
        return cls(offset = (offset_x,offset_y), scale = (scale_x,scale_y))

    @classmethod
    def fromScale(cls, x,y):
        return cls(scale=(x,y))

    @classmethod
    def fromOffset(cls, x, y):
        return cls(offset=(x,y))

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class _BuiltInFontFamilies:
    Arial = 'Arial'
    Courier = 'Courier'
    Times = 'Times'
    Helvetica = 'Helvetica'

class _BuiltInFontStyles:
    Normal = 'normal'
    Bold = 'bold'
    Roman = 'roman'
    Italic = 'italic'
    Underline = 'underline'
    Overstrike = 'overstrike'

class _TextXAlignments:
    Left = 'left'
    Right = 'right'
    Center = 'center'

class _TextYAlignments:
    Top = 'top'
    Bottom = 'bottom'
    Center = 'center'

class Enum:
    FontFamily = _BuiltInFontFamilies
    FontStyle = _BuiltInFontStyles
    TextXAlignment = _TextXAlignments
    TextYAlignment = _TextYAlignments

class Font:
    def __init__(self, family, styles):
        self.family = family # 'Arial'
        self.styles = styles if isinstance(styles, tuple) else tuple([styles]) # Font.Bold


