# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_SettingsForm(object):
    def setupUi(self, SettingsForm):
        if not SettingsForm.objectName():
            SettingsForm.setObjectName(u"SettingsForm")
        SettingsForm.resize(286, 442)
        self.gridLayout = QGridLayout(SettingsForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelHotkey = QLabel(SettingsForm)
        self.labelHotkey.setObjectName(u"labelHotkey")
        self.labelHotkey.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setPointSize(12)
        self.labelHotkey.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelHotkey)

        self.hotkey_edit = QPushButton(SettingsForm)
        self.hotkey_edit.setObjectName(u"hotkey_edit")
        self.hotkey_edit.setMinimumSize(QSize(150, 30))
        self.hotkey_edit.setFont(font)

        self.horizontalLayout_2.addWidget(self.hotkey_edit)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.labelHistoryLimit = QLabel(SettingsForm)
        self.labelHistoryLimit.setObjectName(u"labelHistoryLimit")
        self.labelHistoryLimit.setMinimumSize(QSize(0, 30))
        self.labelHistoryLimit.setFont(font)

        self.horizontalLayout.addWidget(self.labelHistoryLimit)

        self.history_limit = QLineEdit(SettingsForm)
        self.history_limit.setObjectName(u"history_limit")
        self.history_limit.setMinimumSize(QSize(0, 30))
        self.history_limit.setFont(font)

        self.horizontalLayout.addWidget(self.history_limit)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.auto_start = QCheckBox(SettingsForm)
        self.auto_start.setObjectName(u"auto_start")
        self.auto_start.setMinimumSize(QSize(0, 30))
        self.auto_start.setFont(font)

        self.horizontalLayout_3.addWidget(self.auto_start)

        self.enable_db_box = QCheckBox(SettingsForm)
        self.enable_db_box.setObjectName(u"enable_db_box")
        self.enable_db_box.setMinimumSize(QSize(0, 30))
        self.enable_db_box.setFont(font)

        self.horizontalLayout_3.addWidget(self.enable_db_box)


        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        self.database_btn = QPushButton(SettingsForm)
        self.database_btn.setObjectName(u"database_btn")
        self.database_btn.setMinimumSize(QSize(0, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.database_btn.setFont(font1)

        self.gridLayout.addWidget(self.database_btn, 3, 0, 1, 1)

        self.import_btn = QPushButton(SettingsForm)
        self.import_btn.setObjectName(u"import_btn")
        self.import_btn.setMinimumSize(QSize(0, 31))
        self.import_btn.setFont(font1)

        self.gridLayout.addWidget(self.import_btn, 4, 0, 1, 1)

        self.export_btn = QPushButton(SettingsForm)
        self.export_btn.setObjectName(u"export_btn")
        self.export_btn.setMinimumSize(QSize(0, 31))
        self.export_btn.setFont(font1)

        self.gridLayout.addWidget(self.export_btn, 5, 0, 1, 1)

        self.shouquan = QPushButton(SettingsForm)
        self.shouquan.setObjectName(u"shouquan")
        self.shouquan.setMinimumSize(QSize(0, 31))
        self.shouquan.setFont(font1)

        self.gridLayout.addWidget(self.shouquan, 6, 0, 1, 1)

        self.save_btn = QPushButton(SettingsForm)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setMinimumSize(QSize(0, 31))
        self.save_btn.setFont(font1)

        self.gridLayout.addWidget(self.save_btn, 7, 0, 1, 1)


        self.retranslateUi(SettingsForm)

        QMetaObject.connectSlotsByName(SettingsForm)
    # setupUi

    def retranslateUi(self, SettingsForm):
        SettingsForm.setWindowTitle(QCoreApplication.translate("SettingsForm", u"\u526a\u8d34\u677f\u5386\u53f2\u8bbe\u7f6e", None))
        self.labelHotkey.setText(QCoreApplication.translate("SettingsForm", u"\u5feb\u6377\u70ed\u952e:", None))
        self.hotkey_edit.setText(QCoreApplication.translate("SettingsForm", u"F9", None))
        self.labelHistoryLimit.setText(QCoreApplication.translate("SettingsForm", u"\u6700\u5927\u8bb0\u5f55\u6570:", None))
        self.history_limit.setText(QCoreApplication.translate("SettingsForm", u"10000", None))
        self.history_limit.setPlaceholderText(QCoreApplication.translate("SettingsForm", u"\u8f93\u516510-500\u7684\u6574\u6570", None))
        self.auto_start.setText(QCoreApplication.translate("SettingsForm", u"\u5f00\u673a\u81ea\u52a8\u542f\u52a8", None))
        self.enable_db_box.setText(QCoreApplication.translate("SettingsForm", u"\u542f\u7528\u8fdc\u7a0b\u6570\u636e\u5e93", None))
        self.database_btn.setText(QCoreApplication.translate("SettingsForm", u"\u8fdc\u7a0b\u6570\u636e\u5e93\u914d\u7f6e", None))
        self.import_btn.setText(QCoreApplication.translate("SettingsForm", u"\u5bfc\u5165\u914d\u7f6e", None))
        self.export_btn.setText(QCoreApplication.translate("SettingsForm", u"\u5bfc\u51fa\u914d\u7f6e", None))
        self.shouquan.setText(QCoreApplication.translate("SettingsForm", u"\u4ee3\u7801\u5757\u6388\u6743", None))
        self.save_btn.setText(QCoreApplication.translate("SettingsForm", u"\u4fdd\u5b58\u8bbe\u7f6e", None))
    # retranslateUi

