import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
import yaml
import h_giftools
import h_contextmenu

import svc_ttk


class GifMate:
    def __init__(self, root, gif_path, pos_x, pos_y):
        self.root = root
        self.setup_window(pos_x, pos_y)
        self.load_gif(gif_path)
        self.setup_ui()

        # Set up mouse binding for right-click
        self.root.bind("<Button-3>", self.show_context_menu)

        # Set up mouse bindings for dragging
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # Start the animation
        self.animate_gif()

    def setup_window(self, pos_x, pos_y):
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes("-topmost", True)  # Keep the window on top
        self.root.resizable(True, True)  # Make the window resizable
        self.root.geometry(f"+{pos_x}+{pos_y}")

    def load_gif(self, gif_path):
        self.gif = Image.open(gif_path)
        self.gif_transparency_hex_color = h_giftools.get_gif_transparent_color(self.gif)
        self.gif_frame_duration = int(h_giftools.get_gif_speed(self.gif))

        self.frames = []
        try:
            while True:
                frame = self.gif.copy().convert("RGBA")
                self.frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass

        self.gif_frame_index = 0

    def setup_ui(self):
        self.root.geometry(f"{self.gif.width}x{self.gif.height}")  # Set initial window size
        self.label = tk.Label(self.root, bg=self.gif_transparency_hex_color)
        self.root.attributes("-transparentcolor", self.gif_transparency_hex_color)  # Set the transparent color
        self.label.pack(expand=True, fill=tk.BOTH)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.create_context_menu()

    def create_context_menu(self):
        size_menu = tk.Menu(self.context_menu, tearoff=0)
        for scale in [2.00, 1.50, 1.00, 0.75, 0.50]:
            size_menu.add_command(label=f"{scale:.2f}x", command=lambda s=scale: self.size_scale(s))

        speed_menu = tk.Menu(self.context_menu, tearoff=0)
        for scale in [2.00, 1.50, 1.00, 0.75, 0.50]:
            speed_menu.add_command(label=f"{scale:.2f}x", command=lambda s=scale: self.framerate_scale(s))

        # self.context_menu.add_command(label="Transparency Settings", command=self.setting_transparency)
        self.context_menu.add_cascade(label="Change Framerate", menu=speed_menu)
        self.context_menu.add_cascade(label="Change Size", menu=size_menu)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Import new GIF", command=self.setting_import_gif)
        self.context_menu.add_command(label="Select GIF", command=self.setting_select_gif)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="About", command=self.setting_about)
        self.context_menu.add_command(label="Close", command=self.setting_close)

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

    # def setting_transparency(self):
    #     h_contextmenu.s_transparency(self)

    def setting_import_gif(self):
        h_contextmenu.s_import_gif(self)

    def setting_select_gif(self):
        h_contextmenu.s_select_gif(self)

    def setting_about(self):
        h_contextmenu.s_about(self.root)

    def setting_close(self):
        self.save_config()
        self.root.destroy()

    def save_config(self):
        config_path = 'config.yaml'
        try:
            with open(config_path, 'r') as file:
                config_data = yaml.safe_load(file)
            config_data['last_pos_X'] = self.root.winfo_x()
            config_data['last_pos_Y'] = self.root.winfo_y()
            with open(config_path, 'w') as file:
                yaml.dump(config_data, file)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error saving config: {e}")

    def size_scale(self, scale_factor):
        h_giftools.rescale_gif(self, scale_factor)

    def framerate_scale(self, scale_factor):
        h_giftools.change_framerate_gif(self, scale_factor)


def load_config():
    config_path = "config.yaml"
    default_config = {
        'gif_name': 'gifs/gif.gif',
        'first_run': True,
        'last_pos_X': 0,
        'last_pos_Y': 0,
    }

    if not os.path.exists(config_path):
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file)

    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except (FileNotFoundError, yaml.YAMLError):
        return default_config


def ensure_gifs_folder():
    gifs_folder = "gifs/"
    if not os.path.exists(gifs_folder):
        os.makedirs(gifs_folder)


def main():
    root = tk.Tk()
    config_data = load_config()

    ensure_gifs_folder()

    gif_path = config_data.get('gif_name')
    if not os.path.exists(gif_path):
        initial_path = "/"
        source_path = h_giftools.initial_pick_gif(initial_path)
        destination_path = os.path.join(os.getcwd(), "gifs")
        shutil.copy(source_path, destination_path)
        gif_path = os.path.join("gifs", os.path.basename(source_path))
        config_data['gif_name'] = gif_path
        with open('config.yaml', 'w') as file:
            yaml.dump(config_data, file)

    if config_data.get('first_run', True):
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        pos_x = ws // 2
        pos_y = hs // 2
        config_data['first_run'] = False
        with open('config.yaml', 'w') as file:
            yaml.dump(config_data, file)
    else:
        pos_x = config_data.get('last_pos_X', 0)
        pos_y = config_data.get('last_pos_Y', 0)

    app = GifMate(root, gif_path, pos_x, pos_y)
    svc_ttk.set_theme("dark")
    root.mainloop()


if __name__ == "__main__":
    main()
