import math

from rtkinter.data_types import UDim2, Vector2, Color3, Font, Enum
from mttkinter import mtTkinter as mtk
from tkinter import font as tkfont

# -- runs function it's connected to upon being signaled -- #
class _Event:
    connected = None
    def __init__(self, tk, event_string="", first_fire=None):
        self.tk = tk
        self.event_string = event_string
        self.first = first_fire

        if event_string != "":
            self.tk.bind(event_string, self._fired)
    def Connect(self, func):
        self.connected = func
    def _fired(self, event=None):
        success = (self.connected is not None)
        if self.first is not None:
            success = (self.first(event) and success)

        if not success:
            return
        if event is None:
            self.connected()
        else:
            self.connected(event)

# -- Objects that don't have a direct appearance (But still affect other things) -- #
class _GuiBase:
    __frozen = True
    def __init__(self, name: str = "GuiBase", parent = None):
        self.Name: str = name
        self.Parent: _GuiBase = parent

        self.children = []

        self.__frozen = False
    def _set_parent(self, parent):
        super().__setattr__("Parent", parent)

        everything = self.__dict__
        for key in everything.keys():
            if not key in ["Parent"]:
                self.__setattr__(key, everything[key])
    def FindFirstChild(self, name):
        for child in self.children:
            if child.Name == name:
                return child
        return None

    def _update_children(self):
        for child in self.children:
            child.Parent = self
    def __setattr__(self, key, value):
        if self.__frozen:
            super().__setattr__(key, value)
            return

        if key == "Parent":
            self._set_parent(value)
            return
        elif not key in self.__dict__.keys():
            print("Error found! Key: " + key)
            raise
        super().__setattr__(key, value)

# -- Objects that make a direct appearance -- #
class _GuiObject(_GuiBase):
    __frozen = True
    def __init__(self, tk, name, parent=None,
                 position: UDim2 = UDim2((0,0)), size: UDim2 = UDim2((200,200)), anchor: Vector2 = Vector2(0,0),
                 bg:Color3=Color3(rgb=(255,255,255)),
                 border_width=0, border_color=Color3(rgb=(0,0,0)),
                 encapsulated = False):

        self.encapsulated = encapsulated
        if not encapsulated:
            super().__init__(name, parent)
            self.tk = tk(parent.tk if parent is not None else None)
            self.capsule = self.tk
        else:
            super().__init__(name, parent)
            self.capsule = mtk.Frame(parent.tk if parent is not None else None)
            self.tk = tk(self.capsule)
            self.tk.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        self._class = tk
        self.tk: mtk.Widget
        self.capsule: mtk.Frame

        self.BackgroundColor3 = bg

        self.AnchorPoint = anchor
        self.Position = position
        self.Size = size

        self.AbsolutePosition: tuple = self.AbsolutePosition
        self.AbsoluteSize: tuple = self.AbsoluteSize

        self.MouseEnter = _Event(self.capsule, "<Enter>")
        self.MouseLeave = _Event(self.capsule, "<Leave>")
        self.MouseMoved = _Event(self.capsule, "<Motion>")

        self.capsule.bind("<Configure>", self._resized)
        self.BorderColor3 = border_color
        self.BorderSizePixel = border_width
        self.__frozen = False
        self.place()
    def _resized(self,event=None):
        self.place()
    def place(self):
        if self.Parent is None:
            return
        parent: mtk.Widget = self.Parent.tk
        parent.update()
        absolute_size_x = self.Size.scale_x*parent.winfo_width() + self.Size.offset_x
        absolute_size_y = self.Size.scale_y*parent.winfo_height() + self.Size.offset_y
        object.__setattr__(self, "AbsoluteSize", (absolute_size_x, absolute_size_y))
        offset_x = self.Position.offset_x - absolute_size_x*self.AnchorPoint.x
        offset_y = self.Position.offset_y - absolute_size_y*self.AnchorPoint.y
        self.capsule.place(width=self.Size.offset_x,height=self.Size.offset_y,
                       relwidth=self.Size.scale_x,relheight=self.Size.scale_y,
                       x=offset_x, y=offset_y,
                       anchor='nw', relx=self.Position.scale_x, rely=self.Position.scale_y)
    def __setattr__(self, key, value):
        if self.__frozen:
            object.__setattr__(self,key, value)
            return

        if key == "Parent":
            # __setattr__ in _GuiBase still runs, this is just an addon
            if self.tk is not None:
                self.tk.destroy()
                self.tk = self._class(value.tk if value is not None else None)

        if key == "tk" and not self.encapsulated:
            object.__setattr__(self,key,value)
            self.capsule = self.tk

        if key in ["Position", "Size", "AnchorPoint"]:
            object.__setattr__(self, key, value)
            self.place()
        elif key == "BackgroundColor3":
            value: Color3
            object.__setattr__(self, "BackgroundColor3", value)
            self.capsule.config(bg=str(value))
        elif key in ["BorderSizePixel", "BorderColor3"]:
            object.__setattr__(self, key, value)
            self.capsule.config(highlightbackground=str(self.BorderColor3), highlightthickness=self.BorderSizePixel)
        else:
            super().__setattr__(key, value)
            return
    def __getattr__(self, item):
        if item == "AbsolutePosition":
            return self.capsule.winfo_x(), self.capsule.winfo_y()
        elif item == "AbsoluteSize":
            try:
                return object.__getattribute__(self, "AbsoluteSize")
            except AttributeError:
                return self.capsule.winfo_width(), self.capsule.winfo_height()
        else:
            return super().__getattribute__(item)

# -- For all GuiObjects with Text -- #
class _TextObject(_GuiObject):
    def __init__(self, tk, name, parent=None, encapsulated = False):
        super().__init__(tk, name, parent, encapsulated=encapsulated)
        self.Text = name
        self.TextColor3 = Color3(0, 0, 0)
        self.Font: Font = Font(Enum.FontFamily.Arial, Enum.FontStyle.Normal)
        self.TextSize = 11
        self.TextScaled = False

        self.TextXAlignment = 'left' # Left, Center, Right
        self.TextYAlignment = 'top' # Top, Center, Bottom
    def _resized(self,event=None):
        super()._resized()
        if hasattr(self, "TextScaled") and self.TextScaled:
            self._update_text_size()
    def _update_text_size(self):
        border_width, border_height = self.AbsoluteSize
        # Insert me getting font here (with 1 PT size!):
        font = tkfont.Font(family=self.Font.family, size=5, weight=self.Font.styles[0])
        unit_width = font.measure(self.Text)
        unit_height = font.metrics("linespace")
        max_width = 5*border_width/unit_width
        max_height = 5*border_height/unit_height
        self.TextSize = max_width if max_width < max_height else max_height
    def _tk_alignment(self, x=None, y=None):
        # converts X and Y Alignment into tk config ('nw','n', etc..)
        x = self.TextXAlignment if x is None else x
        y = (self.TextYAlignment if hasattr(self,'TextYAlignment') else 'center') if y is None else y
        tk_x = ''
        tk_y = ''
        match x:
            case 'left':
                tk_x = 'w'
            case 'center':
                tk_x = ''
            case 'right':
                tk_x = 'e'
            case _:
                raise ValueError
        match y:
            case 'top':
                tk_y = 'n'
            case 'center':
                tk_y = ''
            case 'bottom':
                tk_y = 's'
            case _:
                raise ValueError
        # If both alignment is at center, use mtk.CENTER
        return tk_y+tk_x if tk_y+tk_x != '' else mtk.CENTER
    def __setattr__(self, key, value):
        if key == "Text":
            self.tk.config(text=value)
        elif key == "TextColor3":
            self.tk.config(fg=value)
        elif key in ["Font", "TextSize"]:
            object.__setattr__(self, key, value)

            try:
                super().__getattribute__("Font")
                super().__getattribute__("TextSize")
            except AttributeError:
                return

            styles_str = "".join(style + " " for style in self.Font.styles)
            font = (self.Font.family, math.floor(self.TextSize), styles_str)
            self.tk.config(font=font)
            return
        elif key == "TextXAlignment":
            anchor = self._tk_alignment(x=value)
            self.tk.config(anchor=anchor)
        elif key == "TextYAlignment":
            anchor = self._tk_alignment(y=value)
            self.tk.config(anchor=anchor)
        elif key != "TextScaled":
            super().__setattr__(key, value)
        object.__setattr__(self,key,value)

