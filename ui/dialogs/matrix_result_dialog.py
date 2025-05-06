from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QGridLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

class MatrixResultDialog(QDialog):
    def __init__(self, matrices, result_matrix, operation="", parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self._drag_position = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Contenedor horizontal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # Widget personalizado (derecha)
        custom_widget = QWidget()
        custom_layout = QVBoxLayout(custom_widget)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        custom_layout.setSpacing(15)

        # Matrices de entrada
        input_container = QWidget()
        input_layout = QGridLayout(input_container)
        input_layout.setHorizontalSpacing(30)
        input_layout.setVerticalSpacing(20)
        input_layout.setContentsMargins(0, 0, 0, 0)

        max_width = max([matrix.cols * 45 + 20 for matrix in matrices] + [result_matrix.cols * 45 + 20])
        for idx, matrix in enumerate(matrices):
            matrix_widget = self._create_matrix_widget(matrix, f"Matriz {chr(65 + idx)}", max_width)
            input_layout.addWidget(matrix_widget, idx // 2, idx % 2, Qt.AlignCenter)

        custom_layout.addWidget(input_container)

        # Resultado
        result_label = QLabel(f"🟢 RESULTADO DE {operation.upper():}")

        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("font-weight: bold; color: #72e48c; font-size: 20px;")
        custom_layout.addWidget(result_label)

        if hasattr(result_matrix, 'rows') and hasattr(result_matrix, 'cols'):
            result_widget = self._create_matrix_widget(result_matrix, "", max_width)
        else:
            result_widget = self._create_special_result_widget(result_matrix)
        custom_layout.addWidget(result_widget, alignment=Qt.AlignCenter)

        content_layout.addWidget(custom_widget)
        main_layout.addLayout(content_layout)

        # Botón cerrar
        button = QPushButton("Aceptar")
        button.setObjectName("ctaButton")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setFixedWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.adjustSize()

    def _create_matrix_widget(self, matrix, title, max_width=None):
        """Crea un widget de matriz con estilo consistente"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Título de la matriz (si existe)
        if title:
            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold;")
            layout.addWidget(label)

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
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        cell_size = 55
        for i in range(matrix.cols):
            table.setColumnWidth(i, cell_size)
        for i in range(matrix.rows):
            table.setRowHeight(i, cell_size)
        
        # Tamaño fijo de la tabla
        table_width = matrix.cols * cell_size + 2
        table_height = matrix.rows * cell_size + 2
        table.setFixedSize(table_width, table_height)
        
        # Llenar tabla con datos formateados
        for r in range(matrix.rows):
            for c in range(matrix.cols):
                value = matrix.data[r, c]
                display_value = f"{int(value)}" if value.is_integer() else f"{value:.2f}".rstrip('0').rstrip('.')
                item = QTableWidgetItem(display_value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(r, c, item)
        
        # Contenedor para centrado si es necesario
        if max_width and table_width < max_width:
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.addSpacerItem(QSpacerItem((max_width - table_width) // 2, 0))
            container_layout.addWidget(table)
            container_layout.addSpacerItem(QSpacerItem((max_width - table_width) // 2, 0))
            layout.addWidget(container)
        else:
            layout.addWidget(table, 0, Qt.AlignCenter)
        
        return widget
    
    def _create_special_result_widget(self, raw_result):
        """Muestra resultados como texto legible (para determinantes o inversas)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if isinstance(raw_result, list):
            for name, value in raw_result:
                label = QLabel()
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("font-size: 14px;")
                
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
