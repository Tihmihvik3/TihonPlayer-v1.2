import wx
from tabs import Tabs
from settings import SettingsDialog

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = Tabs(panel)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        # Activate the first tab and set focus to the listbox
        self.notebook.SetSelection(0)
        self.notebook.tab1.listbox.SetFocus()

        # Bind the close event to the on_close method
        self.Bind(wx.EVT_CLOSE, self.on_close)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('1'), 1000),  # Ctrl+1 for Tab 1
            (wx.ACCEL_CTRL, ord('2'), 1001),  # Ctrl+1 for Tab 2
            (wx.ACCEL_CTRL, ord('3'), 1002)  # Ctrl+3 for Tab 3
        ])
        self.SetAcceleratorTable(accel_tbl)

        # Bind the accelerator table events
        self.Bind(wx.EVT_MENU, lambda event: self.activate_tab(0), id=1000)  # Bind Ctrl+1 to tab1
        self.Bind(wx.EVT_MENU, lambda event: self.activate_tab(1), id=1001)  # Bind Ctrl+1 to tab2
        self.Bind(wx.EVT_MENU, lambda event: self.activate_tab(2), id=1002)  # Bind Ctrl+3 to tab3

    def activate_tab(self, tab_index):
        """Activate the specified tab by index."""
        self.notebook.SetSelection(tab_index)
        active_tab = [self.notebook.tab1, self.notebook.tab2, self.notebook.tab3][tab_index]
        active_tab.listbox.SetFocus()

    def on_close(self, event):
        # Stop all processes and clear the player
        for tab in [self.notebook.tab1, self.notebook.tab2, self.notebook.tab3]:
            tab.player.stop()
        self.Destroy()

def create_window():
    app = wx.App(False)
    frame = MyFrame(None, title="TihonPlayer v1.1", size=(400, 400))
    frame.Show(True)

    app.MainLoop()

create_window()
