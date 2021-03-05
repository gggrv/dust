# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script main.
"""

# embedded in python
import os
# pip install
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
# same folder

"""-------------------------------------------------------------------------+++
Everything about AAAAAAAAAA.
"""
class sample( QtWidgets.QMainWindow ):
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( sample, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        
    """---------------------------------------------------------------------+++
    Everything about events.
    """
    def closeEvent( self, ev ):
        ev.ignore() # otherwise app closes, if it's self.w is hidden
        self.hide()
        self = None
        del self
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """ 
    def _init( self ):
        self.setObjectName( 'editor' )
        self.setWindowTitle( 'hit' )
        
"""-------------------------------------------------------------------------+++
autorun
"""
def inject_intotraymenu():
    """What to add to the host tray menu."""
    actions = [
        {
            'text': 'sample',
            'connect': autorun,
            'icon': 'icon.png',
            },
        ]
    return actions

def autorun( parent, *argv ):
    w = sample( parent=parent )
    w.show()
    
#---------------------------------------------------------------------------+++
# конец 2021.01.28 → 2021.02.03
