#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import platform


class SystemUtils:
    """"工具类"""

    @staticmethod
    def get_sys_absolute_path():
        """获取档期系统的绝对路径"""
        return os.path.abspath('.') + "/"

    @staticmethod
    def get_file_absolute(path):
        """获取文件的绝对路径"""
        return os.path.abspath('.') + "/" + path

    @staticmethod
    def is_windows():
        """是否是window"""
        return True if 'Windows' in platform.system() else False
