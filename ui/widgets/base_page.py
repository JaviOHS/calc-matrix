from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QScrollArea, QStackedWidget, QMenu, QWidgetAction
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from utils.image_utils import create_image_label
from utils.content_manager import ContentManager
from utils.action_buttons import ActionButton
from ui.dialogs.message_dialog import MessageDialog

class BasePage(QWidget):
    def __init__(self, navigate_callback=None, page_key=None, controller=None, manager=None):
        super(BasePage, self).__init__()
        self.navigate_callback = navigate_callback
        self.page_key = page_key
        self.controller = controller
        self.manager = manager
        
        # Para contenido dinámico desde JSON
        self.content_manager = ContentManager.get_instance()
        self.page_content = self.content_manager.get_page_content(self.page_key) if self.page_key else {}
        
        # Para operaciones matemáticas
        self.operations = {}  # Será configurado por las clases derivadas si es necesario
        self.current_operation = None
        self.operation_widgets = {}
        
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Contenedor para el título de operación (visible solo durante operaciones)
        self.operation_title_container = QWidget()
        self.operation_title_container.hide()  # Oculto inicialmente
        
        operation_title_layout = QHBoxLayout(self.operation_title_container)
        operation_title_layout.setContentsMargins(30, 20, 10, 10)
        
        self.operation_title_label = QLabel()
        self.operation_title_label.setObjectName("operationTitle")
        
        operation_title_layout.addWidget(self.operation_title_label)
        operation_title_layout.addStretch()

        # Botón de opciones alineado a la derecha
        self.toggle_button = ActionButton.options()
        self.toggle_button.clicked.connect(self.show_dropdown_menu)
        self.toggle_button.hide()

        operation_title_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.operation_title_container)

        # Widget apilado para manejar diferentes vistas
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Crear y añadir la vista de intro
        self.intro_view = self.create_intro_view()
        self.stacked_widget.addWidget(self.intro_view)

    def create_intro_view(self):
        # Crear un área de desplazamiento para contenido largo
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Cambiar la política de scroll horizontal a nunca mostrar
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QFrame()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(40)

        # Panel de contenido principal - establecer políticas de tamaño
        self.text_panel = QFrame()
        self.text_panel.setObjectName("contentPanel")
        self.text_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.text_panel.setMinimumWidth(350)
        self.text_panel.setMaximumWidth(600)
        
        self.text_layout = QVBoxLayout(self.text_panel)
        self.text_layout.setSpacing(24)
        self.text_layout.setContentsMargins(28, 28, 28, 28)

        self.setup_text_content()

        # Imagen con efectos visuales - puede comprimirse si es necesario
        image_panel = QFrame()
        image_panel.setObjectName("imagePanel")
        image_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # Anchura mínima para el panel de imagen
        image_panel.setMinimumWidth(250)

        image_layout = QVBoxLayout(image_panel)
        image_layout.setContentsMargins(20, 20, 20, 0)

        image_container = QFrame()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        # Usar la utilidad para crear la imagen
        image = create_image_label(self.get_image_path(), width=self.get_image_width(), height=self.get_image_height())
        image_container_layout.addWidget(image, 0, Qt.AlignCenter)

        image_layout.addWidget(image_container)
        
        # Agregar contenido educativo adicional
        self.setup_educational_content(image_layout)

        # Añadir los paneles al layout con proporciones flexibles
        container_layout.addWidget(self.text_panel, 6)
        container_layout.addWidget(image_panel, 4)

        scroll_area.setWidget(container)
        return scroll_area

    def setup_text_content(self):
        """
        Configura el contenido de texto para la página basado en el contenido JSON.
        Las clases derivadas pueden sobrescribir este método si necesitan un comportamiento personalizado.
        """
        # Título de la página
        header = QFrame()
        header.setObjectName("heroHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Usar el método format_title para procesar el título
        formatted_title = self.format_title(self.page_content.get("title", "Título de la Página"))
        title = QLabel(formatted_title)
        title.setObjectName("heroTitle")
        title.setTextFormat(Qt.RichText) # Permite interpretar el HTML
        header_layout.addWidget(title)

        if "subtitle" in self.page_content:
            subtitle = self.page_content["subtitle"]
            subtitle_highlight = QLabel(subtitle)
            subtitle_highlight.setObjectName("heroHighlight")
            subtitle_highlight.setTextFormat(Qt.RichText)
            subtitle_highlight.setWordWrap(True)  # Habilitar ajuste de texto
            header_layout.addWidget(subtitle_highlight)

        self.text_layout.addWidget(header)
        
        # Descripción de la página
        intro_card = QFrame()
        intro_layout = QVBoxLayout(intro_card)
        
        description = QLabel(self.page_content.get("description", ""))
        description.setObjectName("heroDescription")
        description.setWordWrap(True)
        description.setTextFormat(Qt.RichText) # Permite interpretar el HTML en la descripción
        intro_layout.addWidget(description)
        
        self.text_layout.addWidget(intro_card)
        
        # Características/funcionalidades
        features = QFrame()
        features.setObjectName("featureContainer")
        features_layout = QVBoxLayout(features)
        features_layout.setSpacing(16)
        
        # Añadir características desde JSON
        for feature_data in self.page_content.get("features", []):
            feature = self.create_info_item(
                feature_data.get("icon", "⭐"), 
                feature_data.get("title", "Característica"), 
                feature_data.get("description", None)
            )
            features_layout.addWidget(feature)
        
        self.text_layout.addWidget(features)
        self.text_layout.addStretch()

    def setup_educational_content(self, layout, button_callback=None, external_url=None, button_icon=None):
        """
        Método para configurar contenido educativo adicional
        
        Args:
            layout: El layout donde se añadirá el contenido
            button_callback: Función opcional a llamar cuando se presione el botón.
                            Si es None, se usa start_first_operation
            external_url: URL externa para abrir cuando se presione el botón
            button_icon: Nombre del archivo de icono personalizado para el botón
        """
        cta_container = QFrame()
        cta_container.setObjectName("ctaContainer")
        cta_layout = QVBoxLayout(cta_container)
        # Reducir el espaciado superior
        cta_layout.setContentsMargins(15, 0, 15, 15)
        
        # Activar wordWrap en el texto del CTA
        cta_text = QLabel(self.page_content.get("cta", {}).get("text", "¿Listo para empezar?"))
        cta_text.setObjectName("ctaText")
        cta_text.setWordWrap(True)  # Habilitar ajuste de texto
        cta_layout.addWidget(cta_text)
        
        button_row = QFrame()
        button_layout = QHBoxLayout(button_row)
        button_layout.setContentsMargins(0, 12, 0, 0)
        
        # Crear botón con icono personalizado si se especifica
        if button_icon:
            start_button = ActionButton.custom_icon(
                self.page_content.get("cta", {}).get("button", "Comenzar"),
                button_icon
            )
        else:
            start_button = ActionButton.primary(self.page_content.get("cta", {}).get("button", "Comenzar"))
        
        # Usar la URL externa, la función de callback personalizada o la predeterminada
        if external_url:
            from PySide6.QtCore import QUrl
            from PySide6.QtGui import QDesktopServices
            start_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(external_url)))
        elif button_callback:
            start_button.clicked.connect(button_callback)
        else:
            start_button.clicked.connect(self.start_first_operation)
        
        button_layout.addWidget(start_button)
        button_layout.addStretch()
        cta_layout.addWidget(button_row)
        
        # Activar wordWrap en el texto del footer
        footer_text = QLabel(self.page_content.get("cta", {}).get("footer", ""))
        footer_text.setObjectName("footerText")
        footer_text.setWordWrap(True)  # Habilitar ajuste de texto
        cta_layout.addWidget(footer_text)
        
        layout.addWidget(cta_container)
        
        # Añadir tarjeta educativa si existe en el contenido JSON
        if self.page_content and "educational" in self.page_content:
            # Educational card desde JSON
            edu_card = QFrame()
            edu_card.setObjectName("educationalCard")
            edu_layout = QVBoxLayout(edu_card)
            
            # Activar wordWrap en el título educativo
            edu_title = QLabel(self.page_content.get("educational", {}).get("title", "¿Sabías que...?"))
            edu_title.setObjectName("eduTitle")
            edu_title.setWordWrap(True)  # Habilitar ajuste de texto
            edu_layout.addWidget(edu_title)
            
            edu_fact = QLabel(self.page_content.get("educational", {}).get("fact", ""))
            edu_fact.setObjectName("eduFact")
            edu_fact.setWordWrap(True)  # Ya estaba habilitado
            edu_layout.addWidget(edu_fact)

            # Agregar imagen educativa
            edu_image_path = "assets/images/educational.png"
            edu_image = create_image_label(edu_image_path, width=180, height=120)
            edu_image.setAlignment(Qt.AlignCenter)
            edu_image.setObjectName("eduImage")
            edu_layout.addWidget(edu_image, 0, Qt.AlignCenter)
            
            # Añadir espacio después de la imagen
            edu_layout.addSpacing(10)
            
            layout.addWidget(edu_card)

    def get_image_path(self):
        """Obtiene la ruta de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("path", "assets/images/intro/deco.png")
        return "assets/images/intro/default.png"

    def get_image_width(self):
        """Obtiene el ancho de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("width", 200)
        return 200

    def get_image_height(self):
        """Obtiene la altura de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("height", 200)
        return 200

    def get_image_caption(self):
        """Obtiene la descripción de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("caption", None)
        return None
    
    def create_info_item(self, icon, text, description=None):
        """Crea un elemento de información con icono y descripción"""
        feature_item = QFrame()
        feature_item.setObjectName("featureItem")
        feature_layout = QVBoxLayout(feature_item)
        feature_layout.setSpacing(8)
        feature_layout.setContentsMargins(12, 12, 12, description is not None and 12 or 6)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        icon_label = QLabel(icon)
        icon_label.setObjectName("featureIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedWidth(40)
        icon_label.setFixedHeight(40)
        icon_label.setAutoFillBackground(True) 

        text_label = QLabel(text)
        text_label.setObjectName("featureText")
        text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        header_layout.addWidget(icon_label)
        header_layout.addWidget(text_label)
        
        feature_layout.addLayout(header_layout)
        
        # Agregar descripción educativa bajo el texto si existe
        if description:
            desc_label = QLabel(description)
            desc_label.setObjectName("featureDescription")
            desc_label.setWordWrap(True)
            desc_label.setContentsMargins(12, 0, 0, 0)
            feature_layout.addWidget(desc_label)

        return feature_item

    # Métodos para la funcionalidad de operaciones matemáticas
    def show_dropdown_menu(self):
        if not self.operations:
            return
            
        menu = QMenu(self)
        menu.setObjectName("operationsMenu")
        
        spacer = QWidgetAction(menu)
        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(10)
        spacer_widget.setStyleSheet("background-color: transparent;")
        spacer.setDefaultWidget(spacer_widget)
        menu.addAction(spacer)
        
        for label, (op_key, _) in self.operations.items():
            action = QAction(label, self)
            action.triggered.connect(lambda _, k=label: self.prepare_operation(k))
            menu.addAction(action)
        
        position = self.toggle_button.mapToGlobal(QPoint(0, self.toggle_button.height() + 5))
        menu.exec_(position)

    def prepare_operation(self, operation_key):
        self.toggle_button.show()
        
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        
        # Actualizar título de operación
        object_name = self.get_object_name()
        operation_title = f"{operation_key} de <span style='color:#ff8103;'>{object_name}</span>"
        self.operation_title_label.setText(operation_title)
        self.operation_title_label.setWordWrap(True)  # Habilitar ajuste de texto
        self.operation_title_container.show()
        
        if operation_key not in self.operation_widgets:
            try:
                widget = widget_class(self.manager, self.controller, op_key)
            except TypeError:
                widget = widget_class(self.manager, self.controller)

            # Configurar título en el widget si es necesario
            if hasattr(widget, 'set_operation_title'):
                widget.set_operation_title(operation_title)

            if hasattr(widget, 'calculate_button'):
                widget.calculate_button.clicked.connect(self.execute_current_operation)
            if hasattr(widget, 'cancel_button'):
                widget.cancel_button.clicked.connect(self.reset_interface)

            self.operation_widgets[operation_key] = widget
            self.stacked_widget.addWidget(widget)

        widget = self.operation_widgets[operation_key]
        self.stacked_widget.setCurrentWidget(widget)

    def get_object_name(self):
        """Obtiene el nombre del objeto desde el título de la página"""
        page_title = self.page_content.get("title", "Objeto")
        if "{" in page_title and "}" in page_title:
            return page_title.split("{")[1].replace("}", "")
        return "Objeto"
    
    def format_title(self, title_text):
        """Formatea el título reemplazando el texto entre llaves con formato HTML de color"""
        if "{" in title_text and "}" in title_text:
            parts = title_text.split("{")
            before_brace = parts[0]
            after_brace = parts[1].split("}")
            highlighted_text = after_brace[0]
            end_text = after_brace[1] if len(after_brace) > 1 else ""
            
            return f"{before_brace}<span style='color:#ff8103;'>{highlighted_text}</span>{end_text}"
        return title_text

    def reset_interface(self):
        """Restablece la interfaz a su estado inicial"""
        self.toggle_button.hide()

        if self.current_operation:
            widget = self.operation_widgets.get(self.current_operation)
            if widget and hasattr(widget, 'cleanup'):
                widget.cleanup()
                
            if self.manager:
                self.manager.clear()
                
        self.current_operation = None
        self.operation_title_container.hide()
        self.stacked_widget.setCurrentIndex(0)

    def start_first_operation(self):
        """Inicia la primera operación disponible"""
        if self.operations:
            first_label = next(iter(self.operations))  # Obtiene la primera operación
            self.prepare_operation(first_label)  # Navega a la operación
        else:
            self.show_message_dialog(
                "🔴 ERROR", 
                "#f44336", 
                "No hay operaciones configuradas para esta página."
            )
            
    def show_message_dialog(self, title: str, title_color: str, message: str, image_name: str = "error.png"):
        """Muestra un diálogo de mensaje"""
        dialog = MessageDialog(title, title_color, message, image_name, parent=self)
        dialog.exec()

    def execute_current_operation(self):
        """Método para ser implementado por las subclases"""
        pass

    def show_result(self, result, message):
        """Método para ser implementado por las subclases"""
        pass