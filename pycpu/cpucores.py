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

import re


class CoreList(set):

    def __init__(self, core_list):
        if isinstance(core_list, int):
            self._format_core_mask(core_list)
        elif core_list.find(",") != -1 or core_list.find("-") != -1:
            self._format_string_core_list(core_list)
        elif re.match(r"^\d+$", core_list):
            self.add(int(core_list))
        else:
            raise TypeError(
                "%s is not a correct core list format!" % core_list)

    def _format_core_mask(self, core_list):
        i = 0
        while core_list > (1 << i):
            if 1 << i & core_list:
                self.add(i)
            i += 1

    def _format_string_core_list(self, core_list):
        core_list = core_list.split(",")
        for element in core_list:
            if element.find("-") != -1:
                self._format_core_range(element)
            else:
                self.add(int(element))

    def _format_core_range(self, core_range):
        core_start, core_end = tuple([int(i) for i in core_range.split("-")])
        if core_end < core_start:
            core_end, core_start = core_start, core_end

        for i in range(core_start, core_end + 1):
            self.add(i)

    @property
    def core_mask(self):
        mask = 0
        for i in self:
            mask += 1 << i

        return mask

    @property
    def core_list(self):
        return ",".join([str(i) for i in sorted(self)])

    @property
    def core_range(self):

        def fmt(s, e):
            if s is e:
                return str(s)
            return "%s-%s" % (s, e)

        all_cores = sorted(self)
        core_list = []
        core_start, core_end = all_cores[0], 0
        step = 0
        for curr in all_cores:
            if curr is (core_start + step):
                step += 1
            else:
                core_list.append(fmt(core_start, core_end))

                step = 1
                core_start = curr

            core_end = curr

        core_list.append(fmt(core_start, core_end))

        return ",".join(core_list)

    def __str__(self):
        return self.core_range
