
from PySide.QtCore import QAbstractListModel, QModelIndex, Qt

class TreeModel(QAbstractListModel):

    def __init__(self, items):
        super(TreeModel, self).__init__()

        self.items = items

    def rowCount(self, index=QModelIndex()):
        return len(self.items)

    def data(self, index, role):

        if role == Qt.DisplayRole:
            return self.items[index.row()]

    @staticmethod
    def from_text(text):
        return TreeModel(text.split('\n'))
