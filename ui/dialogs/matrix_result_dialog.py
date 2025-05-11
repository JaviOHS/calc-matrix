from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, QScrollArea, QFrame
from PySide6.QtCore import Qt
from utils.action_buttons import ActionButton
from PySide6.QtCore import QSize

class MatrixResultDialog(QDialog):
    def __init__(self, result_matrix, operation="", parent=None):
        super().__init__(parent)

        # Ventana sin bordes y con fondo transparente
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self._drag_position = None

        # Contenedor con borde redondeado
        background_frame = QFrame(self)
        background_frame.setObjectName("backgroundFrame")
        background_layout = QVBoxLayout(background_frame)
        background_layout.setContentsMargins(20, 20, 20, 20)
        background_layout.setSpacing(20)

        # Título
        title_label = QLabel(f"🟢 RESULTADO DE {operation.upper()}:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("titleDialog")
        background_layout.addWidget(title_label)

        # Resultado de matriz
        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.setContentsMargins(0, 10, 0, 10)
        result_layout.setSpacing(15)

        if hasattr(result_matrix, 'rows') and hasattr(result_matrix, 'cols'):
            result_widget = self._create_matrix_widget(result_matrix)
        else:
            result_widget = self._create_special_result_widget(result_matrix)

        result_layout.addWidget(result_widget, 0, Qt.AlignCenter)
        background_layout.addWidget(result_container)

        # Botón aceptar
        button = ActionButton("Aceptar", icon_name="check.svg", icon_size=QSize(20, 20), object_name="ctaButton")
        button.clicked.connect(self.accept)
        button.setFixedWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        background_layout.addLayout(button_layout)

        # Layout externo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(background_frame)

        self.adjustSize()

    def _create_matrix_widget(self, matrix):
        """Crea un widget de matriz con estilo consistente"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Determinar si necesitamos scroll vertical (matrices con más de 5 filas)
        needs_scroll = matrix.rows > 6
        
        # Configurar tamaño de celda
        cell_size = 70
        
        if needs_scroll:
            # Crear un área de desplazamiento (solo vertical)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Sin scroll horizontal
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)     # Scroll vertical cuando sea necesario
            
            # Tamaño máximo para el área de scroll (5 filas visibles, todas las columnas)
            max_height = min(matrix.rows, 5) * cell_size + 30
            max_width = matrix.cols * cell_size + 30  # Mostrar todas las columnas
            scroll_area.setMaximumSize(max_width, max_height)
            
            # Contenedor para la tabla dentro del área de scroll
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setContentsMargins(0, 0, 0, 0)
            
            # Crear tabla
            table = QTableWidget()
            table.setRowCount(matrix.rows)
            table.setColumnCount(matrix.cols)
            
            # Configuración de la tabla
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionMode(QTableWidget.NoSelection)
            table.setFocusPolicy(Qt.NoFocus)
            table.horizontalHeader().setVisible(False)
            table.verticalHeader().setVisible(False)
            table.setShowGrid(True)
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Asegurar que la tabla no tenga scroll horizontal
            
            # Configurar tamaño de celdas
            for i in range(matrix.cols):
                table.setColumnWidth(i, cell_size)
            for i in range(matrix.rows):
                table.setRowHeight(i, cell_size)
            
            # Ajustar el ancho de la tabla para mostrar todas las columnas
            table_width = matrix.cols * cell_size + 2
            table.setMinimumWidth(table_width)
            
            scroll_layout.addWidget(table)
            scroll_area.setWidget(scroll_content)
            layout.addWidget(scroll_area, 0, Qt.AlignCenter)
            
        else:
            # Para matrices pequeñas, usar el enfoque original sin scroll
            table = QTableWidget()
            table.setRowCount(matrix.rows)
            table.setColumnCount(matrix.cols)
            
            # Configuración de la tabla
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionMode(QTableWidget.NoSelection)
            table.setFocusPolicy(Qt.NoFocus)
            table.horizontalHeader().setVisible(False)
            table.verticalHeader().setVisible(False)
            table.setShowGrid(True)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            # Configurar tamaño de celdas
            for i in range(matrix.cols):
                table.setColumnWidth(i, cell_size)
            for i in range(matrix.rows):
                table.setRowHeight(i, cell_size)
            
            # Tamaño fijo de la tabla
            table_width = matrix.cols * cell_size + 2
            table_height = matrix.rows * cell_size + 2
            table.setFixedSize(table_width, table_height)
            
            layout.addWidget(table, 0, Qt.AlignCenter)
        
        # Llenar tabla con datos formateados
        for r in range(matrix.rows):
            for c in range(matrix.cols):
                value = matrix.data[r, c]
                
                # Mejorar el formato de los números para mostrarlos completos
                if value.is_integer():
                    display_value = f"{int(value)}"
                else:
                    # Limitar a 4 decimales para valores no enteros, pero mostrar todos los necesarios
                    display_value = f"{value:.4f}".rstrip('0').rstrip('.')
                    if len(display_value) > 8:  # Si es demasiado largo
                        display_value = f"{value:.2f}".rstrip('0').rstrip('.')
                
                item = QTableWidgetItem(display_value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                # Establecer tooltip para mostrar el valor completo al pasar el mouse
                item.setToolTip(str(value))
                table.setItem(r, c, item)
        return widget
    
    def _create_special_result_widget(self, raw_result):
        """Muestra resultados como texto legible (para determinantes o inversas)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        if isinstance(raw_result, list):
            for name, value in raw_result:
                label = QLabel()
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignCenter)
                
                if isinstance(value, float):
                    label.setText(f"{name}: {value:.2f}")
                elif hasattr(value, '__array__'):
                    matrix_str = '\n'.join(['  '.join(f"{v:.2f}" for v in row) for row in value])
                    label.setText(f"{name}:\n{matrix_str}")
                else:
                    label.setText(f"{name}: {value}")
                
                layout.addWidget(label)
        else:
            label = QLabel(str(raw_result))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        return widget
