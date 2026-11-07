import SaveSystem
import customtkinter as ct
from tkinter.font import Font
import CTkColorPicker as ctkcp

def GenerateFrame(master: ct.CTkBaseClass, transparent: bool = False) -> ct.CTkFrame:
    if transparent:
        return ct.CTkFrame(master, fg_color="transparent")
    
    return ct.CTkFrame(master, fg_color=SaveSystem.GetSettings().fgColor, bg_color=SaveSystem.GetSettings().bgColor, border_color=SaveSystem.GetSettings().borderColor)

def GenerateScrollFrame(master: ct.CTkBaseClass) -> ct.CTkScrollableFrame:
    return ct.CTkScrollableFrame(master=master, fg_color="transparent", bg_color=SaveSystem.GetSettings().bgColor)

def GenerateEntry(master: ct.CTkBaseClass, placeholder_text: str = "", width: int = 200, height: int = 30, textvariable=None) -> ct.CTkEntry:
    return ct.CTkEntry(master=master, placeholder_text=placeholder_text, width=width, height=height, textvariable=textvariable, fg_color=SaveSystem.GetSettings().fgColor, bg_color=SaveSystem.GetSettings().bgColor, border_color=SaveSystem.GetSettings().borderColor, text_color=SaveSystem.GetSettings().textColor, placeholder_text_color=SaveSystem.GetSettings().placeholderTextColor)

def GenerateCheckbox(master: ct.CTkBaseClass, text: str = "", font=None, checked=False, command=None) -> ct.CTkCheckBox:
    var = ct.BooleanVar(value=bool(checked))
    return ct.CTkCheckBox(master=master, text=text, font=font, variable=var, command=command, fg_color=SaveSystem.GetSettings().fgColor, bg_color=SaveSystem.GetSettings().bgColor, hover_color=SaveSystem.GetSettings().hoverColor, border_color=SaveSystem.GetSettings().borderColor, checkmark_color=SaveSystem.GetSettings().checkmarkColor, text_color=SaveSystem.GetSettings().textColor)

def GenerateButton(master: ct.CTkBaseClass, text: str = "", command=None, width: int = 0) -> ct.CTkButton:
    button = ct.CTkButton(master=master, text=text, command=command, fg_color=SaveSystem.GetSettings().buttonColor, bg_color=SaveSystem.GetSettings().bgColor, hover_color=SaveSystem.GetSettings().buttonHoverColor, border_color=SaveSystem.GetSettings().borderColor, text_color=SaveSystem.GetSettings().textColor, text_color_disabled=SaveSystem.GetSettings().textColorDisabled)
    if width > 0:
        button.configure(width=width)
    return button

def GenerateCanvas(master: ct.CTkBaseClass, width: int, height: int) -> ct.CTkCanvas:
    # CTkCanvas is a plain Tk canvas: it takes bg, not CTk color params
    return ct.CTkCanvas(master=master, width=width, height=height, bg="#FFFFFF", highlightthickness=0)

def GenerateDropdown(master: ct.CTkFrame, title: str, options: list, curSelection, eventFunc: function) -> ct.CTkComboBox:
    dropdownTitle: ct.CTkLabel = None
    dropdown: ct.CTkComboBox = None

    # Dropdown row
    row = ct.CTkFrame(master, fg_color="transparent")
    row.pack(fill="x", pady=(5, 5))
    row.grid_columnconfigure(1, weight=1)
    
    # Dropdown title
    dropdownTitle = GenerateTitle(master=row, text=title, font=("Arial", 14), text_color=SaveSystem.GetSettings().textColor)
    dropdownTitle.grid(row=0, column=0, padx=(0, 0), sticky="w")

    # Calculate padding with title width
    titleWidth = dropdownTitle.winfo_reqwidth()
    tkFont: Font = Font(family="Arial", size=14)
    textWidth = tkFont.measure(title)
    dropdownPadding = titleWidth + textWidth

    # Dropdown
    dropdown = ct.CTkComboBox(master=row, values=options, command=eventFunc, dropdown_fg_color=SaveSystem.GetSettings().dropdownFgColor, dropdown_text_color=SaveSystem.GetSettings().dropdownTextColor, fg_color=SaveSystem.GetSettings().dropdownFgColor, text_color=SaveSystem.GetSettings().dropdownTextColor, button_color=SaveSystem.GetSettings().buttonColor, button_hover_color=SaveSystem.GetSettings().buttonHoverColor, border_color=SaveSystem.GetSettings().borderColor, bg_color=SaveSystem.GetSettings().bgColor)
    dropdown.grid(row=0, column=0, padx=(dropdownPadding), sticky="w")
    dropdown.set(curSelection)

    return dropdown

def CreateSlider(master: ct.CTkFrame, min: int, max: int, titleText: str, eventFunc: function) -> tuple[ct.CTkSlider, ct.CTkLabel]:
    sliderTitle: ct.CTkLabel = None
    slider: ct.CTkSlider = None
    sliderValue: ct.CTkLabel = None

    # Slider row
    row = ct.CTkFrame(master, fg_color="transparent")
    row.pack(fill="x", pady=(15, 5))
    row.grid_columnconfigure(1, weight=1)
    
    # Slider title
    sliderTitle = GenerateTitle(master=row, text=titleText, font=("Arial", 14), text_color=SaveSystem.GetSettings().textColor)
    sliderTitle.grid(row=0, column=0, padx=(0, 0), sticky="w")

    # Calculate padding with title width
    titleWidth = sliderTitle.winfo_reqwidth()
    tkFont: Font = Font(family="Arial", size=14)
    textWidth = tkFont.measure(titleText)
    sliderPadding = titleWidth + textWidth

    # Slider
    slider = ct.CTkSlider(master=row, from_=min, to=max, height=20, number_of_steps=max, command=eventFunc, fg_color=SaveSystem.GetSettings().fgColor, bg_color=SaveSystem.GetSettings().bgColor, border_color=SaveSystem.GetSettings().borderColor, button_color=SaveSystem.GetSettings().buttonColor, progress_color=SaveSystem.GetSettings().progressColor, button_hover_color=SaveSystem.GetSettings().buttonHoverColor)
    slider.grid(row=0, column=0, padx=(sliderPadding), sticky="w")

    # Padding for slider value
    sliderWidth = slider.winfo_reqwidth()
    sliderValPadding = sliderPadding + sliderWidth + 5

    # Slider value
    sliderValue = GenerateTitle(master=row, text="", font=("Arial", 14), text_color=SaveSystem.GetSettings().textColor)
    sliderValue.grid(row=0, column=0, padx=(sliderValPadding, 0), sticky="w")

    return (slider, sliderValue)

def GenerateColorPickerButton(master: ct.CTkFrame, title: str, curColor: str, buttonText:str, buttonCommand: function) -> ct.CTkButton:
    pickerTitle: ct.CTkLabel = None
    pickerButton: ct.CTkButton = None

    # Row
    row = ct.CTkFrame(master, fg_color="transparent")
    row.pack(fill="x", pady=(5, 5))
    row.grid_columnconfigure(0, weight=1)  # title column expands
    row.grid_columnconfigure(1, weight=0)  # preview box fixed
    row.grid_columnconfigure(2, weight=0)  # button fixed

    # Title 
    pickerTitle = GenerateTitle(row, text=title, font=("Arial", 14), text_color=SaveSystem.GetSettings().textColor)
    pickerTitle.grid(row=0, column=0, sticky="w")

    # Preview box 
    previewSize = 20
    colorBox = ct.CTkFrame(row, width=previewSize, height=previewSize, fg_color=curColor)
    colorBox.grid(row=0, column=1, padx=(15, 15), sticky="e")

    # Picker button
    pickerButton = ct.CTkButton(row, text=buttonText, command=buttonCommand, fg_color=SaveSystem.GetSettings().buttonColor, bg_color=SaveSystem.GetSettings().bgColor, text_color=SaveSystem.GetSettings().textColor, text_color_disabled=SaveSystem.GetSettings().textColorDisabled, hover_color=SaveSystem.GetSettings().buttonHoverColor)
    pickerButton.grid(row=0, column=2, sticky="e")

    return pickerButton

def PickColor(colorToPick: str) -> str:
    bgColor = SaveSystem.GetSettings().GetBgColor()
    if bgColor == "transparent":
        bgColor = SaveSystem.GetSettings().GetFgColor()

    initialColor = colorToPick
    if colorToPick == "transparent" or initialColor == "":
        initialColor = bgColor

    pickColor = ctkcp.AskColor(width=300, title="Pick new color", fg_color=SaveSystem.GetSettings().GetFgColor(), bg_color=bgColor, button_color=SaveSystem.GetSettings().GetButtonColor(), button_hover_color=SaveSystem.GetSettings().GetButtonHoverColor(), text="Confirm", initial_color=initialColor)
    newColor = pickColor.get()

    if isinstance(newColor, str) and len(newColor) == 9 and newColor.startswith("#") and newColor[7:9].lower() == "00":
        newColor = "transparent"

    return newColor

def GenerateTitle(master: ct.CTkFrame, text: str, font: tuple[str, str], text_color: str = "", justify: str = "", wraplength: int = 0) -> ct.CTkLabel:
    if text_color == "":
        text_color = SaveSystem.GetSettings().GetTextColor()
    return ct.CTkLabel(master=master, text=text, font=font, text_color=text_color, bg_color=SaveSystem.GetSettings().GetBgColor())