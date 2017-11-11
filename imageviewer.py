#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from PyQt4 import QtCore, QtGui
import json
import sys


class ImageViewer(QtGui.QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.ap_cur = None
        self.ap_list = []

        self.printer = QtGui.QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.mousePressEvent = self.onClick

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)

    def open_image(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())
        if fileName:
            self.image = QtGui.QImage(fileName)
            if self.image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
            self.scaleFactor = 1.0

            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def open_ap_list(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())
        if fileName:
            try:
                self.ap_list = json.load(open(fileName))
                self.ap_list_filename = str(fileName)
            except Exception as e:
                print(e)
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load AP List %s." % fileName)
                return
            self.ap_cur = -1
            self.next()

    def save_ap_list(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save File",
                QtCore.QDir.currentPath(), "JSON (*.json)")
        if fileName:
            ap_loc_dict = {ap['name']: ap['loc'] for ap in self.ap_list if 'loc' in ap}
            try:
                json.dump(ap_loc_dict, open(fileName, 'w'))
            except Exception as e:
                print(e)
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot save AP List %s." % fileName)
                return

    def next(self):
        self.ap_cur += 1
        if len(self.ap_list) > self.ap_cur:
            print()
            sys.stdout.write("Please click for " + self.ap_list[self.ap_cur]['name']+": ")
            sys.stdout.flush()
        else:
            print('out of aps, please save data!')

    def find(self):
        search_string, ok = QtGui.QInputDialog.getText(
            self, "Search by AP name", "Search substring:")
        if not ok:
            return

        print("Searching for {!r}... ".format(search_string), end='')
        found_aps = [(i, ap) for i, ap in enumerate(self.ap_list)
                     if search_string.lower() in ap['name'].lower()]
        if len(found_aps) == 0:
            print('Nothing found.')
            return
        elif len(found_aps) > 1:
            print("{} APs matched ({})".format(
                len(found_aps), ', '.join([ap['name'] for i, ap in found_aps])))
            return
        else:
            self.ap_cur = found_aps[0][0]-1
            self.next()

    def back(self):
        self.ap_cur = max(self.ap_cur - 2, -1)
        print()
        self.next()

    def clear_loc(self):
        if self.ap_cur < len(self.ap_list):
            del self.ap_list[self.ap_cur]['loc']
        self.next()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def onClick(self, event):
        loc = (event.pos().x()/self.scaleFactor/self.image.width(),
               event.pos().y()/self.scaleFactor/self.image.height())
        print(loc)
        if self.ap_cur is not None:
            if self.ap_cur < len(self.ap_list):
                self.ap_list[self.ap_cur]['loc'] = list(loc)
            self.next()

    def about(self):
        QtGui.QMessageBox.about(self, "About Image Viewer",
                "<p>The <b>Image Viewer</b> example shows how to combine "
                "QLabel and QScrollArea to display an image. QLabel is "
                "typically used for displaying text, but it can also display "
                "an image. QScrollArea provides a scrolling view around "
                "another widget. If the child widget exceeds the size of the "
                "frame, QScrollArea automatically provides scroll bars.</p>"
                "<p>The example demonstrates how QLabel's ability to scale "
                "its contents (QLabel.scaledContents), and QScrollArea's "
                "ability to automatically resize its contents "
                "(QScrollArea.widgetResizable), can be used to implement "
                "zooming and scaling features.</p>")

    def createActions(self):
        self.openImageAct = QtGui.QAction("&Open Image...", self, shortcut="Ctrl+O",
                triggered=self.open_image)

        self.openAPListAct = QtGui.QAction("Open &AP List...", self, shortcut="Ctrl+L",
                triggered=self.open_ap_list)

        self.saveAPListAct = QtGui.QAction("&Save AP List...", self, shortcut="Ctrl+S",
                triggered=self.save_ap_list)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.nextAct = QtGui.QAction("&Next AP / Skip", self, shortcut="Ctrl+N",
                triggered=self.next)
        self.backAct = QtGui.QAction("Go &Back one AP", self, shortcut="Ctrl+B",
                triggered=self.back)
        self.findAct = QtGui.QAction("&Find AP by substring", self, shortcut="Ctrl+F",
                triggered=self.find)
        self.clearLocAct = QtGui.QAction("&Clear current AP location", self, shortcut="Ctrl+C",
                triggered=self.clear_loc)

        self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
                shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
                shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

        self.fitToWindowAct = QtGui.QAction("Fi&t to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+T",
                triggered=self.fitToWindow)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openImageAct)
        self.fileMenu.addAction(self.openAPListAct)
        self.fileMenu.addAction(self.saveAPListAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.apMenu = QtGui.QMenu("&APs", self)
        self.viewMenu.addAction(self.findAct)
        self.viewMenu.addAction(self.nextAct)
        self.viewMenu.addAction(self.backAct)
        self.viewMenu.addAction(self.clearLocAct)

        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 10.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.1)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
