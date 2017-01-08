# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from veriso.base.utils.utils import dynamic_import
from veriso.modules.applicationmodule_base import ApplicationModuleBase


class ApplicationModule(ApplicationModuleBase):
    def __init__(self, iface, toolbar, locale_path):
        super(ApplicationModule, self).__init__(iface, toolbar, locale_path)

    def do_load_defects(self):
        defects_module = 'veriso.modules.loaddefects_base'
        defects_module = dynamic_import(defects_module)
        d = defects_module.LoadDefectsBase(self.iface, self.module,
                                           self.module_name)

        d.layers['point']['fields'] = {
                'ogc_fid': {'widget': 'TextEdit'},
                'topic': {
                    'widget': 'Enumeration',
                    'alias': 'Topic:'
                },
                'bemerkung': {
                    'widget': 'TextEdit',
                    'alias': 'Bemekung:',
                    'config': {"IsMultiline": True}
                },
                'datum': {'widget': 'Hidden'}
            }

        d.run()
