# How to build and run
Run platform specific build commands below and run the generated executable. 

# Build dependencies
| Dependency | Purpose |
|------------|---------|
| nuitka | For building |
| qrcode | For generating the QR code |
| customtkinter | For UI |
| Pillow | For image handling |
| requests | For URL shortening |
| pyperclip | For clipboard access |
| validators | For validating URL |

Install build dependencies with:
`python -m pip install qrcode customtkinter Pillow nuitka requests pyperclip validators`
or 
`pip install qrcode customtkinter Pillow nuitka requests pyperclip validators`

# Platform specific build commands
## Linux
`python -m nuitka --onefile --output-filename=QRL --linux-icon=assets/python_sucks.png --lto=yes --remove-output --enable-plugin=tk-inter main.py`

## Windows
### Window dependencies
| Dependency | Purpose |
|------------|---------|
| pywin32 | For win32clipboard and win32con |

Install with 
`python.exe -m pip install pywin32`

### Build command
`python.exe -m nuitka --onefile --output-filename=QRL.exe --windows-icon-from-ico=assets/python_sucks.ico --windows-console-mode=disable --tcl-library-dir="C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python314\tcl" --tk-library-dir="C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python314\tcl" --lto=yes --remove-output --enable-plugin=tk-inter main.py`

Change `YOUR_USER` to your actual username.
Use Python 3.14 for building.

## MacOS
### MacOS dependencies
| Dependency | Purpose |
|------------|---------|
| pyobjc-framework-AppKit | For MacOS only clipboard |
| pyobjc-framework-Foundation | For MacOS only data types |

Install with
`python -m pip install pyobjc-framework-AppKit pyobjc-framework-Foundation`

### Build command
`python -m nuitka --output-filename=QRL --mode=app --macos-app-icon=assets/python_sucks.icns --lto=yes --remove-output --enable-plugin=tk-inter main.py`

# License
Licensed under MIT

# Changelog
## v1.0.1
- Fixed MacOS clipboard issues
- Fixed MacOS build command
- Added MacOS build

## v1.0
- Initial release