from ui.sidebar import Sidebar
from ui.navbar import TopNavbar
import getpass

from ui.pages.home_page import MainHomePage
from ui.pages.matrix_page.matrix_page import MatrixPage
from ui.pages.poly_page.poly_page import PolynomialPage
from ui.pages.vector_page.vector_page import VectorPage
from ui.pages.graph_page.graph_page import GraphPage
from ui.pages.sym_cal_page.sym_cal_page import SymCalPage
from ui.pages.distribution_page.distribution_page import DistributionPage
from ui.pages.about_page import AboutPage

from model.matrix_manager import MatrixManager
from model.polynomial_manager import PolynomialManager
from model.vector_manager import VectorManager
from model.graph_manager import GraphManager
from model.sym_cal_manager import SymCalManager
from model.distribution_manager import DistributionManager

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from utils.core.resources import resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.matrix_manager = MatrixManager()
        self.polynomial_manager = PolynomialManager()
        self.vector_manager = VectorManager()
        self.graph_manager = GraphManager()
        self.symbolic_calculation_manager = SymCalManager()
        self.distribution_manager = DistributionManager()

        self.setup_window()
        
        self.pages = {}
        self.current_page = None
        
        self.setup_ui()
        self.show_page("home")
        self.showMaximized()

    def setup_window(self):
        """Configurar propiedades básicas de la ventana"""
        self.resize(1000, 600)
        self.setMinimumSize(456, 637) 
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowIcon(QIcon(resource_path("assets/icons/_ico.ico")))

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

        # Usar QStackedWidget para manejar las páginas
        self.page_widget = QStackedWidget()
        self.page_container_layout.addWidget(self.page_widget)

        self.layout.addWidget(self.page_container)

    def toggle_sidebar(self):
        """Alternar la visibilidad de la barra lateral"""
        visible = self.sidebar.isVisible()
        self.sidebar.setVisible(not visible)

    def show_page(self, name):
        """Cambiar a la página especificada"""
        # Si la página no existe, crearla
        if name not in self.pages:
            self.create_page(name)

        # Cambiar a la página en el QStackedWidget
        self.current_page = self.pages[name]
        index = self.page_widget.indexOf(self.current_page)
        if index == -1:
            self.page_widget.addWidget(self.current_page)
            index = self.page_widget.indexOf(self.current_page)
        
        # Forzar un nuevo evento show para activar la animación
        if self.current_page.isVisible():
            self.current_page.hide()
        self.page_widget.setCurrentIndex(index)
        self.current_page.show()

        # Actualizar el botón activo en la barra lateral
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
        elif name == "distribution":
            self.pages[name] = DistributionPage(self.distribution_manager)
        elif name == "about":
            self.pages[name] = AboutPage()
        else:
            raise ValueError(f"Página '{name}' no reconocida.")
