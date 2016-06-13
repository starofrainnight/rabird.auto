'''
@date 2015-02-22
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import re
import subprocess
import six
import sys
from . import common
from ..mouse.xdotool import Mouse
from ..keyboard.xdotool import Keyboard


def _check_output(*args, **kwargs):
    output = subprocess.check_output(*args, **kwargs)
    if six.PY3:
        output = output.decode(sys.getdefaultencoding())
    return output


class Window(common.Window):

    def __init__(self, handle):
        super(Window, self).__init__()

        self.__handle = int(handle)
        self._keyboard = Keyboard()

    @property
    def handle(self):
        return self.__handle

    @property
    def title(self):
        output = _check_output(
            ["xdotool", "getwindowname", str(self.__handle)])
        return output.strip('\r\n').strip()

    @property
    def geometry(self):
        output = _check_output(
            ["xdotool", "getwindowgeometry", str(self.__handle)])
        matched = re.match(
            "(?:\n|.)*"
            "Absolute upper-left X:[^\d]*(\d+)[^\d]*(?:\n|.)*"
            "Absolute upper-left Y:[^\d]*(\d+)[^\d]*(?:\n|.)*"
            "idth:[^\d]*(\d+)[^\d]*(?:\n|.)*"
            "eight:[^\d]*(\d+)[^\d]*(?:\n|.)*", output, re.M)
        if matched is None:
            # Return text different from original after upgraded to ubuntu
            # 16.04
            matched = re.match(
                "(?:\n|.)*"
                "osition:[^\d]*(\d+),(\d+)[^\d]*(?:\n|.)*"
                "eometry:[^\d]*(\d+)x(\d+)[^\d]*(?:\n|.)*", output, re.M)

        return (int(matched.group(1)),
                int(matched.group(2)),
                int(matched.group(3)),
                int(matched.group(4)))

    def raise_(self):
        subprocess.call(["xdotool", "windowraise",
                         "--sync", str(self.__handle)])

    def activate(self):
        subprocess.call(["xdotool", "windowactivate",
                         "--sync", str(self.__handle)])

    def close(self):
        subprocess.call(["xdotool", "windowkill", str(self.__handle)])

    def send(self, *args, **kwargs):
        self._keyboard.send(*args, **kwargs, window=self.handle)


class Manager(common.Manager):

    def __init__(self):
        super(Manager, self).__init__()
        self.__mouse = Mouse()

    def get_active(self):
        output = _check_output(["xdotool", "getactivewindow"])
        return Window(int(output.strip('\r\n').strip()))

    def get_from_position(self, position):
        old_position = None

        if position != self.__mouse.position():
            old_position = self.__mouse.position()
            self.__mouse.move(position)
        try:
            output = _check_output(["xdotool", "getmouselocation"])
            matched = re.match("(?:\n|.)*window:(\d+)*(?:\n|.)*", output)
            return Window(int(matched.group(1)))
        finally:
            if old_position is not None:
                self.__mouse.move(old_position)

    def find(self, **kwargs):
        self._prepare_find_arguments(kwargs)

        result = []

        command = ["xdotool", "search"]
        command.append("--all")
        # It will freeze the search behaviors
        # command.append("--sync")

        # Seems xdotool can't work if class name and title
        # at the sametime. So we search by ourself.
        command += ["--name", '']  # Search all windows

        output = _check_output(command)
        window_ids = re.findall("\d+", output, re.M)
        window_ids = [int(window_id) for window_id in window_ids]

        for window_id in window_ids:
            window = Window(window_id)

            if (("title" in kwargs) and
                    (re.match(str(kwargs["title"]), window.title) is None)):
                continue

            if (("class_name" in kwargs) and
                    (re.match(str(kwargs["class_name"]), window.class_name) is None)):
                continue

            result.append(window)

            if kwargs["limit"] > 0:
                if len(result) >= kwargs["limit"]:
                    break

        return result
