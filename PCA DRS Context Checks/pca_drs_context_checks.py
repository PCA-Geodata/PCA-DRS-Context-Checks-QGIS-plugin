# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PCA_DRS_Context_Checks
                                 A QGIS plugin
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-11-26
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Valerio Pinna (Pre-Construct Archaeology)
        email                : vpinna@pre-construct.com
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

import re
import win32clipboard
from qgis.core import *
from qgis.utils import iface
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QApplication
from qgis.PyQt.QtWidgets import QAction,QMessageBox, QToolBar, QLabel, QDockWidget
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .pca_drs_context_checks_dockwidget import PCA_DRS_Context_ChecksDockWidget
import os.path


class PCA_DRS_Context_Checks:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PCA_DRS_Context_Checks_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
            
        self.toolbar = iface.mainWindow().findChild( QToolBar, u'PCA DRS Context Checks')
        if not self.toolbar:
            self.toolbar = iface.addToolBar( u'PCA DRS Context Checks' )
            self.toolbar.setObjectName( u'PCA DRS Context Checks')
            self.toolbar.setToolTip("")       
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PCA DRS Context Checks')   
        
        # TODO: We are going to let the user set this up in a future iteration
        # self.toolbar = self.iface.addToolBar(u'PCA_DRS_Context_Checks')
        # self.toolbar.setObjectName(u'PCA_DRS_Context_Checks')

        #print "** INITIALIZING PCA_DRS_Context_Checks"

        self.pluginIsActive = False
        self.dockwidget = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PCA_DRS_Context_Checks', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/pca_drs_context_checks/icons/PCA_logo_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.dontdonothing,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/pca_drs_context_checks/icons/PCA_DRS_context_checks_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'PCA DRS Context Checks'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING PCA_DRS_Context_Checks"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None
        self.clear_lists()
        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD PCA_DRS_Context_Checks"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PCA DRS Context Checks'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING PCA_DRS_Context_Checks"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = PCA_DRS_Context_ChecksDockWidget()
                
            self.dockwidget.update_lists_pushButton.clicked.connect(self.update_button_pressed)
            self.dockwidget.clean_lists_pushButton.clicked.connect(self.clear_lists)
            

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)
            
            ##Configure dockwidget
            self.dockwidget.DRS_mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)
            self.dockwidget.DRS_mMapLayerComboBox.layerChanged.connect(self.calculate_context_number_range)
            
            self.dockwidget.progressBar.setVisible(False)
            self.dockwidget.progressBar.setValue(0)
            
            self.dockwidget.update_lists_pushButton.setEnabled(False)
            
            # show the dockwidget
            #self.iface.addDockWidget(Qt.AllDockWidgetAreas, self.dockwidget)
            self.iface.addTabifiedDockWidget(Qt.RightDockWidgetArea, self.dockwidget, raiseTab=True)           
            
            self.dockwidget.show()
            iface.mainWindow().showFullScreen()
            iface.mainWindow().showMaximized()
            #iface.mainWindow().showMaximized()
            self.calculate_context_number_range()
   
        
    def update_button_pressed(self):
        print ('pressed button')
        print (self.dockwidget.DRS_mMapLayerComboBox.currentLayer()  )
        self.update_duplicated_list()
        self.update_missing_context_list()
        self.cuts_not_in_plan()
        self.update_wrong_parent_numbers()
        
    def natural_sort(self, l): 
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)

        
    def calculate_context_number_range(self):
        layer =  self.dockwidget.DRS_mMapLayerComboBox.currentLayer()             
        self.dockwidget.update_lists_pushButton.setEnabled(False)
        self.dockwidget.first_context_spinBox.setValue(0)
        self.dockwidget.last_context_spinBox.setValue(0)
        self.dockwidget.first_context_spinBox.setEnabled(False)
        self.dockwidget.last_context_spinBox.setEnabled(False)
        if layer is None:
            print ('error')
        else: 
            
            layer = self.dockwidget.DRS_mMapLayerComboBox.currentLayer()
            context_list = []
            
            if 'Context' in [f.name() for f in layer.fields()]:
                self.dockwidget.update_lists_pushButton.setEnabled(True)
                for f in layer.getFeatures():           
                    
                    context_value = f['Context']
                    if context_value == NULL:
                        context_to_add = 'EMPTY'
                    if context_value != NULL:
                        context_to_add = int(context_value)
                    
                    context_list.append(context_to_add)
                    
                if 'EMPTY' in context_list:
                    QMessageBox.warning(None,'PCA DRS Checks', 'The selected DRS context table contains one o more empty Context Number values (e.g., NULL). Please fix this errors before using the tool.') 
                    
                    e = ''' 
                    "Context" is NULL
                    '''
                    layer.selectByExpression(e)
                    
                    
                if 'EMPTY' not in context_list:
                    if len(context_list) != 0:
                        min_context = int(min(context_list))
                        max_context = int(max(context_list))

                        self.dockwidget.first_context_spinBox.setValue(min_context)
                        self.dockwidget.last_context_spinBox.setValue(max_context)
                        self.dockwidget.first_context_spinBox.setEnabled(True)
                        self.dockwidget.last_context_spinBox.setEnabled(True)
            
    def update_duplicated_list(self):
        
        self.dockwidget.progressBar.setVisible(True)
        self.clear_lists()
        
        min_context_no = self.dockwidget.first_context_spinBox.value()
        max_context_no = self.dockwidget.last_context_spinBox.value()
        layer = self.dockwidget.DRS_mMapLayerComboBox.currentLayer()

        numbers = []
        duplicated_list = []
        
        for u in range(min_context_no, (max_context_no+1)):
            numbers.append(u)
            
        context_list = []
        for f in layer.getFeatures():
            context_list.append(int(f['Context']))
        
        range_filtered_context_list = []
        for n in context_list:
            if n in numbers:
                range_filtered_context_list.append(n)
                
        seen = set()
        dupes = [x for x in range_filtered_context_list if x in seen or seen.add(x)] 

        duplicated_list =  (set(dupes))
        
        duplicated_list_as_string = ', ' .join(str(e) for e in duplicated_list)
        
        self.dockwidget.duplicated_plainTextEdit.setPlainText(duplicated_list_as_string)
        self.dockwidget.progressBar.setValue(5)
        
    
    def update_missing_context_list(self):
        min_context_no = self.dockwidget.first_context_spinBox.value()
        max_context_no = self.dockwidget.last_context_spinBox.value()
        numbers = []
        
        for u in range(min_context_no, (max_context_no+1)):
            numbers.append(u)

        layer = self.dockwidget.DRS_mMapLayerComboBox.currentLayer()

        context_list = []
        for f in layer.getFeatures():
            context_list.append(int(f['Context']))

        missing_list = []
        for c in numbers:
            if c not in context_list:
                missing_list.append(c)
                
        #print ('missing are: ', missing_list)
        missing_list_as_string = ', ' .join(str(e) for e in missing_list)
        
        self.dockwidget.missing_context_plainTextEdit.setPlainText(missing_list_as_string)
        self.dockwidget.progressBar.setValue(10)
        
    def update_wrong_parent_numbers(self):  
        min_context_no = self.dockwidget.first_context_spinBox.value()
        max_context_no = self.dockwidget.last_context_spinBox.value()
        layer = self.dockwidget.DRS_mMapLayerComboBox.currentLayer()
        numbers = []
        wrong_cuts_list = []
        dict = {}
        
        for u in range(min_context_no, (max_context_no+1)):
            numbers.append(u)

        for f in layer.getFeatures():
            if int(f['Context']) in numbers:
                key = f['Context']
                dict.setdefault(key, []).append(f['Type'])

        #cuts check
        for n in layer.getFeatures():
                if int(n['Context']) in numbers:
                    try:
                        dict[n['Cut']]
                    except (KeyError):
                        print('error')
                    else:
                        if dict[n['Cut']] != ['Cut']:
                            if dict[n['Cut']] != ['VOID']:
                                if dict[n['Cut']] != ['Layer']:
                                    string = '{} is a {}'.format(n['Cut'], ''.join(dict[n['Cut']]))
                                    wrong_cuts_list.append(string)
        wrong_cuts_list.append('\n\n')
        
        #layer checks
        for n in layer.getFeatures():
            
                if n['Type'] == 'Layer':
                    if int(n['Context']) in numbers:
                        if n['Context'] != n['Cut']:
                            string = 'Layer {} has a wrong "Cut/parent" number'.format(n['Context'])
                            wrong_cuts_list.append(string)        

        wrong_cuts_list_string = ', '.join(wrong_cuts_list)



        
        self.dockwidget.wrong_parent_numbers_plainTextEdit.setPlainText(wrong_cuts_list_string)
        self.dockwidget.progressBar.setValue(20)

    
    def cuts_not_in_plan(self):
        try:
            interventions = QgsProject.instance().mapLayersByName('Interventions')[0]
        except:
            QMessageBox.about(None,'PCA DRS Checks', '''The project doesn't contain any valid Interventions layer.\n\nIt was not possible to calculate the Cut numbers not in plan.''')
            self.dockwidget.progressBar.setVisible(False)
        else:
            layer = self.dockwidget.DRS_mMapLayerComboBox.currentLayer()
            min_context_no = self.dockwidget.first_context_spinBox.value()
            max_context_no = self.dockwidget.last_context_spinBox.value()
            
            numbers = []
            not_in_plan_range_list = []

            
        
            for u in range(min_context_no, (max_context_no+1)):
                numbers.append(u)
            
            e = ''' 
            Cut = 
            array_to_string(
            aggregate( 
            layer:='Interventions',
            aggregate:='array_agg',
            expression:="context_no",
            filter:=  "context_no" = attribute(@parent,'Cut')
            )
            ) = 1
            '''
            layer.selectByExpression(e)
            layer.invertSelection()
            
            not_in_plan_all_list = []
            for f in layer.selectedFeatures():
                if 'Type' in [f.name() for f in layer.fields()]:
                    if f['Type'] != None:
                        if f['Type'].casefold() != 'void':
                            not_in_plan_all_list.append(int(f['Context']))
                
            self.dockwidget.progressBar.setValue(50)  
            
            
            not_in_plan_range_list = []
            for n in not_in_plan_all_list:
                if n in numbers:
                    not_in_plan_range_list.append(n)
                    
            self.dockwidget.progressBar.setValue(80)
            
            not_in_plan_range_list_as_string = ', ' .join(str(e) for e in not_in_plan_range_list)
            
            self.dockwidget.not_on_map_plainTextEdit.setPlainText(not_in_plan_range_list_as_string)
            self.dockwidget.progressBar.setValue(100)
            self.dockwidget.progressBar.setVisible(False)
        
    def clear_lists(self):
        self.dockwidget.missing_context_plainTextEdit.setPlainText('')
        self.dockwidget.duplicated_plainTextEdit.setPlainText('')
        self.dockwidget.not_on_map_plainTextEdit.setPlainText('')
        self.dockwidget.wrong_parent_numbers_plainTextEdit.setPlainText('')
  
    def dontdonothing(self):
                pass
                
                
                
                
                
