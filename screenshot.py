import os
from pynput import keyboard
from PIL import ImageGrab
import time
import winsound
from env import *

class Screenshot():

    def __init__ (self):
        self.is_program_running = True
        self.listener = keyboard.Listener(on_press=lambda key:self.take_screenshot_and_save(pressed_key=key))

    def run_program(self):
        print(f"Press the '{SCREENSHOT_KEY}' key to take a screenshot")
        self.listener.start()

        try:
            while self.is_program_running:
                time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            self.exit_program()

    def exit_program(self):
        print("Exiting program...")
        self.listener.stop()
        self.is_program_running = False

    def take_screenshot_and_save(self, pressed_key):
        
        try:
            # Ensure the directory exists, create it if it doesn't
            os.makedirs(name=SAVE_DIRECTORY, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")
            return
        
        try:
            pressed_key = pressed_key.char
            
            if SCREENSHOT_KEY == pressed_key:
                print(f"Key '{pressed_key}' has been pressed")
                # You can adjust the frequency (400) and duration (200) of the beep
                winsound.Beep(FREQUENCY, DURATION)  

                # Capture the screenshot
                screenshot = ImageGrab.grab()

                # Generate a unique filename with a timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_filename = f"{FILENAME}_{timestamp}.{EXTENSION}"

                # Save the screenshot as a PNG file
                screenshot_path = os.path.join(SAVE_DIRECTORY, f"{screenshot_filename}")
                screenshot.save(screenshot_path)

                print(f"Screenshot saved as {screenshot_path}")
            elif pressed_key == 'q' or pressed_key == 'Q':
                self.exit_program()
            else:
                print(f"You pressed '{pressed_key}'. Press '{SCREENSHOT_KEY}' key to take a screenshot")
        except AttributeError:
            # Ignore special keys like Shift, Alt, etc.
            pass
            
    
if __name__ == "__main__":
    screen_shot = Screenshot()
    screen_shot.run_program()


