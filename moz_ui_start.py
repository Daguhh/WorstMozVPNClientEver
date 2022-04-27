#!/usr/bin/env python3

import sys
import subprocess
from PyQt5 import QtWidgets
import moz_commands as moz


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.resize(300, 460)

        self.is_moz_on = False
        dct = moz.status()

        self.centralwidget = QtWidgets.QTabWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        tab1 = QtWidgets.QWidget()
        self.centralwidget.addTab(tab1, 'Server')

        box = QtWidgets.QVBoxLayout()

        self.start_btn = QtWidgets.QPushButton('Start')
        self.start_btn.clicked.connect(self.toogle_moz)
        self.choose_server_btn = ChooseServerBtn(tab1)
        ip_wdg = IPStatus()
        server_status = StatusWdg(dct, 'Server')
        self.choose_server_btn.connect(server_status.update)
        self.choose_server_btn.connect(ip_wdg.update)

        box.addWidget(self.choose_server_btn)
        box.addWidget(self.start_btn)
        box.addWidget(server_status)
        box.addWidget(ip_wdg)
        box.addStretch()
        tab1.setLayout(box)

        tab2 = QtWidgets.QWidget()
        self.centralwidget.addTab(tab2, 'User')
        box = QtWidgets.QVBoxLayout()
        user_status = StatusWdg(dct, 'User')
        self.choose_server_btn.connect(user_status.update)
        box.addWidget(user_status)
        box.addStretch()
        tab2.setLayout(box)

        tab3 = QtWidgets.QWidget()
        self.centralwidget.addTab(tab3, 'Devices')
        box = QtWidgets.QVBoxLayout()
        device_status = DeviceStatusWdg(dct)
        self.choose_server_btn.connect(device_status.update)
        box.addWidget(device_status)
        box.addStretch()
        tab3.setLayout(box)

    def toogle_moz(self):

        if self.is_moz_on:
            moz.deactivate()
            self.start_btn.setText('Start')
        else:
            moz.activate()
            self.start_btn.setText('Stop')

        self.is_moz_on = not self.is_moz_on

        dct = moz.status()
        for update_fct in self.choose_server_btn.connections:
            update_fct(dct)


class ChooseServerBtn(QtWidgets.QToolButton):

    def __init__(self, parent):

        super().__init__(parent)

        self.connections = []

        self.setText('Servers')
        self.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)

        self.selected_server = None
        servers = moz.servers()

        menu = QtWidgets.QMenu()
        for country, cities_dct in servers.items():
            sub_menu = menu.addMenu(country)
            for city, server in cities_dct.items():
                sub_sub_menu = sub_menu.addMenu(city)
                for s in server:
                    action = sub_sub_menu.addAction(str(s))

        menu.triggered.connect(self.menu_pressed)

        self.setMenu(menu)

    def connect(self, callback):

        self.connections += [callback]

    def menu_pressed(self, action_str):

        self.selected_server = action_str.text()
        moz.select(self.selected_server)


class StatusWdg(QtWidgets.QFrame):

    def __init__(self, dct, kind):

        super().__init__()

        self.kind = kind

        box = QtWidgets.QGridLayout()
        self.dct={}

        for i, label in enumerate([k for k in dct.keys() if kind in k]):

            box.addWidget(QtWidgets.QLabel(label), i, 0)
            self.dct[label] = QtWidgets.QLabel(dct[label])
            box.addWidget(self.dct[label], i, 1)

        self.setLayout(box)

    def update(self, dct):

        for label in [k for k in dct.keys() if self.kind in k]:

            self.dct[label].setText(dct[label])

class DeviceStatusWdg(QtWidgets.QFrame):
    labels = ['Active devices', 'Current devices', 'Devices']

    def __init__(self, dct):

        super().__init__()

        box = QtWidgets.QGridLayout()
        self.dct={}

        for i, label in enumerate(DeviceStatusWdg.labels):

            box.addWidget(QtWidgets.QLabel(label), i, 0)
            self.dct[label] = QtWidgets.QLabel(dct[label])
            box.addWidget(self.dct[label], i , 1)

        self.setLayout(box)

    def update(self, dct):

        for label in DeviceStatusWdg.labels:

            self.dct[label].setText(dct[label])

class IPStatus(QtWidgets.QFrame):

    def __init__(self):

        super().__init__()

        box = QtWidgets.QVBoxLayout()
        self.lbl = QtWidgets.QLabel('---')
        box.addWidget(self.lbl)
        self.setLayout(box)

        self.update(None)

    def update(self, _):

        self.lbl.setText(subprocess.check_output('ip addr', shell=True).decode())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


