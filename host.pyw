# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script host.
"""

# embedded in python
import importlib
from functools import partial
import os
import sys
# pip install
from PyQt5 import QtCore, QtGui, QtWidgets
# same folder

class centralwidget( QtWidgets.QWidget ):
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( centralwidget, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setObjectName( 'centralwidget' )

class mainwindow( QtWidgets.QMainWindow ):
    """Serves as parent for pieces pyqt5 windows."""
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( mainwindow, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about communication with pieces.
    """
    def all_windows_are_hidden( widget ):
        print( widget )
        widget.hide()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        w = centralwidget( self )
        self.setCentralWidget( w )
        
    def _init( self ):
        self.setObjectName( 'mainwindow' )
        self.setWindowTitle( 'AAAAAAAAAA' )

class application( object ):
    
    pluginroot = 'pieces'
    pluginfile = 'main'
    
    def __init__( self,
                  *args, **kwargs ):
        super( application, self ).__init__( *args, **kwargs )
        
        # gui
        self._init()
        self._init_tray()
        
        # plugins
        self._seek_plugins()
        self._dynamically_import()
        
        # infinite mainloop
        self.app.exec_()
        #sys.exit( self.app.exec_() )
        
    """---------------------------------------------------------------------+++
    Everything about traymenu actions.
    """
    def _trayicon_activated( self, reason ):
        if reason==1: pass # right click
        elif reason==2: pass # double left click
        elif reason==3: pass # left click 
        elif reason==4: pass # middle click
            
    @staticmethod
    def _traymenu_openfolder():
        # open application folder
        os.startfile( os.getcwd() )
        
    @staticmethod
    def _traymenu_exitapp():
        QtCore.QCoreApplication.exit()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.app = QtWidgets.QApplication( sys.argv )
        self.w = mainwindow()
        #self.w.show()
        #self.w.showMinimized()
        
    def _init_tray( self ):
        # tray context menu
        m = QtWidgets.QMenu( self.w )
        m.setObjectName( 'traymenu' )
        m_op = m.addAction( 'Open folder' )
        m_op.triggered.connect( self._traymenu_openfolder )
        m_ex = m.addAction( 'Exit' )
        m_ex.triggered.connect( self._traymenu_exitapp )
        
        # tray icon
        iconpath = 'tray.png'
        icon = QtWidgets.QSystemTrayIcon( QtGui.QIcon(iconpath), self.w )
        icon.setContextMenu( m )
        icon.activated.connect( self._trayicon_activated )
        icon.show()
        
        """
        icon.showMessage( "dust", "eeeeee",
            QtWidgets.QSystemTrayIcon.Information,
            2000 )
        """
        
    """---------------------------------------------------------------------+++
    Everything about plugins.
    """
    def _seek_plugins( self ):
        self.plugins = {}
        for foldername in os.listdir( self.pluginroot ):
            dest = os.path.join( self.pluginroot,foldername,self.pluginfile )
            
            row = {
                'path': dest,
                'module': None,
                'load': os.path.exists(
                    os.path.join( self.pluginroot,foldername,'load' ) ),
                }
            self.plugins.setdefault( foldername, row )
            
    def _dynamically_import( self ):
        """-----------------------------------------------------------------+++
        Definitions.
        """
        MENU = self.w.findChild( QtWidgets.QMenu,'traymenu' )
        def inject_intotraymenu():
            """Injects items into tray menu depending on the info within
            plugin's inject_intotraymenu method.
            """
            # skip if there is no such method at all
            try: getattr( module, 'inject_intotraymenu' )
            except AttributeError: return None
            
            for action in module.inject_intotraymenu():
                a=MENU.addAction( action['text'] )
                
                if 'connect' in action:
                    f = partial( action['connect'], parent=self.w )
                    a.triggered.connect( f )
                if 'icon' in action:
                    iconpath = os.path.join( self.pluginroot, foldername,
                        action['icon'] )
                    a.setIcon( QtGui.QIcon(iconpath) )
                    
        """-----------------------------------------------------------------+++
        Actual code.
        """
        for foldername, plugindata in self.plugins.items():
            if not plugindata['load']: continue
        
            # import the module
            modulename = plugindata['path'].replace('\\','.')
            module = importlib.import_module( modulename )
            self.plugins[foldername]['module'] = module
            
            inject_intotraymenu()
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    ob = application()

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2021.02.03 → 2021.02.03
