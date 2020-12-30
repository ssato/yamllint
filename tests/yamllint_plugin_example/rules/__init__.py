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

"""yamllint plugin entry point
"""
from __future__ import absolute_import

from . import (
    forbid_comments, no_forty_two, random_failure
)


RULES = (
    (forbid_comments.ID, forbid_comments),
    (no_forty_two.ID, no_forty_two),
    (random_failure.ID, random_failure)
)
