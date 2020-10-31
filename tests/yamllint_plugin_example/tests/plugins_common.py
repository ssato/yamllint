# -*- coding: utf-8 -*-
# Copyright (C) 2020 Satoru SATOH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

try:
    from unittest import mock
except ImportError:  # for Python 2.7
    mock = False

import yamllint.rules

try:
    from ...common import RuleTestCase
except ImportError:
    from .common import RuleTestCase

try:
    from ..rules import RULES
except (ImportError, ValueError):
    from rules import RULES


class PluginTestCase(RuleTestCase):
    def check(self, source, conf, **kwargs):
        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, RULES):
            super(PluginTestCase, self).check(source, conf, **kwargs)
