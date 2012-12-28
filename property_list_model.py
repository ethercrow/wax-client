
from PySide.QtCore import QAbstractListModel, QModelIndex, Qt

class PropertyListModel(QAbstractListModel):

    def __init__(self, itemdict):
        super(PropertyListModel, self).__init__()
        self.itemdict = itemdict

    def rowCount(self, index=QModelIndex()):
        return len(self.itemdict)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            item = self.items.items()[index.row()]
            return "{}: {}".format(item['key'], item['value'])

    @staticmethod
    def from_dict(d):
        return PropertyListModel(d)
