from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from model.matrix_model import Matrix
from ui.pages.matrix_page.operation_widgets.add_sub_widget import MatrixAddSubWidget
from ui.pages.matrix_page.operation_widgets.det_inv_widget import MatrixDeterminantWidget, MatrixInverseWidget
from ui.pages.matrix_page.operation_widgets.solver_sys_widget import MatrixSystemSolverWidget
from ui.pages.matrix_page.operation_widgets.mult_widget import MatrixMultiplicationWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QMessageBox, QTableWidgetItem

class MatrixPage(QWidget):
    def __init__(self, manager: MatrixManager):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.manager = manager
        self.controller = MatrixController(manager)

        self.current_operation = None
        self.operation_widgets = {}
        self.result_widget = None

        # Para estado activo de botones
        self.operation_buttons_map = {}

        # Diccionario de operaciones: {Botón: (clave operación, widget)}
        self.operations = {
            "Suma": ("suma", MatrixAddSubWidget),
            "Resta": ("resta", MatrixAddSubWidget),
            "Multiplicación": ("multiplicacion", MatrixMultiplicationWidget),
            "División": ("division", MatrixAddSubWidget),
            "Determinante": ("determinante", MatrixDeterminantWidget),
            "Inversa": ("inversa", MatrixInverseWidget),
            "Sistema de Ecuaciones": ("sistema", MatrixSystemSolverWidget) 
        }

        self.intro_widget = self.create_intro_widget()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        title_label = QLabel("Operaciones con Matrices")
        title_label.setObjectName("title_label")
        self.layout.addWidget(title_label)
        self.title_label = title_label # Para títulos dinámicos
        self.title_label.setAlignment(Qt.AlignLeft)

        label = QLabel("Seleccione una operación:")
        self.layout.addWidget(label)

        self.operations_buttons = QHBoxLayout()
        self.add_operation_buttons()
        self.layout.addLayout(self.operations_buttons)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.intro_widget)  # Página 0
        self.layout.addWidget(self.stacked_widget)

        self.init_result_widget()

        self.setLayout(self.layout)

    def create_intro_widget(self):
        intro_widget = QWidget()
        layout = QHBoxLayout()

        # Texto a la izquierda
        text_label = QLabel(
            "Bienvenido a la sección de operaciones con matrices.\n\n"
            "Puedes realizar suma, resta, multiplicación, obtener determinantes,\n"
            "inversas o resolver sistemas de ecuaciones lineales.\n\n"
            "Selecciona una operación para comenzar."
        )
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        text_label.setObjectName("intro_text")

        # Imagen a la derecha
        image_label = QLabel()
        image_label.setPixmap(QPixmap("assets/images/matrix_intro.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(text_label, stretch=2)
        layout.addWidget(image_label, stretch=1)
        intro_widget.setLayout(layout)

        return intro_widget

    def add_operation_buttons(self):
        for label, (op_key, _) in self.operations.items():
            btn = QPushButton(label)
            btn.setProperty("class", "operation-button")
            btn.clicked.connect(lambda _, k=label: self.prepare_operation(k))
            self.operations_buttons.addWidget(btn)
            self.operation_buttons_map[label] = btn # Para estado activo de botones

    def init_result_widget(self):
        self.result_widget = QWidget()
        layout = QVBoxLayout()

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setObjectName("success_message")
        layout.addWidget(self.result_label)

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.new_operation_btn = QPushButton("Nueva Operación")
        self.new_operation_btn.setObjectName("new_operation_button")
        self.new_operation_btn.clicked.connect(self.reset_interface)
        layout.addWidget(self.new_operation_btn)

        self.result_widget.setLayout(layout)

    def prepare_operation(self, label):
        op_key, widget_class = self.operations[label]
        self.current_operation = op_key
        self.title_label.setText(f"Operaciones con Matrices - {label.capitalize()}")

        if widget_class is None:
            QMessageBox.information(self, "Pendiente", "Esta operación aún no está implementada.")
            return

        if op_key not in self.operation_widgets:
            widget = widget_class(self.manager, self.controller)
            widget.calculate_button.clicked.connect(self.execute_current_operation)
            widget.cancel_button.clicked.connect(self.reset_interface)
            self.operation_widgets[op_key] = widget
            self.stacked_widget.addWidget(widget)

        self.stacked_widget.setCurrentWidget(self.operation_widgets[op_key])
        self.manager.matrices.clear()

        for lbl, btn in self.operation_buttons_map.items():
            is_active = (lbl == label)
            btn.setProperty("active", is_active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def execute_current_operation(self):
        widget = self.operation_widgets.get(self.current_operation)
        if not widget:
            QMessageBox.critical(self, "Error", "No se encontró el widget de la operación.")
            return

        is_valid, error_msg = widget.validate_operation()
        if not is_valid:
            QMessageBox.warning(self, "Validación", error_msg)
            return

        try:
            matrices = widget.collect_matrices()
            self.manager.matrices.clear()
            for matrix in matrices:
                self.manager.add_matrix(matrix)

            result = self.controller.execute_operation(self.current_operation)
            self.show_result(result, f"{self.current_operation.capitalize()} realizada correctamente")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def show_result(self, result, message):
        self.result_label.setText(message)

        # Limpiar el contenido anterior
        self.result_table.clear()

        # Si es una lista de resultados (como inversas o determinantes)
        if isinstance(result, list):
            if isinstance(result[0][1], Matrix):
                # Mostrar la primera inversa (opcionalmente puedes mostrar todas)
                matrix = result[0][1]
                dimension = matrix.rows
                self.result_table.setRowCount(dimension)
                self.result_table.setColumnCount(dimension)
                self.result_table.setHorizontalHeaderLabels([str(i + 1) for i in range(dimension)])
                self.result_table.setVerticalHeaderLabels([str(i + 1) for i in range(dimension)])
                for row in range(dimension):
                    for col in range(dimension):
                        value = matrix.data[row, col]
                        item = QTableWidgetItem(f"{value:.2f}")
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        self.result_table.setItem(row, col, item)
            else:
                # Por ejemplo, determinantes: mostrar en texto
                text = "\n".join([f"{name}: {value}" for name, value in result])
                self.result_label.setText(f"{message}\n\n{text}")
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(0)
        else:
            # Resultado único (como suma, resta, etc.)
            rows = result.rows
            cols = result.cols
            self.result_table.setRowCount(rows)
            self.result_table.setColumnCount(cols)
            self.result_table.setHorizontalHeaderLabels([str(i + 1) for i in range(cols)])
            self.result_table.setVerticalHeaderLabels([str(i + 1) for i in range(rows)])

            for row in range(rows):
                for col in range(cols):
                    value = result.data[row, col]
                    item = QTableWidgetItem(f"{value:.2f}")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.result_table.setItem(row, col, item)

        self.stacked_widget.addWidget(self.result_widget)
        self.stacked_widget.setCurrentWidget(self.result_widget)

    def reset_interface(self):
        self.current_operation = None
        self.manager.matrices.clear()
        self.title_label.setText("Operaciones con Matrices")

        for widget in self.operation_widgets.values():
            widget.cleanup()

        if self.stacked_widget.count() > 0:
            self.stacked_widget.setCurrentIndex(0)

        self.stacked_widget.setCurrentWidget(self.intro_widget)

        for btn in self.operation_buttons_map.values():
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
