import wx
import os
import wx.adv
from hotkeys import HotkeysManager  # Import the HotkeysManager
from buttons import create_buttons
from labels import CHOIS_FOLDER_LABEL
from player import AudioPlayer
from settings import SettingsDialog
from context_menu import ShowContextMenu
from config import Config

all_play = True

class Tab1(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        config = Config()
        self.default_folder_path = config.get('FOLDER_PATH', 'folder_path1')
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.player = AudioPlayer(self)  # Pass self as the tab argument

        self.folder_path = ""  # Initialize folder_path early
        self.current_file = None

        # Create a horizontal BoxSizer for the buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create buttons and add them to the horizontal BoxSizer
        buttons = create_buttons(self)
        self.play_button = buttons["play_button"]
        self.stop_button = buttons["stop_button"]
        self.seek_backward_button = buttons["seek_backward_button"]
        self.seek_forward_button = buttons["seek_forward_button"]
        self.prev_track_button = buttons["prev_track_button"]
        self.next_track_button = buttons["next_track_button"]
        self.volume_up_button = buttons["volume_up_button"]
        self.volume_down_button = buttons["volume_down_button"]
        self.browse_button = buttons["browse_button"]
        self.pause_button = buttons["pause_button"]
        self.resume_button = buttons["resume_button"]
        self.mute_button = buttons["mute_button"]

        button_sizer.Add(self.play_button, 0, wx.ALL, 1)
        button_sizer.Add(self.pause_button, 0, wx.ALL, 1)
        button_sizer.Add(self.resume_button, 0, wx.ALL, 1)
        button_sizer.Add(self.stop_button, 0, wx.ALL, 1)
        button_sizer.Add(self.seek_backward_button, 0, wx.ALL, 1)
        button_sizer.Add(self.seek_forward_button, 0, wx.ALL, 1)
        button_sizer.Add(self.prev_track_button, 0, wx.ALL, 1)
        button_sizer.Add(self.next_track_button, 0, wx.ALL, 1)
        button_sizer.Add(self.volume_down_button, 0, wx.ALL, 1)
        button_sizer.Add(self.volume_up_button, 0, wx.ALL, 1)
        button_sizer.Add(self.mute_button, 0, wx.ALL, 1)

        # Hide pause and resume buttons initially
        self.pause_button.Hide()
        self.resume_button.Hide()

        # Bind button events
        self.play_button.Bind(wx.EVT_BUTTON, self.on_play)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop)
        self.seek_backward_button.Bind(wx.EVT_BUTTON, self.on_seek_backward)
        self.seek_forward_button.Bind(wx.EVT_BUTTON, self.on_seek_forward)
        self.prev_track_button.Bind(wx.EVT_BUTTON, self.on_prev_track)
        self.next_track_button.Bind(wx.EVT_BUTTON, self.on_next_track)
        self.volume_up_button.Bind(wx.EVT_BUTTON, self.on_volume_up)
        self.volume_down_button.Bind(wx.EVT_BUTTON, self.on_volume_down)
        self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause)
        self.resume_button.Bind(wx.EVT_BUTTON, self.on_resume)
        self.mute_button.Bind(wx.EVT_BUTTON, self.on_mute)

        # Add the horizontal BoxSizer to the vertical BoxSizer
        self.sizer.Add(button_sizer, 0, wx.ALL, 5)

        # Add a label to the panel between buttons and listbox
        self.label = wx.StaticText(self, label="Плеер 1")
        self.sizer.Add(self.label, 0, wx.ALL, 5)


        # Create a ListBox and add it to the vertical BoxSizer
        self.listbox = wx.ListBox(self)
        self.sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)

        # Initialize the context menu handler after the listbox is created
        self.context_menu = ShowContextMenu(self, self.listbox, self.folder_path)

        # Create the Browse button and add it to the vertical BoxSizer
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_folder)
        self.sizer.Add(self.browse_button, 0, wx.ALL, 5)

        # Add a label to display the active tab information
        self.active_tab_label = wx.StaticText(self, label="")
        self.sizer.Add(self.active_tab_label, 0, wx.ALL, 5)

        self.SetSizer(self.sizer)

        # Initialize the hotkeys manager and register hotkeys
        self.hotkeys_manager = HotkeysManager(self)
        self.hotkeys_manager.register_hotkeys()

        # Bind listbox selection event
        self.listbox.Bind(wx.EVT_LISTBOX, self.on_listbox_selection)
        self.listbox.Bind(wx.EVT_KEY_DOWN, self.on_key_press)

        # Load default folder and populate listbox
        self.load_default_folder()

        # Update button states initially
        self.update_button_states()

    def is_active_tab(self):
        """Check if this tab is the active tab."""
        notebook = self.GetParent()
        return notebook.GetSelection() == notebook.FindPage(self)

    def load_default_folder(self):
        self.folder_path = self.default_folder_path
        self.populate_listbox()
        self.listbox.SetFocus()  # Set focus to the listbox after loading

    def populate_listbox(self):
        self.listbox.Clear()
        if os.path.isdir(self.folder_path):
            for file_name in os.listdir(self.folder_path):
                if file_name.endswith(('.mp3', '.wav', '.ogg')):
                    self.listbox.Append(file_name)
            if self.listbox.GetCount() > 0:
                self.listbox.SetSelection(0)
        self.context_menu.folder_path = self.folder_path  # Update the folder path in the context menu
        self.update_button_states()

    def on_browse_folder(self, event):
        if not self.is_active_tab():
            return

        default_path = self.default_folder_path

        with wx.DirDialog(self, CHOIS_FOLDER_LABEL, defaultPath=default_path, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.folder_path = dialog.GetPath()
                self.populate_listbox()
                self.listbox.SetFocus()  # Set focus to the listbox

    def on_play(self, event):
        if not self.is_active_tab():
            return
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            self.current_file = os.path.join(self.folder_path, file_name)
            print(f"Playing file: {self.current_file}")  # Debug print
            self.player.play(self.current_file)
            self.play_button.Hide()
            self.pause_button.Show()
            self.Layout()

    def on_stop(self, event):
        if not self.is_active_tab():
            return
        print("Stopping playback")  # Debug print
        self.player.stop()
        self.play_button.Show()
        self.pause_button.Hide()
        self.resume_button.Hide()
        self.Layout()

    def on_seek_backward(self, event, seconds=-2):
        if not self.is_active_tab():
            return
        print(f"seconds = {seconds}")  # Debug print
        self.player.seek(seconds)  # Seek backward by 10 seconds

    def on_seek_forward(self, event, seconds=2):
        if not self.is_active_tab():
            return
        print(f"seconds = {seconds}")  # Debug print
        self.player.seek(seconds)  # Seek forward by 10 seconds

    def on_prev_track(self, event):
        if not self.is_active_tab():
            return
        selection = self.listbox.GetSelection()
        if selection > 0:
            self.listbox.SetSelection(selection - 1)
            self.on_play(None)

    def on_next_track(self, event):
        if not self.is_active_tab():
            return
        selection = self.listbox.GetSelection()
        if selection < self.listbox.GetCount() - 1:  # Ensure not to go out of bounds
            self.listbox.SetSelection(selection + 1)
        else:
            self.listbox.SetSelection(0)  # Loop back to the first item
        print("Переход к следующему элементу")
        self.on_play(None)

    def on_volume_up(self, event):
        if not self.is_active_tab():
            return
        print("Volume up")  # Debug print
        self.player.volume_up()

    def on_volume_down(self, event):
        if not self.is_active_tab():
            return
        print("Volume down")  # Debug print
        self.player.volume_down()

    def on_pause(self, event):
        if not self.is_active_tab():
            return
        print("Pausing playback")  # Debug print
        self.player.pause()
        self.pause_button.Hide()
        self.resume_button.Show()
        self.Layout()

    def on_resume(self, event):
        if not self.is_active_tab():
            return
        print("Resuming playback")  # Debug print
        self.player.pause()
        self.resume_button.Hide()
        self.pause_button.Show()
        self.Layout()

    def on_mute(self, event):
        if not self.is_active_tab():
            return
        print("Muting playback")  # Debug print
        self.player.mute()

    def on_listbox_selection(self, event):
        self.update_button_states()

    def update_button_states(self):
        selection = self.listbox.GetSelection()
        enable = selection != wx.NOT_FOUND
        self.play_button.Enable(enable)
        self.stop_button.Enable(enable)
        self.seek_backward_button.Enable(enable)
        self.seek_forward_button.Enable(enable)
        self.prev_track_button.Enable(enable)
        self.next_track_button.Enable(enable)
        self.volume_up_button.Enable(enable)
        self.volume_down_button.Enable(enable)
        self.pause_button.Enable(enable)
        self.resume_button.Enable(enable)
        self.mute_button.Enable(enable)

    def on_show_info(self, event):
        notebook = self.GetParent()
        active_tab_index = notebook.GetSelection()
        active_tab_label = ""
        active_tab_info = notebook.GetPageText(active_tab_index)
        if active_tab_info == "Tab 1":
            active_tab_label = "Плеер 1"
        elif active_tab_info == "Tab 2":
            active_tab_label = "Плеер 2"
        elif active_tab_info == "Tab 3":
            active_tab_label = "Плеер 3"
        self.active_tab_label.SetLabel(f"Активна вкладка: {active_tab_label}")
        message = f"Активна вкладка: {active_tab_label}\nОткрыта папка: {self.folder_path}"
        wx.adv.NotificationMessage("Информация:", message).Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)

    def on_play_sample(self, event, file_name_sample):
        sample_file = os.path.join("sample", file_name_sample)
        if os.path.exists(sample_file):
            print(f"Playing sample file: {sample_file}")  # Debug print
            self.player.on_play_sample(sample_file)
        else:
            wx.MessageBox("Sample file not found!", "Error", wx.OK | wx.ICON_ERROR)

    def on_refresh_listbox(self, event):
        if not self.is_active_tab():
            return
        self.populate_listbox()

    def on_space_key(self):
        if not self.is_active_tab():
            return
        if self.play_button.IsShown():
            self.on_play(None)
        elif self.pause_button.IsShown():
            self.on_pause(None)
        elif self.resume_button.IsShown():
            self.on_resume(None)

    def on_key_press(self, event):
        """Handle key press events."""
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()

        # Ignore Ctrl+Up and Ctrl+Down key events
        if (modifiers == wx.MOD_CONTROL and keycode in (wx.WXK_UP, wx.WXK_DOWN)):
            return
        if keycode in [wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_PAGEUP, wx.WXK_PAGEDOWN]:
            return
        if event.ShiftDown() and keycode in [wx.WXK_UP, wx.WXK_DOWN]:
            return

        if keycode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):  # Check for Enter or Numpad Enter
            self.on_play(None)
        elif keycode == wx.WXK_UP:  # Handle Up Arrow key
            self.navigate_listbox(-1)
        elif keycode == wx.WXK_DOWN:  # Handle Down Arrow key
            self.navigate_listbox(1)
        else:
            event.Skip()

    def navigate_listbox(self, direction):
        """Navigate the listbox based on the direction."""
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            new_selection = selection + direction
            if 0 <= new_selection < self.listbox.GetCount():
                self.listbox.SetSelection(new_selection)
                self.update_button_states()

    def on_settings(self, event):
        if not self.is_active_tab():
            return
        settings_dialog = SettingsDialog(self)
        settings_dialog.ShowModal()
        settings_dialog.Destroy()
