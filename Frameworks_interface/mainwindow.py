# This Python file uses the following encoding: utf-8
import sys
import time

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PIL import Image   # pip install Pillow(PIL)
from PySide6.QtCore import (
    Qt,
    QCoreApplication,
    QSettings,
    QMargins,
    QSize,
    QPoint
)
from PySide6.QtGui import (
    QAction,
    QIcon,
    QMouseEvent,
    QCursor,
    QIntValidator,
    QDoubleValidator,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QGridLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QStyleFactory,
    QMenuBar,
    QSpacerItem,
    QSizePolicy,
    QFrame,
    QMdiArea,
    QMdiSubWindow,
    QGraphicsDropShadowEffect,
    QButtonGroup,
    QRadioButton,
    QFileDialog,
    QDockWidget,
    QComboBox,
    QScrollArea,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from Frameworks_ccore.SettingsApp import SettingsApp
from ui_form import Ui_MainWindow
from Frameworks_ccore.Loader import Loader
from widgets.sliderButton.QSliderButton import QSliderButton
from sklearn.datasets import make_moons, make_blobs, make_circles  # pip install scikit-learn
from DatasetsGenerators.make_dna import make_dna
from DatasetsGenerators.make_spheres import make_spheres
from ClusteringMethods.ClasteringAlgorithms import (
    Context,
    ConcreteStrategyBIRCH_from_SKLEARN_LEARN,
    ConcreteStrategyBIRCH_from_PYCLUSTERING,
    ConcreteStrategyCURE,
    ConcreteStrategyROCK,
)
from widgets.QSpliter.qspliter import QSpliter
from AnalysisMethods.AnalysisAlgorithms import DunnIndex, DunnIndexMean, DBi, converter_to_c

import qstylizer.parser     # pip install qstylizer
import cv2                  # pip install opencv-python
import numpy as np          # pip install numpy
import csv                  # pip install csv
import os

os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(5)) # Установить в зависимости от количества ядер[5] на вашем компьютере.

# [1.1]
ORGANIZATION_NAME = 'RTU MIREA'
ORGANIZATION_DOMAIN = 'mirea.ru'
APPLICATION_NAME = 'ClustSystem'
APPLICATION_VERSION = '0.1.2'
app = None
LIST_TYPE_DISTRIBUTION = ['Нормальное', 'Показательное', 'Биноминальное']
CASE_TYPES = {'lb': QLabel, 'le': QLineEdit, 'chb': QCheckBox, 'pb': QPushButton}
DEFAULT_VALUE = [100,  # n_sample
                 2,  # n_features
                 None,  # centers
                 1.0,  # cluster_std
                 (-0.1, 0.1),  # center_box
                 None,  # random_state(seed)
                 0.8,  # factor
                 None,  # noise
                 1.0,  # norm
                 0.0,  # y
                 0.0,  # z
                 False,  # shuffle
                 False  # return_centers
                 ]
DEFAULT_VALUE_TW3 = ['',  # used
                     str(3),  # n_cluster
                     str(50),  # branching_factor
                     str(0.5),  # threshold
                     '',  # compute_labels
                     '',  # copy
                     str(200),  # max_node_entries
                     str(0.5),  # diameter
                     str(500),  # entry_size_limit
                     str(1.5),  # diameter_multiplier
                     '',  # type_measurement
                     '',  # ccore
                     str(5),  # n_represent_points
                     str(0.5),  # compression
                     str(2.0)  # eps
                     ]
switch_tootip_tw2_fr1 = [
    f"Количество точек [uint, (default: {DEFAULT_VALUE[0]})]",
    f"Количество фитчей [uint, (default: {DEFAULT_VALUE[1]})]",
    f"Количество центров [uint, (default: {DEFAULT_VALUE[2]})]",
    f"Стандартное отклонение кластеров [float, (default: {DEFAULT_VALUE[3]})]",
    f"Ограничивающая рамка для каждого центра кластера [tuple(float, float), (default: {DEFAULT_VALUE[4]})]",
    f"random_state (seed) [int, (default: {DEFAULT_VALUE[5]})]",
    f"коэффициент масштабирования [int, (default: {DEFAULT_VALUE[6]})]",
    f"noise [float, (default: {DEFAULT_VALUE[7]})]",
    f"Коэффициент нормировки [float: (default: {DEFAULT_VALUE[8]})]",
    f"Смещение по оси y для одномерных данных [float: (default: {DEFAULT_VALUE[9]})]",
    f"смещение по оси z для двумерных данных [float: (default: {DEFAULT_VALUE[10]})]",
    f"Следует ли перетасовывать точки? [bool, (default: {DEFAULT_VALUE[11]})]",
    f"Возвращать ли центры? [bool, (default: {DEFAULT_VALUE[12]})]"]

# [1.2]
'''
    @brief  Инициализатор метаданных приложения для последующей их регистрации в реестре ОС.
'''


def init_config_app():
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    QCoreApplication.setApplicationVersion(APPLICATION_VERSION)


# [1.3]
'''
    @brief  Создание настроек приложения
'''


def create_settings_app():
    settings = QSettings()
    settings.beginGroup("BaseSettings")
    settings.setValue("NameApp", APPLICATION_NAME)
    settings.setValue("VersionApp", APPLICATION_VERSION)
    settings.endGroup()
    settings.beginGroup("StyleSettings")
    settings.setValue("theme_current", 'theme_first')
    settings.endGroup()
    settings.sync()  # Фиксация настроек приложения


# [1.4]
'''
    @brief  Проверка наличия настроек в реестре и установка в случае их отсутствия.
'''


def load_settings_app() -> bool:
    settings = QSettings()
    if len(settings.allKeys()) == 0:
        create_settings_app()
        return load_settings_app()
    else:
        return True


'''
    @brief  Загрузка из реестра информации по текущей теме приложения.
'''


def load_theme_current_app() -> str:
    settings = QSettings()
    settings.beginGroup("StyleSettings")
    theme_current = settings.value("theme_current", str)
    settings.endGroup()
    return theme_current


# [1.6]
'''
    @brief  Загрузка текущей темы [147:9] и стиля приложения [148:9] с глобальной установкой [149:9].
'''


def loader_settings():
    if load_settings_app():
        current_theme = load_theme_current_app()
        qAppStyle = Loader.load_style_app(current_theme)
        app.setStyleSheet(qAppStyle)
    return qAppStyle, current_theme


'''
    @brief  Основной класс приложения.
'''


class MainWindow(QMainWindow):
    '''
        @brief  Инициализация приложения.
    '''

    def __init__(self, styleApp, theme_current, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()                           # Инициализация gui окна.
        self.ui.setupUi(self)
        self.setProperty('theme_current', theme_current)    # Задание значения текущей темы.
        self.setStyleSheet(styleApp)                        # Установка стилей программы
        self.dialog: SettingsApp = None                     # Диалоговое окно настроек программы.
        self.setProperty('dragPos', None)                   # Позиция перемещения курсора мышки при изменении размеров окна.
        self.setProperty('fl', True)                        # Флаг переключения подокон в левом окне.
        # Границы отключены
        self.setWindowFlag(Qt.FramelessWindowHint)          # Отключение класической рамки обрамления.
        # Отслеживание мышки
        self.setMouseTracking(True)                         # Включение для отслеживания курсора мышки с последующим изменением размеров окна.
        # Инициализация базового gridlayout и возвращение вложенного основного gridlayout
        # для настройки пользовательских компонентов
        self.init_gridBase()  # Инициализация базового GridLayout
        self.init_grid_subWinLeft()                         # Инициализация компонентов на левой нижней панели
        self.init_grid_subWinRight()                        # Инициализация компонентов на правой нижней панели
        self.setStatusBar(QStatusBar())                     # Создания явного QStatusBar т. к. default не так работает как нужно.
        self.cursor1 = QCursor()                            # Создания явного QCursor т. к. default не так работает как нужно.
        self.setCursor(self.cursor1)

    '''
        @brief  Инициализация базового GridLayout.
    '''

    def init_gridBase(self) -> None:  # QGridLayout()
        grid = QGridLayout(objectName='gridBasis')
        grid.addWidget(QPushButton(icon=QIcon('./icon/icon.ico')), 0, 0, 1, 1,
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label = QLabel(APPLICATION_NAME, self, objectName='labelClassA')
        grid.addWidget(self.label, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        hlayout = QHBoxLayout(contentsMargins=QMargins(0, 0, 0, 0))
        grid.addWidget(QWidget(layout=hlayout), 0, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.sldbtn = QSliderButton()
        self.sldbtn.setStatus((1, 0)[self.property('theme_current') == 'theme_first'])
        self.sldbtn.toggled.connect(self.clickSliderButtonBool)
        self.sliderButton_install_style()
        hlayout.addWidget(self.sldbtn, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        hlayout.addWidget(QPushButton("-", statusTip="Свернуть",
                                      clicked=lambda: self.setWindowState(
                                          self.windowState() ^ Qt.WindowState.WindowMinimized)),
                          1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        hlayout.addWidget(QPushButton("+", statusTip="Развернуть/Восстановить",
                                      clicked=lambda: self.setWindowState(
                                          self.windowState() ^ Qt.WindowState.WindowFullScreen)),
                          2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        hlayout.addWidget(QPushButton("☼", statusTip="Закрыть", clicked=lambda: self.close()),
                          3, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.menubar = QMenuBar()
        grid.addWidget(self.menubar, 1, 0, 1, 3, Qt.AlignmentFlag.AlignTop)
        self.init_menu(self.menubar)
        self.setCentralWidget(QWidget(layout=grid))
        # ------------------------------------------------------------------------------------------------- #
        self.widget1 = QWidget(objectName='widgetElem', fixedWidth=0.5 * self.width())
        self.widget1.setLayout(QGridLayout(objectName='gridBase'))
        dropShawdowEffect1 = QGraphicsDropShadowEffect(self.widget1, color=Qt.GlobalColor.gray, blurRadius=25,
                                                       offset=QPoint(5, 5))  # Обеспечивает размытие по контору.
        self.widget1.setGraphicsEffect(dropShawdowEffect1)
        grid.addWidget(self.widget1, 2, 0, 1, 1)
        # ------------------------------------------------------------------------------------------------- #
        self._mdiarea = QMdiArea()
        grid.addWidget(self._mdiarea, 2, 1, 1, 2)
        dropShawdowEffect3 = QGraphicsDropShadowEffect(self._mdiarea, color=Qt.GlobalColor.gray, blurRadius=25,
                                                       offset=QPoint(5, 5))  # Обеспечивает размытие по контору.
        self._mdiarea.setGraphicsEffect(dropShawdowEffect3)
        self._mdiarea.tileSubWindows()

    '''
        @brief  Инициализация компонентов правого подокна.
    '''

    def init_grid_subWinRight(self):  # Основной grid для добавления элементов
        genDockWidget = lambda layout, row, column, rowSpace, colSpace, n, obj: [
            qmw := QMainWindow(windowFlags=Qt.WindowType.Widget, objectName='qmw' + str(n)),
            (type == 'FG') and qmw.setMaximumHeight(400),
            qmw.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),
            gl := QGridLayout(),
            dw := QDockWidget(widget=QWidget(layout=gl), objectName='dw' + str(n),
                              features=QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                                       QDockWidget.DockWidgetFeature.DockWidgetMovable),
            dw.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),
            gl.addWidget(obj, 0, 0),
            qmw.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dw),
            layout.addWidget(qmw, row, column, rowSpace, colSpace)
        ]
        genSubWin = lambda subwin_name, cnv1_name, cnv2_name, win_title, row, column: [
            subwin := QMdiSubWindow(objectName=subwin_name,
                                    windowTitle=win_title, visible=True, layout=QGridLayout()),
            cnv11_wg := QWidget(subwin, objectName=cnv1_name, layout=QGridLayout(), minimumSize=QSize(150, 150)),
            cnv11_wg.layout().addWidget(QLabel("Результат кластеризации: "), 0, 0),
            fg1 := FigureCanvasQTAgg(Figure(figsize=(5, 5), dpi=60)),
            fg2 := FigureCanvasQTAgg(Figure(figsize=(5, 5), dpi=60)),
            genDockWidget(cnv11_wg.layout(), 1, 0, 1, 1, 1, fg1),
            genDockWidget(cnv11_wg.layout(), 1, 1, 1, 1, 2, fg2),
            label := QLabel('Ок', styleSheet='QLabel {color: green; }', visible=False),
            spl1 := QSpliter('Параметры', subwin),
            grid := QGridLayout(),
            table := QTableWidget(rowCount=4, columnCount=2, objectName='stw',
                                  minimumSize=QSize(250, 50), horizontalHeaderLabels=["Параметр", "Значение"]),
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
            table.setItem(0, 0, QTableWidgetItem('Время работы алгоритма')),
            table.setCellWidget(1, 0, QLabel("Показатель DunnIndex",
                                             toolTip='Минимальное расстояние между кластерами')),
            table.setCellWidget(2, 0, QLabel('Показатель DunnIndexMean',
                                             toolTip='Минимальное среднее расстояние между кластерами')),
            table.setCellWidget(3, 0, QLabel('Показатель DBi', toolTip='...')),
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
            genDockWidget(grid, 0, 0, 5, 1, 3, table),
            spl1.setContentLayout(grid),
            grid.addWidget(QPushButton('Сохранить снимки', clicked=lambda status: [
                fg1.figure.savefig(subwin_name + '_image2D.png'),
                fg2.figure.savefig(subwin_name + '_image3D.png'),
                label.setVisible(True),
            ]), 0, 1),
            grid.addWidget(QPushButton('Сохранить таблицу', clicked=lambda status: [
                label.setVisible(True),
                self.table_to_csv(table, subwin_name),
            ]), 1, 1),
            grid.addWidget(label, 2, 1, Qt.AlignmentFlag.AlignCenter),
            subwin.layout().addWidget(cnv11_wg, 0),
            subwin.layout().addWidget(spl1, 1, Qt.AlignmentFlag.AlignVertical_Mask | Qt.AlignmentFlag.AlignBottom),
            subwin.layout().setStretch(0, 12),
            subwin.layout().setStretch(1, 1),
            self._mdiarea.addSubWindow(subwin),
        ]
        genSubWin('sub_birch_s1', 'cnv11_wg', 'spl12_wg', 'BIRCH_S', 0, 0)
        genSubWin('sub_birch_p1', 'cnv21_wg', 'spl22_wg', 'BIRCH_P', 0, 1)
        genSubWin('sub_cure_1', 'cnv31_wg', 'spl32_wg', 'CURE', 1, 0)
        genSubWin('sub_rock_1', 'cnv41_wg', 'spl42_wg', 'ROCK', 1, 1)
        self._mdiarea.tileSubWindows(),

    '''
        @brief  Экспорт данных из таблицы в csv-файл.
    '''

    def table_to_csv(self, table, subwin_name):
        with open(subwin_name + '_DataTable.csv', 'w', newline='', encoding='utf-8') as myfile:
            writer = csv.writer(myfile, dialect='excel', delimiter=";", quoting=csv.QUOTE_ALL)
            for row in range(table.rowCount()):
                rowData = []
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    if item == None:
                        item = table.cellWidget(row, column)
                    rowData.append(((item is not None) and item.text() or ''))  # encode('utf8')
                writer.writerow(rowData)

    '''
        @brief  Инициализация панели `меню`.
    '''
    def init_menu(self, menu):
        file_menu = menu.addMenu("Инструменты")
        action21_settings_project = QAction("Настройки", self,
                                            statusTip="Изменить настройки", triggered=self.ChangeSettingsClick)
        file_menu.addAction(action21_settings_project)

    '''
        @brief  Инициализация левого подокна.
    '''

    def init_grid_subWinLeft(self):
        self.init_frame(1, True)
        self.init_frame(2, True)
        self.init_frame(3, True)
        self.button_start = QPushButton("Провести кластеризацию",
                                        statusTip="Проведение кластеризации", enabled=False,
                                        clicked=self.clickStartClustering)
        self.widget1.findChild(QGridLayout, 'gridBase') \
            .addWidget(self.button_start, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.widget1.layout().addWidget(self.button_start, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.widget1.layout().addWidget(QPushButton('Перестроить подокна',
                                                    clicked=lambda status: [
                                                        (self.property('fl')) and [self._mdiarea.cascadeSubWindows(),
                                                                                   [sub.resize(QSize(1440, 920)) for sub
                                                                                    in self._mdiarea.subWindowList()]]
                                                        or self._mdiarea.tileSubWindows(),
                                                        self.fun(not self.property('fl'))]),
                                        6, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

    '''
        @brief  Переключение флага между способами отображения подокон: `cascadeSubWindows` (True) и `tileSubWindows`(False).
    '''

    def fun(self, status):
        self.setProperty('fl', status)

    '''
        @brief  Обработчик для frame4 переключение между виджетами `widget_image` и `widget_table`.
    '''

    def handler_fr3(self):
        frame3 = self.widget1.findChild(QFrame, 'frame3')
        frame3.setEnabled(True)
        match self.property('format_file'):
            case 'jpg' | 'png' | 'bmp':
                frame3.findChild(QWidget, 'widget_image').setVisible(True)
                self.button_start.setEnabled(True)
                # frame4.findChild(QWidget, 'widget_table').setVisible(False)
            case 'csv' | 'xlsx':  # [В версии v1.0 загрузка данных из csv не предусмотрена]
                '''frame4.findChild(QWidget, 'widget_image').setVisible(False)
                frame4.findChild(QWidget, 'widget_table').setVisible(True)'''
                pass
            case _:
                pass

    '''
        @brief  Инициализация кнопок переключения между вводом(изображений) и генерацией данных.
    '''

    def init_groupButton(self, grid):
        self.radio_button_1 = QRadioButton("1. Ввод данных", objectName="radioButton1", checked=True)
        grid.addWidget(self.radio_button_1, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.radio_button_2 = QRadioButton("2. Генерация данных", objectName="radioButton2")
        grid.addWidget(self.radio_button_2, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_button_1)
        self.button_group.addButton(self.radio_button_2)
        self.button_group.buttonClicked.connect(self.switch_frame1_frame2)

    '''
        @brief  Инициализация frame(s).
    '''

    def init_frame(self, index_frame, status):
        grid: QGridLayout = self.widget1.findChild(QGridLayout, 'gridBase')  # Получение базового грида
        frame = QFrame(self, frameStyle=QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken,
                       objectName="frame" + str(index_frame), visible=status, minimumWidth=self.widget1.width() - 25,
                       layout=QGridLayout(objectName='gridLayout1'), contentsMargins=QMargins(0, 0, 0, 0))
        grid.addWidget(frame, index_frame + 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        qmw = QMainWindow(frame, windowFlags=Qt.WindowType.Widget)
        frame.layout().addWidget(qmw)
        match index_frame:
            case 1:
                frame.setEnabled(False)
                gl1_fr1 = QGridLayout()
                dockWidget = QDockWidget('Генерация данных', objectName='DW' + str(index_frame),
                                         widget=QScrollArea(widget=QWidget(layout=gl1_fr1), widgetResizable=True),
                                         features=QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable,
                                         dockLocationChanged=lambda status: (
                                                                                        status == Qt.DockWidgetArea.NoDockWidgetArea) and (
                                                                                    dockWidget.setMinimumWidth(
                                                                                        300) or dockWidget.setMinimumHeight(
                                                                                500)) or
                                                                            dockWidget.setMinimumWidth(
                                                                                100) or dockWidget.setMinimumHeight(100)
                                         )
                # -----------------------------------------------------------------------------------------------------#
                sgl1_fr1 = QGridLayout()
                gl1_fr1.addWidget(QWidget(layout=sgl1_fr1), 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                alabel_gen = QLabel("Данные успешно сгенерированны!", objectName='labelClassC', visible=False)
                sgl1_fr1.addWidget(alabel_gen, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                sgl1_fr1.addWidget(QRadioButton("1. Генерация распределений", objectName="srb1_fr1", checked=False,
                                                toggled=lambda state: wg1_fr1.setVisible(True) or [
                                                    wg2_fr1.setVisible(False), alabel_gen.setVisible(False)]),
                                   0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                sgl1_fr1.addWidget(QRadioButton("2. Генерация изображений", objectName="srb2_fr1",
                                                toggled=lambda state: wg1_fr1.setVisible(False) or [
                                                    wg2_fr1.setVisible(True), alabel_gen.setVisible(False)]),
                                   1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                # -----------------------------------------------------------------------------------------------------#
                wg1_fr1 = QWidget(objectName='wg1_fr1', visible=False, layout=QGridLayout())
                sgl1_fr1.addWidget(wg1_fr1, 2, 0, 2, 1, Qt.AlignmentFlag.AlignCenter)
                wg1_fr1.layout().addWidget(QLabel("Введите количество точек для генерации: "),
                                           0, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
                wg1_fr1.layout().addWidget(QLineEdit(objectName='le1_fr1', validator=QIntValidator(bottom=0)),
                                           1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                def FIG(layout, row, column, rowSpan, colSpan):
                    cnv_fr = FigureCanvasQTAgg(Figure(figsize=(5, 5), dpi=60))
                    cnv = QWidget(layout=QGridLayout(), fixedSize=QSize(250, 250))
                    cnv.layout().addWidget(cnv_fr)
                    layout.addWidget(cnv, row, column, rowSpan, colSpan, Qt.AlignmentFlag.AlignCenter)
                    return cnv_fr
                cnv1_fr1 = FIG(sgl1_fr1, 5, 0, 1, 4)
                cnv2_fr1 = FIG(sgl1_fr1, 6, 0, 1, 4)
                switch = ['le1_fr1', 'le2_fr1', 'le3_fr1']
                wg1_fr1.layout().addWidget(QPushButton("Сгенерировать набор данных", objectName='pb6_fr1',
                                                       visible=False, clicked=lambda status:
                    [le1 := wg1_fr1.findChild(QLineEdit, switch[0]), le2 := wg1_fr1.findChild(QLineEdit, switch[1]),
                     self.handler_pb6_fr1(int((0, le1.text())[le1.text() != '']),
                                          int((0, le2.text())[le2.text() != '']), tw1_fr1, alabel_gen, cnv1_fr1,
                                          cnv2_fr1,
                                          grid.parentWidget().findChild(QFrame, 'frame2').findChild(QRadioButton,
                                                                                                    'rb1_fr2'),
                                          grid.parentWidget().findChild(QFrame, 'frame3'))]),
                                           12, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                agrid_add = QGridLayout()
                wg_add = QWidget(wg1_fr1, objectName='wg_add', visible=True, layout=agrid_add)
                wg1_fr1.layout().addWidget(wg_add, 11, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                agrid_add.addWidget(QLabel("Начало", objectName='lb_add1'), 0, 0, 1, 1)
                agrid_add.addWidget(QLabel("Шаг", objectName='lb_add2'), 0, 1, 1, 1)
                agrid_add.addWidget(QLabel("Конец", objectName='lb_add3'), 0, 2, 1, 1)
                agrid_add.addWidget(QLabel("Тип распределения фитчей", objectName='lb_add4'), 0, 3, 1, 1)
                agrid_add.addWidget(QLineEdit(objectName='le_add1'), 1, 0, 1, 1)
                agrid_add.addWidget(QLineEdit(objectName='le_add2'), 1, 1, 1, 1)
                agrid_add.addWidget(QLineEdit(objectName='le_add3'), 1, 2, 1, 1)
                alb3_fr1 = QLabel("Укажите seed: ", enabled=False)
                agrid_add.addWidget(QCheckBox(clicked=lambda status: [
                    alb3_fr1.setEnabled(status), le3_ptd.clear(), le3_ptd.setEnabled(status)]),
                                    2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                agrid_add.addWidget(alb3_fr1, 2, 1, 1, 2, Qt.AlignmentFlag.AlignLeft)
                le3_ptd = QLineEdit(objectName='le3_ptd', enabled=False, validator=QIntValidator(bottom=0))
                agrid_add.addWidget(le3_ptd, 2, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
                agrid_add.addWidget(QPushButton("Далее", objectName='pb5_fr1', visible=True,
                clicked=lambda state: agrid_add.parentWidget().findChild(QWidget,'wg_ptd').setVisible(True) or
                self.handler_pb5_fr1(acb_add1.currentText(), [
                    wg_ptd.findChild(QLabel, 'lb1_ptd'), wg_ptd.findChild(QLabel, 'lb2_ptd')], [
                        wg_ptd.findChild(QLineEdit,'le1_ptd'), wg_ptd.findChild(QLineEdit, 'le2_ptd')])),
                3, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
                acb_add1 = QComboBox(objectName='cb_add1')
                acb_add1.addItems(LIST_TYPE_DISTRIBUTION)
                agrid_add.addWidget(acb_add1, 1, 3, 1, 1)
                agrid_ptd = QGridLayout()
                wg_ptd = QWidget(wg1_fr1, objectName='wg_ptd', visible=False,
                                 layout=agrid_ptd)  # ptd - param_type_distribution
                agrid_add.addWidget(wg_ptd, 4, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
                agrid_ptd.addWidget(QLabel("n", objectName='lb1_ptd', toolTip="Количество испытаний"), 0, 0, 1, 1)
                agrid_ptd.addWidget(QLineEdit(objectName='le1_ptd', validator=QDoubleValidator(bottom=0.0)), 0, 1, 1, 1)  # param1
                agrid_ptd.addWidget(QLabel("p", objectName='lb2_ptd', toolTip="Параметр распределения"), 1, 0, 1, 1)
                agrid_ptd.addWidget(QLineEdit(objectName='le2_ptd', validator=QDoubleValidator(bottom=0.0, top=1.0)), 1, 1, 1, 1)  # param2
                agrid_ptd.addWidget(QPushButton("Добавить запись", objectName='pb7_fr1', clicked=lambda state:
                [le2_fr1_text := wg1_fr1.findChild(QLineEdit, 'le2_fr1').text(),
                 tw1_fr1.setRowCount(int((0, le2_fr1_text)[le2_fr1_text != ''])),
                 le_add1_text := wg_add.findChild(QLineEdit, 'le_add1').text(),
                 le_add2_text := wg_add.findChild(QLineEdit, 'le_add2').text(),
                 le_add3_text := wg_add.findChild(QLineEdit, 'le_add3').text(),
                 le3_ptd_text := wg_add.findChild(QLineEdit, 'le3_ptd').text(),
                 self.handler_tw1_fr1(
                     int((0, le_add1_text)[le_add1_text != '']), int((0, le_add2_text)[le_add2_text != '']),
                     int((0, le_add3_text)[le_add3_text != '']), acb_add1.currentText(), tw1_fr1,
                     wg1_fr1.findChild(QPushButton, 'pb6_fr1'),
                     [wg_add.findChild(QLabel, 'lb1_ptd'), wg_add.findChild(QLabel, 'lb2_ptd')],
                     [wg_add.findChild(QLineEdit, 'le1_ptd'), wg_add.findChild(QLineEdit, 'le2_ptd')],
                     grid.parentWidget().findChild(QFrame, 'frame3'),
                     int((-1, le3_ptd_text)[le3_ptd_text != '']))]),
                                    3, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
                tw1_fr1 = QTableWidget(visible=True, objectName='tw1_fr1', columnCount=2, minimumSize=QSize(295, 250),
                                       horizontalHeaderLabels=["Тип распределения", "Параметры распределения"])
                tw1_fr1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                wg1_fr1.layout().addWidget(tw1_fr1, 10, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
                wg1_fr1.layout().addWidget(
                    QLabel("Укажите размерность пространства фитч: ", objectName='lb2_fr1', visible=True),
                    2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
                wg1_fr1.layout().addWidget(
                    QLineEdit(visible=True, objectName='le2_fr1', validator=QIntValidator(bottom=0)),
                    3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                # -----------------------------------------------------------------------------------------------------#
                wg2_fr1 = QWidget(objectName='wg2_fr1', visible=False, layout=QGridLayout())
                sgl1_fr1.addWidget(wg2_fr1, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                tw2_fr1 = QTableWidget(visible=True, objectName='tw2_fr1', columnCount=14, minimumSize=QSize(290, 250),
                                       horizontalHeaderLabels=["method", "n_samples", "n_features", "centers",
                                                               "cluster_std", "center_box",
                                                               "random_state(seed)", "factor", "noise", "norm", "y",
                                                               "z", "shuffle", "return_centers"])
                tw2_fr1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
                tw2_fr1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                wg2_fr1.layout().addWidget(tw2_fr1, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
                gl = QGridLayout()
                wg2_fr1.layout().addWidget(QWidget(layout=gl), 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                FLAG_not_enabled = ~Qt.ItemFlag.ItemIsEnabled,
                FLAG_enabled = Qt.ItemFlag.ItemIsEnabled
                ALL = [
                    (str(DEFAULT_VALUE[0]), FLAG_enabled), (str('-'), FLAG_not_enabled),
                    (str('-'), FLAG_not_enabled), (str('-'), FLAG_not_enabled),
                    (str('-'), FLAG_not_enabled), (str(DEFAULT_VALUE[5]), FLAG_not_enabled),
                    (str('-'), FLAG_not_enabled), (str(DEFAULT_VALUE[7]), FLAG_enabled),
                    (str(DEFAULT_VALUE[8]), FLAG_enabled), (str(DEFAULT_VALUE[9]), FLAG_enabled),
                    (str(DEFAULT_VALUE[10]), FLAG_enabled)
                ]
                gl.addWidget(QPushButton("Добавить запись", clicked=lambda status: [
                    tw2_fr1.setRowCount(tw2_fr1.rowCount() + 1),
                    cb := QComboBox(),
                    cb.setProperty('rowtable', tw2_fr1.rowCount() - 1),
                    cb.currentTextChanged.connect(lambda status: [
                        row := cb.property('rowtable'),
                        inr := lambda item, val: (FLAG_enabled == val) and
                                                 (not item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled)) or
                                                 (item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)),
                        [[tw2_fr1.item(row, index + 1).setText(val[0]), inr(tw2_fr1.item(row, index + 1), val[1])] for
                         index, val in enumerate(ALL)],
                        tw2_fr1.cellWidget(row, 12).setEnabled(DEFAULT_VALUE[11]),
                        tw2_fr1.cellWidget(row, 13).setEnabled(DEFAULT_VALUE[12]),
                        (status == 'make_blobs') and ([
                            tw2_fr1.item(row, 2).setText(str(DEFAULT_VALUE[1])),
                            inr(tw2_fr1.item(row, 2), FLAG_enabled),
                            tw2_fr1.item(row, 3).setText(str(DEFAULT_VALUE[2])),
                            inr(tw2_fr1.item(row, 3), FLAG_enabled),
                            tw2_fr1.item(row, 4).setText(str(DEFAULT_VALUE[3])),
                            inr(tw2_fr1.item(row, 4), FLAG_enabled),
                            tw2_fr1.item(row, 5).setText(str(DEFAULT_VALUE[4])),
                            inr(tw2_fr1.item(row, 5), FLAG_enabled),
                            tw2_fr1.item(row, 8).setText('-'), inr(tw2_fr1.item(row, 8), FLAG_not_enabled),
                            tw2_fr1.cellWidget(row, 13).setEnabled(True),
                        ]) or (status == 'make_dna') and ([
                            tw2_fr1.item(row, 5).setText(str(DEFAULT_VALUE[4])),
                            tw2_fr1.item(row, 2).setText('3'),  # n_features
                            tw2_fr1.item(row, 6).setText('-'), inr(tw2_fr1.item(row, 6), FLAG_not_enabled),
                            tw2_fr1.item(row, 8).setText('-'), inr(tw2_fr1.item(row, 8), FLAG_not_enabled),
                            tw2_fr1.item(row, 9).setText('-'), inr(tw2_fr1.item(row, 9), FLAG_not_enabled),
                            tw2_fr1.item(row, 10).setText('-'), inr(tw2_fr1.item(row, 10), FLAG_not_enabled),
                            tw2_fr1.item(row, 11).setText('-'), inr(tw2_fr1.item(row, 11), FLAG_not_enabled),
                            tw2_fr1.cellWidget(row, 12).setEnabled(False),
                        ]) or (status == 'make_circle') and ([
                            tw2_fr1.item(row, 7).setText(str(DEFAULT_VALUE[6])),
                        ]) or (status == 'make_spheres') and ([
                            tw2_fr1.item(row, 7).setText(str(DEFAULT_VALUE[6])),
                            tw2_fr1.item(row, 2).setText('3'),  # n_features
                            tw2_fr1.item(row, 9).setText('-'), inr(tw2_fr1.item(row, 9), FLAG_not_enabled),
                            tw2_fr1.item(row, 10).setText('-'), inr(tw2_fr1.item(row, 10), FLAG_not_enabled),
                            tw2_fr1.item(row, 11).setText('-'), inr(tw2_fr1.item(row, 11), FLAG_not_enabled)
                        ])
                    ]),
                    tw2_fr1.setCellWidget(tw2_fr1.rowCount() - 1, 0, cb),
                    [[twi := QTableWidgetItem(), twi.setToolTip(switch_tootip_tw2_fr1[i - 1]),
                      tw2_fr1.setItem(tw2_fr1.rowCount() - 1, i, twi)] for i in range(1, 12)],
                    tw2_fr1.setCellWidget(tw2_fr1.rowCount() - 1, 12, QCheckBox(toolTip=switch_tootip_tw2_fr1[11])),
                    tw2_fr1.setCellWidget(tw2_fr1.rowCount() - 1, 13, QCheckBox(toolTip=switch_tootip_tw2_fr1[12])),
                    cb.addItems(['make_blobs', 'make_circles', 'make_moons', 'make_dna', 'make_spheres']),
                    pb4_fr1.setVisible(True),
                    pb3_fr1.setVisible(True)
                ]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

                pb4_fr1 = QPushButton("Удалить запись", objectName='pb4_fr1', visible=False,
                                      clicked=lambda state: (tw2_fr1.rowCount() > 0 and tw2_fr1.currentRow() > -1) and
                                                            [tw2_fr1.removeRow(tw2_fr1.currentRow()),
                                                             (tw2_fr1.rowCount() == 0) and [pb4_fr1.setVisible(False),
                                                                                            pb3_fr1.setVisible(False)]])
                gl.addWidget(pb4_fr1, 1, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

                pb3_fr1 = QPushButton("Сгенерировать набор данных", objectName='pb3_fr1', visible=False,
                                      clicked=lambda state: self.handler_tw2_fr1(tw2_fr1, cnv1_fr1, cnv2_fr1,
                                                                                 grid.parentWidget().findChild(QFrame,
                                                                                                               'frame2').findChild(
                                                                                     QRadioButton, 'rb1_fr2'),
                                                                                 alabel_gen,
                                                                                 grid.parentWidget().findChild(QFrame,
                                                                                                               'frame3')))
                gl.addWidget(pb3_fr1, 18, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                # -----------------------------------------------------------------------------------------------------#
                dockWidget.widget().widget().layout().addItem(
                    QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
            case 2:
                frame.setFixedHeight(155)
                gl1_fr2 = QGridLayout()
                dockWidget = QDockWidget('Загрузка данных', objectName='DW' + str(index_frame),
                                         features=QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                                                  QDockWidget.DockWidgetFeature.DockWidgetMovable,
                                         widget=QScrollArea(widgetResizable=True, widget=QWidget(layout=gl1_fr2)))
                gl1_fr2.addWidget(QRadioButton("1. Сгенерировать и кластеризовать данные",
                                               objectName='rb1_fr2', checked=False, toggled=lambda state: [
                        gl11_fr2.parentWidget().setVisible(False),
                        grid.parentWidget().findChild(QWidget, 'widget_image').setVisible(False),
                        grid.parentWidget().findChild(QFrame, 'frame1').setEnabled(True),
                        # grid.itemAtPosition(2 + 1, 0).widget().setEnabled(True)
                    ]), 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                gl1_fr2.addWidget(QRadioButton("2. Загрузить данные", objectName='rb2_fr2', checked=True,
                                               toggled=lambda state: gl11_fr2.parentWidget().setVisible(True)),
                                  1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                gl11_fr2 = QGridLayout()
                gl1_fr2.addWidget(QWidget(layout=gl11_fr2, objectName='wg1_fr2'),
                                  2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                gl11_fr2.addWidget(QLabel("Набор данных: ", objectName='lb1_fr2'),
                                   0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                gl11_fr2.addWidget(QLineEdit(dockWidget.widget().widget(), objectName='le1_fr2'),
                                   0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
                gl11_fr2.addWidget(
                    QPushButton("Выбрать", objectName='pb1_fr2', statusTip="Выбор", clicked=self.clickSelectData),
                    0, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
            case 3:
                frame.setEnabled(False)
                grid_frame4 = QGridLayout()
                dockWidget = QDockWidget('Кластеризация данных', frame, objectName='DW' + str(index_frame),
                                         baseSize=QSize(100, 300),
                                         features=QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                                                  QDockWidget.DockWidgetFeature.DockWidgetMovable,
                                         widget=QScrollArea(widgetResizable=True, widget=QWidget(layout=grid_frame4)))
                dockWidget.dockLocationChanged.connect(lambda status: (status == Qt.DockWidgetArea.NoDockWidgetArea)
                                                                      and (dockWidget.setMinimumWidth(
                    200) or dockWidget.setMinimumHeight(500)) or
                                                                      dockWidget.setMinimumWidth(
                                                                          100) or dockWidget.setMinimumHeight(100))
                # -----------------------------------------------------------------------------------------------------#
                gl1_fr3 = QGridLayout()
                grid_frame4.addWidget(QWidget(layout=gl1_fr3, objectName='wg1_fr3'),
                                      0, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
                gl1_fr3.addWidget(QLabel("Выберите алгоритмы кластеризации: ", objectName='lb1_fr3'),
                                  0, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
                tw3_fr3 = QTableWidget(visible=True, objectName='tw3_fr3', columnCount=4, rowCount=15,
                                       minimumSize=QSize(300, 350),
                                       verticalHeaderLabels=["00| used", "01| n_cluster", "02| branching_factor",
                                                             "03| threshold",
                                                             "04| compute_labels", "05| copy", "06| max_node_entries",
                                                             "07| diameter",
                                                             "08| entry_size_limit", "09| diameter_multiplier",
                                                             "10| type_measurement", "11| ccore",
                                                             "12| n_represent_points", "13| compression", "14| eps"],
                                       horizontalHeaderLabels=["BIRCH_S", "BIRCH_P", "CURE", "ROCK"])
                tw3_fr3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                tw3_fr3.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                addItemOpen = lambda i, j: \
                    (i in [0, 4, 5, 11]) and (tw3_fr3.setCellWidget(i, j, QCheckBox(checked=False))) or \
                    (i in [10]) and ([cb := QComboBox(),
                                      cb.addItems(["Euclidean", "Manhattan", "Inter", "Intra", "Increase"]),
                                      tw3_fr3.setCellWidget(i, j, cb)]) \
                    or [twi := QTableWidgetItem(),
                        twi.setText(DEFAULT_VALUE_TW3[i]),  # Установка значений по умолчанию.
                        tw3_fr3.setItem(i, j, twi)]
                addItemClose = lambda i, j: [tw := QTableWidgetItem(), tw.setText('-'),
                                             tw.setFlags(~Qt.ItemFlag.ItemIsEnabled), tw3_fr3.setItem(i, j, tw)]
                switch_case_components = [
                    {0: True, 1: True, 2: True, 3: True, 4: True, 5: True},
                    # Column 0: BIRCH_S; Row: [0, 1, 2, 3] - True overwise False .get();
                    {0: True, 1: True, 2: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True},
                    # Column 1: BIRCH_P
                    {0: True, 1: True, 11: True, 12: True, 13: True},  # Column 2: CURE
                    {0: True, 1: True, 3: True, 11: True, 14: True}  # Column 3: ROCK
                ]
                [switch_case_components[j].get(i, False) and [addItemOpen(i, j)] or [addItemClose(i, j)]
                 for j in range(4) for i in range(15)]
                gl1_fr3.addWidget(tw3_fr3, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                # -----------------------------------------------------------------------------------------------------#
                # Виджет установки параметров кластеризации изображения
                asubgrid2 = QGridLayout()
                grid_frame4.addWidget(QWidget(visible=False, objectName='widget_image', layout=asubgrid2), 1, 0, 1, 2,
                                      Qt.AlignmentFlag.AlignLeft)
                # По этому имени потом находится объект и делается видимым в функции handler_frame.
                asubgrid2.addWidget(QLabel("Выберите тип конвертации изображения: ", objectName='alb2_fr3'), 1, 0,
                                    1, 1, Qt.AlignmentFlag.AlignLeft)
                acb1 = QComboBox(objectName='acb1_fr3')
                acb1.addItems(['None(used rashape)', 'HSV', 'HLS', 'YUV'])
                asubgrid2.addWidget(acb1, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
                # -----------------------------------------------------------------------------------------------------#
                spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                grid_frame4.addItem(spacer)
                # -----------------------------------------------------------------------------------------------------#
        qmw.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dockWidget)

    '''
        @brief  Проверка возможности преобразования типа к float.
    '''

    def is_float(self, element: any) -> bool:
        # If you expect None to be passed:
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    '''
        @brief  Обработчик таблицы tw2_fr1 (Задание параметров генерации данных make_* функций).
    '''

    def handler_tw2_fr1(self, table: QTableWidget, cnv1_ax: FigureCanvasQTAgg,
                        cnv2_ax: FigureCanvasQTAgg, rb13: QRadioButton, lb_res: QLabel, wg: QWidget):
        print(table.rowCount())
        cnv1_ax.figure.clear()
        cnv2_ax.figure.clear()
        cnv1_ax.figure.add_subplot(1, 1, 1)
        cnv2_ax.figure.add_subplot(projection="3d")
        Data = [[], [], []]
        for row in range(table.rowCount()):
            param = table.cellWidget(row, 0).currentText()
            n_samples = int((table.item(row, 1).text().isdigit()) and (table.item(row, 1).text()) or DEFAULT_VALUE[0])
            n_features = int((table.item(row, 2).text().isdigit()) and (table.item(row, 2).text()) or DEFAULT_VALUE[1])
            centers = (table.item(row, 3).text().isdigit()) and int(table.item(row, 3).text()) or DEFAULT_VALUE[2]
            cluster_std = (self.is_float(table.item(row, 4).text())) and float(table.item(row, 4).text()) or \
                          DEFAULT_VALUE[3]
            center_box = (float(self.is_float(table.item(row, 5).text()) and table.item(row, 5).text().split(',')[0] or
                                DEFAULT_VALUE[4][0]),)
            center_box += (float(self.is_float(table.item(row, 5).text()) and
                                 (len(table.item(row, 5).text().split(',')) > 1) and (
                                 table.item(row, 5).text().split(',')[1]) or DEFAULT_VALUE[4][1]),)
            random_state = (table.item(row, 6).text().isdigit()) and int(table.item(row, 7).text()) or DEFAULT_VALUE[5]
            rep1 = table.item(row, 7).text().replace(',', '.')
            factor = self.is_float(rep1) and float(rep1) or DEFAULT_VALUE[6]
            rep2 = table.item(row, 8).text().replace(',', '.')
            noise = (self.is_float(rep2)) and float(rep2) or DEFAULT_VALUE[7]
            rep3 = table.item(row, 9).text().replace(',', '.')
            norm = (self.is_float(rep3)) and float(rep3) or DEFAULT_VALUE[8]
            rep4 = table.item(row, 10).text().replace(',', '.')
            y_step = (self.is_float(rep4)) and float(rep4) or DEFAULT_VALUE[9]
            rep5 = table.item(row, 11).text().replace(',', '.')
            z_step = (self.is_float(rep5)) and float(rep5) or DEFAULT_VALUE[10]
            shuffle = table.cellWidget(row, 12).isChecked()
            return_centers = table.cellWidget(row, 13).isChecked()
            match param:
                case 'make_blobs':
                    data, labels = make_blobs(n_samples=n_samples, n_features=n_features, centers=centers,
                                              cluster_std=cluster_std, center_box=center_box, shuffle=shuffle,
                                              random_state=random_state, return_centers=return_centers)
                case 'make_circles':
                    data, labels = make_circles(n_samples=n_samples, factor=factor, noise=noise,
                                                shuffle=shuffle, random_state=random_state)
                case 'make_moons':
                    data, labels = make_moons(n_samples=n_samples, noise=noise, shuffle=shuffle,
                                              random_state=random_state)
                case 'make_dna':
                    Data, labels = make_dna(n_samples=n_samples, center_box=center_box)
                    data = np.array(Data[0]).transpose()
                    # Data[0] - points, Data[1] - lines;
                case 'make_spheres':
                    Data, labels = make_spheres(n_samples=n_samples, factor=factor, noise=noise,
                                                shuffle=shuffle, random_state=random_state)
                    data = np.array(Data).transpose()

            data /= norm
            match data.shape[1]:
                case 0:
                    pass
                case 1:
                    data_image1 = [x[0] for x in data]
                    data_image2 = [y_step for _ in data]
                    data_image3 = [z_step for _ in data]
                    cnv1_ax.figure.axes[0].scatter(data_image1, data_image2, c=labels)
                    cnv2_ax.figure.axes[0].scatter(data_image1, data_image2, data_image3, c=labels)
                case 2:
                    data_image1 = [x[0] for x in data]
                    data_image2 = [y[1] for y in data]
                    data_image3 = [z_step for _ in data]
                    cnv1_ax.figure.axes[0].scatter(data_image1, data_image2, c=labels)
                    cnv2_ax.figure.axes[0].scatter(data_image1, data_image2, data_image3, c=labels)
                case 3 | _:
                    data_image1 = [x[0] for x in data]
                    data_image2 = [y[1] for y in data]
                    data_image3 = [z[2] for z in data]
                    cnv1_ax.figure.axes[0].scatter(data_image1, data_image2, c=labels)
                    cnv2_ax.figure.axes[0].scatter(data_image1, data_image2, data_image3, c=labels)
            cnv1_ax.draw()
            cnv2_ax.draw()
            rb13.setChecked(True)
            if data.shape[1] > 3:
                s = len(Data[0])
                Data[0] = data_image1
                Data[1] = data_image2
                Data[2] = data_image3
                for j in range(3, len(data[0])):
                    Data.append([])
                    Data[j] += [0.0 for _ in range(s)]
                    Data[j] += [x[j] for x in data]
            elif param in ['make_blobs', 'make_circles', 'make_moons']:
                Data[0] += data_image1
                Data[1] += data_image2
                Data[2] += data_image3
            else:
                Data[0] = data_image1
                Data[1] = data_image2
                Data[2] = data_image3
        self.setProperty('Data', Data)
        cnv1_ax.figure.savefig('image2D.png')
        cnv2_ax.figure.savefig('image3D.png')
        with open('dataPoints.csv', 'w', newline='', encoding='utf-8') as myfile:
            writer = csv.writer(myfile, dialect='excel', delimiter=";",
                                quoting=csv.QUOTE_ALL)  # quoting=csv.QUOTE_ALL
            writer.writerows(Data)  # writer.writerows(data)
        with open('dataLabels.csv', 'w', newline='', encoding='utf-8') as myfile:
            writer = csv.writer(myfile, dialect='excel', delimiter=";",
                                quoting=csv.QUOTE_ALL)  # quoting=csv.QUOTE_ALL
            writer.writerow(labels)  # writer.writerows(data)
            lb_res.setVisible(True)
            wg.setEnabled(True)
            self.button_start.setEnabled(True)

    '''
        @brief  Обработчик кнопки pb5_fr1 (-).
    '''

    def handler_pb5_fr1(self, current_type_dist, labels, lines) -> None:
        labels[0].setText("loc: ")
        labels[0].setToolTip("Среднее (центр) распределения")
        labels[1].setText("scale: ")
        labels[1].setToolTip("Стандартное отклонение")
        labels[1].setVisible(True)
        lines[1].setVisible(True)
        match current_type_dist:
            case 'Нормальное' | 'Биноминальное':
                labels[0].setVisible(True)
                lines[0].setVisible(True)
                if current_type_dist == 'Биноминальное':
                    labels[0].setText("n: ")
                    labels[0].setToolTip("Количество испытаний")
                    labels[1].setText("p: ")
                    labels[1].setToolTip("Вероятность успеха при проведении одного испытания")
            case 'Показательное':
                labels[0].setVisible(False)
                lines[0].setVisible(False)
            case _:
                pass

    '''
        @brief  Обработчик таблицы tw1_fr1 (Задание параметров генерации данных по распределениям).
    '''

    def handler_tw1_fr1(self, start, step, end, type_distribution, table: QTableWidget, pb, labels_ptd,
                        lines_ptd, wg: QWidget, seed: -1):
        pos = start - 1
        param1 = labels_ptd[0].text()
        param2 = labels_ptd[1].text() + lines_ptd[1].text()
        match type_distribution:
            case 'Нормальное' | 'Биноминальное':
                param1 += lines_ptd[0].text()
            case 'Показательное':  # Экспоненциальное/Гамма
                param1 += '-'
            case _:
                pass

        if seed < 0:
            seed = 'None'
        if end > 0:
            while pos < end:
                table.setItem(pos, 0, QTableWidgetItem(type_distribution))
                if seed is not None:
                    table.setItem(pos, 1, QTableWidgetItem(param1 + "; " + param2 + "; seed: " + str(seed)))
                else:
                    table.setItem(pos, 1, QTableWidgetItem(param1 + "; " + param2))
                pos += step
            count = 0
        if table.rowCount() > 0:
            for i in range(table.rowCount()):
                if table.item(i, 0) is None:
                    continue
                else:
                    count += 1
            if count == table.rowCount():
                pb.setVisible(True)
        wg.setEnabled(True)
        self.button_start.setEnabled(True)

    '''
        @brief  Обработчик кнопки pb6_fr1 (Генерация набора данных).
    '''

    def handler_pb6_fr1(self, count_point, dim_space, table, label_gen, cnv1_ax: FigureCanvasQTAgg,
                        cnv2_ax: FigureCanvasQTAgg, rb13: QRadioButton, wg: QWidget):
        # LIST_TYPE_DISTRIBUTION
        if count_point == 0 or dim_space == 0 or table is None:
            return
        # TODO; Код для генерациии распределения;
        data_image1 = []
        data_image2 = []
        Data = [[], [], []]
        try:
            for i in range(dim_space):
                val = table.item(i, 1).text().split(';')
                param1 = val[0].split(':')[1]
                param1 = param1.replace(',', '.')
                if param1 == ' -':
                    param1 = 0
                param1 = float(param1) ##
                param2 = float(val[1].split(':')[1].replace(',', '.'))
                seed = (val[2].split(':')[1] != ' None') and (int(val[2].split(':')[1])) or None
                rand = np.random.RandomState(seed)
                rand.seed(seed)
                switch_case = {
                    'Нормальное': rand.normal(param1, param2, size=(count_point, 1)),
                    'Биноминальное': rand.binomial(param1, param2, size=(count_point, 1)),
                    'Показательное': rand.exponential(param2, size=(count_point, 1)),
                }
                data = switch_case[table.item(i, 0).text()].tolist()
                if i < 1:
                    data_image1 = [x[0] for x in data]
                    data_image2 = [0.0 for _ in data]
                    data_image3 = [0.0 for _ in data]
                    cnv1_ax.figure.clear()
                    cnv1_ax.figure.add_subplot(1, 1, 1)
                    cnv1_ax.figure.axes[0].scatter(data_image1, data_image2, c='r')
                    cnv1_ax.draw()
                elif i == 1:
                    data_image2 = [x[0] for x in data]
                    data_image3 = [0.0 for _ in data]
                    cnv1_ax.figure.clear()
                    cnv1_ax.figure.add_subplot(1, 1, 1)
                    cnv1_ax.figure.axes[0].scatter(data_image1, data_image2, c='r')
                    cnv1_ax.draw()
                elif i == 2:
                    data_image3 = [x[0] for x in data]
                    cnv2_ax.figure.clear()
                    cnv2_ax.figure.add_subplot(projection="3d")
                    cnv2_ax.figure.axes[0].scatter(data_image1, data_image2, data_image3, c='r')
                    cnv2_ax.draw()
            label_gen.setVisible(True)
            rb13.setChecked(True)
            wg.setEnabled(True)
            self.button_start.setEnabled(True)
            if i > 3:
                s = len(Data[0])
                Data[0] += data_image1
                Data[1] += data_image2
                Data[2] += data_image3
                for j in range(3, len(data[0])):
                    Data.append([])
                    Data[j] += [0.0 for _ in range(s)]
                    Data[j] += [x[j] for x in data]
            else:
                Data[0] += data_image1
                Data[1] += data_image2
                Data[2] += data_image3
            if dim_space < 3:
                cnv2_ax.figure.clear()
                cnv2_ax.figure.add_subplot(projection="3d")
                cnv2_ax.figure.axes[0].scatter(data_image1, data_image2, data_image3, c='r')
                cnv2_ax.draw()
            self.setProperty('Data', Data)
            with open('dataPoints.csv', 'w', newline='', encoding='utf-8') as myfile:
                writer = csv.writer(myfile, dialect='excel', delimiter=";",
                                    quoting=csv.QUOTE_ALL)  # quoting=csv.QUOTE_ALL
                writer.writerow(Data)  # writer.writerows(data)
            with open('dataLabels.csv', 'w', newline='', encoding='utf-8') as myfile:
                writer = csv.writer(myfile, dialect='excel', delimiter=";",
                                    quoting=csv.QUOTE_ALL)  # quoting=csv.QUOTE_ALL
                writer.writerow(Data)  # writer.writerows(data)
                label_gen.setVisible(True)
        except:
            self.statusBar().showMessage(
                f'При данных параметрах кластеризация не возможна. Попробуйте уменьшить размерность или количество фитч!')

    '''
        @brief  Кластеризация данных.
    '''

    def clickStartClustering(self):
        grid: QGridLayout = self.widget1.findChild(QGridLayout, 'gridBase')
        frame2: QFrame = grid.parentWidget().findChild(QFrame, 'frame2')  # grid.itemAtPosition(3 + 1, 0).widget()
        rb1_fr2: QRadioButton = frame2.findChild(QRadioButton, 'rb1_fr2')
        frame1: QFrame = grid.parentWidget().findChild(QFrame, 'frame1')  # grid.itemAtPosition(2 + 1, 0).widget()
        frame3: QFrame = grid.parentWidget().findChild(QFrame, 'frame3')  # grid.itemAtPosition(4 + 1, 0).widget()
        # rb2_fr1: QRadioButton = frame1.findChild(QRadioButton, 'rb2_fr1')
        srb1_fr1: QRadioButton = frame1.findChild(QRadioButton, 'srb1_fr1')
        srb2_fr1: QRadioButton = frame1.findChild(QRadioButton, 'srb2_fr1')
        tw3: QTableWidget = frame3.findChild(QTableWidget, 'tw3_fr3')
        switch_case_componentsl = {0: 'sub_birch_s1', 1: 'sub_birch_p1', 2: 'sub_cure_1', 3: 'sub_rock_1'}
        Param = []
        for j in range(tw3.columnCount()):
            Param.append(list())
            for i in range(tw3.rowCount()):
                item = tw3.cellWidget(i, j)
                if item == None:
                    item = tw3.item(i, j)
                    if item == None:
                        Param[j] += [None]
                    else:
                        if self.is_float(tw3.item(i, j).text()):
                            Param[j] += [float(tw3.item(i, j).text())]
                        elif tw3.item(i, j).text() in ['-', '', ' ']:
                            Param[j] += [None]
                        else:
                            Param[j] += [int(tw3.item(i, j).text())]
                else:
                    if isinstance(item, QCheckBox):
                        Param[j] += [item.isChecked()]
                    elif isinstance(item, QComboBox):
                        Param[j] += [item.currentText()]
        # print(Param)
        if rb1_fr2.isChecked():  # Кластеризация точек
            if srb2_fr1.isChecked() or srb1_fr1.isChecked():  # rb2_fr1.isChecked()
                Data = self.property('Data')  # Получение данных
                for i in range(len(Param)):
                    #try:
                        used = Param[i].pop(0)
                        if used and Param[i].count(None) + Param[i].count('') != tw3.rowCount():
                            match i:
                                case 0:  # BIRCH_S clustering
                                    context = Context(ConcreteStrategyBIRCH_from_SKLEARN_LEARN())
                                case 1:  # BIRCH_P clustering
                                    context = Context(ConcreteStrategyBIRCH_from_PYCLUSTERING())
                                case 2:  # CURE clustering
                                    context = Context(ConcreteStrategyCURE())
                                case 3:  # ROCK clustering
                                    context = Context(ConcreteStrategyROCK())
                            self._mdiarea.findChild(QMdiSubWindow, switch_case_componentsl[i]).setVisible(True)
                            tic = time.process_time()
                            labels = context.do_some_clustering_points(Data, Param[i])
                            toc = time.process_time()
                            elapsed = toc - tic
                            qmv: QMdiSubWindow = self._mdiarea.findChild(QMdiSubWindow, switch_case_componentsl[i])
                            spl: QSpliter = qmv.layout().itemAt(1).widget()
                            qmvv: QMainWindow = spl.layoutContentArea().itemAt(0).widget()
                            tw: QTableWidget = qmvv.findChild(QTableWidget, 'stw')
                            tw.setItem(0, 1, QTableWidgetItem(str(elapsed)))
                            C = converter_to_c(np.array(Data).transpose().tolist(), labels)
                            dunn = DunnIndex(C)
                            tw.setItem(1, 1, QTableWidgetItem(str(dunn)))
                            dunnMean = DunnIndexMean(C)
                            tw.setItem(2, 1, QTableWidgetItem(str(dunnMean)))
                            #dbi = DBi(C, 0, 0, 1, 1)
                            #tw.setItem(3, 1, QTableWidgetItem(str(dbi)))
                            cnv11 = self._mdiarea.findChild(QWidget, 'cnv' + str(i + 1) + '1_wg') \
                                .layout().itemAtPosition(1, 0).widget().findChild(QDockWidget, 'dw1') \
                                .widget().layout().itemAtPosition(0, 0).widget()
                            qmv1 = self._mdiarea.findChild(QWidget, 'cnv' + str(i + 1) + '1_wg') \
                                .layout().itemAtPosition(1, 1).widget()
                            cnv12 = qmv1.findChild(QDockWidget, 'dw2') \
                                .widget().layout().itemAtPosition(0, 0).widget()
                            cnv11.figure.clear()
                            cnv11.figure.add_subplot(1, 1, 1)
                            cnv11.figure.axes[0].scatter(Data[0], Data[1], c=labels,
                                                         cmap="rainbow")  # c=scatter.cmap(0.7) # jet
                            cnv11.draw()
                            qmv1.setVisible(True)
                            cnv12.figure.clear()
                            cnv12.figure.add_subplot(projection="3d")
                            cnv12.figure.axes[0].scatter(Data[0], Data[1], Data[2], c=labels, cmap="rainbow")
                            cnv12.draw()
                        else:
                            self._mdiarea.findChild(QMdiSubWindow, switch_case_componentsl[i]).setVisible(False)
                        self.statusBar().showMessage('Кластеризация успешно проведена!')
                    #except:
                        #self.statusBar().showMessage(
                            #f'При данных параметрах кластеризация {switch_case_componentsl[i]} не возможна!')
        else:  # Кластеризация изображений
            acb1_fr3: QComboBox = frame3.findChild(QComboBox, 'acb1_fr3')
            # print(acb1_fr3.currentIndex(), acb1_fr3.currentText())
            le1_fr2 = self.widget1.findChild(QLineEdit, 'le1_fr2')
            image_path = le1_fr2.text()
            if acb1_fr3.currentIndex() > 0:
                image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            match acb1_fr3.currentIndex():
                case 0:  # None
                    image = Image.open(image_path)
                    image = np.array(image)
                    pixels = image.reshape((-1, 3))
                case 1:  # HSV
                    pixels = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                case 2:  # HLS
                    pixels = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
                case 3:  # YUV
                    pixels = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
            for i in range(len(Param)):
                try:
                    # print(switch_case_componentsl[i])
                    used = Param[i].pop(0)
                    self.setStatusTip(switch_case_componentsl[i])
                    buff = Param[i].copy()
                    buff.pop(9)  # QComboBox
                    if used and buff.count(None) + buff.count('') + buff.count(False) != tw3.rowCount() - 1:
                        self._mdiarea.findChild(QMdiSubWindow, switch_case_componentsl[i]).setVisible(True)
                        match i:
                            case 0:  # BIRCH_S clustering
                                context = Context(ConcreteStrategyBIRCH_from_SKLEARN_LEARN())
                            case 1:  # BIRCH_P clustering
                                context = Context(ConcreteStrategyBIRCH_from_PYCLUSTERING())
                            case 2:  # CURE clustering
                                context = Context(ConcreteStrategyCURE())
                            case 3:  # ROCK clustering
                                context = Context(ConcreteStrategyROCK())
                        tic = time.process_time()
                        labels = context.do_some_clustering_image(pixels, Param[i], acb1_fr3.currentIndex())
                        toc = time.process_time()
                        clustered_image = labels.reshape(image.shape[:2])
                        elapsed = toc - tic
                        qmv: QMdiSubWindow = self._mdiarea.findChild(QMdiSubWindow, switch_case_componentsl[i])
                        spl: QSpliter = qmv.layout().itemAt(1).widget()
                        qmvv: QMainWindow = spl.layoutContentArea().itemAt(0).widget()
                        tw: QTableWidget = qmvv.findChild(QTableWidget, 'stw')
                        tw.setItem(0, 1, QTableWidgetItem(str(elapsed)))
                        # C = converter_to_c(pixels.tolist(), labels)    # Оценка изображений отключена
                        # из-за слишком долгого времени расчета.
                        # dunn = DunnIndex(C) # Медленная
                        # tw.setItem(1, 1, QTableWidgetItem(str(dunn)))
                        # dunnMean = DunnIndexMean(C)
                        # tw.setItem(2, 1, QTableWidgetItem(str(dunnMean)))
                        # dbi = DBi(C, 0, 1, 1, 1)
                        # tw.setItem(3, 1, QTableWidgetItem(str(dbi)))
                        cnv11 = self._mdiarea.findChild(QWidget, 'cnv' + str(i + 1) + '1_wg') \
                            .layout().itemAtPosition(1, 0).widget().findChild(QDockWidget, 'dw1') \
                            .widget().layout().itemAtPosition(0, 0).widget()
                        qmv1 = self._mdiarea.findChild(QWidget, 'cnv' + str(i + 1) + '1_wg') \
                            .layout().itemAtPosition(1, 1).widget()
                        cnv12 = qmv1.findChild(QDockWidget, 'dw2') \
                            .widget().layout().itemAtPosition(0, 0).widget()
                        cnv11.figure.clear()
                        cnv11.figure.add_subplot(1, 1, 1)
                        cnv11.figure.axes[0].imshow(image)
                        cnv11.draw()
                        qmv1.setVisible(True)
                        cnv12.figure.clear()
                        cnv12.figure.add_subplot(1, 1, 1)
                        cnv12.figure.axes[0].imshow(clustered_image)
                        cnv12.draw()
                    else:
                        self._mdiarea.findChild(QMdiSubWindow, switch_case_componentsl[i]).setVisible(False)
                    self.statusBar().showMessage(f'Кластеризация успешно проведена!')
                except:
                    self.statusBar().showMessage(
                        f'При данных параметрах кластеризация {switch_case_componentsl[i]} не возможна!')
        self._mdiarea.tileSubWindows()

    '''
        @brief  Загрузка изображений.
    '''

    def clickSelectData(self):
        str = "Image (*.png *.jpg *jpeg)"  # ;; Excel (*.csv *.xlsx)
        file, filter = QFileDialog.getOpenFileName(self, 'Open file', None, str)
        le1_fr2 = self.widget1.findChild(QLineEdit, 'le1_fr2')
        le1_fr2.setText(file)
        arr1 = file.split('/')
        format_file = arr1[-1].split('.')[-1]
        self.setProperty('format_file', format_file)
        self.handler_fr3()

    '''
        @brief  Переключение между frame1 и frame2.
    '''

    def switch_frame1_frame2(self, button_id):
        frame1 = self.widget1.findChild(QFrame, 'frame1')
        frame2 = self.widget1.findChild(QFrame, 'frame2')
        match button_id.objectName():
            case 'radioButton1':
                frame1.setVisible(True)
                frame2.setVisible(False)
            case 'radioButton2':
                frame1.setVisible(False)
                frame2.setVisible(True)
            case _:
                pass

    '''
        @brief  Захват левой кнопкой мыши нижнего правого уголка/рамки окна для последующего изменения его размеров.
    '''

    def mousePressEvent(self, event: QMouseEvent):
        self.setProperty('dragPos', event.globalPosition().toPoint())
        self.cursor1.setShape(Qt.CursorShape.ClosedHandCursor)

    '''
        @brief  Изменение размеров окна в захваченом состоянии нижнего правого уголка/рамки окна.
    '''

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.cursor1.shape() == Qt.CursorShape.ClosedHandCursor:
            self.move(self.pos() + event.globalPosition().toPoint() - self.property('dragPos'))
            self.setProperty('dragPos', event.globalPosition().toPoint())
            event.accept()

    '''
        @brief  Завершение изменения размеров окна(Отпускание левой кнопки мыши при захвате нижнего правого уголка/рамки окна приложения).
    '''

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.cursor1.setShape(Qt.CursorShape.OpenHandCursor)

    '''
        @brief  Изменение темы приложения на первую.
    '''

    def changeFirstTheme(self, Color, message):
        self.changeTheme(Color, 'theme_first', message)

    '''
        @brief  Изменение темы приложения на вторую.
    '''

    def changeSecondTheme(self, Color, message):
        self.changeTheme(Color, 'theme_second', message)

    '''
        @brief  Изменение темы приложения.
    '''

    def changeTheme(self, Color, theme, message):
        styleApp = Loader.change_color_theme(theme, Color.name(), message)
        if self.property('theme_current') == theme:
            self.setStyleSheet(styleApp)
            if self.dialog is not None:
                self.dialog.setStyleSheet(styleApp)
                self.sliderButton_install_style()
        self.dialog.updateframes(message)

    '''
        @brief  Установка стиля для переключателя тем.
    '''

    def sliderButton_install_style(self):
        style = self.styleSheet()
        css = qstylizer.parser.parse(style)
        match not self.sldbtn.getStatus():
            case 0:
                self.sldbtn.setBgColor(css['QSliderButton'].backgroundColor.value)
                self.sldbtn.setColor(css['QSliderButton'].color.value)
            case 1:
                self.sldbtn.setOffBgColor(css['QSliderButton'].backgroundColor.value)
                self.sldbtn.setOffColor(css['QSliderButton'].color.value)
        self.sldbtn.repaint()

    '''
        @brief  Переключение между темами.
    '''

    def clickSliderButtonBool(self, status: bool):
        self.change_path_style_app(status)
        self.sliderButton_install_style()
        self._mdiarea.tileSubWindows()

    '''
        @brief  Открытие окна настроек для последующего их изменения.
    '''

    def ChangeSettingsClick(self):
        self.dialog = SettingsApp(self.styleSheet())
        self.dialog.changeThemeDark.connect(self.changeFirstTheme)
        self.dialog.changeThemeLight.connect(self.changeSecondTheme)
        self.dialog.closed.connect(self.closedDialog)
        self.dialog.show()

    '''
        @brief  Закрытие окна настроек с последующим его удалением.
    '''

    def closedDialog(self):
        del self.dialog
        self.dialog = None

    '''
        @brief  Изменение темы приложения.
    '''

    def change_path_style_app(self, status) -> None:
        settings = QSettings()
        settings.beginGroup("StyleSettings")
        settings.setValue("theme_current", ('theme_first', 'theme_second')[status])
        settings.endGroup()
        [styleApp, theme_current] = loader_settings()
        self.setProperty('theme_current', theme_current)
        self.setStyleSheet(styleApp)
        if self.dialog is not None:
            self.dialog.setStyleSheet(self.styleSheet())
        self.sliderButton_install_style()


# [1.5]
'''
    @brief  Точка входа в приложение.
'''
if __name__ == "__main__":
    init_config_app()  # Инициализация метаданных приложения для возможности обращения по ним к реестру ОС
    # и получение информации о текущей теме
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    [qAppStyle, current_theme] = loader_settings()
    mw = MainWindow(qAppStyle, current_theme)
    mw.show()
    sys.exit(app.exec())
