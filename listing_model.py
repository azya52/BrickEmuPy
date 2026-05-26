from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt

class ListingModel(QtCore.QAbstractTableModel):
    def __init__(self, data, breakpoints, mask="%X"):
        super().__init__()
        self._pc = -1
        self._data = data
        self._breakpoints = breakpoints
        self._mask = mask
        self._dataSize = len(data)
        self._addr_color = QtGui.QBrush(QtGui.QColor(128, 128, 128))

    def rowCount(self, parent=None):
        return self._dataSize

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                col = index.column()
                if col == 0:
                    return self._mask % index.row()
                data = self._data[index.row()]
                if (data):
                    return data[col - 1]

            if role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
                if self._breakpoints and index.row() in self._breakpoints:
                    return Qt.CheckState.Checked
                return Qt.CheckState.Unchecked

            if role == Qt.ItemDataRole.ForegroundRole and index.column() == 0:
                return self._addr_color

        return None

    def getPC(self):
        return self._pc

    def setPC(self, pc):
        self._pc = pc

    def flags(self, index):
        if index.column() == 0:
            return (
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsUserCheckable
            )
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def isBreakpoint(self, row):
        return row in self._breakpoints
    
    def setData(self, index, value, role):
        if index.column() == 0 and role == Qt.ItemDataRole.CheckStateRole:
            if Qt.CheckState(value) == Qt.CheckState.Checked:
                self._breakpoints.append(index.row())
            else:
                self._breakpoints.remove(index.row())
            self.dataChanged.emit(index, index)
            return True
        
        return False

    def updateData(self, data):
        self.beginResetModel()
        self._data = data
        self._dataSize = len(data)
        self.endResetModel()