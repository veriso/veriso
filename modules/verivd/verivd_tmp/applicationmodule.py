# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from veriso.modules.applicationmodule_base import ApplicationModuleBase


class ApplicationModule(ApplicationModuleBase):
    """
    This is the minimum required implementation to have your own module
    """
    def __init__(self, veriso):
        super(ApplicationModule, self).__init__(veriso)

"""
    def do_load_defects(self):
        # example of how to add your own defect layers or fields
        defects_module = 'veriso.modules.loaddefects_base'
        defects_module = dynamic_import(defects_module)
        d = defects_module.LoadDefectsBase(self.iface, self.module_name)

        d.layers['point']['fields'] = {
            'ogc_fid': {'widget': 'TextEdit'},
            'topic': {
                'widget': 'Enumeration',
                'alias': 'Topic:',
                'default': 'my default value'
            },
            'bemerkung': {
                'widget': 'TextEdit',
                'alias': 'Bemekung:',
                'config': {"IsMultiline": True},
                'writable_only_by': ['PG_role_1', 'PG_role_3']
            },
            'datum': {'widget': 'Hidden'}
        }

        return d.run()
"""