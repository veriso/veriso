# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VeriSO
                                 A QGIS plugin
 Verification application module for Interlis data.
                              -------------------
        begin                : 2014-07-28
        git sha              : $Format:%H$
        copyright            : (C) 2016 OPENGIS.ch
                             :     2014 by Stefan Ziegler
        email                : info@opengis.ch
                             : edi.gonzales@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


from base.utils.utils import check_compat
check_compat()


def classFactory(iface):  # pylint: disable=invalid-name
    """Load VeriSO class from file VeriSO.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from .veriso import VeriSO
    return VeriSO(iface)


