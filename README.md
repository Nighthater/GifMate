# GifMate

```
This is a Work in Progress! Some stuff might not Work.

Encountered a Problem? Please open an issue
```

GifMate is a Python application that allows you to display and interact with GIFs using a Tkinter-based GUI.  
This tool provides various functionalities such as resizing the GIF, changing its framerate, and importing new GIFs.

## Feature Overview

### Implemented

- Transparent Window: The application window is transparent, displaying only the GIF.
- Always on Top: The window stays on top of other windows.
- Context Menu: Right-click to access a context menu with various options.
- Customizable: Change the GIF size, framerate, and transparency settings.
- Drag to Move: Click and drag to move the window.
- Persistent State: The application's position is saved between sessions.
- Portable: The Program only requires a folder to work

### Installation

1. Clone the repository:

``` bash
git clone https://github.com/Nighthater/GifMate.git
cd gifmate
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```
### Usage

1. Prepare the configuration file  ```config.yaml``` in the root directory:

```yaml
gif_name: [FILENAME / PATH TO GIF].gif
first_run: true
last_pos_X: 0
last_pos_Y: 0
```

2. Run the application:

```bash
python main.py
```

The Gif should appear in the centre of your monitor.

### License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

Enjoy using GifMate!
