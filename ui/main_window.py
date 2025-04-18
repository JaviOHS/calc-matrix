from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
from ui.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.matrix_page.matrix_page import MatrixPage
from ui.pages.polynomial_page.polynomial_page import PolynomialPage
from ui.pages.vector_page import VectorPage
from ui.pages.graph_page import GraphPage
from ui.pages.derivative_page import DerivativePage
from ui.pages.integral_page import IntegralPage
from ui.pages.about_page import AboutPage

from model.matrix_manager import MatrixManager

manager = MatrixManager()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CalcMatrix")
        self.resize(1000, 600)

        # ---------- Widget central ----------
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ---------- Layout principal sin márgenes ----------
        self.layout = QHBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)  # <-- importante para diseño limpio
        self.layout.setSpacing(0)

        # ---------- Sidebar con nombre de objeto para aplicar estilos desde QSS ----------
        self.sidebar = Sidebar(self.show_page)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout.addWidget(self.sidebar)
        self.sidebar.setMinimumWidth(200)
        
        # ---------- Contenedor de páginas ----------
        self.page_container = QWidget()
        self.page_layout = QVBoxLayout(self.page_container)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.page_container)
        # Color de fondo para el contenedor de páginas
        # self.page_container.setStyleSheet("background-color: #f0f0f0;")

        # ---------- Diccionario de páginas ----------
        self.pages = {}

        self.current_page = None
        self.show_page("home")

    def show_page(self, name):
        # ---------- Eliminar página ----------
        for i in reversed(range(self.page_layout.count())):
            widget = self.page_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # ---------- Agregar nueva página ----------
        if name not in self.pages:
            if name == "home":
                self.pages[name] = HomePage()
            elif name == "matrix":
                self.pages[name] = MatrixPage(manager)
            elif name == "polynomial":
                self.pages[name] = PolynomialPage()
            elif name == "vector":
                self.pages[name] = VectorPage()
            elif name == "graph":
                self.pages[name] = GraphPage()
            elif name == "derivative":
                self.pages[name] = DerivativePage()
            elif name == "integral":
                self.pages[name] = IntegralPage()
            elif name == "about":
                self.pages[name] = AboutPage()
            else:
                raise ValueError(f"Página '{name}' no reconocida.")
        
        self.current_page = self.pages[name]
        self.page_layout.addWidget(self.current_page)
