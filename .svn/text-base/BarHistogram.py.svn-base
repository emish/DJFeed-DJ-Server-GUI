
if False:
    import sip
    sip.settracemask(0x3f)


import random
import sys
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt


#plot bars
class BarHistogram(Qwt.QwtPlotCurve):
    
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

            
