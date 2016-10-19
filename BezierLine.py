from PyQt4.QtGui import QGraphicsItem, QPen
from PyQt4.QtCore import QRectF, Qt, QPointF, QPoint
import math


def binomial(n,k):
	"""n choose k"""
	if n-k <0: return 1
	else:
		return math.factorial(n) / float(
		math.factorial(k) * math.factorial(n - k))


def bernsteinPolynomial(x, n, k):
	return binomial(n,k) * (x ** k) * ((1 - x) ** (n - k))

def bezier(t, points):
    """Calculate coordinate of a point in the bezier curve"""
    n = len(points) - 1
    x = y = 0
    for k, pos in enumerate(points):
        bern = bernsteinPolynomial(t, n, k)
        x += pos.x() * bern
        y += pos.y() * bern
    return QPointF(x, y)

def bezierCurveRange(n, points):
    """Range of points in a curve bezier"""
    for i in xrange(n):
        t = i / float(n - 1)
        yield bezier(t, points)


class BezierLine(QGraphicsItem):
	def __init__(self, p1):
		super(BezierLine, self).__init__()
		self._p1 = p1
		self._p2 = p1
		self._color = Qt.black
		self._steps = 100 #Number of line segments that make up the curve


		self.setFlags(
			self.flags() | 
			QGraphicsItem.ItemIsMovable | 
			QGraphicsItem.ItemIsSelectable | 
			QGraphicsItem.ItemSendsGeometryChanges
			)

	def steps(self): return self._steps
	def setSteps(self, steps): self._steps = steps

	def color(self): return self._color
	def setColor(self, color): self._color = color

	def controlPoints(self):
		x1 = (self.p1().x() + self.p2().x()) / 2
		y1 = x1/2

		return (
            self.p1(), 
            QPointF(x1,y1), 
            QPointF(x1,-y1), 
            self.p2())


	def paint(self, painter, option, widget):
		
	#Set Pen#############################
		if self.isSelected(): 
			line_style = Qt.DashLine
			width = 2
			steps = 25
		else: 
			line_style = Qt.SolidLine
			width = 2
			steps = 125

		pen = QPen()
		pen.setWidth(width)
		pen.setColor(self._color)
		pen.setStyle(line_style)
		painter.setPen(pen)
		self.setSteps(steps)
	######################################
		
		#painter.drawLine(self.p1(),self.p2())
		
		
		control_points = self.controlPoints()
		oldPoint = control_points[0]
		for point in bezierCurveRange(self.steps(), control_points):
			painter.drawLine(self.mapToScene(oldPoint), self.mapToScene(point))
			oldPoint = point
		

	def boundingRect(self):
		return QRectF(self.p1(), self.p2())

	

	def setP1(self, p1): 
		self._p1 = self.mapFromScene(p1)

	def setP2(self, p2): 
		self._p2 = self.mapFromScene(p2)

	def p1(self): return self._p1
	def p2(self): return self._p2
