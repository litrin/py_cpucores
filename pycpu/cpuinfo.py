#
# BSD 3-Clause License
#
# Copyright (c) 2018, Litrin Jiang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import abc
import os

import sys


class BaseCPUInfo:
    __metaclass__ = abc.ABCMeta

    nodes = None
    sockets = None
    cores = None
    freq = 0
    freq_range = (0, 0)
    features = []

    cpu_info_command = None

    def __init__(self, filename=None):
        if filename is not None:
            with open(filename, "r") as fd:
                data = fd.readlines()
        else:
            output = os.popen(self.cpu_info_command, "r")
            data = output.readlines()

        self.cpu_description = self.read_data(data)

    def read_data(self, data):
        return data

    def has_feature(self, name):
        return name.lower() in self.features


class CPUInfoMac(BaseCPUInfo):
    cpu_info_command = "sysctl hw"

    def read_data(self, data):
        tmp_value = {"feature": []}

        for line in data:
            line = line[:-1].split(":")
            key = line[0][3:]
            value = line[1]

            if key.startswith("optional"):
                if int(value) is 1:
                    tmp_value["feature"].append(key[9:])
            else:
                tmp_value[key] = value

        return tmp_value

    def _get_int_attr(self, value):
        return int(self.cpu_description[value])

    @property
    def sockets(self):
        return self._get_int_attr("packages")

    @property
    def nodes(self):
        return self.sockets

    @property
    def cpus(self):
        return self._get_int_attr("logicalcpu_max")

    @property
    def cores(self):
        return self._get_int_attr("physicalcpu")

    @property
    def freq(self):
        return self._get_int_attr("cpufrequency") / 10E6

    @property
    def freq_range(self):
        return self._get_int_attr(
            "cpufrequency_min") // 10E6, self._get_int_attr(
            "cpufrequency_max") // 10E6

    @property
    def features(self):
        return self.cpu_description["feature"]


class CPUInfoLinux(BaseCPUInfo):
    cpu_info_command = "LANGUAGE=en_US:en lscpu"

    def read_data(self, data):
        tmp_value = {}
        for line in data:
            line = line.split(":")
            key = line[0].lower().strip()
            value = ":".join(line[1:]).lower().strip()
            tmp_value[key] = value
        return tmp_value

    def _get_int_attr(self, value):
        return int(self.cpu_description[value])

    @property
    def nodes(self):
        return self._get_int_attr("numa node(s)")

    @property
    def sockets(self):
        return self._get_int_attr("socket(s)")

    @property
    def cores(self):
        return self.sockets * self._get_int_attr("core(s) per socket")

    @property
    def cpus(self):
        return self._get_int_attr("cpu(s)")

    @property
    def freq(self):
        return int(float(self.cpu_description["cpu mhz"]))

    @property
    def freq_range(self):
        get_int = lambda a: int(float(self.cpu_description[a]))
        return get_int("cpu min mhz"), get_int("cpu max mhz")

    @property
    def features(self):
        return self.cpu_description["flags"].split()


class CPUInfoWin32(BaseCPUInfo):

    # todo: encode issue, file input is invalid

    cpu_info_command = "wmic cpu get"

    def read_data(self, data):
        column_name, values = [], []

        t_col = data[0].lstrip()
        t_val = data[2].lstrip()

        while True:
            offset = t_col.find(" ")
            if offset is -1:
                break

            col = t_col[:offset]

            offset += len(t_col[offset:]) - len(t_col[offset:].lstrip())
            val = t_val[:offset].rstrip()

            if len(col) > 0 and len(val) > 0:
                column_name.append(col)
                values.append(val)

            t_val = t_val[offset:]
            t_col = t_col[offset:]

        # # last col must empty
        # column_name.append(t_col)
        # values.append(t_val.rstrip())

        return dict(zip(column_name, values))

    @property
    def nodes(self):
        pass

    @property
    def sockets(self):
        pass

    @property
    def cores(self):
        return int(self.cpu_description["NumberOfCores"])

    @property
    def cpus(self):
        return int(self.cpu_description["NumberOfLogicalProcessors"])

    @property
    def freq(self):
        return int(self.cpu_description["CurrentClockSpeed"])

    @property
    def freq_range(self):
        return 0, int(self.cpu_description["MaxClockSpeed"])

    @property
    def features(self):
        return []


if sys.platform == "darwin":
    CPUInfo = CPUInfoMac
elif sys.platform == "linux":
    CPUInfo = CPUInfoLinux
elif sys.platform == "win32":
    CPUInfo = CPUInfoWin32
else:
    CPUInfo = NotImplemented
