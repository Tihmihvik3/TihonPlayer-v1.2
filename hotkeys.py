import keyboard
import wx

class HotkeysManager:
    def __init__(self, tab):
        self.tab = tab

    def is_main_window_active(self):
        """Check if the main window is active."""
        main_window = wx.GetTopLevelParent(self.tab)
        return wx.GetActiveWindow() == main_window

    def register_hotkeys(self):
        """Register all hotkeys for the tab."""
        keyboard.add_hotkey('ctrl+b', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_browse_folder, None))
        keyboard.add_hotkey('space', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_space_key))
        keyboard.add_hotkey('ctrl+space', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_stop, None))
        keyboard.add_hotkey('menu', lambda: wx.CallAfter(self.execute_if_active, self.tab.context_menu.show))
        keyboard.add_hotkey('page up', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_prev_track, None))
        keyboard.add_hotkey('page down', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_next_track, None))
        keyboard.add_hotkey('ctrl+left', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_seek_backward, None, -10))
        keyboard.add_hotkey('alt+left', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_seek_backward, None, -30))
        keyboard.add_hotkey('ctrl+right', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_seek_forward, None, 10))
        keyboard.add_hotkey('alt+right', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_seek_forward, None, 30))
        keyboard.add_hotkey('left', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_seek_backward, None))
        keyboard.add_hotkey('right', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_seek_forward, None))
        keyboard.add_hotkey('esc', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_mute, None))
        keyboard.add_hotkey('ctrl+up', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_volume_up, None))
        keyboard.add_hotkey('ctrl+down', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_volume_down, None))
        keyboard.add_hotkey('ctrl+p', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_settings, None))
        keyboard.add_hotkey('shift+q', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_sample, None, '01.mp3'))
        keyboard.add_hotkey('shift+w', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_sample, None, '02.mp3'))
        keyboard.add_hotkey('shift+e', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_sample, None, '03.mp3'))
        keyboard.add_hotkey('shift+r', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_sample, None, '04.mp3'))
        keyboard.add_hotkey('shift+t', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_sample, None, '05.mp3'))
        keyboard.add_hotkey('shift+1', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_bookmarks, 1))
        keyboard.add_hotkey('shift+2', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_bookmarks, 2))
        keyboard.add_hotkey('shift+3', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_bookmarks, 3))
        keyboard.add_hotkey('alt+1', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_bookmarks, 1))
        keyboard.add_hotkey('alt+2', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_bookmarks, 2))
        keyboard.add_hotkey('alt+3', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play_bookmarks, 3))
        keyboard.add_hotkey('enter', lambda: wx.CallAfter(self.execute_if_active, self.tab.on_play, None))

    def execute_if_active(self, func, *args, **kwargs):
        """Execute the function only if the main window is active."""
        if self.is_main_window_active():
            func(*args, **kwargs)