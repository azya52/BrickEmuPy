from PyQt6 import uic, QtWidgets
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from listing_model import ListingModel

class DebugWidget(QtWidgets.QWidget):
    editStateSignal = pyqtSignal(dict)
    debugRunSignal = pyqtSignal()
    debugStopSignal = pyqtSignal()
    debugPauseSignal = pyqtSignal()
    debugStepSignal = pyqtSignal()

    def __init__(self, core_name, breakpoints):
        super().__init__()

        self._breakpoints = breakpoints
        self._examineMap = {}

        try:
            uic.loadUi("ui/" + core_name + ".ui", self)
        except Exception as e:
            QMessageBox(parent=self, text=str(e)).exec()
            self.close()

        self.prepareWidgetMap()

    def showEvent(self, event):
        for table in self.findChildren(QtWidgets.QTableWidget):
            self.prepareTable(table)
        super().showEvent(event)

    def prepareTable(self, tableView):
        tableView.blockSignals(True)

        tableView.resizeRowsToContents()
        tableView.resizeColumnsToContents()

        try:
            startIndex = int(tableView.property("start_index") or "0", 0)
        except ValueError:
            startIndex = 0

        rowCount = tableView.rowCount()
        colCount = tableView.columnCount()
        for row in range(rowCount):
            for col in range(colCount):
                tableView.item(row, col) or tableView.setItem(row, col, QTableWidgetItem(""))
            tableView.verticalHeaderItem(row) or tableView.setVerticalHeaderItem(row, QTableWidgetItem("%X" % (startIndex + (row * colCount))))

        tableView.blockSignals(False)

    def prepareWidgetMap(self):
        for widget in self.findChildren((QtWidgets.QLineEdit, QtWidgets.QCheckBox, QtWidgets.QTableView)):
            key = widget.property("key")
            if (key):
                self._examineMap[key] = (widget, widget.property("type"), widget.property("mask"))

    def str2int(self, value):
        try:
            return int(value, 0)
        except ValueError:
            return int(value, 16)

    @pyqtSlot()
    def lineEditFinished(self):
        self.sender().clearFocus()
        try:
            self.editStateSignal.emit({self.sender().property("key"): self.str2int(self.sender().text())})
        except ValueError:
            self.editStateSignal.emit({})

    @pyqtSlot(QtWidgets.QTableWidgetItem)
    def tableItemChanged(self, item):
        try:
            self.editStateSignal.emit({self.sender().property("key"): {
                    item.row() * self.sender().columnCount() + item.column(): self.str2int(item.text())
                }})
        except ValueError:
            self.editStateSignal.emit({})

    @pyqtSlot()
    def refrashStateSignal(self):
        self.editStateSignal.emit({})

    @pyqtSlot(int)
    def checkBoxStateChanged(self, state):
        self.editStateSignal.emit({self.sender().property("key"): int(state == Qt.CheckState.Checked.value)})

    @pyqtSlot(int)
    def comboBoxItemChanged(self, index):
        self.editStateSignal.emit({self.sender().property("key"): index})

    def _onListingEdit(self, index):
        if index.isValid():
            if index.column() == 0:
                self.editStateSignal.emit({
                    "BRKPT": (index.row(), index.model().isBreakpoint(index.row()))
                })

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
                    elif datatype == "listing":
                        if not hasattr(widget, "_model"):
                            widget._model = ListingModel(value, self._breakpoints, mask)
                            widget.setModel(widget._model)
                            header = widget.horizontalHeader()
                            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
                            widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                            widget._model.dataChanged.connect(
                                lambda topLeft, bottomRight: self._onListingEdit(topLeft)
                            )
                        else:
                            widget._model.updateData(value)

            if "PC" in state and "LISTING" in self._examineMap:
                view = self._examineMap["LISTING"][0]
                if (view):
                    model = view.model()
                    if (model):
                        if (model.getPC() != state["PC"]):
                            model.setPC(state["PC"])
                            index = model.index(state["PC"], 0)
                            view.selectionModel().setCurrentIndex(index, 
                                QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect | 
                                QtCore.QItemSelectionModel.SelectionFlag.Rows
                            )