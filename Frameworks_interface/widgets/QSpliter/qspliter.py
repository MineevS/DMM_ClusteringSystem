# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
## from ui_form import Ui_QSpliter

from PySide6.QtCore import (
    Qt,
    QSize,
    QPointF,
    QRectF,
    Signal,
    QObject,

)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QToolButton,
    QGridLayout,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QLayout,
    QTableWidget,
    QVBoxLayout,
)

from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QPen,
    QColor,
    QLinearGradient,
    QMouseEvent,


)

from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation


class QSpliter(QWidget):

    #Q_OBJECT

    def __init__(self, title, parent=None):
        super().__init__(parent)
        #self.ui = Ui_QSpliter()
        #self.ui.setupUi(self)
        self.toggledButton = QToolButton()
        self.mainLayout = QGridLayout()
        self.headerLine = QFrame()
        self.toogledAnimation = QParallelAnimationGroup()
        self.contentArea = QScrollArea()
        self.animationDuration = 300
        self.init(title)

    def init(self, title):
        self.toggledButton.setStyleSheet("QToolButton { border: none; }")
        self.toggledButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggledButton.setArrowType(Qt.ArrowType.RightArrow)
        self.toggledButton.setText(title)
        self.toggledButton.setCheckable(True)
        self.toggledButton.setChecked(False)

        self.headerLine.setFrameShape(QFrame.Shape.HLine)
        self.headerLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.headerLine.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)

        self.contentArea.setStyleSheet("QScrollArea { background-color: white; border: none; }")
        self.contentArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)

        self.toogledAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toogledAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toogledAnimation.addAnimation(QPropertyAnimation(self.contentArea, b"maximumHeight"))

        self.mainLayout.setVerticalSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.toggledButton, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.headerLine, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.contentArea, 1, 0, 1, 2)

        self.setLayout(self.mainLayout)

        self.toggledButton.clicked.connect(lambda status_checked: [
            print(status_checked),
            self.toggledButton.setArrowType(status_checked and Qt.ArrowType.DownArrow or Qt.ArrowType.RightArrow),
            self.toogledAnimation.setDirection(status_checked and QAbstractAnimation.Forward or QAbstractAnimation.Backward),
            self.toogledAnimation.start()
        ])

    def setContentLayout(self, contentLayout: QLayout):
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()

        '''[[ spoilerAnimation := self.toogledAnimation.animationAt(i),
           spoilerAnimation.setDuration(self.animationDuration),
           spoilerAnimation.setStartValue(collapsedHeight),
           spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
        ] for i in range(self.toogledAnimation.animationCount() - 1)]'''

        contentAnimation = self.toogledAnimation.animationAt(self.toogledAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

    def layoutContentArea(self) -> QLayout:
        return self.contentArea.layout()

''' 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    spoiler = QSpliter()
    anyLayout = QVBoxLayout()
    anyLayout.addWidget(QTableWidget())
    spoiler.setContentLayout(anyLayout)

    spoiler.show()
    sys.exit(app.exec())'''

# https://translated.turbopages.org/proxy_u/en-ru.ru.26372980-657c809d-2e1ef84f-74722d776562/https/stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
