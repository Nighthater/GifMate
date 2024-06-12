import tkinter as tk
from PIL import Image, ImageTk

import h_giftools
import h_contextmenu

class GifMate:
    def __init__(self, root, gif_path):
        self.root = root
        self.root.overrideredirect(True)        # Remove window decorations
        self.root.attributes("-topmost", True)  # Keep the window on top
        self.root.resizable(True, True)         # Make the window resizable
        
        # Load GIF
        self.gif = Image.open(gif_path)
        
        # Determine the transparent color of the GIF
        self.gif_transparency_hex_color = h_giftools.get_gif_transparent_color(self.gif)
        
        # Determine the Framerate of the GIF
        self.gif_frame_duration = int(h_giftools.get_gif_speed(self.gif))
        
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

        # Create a label to display the GIF
        self.label = tk.Label(root, bg=self.gif_transparency_hex_color)
        self.root.attributes("-transparentcolor", self.gif_transparency_hex_color)  # Set the transparent color
        self.label.pack(expand=True, fill=tk.BOTH)

        # Set up mouse binding for right-click
        self.root.bind("<Button-3>", self.show_context_menu)

        # Set up mouse bindings for dragging
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # Create context menu for right click using tk.Menu
        self.context_menu = tk.Menu(root, tearoff=0)
        
        # Create Size Submenu
        self.submenu_size = tk.Menu(self.context_menu, tearoff=0)
        self.submenu_size.add_command(label="2.00x", command= lambda: self.size_scale(2.00))
        self.submenu_size.add_command(label="1.50x", command= lambda: self.size_scale(1.50))
        self.submenu_size.add_command(label="1.00x", command= lambda: self.size_scale(1.00))
        self.submenu_size.add_command(label="0.75x", command= lambda: self.size_scale(0.75))
        self.submenu_size.add_command(label="0.50x", command= lambda: self.size_scale(0.50))
        
        # Create Framerate Submenu
        self.submenu_speed = tk.Menu(self.context_menu, tearoff=0)
        self.submenu_speed.add_command(label="2.00x", command= lambda: self.framerate_scale(2.00))
        self.submenu_speed.add_command(label="1.50x", command= lambda: self.framerate_scale(1.50))
        self.submenu_speed.add_command(label="1.00x", command= lambda: self.framerate_scale(1.00))
        self.submenu_speed.add_command(label="0.75x", command= lambda: self.framerate_scale(0.75))
        self.submenu_speed.add_command(label="0.50x", command= lambda: self.framerate_scale(0.50))
        
        # Create context menu
        self.context_menu.add_command(label="Transparency Settings", command=self.setting_transparency)
        self.context_menu.add_cascade(label="Change Framerate", menu=self.submenu_speed)
        self.context_menu.add_cascade(label="Change Size", menu=self.submenu_size)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Import new GIF", command=self.setting_import_gif)
        self.context_menu.add_command(label="Select GIF", command=self.setting_select_gif)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="About", command=self.setting_about)
        self.context_menu.add_command(label="Close", command=self.setting_close)

        # Start the animation
        self.animate_gif()

    def animate_gif(self):
        self.gif_frame_index = (self.gif_frame_index + 1) % len(self.frames)
        self.label.config(image=self.frames[self.gif_frame_index])
        self.root.after(self.gif_frame_duration*2, self.animate_gif)  # Adjust delay as needed for your GIF

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")

    def setting_transparency(self):
        h_contextmenu.s_transparency()

    def setting_framerate(self):
        h_contextmenu.s_framerate()
    
    def setting_import_gif(self):
        h_contextmenu.s_import_gif()
        
    def setting_select_gif(self):
        h_contextmenu.s_select_gif()
    
    def setting_about(self):
        h_contextmenu.s_about(self.root)

    def setting_close(self):
        self.root.destroy()
        
    def size_scale(self, scale_factor):
        h_giftools.rescale_gif(self, scale_factor)
        
    def framerate_scale(self, scale_factor):
        h_giftools.change_framerate_gif(self, scale_factor)

if __name__ == "__main__":
    root = tk.Tk()
    app = GifMate(root, "dance.gif")  # Set the desired GIF path
    root.mainloop()
