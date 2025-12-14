## What's a ScreenGui?
In Roblox Studio, UI objects can be placed relative to the screen's size with offset pixels. Moreover, UI objects have anchor points that can be positioned anywhere around the object.
Ofcourse, Tkinter has the same abilities. Tkinter can place widgets with `x`,`y`,`relx`,`rely`, and anchor points are set with a combination of `n`,`e`,`s`,`w`
The issue is, for Roblox Studio developers switching to python, switching to tkinter is challenging. In fact, many people recommend to use `grid` in tkinter, which places objects based on grids.
This means that new-comers of python have to get used to the `grid` way of positioning and sizing widgets, which is takes time for Roblox Studio developers who are using to make UI Objects differently.
To solve this problem, this library simulates the Roblox Studio way of creating UI in Tkinter. In this repository, A ScreenGui is a window that can have UI Objects such as TextLabels, TextButtons, and Frames.
