import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GifMate:
    def __init__(self, root, gif_path):
        self.root = root
        self.root.overrideredirect(True)        # Remove window decorations
        self.root.attributes("-topmost", True)  # Keep the window on top
        self.root.resizable(True, True)         # Make the window resizable
        
        # Load GIF
        self.gif = Image.open(gif_path)
        
        # Determine the transparent color of the GIF
        try:
            self.gif_transparency = self.gif.info['transparency']
            palette = self.gif.getpalette()
            start_index = self.gif_transparency * 3
            end_index = start_index + 3
            r, g, b = palette[start_index:end_index]
            self.gif_transparency_hex_color = f'#{r:02x}{g:02x}{b:02x}'
        except:
            self.gif_transparency_hex_color = "white"
            self.root.attributes("-transparentcolor", "white")  # Set white as the transparent color
        
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
        self.context_menu = tk.Menu(root, tearoff=0, bg="#333", fg="#fff", bd=5, activebackground="#555", activeforeground="#fff")
        self.context_menu.add_command(label="Transparency Settings", command=self.setting_transparency)
        self.context_menu.add_command(label="Change Framerate", command=self.setting_framerate)
        self.context_menu.add_command(label="Change Size", command=self.setting_size)
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
        self.root.after(60, self.animate_gif)  # Adjust delay as needed for your GIF

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
        print("Transparency Setting selected")

    def setting_framerate(self):
        print("Framerate Setting selected")

    def setting_size(self):
        print("Size Setting selected")
    
    def setting_import_gif(self):
        print("Import GIF selected")
        
    def setting_select_gif(self):
        print("Select GIF selected")
    
    def setting_about(self):
        print("About Section selected")

    def setting_close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GifMate(root, "dance.gif")  # Set the desired GIF path
    root.mainloop()
