import wx
from labels import DEFAULT_FOLDER_LABEL
from labels import CHOIS_FOLDER_LABEL
from labels import BROWS_BUTTON
from labels import CHOIS_DEFAULT_FOLDER_LABEL
from labels import SAVE_BUTTON
from config import Config

config = Config()


class SettingsDialog(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, title="Настройки", size=(300, 700))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.default_folder_label1 = wx.StaticText(self.panel, label=CHOIS_DEFAULT_FOLDER_LABEL + 'для плеера 1')
        self.default_folder_text1 = wx.TextCtrl(self.panel)
        self.browse_button1 = wx.Button(self.panel, label=BROWS_BUTTON)
        self.default_folder_label2 = wx.StaticText(self.panel, label=CHOIS_DEFAULT_FOLDER_LABEL + 'для плеера 2')
        self.default_folder_text2 = wx.TextCtrl(self.panel)
        self.browse_button2 = wx.Button(self.panel, label=BROWS_BUTTON)
        self.default_folder_label3 = wx.StaticText(self.panel, label=CHOIS_DEFAULT_FOLDER_LABEL + 'для плеера 3')
        self.default_folder_text3 = wx.TextCtrl(self.panel)
        self.browse_button3 = wx.Button(self.panel, label=BROWS_BUTTON)

        # Add a radio box for playback options
        self.playback_options1 = wx.RadioBox(
            self.panel,
            label="Настройка повтора в плеере 1",
            choices=["Отключено", "Повтор трека", "Повтор списка треков"],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS  # Располагаем кнопки вертикально
        )

        self.playback_options2 = wx.RadioBox(
            self.panel,
            label="Настройка повтора в плеере 2",
            choices=["Отключено", "Повтор трека", "Повтор списка треков"],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS  # Располагаем кнопки вертикально
        )

        self.playback_options3 = wx.RadioBox(
            self.panel,
            label="Настройка повтора в плеере 3",
            choices=["Отключено", "Повтор трека", "Повтор списка треков"],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS  # Располагаем кнопки вертикально
        )

        self.save_button = wx.Button(self.panel, label=SAVE_BUTTON)

        self.sizer.Add(self.default_folder_label1, 0, wx.ALL, 5)
        self.sizer.Add(self.default_folder_text1, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.browse_button1, 0, wx.ALL, 5)
        self.sizer.Add(self.default_folder_label2, 0, wx.ALL, 5)
        self.sizer.Add(self.default_folder_text2, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.browse_button2, 0, wx.ALL, 5)
        self.sizer.Add(self.default_folder_label3, 0, wx.ALL, 5)
        self.sizer.Add(self.default_folder_text3, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.browse_button3, 0, wx.ALL, 5)
        self.sizer.Add(self.playback_options1, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.playback_options2, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.playback_options3, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.save_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.SetSizer(self.sizer)

        self.Bind(wx.EVT_BUTTON, self.on_browse1, self.browse_button1)
        self.Bind(wx.EVT_BUTTON, self.on_browse2, self.browse_button2)
        self.Bind(wx.EVT_BUTTON, self.on_browse3, self.browse_button3)

        self.Bind(wx.EVT_BUTTON, self.on_save, self.save_button)

        self.default_folder = None
        self.load_default_folder1()
        self.load_default_folder2()
        self.load_default_folder3()

    def load_default_folder1(self):
        folder_path1 = config.get('FOLDER_PATH', 'folder_path1')
        self.default_folder_text1.SetValue(folder_path1)

    def load_default_folder2(self):
        folder_path2 = config.get('FOLDER_PATH', 'folder_path2')
        self.default_folder_text2.SetValue(folder_path2)

    def load_default_folder3(self):
        folder_path3 = config.get('FOLDER_PATH', 'folder_path3')
        self.default_folder_text3.SetValue(folder_path3)

    def on_browse1(self, event):
        with wx.DirDialog(self, CHOIS_DEFAULT_FOLDER_LABEL, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.default_folder = dialog.GetPath()
                self.default_folder_text1.SetValue(self.default_folder)
                print(self.default_folder_text1.GetValue())

    def on_browse2(self, event):
        with wx.DirDialog(self, CHOIS_DEFAULT_FOLDER_LABEL, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.default_folder = dialog.GetPath()
                self.default_folder_text2.SetValue(self.default_folder)

    def on_browse3(self, event):
        with wx.DirDialog(self, CHOIS_DEFAULT_FOLDER_LABEL, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.default_folder = dialog.GetPath()
                self.default_folder_text3.SetValue(self.default_folder)

    def on_save(self, event):
        config.set('FOLDER_PATH', 'folder_path1', self.default_folder_text1.GetValue())
        config.set('FOLDER_PATH', 'folder_path2', self.default_folder_text2.GetValue())
        config.set('FOLDER_PATH', 'folder_path3', self.default_folder_text3.GetValue())
        config.save()
        self.Close()
