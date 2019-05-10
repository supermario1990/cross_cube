#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gettext
import os
from utils import dir_path

GLOBAL_LANG = "zh_CN"
GLOBAL_LANG_PATH = "/locale"
GLOBAL_LANG_FILE = "lang"


def get_lang_folder_path():
    locale_path = os.path.abspath(os.path.dirname(__file__) + "/../")
    return locale_path


def install_i18n_lang(lang_path):
    try:
        global GLOBAL_LANG_PATH
        global GLOBAL_LANG_FILE
        locale_path = get_lang_folder_path() + GLOBAL_LANG_PATH
        lang_file_name = GLOBAL_LANG_FILE
        gettext.install(lang_file_name, locale_path)
        gettext.translation(lang_file_name,
                            locale_path,
                            languages=[lang_path]).install(True)
    except Exception as exception:
        print("Load lang path {} failed with {}".format(lang_path, exception))


def load_call_back(path, file):
    file_path = os.path.join(path, file)
    if os.path.isdir(file_path):
        install_i18n_lang(file)


def load_all_lang():
    global GLOBAL_LANG_PATH
    dir_path(get_lang_folder_path() + GLOBAL_LANG_PATH, load_call_back)


def get_current_lang(lang=GLOBAL_LANG):
    global GLOBAL_LANG_PATH
    global GLOBAL_LANG_FILE
    global GLOBAL_LANG
    lang_translation = gettext.translation(GLOBAL_LANG_FILE,
                                           get_lang_folder_path() + GLOBAL_LANG_PATH,
                                           languages=[GLOBAL_LANG])
    return lang_translation.gettext


# 引用模块自动加载所有语言和生成全局语言对象
load_all_lang()
L = get_current_lang()
