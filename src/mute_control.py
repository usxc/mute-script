from ctypes import windll
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def mute():
    """スピーカーをミュートにする"""
    windll.ole32.CoInitialize(None)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMute(True, None)  # ミュートにする

def unmute():
    """スピーカーのミュートを解除する"""
    windll.ole32.CoInitialize(None)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMute(False, None)  # ミュート解除
