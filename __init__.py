# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsOpenScope
                                 A QGIS plugin
 A collection of tools for the openScope project

 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-09-13
        copyright            : (C) 2019 by openScope
        email                : 3430117+oobayly@users.noreply.github.com

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
    """Load QgsOpenScope class from file QgsOpenScope.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .QgsOpenScope import QgsOpenScope
    return QgsOpenScope(iface)
