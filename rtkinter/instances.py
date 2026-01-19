from mttkinter import mtTkinter as mtk
import threading
from rtkinter.data_types import *
from rtkinter.abstract_classes import _GuiObject, _TextObject, _Event

# -- SCREENGUI -- #
class ScreenGui(_GuiObject):
    __frozen = True
    def __start_thread(self, ready: threading.Event):
        super().__init__(mtk.Tk, "ScreenGui")
        ready.set()
        self.tk.mainloop()
    def __init__(self):
        ready = threading.Event()
        self._thread = threading.Thread(target=self.__start_thread, args=[ready])
        self._thread.start()
        ready.wait()

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

class TextLabel(_TextObject):
    def __init__(self, parent = None):
        super().__init__(mtk.Label,"TextLabel", parent)
    def __setattr__(self, key, value):
        super().__setattr__(key, value)

class TextButton(_TextObject):
    def __init__(self, parent = None):
        self.Activated = _Event(tk=None)

        super().__init__(mtk.Button,"TextButton", parent, encapsulated=True)

        self.tk.config(command=self.Activated._fired)
    def __setattr__(self, key, value):
        if not key in ["Activated"]:
            super().__setattr__(key, value)
        object.__setattr__(self, key, value)

class TextBox(_TextObject):
    __multi_frozen = True
    def __init__(self, parent = None, multiline= True):
        self.__multi_frozen = True
        self.MultiLine = multiline

        super().__init__((mtk.Text if self.MultiLine else mtk.Entry),"TextBox", parent)

        self.tk.edit_modified(False)
        self.tk.bind("<<Modified>>", self._realign)
        self.tk.tag_configure("left", justify="center")
        self.tk.tag_configure("center", justify="center")
        self.tk.tag_configure("right", justify="right")
        self.__multi_frozen = False

        self._realign(None)
    def _realign(self, event):
        if self.tk.edit_modified():
            self.tk.tag_add(self.TextXAlignment,'1.0', 'end')
        if not self.MultiLine:
            self.tk.delete("2.0", "end")
        self.tk.edit_modified(False)
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
        elif key == "MultiLine" and not self.__multi_frozen:
            object.__setattr__(self, key, value)
            return
        elif not key in ["MultiLine", "TextXAlignment", "TextYAlignment"]:
            super().__setattr__(key, value)
        object.__setattr__(self,key,value)