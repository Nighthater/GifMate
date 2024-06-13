# h_contextmenu.py
import tkinter as tk
from tkinter import ttk, filedialog, Toplevel
import os
from PIL import Image, ImageTk
import imghdr
import h_experimental
import h_giftools


def s_transparency(self):
    print("Transparency Setting selected")
    h_experimental.show_speech_bubble(self)

    
def s_import_gif(self):
    print("Import GIF selected")
    initial_dir = "/"
    
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="Select a GIF file",
        filetypes=(("GIF images", "*.gif"), ("All files", "*.*"))
    )
    h_experimental.show_speech_bubble(self)



def s_select_gif(self):
    print("Select GIF selected")
    initial_dir = os.getcwd() + '/gifs'
    
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="Select a GIF file",
        filetypes=(("GIF images", "*.gif"), ("All files", "*.*"))
    )

    # 
    if os.path.isfile(file_path) and file_path.lower().endswith('.gif'):
        # Verify the file type is actually a gif
        if imghdr.what(file_path) == 'gif':
            # Verify that the Gif is in the relative folder '/gifs' 
            if os.path.commonpath([os.path.realpath(file_path), os.path.realpath('./gifs')]) == os.path.realpath('./gifs'):
                # change the filename in the config
                # reload the gif
                h_giftools.load_gif(self, file_path)
            
        



def s_about(root):
    # Create new window
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x200")
    
    # Disable interaction with the main window
    about_window.transient(root)
    about_window.grab_set()
    
    # Add a label in the new window
    label = ttk.Label(about_window, text="GifMate © 2024 Nighthater")
    label.pack(pady=20)
