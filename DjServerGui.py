

import sys
import PyQt4.Qt as Qt
#import PyQt4.Qwt5 as Qwt

from PyQt4 import QtSql, QtCore, QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Song import Song
#from PlaylistTableDelegate import PlaylistTableDelegate
#from BarHistogram import BarHistogram
from delegates import ProgressBarDelegate, myTableModel
import id3reader
from xml.dom import minidom
from servermain import DJServer
import socket, json

__version__ = "1.0.0"

#from pygooglechart import StackedHorizontalBarChart
from SocketMusicServer import initMusicServer


import ui_DjServerGui
import xml

#main window class

class DjServerGui(QMainWindow, ui_DjServerGui.Ui_ServerWindow):

    colors = (Qt.red,
              Qt.green,
              Qt.blue,
              Qt.cyan,
              Qt.magenta,
              Qt.yellow,
              )
    
    def __init__(self, mainHost = "localhost", mainPort = 9993, filename = None, parent = None):
        
        super(DjServerGui, self).__init__(parent)
        self.dir = None
        #set up widgets created from qt designer
        self.setupUi(self)
        self.setUpPlaylistTable()
#        self.setUpRatingChart()
        self.setUpRequestTable()
        
##        self.zipCode = self.getZipCode()
##        self.DJName = self.getDJName()
##        self.desc = self.getDescription()
        self.playlist = {}
        self.mainHost = mainHost
        self.mainPort = mainPort
        self.HOST = "localhost"
        self.PORT = 9999
        self.server = initMusicServer(self.HOST, self.PORT, self.playlist)
        #self.layout.setResizeMode(Qt.Fixed)
        self.id = 0
##        self.sendToMainServer(self.zipCode, self.DJName, self.desc)
##        
##    def sendToMainServer(self, zipCode, name, description):
##        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##        s.connect(("gmail.com",80))
##        ip = s.getsockname()[0]
##        s.close()
##        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##        if not self.connect_to_server():
##            print "brublem"
##            sys.exit(1)
##        msg = json.dumps({"req":str(2), "zip":str(zipCode), "name":name,
##                          "desc":description})
##        self.conn.send(msg)
##        print self.get_data()
##        self.conn.close()
##
##    def get_data(self):
##        data = []
##        while 1:
##            d = self.conn.recv(1024)
##            data.extend(d)
##            if len(d) < 1024: break
##        return "".join(data)
##    
##    def connect_to_server(self):
##        try:
##            self.conn.connect((self.mainHost, self.mainPort))
##            return 1
##        except socket.error, e:
##            print >>sys.stderr, "Cant connect to remote host", str(e)
##            return 0
        
    def getDJName(self):
        ok = False

        res, ok = QInputDialog.getText(self, "Enter Name", "Enter DJ name",  QLineEdit.Normal, "")

        if ok and not res.isEmpty(): pass
        else:
            sys.exit()
        return str(res)

    def getDescription(self):
        ok = False

        res, ok = QInputDialog.getText(self, "Enter Description", "Enter a Short Description(Theme, Genre etc.)",  QLineEdit.Normal, "")

        if ok and not res.isEmpty(): pass
        else:
            sys.exit()
        return str(res)


    def getZipCode(self):
        while True:
            ok = False

            res, ok = QInputDialog.getText(self, "Enter Zip Code",
                                       "Enter Zip Code of Your Current Location",
                                       QLineEdit.Normal, "")

            if ok and not res.isEmpty():
                if len(str(res))== 5 and str(res).isdigit():
                    break
                else:
                    QMessageBox.warning(self, "Warning", "Not a valid zip Code")
            else:
                #QApplication.exit(1)
                sys.exit()
        
        return int(str(res))

    
    def setUpPlaylistTable(self):

        self.model = myTableModel(['Title', 'Artist', 'Vote(s)'], self)
        self.tableViewSong.setModel(self.model)
        self.tableViewSong.setSortingEnabled(True)

        #progressDelegate = ProgressBarDelegate()
        #self.tableViewSong.setItemDelegate(progressDelegate)
        self.tableViewSong.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableViewSong.setShowGrid(False)
        # hide vertical header
        vh = self.tableViewSong.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = self.tableViewSong.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.tableViewSong.resizeColumnsToContents()

##        # set row height
##        nrows = len(self.playlist)
##        for row in xrange(nrows):
##            tv.setRowHeight(row, 18)
        self.tableViewSong.setSortingEnabled(True)
        #self.tableViewSong.
        
#    def setUpRatingChart(self): 
#        
#        chart = StackedHorizontalBarChart(500, 500,
#                                      x_range=(0, 35))
#        chart.set_bar_width(10)
#        chart.set_colours(['00ff00', 'ff0000'])
#        chart.add_data([1,2,3,4,5])
#        chart.add_data([1,4,9,16,25])
#        chart.download('bar-horizontal-stacked.png')

        

    def setUpRequestTable(self):
        self.model2 = myTableModel(['Title', 'Artist', 'Request(s)'], self)
        self.tableViewRequest.setModel(self.model2)
        self.tableViewRequest.setSortingEnabled(True)
        self.tableViewRequest.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableViewRequest.setShowGrid(False)
        # hide vertical header
        vh = self.tableViewRequest.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = self.tableViewRequest.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.tableViewRequest.resizeColumnsToContents()

##        # set row height
##        nrows = len(self.playlist)
##        for row in xrange(nrows):
##            tv.setRowHeight(row, 18)
        self.tableViewRequest.setSortingEnabled(True)
        #progressDelegate = ProgressBarDelegate()
        #self.tableViewRequest.setItemDelegateForColumn(1,progressDelegate)

    


    def getNextTag(self, nextSib):

        try:
            while nextSib.firstChild == None or not nextSib.firstChild.nodeValue in ["Name", "Artist", "Album"]:
                nextSib = nextSib.nextSibling
            return nextSib
        except AttributeError:
            return None
        #return False
        
    #parse itunes library xml file
    def importPlayList(self):

        self.clearSongList()
        
        if self.dir:
            dir = self.dir
        else:
            dir = "."
        
        fileName = QFileDialog.getOpenFileName(self, self.tr("Open Playlist"),
                                                   dir,
                                                   self.tr("xml (*.xml)"))
        if fileName == "":
            return
        try:
            xmlDoc = minidom.parse(str(fileName))
        except xml.parsers.expat.ExpatError:
            QMessageBox.warning(self, "Warning", fileName+" is not a valid \
xml file.")
            return
        
        keyList = xmlDoc.childNodes[1].childNodes[1].getElementsByTagName("key")
        
        #arbitrary list and dict that keeps the order in the original list.
        
        idSongDict = {}
        
        for x in xmlDoc.childNodes[1].childNodes[1].childNodes:
            if x.firstChild != None and x.firstChild.nodeValue == "Tracks":
                
                for y in x.nextSibling.nextSibling.getElementsByTagName("key"):

                    if y.firstChild.nodeValue == "Track ID":
                        ID = y.nextSibling.firstChild.nodeValue
                        nextSib = y.nextSibling
                        title =""
                        album =""
                        artist = ""
                        nextSib = self.getNextTag(nextSib)
                        while nextSib:
                            if nextSib.firstChild.nodeValue == "Name":
                                title = nextSib.nextSibling.firstChild.nodeValue
                            elif nextSib.firstChild.nodeValue == "Artist":
                                
                                artist = nextSib.nextSibling.firstChild.nodeValue
                                
                            elif nextSib.firstChild.nodeValue == "Album":
                                album = nextSib.nextSibling.firstChild.nodeValue
                            
                            nextSib = self.getNextTag(nextSib.nextSibling)
                        song = Song(title, artist, album)
                        idSongDict[int(ID)] = song
                        
            elif x.firstChild != None and x.firstChild.nodeValue == "Playlists":
                nodes = [node for node in  x.nextSibling.nextSibling.getElementsByTagName("key") if node.firstChild.nodeValue == "Track ID"]
                for y in nodes:
                    num =  y.nextSibling.firstChild.nodeValue
                    idSongDict[int(num)].id = self.id
                    self.playlist[self.id] = idSongDict[int(num)]
                    self.id +=1
                    self.addSongToTable(idSongDict[int(num)], self.model.rowCount()-2)
                    
        self.tableViewSong.resizeColumnsToContents()
        
    def addNewSong(self):
        if self.dir:
            dir = self.dir
        else:
            dir = "."
        
        fileName = QFileDialog.getOpenFileName(self, self.tr("Open audio file"),
                                                   dir,
                                                   self.tr("mp3 (*.mp3)"))
        if fileName == "":
            return
        id3r = id3reader.Reader(str(fileName))
        album = id3r.getValue('album')
        title = id3r.getValue('title')
        artist = id3r.getValue('performer')

        song = Song(title, artist, album)
        song.id = self.id
        self.playlist[self.id]=song
        self.id+=1
        self.addSongToTable(song)
        self.tableViewSong.resizeColumnsToContents()

        
    def addSongToTable(self, song, location = 0):
        songList = self.model.getList()
        
        if not song in songList:
            #print "adding"
            self.model.insertRows(0, 1, QModelIndex())
            
            index = self.model.index(0, 0, QModelIndex())
            self.model.setData(index, song.title, Qt.EditRole)
            index = self.model.index(0, 1, QModelIndex())
            self.model.setData(index, song.artist, Qt.EditRole)
            #removeTab(indexOf(newAddressTab))
            index = self.model.index(0, 2, QModelIndex())
            self.model.setData(index, song.votes, Qt.EditRole)
        else:
             QMessageBox.information(self, self.tr("Duplicate Song"),
             self.tr("The song \"%1\" already exists.").arg(song.title))
         

    def deleteSong(self):
        temp = self.tableViewSong
        proxy = temp.model()
        selectionModel = temp.selectionModel()
        #print selectionModel
        indexes = selectionModel.selectedIndexes()
     
        for index in indexes:
            self.model.removeRows(index.row(), 1, QModelIndex())
        #self.tableViewSong.resizeColumnsToContents()


        
    def clearSongList(self):

        self.model.removeRows(0, self.model.rowCount(), QModelIndex())
    
    def moveSongUp(self):
        selectionModel = temp.selectionModel()

    def moveSongDown(self): pass

    def closeApp(self):
        QApplication.exit(1)


    def addRequest(self, song):

        requestList = self.model.getList()
        
        if not song in requestList:
            
            self.model.insertRows(0, 1, QModelIndex())
            index = self.model.index(0, 0, QModelIndex())
            self.model.setData(index, song.title, Qt.EditRole)
            index = self.model.index(0, 1, QModelIndex())
            self.model.setData(index, song.artist, Qt.EditRole)
            #removeTab(indexOf(newAddressTab))
            index = self.model.index(0, 2, QModelIndex())
            self.model.setData(index, song.requests, Qt.EditRole)
        else:
            index = self.model.index(0, 2, QModelIndex())
            currentRequest = requestList[index.row()]
            self.model.setData(index, currentRequest+1, Qt.EditRole)
        self.tableViewSong.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = DjServerGui()
    gui.show()
    app.exec_()
