"""OOP file to set graphics"""

# imported libraries
from tkinter import *
import properties as prop
from tkinter import ttk, PhotoImage, messagebox


def seperator(place_x, place_y, width=1200, height=2, bg=prop.LINE_COLOUR, ref=None):
    """Use this function to make a divider in the window, horizontal, vertical"""
    sep = Canvas(width=width, height=height, background=bg, relief=ref)
    sep.place(x=place_x, y=place_y)


class GWindow(Tk):
    """Creates the window for the GUI"""

    def __init__(self):
        super().__init__()
        self.x_padding = 8
        self.y_padding = 1

    def start_window(self):
        """Create a window, which fits to the users screen size."""
        self.title(prop.TITLE)
        self.config(padx=self.x_padding, pady=self.y_padding, background=prop.SCREEN_BG)
        self.geometry("1200x675")
        self.resizable(False, False)

    def loop(self):
        """Runs the mainloop to let the window stay open."""
        self.mainloop()

    def win_destroy(self):
        self.destroy()


class GCanvas:
    """Has all the required canvas properties, text, rectangle, etc."""

    def __init__(self, parent, width, height, bg=prop.CANVAS_COLOUR, ref=None, hb=None):
        """Initializer to create the other parameters along with canvas, enter, width, and parent required."""
        self.canvas = Canvas(parent, width=width, height=height, background=bg, relief=ref, bd=1.8,
                             highlightbackground=hb)
        self.image = None
        self.scaled_image = None
        self.style = None
        self.combo = None
        self.check = None
        self.entry = None
        self.button = None

    def add_image(self, file_path, x, y, scale=1):
        """Add an image to the canvas at specified coordinates with optional scaling."""
        self.image = PhotoImage(file=file_path)
        self.scaled_image = self.image.subsample(scale, scale)
        self.canvas.create_image(x, y, image=self.scaled_image, anchor="nw")

    def add_rect(self, x0, y0, x1, y1, fill=prop.RECT_COLOUR):
        """Adds a rectangle on the selected canvas, enter initial (x0,y0), and final (x1,y1) coordinates; along with color to fill with."""
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)

    def add_text(self, x, y, text, anc, tag=None, font=(prop.FONT_STYLE, 12), fill="black"):
        """Adds a text on the selected canvas, enter placeholders (x,y) along with text to be written, anchor and text color."""
        self.canvas.create_text(x, y, text=text, anchor=anc, fill=fill, font=font, tags=tag)

    def del_text(self, text):
        """Deletes a tagged text."""
        self.canvas.delete(text)

    def add_button(self, text, comm, place_x, place_y, anc):
        """Adds a button on the canvas, to run desired functions."""
        self.button = Button(self.canvas, text=text, command=comm, background=prop.SCREEN_BG, relief="raised",
                             font=(prop.FONT_STYLE, 10))
        self.button.place(x=place_x, y=place_y, anchor=anc)

    def add_entry(self, text_var, width, place_x, place_y, anc):
        """Adds an entry box on canvas, to display text."""
        self.entry = Entry(self.canvas, textvariable=text_var, state="normal", width=width, background=prop.SCREEN_BG,
                           relief="sunken")
        self.entry.place(x=place_x, y=place_y, anchor=anc)

    def add_combo(self, opts, place_x, place_y, anc, comm, width, var=None):
        """Adds a drop box, to list options to select."""
        self.style = ttk.Style()
        self.style.configure('TCombobox', font=(prop.FONT_STYLE, 12))
        self.combo = ttk.Combobox(self.canvas, width=width, textvariable=var, values=opts, state="readonly")
        self.combo.place(x=place_x, y=place_y, anchor=anc)
        self.combo.set('----')
        self.combo.bind("<<ComboboxSelected>>", comm)

    def add_checkbox(self, place_x, place_y, var, comm, text=None):
        """Adds a checkbox on canvas to select desired options."""
        self.check = Checkbutton(self.canvas, text=text, variable=var, command=comm, background=prop.CANVAS_COLOUR,
                                 font=(prop.FONT_STYLE, 12))
        self.check.place(x=place_x, y=place_y, anchor="nw")

    def place_canvas(self, place_x, place_y):
        """To place the canvas on the desired location on screen."""
        self.canvas.place(x=place_x, y=place_y)


class Message:

    def __init__(self):
        self.res = None
        self.mess = messagebox

    def error_message(self, text):
        self.mess.showerror("Error", text)

    def warn_message(self, text):
        self.mess.showwarning("Warning", text)

    def confirm_message(self, text):
        self.res = self.mess.askyesno("Confirmation", text)
        return self.res
