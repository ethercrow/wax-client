
import Queue as Q
import threading as T
import messages as M

import telnetlib

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
        self.conn.write("window:recursiveDescription()\n")
        s = self.read_reply()
        self.gui_queue.put(M.GuiMessage(M.GuiMessage.HIERARCHY, s))

        while self.alive.isSet():
            try:
                command = self.queue.get(True, 0.03)
                print(command)
                self.conn.write(command + "\n")
                reply = self.read_reply()
                msg = M.GuiMessage(M.GuiMessage.HIERARCHY, reply)
                self.gui_queue.put(msg)
            except Q.Empty:
                pass

        self.conn.write('\x04')
        self.conn.close()

    def handle_message(self, msg):
        assert(isinstance(msg, M.GuiMessage))

        if msg.kind == M.CommMessage.HIERARCHY:
            self.conn.write("UIApplication:sharedApplication():keyWindow():recursiveDescription()\n")
            s = self.read_reply()
            self.gui_queue.put(M.GuiMessage(M.GuiMessage.HIERARCHY, s))
        elif msg.kind == M.CommMessage.PROPERTY:
            self.gui_queue.put(M.GuiMessage(M.GuiMessage.PROPERTY, s))
        else:
            assert(False)

    def join(self, timeout=None):
        self.alive.clear()
        T.Thread.join(self, timeout)

    def read_reply(self):
        index, match, text = self.conn.expect(['\n> $'], 0.2)
        print(index, match, text)
        if not match:
            print("Unexpected reply")
            return None
        return text[:-3]
