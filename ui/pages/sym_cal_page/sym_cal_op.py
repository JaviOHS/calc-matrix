from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox
from widgets.math_operation_widget import MathOperationWidget

class SymCalOpWidget(MathOperationWidget):
    def __init__(self, manager, controller, operation_type=None):
        super().__init__(manager, controller, operation_type)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        func_layout = QHBoxLayout()
        func_layout.addWidget(QLabel("f(x) ="))
        self.function_input = QLineEdit("x**2 + 3*x")
        func_layout.addWidget(self.function_input)
        layout.addLayout(func_layout)

        if self.operation_type == "integrales":
            limits_layout = QHBoxLayout()
            limits_layout.addWidget(QLabel("Desde x ="))
            self.lower_limit = QSpinBox()
            self.lower_limit.setRange(-1000, 1000)
            self.lower_limit.setValue(0)
            limits_layout.addWidget(self.lower_limit)

            limits_layout.addWidget(QLabel("Hasta x ="))
            self.upper_limit = QSpinBox()
            self.upper_limit.setRange(-1000, 1000)
            self.upper_limit.setValue(1)
            limits_layout.addWidget(self.upper_limit)
            layout.addLayout(limits_layout)

        buttons_widget = self.create_buttons("Cancelar", "Calcular")
        self.cancel_button.clicked.connect(self.cleanup)
        self.calculate_button.clicked.connect(self.on_calculate_clicked)
        layout.addWidget(buttons_widget)

        # Área donde se mostrará el resultado
        self.result_area = QVBoxLayout()
        layout.addLayout(self.result_area)

    def get_inputs(self):
        inputs = {"expression": self.function_input.text()}
        if self.operation_type == "integrales":
            inputs["limits"] = (self.lower_limit.value(), self.upper_limit.value())
        return inputs

    def on_calculate_clicked(self):
        data = self.get_inputs()
        if self.operation_type == "derivadas":
            result = self.controller.compute_derivative(data["expression"])
        elif self.operation_type == "integrales":
            result = self.controller.compute_integral(data["expression"], data["limits"])
        else:
            result = "Operación desconocida"
        self.display_result(str(result))

    def display_result(self, result_text):
        self.clear_result()
        result_label = QLabel(f"Resultado:\n{result_text}")
        result_label.setWordWrap(True)
        self.result_area.addWidget(result_label)

    def clear_result(self):
        while self.result_area.count():
            child = self.result_area.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
