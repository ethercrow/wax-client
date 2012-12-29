
from PySide.QtCore import QUrl, QTimer
from PySide.QtDeclarative import QDeclarativeView

import messages as M
import Queue as Q
from tree_model import TreeModel
from property_list_model import PropertyListModel

class MainWindow(QDeclarativeView):

    def __init__(self, gui_queue, worker_queue, parent=None):

        super(MainWindow, self).__init__(parent)

        self.queue = gui_queue
        self.worker_queue = worker_queue
        self.setWindowTitle('Main Window')

        self.setSource(QUrl.fromLocalFile('main.qml'))

        self.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(30)

    def on_timer(self):
        try:
            msg = self.queue.get_nowait()
            self.handle_message(msg)
        except Q.Empty:
            pass

    def handle_message(self, msg):
        assert(isinstance(msg, M.GuiMessage))

        if msg.kind == M.GuiMessage.HIERARCHY:
            self.treeModel = TreeModel(msg.payload)
            self.rootContext().setContextProperty("treeModel", self.treeModel)
        elif msg.kind == M.GuiMessage.PROPERTY:
            self.currentViewProperties.update(msg.payload)
            self.propertyListModel = PropertyListModel.from_dict(
                self.currentViewProperties)
        else:
            assert(False)
