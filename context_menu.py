# context_menu.py
import wx
import os
from labels import COPY_LABEL, PASTE_LABEL, DELETE_LABEL, RENAME_LABEL, NEW_NAME, CONFIRM_DELETE, DELETE_FILE

clipboard = None
ID_RENAME = wx.NewId()  # Use wx.NewId() instead of wx.NewIdRef().Id

class ShowContextMenu:
    def __init__(self, parent, listbox, folder_path):
        self.parent = parent
        self.listbox = listbox
        self.folder_path = folder_path
        print(self.folder_path)
        self.is_open = False  # Добавляем атрибут для отслеживания состояния

    def show(self):
        self.is_open = True  # Устанавливаем в True при открытии
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            menu = wx.Menu()
            menu.Append(wx.ID_COPY, COPY_LABEL)
            menu.Append(wx.ID_PASTE, PASTE_LABEL)
            menu.Append(wx.ID_DELETE, DELETE_LABEL)
            menu.Append(ID_RENAME, RENAME_LABEL)  # Use custom ID_RENAME
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_copy(event), id=wx.ID_COPY)
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_paste(event), id=wx.ID_PASTE)
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_delete(event), id=wx.ID_DELETE)
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_rename(event), id=ID_RENAME)  # Bind Rename event with custom ID
            
            # Get the center position of the parent window
            parent_pos = self.parent.GetPosition()
            parent_size = self.parent.GetSize()
            center_pos = (parent_pos.x + parent_size.x // 2, parent_pos.y + parent_size.y // 2)
            
            self.parent.PopupMenu(menu, center_pos)
            menu.Destroy()
            self.is_open = False  # Устанавливаем в False после закрытия

    def on_copy(self, event):
        global clipboard
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            clipboard = os.path.join(self.folder_path, file_name)
            print(clipboard)

    def on_paste(self, event):
        global clipboard
        if clipboard:
            destination = os.path.join(self.folder_path, os.path.basename(clipboard))
            if not os.path.exists(destination):
                with open(clipboard, 'rb') as src_file:
                    with open(destination, 'wb') as dest_file:
                        dest_file.write(src_file.read())
                self.listbox.Append(os.path.basename(clipboard))
                clipboard = None
                # Refresh the listbox
                self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.Clear()
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.mp3') or file_name.endswith('.wav'):  # Add filter for audio files
                self.listbox.Append(file_name)

    def on_delete(self, event):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            confirm_dialog = wx.MessageDialog(self.parent, f"{DELETE_FILE} {file_name}?", CONFIRM_DELETE, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
            if confirm_dialog.ShowModal() == wx.ID_YES:
                os.remove(os.path.join(self.folder_path, file_name))
                self.listbox.Delete(selection)
            confirm_dialog.Destroy()

    def on_rename(self, event):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            new_file_name = wx.GetTextFromUser(NEW_NAME, RENAME_LABEL, file_name)
            if new_file_name:
                old_path = os.path.join(self.folder_path, file_name)
                new_path = os.path.join(self.folder_path, new_file_name)
                os.rename(old_path, new_path)
                self.refresh_listbox()

    def on_context_menu_key(self):
        """Open the context menu programmatically."""
        self.show()

    def on_key_press(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_F2:
            self.on_rename(event)
        elif keycode == wx.WXK_F5:
            self.refresh_listbox()
        else:
            event.Skip()
