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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QSizePolicy, QWidget)

class Ui_SimpleClipboardHistory(object):
    def setupUi(self, SimpleClipboardHistory):
        if not SimpleClipboardHistory.objectName():
            SimpleClipboardHistory.setObjectName(u"SimpleClipboardHistory")
        SimpleClipboardHistory.resize(384, 536)
        SimpleClipboardHistory.setMinimumSize(QSize(0, 0))
        SimpleClipboardHistory.setMaximumSize(QSize(16777215, 16777215))
        SimpleClipboardHistory.setStyleSheet(u"/* ===== \u4e3b\u7a97\u53e3 ===== */\n"
"SimpleClipboardHistory {\n"
"    background: #f0f2f5;\n"
"    border-radius: 10px;\n"
"    border: 1px solid #d5e3ff;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"/* ===== \u641c\u7d22\u6846 (QQ9\u8f93\u5165\u6846\u98ce\u683c) ===== */\n"
"QLineEdit#search_box {\n"
"    border: 1px solid #cce0ff;\n"
"    border-radius: 6px;\n"
"    padding: 8px 12px 8px 32px;  /* \u5de6\u4fa7\u7559\u51fa\u56fe\u6807\u7a7a\u95f4 */\n"
"    margin: 6px;\n"
"    font-size: 13px;\n"
"    background: white url(:/icons/search.svg) no-repeat 10px center;\n"
"    selection-background-color: #b3d7ff;\n"
"    color: #333;\n"
"}\n"
"\n"
"QLineEdit#search_box:focus {\n"
"    border: 1px solid #66a3ff;\n"
"    background-color: #f5f9ff;\n"
"}\n"
"\n"
"/* ===== \u5386\u53f2\u5217\u8868 (QQ9\u5361\u7247\u98ce\u683c) ===== */\n"
"QListWidget#history_list {\n"
"    background: white;\n"
"    border: 1px solid #d5e3ff;\n"
"    border-radius: 8px;\n"
"    padding: 2px;\n"
"    margin: 0 6px 6px 6px;\n"
"    outli"
                        "ne: none;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"/* \u5217\u8868\u9879 */\n"
"QListWidget#history_list::item {\n"
"    height: 36px;\n"
"    padding: 8px 12px;\n"
"    border-bottom: 1px solid #ebf1ff;\n"
"    color: #333;\n"
"}\n"
"\n"
"/* \u60ac\u505c\u6548\u679c */\n"
"QListWidget#history_list::item:hover {\n"
"    background: #f0f7ff;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u6548\u679c */\n"
"QListWidget#history_list::item:selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                              stop:0 #d9ecff, stop:1 #c4e1ff);\n"
"    color: #0066cc;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* ===== QQ9\u7ecf\u5178\u6309\u94ae ===== */\n"
"QPushButton#toggle_btn {\n"
"    /* \u57fa\u7840\u6837\u5f0f */\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                              stop:0 #4facfe, stop:1 #00b2ff);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 10px;\n"
"    margin: 6px;\n"
"    font"
                        "-size: 13px;\n"
"    font-weight: bold;\n"
"    min-height: 36px;\n"
"    \n"
"    /* QQ9\u7acb\u4f53\u6548\u679c */\n"
"    border-top: 1px solid rgba(255,255,255,0.5);\n"
"    border-bottom: 1px solid rgba(0,0,0,0.1);\n"
"    text-shadow: 0 1px 1px rgba(0,0,0,0.2);\n"
"}\n"
"\n"
"/* \u60ac\u505c\u6548\u679c */\n"
"QPushButton#toggle_btn:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                              stop:0 #5fb8ff, stop:1 #00bfff);\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u6548\u679c */\n"
"QPushButton#toggle_btn:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                              stop:0 #3a9df4, stop:1 #0099e6);\n"
"    padding-top: 11px;\n"
"    padding-bottom: 9px;\n"
"    border-top: 1px solid rgba(0,0,0,0.1);\n"
"}\n"
"\n"
"/* ===== \u6eda\u52a8\u6761 (QQ9\u8f7b\u91cf\u98ce\u683c) ===== */\n"
"QScrollBar:vertical {\n"
"    width: 8px;\n"
"    background: transparent;\n"
"    border-left: 1px solid #e1e8f0;\n"
"}\n"
"\n"
"QScrollBar::handle:v"
                        "ertical {\n"
"    background: #c1d9ff;\n"
"    border-radius: 3px;\n"
"    min-height: 30px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #a8c8ff;\n"
"}")
        self.centralwidget = QWidget(SimpleClipboardHistory)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.search_box = QLineEdit(self.centralwidget)
        self.search_box.setObjectName(u"search_box")
        self.search_box.setStyleSheet(u"")

        self.gridLayout.addWidget(self.search_box, 0, 0, 1, 1)

        self.history_list = QListWidget(self.centralwidget)
        self.history_list.setObjectName(u"history_list")

        self.gridLayout.addWidget(self.history_list, 1, 0, 1, 1)

        SimpleClipboardHistory.setCentralWidget(self.centralwidget)

        self.retranslateUi(SimpleClipboardHistory)

        QMetaObject.connectSlotsByName(SimpleClipboardHistory)
    # setupUi

    def retranslateUi(self, SimpleClipboardHistory):
        SimpleClipboardHistory.setWindowTitle(QCoreApplication.translate("SimpleClipboardHistory", u"\u526a\u8d34\u677f\u5386\u53f2\u8bb0\u5f55", None))
        self.search_box.setPlaceholderText(QCoreApplication.translate("SimpleClipboardHistory", u"\u641c\u7d22\u526a\u8d34\u677f\u5386\u53f2...", None))
    # retranslateUi

