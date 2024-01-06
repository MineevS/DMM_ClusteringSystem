# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtCore import (
    Qt,
    QSize,
    QPointF,
    QRectF,
    Signal,
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
)
from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QPen,
    QColor,
    QLinearGradient,
    QMouseEvent,
)

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
# from ui_form import Ui_Widget

class QSliderButton(QWidget):
    Off = False
    On = True

    color = "#444"
    offcolor = "#444"

    bgcolor = "#ffffff"
    offbgcolor = "#ffffff"

    clicked = Signal(QMouseEvent)
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        #self.ui = Ui_Widget()
        #self.ui.setupUi(self)
        self.setWindowTitle("QSliderButton")
        self.status: bool = False

        self.setFixedWidth(50)
        self.setFixedHeight(27)

        self.clicked.connect(self.BtnClicked)
        self.toggled.connect(self.btnToggled)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(QPen(QColor("#fff"), 0.1))
        if(self.status == QSliderButton.On):
            bgColorText = self.bgcolor
            bgColor = QColor(bgColorText)
            painter.setBrush(bgColor)

            painter.drawRoundedRect(QRectF(0, 2, self.width(), self.height() - 7), 10, 10)

            onColor = self.color
            mainColorOn = QColor(onColor)
            subColorOn = QColor(onColor)
            subColorOn.setHsl(0, 100, 95, 0)

            ##############################################

            linearGrad = QLinearGradient(QPointF(32, 2), QPointF(46, 16))
            linearGrad.setColorAt(0, subColorOn)
            linearGrad.setColorAt(1, mainColorOn)

            painter.setBrush(linearGrad)
            painter.drawEllipse(QRectF(30, 4, 17, 16))
        else:
            bgColorText = self.offbgcolor
            bgColor = QColor(bgColorText)
            painter.setBrush(bgColor)

            painter.drawRoundedRect(QRectF(0, 2, self.width(), self.height() - 7), 10, 10)

            aoffColor = self.offcolor
            mainColorOn = QColor(aoffColor)
            subColorOn = QColor(aoffColor)
            subColorOn.setHsl(0, 100, 95, 0)

            #############################################

            linearGrad = QLinearGradient(QPointF(2, 2), QPointF(16, 16))
            linearGrad.setColorAt(0, subColorOn)
            linearGrad.setColorAt(1, mainColorOn)

            painter.setBrush(linearGrad)
            painter.drawEllipse(QRectF(2, 4, 16, 16))

    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.MouseButton.LeftButton):
            self.status = not self.status
            self.repaint()
            self.toggled.emit(self.status)
        self.clicked.emit(event)

    # @Slot(bool)
    def btnToggled(self, status: bool):
        pass

    # @Slot(QMouseEvent)
    def BtnClicked(self, event: QMouseEvent):
        pass

    def getStatus(self) -> bool:
        return self.status

    def setStatus(self, value):
        self.status = value
        self.repaint()

    def sizeHint(self) -> QSize:
        return QSize(50, 20)

    def getColor(self) -> str:
        return self.color

    def setColor(self, value) -> None:
        self.color = value
        self.repaint()

    def getOffColor(self) -> str:
        return self.offcolor

    def setOffColor(self, value) -> None:
        self.offcolor = value
        self.repaint()

    def getBgColor(self) -> str:
        return self.bgcolor

    def setBgColor(self, value) -> None:
        self.bgcolor = value
        self.repaint()

    def getOffBgColor(self) -> str:
        return self.offbgcolor

    def setOffBgColor(self, value) -> None:
        self.offbgcolor = value
        self.repaint()

'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sldbtn = QSliderButton()

    # QObject::connect(sldbtn, SIGNAL(toggle(bool)), sldbtn, SLOT(btnToogled(bool)))
    # QObject::connect(sldbtn, SIGNAL(clicked(QMouseEvent)), sldbtn, SLOT(clicked(QMouseEvent)))

    sldbtn.setColor("#557d00")
    sldbtn.setOffColor("#F00")

    sldbtn.setBgColor("#99f5aa")
    sldbtn.setOffBgColor("#ffafaf")

    sldbtn.show()
    sys.exit(app.exec())
'''
