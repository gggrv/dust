# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script main.
"""

# embedded in python
from time import sleep
# pip install
from numpy import int
import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
# same folder

class hungrywidget( QtWidgets.QWidget ):
    
    # minimum height of the open mouth
    zev_height = 100
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( hungrywidget, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setObjectName( 'hungrywidget' )
        
    def _init_staticwidgets( self ):
        
        # layout
        lyt = QtWidgets.QVBoxLayout()
        lyt.setObjectName( 'vbox' )
        lyt.setContentsMargins(0,0,0,0)
        
        # top label
        eyes = QtWidgets.QLabel( self )
        eyes.setObjectName( 'eyes' )
        eyes.setText( '     Θ     Θ     ' )
        jaw1 = QtWidgets.QLabel( self )
        jaw1.setObjectName( 'jaw1' )
        jaw1.setText( 'VVVVVVVVVVVVVVVVV' )
        
        # middle label
        zev = QtWidgets.QLabel( self )
        zev.setObjectName( 'zev' )
        zev.setMinimumHeight( self.zev_height )
        
        # bottom label
        jaw2 = QtWidgets.QLabel( self )
        jaw2.setObjectName( 'jaw2' )
        jaw2.setText( 'ЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛ' )
        
        # assemble
        lyt.addWidget( eyes )
        lyt.addWidget( jaw1 )
        lyt.addWidget( zev )
        lyt.addWidget( jaw2 )
        self.setLayout( lyt )

class followindow( QtWidgets.QWidget ):
    
    # distance from mouse
    mouse_distance = [50,50] # where to stop near the mouse
    trigger_distance = [150,150] # when to chase after mouse
    
    # followindow dimensions
    bigger_dims = [300,300] # when enlarged
    smaller_dims = [10,10] # when small
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( followindow, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init_staticwidgets()
        
        
        # i *must* call the following lines from the constructor,
        # because otherwise dropping items with mouse on the
        # followindow does not work.
        # this behaviour heavily depends on the window flag
        # that i *need*: QtCore.Qt.SplashScreen
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.SplashScreen
            ) # !!!
        self.setAcceptDrops(True) # !!!
        
    """---------------------------------------------------------------------+++
    Everything about events.
    """
    def closeEvent( self, ev ):
        """Otherwise the application class in host.py disregards it's own
        QMainWindow object instance at self.m and stops the gui mainloop.
        """
        self.destroy()
        ev.ignore() # !!!
        
    def dragEnterEvent( self, ev ):
        print( 'enter', ev.mimeData() )
        
        # show the hungry widget
        self.hung.setVisible(True)
        
        # show enlarged window, mouse in the middle
        cx,cy = self.x(), self.y() # current dims and coords
        nw,nh = self.hung.width(),self.hung.height() # next dims and coords
        self.resize( nw,nh )
        self.move( cx-nw//2, cy-nh//2 )
        
        #if ev.mimeData().hasText(): ev.accept()
        #else: ev.ignore()
        ev.accept()
        
    def dropEvent( self, ev ):
        print( 'drop' )
        
        # hide the hungry widget
        self.hung.setVisible(False)
        
        # show small window near the mouse
        cw,ch = self.width(),self.height() # current dims and coords↓
        cx,cy = self.x(), self.y()
        nw,nh = self.smaller_dims # next dims and coords
        self.resize( nw,nh )
        self.move( cx+cw//2, cy+ch//2 )
        
        ev.accept()
        
    def dragLeaveEvent( self, ev ):
        # hide the hungry widget
        self.hung.setVisible(False)
        
        # show small window near the mouse
        cw,ch = self.width(),self.height() # current dims and coords↓
        cx,cy = self.x(), self.y()
        nw,nh = self.smaller_dims # next dims and coords
        self.resize( nw,nh )
        self.move( cx+cw//2, cy+ch//2 )
        
        ev.accept()
        
    def mouseEnter( self, ev ):
        # show enlarged window, mouse in the middle
        cx,cy = self.x(), self.y() # current dims and coords
        nw,nh = self.bigger_dims # next dims and coords
        self.resize( nw,nh )
        self.move( cx-nw//2, cy-nh//2 )
        
    def mouseLeave( self, ev ):
        # show small window near the mouse
        cw,ch = self.width(),self.height() # current dims and coords↓
        cx,cy = self.x(), self.y()
        nw,nh = self.smaller_dims # next dims and coords
        self.resize( nw,nh )
        self.move( cx+cw//2, cy+ch//2 )
        
    def teleport( self, x,y ):
        smallest_dim = min(self.smaller_dims)
        amount = 2
        halfamount = amount//2
        frames = smallest_dim//amount-1
        
        # shrink in place
        for _ in range( frames ):
            self.resize( self.width()-amount, self.height()-amount )
            self.move( self.x()+halfamount,self.y()+halfamount )
            sleep(0.05)
        self.hide()
        self.move( x,y )
        self.resize( 1, 1 )
        self.show()
        # grow in place
        for _ in range( frames ):
            self.resize( self.width()+amount, self.height()+amount )
            self.move( self.x()-halfamount,self.y()-halfamount )
            sleep(0.08)
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        
        # layout
        lyt = QtWidgets.QVBoxLayout()
        lyt.setObjectName( 'vbox' )
        lyt.setContentsMargins(0,0,0,0)
        
        # background label
        bg = QtWidgets.QWidget( self )
        bg.setObjectName( 'bg' )
        bg.setStyleSheet( 'background-color:rgb(33,33,33);color:white;font-family:consolas' )
        
        # hidden hungry widget
        self.hung = hungrywidget( bg )
        self.hung.setVisible( False )
        
        # assemble self
        lyt.addWidget( bg )
        self.setLayout( lyt )
        
        # i *must* call self.show, because if i use .show() from another
        # object, dropping items with mouse on the
        # followindow does not work.
        # this behaviour heavily depends on the window flag
        # that i *need*: QtCore.Qt.SplashScreen
        self.show() # !!!

class interaction_object( QtWidgets.QMainWindow ):
    
    followindows = []
    
    def __init__( self,
                  parent=None,
                  host_app=None,
                  *args, **kwargs ):
        super( interaction_object, self ).__init__( parent, *args, **kwargs )
        
        # pointer to the host application
        self.host = host_app
        
        # gui
        self._init()
        self._init_timer()
        self._spawn_followindows() # they are visible
    
    """---------------------------------------------------------------------+++
    Everything about followindows.
    """
    
    def eventFilter( self, ob, ev ):
        # help:
        # https://stackoverflow.com/questions/52291734/pyqt5-mouse-hover-functions
        
        # what to do with ghostwindows
        if type(ob)==followindow:
            
            # hover enter???
            if ev.type()==10:
                self.follotimer.stop()
                ob.mouseEnter(ev)
            # hover leave???
            elif ev.type()==11:
                self.follotimer.start()
                ob.mouseLeave(ev)
            
        return super(interaction_object,self).eventFilter( ob, ev )
    
    def _control_followindows( self ):
        # help:
        # https://www.geeksforgeeks.org/check-if-a-point-is-inside-outside-or-on-the-ellipse/
        """-----------------------------------------------------------------+++
        Definitions.
        """
        
        def calc_ellipse( x,y,a,b ):
            result = (x*x)/(a*a) + (y*y)/(b*b)
            return result
        
        def chase_after_mouse():
            # here i calculate ellipse equation
            # i check, whether current followindow middle point is
            # inside some ellipse-shaped zone around the mouse
            # that ellipse-shaped zone is defined by
            # values in followindow.trigger_distence
            #result = (dx*dx)/(t1*t1) + (dy*dy)/(t2*t2)
            #if result<=1: return False
            aa,bb = w.trigger_distance # when to start chasing
            result = calc_ellipse( cx-x,cy-y, aa+aa,bb+bb )
            if result<=1: return False
            return True
        
        def closest_point():
            # equation of a line is y=kx+b
            # i have a line between the pointA, the mouse (x;y), and
            # pointB, the followindow middle (cx;cy)
            # those are k and b for the line that connects them:
            b_chis = (x*cy)-(cx*y)
            b_znam = x-cx
            if b_znam==0: b_znam=1
            b = b_chis/b_znam
            k = (y-b)/1 if x==0 else (y-b)/x
            
            # now i need some pointC, where i will move the
            # followindow. pointC lies on the line↑ and also lies on
            # an ellipse around pointA, that is defined by
            # values in followindow.mouse_distance
            aa,bb = w.mouse_distance
            step = -1 if x>cx else 1
            for x1 in range( x,cx,step ):
                y1 = int(k*x1+b)
                if y1<0: break
                result = int( calc_ellipse( x1-x,y1-y, aa+aa,bb+bb ) )
                if result==1: return x1,y1
                
            return cx,cy
        
        """-----------------------------------------------------------------+++
        Actual code.
        """
        for w in self.followindows:
            # skip invisible ones
            if not w.isVisible(): continue
        
            # where is the mouse
            x,y = pyautogui.position() # mouse coords
            
            # where am i
            hw,hh = w.width()//2, w.height()//2 # half followindow dims
            cx,cy = w.x()+hw, w.y()+hh # current middle of the followindow
            
            # do i even need to move?
            if not chase_after_mouse(): return None
            
            # where should i move?
            nx,ny = closest_point()
            
            # initiate the smooth movement
            w.teleport( nx,ny )
    
    def _spawn_followindows( self ):
        """Spawns predefined number of followindows."""
        
        for iloc in range(1):
            # spawn the window
            #w = followindow( parent=self )
            w = followindow()
            
            # give it unique object name
            w.setObjectName( 'followindow_%s'%iloc )
            
            # resize it so it's small
            w.resize( 10, 10 )
            
            # event filter
            w.installEventFilter(self)
            
            # remember link to it for faster navigation
            self.followindows.append( w )
    
    def show_followindows( self ):
        """Starts showing hidden followindows and launch follotimer."""
        for w in self.followindows:
            w.show()
            self.follotimer.start()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setObjectName( 'grimoire' )
        
    def _init_timer( self ):
        self.follotimer = QtCore.QTimer( self )
        self.follotimer.setInterval(50)
        self.follotimer.timeout.connect( self._control_followindows )
        
    """---------------------------------------------------------------------+++
    Everything about link to the host.
    """
    def uponhostdestruction( self ):
        """What to do when the host terminates."""
        for w in self.followindows: w.destroy()
        self.destroy()
    
    def inject_intotraymenu( self ):
        actions = [
            {
                'text': 'grimoire',
                'connect': self.show_followindows,
                'icon': 'icon.png'
                },
            ]
        return actions
    
#---------------------------------------------------------------------------+++
# конец 2021.03.30 → 2021.04.02
