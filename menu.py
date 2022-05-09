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
            if label == 'c_perception' or label == 'c_amount':
                ent = Scale(form, orient=HORIZONTAL, from_=0, to=300)
            elif label == 'c_size' or label == 'c_tail_size':
                ent = Scale(form, orient=HORIZONTAL, from_=0, to=50)
            elif label == 'c_view_angle':
                ent = Scale(form, orient=HORIZONTAL, from_=0, to=360)
            else:
                ent = Scale(form, orient=HORIZONTAL, from_=0, to=20)
            lab.grid(row=ix, column=0)
            ent.grid(row=ix, column=1)
            self.entries[label] = ent
            self.entries[label].set(getattr(self.your_class, label))
        return window

    def update_(self):
        for key, enter in self.entries.items():
            setattr(self.your_class, key, float(enter.get()))
