# h_giftools.py

from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
from tkinter import ttk, filedialog, Toplevel
import os
import imghdr



# Determine the transparent color of a GIF
def get_gif_transparent_color(gif):
    try:
        gif_transparency = gif.info['transparency']
        palette = gif.getpalette()
        
        start_index = gif_transparency * 3
        end_index = start_index + 3
        r, g, b = palette[start_index:end_index]
        hexcode = f'#{r:02x}{g:02x}{b:02x}'
    except:
        hexcode = "white"
    return hexcode

def get_gif_speed(gif):
    gif.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += gif.info['duration']
            gif.seek(gif.tell() + 1)
        except EOFError:
            return duration / frames
    return None


def rescale_gif(self, scale_factor):
    self.frames = []
    new_width = int(float(self.gif.width) * scale_factor)
    new_height = int(float(self.gif.height) * scale_factor)
    try:
        self.gif.seek(0)
        while True:
            frame = self.gif.copy().convert("RGBA")
            resized_frame = frame.resize((new_width, new_height), Image.NEAREST)
            new_frame = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
            new_frame.paste(resized_frame, (0, 0), resized_frame)
            self.frames.append(ImageTk.PhotoImage(new_frame))
            self.gif.seek(len(self.frames))  # Move to the next frame
    except EOFError:
        pass
    self.root.geometry(f"{new_width}x{new_height}")
    

def change_framerate_gif(self, scale_factor):
    old_framerate = get_gif_speed(self.gif)
    new_framerate = float(old_framerate) / float(scale_factor)
    self.gif_frame_duration = int(new_framerate)


def initial_pick_gif(initial_path):
    file_path = filedialog.askopenfilename(
        initialdir = initial_path,
        title = "Please Select a GIF file",
        filetypes = (("GIF images", "*.gif"), ("All files", "*.*"))
    )
    
    if os.path.isfile(file_path) and file_path.lower().endswith('.gif'):
        # Verify the file type is actually a gif
        if imghdr.what(file_path) == 'gif':
            return file_path



def pick_gif(self, initial_path):
    file_path = filedialog.askopenfilename(
        initialdir = initial_path,
        title = "Select a GIF file",
        filetypes = (("GIF images", "*.gif"), ("All files", "*.*"))
    )
    
    if os.path.isfile(file_path) and file_path.lower().endswith('.gif'):
        # Verify the file type is actually a gif
        if imghdr.what(file_path) == 'gif':
            # Verify that the Gif is in the relative folder '/gifs' 
            if os.path.commonpath([os.path.realpath(file_path), os.path.realpath('./gifs')]) == os.path.realpath('./gifs'):
                # change the filename in the config
                # reload the gif
                load_gif(self, file_path)


def load_gif(self, gif_path):
    self.gif = Image.open(gif_path)
    
    # Determine the transparent color of the GIF
    self.gif_transparency_hex_color = get_gif_transparent_color(self.gif)
    
    # Determine the Framerate of the GIF
    self.gif_frame_duration = int(get_gif_speed(self.gif))
    
    # Get size of the GIF
    self.root.geometry(f"{self.gif.width}x{self.gif.height}")  # Set initial window size

    self.frames = []
    try:
        while True:
            frame = self.gif.copy().convert("RGBA")
            self.frames.append(ImageTk.PhotoImage(frame))
            self.gif.seek(len(self.frames))  # Move to the next frame
    except EOFError:
        pass
    
    self.gif_frame_index = 0