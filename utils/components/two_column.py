from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QHBoxLayout

class TwoColumnWidget(QWidget):
    """Componente reutilizable para crear un diseño de dos columnas con inputs dinámicos."""

    def __init__(self, column1_label=None, column2_label=None, parent=None, expression_label=None):
        """
        Inicializa el widget de dos columnas.
        
        :param column1_label: Título opcional para la primera columna.
        :param column2_label: Título opcional para la segunda columna.
        :param parent: Widget padre.
        :param expression_label: Título opcional para la sección de expresión.
        """
        super().__init__(parent)
        self.column1_label = column1_label
        self.column2_label = column2_label
        self.expression_label = expression_label

        # Layout principal vertical para contener todo
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        # Si hay etiqueta de expresión, crear el grupo de expresión
        if expression_label:
            self.expression_group = QGroupBox(f"📌 {expression_label}")
            self.expression_group.setStyleSheet("QGroupBox { font-weight: bold; }")
            self.expression_layout = QVBoxLayout(self.expression_group)
            self.expression_layout.setContentsMargins(5, 5, 5, 5)
            self.expression_layout.setSpacing(5)
            self.layout.addWidget(self.expression_group)

        # Grid para las dos columnas
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(10)

        # Crear las columnas
        self.column1_group = QGroupBox(f"📌 {self.column1_label}" if self.column1_label else "Columna 1")
        self.column1_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.column1_layout = QVBoxLayout(self.column1_group)
        self.column1_layout.setContentsMargins(5, 5, 5, 5)
        self.column1_layout.setSpacing(5)

        self.column2_group = QGroupBox(f"📌 {self.column2_label}" if self.column2_label else "Columna 2")
        self.column2_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.column2_layout = QVBoxLayout(self.column2_group)
        self.column2_layout.setContentsMargins(5, 5, 5, 5)
        self.column2_layout.setSpacing(5)

        # Añadir las columnas al grid
        self.grid_layout.addWidget(self.column1_group, 0, 0)
        self.grid_layout.addWidget(self.column2_group, 0, 1)
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)

        # Añadir el grid al layout principal
        self.layout.addWidget(self.grid_widget)

    def add_to_expression(self, widget):
        """Añade un widget a la sección de expresión."""
        if hasattr(self, 'expression_layout'):
            self.expression_layout.addWidget(widget)
            if self.expression_layout.count() == 1:
                self.expression_layout.addStretch(1)

    def add_to_column1(self, widget):
        """Añade un widget a la primera columna."""
        # Quitar cualquier stretch que pudiera existir
        while self.column1_layout.count() > 0 and self.column1_layout.itemAt(self.column1_layout.count()-1).spacerItem():
            item = self.column1_layout.takeAt(self.column1_layout.count()-1)
            
        self.column1_layout.addWidget(widget)
        # Añadir el stretch al final de todos los widgets
        self.column1_layout.addStretch(1)

    def add_to_column2(self, widget):
        """Añade un widget a la segunda columna."""
        # Quitar cualquier stretch que pudiera existir
        while self.column2_layout.count() > 0 and self.column2_layout.itemAt(self.column2_layout.count()-1).spacerItem():
            item = self.column2_layout.takeAt(self.column2_layout.count()-1)
            
        self.column2_layout.addWidget(widget)
        # Añadir el stretch al final de todos los widgets
        self.column2_layout.addStretch(1)