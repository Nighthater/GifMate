import tkinter as tk
from PIL import Image, ImageTk

class UntitledProject:
    def __init__(self, root, gif_path):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        
        self.root.attributes("-topmost", True)  # Keep the window on top


        # Make the window resizable
        self.root.resizable(True, True)

        # Load GIF
        self.gif = Image.open(gif_path)
        
        # Determine the transparent Color of the Gif
        try:
            self.gif_transparency = self.gif.info['transparency']
            palette = self.gif.getpalette()
            start_index = self.gif_transparency * 3
            end_index = start_index + 3
            r, g, b = palette[start_index:end_index]
            self.gif_transparency_hex_color = f'#{r:02x}{g:02x}{b:02x}'
            print(self.gif_transparency_hex_color)
        except:
            self.gif_transparency_hex_color = "white"
            self.root.attributes("-transparentcolor", "white")  # Set white as the transparent color
        
        # Get Size of the Gif
        
        self.root.geometry(f"{self.gif.width}x{self.gif.height}")  # Set initial window size
        
        
        self.frames = []
        try:
            while True:
                frame = self.gif.copy().convert("RGBA")
                #frame = frame.resize((width, height))
                self.frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass
        
        
        
        self.gif_frame_index = 0

        # Create a label to display the GIF
        self.label = tk.Label(root, bg=self.gif_transparency_hex_color) # <- insert gif_transparency here
        self.root.attributes("-transparentcolor", self.gif_transparency_hex_color)  # Set white as the transparent color
        self.label.pack(expand=True, fill=tk.BOTH)

        # Set up mouse binding for right-click
        self.root.bind("<Button-3>", self.show_context_menu)

        # Set up mouse bindings for dragging
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # Create context menu for right click
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Transparency Setting", command=self.transparency_setting)
        self.context_menu.add_command(label="Speed Setting", command=self.speed_setting)
        self.context_menu.add_command(label="Gif Setting", command=self.gif_setting)
        self.context_menu.add_command(label="Scale Setting", command=self.scale_setting)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Minimize", command=self.minimize)
        self.context_menu.add_command(label="Close", command=self.close)

        # Start the animation
        self.animate_gif()

    def animate_gif(self):
        self.gif_frame_index = (self.gif_frame_index + 1) % len(self.frames)
        self.label.config(image=self.frames[self.gif_frame_index])
        self.root.after(20, self.animate_gif)  # Adjust delay as needed for your GIF

    def on_right_click(self, event):
        print("Right-clicked at", event.x, event.y)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")

    def transparency_setting(self):
        print("Transparency Setting selected")

    def speed_setting(self):
        print("Speed Setting selected")

    def gif_setting(self):
        print("Gif Setting selected")

    def scale_setting(self):
        print("Scale Setting selected")

    def minimize(self):
        self.root.iconify()

    def close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UntitledProject(root, "fries.gif")  # Set desired width and height
    root.mainloop()
