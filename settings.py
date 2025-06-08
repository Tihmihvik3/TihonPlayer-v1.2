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
        folder_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.default_folder_label1 = wx.StaticText(self.panel, label=CHOIS_DEFAULT_FOLDER_LABEL + 'для плеера')
        self.default_folder_text1 = wx.TextCtrl(self.panel)
        self.browse_button1 = wx.Button(self.panel, label=BROWS_BUTTON)

        # Add a checkbox for "Воспроизводить весь список"
        self.play_all_checkbox = wx.CheckBox(self.panel, label="Воспроизводить весь список")

        # Add a radio box for playback options
        self.playback_options1 = wx.RadioBox(
            self.panel,
            label="Настройка повтора",
            choices=["Отключено", "Повтор трека", "Повтор списка треков"],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS  # Располагаем кнопки вертикально
        )

        self.save_button = wx.Button(self.panel, label=SAVE_BUTTON)
        self.cancel_button = wx.Button(self.panel, label="Отмена")
        # Bind focus event to show a tooltip
        self.save_button.Bind(wx.EVT_SET_FOCUS, self.on_focus_save)

        # Bind the ESC key to the on_cancel method
        accelerators = [
            (wx.ACCEL_NORMAL, wx.WXK_ESCAPE, self.cancel_button.GetId())
        ]
        self.SetAcceleratorTable(wx.AcceleratorTable(accelerators))

        folder_sizer.Add(self.default_folder_text1, 1, wx.ALL | wx.EXPAND, 5)
        folder_sizer.Add(self.browse_button1, 0, wx.ALL, 5)

        button_sizer.Add(self.save_button, 0, wx.ALL, 5)
        button_sizer.Add(self.cancel_button, 0, wx.ALL, 5)

        self.sizer.Add(self.default_folder_label1, 0, wx.ALL, 5)
        self.sizer.Add(folder_sizer, 0, wx.EXPAND, 5)

        # Add the checkbox to the sizer
        self.sizer.Add(self.play_all_checkbox, 0, wx.ALL, 5)

        self.sizer.Add(self.playback_options1, 0, wx.ALL | wx.EXPAND, 5)

        self.sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.panel.SetSizer(self.sizer)

        self.play_all_checkbox.SetValue(config.get('REPEAT_MUSIC', 'all_list') == 'True')

        if config.get('REPEAT_MUSIC', 'repeat_track') == 'True':
            self.playback_options1.SetSelection(1)
        elif config.get('REPEAT_MUSIC', 'repeat_list') == 'True':
            self.playback_options1.SetSelection(2)
        else:
            self.playback_options1.SetSelection(0)

        self.on_checkbox_toggle(None)

        # Check and print the state of the second RadioBox option
        is_second_option_enabled = self.playback_options1.IsItemEnabled(1)
        print(self.playback_options1.IsItemEnabled(1))

        # Bind events
        self.play_all_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_toggle)
        self.Bind(wx.EVT_BUTTON, self.on_browse1, self.browse_button1)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_button)

        self.default_folder = None
        self.load_default_folder1()

    def load_default_folder1(self):
        folder_path1 = config.get('FOLDER_PATH', 'folder_path1')
        self.default_folder_text1.SetValue(folder_path1)

    def on_browse1(self, event):
        with wx.DirDialog(self, CHOIS_DEFAULT_FOLDER_LABEL, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.default_folder = dialog.GetPath()
                self.default_folder_text1.SetValue(self.default_folder)
                print(self.default_folder_text1.GetValue())

    def on_save(self, event):
        config.set('FOLDER_PATH', 'folder_path1', self.default_folder_text1.GetValue())
        config.set('REPEAT_MUSIC', 'repeat_track', str(self.playback_options1.GetSelection() == 1))
        config.set('REPEAT_MUSIC', 'repeat_list', str(self.playback_options1.GetSelection() == 2))
        config.set('REPEAT_MUSIC', 'all_list', str(self.play_all_checkbox.IsChecked()))
        config.save()
        self.Close()

    def on_checkbox_toggle(self, event):
        if self.play_all_checkbox.IsChecked():
            # Disable "Повтор трека", enable "Повтор списка треков", set to "Отключено"
            self.playback_options1.EnableItem(1, False)  # Disable "Повтор трека"
            self.playback_options1.EnableItem(2, True)   # Enable "Повтор списка треков"
            self.playback_options1.SetSelection(0)      # Set to "Отключено"
        else:
            # Enable "Повтор трека", disable "Повтор списка треков", set to "Отключено"
            self.playback_options1.EnableItem(1, True)  # Enable "Повтор трека"
            self.playback_options1.EnableItem(2, False) # Disable "Повтор списка треков"
            self.playback_options1.SetSelection(0)      # Set to "Отключено"

    def on_cancel(self, event):
        self.Close()

    def on_focus_save(self, event):
        wx.TipWindow(self, "Сохранить изменения")
        event.Skip()