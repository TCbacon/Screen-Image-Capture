import os
from pynput import keyboard
from PIL import ImageGrab
import time
import tkinter as tk
from tkinter import filedialog
import winsound

class ScreenShot(object):

    def __init__ (self, root):

        self.root = root
        root.geometry("400x400")
        root.title("Screenshot Capture")

        self.directory_stringvar = tk.StringVar()
        self.filename_stringvar = tk.StringVar()
        self.screenshot_key_stringvar = tk.StringVar(value="s")
        self.extension_stringvar = tk.StringVar(value="png")
        self.frequency_stringvar = tk.StringVar(value=400)
        self.duration_stringvar = tk.StringVar(value=200)

        # Create and pack widgets
        self.directory_label = tk.Label(root, text="Save Directory")
        self.directory_label.pack()
        self.directory_entry = tk.Entry(root, width=40, textvariable=self.directory_stringvar)
        self.directory_entry.pack()
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        self.filename_label = tk.Label(root, text="Base Filename")
        self.filename_label.pack()
        self.filename_entry = tk.Entry(root, width=40, textvariable=self.filename_stringvar)
        self.filename_entry.pack()

        self.key_pressed_label = tk.Label(root, text=f"Press the '{self.screenshot_key_stringvar.get()}' key to take a screenshot", font=("Helvetica", 12, "bold"), wraplength=300)
        self.key_pressed_label.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_data)
        self.save_button.pack()

        self.more_options_button = tk.Button(root, text="More Options", command=self.toggle_more_options)
        self.more_options_button.pack()

        # Frame to hold additional options
        self.more_options_frame = tk.Frame(root)
        self.more_options_frame.pack()

        # Variable to track the state of additional options
        self.more_options_visible = False

        #init data in entry boxes
        self.read_save_data()

        self.listener = keyboard.Listener(on_press=lambda key:self.take_screenshot_and_save(pressed_key=key))
        self.listener.start()
    
    def toggle_more_options(self):
        if not self.more_options_visible:
            # Add the additional entry fields when the button is clicked
            self.create_more_options()
            self.more_options_visible = True
        else:
            # Hide the additional entry fields when the button is clicked again
            self.destroy_more_options()
            self.more_options_visible = False

    def create_more_options(self):
        # Create and pack additional entry fields here
        tk.Label(self.more_options_frame, text="Screenshot Key").pack()
        tk.Entry(self.more_options_frame, textvariable=self.screenshot_key_stringvar).pack()
        tk.Label(self.more_options_frame, text="Extension").pack()
        tk.Entry(self.more_options_frame, textvariable=self.extension_stringvar).pack()
        tk.Label(self.more_options_frame, text="Sound Frequency").pack()
        tk.Entry(self.more_options_frame, textvariable=self.frequency_stringvar).pack()
        tk.Label(self.more_options_frame, text="Sound Duration").pack()
        tk.Entry(self.more_options_frame, textvariable=self.duration_stringvar).pack()

    def destroy_more_options(self):
        # Destroy the additional entry fields here
        for widget in self.more_options_frame.winfo_children():
            widget.destroy()
    
    def read_save_data(self):
        try:
            with open('screenshot_path_save.txt','r') as save_file:
                entry_list = save_file.readlines()
                length_list = len(entry_list)
                
                for i in range(length_list):
                    if i == 0:
                        #clear entry before inserting new data
                        self.directory_entry.delete(0, tk.END)
                        self.directory_entry.insert(0, entry_list[i].rstrip('\n'))
                    elif i == 1:
                        #clear entry before inserting new data
                        self.filename_entry.delete(0, tk.END)
                        self.filename_entry.insert(0, entry_list[i].rstrip('\n'))           
                    else:
                        break
        except FileNotFoundError:
            pass
    
    def save_data(self):
        with open('screenshot_path_save.txt','w') as save_file:
            save_file.write(self.directory_stringvar.get() + "\n")
            save_file.write(self.filename_stringvar.get() + "\n")

    def take_screenshot_and_save(self, pressed_key):

        # Listener ignores typing in tkinter entry fields
        focused_widget = self.root.focus_get()
        if isinstance(focused_widget, tk.Entry):
            return 

        try:
            # Ensure the directory exists, create it if it doesn't
            os.makedirs(name=self.directory_stringvar.get(), exist_ok=True)
        except OSError as e:
            self.key_pressed_label.config(text=f"Error creating directory: {e}")
            return
        
        try:
            pressed_key = pressed_key.char
            
            if self.screenshot_key_stringvar.get() == pressed_key:
                # You can adjust the frequency (400) and duration (200) of the beep
                winsound.Beep(int(self.frequency_stringvar.get()), int(self.duration_stringvar.get()))  

                # Capture the screenshot
                screenshot = ImageGrab.grab()

                # Generate a unique filename with a timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_filename = f"{self.filename_stringvar.get()}_{timestamp}.{self.extension_stringvar.get()}"

                # Save the screenshot as a PNG file
                screenshot_path = os.path.join(self.directory_stringvar.get(), f"{screenshot_filename}")
                screenshot.save(screenshot_path)

                self.key_pressed_label.config(text=f"Screenshot saved as {screenshot_path}")
            else:
                self.key_pressed_label.config(text=f"You pressed '{pressed_key}'. Press '{self.screenshot_key_stringvar.get()}' key to take a screenshot")
                winsound.PlaySound('SystemQuestion', winsound.SND_ASYNC)
            
            

        except AttributeError:
            # Ignore special keys like Shift, Alt, etc.
            pass
        except ValueError:
            self.key_pressed_label.config(text=f"Error: frequency & duration must be an integer")

    def browse_directory(self):
        self.directory = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, self.directory)


# Create the main window
root = tk.Tk()
ScreenShot(root)
root.mainloop()