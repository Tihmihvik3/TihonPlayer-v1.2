import wx
from labels import DEFAULT_FOLDER_LABEL
from labels import CHOIS_FOLDER_LABEL
from labels import BROWS_BUTTON
from labels import CHOIS_DEFAULT_FOLDER_LABEL
from labels import SAVE_BUTTON


class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Настройки", size=(300, 200))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.default_folder_label = wx.StaticText(self.panel, label = CHOIS_DEFAULT_FOLDER_LABEL)
        self.default_folder_text = wx.TextCtrl(self.panel)
        self.browse_button = wx.Button(self.panel, label=BROWS_BUTTON)
        self.save_button = wx.Button(self.panel, label=SAVE_BUTTON)

        self.sizer.Add(self.default_folder_label, 0, wx.ALL, 5)
        self.sizer.Add(self.default_folder_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.browse_button, 0, wx.ALL, 5)
        self.sizer.Add(self.save_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.SetSizer(self.sizer)

        self.Bind(wx.EVT_BUTTON, self.on_browse, self.browse_button)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save_button)

        self.default_folder = None
        self.load_default_folder()

    def load_default_folder(self):
        try:
            with open("default_folder.txt", "r") as file:
                self.default_folder = file.read().strip()
                self.default_folder_text.SetValue(self.default_folder)
        except FileNotFoundError:
            pass

    def on_browse(self, event):
        with wx.DirDialog(self, CHOIS_DEFAULT_FOLDER_LABEL, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.default_folder = dialog.GetPath()
                self.default_folder_text.SetValue(self.default_folder)

    def on_save(self, event):
        self.default_folder = self.default_folder_text.GetValue()
        with open("default_folder.txt", "w") as file:
            file.write(self.default_folder)
        self.Close()
