from tkinter import *


class Menu:
    entries = {}

    def __init__(self, your_class):
        self.your_class = your_class

    def make_widgets(self):
        fields = vars(self.your_class)
        fields = [field for field in fields if field[0:2] == 'c_']
        window = Tk()
        window.title('fish control panel')
        form = Frame(window)
        form.pack()
        for (ix, label) in enumerate(fields):
            lab = Label(form, text=label)
            ent = Entry(form)
            lab.grid(row=ix, column=0)
            ent.grid(row=ix, column=1)
            self.entries[label] = ent
            self.entries[label].insert(0, getattr(self.your_class, label))
        Button(window, text="Update", command=self.update_button).pack(side=LEFT)
        return window

    def update_button(self):
        for key, enter in self.entries.items():
            setattr(self.your_class, key, float(enter.get()))
