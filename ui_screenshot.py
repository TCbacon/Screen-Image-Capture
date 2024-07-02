import os
from pynput import keyboard
from PIL import ImageGrab
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import winsound
import json

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

        # List to store the recent folders
        self.recent_folders = []

        self.folder_dropdown = ttk.Combobox(root, values=self.recent_folders, state='readonly', width=400)
        self.folder_dropdown.bind('<<ComboboxSelected>>', self.on_dropdown_selected)
        self.folder_dropdown.pack(pady=5, padx=10)

        # Binding the folder_entry to the on_folder_selected function
        self.directory_entry.bind("<FocusOut>", self.on_folder_selected)

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
        self.load_drop_down_list()

        self.listener = keyboard.Listener(on_press=lambda key:self.take_screenshot_and_save(pressed_key=key))
        self.listener.start()
    

    def load_drop_down_list(self):
        try:
            with open("screenshot_path_save.json", 'r') as file:
                data = json.load(file)

                selected_dir = data.get('directory', '')
                filename = data.get('filename', '')
                settings = data.get('settings', {})

                if len(selected_dir) > 0:
                    self.directory_entry.delete(0, tk.END)
                    self.directory_entry.insert(0, selected_dir.rstrip('\n'))

                if len(filename) > 0:
                    self.filename_entry.delete(0, tk.END)
                    self.filename_entry.insert(0, filename.rstrip('\n'))  
            
                if settings:
                    self.screenshot_key_stringvar = tk.StringVar(value=settings['screenshot_key'])
                    self.extension_stringvar = tk.StringVar(value=settings['extension'])
                    self.frequency_stringvar = tk.StringVar(value=settings['frequency'])
                    self.duration_stringvar = tk.StringVar(value=settings['duration'])
                
                self.recent_folders = data['directories']
                self.update_dropdown()
    
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)

    def save_data(self):
        with open("screenshot_path_save.json", 'w') as file:
            screenshot_key = self.screenshot_key_stringvar.get()
            extension = self.extension_stringvar.get()
            frequency = self.frequency_stringvar.get()
            duration = self.duration_stringvar.get()

            json.dump({'directory': self.directory_stringvar.get(),
                       'settings': {'screenshot_key': screenshot_key, 
                                    'extension': extension, 
                                    'frequency': frequency,
                                    'duration': duration
                                    },
                       'directories': self.recent_folders, 
                       'filename': self.filename_stringvar.get()}, 
                       file, 
                       indent=4
                    )

    
    def remove_duplicates_and_reorder(self, directory_path):
        # Remove the selected folder if it already exists in the recent_folders list
        if directory_path in self.recent_folders:
            self.recent_folders.remove(directory_path)

        if not directory_path:
            return

        # Insert the folder at the beginning of the list
        self.recent_folders.insert(0, directory_path)

    
    def on_folder_selected(self, event):
        directory_path = self.directory_stringvar.get()
        self.remove_duplicates_and_reorder(directory_path)
        self.update_dropdown()
        self.save_data()

    def update_dropdown(self):
        self.folder_dropdown['values'] = self.recent_folders
        
    def on_dropdown_selected(self, event):
        selected_folder = self.folder_dropdown.get()
        self.directory_stringvar.set(selected_folder)
    
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
        self.remove_duplicates_and_reorder(self.directory)
        self.update_dropdown()
        


# Create the main window
root = tk.Tk()
ScreenShot(root)
root.mainloop()