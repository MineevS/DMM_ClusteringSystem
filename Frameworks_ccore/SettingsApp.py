# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QIcon,
    QColor,
)

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
    QHBoxLayout,
    QWidget,
    QMenuBar,
    QSpacerItem,
    QSizePolicy,
    QColorDialog,
)

import qstylizer.parser
from Frameworks_ccore.Loader import Loader

class SettingsApp(QDialog):
    closed = Signal()

    changeThemeDark = Signal(QColor, str)
    changeThemeLight = Signal(QColor, str)

    def __init__(self, styleApp, parent=None):
        super(__class__, self).__init__(parent)
        self.setStyleSheet(styleApp)

        self.setWindowTitle("Настройки приложения")
        self.setFixedSize(600, 800)

        # Фон прозрачный (Поддержка настройки фона qss)
        self.setAttribute(Qt.WidgetAttribute.WA_TintedBackground, True)

        # Границы отключены
        self.setWindowFlags(self.windowFlags())     # | Qt.FramelessWindowHint
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Отслеживание мышки
        self.setMouseTracking(True)

        self.grid = self.init_grid()

        self.up()

    def h(self, frame, row, rowspan):
        frame.setFrameShape(QFrame.Shape.HLine)
        frame.setFixedSize(self.width(), 10)
        self.grid.addWidget(frame, row, 0, 1, rowspan, Qt.AlignCenter)

    def up(self):
        self.frame1 = QFrame(self)
        self.init_frame("первой", "фон", self.frame1, 'theme_first', "Выбрать цвет первой темы", 0, 0, self.changeColorFirstThemeFone)
        # ----------------------------------------------------------------------------------------------- #
        self.frame2 = QFrame()
        self.init_frame("второй", "фон", self.frame2, 'theme_second', "Выбрать цвет второй темы", 1, 0, self.changeColorSecondThemeFone)
        # ----------------------------------------------------------------------------------------------- #
        self.frame3 = QFrame()
        self.h(self.frame3, 2, 3)
        # ----------------------------------------------------------------------------------------------- #
        self.frame4 = QFrame(self)
        self.init_frame("первой", "текст", self.frame4, 'theme_first', "Выбрать цвет первой темы", 3, 0, self.changeColorFirstThemeText)
        # ----------------------------------------------------------------------------------------------- #
        self.frame5 = QFrame()
        self.init_frame("второй", "текст", self.frame5, 'theme_second', "Выбрать цвет второй темы", 4, 0, self.changeColorSecondThemeText)
        # ----------------------------------------------------------------------------------------------- #
        self.frame6 = QFrame()
        self.h(self.frame6, 5, 3)
        # ----------------------------------------------------------------------------------------------- #
        self.frame7 = QFrame(self)
        self.init_frame("первой", "слайдер", self.frame7, 'theme_first', "Выбрать цвет первой темы", 6, 0, self.changeColorFirstThemeSlider)
        # ----------------------------------------------------------------------------------------------- #
        self.frame8 = QFrame()
        self.init_frame("второй", "слайдер", self.frame8, 'theme_second', "Выбрать цвет второй темы", 7, 0, self.changeColorSecondThemeSlider)
        # ----------------------------------------------------------------------------------------------- #
        self.frame9 = QFrame()
        self.h(self.frame9, 8, 3)
        # ----------------------------------------------------------------------------------------------- #
        # TODO
        # ----------------------------------------------------------------------------------------------- #
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.grid.addItem(spacer)
        # ----------------------------------------------------------------------------------------------- #
        # TODO

    def init_frame(self, pretext, apretext, frame, theme, text, posstr, postop, handler):
        labelDark = QLabel("В качестве цвета " + apretext + "a " + pretext + " темы использовать:  ")
        labelDark.setFixedWidth(len(labelDark.text())*7)
        self.grid.addWidget(labelDark, posstr, postop, 1, 1, Qt.AlignLeft)

        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Sunken)
        frame.setFixedSize(25, 25)
        frame.setFrameShadow(QFrame.Shadow.Raised)

        self.style_frames(frame, theme, apretext)

        self.grid.addWidget(frame, posstr, postop + 1, 1, 1, Qt.AlignCenter)

        buttonDark = QPushButton(text)
        buttonDark.clicked.connect(handler)

        self.grid.addWidget(buttonDark, posstr, postop + 2, 1, 1, Qt.AlignRight)

    def style_frames(self, frame, theme, message):
        css = qstylizer.parser.parse(self.load_theme(theme))
        back1 = css.QMainWindow.border.value
        match message:
            case 'фон':
                back2 = css.QMainWindow.backgroundColor.value
            case 'текст':
                back2 = css.QMainWindow.color.value
            case 'слайдер':
                back2 = css['QSliderButton'].backgroundColor.value

        frame.setStyleSheet("QFrame {"
                            "background-color: " + ("white", back2)[back2 is not None] + ";" +
                            "border: " + ("black", back1)[back1 is not None] + "; }")

    def updateframes(self, message):
        match message:
            case 'фон':
                self.style_frames(self.frame1, 'theme_first', message)
                self.style_frames(self.frame2, 'theme_second', message)
            case 'текст':
                self.style_frames(self.frame4, 'theme_first', message)
                self.style_frames(self.frame5, 'theme_second', message)
            case 'слайдер':
                self.style_frames(self.frame7, 'theme_first', message)
                self.style_frames(self.frame8, 'theme_second', message)

    def load_theme(self, path_theme) -> str:
        style_theme = Loader.load_style_app(path_theme)
        return style_theme

    def changeColorFirstThemeFone(self):
        color = self.changeColor()
        if color.isValid():
            self.changeThemeDark.emit(color, 'фон')

    def changeColorSecondThemeFone(self):
        color = self.changeColor()
        if color.isValid():
            self.changeThemeLight.emit(color, 'фон')

    def changeColorFirstThemeText(self):
        color = self.changeColor()
        if color.isValid():
            self.changeThemeDark.emit(color, 'текст')

    def changeColorSecondThemeText(self):
        color = self.changeColor()
        if color.isValid():
            self.changeThemeLight.emit(color, 'текст')

    def changeColorFirstThemeSlider(self):
        color = self.changeColor()
        if color.isValid():
            self.changeThemeDark.emit(color, 'слайдер')

    def changeColorSecondThemeSlider(self):
        color = self.changeColor()
        if color.isValid():
            self.changeThemeLight.emit(color, 'слайдер')

    def changeColor(self) -> QColor():
        Color = QColorDialog()
        return Color.getColor("Выбрать цвет")

    def init_grid(self):
        gridW = QGridLayout()
        self.setLayout(gridW)

        button = QPushButton()
        button.setIcon(QIcon(':/icon/icon.ico'))
        gridW.addWidget(button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        prewidget = QWidget(self)

        gridH = QHBoxLayout()
        gridH.setContentsMargins(0, 0, 0, 0)

        collapseToTray = QPushButton("-")
        collapseToTray.setStatusTip("collapseToTray")
        collapseToTray.clicked.connect(self.on_click_collapseToTray)
        gridH.addWidget(collapseToTray, 0, Qt.AlignmentFlag.AlignRight)

        '''collapse = QPushButton("+")
        collapse.setStatusTip("collapse")
        collapse.clicked.connect(self.on_click_collapse)
        gridH.addWidget(collapse, 1, Qt.AlignmentFlag.AlignRight)'''

        close = QPushButton("☼")
        close.setStatusTip("close")
        close.clicked.connect(self.on_click_close)
        gridH.addWidget(close, 2, Qt.AlignmentFlag.AlignRight)

        prewidget.setLayout(gridH)
        gridW.addWidget(prewidget, 0, 1, 1, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        menubar = QMenuBar()
        gridW.addWidget(menubar, 1, 0, 1, 2,  Qt.AlignmentFlag.AlignTop)

        self.widw = QWidget()

        wid = QWidget()
        gridW.addWidget(wid, 2, 0, 1, 3, Qt.AlignmentFlag.AlignTop)

        gridlay = QGridLayout()
        wid.setLayout(gridlay)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gridW.addItem(spacer, 3, 0, 1, 3, Qt.AlignmentFlag.AlignTop)

        return gridlay

    def on_click_collapseToTray(self):
        self.setWindowState(self.windowState() ^ Qt.WindowState.WindowMinimized)

    def on_click_collapse(self):
        self.setWindowState(self.windowState() ^ Qt.WindowState.WindowFullScreen)

    def on_click_close(self):
        self.close()
        self.closed.emit()

    def ChangeIndexComboboxDark(self, i):
        self.changeThemeDark.emit(i)

    def ChangeIndexComboboxLight(self, i):
        self.changeThemeLight.emit(i)
