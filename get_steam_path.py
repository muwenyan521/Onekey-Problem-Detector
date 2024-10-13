import winreg
from pathlib import Path
from .stack_error import stack_error

def get_steam_path() -> Path:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam')
        steam_path = Path(winreg.QueryValueEx(key, 'SteamPath')[0])
        return Path(steam_path)
    except Exception as e:
        return Path()

steam_path = get_steam_path()