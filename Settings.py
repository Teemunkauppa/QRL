import Helpers
import SaveSystem
import customtkinter as ct

class Settings():
    name: str = ""
    tab: ct.CTkFrame = None

    enableAdvToggle: ct.CTkCheckBox = None

    def __init__(self, tabview: ct.CTkTabview, name: str, size: tuple[int]):
        self.tab = tabview.add(name)
        self.name = name
        self.DrawUI(size)

    def DrawUI(self, size: tuple[int]):
        # Split into 2 columns
        self.tab.columnconfigure(0, weight=1)
        self.tab.columnconfigure(1, weight=1)
        self.tab.rowconfigure(1, weight=1)

        # Title
        title = Helpers.GenerateTitle(master=self.tab, text=self.name, font=("ArialBold", 20))
        title.grid(row=0, column=0, columnspan=2, pady=(5, 5))

        # Left panel
        left = Helpers.GenerateFrame(master=self.tab)
        left.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        # General title
        generalTitle = Helpers.GenerateTitle(master=left, text="General", font=("ArialBold", 18))
        generalTitle.pack(pady=(10, 10), anchor="n")

        # Default tab dropdown
        defaultTabDropdown = Helpers.GenerateDropdown(left, "Default tab", SaveSystem.Tabs().Get(), SaveSystem.GetSettings().defaultTab, self.EventTabDropdown)

        # QrGen title
        qrGenTitle = Helpers.GenerateTitle(master=left, text="QR Code -Generator", font=("ArialBold", 18))
        qrGenTitle.pack(pady=(20, 10), anchor="n")

        # Enable adv by default
        self.enableAdvToggle = Helpers.GenerateCheckbox(master=left, text="Enable advanced settings by default", font=("Arial", 14), checked=SaveSystem.GetSettings().enableAdv, command=self.EventEnableAdv)
        self.enableAdvToggle.pack(pady=(0, 0), anchor="nw")

        # Reset to defaults title
        resetDefaultsTitle = Helpers.GenerateTitle(master=left, text="Reset to defaults", font=("ArialBold", 18))
        resetDefaultsTitle.pack(pady=(20, 10), anchor="n")

        # Reset to defaults button
        resetDefaultsButton = Helpers.GenerateButton(master=left, text="Reset to defaults", command=self.EventResetDefaults)
        resetDefaultsButton.pack(pady=(0, 0), anchor="nw")

        # Right panel
        right = Helpers.GenerateFrame(self.tab)
        right.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1) 

        # Style title
        styleTitle: ct.CTkFrame = Helpers.GenerateTitle(master=right, text="Style", font=("ArialBold", 18))
        styleTitle.grid(row=0, column=0, pady=(5, 5), sticky="n")

        # Scroll frame
        scrollFrame = Helpers.GenerateScrollFrame(right)
        scrollFrame.grid(row=1, column=0, sticky="nsew", padx=(0, 0))
        scrollFrame.grid_columnconfigure(0, weight=1)

        # Colors
        fgColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Foreground color", SaveSystem.GetSettings().GetFgColor(), "Pick new color", self.EventPickFgColor)
        bgColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Background color", SaveSystem.GetSettings().GetBgColor(), "Pick new color", self.EventPickBgColor)
        hoverColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Hover color", SaveSystem.GetSettings().GetHoverColor(), "Pick new color", self.EventPickHoverColor)
        buttonHoverColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Button hover color", SaveSystem.GetSettings().GetButtonHoverColor(), "Pick new color", self.EventPickButtonHoverColor)
        borderColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Border color", SaveSystem.GetSettings().GetBorderColor(), "Pick new color", self.EventPickBorderColor)
        textColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Text color", SaveSystem.GetSettings().GetTextColor(), "Pick new color", self.EventPickTextColor)
        checkmarkColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Checkmark color", SaveSystem.GetSettings().GetCheckmarkColor(), "Pick new color", self.EventPickCheckmarkColor)
        progressColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Slider progress color", SaveSystem.GetSettings().GetProgressColor(), "Pick new color", self.EventPickProgressColor)
        buttonColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Button color", SaveSystem.GetSettings().GetButtonColor(), "Pick new color", self.EventPickButtonColor)
        dropdownFgColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Dropdown color", SaveSystem.GetSettings().GetDropdownFgColor(), "Pick new color", self.EventPickDropdownFgColor)
        dropdownTextColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Dropdown text color", SaveSystem.GetSettings().GetDropdownTextColor(), "Pick new color", self.EventPickDropdownTextColor)
        placeholderTextColorButton = Helpers.GenerateColorPickerButton(scrollFrame, "Placeholder text color", SaveSystem.GetSettings().GetPlaceholderTextColor(), "Pick new color", self.EventPickPlaceholderTextColor)
        textColorDisabledButton = Helpers.GenerateColorPickerButton(scrollFrame, "Disabled text color", SaveSystem.GetSettings().GetTextColorDisabled(), "Pick new color", self.EventPickTextDisabledColor)

    def EventTabDropdown(self, sel):
        SaveSystem.GetSettings().defaultTab = sel
        SaveSystem.QueueSave()

    def EventEnableAdv(self):
        SaveSystem.GetSettings().enableAdv = True if self.enableAdvToggle.get() else False
        SaveSystem.QueueSave()

    def Focus(self, tabview: ct.CTkTabview):
        tabview.set(self.name)

    def EventPickFgColor(self):
        SaveSystem.GetSettings().fgColor = Helpers.PickColor(SaveSystem.GetSettings().fgColor)
        SaveSystem.QueueSave(True)

    def EventPickBgColor(self):
        SaveSystem.GetSettings().bgColor = Helpers.PickColor(SaveSystem.GetSettings().bgColor)
        SaveSystem.QueueSave(True)

    def EventPickHoverColor(self):
        SaveSystem.GetSettings().hoverColor = Helpers.PickColor(SaveSystem.GetSettings().hoverColor)
        SaveSystem.QueueSave(True)

    def EventPickButtonHoverColor(self):
        SaveSystem.GetSettings().buttonHoverColor = Helpers.PickColor(SaveSystem.GetSettings().buttonHoverColor)
        SaveSystem.QueueSave(True)

    def EventPickBorderColor(self):
        SaveSystem.GetSettings().borderColor = Helpers.PickColor(SaveSystem.GetSettings().borderColor)
        SaveSystem.QueueSave(True)

    def EventPickTextColor(self):
        SaveSystem.GetSettings().textColor = Helpers.PickColor(SaveSystem.GetSettings().textColor)
        SaveSystem.QueueSave(True)

    def EventPickCheckmarkColor(self):
        SaveSystem.GetSettings().checkmarkColor = Helpers.PickColor(SaveSystem.GetSettings().checkmarkColor)
        SaveSystem.QueueSave(True)

    def EventPickProgressColor(self):
        SaveSystem.GetSettings().progressColor = Helpers.PickColor(SaveSystem.GetSettings().progressColor)
        SaveSystem.QueueSave()

    def EventPickButtonColor(self):
        SaveSystem.GetSettings().buttonColor = Helpers.PickColor(SaveSystem.GetSettings().buttonColor)
        SaveSystem.QueueSave(True)

    def EventPickDropdownFgColor(self):
        SaveSystem.GetSettings().dropdownFgColor = Helpers.PickColor(SaveSystem.GetSettings().dropdownFgColor)
        SaveSystem.QueueSave(True)

    def EventPickDropdownTextColor(self):
        SaveSystem.GetSettings().dropdownTextColor = Helpers.PickColor(SaveSystem.GetSettings().dropdownTextColor)
        SaveSystem.QueueSave(True)

    def EventPickPlaceholderTextColor(self):
        SaveSystem.GetSettings().placeholderTextColor = Helpers.PickColor(SaveSystem.GetSettings().placeholderTextColor)
        SaveSystem.QueueSave(True)

    def EventPickTextDisabledColor(self):
        SaveSystem.GetSettings().textColorDisabled = Helpers.PickColor(SaveSystem.GetSettings().textColorDisabled)
        SaveSystem.QueueSave(True)

    def EventResetDefaults(self):
        SaveSystem.settings = SaveSystem.SettingsData()
        SaveSystem.QueueSave(True)