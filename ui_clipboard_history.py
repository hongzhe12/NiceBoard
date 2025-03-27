# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clipboard_history.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_SimpleClipboardHistory(object):
    def setupUi(self, SimpleClipboardHistory):
        if not SimpleClipboardHistory.objectName():
            SimpleClipboardHistory.setObjectName(u"SimpleClipboardHistory")
        SimpleClipboardHistory.resize(300, 400)
        SimpleClipboardHistory.setMinimumSize(QSize(300, 400))
        SimpleClipboardHistory.setMaximumSize(QSize(300, 400))
        self.centralwidget = QWidget(SimpleClipboardHistory)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.history_list = QListWidget(self.centralwidget)
        self.history_list.setObjectName(u"history_list")

        self.verticalLayout.addWidget(self.history_list)

        self.toggle_btn = QPushButton(self.centralwidget)
        self.toggle_btn.setObjectName(u"toggle_btn")

        self.verticalLayout.addWidget(self.toggle_btn)

        SimpleClipboardHistory.setCentralWidget(self.centralwidget)

        self.retranslateUi(SimpleClipboardHistory)

        QMetaObject.connectSlotsByName(SimpleClipboardHistory)
    # setupUi

    def retranslateUi(self, SimpleClipboardHistory):
        SimpleClipboardHistory.setWindowTitle(QCoreApplication.translate("SimpleClipboardHistory", u"\u526a\u8d34\u677f\u5386\u53f2\u8bb0\u5f55", None))
        self.toggle_btn.setText(QCoreApplication.translate("SimpleClipboardHistory", u"\u9690\u85cf\u7a97\u53e3", None))
    # retranslateUi

