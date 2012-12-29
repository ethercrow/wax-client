
import Queue as Q
import threading as T
import messages as M

import telnetlib
import re
from uiview_tree import UIViewTree

class WorkerThread(T.Thread):

    def __init__(self, worker_queue, gui_queue, host, port):
        super(WorkerThread, self).__init__()
        self.alive = T.Event()
        self.alive.set()
        self.queue = worker_queue
        self.gui_queue = gui_queue

        self.host = host
        self.port = port

    def run(self):

        self.conn = telnetlib.Telnet(self.host, self.port)

        self.read_reply()
        self.conn.write("window = UIApplication:sharedApplication():keyWindow()\n")
        self.read_reply()

        while self.alive.isSet():
            try:
                msg = self.queue.get(True, 0.03)
                self.handle_message(msg)
            except Q.Empty:
                pass

        self.conn.write('\x04')
        self.conn.close()

    def handle_message(self, msg):
        assert(isinstance(msg, M.CommMessage))

        if msg.kind == M.CommMessage.HIERARCHY:
            self.conn.write("window:recursiveDescription()\n")
            hier = self.read_reply()
            uitree = UIViewTree.from_recursive_description(hier)
            # print('remember_command = ' + self.make_remember_views_command(uitree))
            self.conn.write(self.make_remember_views_command(uitree))
            self.read_reply()
            self.gui_queue.put(M.GuiMessage(M.GuiMessage.HIERARCHY, uitree))
        elif msg.kind == M.CommMessage.PROPERTY:
            pass
        else:
            assert(False)

    def join(self, timeout=None):
        self.alive.clear()
        T.Thread.join(self, timeout)

    def read_reply(self):
        index, match, text = self.conn.expect(['\n> $'], 0.2)
        if not match:
            print("Unexpected reply {}".format(text))
            return None
        return text[:-3]

    def make_remember_views_command(self, uitree):

        def make_assignment(view):
            ptr = view['pointer']
            return 'v{} = {}'.format(ptr, ptr)

        assignments = (make_assignment(view) for view in uitree.to_list())

        result = '; '.join(assignments) + '\n'
        return result
