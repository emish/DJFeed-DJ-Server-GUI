

import sys
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Song import Song

__version__ = "1.0.0"





#main window class

class DjServer(QMainWindow, ui_sc_ext.Ui_MainWindow):
    
    def __init__(self, filename = None, parent = None):
        
        super(DjServer, self).__init__(parent)
        
        #set up widgets created from qt designer
        self.setupUi(self)
    


    #parse itunes library xml file
    def importPlayList(self):
        fileName = QFileDialog.getOpenFileName(self, self.tr("Open Playlist"),
                                                   self.dir,
                                                   self.tr("xml (*.xml)"))
        try:
            xmlDoc = minidom.parse(str(fileName))
        except xml.parsers.expat.ExpatError:
            QMessageBox.warning(self, "Warning", fileName+" is not a valid \
xml file.")
            return
        
        keyList = xml.childNodes[1].childNodes[1].getElementsByTagName("key")
        

        #arbitrary list and dict that keeps the order in the original list.
        playlist = []
        order = {}
        number = 0
        for x in xml.childNodes[1].childNodes[1].childNodes:
            if x.firstChild != None and x.firstChild.nodeValue == "Tracks":
                
                for y in x.nextSibling.nextSibling.getElementsByTagName("key"):

                    if y.firstChild.nodeValue == "Track ID":
                        ID = y.nextSibling.firstChild.nodeValue
                        nextSib = y.nextSibling
                        while nextSib.firstChild == None or nextSib.firstChild.nodeValue != "Name":
                            nextSib = nextSib.nextSibling
                        title = nextSib.nextSibling.firstChild.nodeValue
                        while nextSib.firstChild == None or nextSib.firstChild.nodeValue != "Artist":
                            nextSib = nextSib.nextSibling
                        artist = nextSib.nextSibling.firstChild.nodeValue
                        song = Song(ID, title, artist)
                        playlist.append(song)
                    
                    elif x.firstChild != None and x.firstChild.nodeValue == "Playlists":
                        nodes = [node for node in  x.nextSibling.nextSibling.getElementsByTagName("key") if node.firstChild.nodeValue == "Track ID"]

                        for y in nodes:
                            order[number] =  y.nextSibling.firstChild.nodeValue
                            number+=1
        
    def addNewSong(): pass

    def deleteSong(): pass

    def clearSongList(): pass
    
    def moveSongUp(): pass

    def pushButtonMoveDown(): pass

    def closeApp():
        QApplication.exit(1)



#table entry with the form of qprograssbar 

class QProgressbarTableItem(QTableItem, QProgressbar):
    
    #paint the progressbar in the cell geometry
    def paintEvent(): pass

    #takes care of resizing.
    def resizeEvent(): pass



#plot bars
class barHistogram(Qwt.QwtPlotCurve):
    
    def __init__(self, penColor=Qt.Qt.black, brushColor=Qt.Qt.white):
        Qwt.QwtPlotCurve.__init__(self)
        self.penColor = penColor
        self.brushColor = brushColor
    
    
    def drawFromTo(self, painter, xMap, yMap, start, stop):
        """Draws rectangles with the corners taken from the x- and y-arrays.
        """

        painter.setPen(Qt.QPen(self.penColor, 2))
        painter.setBrush(self.brushColor)
        if stop == -1:
            stop = self.dataSize()
        # force 'start' and 'stop' to be even and positive
        if start & 1:
            start -= 1
        if stop & 1:
            stop -= 1
        start = max(start, 0)
        stop = max(stop, 0)
        for i in range(start, stop, 2):
            px1 = xMap.transform(self.x(i))
            py1 = yMap.transform(self.y(i))
            px2 = xMap.transform(self.x(i+1))
            py2 = yMap.transform(self.y(i+1))
            painter.drawRect(px1, py1, (px2 - px1), (py2 - py1))


    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = DjServer()
    gui.show()
    app.exec_()
