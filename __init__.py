# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VeriSO
                                 A QGIS plugin
 Verification application module for Interlis data.
                             -------------------
        begin                : 2014-07-28
        copyright            : (C) 2014 by Stefan Ziegler
        email                : edi.gonzales@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load VeriSO class from file VeriSO.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .veriso import VeriSO
    return VeriSO(iface)
