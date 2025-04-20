from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTableWidget, 
                              QTableWidgetItem, QPushButton, QHBoxLayout, 
                              QWidget, QGridLayout, QSpacerItem)
from PySide6.QtCore import Qt

class MatrixResultDialog(QDialog):
    def __init__(self, matrices, result_matrix, operation="", parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint) # Para quitar título

        # Hacer que la ventana sea movible
        self.setMouseTracking(True)
        self._drag_position = None
        
        # Configuración principal del layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(main_layout)

        # Mostrar operación realizada
        if operation:
            op_label = QLabel(f"Operación: {operation}")
            op_label.setAlignment(Qt.AlignCenter)
            op_label.setStyleSheet("font-weight: bold;")
            main_layout.addWidget(op_label)

        # Contenedor para matrices de entrada
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)

        # Grid para matrices de entrada (2 columnas, múltiples filas)
        matrices_grid = QWidget()
        grid_layout = QGridLayout(matrices_grid)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # Calcular tamaño máximo para centrado uniforme
        max_width = max([matrix.cols * 45 + 20 for matrix in matrices] + [result_matrix.cols * 45 + 20])
        max_height = max([matrix.rows * 45 + 30 for matrix in matrices] + [result_matrix.rows * 45 + 30])
        
        # Mostrar matrices de entrada en grid 2 columnas
        for idx, matrix in enumerate(matrices):
            row = idx // 2  # Calcula la fila basada en el índice
            col = idx % 2   # Alterna entre columna 0 y 1
            
            # Crear widget de matriz
            matrix_widget = self._create_matrix_widget(matrix, f"Matriz {chr(65 + idx)}", max_width)
            grid_layout.addWidget(matrix_widget, row, col, Qt.AlignCenter)

        # Ajustar el grid para que ocupe todo el espacio horizontal
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        
        input_layout.addWidget(matrices_grid, 0, Qt.AlignHCenter)
        main_layout.addWidget(input_container)

        # Mostrar matriz resultado
        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título "Resultado"
        result_title = QLabel("Resultado:")
        result_title.setAlignment(Qt.AlignCenter)
        result_title.setStyleSheet("font-weight: bold; color: #72e48c;")
        result_layout.addWidget(result_title)

        # Widget de matriz resultado
        # Mostrar resultado especial si no es Matrix tradicional
        if hasattr(result_matrix, 'rows') and hasattr(result_matrix, 'cols'):
            result_widget = self._create_matrix_widget(result_matrix, "", max_width)
        else:
            result_widget = self._create_special_result_widget(result_matrix)
        result_layout.addWidget(result_widget, 0, Qt.AlignHCenter)
        
        main_layout.addWidget(result_container)
        main_layout.addStretch()

        # Botón para cerrar
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        close_btn = QPushButton("Cerrar")
        close_btn.setFixedWidth(120)
        close_btn.clicked.connect(self.accept)
        
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        
        main_layout.addWidget(btn_container)
        self.adjustSize()

    def mousePressEvent(self, event):
        """Captura la posición del ratón para mover la ventana."""
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """Permite mover la ventana arrastrando."""
        if self._drag_position:
            delta = event.globalPosition().toPoint() - self._drag_position
            self.move(self.pos() + delta)
            self._drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        """Libera la posición de arrastre."""
        self._drag_position = None

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
