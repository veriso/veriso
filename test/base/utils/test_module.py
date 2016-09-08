# coding=utf-8
import json
from unittest import TestCase

from veriso.base.utils.module import (get_baselayers, get_checks_from_files,
                                      get_check_topics, get_layers_from_topic)
from veriso.test.utilities import get_data_content


class TestUtils(TestCase):
    def test_get_baselayers(self):
        expected = get_data_content('base_layers_vd.txt')
        self.assertIsNotNone(expected)

        returned = get_baselayers('veriso_v_d')

        self.assertEqual(str(expected), str(returned))

    def test_get_checks_from_files(self):
        expected = [
            {
                u'file': u'alle_checks',
                u'id': u'alle_checks',
                u'shortcut': u'',
                u'name': {
                    u'fr': u'Touts les Checks',
                    u'de': u'Alle Checks'
                }
            },
            {
                u'file': u'alle_checks_separator',
                u'id': u'alle_checks_separator',
                u'shortcut': u'',
                u'name': u'separator'
            },
            {
                u'file': u'basislayer',
                u'id': u'basislayer',
                u'shortcut': u'',
                u'name': {
                    u'fr': u'Couche de base',
                    u'de': u'Basislayer'
                }
            },
            {
                u'file': u'checklayer',
                u'id': u'checklayer',
                u'shortcut': u'',
                u'name': u'Checklayer'
            },
            {
                u'file': u'lokalisation',
                u'id': u'lokalisation',
                u'shortcut': u'F12',
                u'name': {
                    u'fr': u'Localisation',
                    u'de': u'Lokalisation'
                }
            }]

        checks = get_checks_from_files('veriso_ee', 'gebaeudeadressen')
        checks_list = json.loads(json.dumps(checks))
        self.assertListEqual(checks_list, expected)

    def test_get_check_topics(self):
        expected = {
            u'FixpunkteKategorie3': {
                u'topic': u'FixpunkteKategorie3', u'topic_dir': u'fp3',
                u'checks': [{
                    u'file': u'fp3', u'id': u'fp3',
                    u'shortcut': u'', u'name': {
                        u'fr': u"Vue d'ensemble", u'de': u'\xdcbersicht'
                    }
                }]
            }, u'Gebaeudeadressen': {
                u'topic': u'Gebaeudeadressen',
                u'topic_dir': u'gebaeudeadressen', u'checks': [{
                    u'file':
                        u'alle_checks',
                    u'id':
                        u'alle_checks',
                    u'shortcut': u'',
                    u'name': {
                        u'fr': u'Touts les Checks',
                        u'de': u'Alle Checks'
                    }
                }, {
                    u'file': u'alle_checks_separator',
                    u'id': u'alle_checks_separator',
                    u'shortcut': u'',
                    u'name': u'separator'
                }, {
                    u'file': u'basislayer',
                    u'id': u'basislayer',
                    u'shortcut': u'',
                    u'name': {
                        u'fr': u'Couche de base',
                        u'de': u'Basislayer'
                    }
                }, {
                    u'file': u'checklayer',
                    u'id': u'checklayer',
                    u'shortcut': u'',
                    u'name': u'Checklayer'
                }, {
                    u'file': u'lokalisation',
                    u'id': u'lokalisation',
                    u'shortcut': u'F12',
                    u'name': {
                        u'fr': u'Localisation',
                        u'de': u'Lokalisation'
                    }
                }]
            }
        }

        topics = get_check_topics('veriso_ee')
        topics_list = json.loads(json.dumps(topics))
        self.assertDictEqual(topics_list, expected)
