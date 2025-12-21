### Dependencies
- MtTkinter (atleast version 0.6.1)

## What's a ScreenGui?
In Roblox Studio, UI objects can be placed relative to the screen's size with offset pixels. Moreover, UI objects have anchor points that can be positioned anywhere around the object.
Ofcourse, Tkinter has the same abilities. Tkinter can place widgets with `x`,`y`,`relx`,`rely`, and anchor points are set with a combination of `n`,`e`,`s`,`w`
The issue is, for Roblox Studio developers switching to python, switching to tkinter is challenging. In fact, many people recommend to use `grid` in tkinter, which places objects based on grids.
This means that new-comers of python have to get used to the `grid` way of positioning and sizing widgets, which is takes time for Roblox Studio developers who are using to make UI Objects differently.
To solve this problem, this library simulates the Roblox Studio way of creating UI in Tkinter. In this repository, a ScreenGui is a window that can have UI Objects such as TextLabels, TextButtons, and Frames.
This library is for Roblox Studio Developers who want to make UI in TKinter the same way they make UI in Roblox Studio.

# Guide:
After downloading the repository files and mtTkinter, import them onto your python code to start using it

## Making a ScreenGui
To make a ScreenGui, it simply the following code below:\
`screen_gui = ScreenGui()`\
This will create a new, empty window.\
To change the title of the window, you change the name of the ScreenGui:\
`screen_gui.Name = "My Amazing App"`

### Changing the Background Color
To change the background color of the ScreenGui (As well as any other UI Object), you must change the `BackgroundColor3`\
First you make initialize a Color3, As shown below:\
`red_color = Color3(1,0,0)`\
\
You can also use FromRGB, as well as FromHSV and FromHEX. As shown below:
```
red_color = Color3().fromRGB(255,0,0)
red_color = Color3().fromHSV(1,1,1)
red_color = Color3().fromHex('FF0000')
```
Here are some other ways of making colors:
```
red_color = Color3(rgb=(255,0,0))
red_color = Color3(hsv=(1,1,1))
red_color = Color3(hex_=('FF0000'))
```
The next step is to apply the color to the BackgroundColor3 property of the ScreenGui, as shown below:
```
screen_gui = ScreenGui()
screen_gui.Name = "My amazing yellow app"

yellow = Color3().fromRGB(255,255,0)
screen_gui.BackgroundColor3 = yellow
```

## Making a Frame
To make a Frame is very similar to making a ScreenGui, except Frames need parents:\
```
frame = Frame()
frame.Parent = screen_gui
```
You can also set the parent in the initialization:\
`frame = Frame(screen_gui)`

### Position and Size
Both Position and Size use a data type called `UDim`. A UDim represents a two-dimensional value where each dimension is composed of a relative scale and an absolute offset:
```
position = UDim2(scale=(0.5, 0.5)) # Points at the center (50%, 50%)
size = UDim2(offset=(200, 200)) # The size is in absolute pixels, does not change.

frame = Frame(screen_gui)
frame.Position = position
frame.Size = size
```
This code will have the frame's top left corner positioned at the center of the ScreenGui. For the frame to be centered exactly at the ScreenGui, the anchor point of the frame must be at the center of the frame:
```
top_left = Vector2(0,0) # This would make the anchor point at the top left corner of the frame
bottom_right = Vector2(1,1)
center = Vector2(0.5,0.5)

frame.AnchorPoint = center
```

## Making a TextLabel
A TextLabel is like that of a frame, but with text:
```
label = TextLabel(screen_gui)

label.Position = UDim2(scale=(0.5,0.5))
label.Size = UDim2(offset=(200,200))
label.AnchorPoint = Vector2(0.5,0.5)

label.Text = "Hello World!"
```

### Adding Borders
You can easily give UI objects borders by setting their `BorderSizePixel`, and optionally `BorderColor3`:
```
label.BorderSizePixel = 5
label.BorderColor3 = Color3(1,1,0) # Yellow color
```

## Making a TextButton
To make a TextButton is very similar to that of making a TextLabel:
```
button = TextButton(screen_gui)
button.Text = "Hello World!"
```
To connect the button to the function, you must make use of Events
### Connecting Events
TextButtons have an `Activated` Event which can be connected to a function. Textbuttons would then fire the function everytime it is pressed.
```
num = 0
def button_pressed():
    global button, num
    num += 1
    button.Text = f"Clicked {num} times"

button.Activated.Connect(button_pressed)
```
Other UI Objects do NOT have an `Activated Event`. However, all UI Objects have these 3 Events: `MouseEnter`, `MouseMoved`, `MouseLeave`

## Making a TextBox
TextBoxes are TextLabels that the user can write in. Textboxes can be multiple lines, or just one line
```
text_box = TextBox(screen_gui)
text_box.Text = "Initial Text"  # text_box.Text will be changed by the user
text_box.MultiLine = True  # If user presses 'enter', they can make a new line
```
### Changing the Font
All Text Objects (TextLabels, TextButtons, TextBoxes) have fonts and text sizes. To set the TextSize is as simple as follows:
```text_box.TextSize = 20```
To set the font of the text, you have to make a Font object with the font family, and any weights (normal, bold, italic):
```
font = Font('Arial', 'bold','italic') # First argument is the family
button.Font = font
```
