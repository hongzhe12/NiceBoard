# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clipboard_history.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QSizePolicy, QWidget)

class Ui_SimpleClipboardHistory(object):
    def setupUi(self, SimpleClipboardHistory):
        if not SimpleClipboardHistory.objectName():
            SimpleClipboardHistory.setObjectName(u"SimpleClipboardHistory")
        SimpleClipboardHistory.resize(300, 393)
        SimpleClipboardHistory.setMinimumSize(QSize(0, 0))
        SimpleClipboardHistory.setMaximumSize(QSize(16777215, 16777215))
        SimpleClipboardHistory.setStyleSheet(u"/* ===== \u5168\u5c40\u57fa\u7840\u6837\u5f0f ===== */\n"
"SimpleClipboardHistory,\n"
"QWidget#centralwidget {\n"
"    background-color: white;\n"
"    font-family: \"Microsoft YaHei\";\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* ===== \u5217\u8868\u63a7\u4ef6 ===== */\n"
"QListWidget#history_list {\n"
"    background-color: white;\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 8px;\n"
"    padding: 2px;\n"
"    margin: 6px;\n"
"    font-size: 14px;\n"
"    outline: 0;\n"
"}\n"
"\n"
"QListWidget#history_list::item {\n"
"    height: 36px;\n"
"    padding: 8px 12px;\n"
"    border-bottom: 1px solid #f0f0f0;\n"
"}\n"
"\n"
"QListWidget#history_list::item:hover {\n"
"    background-color: #f5f5f5;\n"
"}\n"
"\n"
"QListWidget#history_list::item:selected {\n"
"    background-color: #e8f5e9;\n"
"    color: #2e7d32;\n"
"}\n"
"\n"
"/* ===== \u641c\u7d22\u6846 ===== */\n"
"QLineEdit#search_box {\n"
"    background-color: white;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 6px;\n"
"    padding: 8px 12"
                        "px;\n"
"    margin: 6px;\n"
"    font-size: 14px;\n"
"    selection-background-color: #c8e6c9;\n"
"}\n"
"\n"
"QLineEdit#search_box:focus {\n"
"    border: 1px solid #4CAF50;\n"
"}\n"
"\n"
"/* ===== \u64cd\u4f5c\u6309\u94ae ===== */\n"
"QPushButton#toggle_btn {\n"
"    background-color: #4CAF50;\n"
"    border: none;\n"
"    color: white;\n"
"    padding: 10px;\n"
"    margin: 6px;\n"
"    border-radius: 6px;\n"
"    font-size: 14px;\n"
"    min-height: 36px;\n"
"}\n"
"\n"
"QPushButton#toggle_btn:hover {\n"
"    background-color: #43a047;\n"
"}\n"
"\n"
"QPushButton#toggle_btn:pressed {\n"
"    background-color: #388e3c;\n"
"}\n"
"\n"
"QPushButton#btn_delete {\n"
"    background-color: #ef5350;\n"
"    border: none;\n"
"    color: white;\n"
"    padding: 10px;\n"
"    margin: 6px;\n"
"    border-radius: 6px;\n"
"    font-size: 14px;\n"
"    min-height: 36px;\n"
"}\n"
"\n"
"QPushButton#btn_delete:hover {\n"
"    background-color: #e53935;\n"
"}\n"
"\n"
"QPushButton#btn_delete:pressed {\n"
"    background-color: #"
                        "d32f2f;\n"
"}\n"
"\n"
"/* ===== \u53f3\u952e\u83dc\u5355 ===== */\n"
"QMenu {\n"
"    background-color: white;\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    padding: 8px 24px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    background-color: #e8f5e9;\n"
"    color: #2e7d32;\n"
"}\n"
"\n"
"/* ===== \u6eda\u52a8\u6761\u4f18\u5316 ===== */\n"
"QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #bdbdbd;\n"
"    border-radius: 4px;\n"
"    min-height: 30px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #9e9e9e;\n"
"}")
        self.centralwidget = QWidget(SimpleClipboardHistory)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.history_list = QListWidget(self.centralwidget)
        self.history_list.setObjectName(u"history_list")
        self.history_list.setStyleSheet(u"margin:5 10px;")

        self.gridLayout.addWidget(self.history_list, 1, 0, 1, 1)

        self.search_box = QLineEdit(self.centralwidget)
        self.search_box.setObjectName(u"search_box")
        self.search_box.setStyleSheet(u"margin:15 10;")

        self.gridLayout.addWidget(self.search_box, 0, 0, 1, 1)

        SimpleClipboardHistory.setCentralWidget(self.centralwidget)

        self.retranslateUi(SimpleClipboardHistory)

        QMetaObject.connectSlotsByName(SimpleClipboardHistory)
    # setupUi

    def retranslateUi(self, SimpleClipboardHistory):
        SimpleClipboardHistory.setWindowTitle(QCoreApplication.translate("SimpleClipboardHistory", u"\u526a\u8d34\u677f\u5386\u53f2\u8bb0\u5f55", None))
        self.search_box.setPlaceholderText(QCoreApplication.translate("SimpleClipboardHistory", u"\u641c\u7d22\u526a\u8d34\u677f\u5386\u53f2...", None))
    # retranslateUi

