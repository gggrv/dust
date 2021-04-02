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
        
    """---------------------------------------------------------------------+++
    Everything about communication with pieces.
    def all_windows_are_hidden( widget ):
        print( widget )
        widget.hide()
    """
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setObjectName( 'mainwindow' )

class application( object ):
    
    # about pieces
    PIECES_ROOT = 'pieces' # where to look for pieces
    PIECE_FILE = 'main' # piece entrypoint python file
    pieces = {} # empty placeholder for pieces available
    
    # about self
    MAY_TERMINATE = False # whether the app may terminate itself
    
    # debug console output control
    DEBUG = True
    
    def __init__( self,
                  *args, **kwargs ):
        super( application, self ).__init__( *args, **kwargs )
        
        # gui
        self._init()
        self._init_tray()
        
        # pieces
        self._seekpieces() # find them
        self._dynaimport() # load the ones i want to load
        
        # gui mainloop, exit app when done
        self.app.exec_()
        if self.DEBUG: print( 'exec' )
        self._traymenu_exitapp()
        
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
        
    def _traymenu_exitapp( self ):
        """What to do when app terminates."""
        
        # run uponhostdestruction methods of pieces
        for k in self.pieces:
        
            # get interaction object
            ob = self.pieces[k]['object']
            if type(ob)==type(None): continue
        
            # run the destructor
            ob.uponhostdestruction()
        
        # self-terminate
        QtCore.QCoreApplication.exit()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.app = QtWidgets.QApplication( sys.argv )
        self.w = mainwindow()
        self.w.setVisible( False )
        
    def _init_tray( self ):
        
        # tray icon
        iconpath = 'tray.png'
        icon = QtWidgets.QSystemTrayIcon( QtGui.QIcon(iconpath), self.w )
        
        # tray context menu
        m = QtWidgets.QMenu( self.w )
        m.setObjectName( 'traymenu' )
        m_op = m.addAction( 'Open folder' )
        m_op.triggered.connect( self._traymenu_openfolder )
        m_ex = m.addAction( 'Exit' )
        m_ex.triggered.connect( self._traymenu_exitapp )
        
        # assemble
        icon.setContextMenu( m )
        icon.activated.connect( self._trayicon_activated )
        
        # visibility
        icon.setVisible(True)
        icon.show()
        
        """
        # tray notification
        icon.showMessage( "dust", "eeeeee",
            QtWidgets.QSystemTrayIcon.Information,
            2000 )
        """
        
    """---------------------------------------------------------------------+++
    Everything about pieces.
    """
    def _seekpieces( self ):
        """Looks for pieces in the corr. directory, catalogues them,
        saves them to self.pieces.
        """
        self.pieces = {} # clear pieces
        for foldername in os.listdir( self.PIECES_ROOT ):
            folderpath = os.path.join( self.PIECES_ROOT,foldername )
            
            # get piece enrty point - a python file
            dest = os.path.join( folderpath,self.PIECE_FILE )
            
            row = {
                'path': dest, # path to the file↑
                'load': os.path.exists(
                    os.path.join(folderpath,'load')
                    ), # bool if i want to load this piece
                'module': None, # loaded module, currently not loaded
                'object': None, # interaction object instance, currently not existing yet
                }
            
            self.pieces.setdefault( foldername, row )
            
    def _dynaimport( self ):
        """-----------------------------------------------------------------+++
        Definitions.
        """
        
        # host tray menu that i will populate with corr. items
        MENU = self.w.findChild( QtWidgets.QMenu,'traymenu' )
        
        def interaction_object():
            """If the piece has a class named interaction_object,
            I create an instance of that class and set it's parent
            and link to the host object - this application class instance.
            """
            # deal with interaction object...
            # skip if there is no such class at all
            try: getattr( module, 'interaction_object' )
            except AttributeError: return None
            
            # get the object (i expect some sort of pyqt5 qwidget)
            ob = module.interaction_object( parent=self.w, host_app=self )
            
            # save pointer to it for forther use
            self.pieces[foldername]['object'] = ob
            
            
            # deal with injection into tray menu...
            # skip if there is no such method at all
            try: getattr( ob, 'inject_intotraymenu' )
            except AttributeError: return None
            for action in ob.inject_intotraymenu():
                a = MENU.addAction( action['text'] )
                
                if 'connect' in action:
                    #f = partial( action['connect'], interaction_object=self.pieces[foldername]['object'] )
                    #a.triggered.connect( f )
                    a.triggered.connect( action['connect'] )
                    
                if 'icon' in action:
                    iconpath = os.path.join( self.PIECES_ROOT, foldername,
                        action['icon'] )
                    a.setIcon( QtGui.QIcon(iconpath) )
                    
        """-----------------------------------------------------------------+++
        Actual code.
        """
        for foldername, piece in self.pieces.items():
            # skip the ones i don't want to load
            if not piece['load']: continue
        
            # import the piece module
            modulename = piece['path'].replace('\\','.')
            module = importlib.import_module( modulename )
            self.pieces[foldername]['module'] = module
            
            # access it's data
            interaction_object()
        
            if self.DEBUG: print( 'loaded piece "%s".'%foldername )
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    ob = application()

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2021.02.03 → 2021.04.02
