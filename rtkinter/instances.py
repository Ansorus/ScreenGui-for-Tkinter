import math
import tkinter

from mttkinter import mtTkinter as mtk
from tkinter import font as tkfont
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
    _ignored_lines = 0
    def __init__(self, parent = None, multiline= True):
        self.__multi_frozen = True
        self.MultiLine = multiline

        super().__init__((mtk.Text if self.MultiLine else mtk.Entry),"TextBox", parent)

        self.tk.edit_modified(False)
        self.tk.tag_configure("left", justify="left")
        self.tk.tag_configure("center", justify="center")
        self.tk.tag_configure("right", justify="right")
        self.tk.config(wrap=tkinter.WORD)
        self.__multi_frozen = False

        self.tk.tag_add(self.TextXAlignment,'1.0', 'end')
        self.tk.bind("<<Modified>>", self._modified)
        self.tk.bind("<Key>", self._check_insertion_point)
    def _check_insertion_point(self, event):
        insertion_point: str = self.tk.index('insert') # returns a value like "1.0" or "2.6"
        if int(insertion_point.split('.')[0]) <= self._ignored_lines:
            self.tk.mark_set('insert',str(self._ignored_lines+1)+'.0')
            return "break"
        return None

    def _focus(self, event):
        self.tk.mark_set('insert', str(self._ignored_lines + 1) + ".0")
    def _modified(self, event):
        if self.tk.edit_modified():
            self._realign(event)
        self.tk.edit_modified(False)
    def _realign(self, event):
        insertion_point: str = self.tk.index('insert')
        insertion_point_rel_line = int(insertion_point.split('.')[0]) - self._ignored_lines
        if insertion_point_rel_line < 1: insertion_point_rel_line = 1

        if not self.__multi_frozen and self.TextYAlignment != "top":
            box_size_x,box_size_y= self.AbsoluteSize
            font = tkfont.Font(font=self.tk['font'])
            text_size_y = font.metrics("linespace")+3 # +C because something is off and I don't know what

            old_text = self.tk.get(str(self._ignored_lines + 1) + ".0", "end-1c")
            self.tk.delete("1.0", 'end')

            old_lines = old_text.count("\n")

            for line in old_text.split("\n"):
                text_size_x = font.measure(line)
                old_lines += math.floor(text_size_x/box_size_x)

            end_line = math.floor(box_size_y / text_size_y)

            times = (end_line-old_lines-1) if self.TextYAlignment == "bottom" else int(end_line / 2 - math.ceil(old_lines / 2))
            self._ignored_lines = times if times >= 0 else 0
            breaks = "".join(["\n" for _ in range(self._ignored_lines)])
            self.tk.insert("1.0", breaks + old_text)

        self.tk.tag_add(self.TextXAlignment, '1.0', 'end')

        new_line_str = str(insertion_point_rel_line+self._ignored_lines)
        char_pos_str = insertion_point.split(".")[1]

        self.tk.mark_set('insert', new_line_str+"."+char_pos_str)

        if not self.MultiLine:
            self.tk.delete("2.0", "end")
    def _resized(self,event=None):
        super()._resized(event)
        if not self.__multi_frozen:
            self._realign(event)
    def __getattribute__(self, item):
        if item == "Text":
            return self.tk.get(str(self._ignored_lines + 1) + ".0", "end-1c")
        else:
            return super().__getattribute__(item)
    def __setattr__(self, key, value):
        if key == "Text":
            self.tk.delete("1.0", mtk.END)
            self.tk.insert("1.0", value)
            if not self.__multi_frozen:
                self._ignored_lines = 0
                self.tk.edit_modified(True)
        elif key == "MultiLine" and not self.__multi_frozen:
            object.__setattr__(self, key, value)
            return
        elif key in ["TextXAlignment", "TextYAlignment"]:
            object.__setattr__(self, key, value)
            self.tk.edit_modified(True) #Repalce if doesn't work with self._realign(None)
        elif not key in ["MultiLine", "_ignored_lines"]:
            super().__setattr__(key, value)
        object.__setattr__(self,key,value)