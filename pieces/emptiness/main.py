# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script main.
"""

# embedded in python
# pip install
from PyQt5 import QtCore, QtGui, QtWidgets
# same folder

class ghostwindow( QtWidgets.QDialog ):
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( ghostwindow, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about events.
    """
    def closeEvent( self, ev ):
        """Otherwise the application class in host.py disregards it's own
        QMainWindow object instance at self.m and stops the gui mainloop.
        """
        self.destroy()
        ev.ignore() # !!!
        
    def subEvFilter10( self, ev ):
        # hover enter???
        
        # get the interaction object
        ob = self.parent()
        
        # hide self, show others
        for w in ob.subwindows: w.show()
        self.hide()
       
    """
    def subEvFilter11( self, ev ):
        # hover leave???
        pass
    """
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.SplashScreen
            )
        
        # i want to access mouse and keyboard input
        self.setMouseTracking( True )
        #self.setFocusPolicy( QtCore.Qt.StrongFocus )
        
    def _init_staticwidgets( self ):
        
        # layout
        lyt = QtWidgets.QVBoxLayout()
        lyt.setObjectName( 'vbox' )
        lyt.setContentsMargins(0,0,0,0)
        
        # label
        lab = QtWidgets.QWidget( self )
        lab.setObjectName( 'bg' )
        lab.setStyleSheet( 'background-color:rgb(33,33,33);' )
        
        # assemble
        lyt.addWidget( lab )
        self.setLayout( lyt )

class emptiness( QtWidgets.QMainWindow ):
    
    subwindows = []
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( emptiness, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        #self._spawn_windows()
    
    """---------------------------------------------------------------------+++
    Everything about subwindows.
    """
    def eventFilter( self, ob, ev ):
        # help:
        # https://stackoverflow.com/questions/52291734/pyqt5-mouse-hover-functions
        
        # what to do with ghostwindows
        if type(ob)==ghostwindow:
            
            # hover enter???
            if ev.type()==10: ob.subEvFilter10(ev)
            # hover leave???
            #elif ev.type()==11: ob.subEvFilter11(ev)
            
        return super(emptiness,self).eventFilter( ob, ev )
    
    def _spawn_windows( self ):
        """Spawns a hidden subwindow on each screen."""
        
        nscreens = QtWidgets.QDesktopWidget().screenCount()
        for iloc in range(nscreens):
            # spawn the window
            w = ghostwindow( parent=self )
            
            # give it unique object name
            w.setObjectName( 'ghostwindow_%s'%iloc )
            
            # place it on the correct screen
            screen = QtWidgets.QDesktopWidget().screenGeometry(iloc)
            #w.move( screen.left(), screen.top()//2 ) # debug
            #w.resize( screen.width(), screen.height()//2 ) # debug
            w.move( screen.left(), screen.top() )
            w.resize( screen.width(), screen.height() )
            
            # event filter
            w.installEventFilter(self)
            
            # remember link to it for faster navigation
            self.subwindows.append( w )
            
            w.show()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setObjectName( 'emptiness' )
        
"""-------------------------------------------------------------------------+++
autorun
"""
def interaction_object():
    """Is there any object that allows further interaction with this piece?"""
    emp = emptiness()
    return emp

def inject_intotraymenu():
    """What to add to the host tray menu.
    Depends on interaction_object from the host side!
    """
    actions = [
        {
            'text': 'emptiness',
            'connect': trayrun,
            'icon': 'icon.png',
            },
        ]
    return actions
    
def uponhostdestruction( interaction_object ):
    """What to do when the host terminates.
    Depends on interaction_object!
    """
    ob = interaction_object # shorter name
    for w in ob.subwindows: w.destroy()
    ob.destroy()
    
def trayrun( interaction_object ):
    """What to do when the corr. to this piece tray menu item
    in the host is clicked.
    Depends on interaction_object!
    """
    ob = interaction_object # shorter name
    ob._spawn_windows()
    
#---------------------------------------------------------------------------+++
# конец 2021.03.27 → 2021.03.28
