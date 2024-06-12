# h_giftools.py

from PIL import Image, ImageTk

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
            return frames / duration * 1000
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
            # Create a new image with a transparent background
            new_frame = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
            new_frame.paste(resized_frame, (0, 0), resized_frame)
            self.frames.append(ImageTk.PhotoImage(new_frame))
            self.gif.seek(len(self.frames))  # Move to the next frame
    except EOFError:
        pass
    self.root.geometry(f"{new_width}x{new_height}")
    

