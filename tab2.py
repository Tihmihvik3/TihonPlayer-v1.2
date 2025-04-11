from tab1 import Tab1

class Tab2(Tab1):
    def __init__(self, parent):
        super().__init__(parent)
        self.label.SetLabel("Плеер 2")

        # Additional initialization for Tab2 if needed

