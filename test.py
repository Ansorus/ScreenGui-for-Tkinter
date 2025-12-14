from screengui_for_tkinter import *

screen_gui = ScreenGui()
# screen_gui.Position = UDim2(scale=(0.5,0.5))
# screen_gui.Size = UDim2(scale=(0.25,0.25))
# screen_gui.AnchorPoint = Vector2(0.5,0.5)

button = TextButton(screen_gui)
button.Text = "Hello World!"

num = 0
def button_pressed():
    global button, num
    num += 1
    button.Text = f"Clicked {num} times"

button.Activated.Connect(button_pressed)

button.BorderSizePixel = 5
button.BorderColor3 = Color3().fromRGB(255,255,0) # Yellow color
button.BackgroundColor3 = Color3(rgb=(255,0,0))

button.TextSize = 20
button.Font = Font(Enum.FontFamily.Times, Enum.FontStyle.Overstrike)