from types import SimpleNamespace as mini_object
import time
from mttkinter import mtTkinter as mtk
import threading
from value_types import Vector2, UDim2, Color3

# -- BASE -- #
class _Event:
    connected = None
    def __init__(self, tk, event_string, first_fire=None):
        self.tk = tk
        self.event_string = event_string
        self.first = first_fire

        self.tk.bind(event_string, self._fired)
    def Connect(self, func):
        self.connected = func
    def _fired(self, event):
        success = (self.connected is not None)
        if self.first is not None:
            success = (self.first(event) and success)

        if success:
            self.connected(event)

class _GuiBase:
    __frozen = True
    def __init__(self, name: str, parent = None, attributes=None, screen=False, tk = None):
        if attributes is None:
            attributes = {}
        self.Name: str = name
        if not screen:
            self.Parent: _GuiBase = parent
            self.tk = tk
        self.children = []

        for attribute in attributes.keys():
            super().__setattr__(attribute, attributes[attribute])

        self.__frozen = False
    def _set_parent(self, parent):
        self.tk.destroy()
        everything = self.__dict__
        self.__init__(self.Name, parent=parent, attributes=everything)
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
            raise AttributeError
        super().__setattr__(key, value)

class _GuiObject(_GuiBase):
    __frozen = True
    def __init__(self, name, parent=None, attributes = None,
                 position: UDim2 = UDim2((0,0)), size: UDim2 = UDim2((200,200)), anchor: Vector2 = Vector2(0,0),
                 bg:Color3=Color3(rgb=(255,255,255)),
                 border_width=0,border_color=Color3(rgb=(0,0,0)),
                 tk = None, screen=False):
        super().__init__(name, parent, attributes, tk=tk, screen=screen)

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

        super().__init__("ScreenGui", screen=True,)

        self.Name = "ScreenGui"
        self.BackgroundColor3 = Color3(rgb=(255,255,255))
        self.children = []
        self.__frozen = False
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

# -- INSTANCES --
class Frame(_GuiObject):
    def __init__(self, parent = None, attributes=None):
        if attributes is None:
            attributes = {}

        tk = mtk.Frame(parent.tk if parent is not None else None)
        super().__init__("Frame", parent, tk=tk, attributes=attributes)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

class TextLabel(_GuiObject):
    def __init__(self, parent = None, attributes=None):
        if attributes is None:
            attributes = {}

        tk = mtk.Label(parent.tk if parent is not None else None)
        super().__init__("TextLabel", parent, tk=tk, attributes=attributes)

        self.Text = attributes["Text"] if "Text" in attributes else "TextLabel"

    def __setattr__(self, key, value):
        if key == "Text":
            self.tk.config(text=value)
        else:
            super().__setattr__(key, value)
        object.__setattr__(self,key,value)

class TextButton(_GuiObject):
    def __init__(self, parent = None, attributes=None):
        if attributes is None:
            attributes = {}

        self.Activated = mini_object()
        self.Activated._connected = None
        self.Activated.Connect = self._set_activated

        tk = mtk.Button((parent.tk if parent is not None else None),command=self._command)
        super().__init__("TextLabel", parent, tk=tk, attributes=attributes)

        self.Text = attributes["Text"] if "Text" in attributes else "TextLabel"

    def _set_activated(self, func):
        self.Activated._connected = func
    def _command(self):
        if self.Activated._connected is not None:
            self.Activated._connected()
    def __setattr__(self, key, value):
        if key == "Text":
            self.tk.config(text=value)
        elif key != "Activated":
            super().__setattr__(key, value)
        object.__setattr__(self, key, value)

# -- TEST --
if __name__ == '__main__':

    def mouse_enter(label_to_change: _GuiObject, event):
        label_to_change.BackgroundColor3 = Color3(rgb=(0, 0, 255))

    def mouse_leave(label_to_change: _GuiObject, event):
        label_to_change.BackgroundColor3 = Color3(rgb=(255, 0, 0))

    def button_pressed(label_to_change: TextButton):
        label_to_change.Text = "Pressed"

    # Create a Window
    screenUI = ScreenGui()
    screenUI.Name = "New Amazing App"
    screenUI.BackgroundColor3 = Color3(rgb=(255,0,255))
    # Position the Window at the middle of the screen
    screenUI.Position = UDim2(scale=(0,0))
    screenUI.AnchorPoint = Vector2(0,0)
    # Window's Initial Size takes up the entire screen
    screenUI.Size = UDim2(scale=(0.5,0.5))

    # Create a Label
    frame = Frame(screenUI)
    # Position the Label at middle of the Window
    frame.AnchorPoint = Vector2(0.5, 0.5)
    frame.Position = UDim2().from_scale_only(0.5, 0.5)

    frame.Size = UDim2(scale=(0.45, 0.45))

    frame.BackgroundColor3 = Color3(rgb=(100, 100, 0))

    frame.BorderSizePixel = 1
    frame.MouseEnter.Connect(lambda event: mouse_enter(frame, event))
    frame.MouseLeave.Connect(lambda event: mouse_leave(frame, event))

    label = TextButton(frame)
    label.Position = UDim2().from_scale_only(0,0)
    label.Size = UDim2(scale=(0.25,0.25))
    label.AnchorPoint = Vector2(0,0)
    label.Activated.Connect(lambda: button_pressed(label))