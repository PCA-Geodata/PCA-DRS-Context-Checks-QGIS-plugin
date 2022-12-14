# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PCA_DRS_Context_Checks
                                 A QGIS plugin
 This...
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-11-26
        copyright            : (C) 2022 by Valerio Pinna (Pre-Construct Archaeology)
        email                : vpinna@pre-construct.com
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
    """Load PCA_DRS_Context_Checks class from file PCA_DRS_Context_Checks.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .pca_drs_context_checks import PCA_DRS_Context_Checks
    return PCA_DRS_Context_Checks(iface)
