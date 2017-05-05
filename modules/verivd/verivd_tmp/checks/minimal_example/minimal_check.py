# coding=utf-8
from __future__ import print_function
from collections import OrderedDict

from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    shortcut = 'F11'
    names = OrderedDict()
    names['de'] = u'mein Übername'
    names['fr'] = 'mon nom'

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)

    def run(self):
        print ("I'm a minimal working ComplexCheck")
