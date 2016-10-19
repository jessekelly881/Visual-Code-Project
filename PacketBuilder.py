from PyQt4 import QtGui, QtCore
import sys
from scapy.all import *
from collections import namedtuple
from CodeObject import CodeObject, Node, In, Out, node_color
from CodeBlock import CodeBlock


#Send Pacet
#Packet Capture
#Display packet
	
class Packet(CodeBlock):
	def __init__(self, scene):
		super(Packet,self).__init__(scene)

		self.setTitle("Packet")
		self.setSize(125,150)

		packet_menu = QtGui.QMenu()
		create = QtGui.QMenu("Create")
		create.addAction("Send Packet")
		packet_menu.addMenu(create)

		self.addNodes([
			Node('src ip', QtCore.Qt.red, In, "Source IP Address(0-255)", None),
			Node('dst ip', QtCore.Qt.red, In, "Destination IP Address(0-255)", None),
			Node('src port', QtCore.Qt.blue, In, "", None),
			Node('dst port', QtCore.Qt.blue, In, "", None),
			Node('ttl', QtCore.Qt.yellow, In, "", None),
			Node('flags', QtCore.Qt.black, In, "", None),
			Node('packet', QtCore.Qt.green, Out, "", packet_menu)
			])

	def showWidgetEvent(self, event):
		w = PacketWidget()
		w.move(event.screenPos())
		w.show()



class PacketWidget(QtGui.QMainWindow):
	def __init__(self):
		super(PacketWidget, self).__init__()
		self.setCentralWidget(PacketTable(self))
		self.resize(820,300)


HeaderItem = namedtuple('HeaderItem', ['name', 'bits', 'default', 'dialog'])

class PacketTable(QtGui.QTableWidget):
	def __init__(self, parent = None):
		super(PacketTable, self).__init__(parent)
		self.resize(820,300)
		self.setRowCount(0)
		self.setColumnCount(32)
		self.setHorizontalHeaderLabels(QtCore.QString(';'.join(str(x) for x in range(0,32))).split(";"))

		self.cellDoubleClicked.connect(self.handleDoubleClicked)

		for i in range(32): self.setColumnWidth(i,25)

		self._currentBit = 0
		self._dialogTable = []   #(item, widget)
		self.protocolStack = []

		self.addICMPHeader()
		self.addIPv4Header()
		#self.addTCPHeader()
		#checkbox = QtGui.QCheckBox('S')
		#self.setCellWidget(0,0,checkbox)

		print hexdump(self.generatePacket())

		self.setVerticalHeaderLabels(QtCore.QString(';'.join(str(4*x) for x in range(0,self.rowCount()))).split(";"))

	def handleDoubleClicked(self, row, column): 
		item = self.item(row, column)
		dialog = self._lookupItemDialog(item)

		if dialog != None: 
			dialogOutput = dialog()
			

	def _lookupItemDialog(self, item):
		dialog = None
		for (i,d) in self._dialogTable: 
			if item == i: 
				dialog = d
				break

		return dialog

	def updateItemValue(self, item):
		pass

	def generatePacket(self): 
		layers = len(self.protocolStack)
		if layers > 0:
			packet = self.protocolStack[0]
			for i in range(1,layers): 
				packet = packet/self.protocolStack[i]

		else: packet = None

		return packet


	#Make cells readonly
	def edit(self, a, b, c): return 0

	#Should be used over _addItem
	def appendItem(self, headerItem): 
		assert isinstance(headerItem,HeaderItem), 'ASSERT: argument to PacketTable.appendItem is not an instance of HeaderItem'

		row = self._currentBit / 32
		if self.rowCount() < row + 1: self.insertRow(row)

		startBit = self._currentBit % 32
		item = self._addItem(headerItem.name,row,startBit,headerItem.bits,headerItem.default)

		self._dialogTable.append((item, headerItem.dialog))

		self._currentBit += headerItem.bits

	def _addItem(self, name, startRow, startBit, bits, value): 
		
		#Needs the ability to span several rows

		self.setSpan(startRow,startBit, 1, bits)

		item = QtGui.QTableWidgetItem(name + "(" + str(value) + ")")
		self.setItem(startRow, startBit, item)
		item.setTextAlignment(QtCore.Qt.AlignCenter)

		return item



	def addIPv4Header(self): 

		ip = IP()

		self.appendItem(  HeaderItem('Version',4,4, None)  				)
		self.appendItem(  HeaderItem('IHL',4,ip.ihl,None)  				)
		self.appendItem(  HeaderItem('DSCP',6,None, None)  				)
		self.appendItem(  HeaderItem('ECN',2,None, None)   				)
		self.appendItem(  HeaderItem('Total Length',16,ip.len,None)   	)

		self.appendItem(  HeaderItem('ID',16,ip.id,None)   				)
		self.appendItem(  HeaderItem('Flags',3,ip.flags, None)   		)
		self.appendItem(  HeaderItem('Frag Offset',13,ip.frag,None) 	)

		self.appendItem(  HeaderItem('TTL',8,ip.ttl,None)   			)
		self.appendItem(  HeaderItem('Protocal',8,ip.proto,None) 		)
		#self.appendItem('Checksum',16,ip.chksum)

		#self.appendItem('Source IP',32,ip.src)
		#self.appendItem('Destination IP',32,ip.dst)
		#self.appendItem('Options',32,None)

		self.protocolStack.append(ip)

	def addTCPHeader(self):
		tcp = TCP()
		
		'''
		self.appendItem('Source Port',16,tcp.seq)
		self.appendItem('Destination Port',16,tcp.dport)

		self.appendItem('Sequence Number',32,tcp.sport)

		self.appendItem('Data Offset',4,tcp.dataofs)
		self.appendItem('Reserved',3,tcp.reserved)
		self.appendItem('Flags',9,tcp.flags)
		self.appendItem('Window Size',16,tcp.window)

		self.appendItem('Checksum',16,tcp.chksum)
		self.appendItem('Urgent Pointer',16,tcp.urgptr)

		self.appendItem('Options',32,None)
		'''

		self.protocolStack.append(tcp)


	def addICMPHeader(self):
		icmp = ICMP()

		'''
		self.appendItem('Type',8,icmp.type)
		self.appendItem('Code',8,icmp.code)
		self.appendItem('Checksum',16,icmp.chksum)

		self.appendItem('Rest of Header',32,None)
		'''

		self.protocolStack.append(icmp)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	table = PacketTable()




	#tb = QtGui.QTextEdit(parent)
	#tb.setReadOnly(True)
	#tb.setText()


	table.show()
	app.exec_()
