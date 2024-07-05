import tkinter as tk
from PIL import Image, ImageTk
import yaml
import os
import h_giftools
import h_contextmenu
import shutil

class GifMate:
    def __init__(self, root, gif_path, pos_x, pos_y):
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
        self.root.geometry('%dx%d+%d+%d' % (self.gif.width, self.gif.height, pos_x, pos_y))

        
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
        self.root.after(self.gif_frame_duration, self.animate_gif)

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
        # Add Overall Alpha Layer to the GIF - TODO
        h_contextmenu.s_transparency(self)
    
    def setting_import_gif(self):
        # Select a GIF from anywhere and import it into a gif folder inside the Program folder
        h_contextmenu.s_import_gif(self)
        
    def setting_select_gif(self):
        # Select a GIF from inside the Program folder
        h_contextmenu.s_select_gif(self)
    
    def setting_about(self):
        # Open the Info Screen - TODO
        h_contextmenu.s_about(self.root)

    def setting_close(self):
        with open('config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)
        
        config_data['last_pos_X'] = self.root.winfo_x()
        config_data['last_pos_Y'] = self.root.winfo_y()
        
        with open('config.yaml', 'w') as file:
            yaml.dump(config_data, file)
        self.root.destroy()
        
    def size_scale(self, scale_factor):
        print("Factor: " + str(scale_factor))
        h_giftools.rescale_gif(self, scale_factor)
        
    def framerate_scale(self, scale_factor):
        h_giftools.change_framerate_gif(self, scale_factor)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Check for config file
    config_file = "config.yaml"
    
    if os.path.exists(config_file) and os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
    else:
        # create file
        f = open(config_file, 'a+')
        f.write('gif_name: gifs/gif.gif\n')
        f.write('first_run: true\n')
        f.write('last_pos_X: 0\n')
        f.write('last_pos_Y: 0\n')
        f.close()
        
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
    
    # Check for Gifs Folder
    gifs_folder = "gifs/"
    if os.path.exists(gifs_folder) and os.path.isdir(gifs_folder):
        pass
    else:
        os.makedirs(gifs_folder)
        
    
    # Get Path of File
    # if empty, open file dialog and abort if nothing is selected
    gif_path = config_data.get('gif_name')
    if os.path.exists(gif_path) and os.path.isfile(gif_path):
        pass
    else:
        initial_path = "/"
        source_path = h_giftools.initial_pick_gif(initial_path)
        destination_path = os.getcwd() + "/gifs"
        shutil.copy(source_path, destination_path)
        gif_path = "gifs/" + os.path.basename(source_path)
        config_data['gif_name'] = gif_path
        
    
    # Check for first run
    if config_data.get('first_run') == True:
        # Place Window at the Center
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen
        pos_x = (ws/2)
        pos_y = (hs/2)
        
        config_data['first_run'] = False
        
        with open('config.yaml', 'w') as file:
            yaml.dump(config_data, file)
    else:
        pos_x = config_data.get('last_pos_X')
        pos_y = config_data.get('last_pos_Y')
    
    app = GifMate(root, gif_path, pos_x, pos_y)
    root.mainloop()
