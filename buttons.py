import wx
from labels import BUTTON_LABELS

def create_buttons(panel):
    # Load icons for buttons
    stop_icon = wx.Bitmap("icons/stop.png", wx.BITMAP_TYPE_PNG)
    browse_icon = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG)
    play_icon = wx.Bitmap("icons/play.png", wx.BITMAP_TYPE_PNG)
    pause_icon = wx.Bitmap("icons/pause.png", wx.BITMAP_TYPE_PNG)
    resume_icon = wx.Bitmap("icons/resume.png", wx.BITMAP_TYPE_PNG)
    volume_up_icon = wx.Bitmap("icons/volume_up.png", wx.BITMAP_TYPE_PNG)
    volume_down_icon = wx.Bitmap("icons/volume_down.png", wx.BITMAP_TYPE_PNG)
    seek_forward_icon = wx.Bitmap("icons/seek_forward.png", wx.BITMAP_TYPE_PNG)
    seek_backward_icon = wx.Bitmap("icons/seek_backward.png", wx.BITMAP_TYPE_PNG)
    prev_track_icon = wx.Bitmap("icons/prev_track.png", wx.BITMAP_TYPE_PNG)
    next_track_icon = wx.Bitmap("icons/next_track.png", wx.BITMAP_TYPE_PNG)
    mute_icon = wx.Bitmap("icons/mute.png", wx.BITMAP_TYPE_PNG)

    buttons = {
        "play_button": wx.BitmapButton(panel, bitmap=play_icon),
        "pause_button": wx.BitmapButton(panel, bitmap=pause_icon),
        "resume_button": wx.BitmapButton(panel, bitmap=resume_icon),
        "stop_button": wx.BitmapButton(panel, bitmap=stop_icon),
        "volume_up_button": wx.BitmapButton(panel, bitmap=volume_up_icon),
        "volume_down_button": wx.BitmapButton(panel, bitmap=volume_down_icon),
        "seek_forward_button": wx.BitmapButton(panel, bitmap=seek_forward_icon),
        "seek_backward_button": wx.BitmapButton(panel, bitmap=seek_backward_icon),
        "prev_track_button": wx.BitmapButton(panel, bitmap=prev_track_icon),
        "next_track_button": wx.BitmapButton(panel, bitmap=next_track_icon),
        "mute_button": wx.BitmapButton(panel, bitmap=mute_icon),
        "browse_button": wx.BitmapButton(panel, bitmap=browse_icon)
    }

    # Set labels for buttons with shortcut keys
    for button_name, label in BUTTON_LABELS.items():
        buttons[button_name].SetLabel(label)

    return buttons
