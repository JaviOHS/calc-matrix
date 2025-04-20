from ui.sidebar import Sidebar

from ui.pages.home_page import HomePage
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

matrix_manager = MatrixManager()
polynomial_manager = PolynomialManager()
vector_manager = VectorManager()
graph_manager = GraphManager()
symbolic_calculation_manager = SymCalManager()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CalcMatrix")
        self.resize(1000, 600)

        # Widget central 
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal sin márgenes 
        self.layout = QHBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Sidebar con nombre de objeto para aplicar estilos desde QSS 
        self.sidebar = Sidebar(self.show_page)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout.addWidget(self.sidebar)
        self.sidebar.setMinimumWidth(200)
        
        # Contenedor de páginas 
        self.page_container = QWidget()
        self.page_layout = QVBoxLayout(self.page_container)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.page_container)
         
        self.pages = {} # Diccionario de páginas

        self.current_page = None # Página actual
        self.show_page("home")

    def show_page(self, name):
        # Eliminar página 
        for i in reversed(range(self.page_layout.count())):
            widget = self.page_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Agregar nueva página 
        if name not in self.pages:
            if name == "home":
                self.pages[name] = HomePage()
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
