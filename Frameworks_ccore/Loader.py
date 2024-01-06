# This Python file uses the following encoding: utf-8
from PySide6.QtCore import (
    QFile,
    QTextStream,
)

import qstylizer.parser # pip install qstylizer
import qstylizer.parser

THEME_FIRST_PATH = 'qss\\ThemeFirst.css'
THEME_SECOND_PATH = 'qss\\ThemeSecond.css'

class Loader:
    def __init__(self):
        pass

    @staticmethod
    def load_style_app(theme_current) -> str:
        path_style = (THEME_SECOND_PATH, THEME_FIRST_PATH)[theme_current == 'theme_first']

        styleF = QFile(path_style)


        # TODO
        # Реализовать проверку наличия/отсутствия тем в путях.


        if styleF.exists():
            print("Ok")

        if styleF.open(
                QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            qssstr = styleF.readAll().toStdString()

        return qssstr

    @staticmethod
    def change_color_theme(theme_current, color, msg):
        style = Loader.load_style_app(theme_current)

        css = qstylizer.parser.parse(style)

        match msg:
            case 'фон':
                css.QMainWindow.backgroundColor.setValue(color)
                css.QDialog.backgroundColor.setValue(color)
                # css.QLabel.backgroundColor.setValue(color)
                css.QLabel['#labelClassA'].backgroundColor.setValue(color)
                css.QMenuBar.backgroundColor.setValue(color)
                css.QDockWidget.backgroundColor.setValue(color)
            case 'текст':
                css.QMainWindow.color.setValue(color)
                css.QDialog.color.setValue(color)
                #css.QDockWidget.color.setValue(color)
                css.QLabel['#labelClassA'].color.setValue(color)
                css.QMenuBar.color.setValue(color)
            case 'слайдер':
                css['QSliderButton'].backgroundColor.setValue(color)

        path_style = (THEME_SECOND_PATH, THEME_FIRST_PATH)[theme_current == 'theme_first']

        styleF = QFile(path_style)

        # TODO
        # Реализовать проверку наличия/отсутствия тем в путях.

        if styleF.exists():
            pass

        if styleF.open(
                QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Truncate):
            stream_out = QTextStream(styleF)
            stream_out << css.toString()

        styleF.close()

        return css.toString()
