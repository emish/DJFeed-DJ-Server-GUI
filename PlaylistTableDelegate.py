

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class PlaylistTableDelegate(QItemDelegate):

    def __init__(self, parent = None):
        QItemDelegate(parent)
        self.mTeams = QStringList()
        
    def createEditor(self, parent, option, index):
        editor = 0

        
        if index.column() == 2:
            editor = QDateEdit(parent)
        elif index.column() == 3: pass
        elif index.column() == 4:
            editor = QProgressBar(parent)
        else:
            model = index.model()
            teams = QStringList()
            chosenTeams = QStringList()
            otherTeams = self.mTeams
            value = model.data(index, Qt.DisplayRole)
            team = value.toString()
            if not team.isEmpty():
                otherTeams.removeAll(team)
                teams << team
            for i in xrange(6):
                for j in xrange(2):
                    if i != index.row() or j != index.column():
                        ix = model.index(i,j)
                        value = model.data(ix, Qt.DisplayRole)
                        team = value.toString()
                        if not team.isEmpty():
                            otherTeams.removeAll(team)
                            chosenTeams << team
            chosenTeams.sort()
            teams << otherTeams << chosenTeams
            box = QComboBox(parent)
            box.addItems(teams)
            editor = box
        editor.installEventFilter(self)
        return editor



    def setEditorData(self, editor, index):

        value = index.model().data(index, Qt.DisplayRole)

        if index.column() == 2:
            editor.setDate(value.toDate())
        elif index.column() == 4:
            editor.setValue(value.toInt())
        else:
            box = editor
            box.setCurrentIndex(box.findText(value.toString()))
            

    def setModelData(self, editor, model, index):

        if index.column() == 2:
            date = editor.date()
            value = date
            MatchesModel.setDefaultDate(date)
        elif index.column() == 4:
            value = editor.value()
        else:
            value = editor.currentText()

        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
