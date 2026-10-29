# Copyright (c) 2021 by xfangfang. All Rights Reserved.

import os
import sys
import shutil
import gettext
import logging
from logging.handlers import RotatingFileHandler
from macast import Setting, SETTING_DIR
from macast.macast import gui

logger = logging.getLogger("Macast")
logger.setLevel(logging.DEBUG)


def configure_latency_log():
    os.makedirs(SETTING_DIR, exist_ok=True)
    latency_logger = logging.getLogger('MacastLatency')
    latency_logger.setLevel(logging.INFO)
    latency_logger.propagate = False
    handler = RotatingFileHandler(os.path.join(SETTING_DIR, 'latency.log'),
                                  maxBytes=1024 * 1024, backupCount=2,
                                  encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    latency_logger.addHandler(handler)


def get_base_path(path="."):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, path)


def set_mpv_default_path():
    mpv_path = 'mpv'
    if sys.platform == 'darwin':
        mpv_path = get_base_path('bin/MacOS/mpv')
        if not os.path.isfile(mpv_path):
            # Finder does not inherit the Homebrew paths from the user's shell.
            mpv_path = shutil.which('mpv') or next(
                (p for p in ('/opt/homebrew/bin/mpv', '/usr/local/bin/mpv') if os.path.isfile(p)),
                'mpv')
    elif sys.platform == 'win32':
        mpv_path = get_base_path('bin/mpv.exe')
    Setting.mpv_default_path = mpv_path
    return mpv_path


def get_lang():
    gettext.NullTranslations().install()
    logger.info('Macast interface language: English')


def clear_env():
    # todo clear pyinstaller file on start
    log_path = os.path.join(SETTING_DIR, 'macast.log')
    try:
        os.remove(log_path)
    except:
        pass


if __name__ == '__main__':
    configure_latency_log()
    clear_env()
    get_lang()
    set_mpv_default_path()
    gui(lang=_)
