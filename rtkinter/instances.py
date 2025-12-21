import time

from mttkinter import mtTkinter as mtk
import threading
from rtkinter.data_types import *

# -- BASE -- #
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

class _GuiBase:
    __frozen = True
    def __init__(self, tk, name: str = "GuiBase", parent = None, screen=False):
        self.Name: str = name
        if not screen:
            self.Parent: _GuiBase = parent
            self.tk = tk(parent.tk if parent is not None else None)
            self._class = tk
        self.children = []

        self.__frozen = False
    def _set_parent(self, parent):
        self.tk.destroy()
        self.tk = self._class(parent.tk if parent is not None else None)
        super().__setattr__("Parent", parent)

        everything = self.__dict__
        for key in everything.keys():
            if not key in ["Parent"]:
                self.__setattr__(key, everything[key])
    def FindFirstChild(self, name):
        return [child for child in self.children if child.Name == name]
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

class _GuiObject(_GuiBase):
    __frozen = True
    def __init__(self, tk, name, parent=None,
                 position: UDim2 = UDim2((0,0)), size: UDim2 = UDim2((200,200)), anchor: Vector2 = Vector2(0,0),
                 bg:Color3=Color3(rgb=(255,255,255)),
                 border_width=0, border_color=Color3(rgb=(0,0,0)),
                 screen=False):
        super().__init__(tk, name, parent, screen=screen)

        self.BackgroundColor3 = bg

        self.AnchorPoint = anchor
        self.Position = position
        self.Size = size

        self.AbsolutePosition: tuple = self.AbsolutePosition
        self.AbsoluteSize: tuple = self.AbsoluteSize

        self.MouseEnter = _Event(self.tk, "<Enter>")
        self.MouseLeave = _Event(self.tk, "<Leave>")
        self.MouseMoved = _Event(self.tk, "<Motion>")

        self.tk.bind("<Configure>", self._resized)
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
        offset_x = self.Position.offset_x - absolute_size_x*self.AnchorPoint.x
        offset_y = self.Position.offset_y - absolute_size_y*self.AnchorPoint.y
        self.tk.place(width=self.Size.offset_x,height=self.Size.offset_y,
                       relwidth=self.Size.scale_x,relheight=self.Size.scale_y,
                       x=offset_x, y=offset_y,
                       anchor='nw', relx=self.Position.scale_x, rely=self.Position.scale_y)
    def __setattr__(self, key, value):
        if self.__frozen:
            object.__setattr__(self,key, value)
            return

        if key in ["Position", "Size", "AnchorPoint"]:
            object.__setattr__(self, key, value)
            self.place()
        elif key == "BackgroundColor3":
            value: Color3
            object.__setattr__(self, "BackgroundColor3", value)
            self.tk.config(bg=str(value))
        elif key in ["BorderSizePixel", "BorderColor3"]:
            object.__setattr__(self, key, value)
            self.tk.config(highlightbackground=str(self.BorderColor3), highlightthickness=self.BorderSizePixel)
        else:
            super().__setattr__(key, value)
            return
    def __getattr__(self, item):
        if item == "AbsolutePosition":
            return self.tk.winfo_x(), self.tk.winfo_y()
        elif item == "AbsoluteSize":
            return self.tk.winfo_width(), self.tk.winfo_height()
        else:
            return super().__getattribute__(item)

# -- SCREENGUI -- #
def screen_loop(obj):
    screen = mtk.Tk()
    obj.tk = screen
    screen.mainloop()

class ScreenGui(_GuiObject):
    __frozen = True
    def __init__(self):
        self.tk = None
        self._thread = threading.Thread(target=lambda: screen_loop(self))
        self._thread.start()

        while self.tk is None:
            time.sleep(0.1)

        super().__init__(None,"ScreenGui", screen=True)

        self.Name = "ScreenGui"
        self.BackgroundColor3 = Color3(rgb=(255,255,255))
        self.children = []
        self.__frozen = False
        self.Size = UDim2(scale=(0.25, 0.25))
    def __setattr__(self, key, value):
        if self.__frozen:
            object.__setattr__(self, key, value)
            return
        if key == "Name":
            self.tk.title(value)
        elif not key in ['tk', '_thread']:
            super().__setattr__(key,value)
        object.__setattr__(self,key,value)
    def _resized(self,event=None):
        pass
    def place(self):
        absolute_size_x = int(self.Size.scale_x * self.tk.winfo_screenwidth() + self.Size.offset_x)
        absolute_size_y = int(self.Size.scale_y * self.tk.winfo_screenheight() + self.Size.offset_y)
        absolute_position_x = int(self.Position.scale_x * self.tk.winfo_screenwidth() + self.Position.offset_x - absolute_size_x*self.AnchorPoint.x)
        absolute_position_y = int(self.Position.scale_y * self.tk.winfo_screenheight() + self.Position.offset_y - absolute_size_y*self.AnchorPoint.y)
        self.tk.geometry(f"{absolute_size_x}x{absolute_size_y}+{absolute_position_x}+{absolute_position_y}")
    def _set_parent(self, parent):
        raise AttributeError

# -- INSTANCES -- #
class Frame(_GuiObject):
    def __init__(self, parent = None):
        super().__init__(mtk.Frame,"Frame", parent)
    def __setattr__(self, key, value):
        super().__setattr__(key, value)

class TextLabel(_GuiObject):
    def __init__(self, parent = None):
        super().__init__(mtk.Label,"TextLabel", parent)

        self.Text = "TextLabel"
        self.TextColor3 = Color3(0,0,0)
        self.Font: Font = Font(Enum.FontFamily.Arial, Enum.FontStyle.Normal)
        self.TextSize = 11

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
            font = (self.Font.family, self.TextSize, styles_str)
            self.tk.config(font=font)
            return
        else:
            super().__setattr__(key, value)
        object.__setattr__(self,key,value)

class TextButton(_GuiObject):
    def __init__(self, parent = None):

        self.Activated = _Event(tk=None)

        super().__init__(mtk.Frame,"TextButton", parent)

        self._button_tk = mtk.Button((self.tk if self is not None else None),command=self.Activated._fired)
        self._button_tk.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        self.Text = "TextButton"
        self.TextColor3 = Color3(0,0,0)
        self.Font: Font = Font(Enum.FontFamily.Arial, Enum.FontStyle.Normal)
        self.TextSize = 11

    def __setattr__(self, key, value):
        if key == "Text":
            self._button_tk.config(text=value)
        elif key in ["Font", "TextSize"]:
            object.__setattr__(self, key, value)

            try:
                super().__getattribute__("Font")
                super().__getattribute__("TextSize")
            except AttributeError:
                return

            styles_str = "".join(style + " " for style in self.Font.styles)
            font = (self.Font.family, self.TextSize, styles_str)
            self._button_tk.config(font=font)
            return
        elif key == "TextColor3":
            self._button_tk.config(fg=value, activeforeground=value)
        elif key == "BackgroundColor3":
            super().__setattr__(key, value)
            if '_button_tk' in self.__dict__:
                self._button_tk.config(bg=str(value), activebackground=str(value))
        elif not key in ["Activated", "_button_tk"]:
            super().__setattr__(key, value)
        object.__setattr__(self, key, value)

class TextBox(_GuiObject):
    __multi_frozen = True
    def __init__(self, parent = None, multiline= False):
        self.__multi_frozen = True
        self.MultiLine = multiline

        super().__init__((mtk.Text if self.MultiLine else mtk.Entry),"TextBox", parent)
        self.__multi_frozen = False

        self.Text = "TextBox"
        self.TextColor3 = Color3(0,0,0)
        self.Font: Font = Font(Enum.FontFamily.Arial, Enum.FontStyle.Normal)
        self.TextSize = 11

    def __getattribute__(self, item):
        if item == "Text":
            if not self.MultiLine:
                return self.tk.get()
            else:
                return self.tk.get("1.0", "end-1c")

        else:
            return super().__getattr__(item)
    def __setattr__(self, key, value):
        if key == "Text":
            if not self.MultiLine:
                self.tk.config(text=value)
            else:
                self.tk.delete("1.0", mtk.END)
                self.tk.insert("1.0", value)
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
            font = (self.Font.family, self.TextSize, styles_str)
            self.tk.config(font=font)
            return
        elif key == "MultiLine" and not self.__multi_frozen:
            try:
                object.__setattr__(self, key, value)
                self.tk.destroy()
                if self.MultiLine:
                    self.tk = mtk.Text(self.Parent.tk if self.Parent is not None else None)
                else:
                    self.tk = mtk.Entry(self.Parent.tk if self.Parent is not None else None)
                everything = self.__dict__
                for attribute in everything.keys():
                    if attribute in ["MultiLine", "Parent"]:
                        continue
                    self.__setattr__(attribute, everything[attribute])
                return
            except AttributeError:
                pass
        elif key != "MultiLine":
            super().__setattr__(key, value)
        object.__setattr__(self,key,value)

