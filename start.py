# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 21:05:12 2023

@author: User
"""
from PyQt6 import QtWidgets
from cwb_gov import MainWindow_controller
import sys

app = QtWidgets.QApplication(sys.argv)
window = MainWindow_controller()
window.show()
sys.exit(app.exec())    
