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
            'ogc_fid': {'widget': 'TextEdit',
                        'readonly': True,
                        'config': {"Editable": False}},
            'topic': {'widget': 'Enumeration',
                      'alias': 'Topic:'},
            'bezeichnung': {
                'widget': 'Enumeration',
                'alias': 'Bezeichnung:',
                'writable_only_by': ['geometerbuero']
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
                'config': {"IsMultiline": True},
                'writable_only_by': ['geometerbuero']
            },
            'forstorgan': {
                'widget': 'Enumeration',
                'alias': 'Forstorgan:',
                'writable_only_by': ['forst']
            },
            'bemerkung_forst': {
                'widget': 'TextEdit',
                'alias': 'Bemekung Forst:',
                'config': {"IsMultiline": True},
                'writable_only_by': ['forst']
            },
            'verifikation': {
                'widget': 'Enumeration',
                'alias': 'Verifikation:',
                'writable_only_by': ['verifikation']
            },
            'bemerkung_verifikation': {
                'widget': 'TextEdit',
                'alias': 'Bemekung Verifikation:',
                'config': {"IsMultiline": True},
                'writable_only_by': ['verifikation']
            },
            'erledigt': {
                'widget': 'CheckBox',
                'alias': 'Erledigt:',
                'config': {
                    'CheckedState': 't',
                    'UncheckedState': 'f'
                },
                'writable_only_by': ['geometerbuero']
            }
        }

        d.layers['point']['fields'] = fields
        d.layers['line']['fields'] = fields
        d.layers['polygon']['fields'] = fields

        d.layers['point']['readonly'] = True
        d.layers['line']['readonly'] = True
        d.layers['polygon']['readonly'] = True

        return d.run()
