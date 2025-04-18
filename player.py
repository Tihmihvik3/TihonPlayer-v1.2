import pygame
import time
import threading
import math
import wx  # Add this import


class AudioPlayer:
    def __init__(self, tab):
        self.is_thread_running = None
        self.tab = tab
        pygame.mixer.init()
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.pause_time = 0
        self.volume = 0.5  # Initial volume level (from 0.0 to 1.0)
        self.is_muted = False
        self.previous_volume = self.volume
        pygame.mixer.music.set_volume(self.volume)
        self.on_end_callback = None
        self.track_length = 0

    def set_on_end_callback(self, callback):
        self.on_end_callback = callback

    def play(self, filepath, on_end_callback=None):
        if self.is_playing:
            self.stop(attenuation=True)
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        self.track_length = pygame.mixer.Sound(filepath).get_length()
        if on_end_callback:
            self.set_on_end_callback(on_end_callback)
        self.is_playing = True
        self.is_paused = False
        self.start_time = time.time()

        # Проверяем, запущен ли поток
        if not hasattr(self, 'is_thread_running') or not self.is_thread_running:
            self.is_thread_running = True
            threading.Thread(target=self.update_playback_duration, daemon=True).start()

    def update_playback_duration(self):

        print("Метод  - дурейшан запущен")
        while self.is_playing:
            current_time = time.time() - self.start_time
            current_time = math.floor(current_time * 10) / 10
            track_time = math.floor(self.track_length * 10) / 10
            print(track_time, current_time)
            if current_time + 3 >= track_time:
                self.tab.on_next_track(None)
            time.sleep(0.5)
        self.is_thread_running = False  # Сбрасываем флаг после завершения

    def on_track_end(self):
        app = wx.GetApp()
        if app:
            frame = app.GetTopWindow()
            if frame:
                notebook = frame.notebook
                active_tab = notebook.GetCurrentPage()
                if hasattr(active_tab, 'on_next_track'):
                    active_tab.on_next_track(None)

    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.pause_time = time.time()
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.start_time += time.time() - self.pause_time

    def stop(self, attenuation=False):
        if self.is_playing:
            if attenuation:
                pygame.mixer.music.fadeout(2000)  # Fade out over 2 seconds
                time.sleep(2)  # Wait for the fadeout to complete
            pygame.mixer.music.stop()  # Stop the music
            self.is_playing = False
            self.is_paused = False
            if self.on_end_callback:
                self.on_end_callback()

    def stop_transition(self    ):
        if self.is_playing:
            pygame.mixer.music.stop()
            # self.is_playing = False
            # self.is_paused = False

    def seek(self, seconds):
        if self.is_playing:
            current_pos = time.time() - self.start_time
            new_pos = current_pos + seconds
            if new_pos < 0:
                new_pos = 0
            self.stop_transition()
            pygame.mixer.music.play(start=new_pos)
            self.is_playing = True
            self.is_paused = False
            self.start_time = time.time() - new_pos

    def get_current_time(self):
        if self.is_playing:
            current_pos = time.time() - self.start_time
            minutes = int(current_pos // 60)
            seconds = int(current_pos % 60)
            milliseconds = int((current_pos * 1000) % 1000)
            return f"{minutes}:{seconds}.{milliseconds}"
        return "0:0.0"

    def volume_up(self):
        self.volume = min(self.volume + 0.1, 1.0)  # Increase volume by 0.1, maximum 1.0
        pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        self.volume = max(self.volume - 0.1, 0.0)  # Decrease volume by 0.1, minimum 0.0
        pygame.mixer.music.set_volume(self.volume)

    def mute(self):
        if self.is_muted:
            self.volume = self.previous_volume
            self.is_muted = False
        else:
            self.previous_volume = self.volume
            self.volume = 0.0
            self.is_muted = True
        pygame.mixer.music.set_volume(self.volume)

    def on_play_sample(self, filepath_sample):
        if self.is_playing:
            self.stop()
        pygame.mixer.music.load(filepath_sample)
        pygame.mixer.music.play(loops=-1)  # Loop the sample playback indefinitely
        self.is_playing = True
        self.is_paused = False
        self.start_time = time.time()

