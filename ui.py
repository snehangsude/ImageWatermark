from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from watermark import Mark
from data import data
import os

THEME = '#8CA1A5'


class Interface:

    def __init__(self):
        """
        Initializes the interface window.

        ---- Description ----

        Text Field: [String] Allows the user to enter the watermark text (Used only in Add text)

        Font Dropdown: [String] Preloaded fonts which allows the user to vary the font style (Used only in Add text)

        Font Size: [Int] Allows the user to increase of decrease the font size (Used only in Add text)

        Rotate: [Int] Allows the user to rotate the text based on the angle provided (Used only in Add text)

        Opacity: [Int] Allows the user to vary the opacity of the text or logo
        [For text: 255 is opaque. For Logo: 0 is opaque]

        Placement Dropdown: [String] Allows the user to choose from the location in the dropdown to place the
        watermark

        Color: [String] Allows the user to change the color of the text (Used only in Add text)

        Margin X-axis: [Int] Allows the user to dynamically change the position of the text along the x-axis
        by altering the value

        Margin Y-axis: [Int] Allows the user to dynamically change the position of the text along the y-axis
        by altering the value


        View Image: [Button] Allows the user to open any image and view it inside the GUI

        Add Text: [Button] Takes all the input and then opens an window to select the image on which the watermark
        would be made

        Add Logo: [Button] Takes the required input and initially opens the Logo selection window and then the Image
        selection window on which the logo would be watermarked

        Save Image: [Button] Saves the image on the user selected directory
        """
        self.watermark = Mark()
        self.window = Tk()
        self.window.title('Watermark Generator')
        self.window.config(bg=THEME, padx=25, pady=15)
        self.window.resizable(True, True)

        # --------------- Labels----------------#
        self.welcome = Label(text="Add Watermark to your Images",
                             font=("Colonna MT", 25, "underline"),
                             bg=THEME, fg='#112031', )
        self.welcome.grid(row=1, column=1, columnspan=4, pady=15, padx=5)

        # -------------- Text --------------#
        self.input = Text(width=39, height=2, font=("Tahoma", 15,), bg='#D4ECDD',
                          fg='grey10', wrap='word', )
        self.input.insert(END, 'Enter watermark text here...')
        self.input.focus()
        self.input.grid(row=4, column=1, columnspan=4, padx=10, pady=10)

        # ---------- Buttons ------------- #
        # Viewer
        self.upload = Button(bd=-2, highlightthickness=0, text='View Image', bg=THEME, padx=2, pady=2,
                             font=("Tw Cen MT", 12, "bold"), fg='#212121', command=self.only_image_viewer)
        self.upload.grid(row=5, column=1, pady=10)
        # Text
        self.text = Button(bd=-2, highlightthickness=0, text='Add Text', bg=THEME, padx=2, pady=2,
                           font=("Tw Cen MT", 12, "bold"), fg='#212121', command=self.add_text_watermark)
        self.text.grid(row=5, column=2, pady=10)
        # Logo
        self.logo = Button(bd=-2, highlightthickness=0, text='Add Logo', bg=THEME, padx=2, pady=2,
                           font=("Tw Cen MT", 12, "bold"), fg='#212121', command=self.add_logo_watermark)
        self.logo.grid(row=5, column=3, pady=10)
        # Save
        self.save = Button(bd=-2, highlightthickness=0, text='Save Image', bg=THEME, padx=2, pady=2,
                           font=("Tw Cen MT", 12, "bold"), fg='#212121', command=lambda: self.save_file())
        self.save.grid(row=5, column=4, pady=10)
        # Font
        options = [key for key, value in data.items()]
        self.clicked = StringVar()
        self.clicked.set('Arial')
        self.fontbox = OptionMenu(self.window, self.clicked, *options)
        self.fontbox.config(bg=THEME, highlightthickness=0, width=20, pady=2, padx=2, font=("Tw Cen MT", 12, "bold"),
                            fg='#212121')
        self.fontbox.grid(row=6, column=1, pady=10, padx=2, columnspan=2)
        # Size
        self.size_label = Label(text="Font Size:", font=("Colonna MT", 15,), bg=THEME, fg='#112031', )
        self.size_label.grid(row=6, column=3)
        self.sizevar = IntVar(self.window)
        self.sizebox = Spinbox(from_=8, to=72, width=8, bg=THEME, fg='#212121', font=("Tw Cen MT", 12, "bold"),
                               justify='center', command=self.sizebox_used)
        self.sizebox.grid(row=6, column=4, pady=10)
        # Angle
        self.angle_label = Label(text="Rotate:", font=("Colonna MT", 15,), bg=THEME, fg='#112031', )
        self.angle_label.grid(row=7, column=1)
        self.anglevar = IntVar(self.window)
        self.anglebox = Spinbox(from_=-360, to=360, width=9, bg=THEME, fg='#212121', font=("Tw Cen MT", 12, "bold"),
                                justify='center', command=self.anglebox_used)
        self.anglebox.grid(row=7, column=2, pady=10)
        # Alpha
        self.opacity_label = Label(text="Opacity:", font=("Colonna MT", 15,), bg=THEME, fg='#112031', )
        self.opacity_label.grid(row=7, column=3)
        self.opacityvar = IntVar(self.window)
        self.opacitybox = Spinbox(from_=0, to=255, width=8, bg=THEME, fg='#212121', font=("Tw Cen MT", 12, "bold"),
                                  justify='center', command=self.opacitybox_used)
        self.opacitybox.grid(row=7, column=4, pady=10)
        # Placement
        self.placement_label = Label(text="Placement:", font=("Colonna MT", 15,), bg=THEME, fg='#112031', )
        self.placement_label.grid(row=8, column=1)
        choices = ["br", "bl", "tr", "tl", "center", "all", "diag"]
        self.choices_clicked = StringVar()
        self.choices_clicked.set('br')
        self.placementbox = OptionMenu(self.window, self.choices_clicked, *choices)
        self.placementbox.config(bg=THEME, highlightthickness=0, width=7, pady=2, padx=2,
                                 font=("Tw Cen MT", 12, "bold"),
                                 fg='#212121')
        self.placementbox.grid(row=8, column=2, pady=10, padx=2)
        # Color
        self.color_label = Label(text="Color:", font=("Colonna MT", 15,), bg=THEME, fg='#112031', )
        self.color_label.grid(row=8, column=3)
        self.color_text = Text(width=10, height=1, font=("Tw Cen MT", 12, "bold"), bg='#D4ECDD',
                               fg='#212121', )
        self.color_text.insert(END, '212121')
        self.color_text.grid(row=8, column=4, )
        # Margin -X
        self.margin_x_label = Label(text="Margin X-axis", font=("Colonna MT", 15,), bg=THEME, fg='#112031', )
        self.margin_x_label.grid(row=9, column=1)
        self.margin_x_text = Text(width=10, height=1, font=("Tw Cen MT", 12, "bold"), bg='#D4ECDD',
                                  fg='#212121', )
        self.margin_x_text.insert(END, '210')
        self.margin_x_text.grid(row=9, column=2, pady=10)
        # Margin -Y
        self.margin_y_label = Label(text="Margin Y-axis", font=("Colonna MT", 15,), bg=THEME, fg='#112031', )
        self.margin_y_label.grid(row=9, column=3)
        self.margin_y_text = Text(width=10, height=1, font=("Tw Cen MT", 12, "bold"), bg='#D4ECDD',
                                  fg='#212121', )
        self.margin_y_text.insert(END, '150')
        self.margin_y_text.grid(row=9, column=4, pady=10)
        # Notification
        self.notification_label = Label(text="", font=("Tahoma", 10, 'bold'), bg=THEME, fg='#950101', )
        self.notification_label.grid(row=10, column=1, columnspan=4, )

        # Catch Closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def open_logo_file(self):
        """
        Function to get the logo. A dialogue box opens which allows the user to navigate and choose the image
        from any directory.
        Note: Used only when applying logo to images
        """
        filename = filedialog.askopenfilename(initialdir='/', filetypes=(('Png files', '*.png'), ('All files', '*.*')),
                                              title='Select your Logo', )
        return filename

    def openfilename(self):
        """
        Function to get the image on which the watermark would be applied
        A dialogue box opens which allows the user to navigate and choose the image from any directory
        """
        filename = filedialog.askopenfilename(initialdir='/', title='Select an Image',
                                              filetypes=(('Png files', '*.png'), ('All files', '*.*')))
        return filename

    def sizebox_used(self):
        """Function to get the size"""
        return int(self.sizebox.get())

    def anglebox_used(self):
        """Function to get the angle"""
        return int(self.anglebox.get())

    def colorbox_used(self):
        """Function to get the color"""
        return self.color_text.get("1.0", END)

    def opacitybox_used(self):
        """Function to get the value of opacity"""
        return int(self.opacitybox.get())

    def textbox_used(self):
        """Function to get the text"""
        return self.input.get("1.0", END)

    def placementbox_used(self):
        """Function to get the place"""
        return self.choices_clicked.get()

    def fontstyle_used(self):
        """Function to get the font style and get the value from data"""
        key_style = self.clicked.get()
        return data.get(key_style).lower()

    def only_image_viewer(self):
        """
        Function that lets you open and view any kind of image file inside the GUI.
        Note: Displays the image with aspect ratio (400 x 250)
        """
        try:
            viewer = self.openfilename()
            img_viewer = Image.open(viewer)
        except AttributeError:
            pass
        else:
            img_viewer = img_viewer.resize((400, 250), Image.ANTIALIAS)
            img_viewer = ImageTk.PhotoImage(img_viewer)
            self.img_viewer = Label(self.window, image=img_viewer)
            self.img_viewer.image = img_viewer
            self.img_viewer.grid(row=2, column=1, rowspan=2, padx=15, pady=15, columnspan=4)

    def add_text_watermark(self):
        """
        Function binds to they key 'Add Text'. Gets all the values from the box and then let's the user
        choose the image to apply the changes on based on parameters.

        Note 1: Displays the image with aspect ratio (400 x 250) in the GUI as Label with the changes made.
        Note 2: Throws an error is the color is left empty or for a invalid hex code
        Note 3: Margin let's you change the placement of your text dynamically
        """
        size = self.sizebox_used()
        angle = self.anglebox_used()
        color = self.colorbox_used()
        opacity = self.opacitybox_used()
        text = self.textbox_used()
        placement = self.placementbox_used()
        font_style = self.fontstyle_used()
        image = self.openfilename()

        try:
            margin_x = int(self.margin_x_text.get("1.0", END))
            margin_y = int(self.margin_y_text.get("1.0", END))
        except ValueError:
            self.notification_label.config(text='Error: Margin value can\'t be empty')
        else:
            self.watermark.margin_x = margin_x
            self.watermark.margin_y = margin_y
            try:
                new_image = self.watermark.generate_text(text=text, style=font_style, angle=angle, size=size,
                                                         alpha=opacity, place=placement, color=color, image=image)
            except AttributeError:
                pass
            except TypeError:
                self.notification_label.config(text='Error: Please use a valid color')
            else:
                image_text = Image.open(new_image)
                image_text = image_text.resize((400, 250), Image.ANTIALIAS)
                image_text = ImageTk.PhotoImage(image_text)
                self.image_viewer = Label(self.window, image=image_text)
                self.image_viewer.image = image_text
                self.image_viewer.grid(row=2, column=1, rowspan=2, padx=15, pady=15, columnspan=4)

    def add_logo_watermark(self):
        """
        Function binds to they key 'Add Logo'. Gets the 'opacity' and 'placement' values from the box and
        let's the user choose the 'logo' first and then the 'image' to apply the changes on based on parameters.

        Note 1: Displays the image with aspect ratio (400 x 250) in the GUI as Label with the changes made.
        Note 2: 'Diag' from the placement is a invalid choice and hence defaults to bottom right or 'br'

        """
        logo = self.open_logo_file()
        image = self.openfilename()
        opacity = self.opacitybox_used()
        placement = self.placementbox_used()
        try:
            margin_x = int(self.margin_x_text.get("1.0", END))
            margin_y = int(self.margin_y_text.get("1.0", END))
        except ValueError:
            self.notification_label.config(text='Error: Margin value can\'t be empty')
        else:
            self.watermark.margin_x = margin_x
            self.watermark.margin_y = margin_y
            try:
                new_image = self.watermark.generate_logo(logo=logo, alpha=opacity, place=placement, image=image)
            except AttributeError:
                pass
            else:
                image_logo = Image.open(new_image)
                image_logo = image_logo.resize((400, 250), Image.ANTIALIAS)
                image_logo = ImageTk.PhotoImage(image_logo)
                self.image_viewer = Label(self.window, image=image_logo)
                self.image_viewer.image = image_logo
                self.image_viewer.grid(row=2, column=1, rowspan=2, padx=15, pady=15, columnspan=4)

    def save_file(self):
        """
        Opens a dialogue box to let the user choose the directory and the filename and saves the file in the
        respective directory.

        Note: This program by default creates a temporary file in the original directory but as soon as the user chooses
        to save the file, the base directory file is deleted
        """
        files = [('All Files', '.*'), ('PNG Files', '.png'), ('JPG Document', '.jpg')]
        file = filedialog.asksaveasfilename(initialdir='C:/Users/Public/Pictures', filetypes=files,
                                            title='Save File as', defaultextension=files)
        save_img = Image.open('tmp.png')
        try:
            save_img.save(file)
        except ValueError:
            pass
        else:
            os.remove("tmp.png")

    def on_closing(self):
        """
        Pops a message box asking the user to confirm the quit action. Deletes all unsaved files.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?\nAll unsaved files will be deleted."):
            self.window.destroy()
            try:
                os.remove("tmp.png")
            except FileNotFoundError:
                pass


