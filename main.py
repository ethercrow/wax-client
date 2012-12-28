#!/usr/bin/env python
# encoding: utf-8

import sys

from PySide.QtGui import QApplication

import Queue as Q

import window as W
import telnet_worker as TW

def main():

    worker_queue = Q.Queue()
    gui_queue = Q.Queue()
    
    app = QApplication(sys.argv)

    window = W.MainWindow(gui_queue, worker_queue)
    window.show()

    worker = TW.WorkerThread(worker_queue, gui_queue, sys.argv[1], sys.argv[2])
    worker.start()

    sys.exit(app.exec_())
    worker.join()

if __name__ == '__main__':
    main()
