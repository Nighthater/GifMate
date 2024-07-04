import tkinter as tk
from tkinter import Toplevel

def show_speech_bubble(self):
    # Create a top-level window for the speech bubble
    bubble_window = tk.Toplevel(self.root)
    bubble_window.overrideredirect(True)  # Remove window decorations
    bubble_window.attributes("-topmost", True)
    bubble_window.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")  # Position it relative to the root window

    # Create a canvas to draw the speech bubble
    canvas = tk.Canvas(bubble_window, width=100, height=50, bg='red')
    canvas.pack()

    # Draw the speech bubble
    canvas.create_text(50, 25, text="ERR", font=('Arial', 24))

    # Close the speech bubble after 3 seconds
    bubble_window.after(3000, bubble_window.destroy)