# src/tabs.py
import wx
from tab1 import Tab1
from tab2 import Tab2
from tab3 import Tab3


class Tabs(wx.Notebook):
    def __init__(self, parent):
        super().__init__(parent)

        # Create instances of the tabs
        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)
        self.tab3 = Tab3(self)

        # Add tabs to the notebook
        self.AddPage(self.tab1, "Плеер 1")
        self.AddPage(self.tab2, "Плеер 2")
        self.AddPage(self.tab3, "Плеер 3")