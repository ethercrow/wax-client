
from PySide.QtCore import QAbstractListModel, QModelIndex, Qt

class TreeModel(QAbstractListModel):

    def __init__(self, uitree):
        super(TreeModel, self).__init__()

        self.uitree = uitree

    def rowCount(self, index=QModelIndex()):
        return len(self.uitree.to_list())

    def data(self, index, role):

        if role == Qt.DisplayRole:
            return self.uitree.to_list()[index.row()]['pointer']
