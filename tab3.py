from tab1 import Tab1
from config import Config

class Tab3(Tab1):
    def __init__(self, parent):
        super().__init__(parent)
        self.label.SetLabel("Плеер 3")
        config = Config()
        self.default_folder_path = config.get('FOLDER_PATH', 'folder_path3')

        # Additional initialization for Tab3 if needed

