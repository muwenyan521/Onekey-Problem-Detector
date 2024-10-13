import os
import platform
import hashlib
import json
import requests
from pathlib import Path
from .log import log
from .get_steam_path import get_steam_path

def check_windows_version():
    version = platform.version()
    major_version = int(version.split('.')[0])
    if platform.system() == "Windows" and major_version >= 10:
        log.info("🌐 系统版本检查通过！你的系统是Windows 10或更高版本.")
        return True
    else:
        log.error("⚠️ Onekey仅支持Windows 10及以上版本,请检查你的系统版本.")
        return False

def check_onekey_file_exists():
    for file in os.listdir('.'):
        if 'onekey' in file.lower() and file.endswith('.exe'):
            log.info(f"📂 找到Onekey文件:{file}")
            return file
    log.error("🚫 当前目录下没有找到Onekey文件.")
    return None

def check_config_file_exists():
    if os.path.exists('config.json'):
        log.info("📝 配置文件config.json存在.")
        return True
    else:
        log.error("⚠️ 配置文件config.json不存在.")
        return False

def get_md5_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        log.info("🔗 成功从URL获取MD5值.")
        return response.text.strip()
    else:
        log.error(f"❌ 无法从URL获取MD5值,返回状态码: {response.status_code}")
        return None

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def validate_config(config):
    required_keys = ["Github_Personal_Token", "Custom_Steam_Path", "QA1", "教程"]
    for key in required_keys:
        if key not in config:
            log.error(f"⚠️ 配置文件config.json缺少键: {key}")
            return False

    if not isinstance(config["Custom_Steam_Path"], str):
        log.error("⚠️ 自定义Steam路径不是有效字符串.")
        return False

    log.info("🗂 配置文件格式验证通过.")
    return True

def check_steam_path(steam_path):
    if os.path.exists(steam_path):
        log.info(f"📍 Steam路径验证通过:{steam_path}")
        return True
    else:
        log.error(f"⚠️ Steam路径无效:{steam_path}")
        return False

def main():
    input("🚀 请先在https://github.com/ikunshare/Onekey/releases下载最新版Onekey并启动一次后再测试,按任意键继续...\n")
    
    if not check_windows_version():
        return

    onekey_file = check_onekey_file_exists()
    if not onekey_file:
        return

    config_exists = check_config_file_exists()
    if config_exists:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            if not validate_config(config):
                return
            
            if config["Custom_Steam_Path"] == "":
                steam_path = get_steam_path()
                if not steam_path.exists():
                    log.error("🚫 获取的Steam路径无效,请检查安装情况.")
                    return
            else:
                steam_path = Path(config["Custom_Steam_Path"])

            if not check_steam_path(steam_path):
                return

            if not os.path.exists(os.path.join(steam_path, 'config', 'stplug-in')):
                log.error("🚫 不存在SteamTools插件,请检查安装情况.")
                return

    onekey_md5 = get_md5_from_url("https://raw.gitmirror.com/muwenyan521/Onekey-Problem-Detector/refs/heads/main/md5.md5")
    if onekey_md5:
        if calculate_md5(onekey_file) == onekey_md5:
            log.info("🎉 Onekey文件校验通过.")
        else:
            log.error("❌ Onekey文件校验失败,请检查下载是否完整.")

if __name__ == "__main__":
    main()