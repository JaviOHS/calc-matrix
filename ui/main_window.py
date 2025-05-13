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
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Inicializar managers
        self.matrix_manager = MatrixManager()
        self.polynomial_manager = PolynomialManager()
        self.vector_manager = VectorManager()
        self.graph_manager = GraphManager()
        self.symbolic_calculation_manager = SymCalManager()

        self.setup_window() # Configuración de la ventana
        self.setup_ui() # Inicializar UI
        
        # Inicializar páginas
        self.pages = {}
        self.current_page = None
        self.show_page("home")

    def setup_window(self):
        """Configurar propiedades básicas de la ventana"""
        self.resize(1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized() # Maximizar ventana al iniciar

    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal sin márgenes 
        self.layout = QHBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setup_sidebar() # Configurar sidebar
        self.setup_page_container() # Configurar contenedor principal

    def setup_sidebar(self):
        """Configurar la barra lateral"""
        self.sidebar = Sidebar(self.show_page)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout.addWidget(self.sidebar)
        self.sidebar.setMinimumWidth(200)
        # self.sidebar.setVisible(False)  # Para sidebar oculto por defecto

    def setup_page_container(self):
        """Configurar el contenedor de páginas"""
        # Contenedor de páginas con encabezado y contenido
        self.page_container = QWidget()
        self.page_container_layout = QVBoxLayout(self.page_container)
        self.page_container_layout.setContentsMargins(0, 0, 0, 0)
        self.page_container_layout.setSpacing(0)

        # Configurar barra de navegación superior
        username = f'@{getpass.getuser().capitalize()}'
        self.navbar = TopNavbar(self, self.toggle_sidebar, username=username)
        self.page_container_layout.addWidget(self.navbar)

        # Widget de contenido real (donde irán las páginas)
        self.page_widget = QWidget()
        self.page_layout = QVBoxLayout(self.page_widget)
        self.page_layout.setContentsMargins(0, 0, 0, 0)

        self.page_container_layout.addWidget(self.page_widget)
        self.layout.addWidget(self.page_container)

    def toggle_sidebar(self):
        """Alternar la visibilidad de la barra lateral"""
        visible = self.sidebar.isVisible()
        self.sidebar.setVisible(not visible)

    def show_page(self, name):
        """Cambiar a la página especificada"""
        # Limpiar la página actual
        for i in reversed(range(self.page_layout.count())):
            widget = self.page_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Crear la página si no existe
        if name not in self.pages:
            self.create_page(name)
        
        # Mostrar la página
        self.current_page = self.pages[name]
        self.page_layout.addWidget(self.current_page)
        self.sidebar.set_active_button(name)
    
    def create_page(self, name):
        """Crear una nueva página según el nombre"""
        if name == "home":
            self.pages[name] = MainHomePage(navigate_callback=self.show_page)
        elif name == "matrix":
            self.pages[name] = MatrixPage(self.matrix_manager)
        elif name == "polynomial":
            self.pages[name] = PolynomialPage(self.polynomial_manager)
        elif name == "vector":
            self.pages[name] = VectorPage(self.vector_manager)
        elif name == "graph":
            self.pages[name] = GraphPage(self.graph_manager)
        elif name == "sym_cal":
            self.pages[name] = SymCalPage(self.symbolic_calculation_manager)
        elif name == "about":
            self.pages[name] = AboutPage()
        else:
            raise ValueError(f"Página '{name}' no reconocida.")
        