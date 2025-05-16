from ui.dialogs.base_dialog import BaseDialog
from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt

class BaseResultDialog(BaseDialog):
    """Diálogo base para mostrar resultados con una interfaz común"""
    def __init__(self, operation="", parent=None):
        super().__init__(f"🟢 RESULTADO DE {operation.upper()}", None, parent)
        self.finalize()

    def setup_content_area(self):
        # Contenedor de resultados
        self.result_container = QWidget()
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setContentsMargins(0, 10, 0, 10)
        self.result_layout.setSpacing(15)
        
        # El contenido se añadirá en las subclases
        self.background_layout.addWidget(self.result_container)

    def create_data_table(self, rows, cols, data_accessor=None, needs_scroll=False):
        """
        Crea una tabla para mostrar datos numéricos
        
        Args:
            rows: Número de filas
            cols: Número de columnas
            data_accessor: Función que recibe (r, c) y devuelve el valor en esa posición
            needs_scroll: Indica si la tabla necesita scroll vertical
        """
        cell_size = 70
        
        # Crear widget contenedor para la tabla (con o sin scroll)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        if needs_scroll and rows > 6:
            # Crear un área de desplazamiento (solo vertical)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            # Tamaño máximo para el área de scroll
            max_height = min(rows, 5) * cell_size + 30
            max_width = cols * cell_size + 30
            scroll_area.setMaximumSize(max_width, max_height)
            
            # Contenedor para la tabla dentro del área de scroll
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setContentsMargins(0, 0, 0, 0)
            
            table = self._setup_table(rows, cols, cell_size)
            scroll_layout.addWidget(table)
            scroll_area.setWidget(scroll_content)
            layout.addWidget(scroll_area, 0, Qt.AlignCenter)
        else:
            table = self._setup_table(rows, cols, cell_size, fixed_size=True)
            layout.addWidget(table, 0, Qt.AlignCenter)
        
        # Llenar tabla con datos
        if data_accessor:
            self._fill_table_data(table, rows, cols, data_accessor)
        
        return widget, table
    
    def _setup_table(self, rows, cols, cell_size, fixed_size=False):
        """Configura una tabla con el formato común"""
        table = QTableWidget()
        table.setRowCount(rows)
        table.setColumnCount(cols)
        
        # Configuración básica
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setFocusPolicy(Qt.NoFocus)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff if fixed_size else Qt.ScrollBarAsNeeded)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Configurar tamaño de celdas
        for i in range(cols):
            table.setColumnWidth(i, cell_size)
        for i in range(rows):
            table.setRowHeight(i, cell_size)
        
        # Fijar tamaño si es necesario
        if fixed_size:
            table_width = cols * cell_size + 2
            table_height = rows * cell_size + 2
            table.setFixedSize(table_width, table_height)
        else:
            table_width = cols * cell_size + 2
            table.setMinimumWidth(table_width)
        
        return table
    
    def _fill_table_data(self, table, rows, cols, data_accessor):
        """Llena la tabla con los datos proporcionados por el data_accessor"""
        for r in range(rows):
            for c in range(cols):
                val = data_accessor(r, c)
                
                # Formato del valor
                if hasattr(val, 'imag') and abs(val.imag) < 1e-10:  # Es un número complejo pero real
                    val = val.real
                
                if isinstance(val, (int, float)):
                    if val.is_integer():
                        display_value = f"{int(val)}"
                    else:
                        display_value = f"{val:.4f}".rstrip('0').rstrip('.')
                        if len(display_value) > 8:
                            display_value = f"{val:.2f}".rstrip('0').rstrip('.')
                else:  # Es un valor especial o complejo
                    display_value = str(val)
                
                item = QTableWidgetItem(display_value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setToolTip(str(val))
                table.setItem(r, c, item)
    
    def add_section(self, title, widget):
        """Añade una sección con título y widget al diálogo, centrado verticalmente"""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(5)
        section_layout.addStretch()
        section_label = QLabel(title)
        section_label.setObjectName("sectionLabel")
        section_label.setAlignment(Qt.AlignCenter)
        section_layout.addWidget(section_label, 0, Qt.AlignHCenter)
        section_layout.addWidget(widget, 0, Qt.AlignHCenter)
        section_layout.addStretch()
        self.result_layout.addWidget(section_widget, 0, Qt.AlignVCenter)
        