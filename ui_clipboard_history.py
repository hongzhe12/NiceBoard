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
        SimpleClipboardHistory.resize(300, 400)
        SimpleClipboardHistory.setMinimumSize(QSize(0, 0))
        SimpleClipboardHistory.setMaximumSize(QSize(16777215, 16777215))
        SimpleClipboardHistory.setStyleSheet(u"/* \u4e3b\u7a97\u53e3\u6837\u5f0f - Windows 11 \u4e9a\u514b\u529b\u6548\u679c */\n"
"SimpleClipboardHistory {\n"
"    background: rgba(243, 243, 243, 0.85);  /* \u534a\u900f\u660e\u80cc\u666f */\n"
"    border-radius: 8px;\n"
"    border: 1px solid rgba(255, 255, 255, 0.2);\n"
"    padding: 0;\n"
"    \n"
"    /* \u4e9a\u514b\u529b\u6a21\u7cca\u6548\u679c (\u9700\u8981\u4ee3\u7801\u4e2d\u542f\u7528) */\n"
"    backdrop-filter: blur(12px);\n"
"    -webkit-backdrop-filter: blur(12px);\n"
"}\n"
"\n"
"/* \u6807\u9898\u680f\u6837\u5f0f */\n"
"QWidget#header {\n"
"    height: 40px;\n"
"    background: transparent;\n"
"    border-top-left-radius: 8px;\n"
"    border-top-right-radius: 8px;\n"
"    padding-left: 12px;\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.05);\n"
"}\n"
"\n"
"/* \u6807\u9898\u6587\u672c */\n"
"QLabel#title_label {\n"
"    font-family: \"Segoe UI Variable Display\", sans-serif;\n"
"    font-size: 14px;\n"
"    font-weight: 600;\n"
"    color: #000000;\n"
"}\n"
"\n"
"/* \u641c\u7d22\u6846 - Win"
                        "dows 11 \u98ce\u683c */\n"
"QLineEdit#search_box {\n"
"    border: 1px solid rgba(0, 0, 0, 0.1);\n"
"    border-radius: 4px;\n"
"    padding: 8px 12px 8px 36px;\n"
"    margin: 12px;\n"
"    font-size: 14px;\n"
"    background: white url(:/icons/search.svg) no-repeat 12px center;\n"
"    background-color: rgba(255, 255, 255, 0.7);\n"
"    color: #000000;\n"
"    selection-background-color: #0078D4;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QLineEdit#search_box:focus {\n"
"    border: 1px solid #0078D4;\n"
"    background-color: rgba(255, 255, 255, 0.9);\n"
"}\n"
"\n"
"/* \u5386\u53f2\u5217\u8868 - \u4e9a\u514b\u529b\u5361\u7247\u6548\u679c */\n"
"QListWidget#history_list {\n"
"    background: transparent;\n"
"    border: none;\n"
"    padding: 0 12px 12px 12px;\n"
"    outline: none;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"/* \u5217\u8868\u9879 - Windows 11 \u5361\u7247\u6837\u5f0f */\n"
"QListWidget#history_list::item {\n"
"    height: 48px;\n"
"    padding: 8px 12px;\n"
"    margin-bottom: 8px;\n"
"    "
                        "background: rgba(255, 255, 255, 0.6);\n"
"    border-radius: 4px;\n"
"    border: 1px solid rgba(0, 0, 0, 0.05);\n"
"    color: #000000;\n"
"}\n"
"\n"
"/* \u60ac\u505c\u6548\u679c */\n"
"QListWidget#history_list::item:hover {\n"
"    background: rgba(255, 255, 255, 0.8);\n"
"    border: 1px solid rgba(0, 0, 0, 0.1);\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u6548\u679c */\n"
"QListWidget#history_list::item:selected {\n"
"    background: rgba(0, 120, 212, 0.2);\n"
"    border: 1px solid rgba(0, 120, 212, 0.3);\n"
"}\n"
"\n"
"/* \u6309\u94ae - Windows 11 \u98ce\u683c */\n"
"QPushButton#toggle_btn {\n"
"    background: rgba(0, 120, 212, 0.9);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 8px 16px;\n"
"    margin: 0 12px 12px 12px;\n"
"    font-family: \"Segoe UI Variable Text\", sans-serif;\n"
"    font-size: 14px;\n"
"    min-height: 32px;\n"
"}\n"
"\n"
"/* \u60ac\u505c\u6548\u679c */\n"
"QPushButton#toggle_btn:hover {\n"
"    background: rgba(0, 120, 212, 1.0);\n"
"}\n"
"\n"
"/* "
                        "\u6309\u4e0b\u6548\u679c */\n"
"QPushButton#toggle_btn:pressed {\n"
"    background: rgba(0, 90, 158, 0.9);\n"
"}\n"
"\n"
"/* \u6eda\u52a8\u6761 - Windows 11 \u98ce\u683c */\n"
"QScrollBar:vertical {\n"
"    width: 8px;\n"
"    background: transparent;\n"
"    margin-right: 2px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgba(0, 0, 0, 0.2);\n"
"    border-radius: 4px;\n"
"    min-height: 30px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: rgba(0, 0, 0, 0.3);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0;\n"
"    background: none;\n"
"}\n"
"\n"
"/* \u7a97\u53e3\u9634\u5f71\u6548\u679c (\u9700\u8981\u5728\u4ee3\u7801\u4e2d\u5b9e\u73b0) */\n"
"QGraphicsEffect#window_shadow {\n"
"    color: rgba(0, 0, 0, 0.1);\n"
"    blur-radius: 16px;\n"
"    offset: 0 4px;\n"
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

