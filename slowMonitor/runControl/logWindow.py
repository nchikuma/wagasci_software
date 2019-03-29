# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore

# /////////////////////////////////////////////////////////////////////////////
#                                                                            //
# /////////////////////////////////////////////////////////////////////////////
class Logger( object ):
  def __init__( self, editor, out=None, color=None ):
    self.editor = editor    
    self.out    = out       
    if not color:
      self.color = editor.textColor()
    else:
      self.color = color

  def write( self, message ):
    self.editor.moveCursor( QtGui.QTextCursor.End )
    self.editor.setTextColor( self.color )
    self.editor.insertPlainText( message )
  
    if self.out:
      self.out.write( message )
# /////////////////////////////////////////////////////////////////////////////
#                                                                            //
# /////////////////////////////////////////////////////////////////////////////

class LogWindow( QtGui.QDialog ):
  def __init__( self, parent=None ):
    super( LogWindow, self ).__init__( parent )
    self.resize( 400, 500 )
    self.setWindowTitle( 'Log Window' )

    layout = QtGui.QVBoxLayout( self )

    resultTE       = QtGui.QTextEdit()
    resultTE.setReadOnly( True )         
    resultTE.setUndoRedoEnabled( False ) 

    sys.stdout = Logger(
      resultTE, sys.stdout
      )
    sys.stderr = Logger(
      resultTE, sys.stderr, QtGui.QColor(255, 0, 0)
      )
    layout.addWidget( resultTE )
