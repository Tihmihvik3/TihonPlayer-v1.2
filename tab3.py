from tab1 import Tab1

class Tab3(Tab1):
    def __init__(self, parent):
        super().__init__(parent)
        self.label.SetLabel("Плеер 3")

        # Additional initialization for Tab3 if needed

