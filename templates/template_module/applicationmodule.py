# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from veriso.modules.applicationmodule_base import ApplicationModuleBase


class ApplicationModule(ApplicationModuleBase):
    """
    This is the minimum required implementation to have your own module
    """
    def __init__(self, iface, toolbar, locale_path):
        super(ApplicationModule, self).__init__(iface, toolbar, locale_path)
