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

import unittest
import warnings

try:
    from unittest import mock
except ImportError:  # for Python 2.7
    mock = False

from tests.common import RuleTestCase
from tests.test_spec_examples import (
    conf_general, conf_overrides, gen_spec_test_cases
)
from tests.yamllint_plugin_example import rules as example

import yamllint.plugins
import yamllint.rules


PLUGIN_RULES = dict(example.RULES)


class FakeEntryPoint(object):
    """Fake object to mimic pkg_resources.EntryPoint.
    """
    RULES = example.RULES

    def load(self):
        """Fake method to return self.
        """
        return self


class BrokenEntryPoint(FakeEntryPoint):
    """Fake object to mimic load failure of pkg_resources.EntryPoint.
    """
    def load(self):
        raise ImportError("This entry point should fail always!")


class PluginFunctionsTestCase(unittest.TestCase):
    def test_validate_rule_module(self):
        fun = yamllint.plugins.validate_rule_module
        rule_mod = example.forbid_comments

        self.assertFalse(fun(object()))
        self.assertTrue(fun(rule_mod))

    @unittest.skipIf(not mock, "unittest.mock is not available")
    def test_validate_rule_module_using_mock(self):
        fun = yamllint.plugins.validate_rule_module
        rule_mod = example.forbid_comments

        with mock.patch.object(rule_mod, "ID", False):
            self.assertFalse(fun(rule_mod))

        with mock.patch.object(rule_mod, "TYPE", False):
            self.assertFalse(fun(rule_mod))

        with mock.patch.object(rule_mod, "check", True):
            self.assertFalse(fun(rule_mod))

    @unittest.skipIf(not mock, "unittest.mock is not available")
    def test_load_plugin_rules_itr(self):
        fun = yamllint.plugins.load_plugin_rules_itr
        entry_points = 'pkg_resources.iter_entry_points'

        with mock.patch(entry_points) as iter_entry_points:
            iter_entry_points.return_value = []
            self.assertEqual(list(fun()), [])

            iter_entry_points.return_value = [FakeEntryPoint(),
                                              FakeEntryPoint()]
            self.assertEqual(sorted(fun()), sorted(FakeEntryPoint.RULES))

            iter_entry_points.return_value = [BrokenEntryPoint()]
            with warnings.catch_warnings(record=True) as warn:
                warnings.simplefilter("always")
                self.assertEqual(list(fun()), [])

                self.assertEqual(len(warn), 1)
                self.assertTrue(issubclass(warn[-1].category, RuntimeWarning))
                self.assertTrue("Could not load the plugin:"
                                in str(warn[-1].message))


@unittest.skipIf(not mock, "unittest.mock is not available")
class RulesTestCase(unittest.TestCase):
    def test_get_default_rule(self):
        self.assertEqual(yamllint.rules.get(yamllint.rules.braces.ID),
                         yamllint.rules.braces)

    def test_get_rule_does_not_exist(self):
        with self.assertRaises(ValueError):
            yamllint.rules.get('DOESNT_EXIST')

    def test_get_default_rule_with_plugins(self):
        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, PLUGIN_RULES):
            self.assertEqual(yamllint.rules.get(yamllint.rules.braces.ID),
                             yamllint.rules.braces)

    def test_get_plugin_rules(self):
        plugin_rule_id = example.forbid_comments.ID
        plugin_rule_mod = example.forbid_comments

        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, PLUGIN_RULES):
            self.assertEqual(yamllint.rules.get(plugin_rule_id),
                             plugin_rule_mod)

    def test_get_rule_does_not_exist_with_plugins(self):
        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, PLUGIN_RULES):
            with self.assertRaises(ValueError):
                yamllint.rules.get('DOESNT_EXIST')


@unittest.skipIf(not mock, "unittest.mock is not available")
class SpecificationTestCase(RuleTestCase):
    rule_id = None


def _gen_test(buffer, conf):
    def test(self):
        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, PLUGIN_RULES):
            self.check(buffer, conf)
    return test


def gen_plugin_spec_test_cases():
    conf_plugin_general = ('forbid-comments:\n'
                           '  forbid: false\n'
                           'random-failure: disable\n'
                           'no-forty-two: disable\n')
    gen_spec_test_cases(conf_general + conf_plugin_general, conf_overrides,
                        cls=SpecificationTestCase, _gen_test=_gen_test)


gen_plugin_spec_test_cases()
