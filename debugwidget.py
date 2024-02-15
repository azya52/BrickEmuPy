from PyQt6 import uic, QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QByteArray
import time

class DebugWidget(QtWidgets.QWidget):
    editStateSignal = pyqtSignal(dict)
    debugRunSignal = pyqtSignal()
    debugStopSignal = pyqtSignal()
    debugPauseSignal = pyqtSignal()
    debugStepSignal = pyqtSignal()

    def __init__(self, core_name, breakpoints):
        super().__init__()
        try:
            uic.loadUi("ui/" + core_name + ".ui", self)
        except Exception as e:
            print(str(e))

        self._breakpoints = breakpoints
        self._examineMap = {}
        self.prepareWidgetMap()
    
    def showEvent(self, event):
        for tableView in self.findChildren(QtWidgets.QTableWidget):
            tableView.resizeRowsToContents()
            tableView.resizeColumnsToContents()
        super().showEvent(event)

    def closeEvent(self, event):
        self.editStateSignal.disconnect()
        self.debugRunSignal.disconnect()
        self.debugStopSignal.disconnect()
        self.debugPauseSignal.disconnect()
        self.debugStepSignal.disconnect()
        super().closeEvent(event)

    def prepareWidgetMap(self):
        for widget in self.findChildren((QtWidgets.QLineEdit, QtWidgets.QCheckBox, QtWidgets.QTableView)):
            key = widget.property("key")
            if (key):
                self._examineMap[key] = (widget, widget.property("type"), widget.property("mask"))

    @pyqtSlot()
    def lineEditFinished(self):
        self.sender().clearFocus()
        try:
            self.editStateSignal.emit({self.sender().property("key"): int(self.sender().text(), 0)})
        except ValueError:
            pass

    @pyqtSlot(QtWidgets.QTableWidgetItem)
    def tableItemChanged(self, item):
        try:
            self.editStateSignal.emit({self.sender().property("key"): {item.row() * self.sender().columnCount() + item.column(): int(item.text(), 0)}})
        except ValueError:
            pass

    @pyqtSlot(QtWidgets.QTableWidgetItem)
    def listingTableChanged(self, item):
        if (item.column() == 1):
            try:
                self.editStateSignal.emit(
                    {"MEMORY": [item.row() * 2, int(item.text(), 0)]}
                )
            except ValueError:
                pass
        else:
            self.editStateSignal.emit({"BRKPT": (item.row(), item.checkState() == Qt.CheckState.Checked)})

    @pyqtSlot()
    def refrashStateSignal(self):
        self.editStateSignal.emit({})

    @pyqtSlot(int)
    def checkBoxStateChanged(self, state):
        self.editStateSignal.emit({self.sender().property("key"): int(state == Qt.CheckState.Checked.value)})

    def examine(self, state):
        if not self.isHidden():
            for key, value in state.items():
                if key in self._examineMap:
                    widget, datatype, mask = self._examineMap[key]
                    if (datatype == "integer" and not widget.hasFocus()):
                        widget.setText(mask % value)
                    elif (datatype == "boolean"):
                        widget.blockSignals(True)
                        widget.setChecked(value)
                        widget.blockSignals(False)
                    elif (datatype == "table" and widget.state() != QtWidgets.QAbstractItemView.State.EditingState and widget.isVisible()):
                        widget.blockSignals(True)
                        cols = widget.columnCount()
                        for i, value in enumerate(value):
                            widget.item(i // cols, i % cols).setText(mask % value)
                        widget.blockSignals(False)
                    elif (datatype == "listing" and widget.state() != QtWidgets.QAbstractItemView.State.EditingState):
                        widget.blockSignals(True)
                        widget.clear()
                        widget.clearContents()
                        widget.setRowCount(1)
                        
                        itemAdr = QtWidgets.QTableWidgetItem()
                        itemAdr.setForeground(QtGui.QBrush(QtGui.QColor(128, 128, 128)))
                        itemAdr.setFlags(itemAdr.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                        itemAdr.setCheckState(Qt.CheckState.Unchecked)

                        for i, instr in enumerate(value):
                            item = itemAdr.clone()
                            if (i in self._breakpoints):
                                item.setCheckState(Qt.CheckState.Checked)
                            item.setText('0x%0.4X:' % i)
                            widget.setItem(i, 0, item)
                            itemOpcode = QtWidgets.QTableWidgetItem(' %0.2X ' % instr[0])
                            itemOpcode.setFlags(itemOpcode.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                            widget.setItem(i, 1, itemOpcode)
                            itemAsm = QtWidgets.QTableWidgetItem(instr[1])
                            itemAsm.setFlags(itemAsm.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                            widget.setItem(i, 2, itemAsm)
                            if (i == 0):
                                widget.resizeRowsToContents()
                                widget.resizeColumnsToContents()
                                widget.setRowCount(len(value))
                        widget.blockSignals(False)

            if ("PC" in state and "LISTING" in self._examineMap):
                widget = self._examineMap["LISTING"][0]
                widget.selectRow(state["PC"])