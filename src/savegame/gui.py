from tkinter import *
from tkinter import ttk


def save():
    # Code to be written
    pass


def load():
    # Code to be written
    pass

root = Tk()
root.geometry("200x150")
frame = Frame(root)
frame.pack()

mainmenu = Menu(frame)
mainmenu.add_command(label="Save", command=save)
mainmenu.add_command(label="Load", command=load)
mainmenu.add_command(label="Exit", command=root.destroy)

root.config(menu=mainmenu)

label = Label(root, text="Your Saves")
label.pack()

listbox = Listbox(root)

# Generate with for loop over list of serialized saves by name
listbox.insert(1, "Bread")
listbox.insert(2, "Milk")
listbox.insert(3, "Meat")
listbox.insert(4, "Cheese")
listbox.insert(5, "Vegetables")

listbox.pack()

# Game select combobox (normalize with game list in SaveManager)
# Also need a load_image() function to change the image based on the game
game_list = ["Elden Ring", "Sekiro", "Dark Souls III"]

Combo = ttk.Combobox(frame, values=game_list)
Combo.set("Choose a game")
Combo.pack(padx=5, pady=5)

root.mainloop()
