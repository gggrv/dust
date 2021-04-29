# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script main.
"""

# embedded in python
import calendar
import datetime as dt
from functools import partial
import os
from sys import argv as ARRRGV
# pip install
from numpy import int
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
# same folder

def readf( path ):
    with open( path, 'r', encoding='utf-8' ) as f:
        return f.read()
    
def savef( path, text ):
    with open( path, 'w', encoding='utf-8' ) as f:
        f.write(text)
    
def appef( path, text ):
    with open( path, 'a', encoding='utf-8' ) as f:
        f.write(text)
    
def append( path ):
    # I might be working from this directory or from the host.pyw
    # directory. With this function I fix paths.
    if __name__ == '__main__': return path
    return os.path.join('pieces','ribbon',path)

def chop( text, L, R ):
    # Chops the text str as instructed.
    
    A, B = 0, len(text) # placeholder
    
    # what to do with L
    if type(L)==int: A=L
    elif type(L)==str: A=text.find(L)+len(L)
    text = text[A:]
    
    # what to do with R
    if type(R)==int: B = R
    elif type(R)==str: B = [B,text.find(R)][R in text]
    
    return text[:B].strip()

def path_safe( text ):
    forbid = list(':?/\\*&|')
    for symbol in forbid: text=text.replace(symbol,'')
    return text

def unique_id():
    now = dt.datetime.now()
    text = path_safe( str(now) )
    return text

"""-------------------------------------------------------------------------+++
Everything about headless.
"""
# names of the files that i need in order to classify path as a ribbon
NAMEKEY = 'name'
SETSKEY = 'sets'
RIBSKEY = 'ribs'

# where i store paths to various ribbons, i.e. the library
FILE_WITH_PATHS = append('ribbons')

def get_ribbon( root ):
    # Gets specific ribbon.
    
    name_file = os.path.join( root,NAMEKEY )
    sets_file = os.path.join( root,SETSKEY )
    ribs_fold = os.path.join( root,RIBSKEY )
    
    ribbon = { # placeholder with default values
        'name': root, # initially, name is the same as the path
        'sets': False, # no sets exist yet
        'ribs': False, # no ribs exist yet
        'show': True, # i want it to show up as a separate tab in the library
        'path': root, # where is it
        }
    
    if os.path.exists( name_file ):
        if os.path.isfile(name_file): ribbon[NAMEKEY]=readf(name_file)
    if os.path.exists( sets_file ):
        if os.path.isfile(sets_file): ribbon[SETSKEY]=True
    if os.path.exists( ribs_fold ):
        if os.path.isdir(ribs_fold): ribbon[RIBSKEY]=True
        
    return ribbon

def get_library():
    # Returns ribbons that are in the library.
    
    if not os.path.exists( FILE_WITH_PATHS ): return {}
    
    text = readf( FILE_WITH_PATHS )
    lines = text.split('\n')
    
    ribbons = {}
    for line in lines:
        if len(line)<2: continue
        # get ribbon and overwrite some library-overwrittable values
        ribbon = get_ribbon( line[1:] )
        ribbon['show'] = True if line[0]=='+' else False
        ribbons.setdefault( ribbon['name'], ribbon )
        
    return ribbons

def already_in_library( path ):
    # Checks whether this ribbon path is already in the library.
    
    ribbons = get_library()
    isduplicate = False
    for ribbon in ribbons.values():
        if ribbon['path']==path:
            isduplicate=True
            break
    return isduplicate

def add_ribbon( path, name=None, show=True ):
    # Adds ribbon to the library.
    
    # i don't want to add duplicate paths to the library
    if already_in_library(path): return True
    
    # ensure ribbon existance
    if not os.path.exists(path): os.mkdir(path)
    if name: savef( os.path.join(path,NAMEKEY),name )
    
    # add record to the library
    show = '+' if show else '-' # whether i want it to show up as a tab
    appef( FILE_WITH_PATHS, '\n%s%s'%(show,path) )
    
    return True

def add_rib( label, ribbon_name ):
    # Adds rib to existing ribbon.
    
    # skip if ribbon_name is not in library
    ribbons = get_library()
    if not ribbon_name in ribbons: return False
    ribbon = ribbons[ribbon_name] # for faster reference
    
    destfolder = os.path.join( ribbon['path'],RIBSKEY )
    # make sure destination exists
    if not ribbon['ribs']: os.mkdir(destfolder) # this would be the first rib
    
    # make unique name
    uniqval = unique_id()
    
    # make empty object
    days = [ i+1 for i in range(31) ]
    days.insert( 0,label )
    df = pd.DataFrame( columns=days )
    
    # save it
    destname = '%s %s.csv'%( uniqval, path_safe(label) )
    dest = os.path.join( destfolder,destname )
    df.to_csv( dest, index=False )
    
    return True

def get_rib( uniqval, ribbon_name ):
    # Gets existing rib from existing ribbon.
    
    # skip if ribbon_name is not in library
    ribbons = get_library()
    if not ribbon_name in ribbons: return None
    ribbon = ribbons[ribbon_name] # for faster reference
    
    destfolder = os.path.join( ribbon['path'],RIBSKEY )
    # make sure destination exists
    if not ribbon['ribs']: return None
    
    for f in os.listdir( destfolder ):
        name,ext = os.path.splitext(f)
        if not ext=='.csv': continue
        if not chop(name,None,' ')==uniqval: continue
    
        df = pd.read_csv( os.path.join(destfolder,f) )
        df.set_index( df.columns[0], inplace=True )
        return df
    
    return None

def add_set( label, uniqvals, ribbon_name ):
    # Defines set of ribs in existing ribbon.
    
    # skip if ribbon_name is not in library
    ribbons = get_library()
    if not ribbon_name in ribbons: return False
    ribbon = ribbons[ribbon_name] # for faster reference
    
    dest = os.path.join( ribbon['path'],SETSKEY )
    
    uniqvals = [ str(v) for v in uniqvals ] # uniqvals must be strings
    uniqvals.insert(0,label) # i also need a label
    appef( dest, '\n%s'%','.join(uniqvals) )
    
    return True

def get_sets( ribbon_name ):
    # Gets existing sets from a library ribbon.
    
    ribbons = get_library()
    
    # skip if ribbon_name is not in the library
    ribbons = get_library()
    if not ribbon_name in ribbons: return []
    ribbon = ribbons[ribbon_name] # for faster reference
    
    setspath = os.path.join( ribbon['path'],SETSKEY )
    setstext = readf(setspath)
    
    sets = {}
    for line in setstext.split('\n'):
        if line.count(',')<1: continue # not enough values, file might be corrupt
        setvals = line.split(',')
        sets.setdefault( setvals[0], setvals[1:] )
        
    return sets

def ribs_per_date( ribs, date=dt.datetime.now() ):
    loc=date
    if not type(loc)==str:
        # by default i assume i want the current date
        loc = dt.datetime.strftime(date,'%Y.%m.%d')
        # %d should be number of days in the %m
        loc = '%s%s'%(loc[:8],calendar.monthrange(date.year,date.month)[1])
    
    # gather all corr. rows from ribs
    rows = []
    labels = []
    for rib in ribs:
        labels.append( rib.index.name ) # ribname is there
        # skip unapplicable
        if not loc in rib.index:
            rows.append( pd.Series() )
            continue
        rows.append( rib.loc[loc] )
    
    # combine them into a single table
    df = pd.concat( rows,axis=1 ).T
    df.index=labels
    return df
    
def newmonth():
    now = dt.datetime.now()
    header = newheader( now.year, now.month )
    ribs = allribs()
    
    lines = [header]
    for loc, rib in ribs.iterrows():
        ribloc = hex(rib['ribloc'])[2:]
        if len(ribloc)<4: ribloc=('0'*(4-len(ribloc)))+ribloc
        line = ribloc + ' '*31*2 + rib['comment']
        lines.append( line )
        
    text = '\n'+'\n'.join(lines)
    appef( RIB, text )

"""-------------------------------------------------------------------------+++
Everything about gui.
"""
class riblabel( QtWidgets.QLabel ):
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( riblabel, self ).__init__( parent, *args, **kwargs )
        
        self.setTextInteractionFlags( QtCore.Qt.TextEditorInteraction )

class ribtab( QtWidgets.QWidget ):
    
    right_pane_width = 200 # max width of the ribtab right half
    value_column_width = 2 # max width of the columns with values
    
    # unusable placeholders that are overwritten
    # during object construction and ribbon loading
    ribbon = None # unusable
    df = None # current table to be shown
    date = None # which date should i show
    
    # usable placeholders
    sets = [] # contains the result of get_sets()
    ribs = [] # contains loaded ribs, i.e. is a list of pd.DataFrames
    
    def __init__( self,
                  ribbon,
                  parent=None,
                  *args, **kwargs ):
        super( ribtab, self ).__init__( parent, *args, **kwargs )
        
        # pointer to ribbon
        self.ribbon = ribbon
    
        now = dt.datetime.now()
        # by default i assume i want the current date
        self.date = dt.datetime.strftime(now,'%Y.%m.%d')
        # %d should be number of days in the %m
        self.date = '%s%s'%(self.date[:8],calendar.monthrange(now.year,now.month)[1])
    
        # gui
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about dynamic changes.
    """
    def _showribs( self ):
        # Looks at the month in self.date.
        # Shows several ribs' values at that month.
        """-----------------------------------------------------------------+++
        Definitions.
        """
        editarea = self.findChild( QtWidgets.QGridLayout,'editarea' )
        
        def populate_toprow():
            
            # top-left corner
            date = riblabel( self )
            date.setObjectName( 'date' )
            date.setText( self.date )
            editarea.addWidget(date,0,0)
            
            # top row
            for iloc in range(1,32):
                day = riblabel( self )
                day.setObjectName( '0_%s'%(iloc) )
                day.setText( str(iloc) )
                editarea.addWidget(day,0,iloc)
        
        def populate_otherrow():
            
            # top-left corner
            date = riblabel( self )
            date.setObjectName( 'date' )
            date.setText( self.date )
            editarea.addWidget(date,0,0)
            
            # top row
            for iloc in range(1,32):
                day = riblabel( self )
                day.setObjectName( '0_%s'%(iloc) )
                day.setText( str(iloc) )
                editarea.addWidget(day,0,iloc)
            
        """-----------------------------------------------------------------+++
        Actual code.
        """
        # remove existing
        while editarea.count()>0:
            item = editarea.takeAt(0)
            if type(item)==type(None): continue
            w = item.widget()
            if type(w)==type(None): continue
            w.deleteLater()
            
        populate_toprow()
        
        # populate with data
        rowiloc = 1
        for loc, row in self.df.iterrows():
            underdate = riblabel( self )
            underdate.setObjectName( '%s_%s'%(rowiloc,0) )
            underdate.setText( loc )
            editarea.addWidget(underdate,rowiloc,0)
            for coliloc, value in enumerate(row):
                underday = riblabel( self )
                underday.setObjectName( '%s_%s'%(rowiloc,coliloc+1) )
                underday.setText( str(value) )
                editarea.addWidget(underday,rowiloc,coliloc+1)
            rowiloc += 1
        
    def _showset( self, setname ):
        # Looks at setname and loads ribs that are defined in that set.
        
        # clear loaded ribs
        self.ribs = []
        
        # load ribs from setname
        univals = self.sets[setname]
        for uniqval in univals:
            df = get_rib( uniqval, self.ribbon['name'] )
            self.ribs.append(df)
            
        # combine into one viewable table for this month
        df = ribs_per_date( self.ribs, date=self.date )
        self.df = df
        
        # show it
        self._showribs()
        
    def _load_sets( self ):
        # Populates scrollarea widget layout with existing sets.
        
        # skip if not a single set exists yet
        if not self.ribbon['sets']: return None
        self.sets = get_sets( self.ribbon['name'] )
        
        #searchbox = self.findChild( QtWidgets.QLineEdit,'searchbox' )
        vbox = self.findChild( QtWidgets.QVBoxLayout,'right_vbox' )
        
        # remove existing after searchbox and before stretch
        while vbox.count()>1:
            item = vbox.takeAt(1)
            if type(item)==type(None): continue
            w = item.widget()
            if type(w)==type(None): continue
            w.deleteLater()
            
        for setname in self.sets:
            item = QtWidgets.QPushButton( self )
            item.setObjectName( 'item_%s'%setname )
            item.setText( setname )
            item.clicked.connect( partial(self._showset,setname) )
            vbox.addWidget( item )
        vbox.addStretch()
    
    """---------------------------------------------------------------------+++
    Everything about init.
    """ 
    def _init_staticwidgets( self ):
        # layout
        lyt = QtWidgets.QHBoxLayout( self )
        lyt.setObjectName( 'hbox' )
        
        # left side
        editarea = QtWidgets.QGridLayout( self )
        editarea.setObjectName( 'editarea' )
        
        # right side
        
        # layout
        rlyt = QtWidgets.QVBoxLayout( self )
        rlyt.setObjectName( 'right_vbox' )
        
        # searchbox
        searchbox = QtWidgets.QLineEdit( self )
        searchbox.setObjectName( 'searchbox' )
        searchbox.setMaximumWidth( self.right_pane_width )
        
        # assemble right side
        rlyt.addWidget( searchbox )
        rlyt.addStretch()
        
        # assemble
        lyt.addLayout( editarea )
        lyt.addLayout( rlyt )
        self.setLayout( lyt )

class ribbontabs( QtWidgets.QTabWidget ):
    
    library = []
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( ribbontabs, self ).__init__( parent, *args, **kwargs )
        
        # headless data
        self.library = get_library()
        
        # gui
        self._init_dynamicwidgets() # they are independent of anything
        self._init_mastertab() # i want it to be the last one
        
        # signals
        self.currentChanged.connect(self.onTabChange)
        
        """
        # flags
        self.setObjectName( 'ribbon' )
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.SplashScreen
            )
        self.setTabPosition( QtWidgets.QTabWidget.East )
        #self.setStyleSheet( 'background-color:rgb(33,33,33);color:white;font-family:consolas' )
        """
        
        # placement
        screen = QtWidgets.QDesktopWidget().screenGeometry(0)
        w,h = screen.width(), screen.height()
        triwidth = w//1.5
        x = screen.left()+w//2-triwidth//2
        self.move( x, screen.top() )
        self.resize( triwidth, h )
        
    """---------------------------------------------------------------------+++
    Everything about tabs.
    """
    def onTabChange( self, iloc ):
        # skip non-dynamically updateable tabs
        tab = self.findChild( ribtab, 'tab_%s'%iloc )
        if type(tab)==type(None): return None
        
        # load available sets from corr. ribbon
        tab._load_sets()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_mastertab( self ):
        # mastertab with library and so on
        mastertab = QtWidgets.QWidget( self )
        mastertab.setObjectName( 'mastertab' )
        """
        # layout
        vbox = QtWidgets.QVBoxLayout( self )
        vbox.setObjectName( 'vbox' )
        
        # ribs
        form_ribs = QtWidgets.QFormLayout( self )
        form_ribs.setObjectName( 'form_ribs' )
        form_ribs.addRow( QtWidgets.QLineEdit(), QtWidgets.QComboBox )
        
        # sets
        form_sets = QtWidgets.QFormLayout()
        form_sets.setObjectName( 'form_sets' )
        
        # assemble
        vbox.addLayout( form_ribs )
        vbox.addLayout( form_sets )
        mastertab.setLayout( vbox )
        """
        self.addTab( mastertab, '' )
        
    def _init_dynamicwidgets( self ):
        # Here I add a tab for each user ribbon folder.
        
        # add tab for each visible ribbon
        for iloc, ribbon in enumerate( self.library.values() ):
            if not ribbon['show']: continue
            tab = ribtab( ribbon, parent=self )
            tab.setObjectName( 'tab_%s'%iloc )
            self.addTab( tab, ribbon['name'] )

class interaction_object( QtWidgets.QMainWindow ):
    
    def __init__( self,
                  parent=None,
                  host_app=None,
                  *args, **kwargs ):
        super( interaction_object, self ).__init__( parent, *args, **kwargs )
        
        # pointer to the host application
        self.host = host_app
        
        # gui
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        #self.w = ribbontabs( self )
        self.w = ribbontabs() # no parent for normal window
        
    """---------------------------------------------------------------------+++
    Everything about subwidgets.
    """
    def show_ribbons( self ):
        self.w.show()
        # i want to update current tab to trigger it's sets loading
        self.w.setCurrentIndex( self.w.count()-1 ) # open mastertab
        self.w.setCurrentIndex(0) # open first tab
        
    """---------------------------------------------------------------------+++
    Everything about link to the host.
    """
    def hosttraynotification( self, text ):
        self.host.icon.showMessage( 'dust ribbon', text,
            QtWidgets.QSystemTrayIcon.Information,
            2000 )
    
    def uponhostdestruction( self ):
        """What to do when the host terminates."""
        self.w.destroy()
        self.destroy()
    
    def inject_intotraymenu( self ):
        actions = [
            {
                'text': 'ribbon',
                'connect': self.show_ribbons,
                'icon': 'icon.png'
                },
            ]
        return actions
    
#---------------------------------------------------------------------------+++
# конец 2021.02.03 → 2021.04.02
