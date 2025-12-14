from screengui_for_tkinter import *

screen_gui = ScreenGui()

button = TextButton(screen_gui)
button.Text = "Hello World!"

num = 0
def button_pressed():
    global button, num
    num += 1
    button.Text = f"Clicked {num} times"

button.Activated.Connect(button_pressed)

button.BorderSizePixel = 1
button.BorderColor3 = Color3().fromRGB(50,0,0) # Yellow color
button.BackgroundColor3 = Color3(rgb=(255,0,0))

button.TextSize = 20
button.Font = Font(Enum.FontFamily.Times, Enum.FontStyle.Overstrike)

button.TextColor3 = Color3().fromRGB(255,255,255)

text_box = TextBox(screen_gui)
text_box.Position = UDim2(scale=(1,0))
text_box.AnchorPoint = Vector2(1,0)

text_box.BackgroundColor3 = Color3().fromRGB(100,0,0)
text_box.TextColor3 = Color3().fromRGB(255,0,0)

text_box.MultiLine = True

time.sleep(3)

print("Text: " + text_box.Text)