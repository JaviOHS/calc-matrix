from utils.resources import resource_path
from ui.sidebar import Sidebar
from ui.navbar import TopNavbar
import getpass

from ui.pages.home_page import MainHomePage
from ui.pages.matrix_page.matrix_page import MatrixPage
from ui.pages.poly_page.poly_page import PolynomialPage
from ui.pages.vector_page.vector_page import VectorPage
from ui.pages.graph_page.graph_page import GraphPage
from ui.pages.sym_cal_page.sym_cal_page import SymCalPage
from ui.pages.about_page import AboutPage

from model.matrix_manager import MatrixManager
from model.polynomial_manager import PolynomialManager
from model.vector_manager import VectorManager
from model.graph_manager import GraphManager
from model.sym_cal_manager import SymCalManager

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QIcon

matrix_manager = MatrixManager()
polynomial_manager = PolynomialManager()
vector_manager = VectorManager()
graph_manager = GraphManager()
symbolic_calculation_manager = SymCalManager()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon(resource_path("assets/icons/ico.ico")))
        self.setWindowTitle("CalcMatrix")
        self.resize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal sin márgenes 
        self.layout = QHBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.sidebar = Sidebar(self.show_page)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout.addWidget(self.sidebar)
        self.sidebar.setMinimumWidth(200)

        # Para sidebar oculto por defecto
        # self.sidebar.setVisible(False)

        # Contenedor de páginas con encabezado y contenido
        self.page_container = QWidget()
        self.page_container_layout = QVBoxLayout(self.page_container)
        self.page_container_layout.setContentsMargins(0, 0, 0, 0)
        self.page_container_layout.setSpacing(0)

        username = f'@{getpass.getuser()}'
        self.navbar = TopNavbar(self.toggle_sidebar, username=username.upper())
        self.page_container_layout.addWidget(self.navbar)

        # Widget de contenido real (donde irán las páginas)
        self.page_widget = QWidget()
        self.page_layout = QVBoxLayout(self.page_widget)
        self.page_layout.setContentsMargins(0, 0, 0, 0)

        self.page_container_layout.addWidget(self.page_widget)
        self.layout.addWidget(self.page_container)
         
        self.pages = {} # Diccionario de páginas

        self.current_page = None # Página actual
        self.show_page("home")

    def toggle_sidebar(self):
        visible = self.sidebar.isVisible()
        self.sidebar.setVisible(not visible)

    def show_page(self, name):
        for i in reversed(range(self.page_layout.count())):
            widget = self.page_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Agregar nueva página 
        if name not in self.pages:
            if name == "home":
                self.pages[name] = MainHomePage(navigate_callback=self.show_page) # IMPORTANTE: 
            elif name == "matrix":
                self.pages[name] = MatrixPage(matrix_manager)
            elif name == "polynomial":
                self.pages[name] = PolynomialPage(polynomial_manager)
            elif name == "vector":
                self.pages[name] = VectorPage(vector_manager)
            elif name == "graph":
                self.pages[name] = GraphPage(graph_manager)
            elif name == "sym_cal":
                self.pages[name] = SymCalPage(symbolic_calculation_manager)
            elif name == "about":
                self.pages[name] = AboutPage()
            else:
                raise ValueError(f"Página '{name}' no reconocida.")
        
        self.current_page = self.pages[name]
        self.page_layout.addWidget(self.current_page)
