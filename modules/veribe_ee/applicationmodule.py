# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from veriso.base.utils.utils import dynamic_import
from veriso.modules.applicationmodule_base import ApplicationModuleBase


class ApplicationModule(ApplicationModuleBase):
    """
    This is the minimum required implementation to have your own module
    """

    def __init__(self, veriso):
        super(ApplicationModule, self).__init__(veriso)

    def do_load_defects(self):
        # example of how to add your own defect layers or fields
        defects_module = 'veriso.modules.loaddefects_base'
        defects_module = dynamic_import(defects_module)
        d = defects_module.LoadDefectsBase(self.iface, self.module_name)

        fields = {
            'ogc_fid': {'widget': 'TextEdit'},
            'topic': {'widget': 'Enumeration',
                      'alias': 'Topic:'},
            'bezeichnung': {
                'widget': 'Enumeration',
                'alias': 'Bezeichnung:'
                },
            'bemerkung': {
                'widget': 'TextEdit',
                'alias': 'Bemekung:',
                'config': {"IsMultiline": True}
            },
            'datum': {'widget': 'Hidden'},
            'bemerkung_nfg': {
                'widget': 'TextEdit',
                'alias': 'Bemekung NFG:',
                'config': {"IsMultiline": True}
            },
            'forstorgan': {
                'widget': 'Enumeration',
                'alias': 'Forstorgan:'
            },
            'bemerkung_forst': {
                'widget': 'TextEdit',
                'alias': 'Bemekung Forst:',
                'config': {"IsMultiline": True}
            },
            'verifikation': {
                'widget': 'Enumeration',
                'alias': 'Verifikation:'
            },
            'bemerkung_verifikation': {
                'widget': 'TextEdit',
                'alias': 'Bemekung Forst:',
                'config': {"IsMultiline": True}
            },
            'erledigt': {
                'widget': 'CheckBox',
                'alias': 'Verifikation:',
                'config': {
                    'CheckedState': 't',
                    'UncheckedState': 'f'
                }
            }
        }

        d.layers['point']['fields'] = fields
        d.layers['line']['fields'] = fields
        d.layers['polygon']['fields'] = fields

        d.layers['point']['readonly'] = True
        d.layers['line']['readonly'] = True
        d.layers['polygon']['readonly'] = True

        return d.run()
