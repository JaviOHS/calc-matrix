import re
from model.polynomial_manager import PolynomialManager
from model.polynomial_model import Polynomial
from controller.polynomial_controller import PolynomialController
from ui.pages.polynomial_page.operation_widgets.poly_operations import PolynomialOpcWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QMessageBox, QTableWidgetItem, QTextEdit

class PolynomialPage(QWidget):
    def __init__(self, manager: PolynomialManager):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.manager = manager
        self.controller = PolynomialController(manager)

        self.current_operation = None
        self.operation_widgets = {}
        self.result_widget = None
        
        self.operation_buttons_map = {} # Para futura implementación de estado activo

        # Diccionario de operaciones: {Botón: (clave operación, widget)}
        self.operations = {
            "Operaciones Combinadas": ("operaciones_combinadas", PolynomialOpcWidget),
            "Raíces": ("raices", PolynomialOpcWidget),
            "Derivación": ("derivacion", PolynomialOpcWidget),
            "Integración": ("integracion", PolynomialOpcWidget),
            "Evaluación": ("evaluacion", PolynomialOpcWidget),
        }

        self.intro_widget = self.create_intro_widget()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        title_label = QLabel("Operaciones con Polinomios")
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
        text_label = QLabel("Bienvenido a la sección de operaciones con polinomios.\n\nPuedes realizar operaciones combinadas (suma, resta, multiplicación, división),\nobtener raíces, derivadas, integrales y evaluación de polinomios.\n\nSelecciona una operación para comenzar.")
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        text_label.setObjectName("intro_text")

        # Imagen a la derecha
        image_label = QLabel()
        image_label.setPixmap(QPixmap("assets/images/polynomial_intro.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

        # Resultado con estilo Cambria Math
        self.result_preview_label = QLabel()
        self.result_preview_label.setAlignment(Qt.AlignCenter)
        self.result_preview_label.setWordWrap(True)
        self.result_preview_label.setStyleSheet("""
            QLabel {
                font-family: 'Cambria Math';
                font-size: 18px;
                color: #ffffff;
                padding: 8px;
            }
        """)
        layout.addWidget(self.result_preview_label)

        self.new_operation_btn = QPushButton("Nueva Operación")
        self.new_operation_btn.setObjectName("new_operation_button")
        self.new_operation_btn.clicked.connect(self.reset_interface)
        layout.addWidget(self.new_operation_btn)

        self.result_widget.setLayout(layout)

    def format_polynomial_html(self, text: str) -> str:
        # Limpieza y formateo simple
        formatted = text.replace(' ', '')
        formatted = formatted.replace('+', ' + ')
        formatted = formatted.replace('-', ' - ')
        formatted = formatted.replace('*', '·')
        formatted = formatted.replace('/', ' ÷ ')
        formatted = formatted.replace('**', '^')
        formatted = re.sub(r'\^(\d+)', r'<sup>\1</sup>', formatted)
        return f"<span style='font-family: Cambria Math; color: #ffffff;'>{formatted}</span>"

    def prepare_operation(self, label):
        op_key, widget_class = self.operations[label]
        self.current_operation = op_key
        self.title_label.setText(f"Operaciones con Polinomios - {label.capitalize()}")

        # Crear el widget con el tipo de operación correspondiente
        widget = PolynomialOpcWidget(self.manager, self.controller, op_key)
        widget.calculate_button.clicked.connect(self.execute_current_operation)
        widget.cancel_button.clicked.connect(self.reset_interface)
        
        self.operation_widgets[op_key] = widget
        self.stacked_widget.addWidget(widget)

        self.stacked_widget.setCurrentWidget(widget)
        self.manager.polynomials.clear()

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
            if self.current_operation == "operaciones_combinadas":
                expression = widget.collect_polynomials()[0] # Caso especial para operaciones combinadas
                result = self.controller.execute_operation(self.current_operation, expression)
            else:
                polynomials = widget.collect_polynomials()
                self.manager.polynomials.clear()

                for poly in polynomials:
                    self.manager.add_polynomial(poly)

                if self.current_operation == "evaluacion":
                    x_value = widget.get_evaluation_value()
                    if x_value is None or x_value.strip() == "":
                        QMessageBox.warning(self, "Validación", "Por favor, ingrese un valor para x.")
                        return
                    try:
                        x_value = float(x_value)
                    except ValueError:
                        QMessageBox.warning(self, "Validación", "El valor de x no es válido.")
                        return
                    result = self.controller.execute_operation(self.current_operation, x_value)
                else:
                    result = self.controller.execute_operation(self.current_operation)
 
            self.show_result(result, f"{self.current_operation.replace('_', ' ').capitalize()} realizada correctamente")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
    
    def show_result(self, result, message):
        self.result_label.setText(message)
        self.result_preview_label.clear()

        if isinstance(result, tuple) and all(isinstance(r, Polynomial) for r in result):
            
            quotient, remainder = result # División: (cociente, residuo)
            formatted_html = (
                f"Cociente: {self.format_polynomial_html(str(quotient))}<br>"
                f"Residuo: {self.format_polynomial_html(str(remainder))}"
            )

        elif isinstance(result, list) and all(isinstance(p, Polynomial) for p in result):
            # Derivación o integración de múltiples polinomios
            formatted_html = "<br>".join(
                f"P{i+1}: {self.format_polynomial_html(str(p))}" for i, p in enumerate(result)
            )

        elif isinstance(result, list):  # Evaluación o raíces (etiqueta, valor)
            formatted_html = "<br>".join(
                f"{label}: {self.format_polynomial_html(str(value))}" for label, value in result
            )

        else:  # Resultado único (como evaluación combinada)
            formatted_html = self.format_polynomial_html(str(result))

        self.result_preview_label.setText(formatted_html)
        self.stacked_widget.addWidget(self.result_widget)
        self.stacked_widget.setCurrentWidget(self.result_widget)

    def reset_interface(self):
        self.current_operation = None
        self.manager.polynomials.clear()
        self.title_label.setText("Operaciones con Polinomios")

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
