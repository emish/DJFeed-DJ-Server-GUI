from PyQt4.QtCore import *
from PyQt4.QtGui import *

import operator
from Song import Song

class ProgressBarDelegate(QItemDelegate):

    def createEditor(self, parent, option, index):
        editor = QProgressBar(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)
        print 'progressbar'
        return editor

    def setEditorData(self, progressBar, index):
        value = index.model().data(index, Qt.EditRole).toInt()[0]

        progressBar.setValue(value)

    def setModelData(self, progressBar, model, index):
        progressBar.interpretText()
        value = progressBar.value()

        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class myTableModel(QAbstractTableModel):

    def __init__(self, headerdata, parent = None):
        self.listOfSongs = list()
        #self.progressBarList = list()
        super(myTableModel, self).__init__(parent)
        self.headerdata = headerdata
        
    def rowCount(self, parent=None):
        return len(self.listOfSongs)

    def columnCount(self, parent=None):
        return 3
    
    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.listOfSongs) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole :
            song = self.listOfSongs[index.row()]

            if index.column() == 0:
                return song.title
            elif index.column() == 1:
                return song.artist
            elif index.column() == 2:
                return song.votes
        return QVariant()

    def insertRows(self, position, rows, index):
        self.beginInsertRows(QModelIndex(), position, position+rows-1)

        for x in xrange(rows):
            song = Song()
            self.listOfSongs.insert(position, song)
            #progressbar = QProgressBar()
            #self.progressBarList.insert(position, progressbar) 
        self.endInsertRows()
        return True

##    def headerData(self, section, orientation, role):
##        if role != Qt.DisplayRole:
##            return QVariant()
##
##        if orientation == Qt.Horizontal:
##            if section == 0:
##                return self.tr("Title")
##
##            elif section == 1:
##                return self.tr("Artist")
##            elif section == 2:
##                return self.tr("Vote")
##            else:
##                 return QVariant()
##        return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()


    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            
            p = self.listOfSongs[row]
            #bar = self.progressBarList[row]
            if index.column() == 0:
                p.title = str(value)
            elif index.column() == 1:
                p.artist = str(value)
            elif index.column() == 2:
                p.votes = int(value)
            else:
                return False

            self.listOfSongs[row] = p
            #self.emit(dataChanged(index, index))

            return True
        return False

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        
        self.listOfSongs = sorted(self.listOfSongs, key =operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.listOfSongs.reverse()
        self.emit(SIGNAL("layoutChanged()"))


    def removeRows(self, position, rows, index):
        self.beginRemoveRows(QModelIndex(), position, position+rows-1)

        for x in xrange(rows):
            self.listOfSongs.pop(position)
            #self.progressBarList.pop(position)
        self.endRemoveRows()
        return True

##    def flags(self, index):
##
##        if not index.isValid():
##            return ItemIsEnabled
##        return QAbstractTableModel.flags(index) | Qt.ItemIsEditable
    
    def getList(self):
        return self.listOfSongs
