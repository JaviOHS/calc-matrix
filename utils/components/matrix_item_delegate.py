from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit

class MatrixItemDelegate(QStyledItemDelegate):
    """Delegado personalizado para la edición de celdas en matrices"""	
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setMaxLength(4)
        
        # Validador para permitir números negativos y positivos
        editor.textChanged.connect(lambda text: self._validate_input(editor, text))
        return editor
    
    def _validate_input(self, editor, text):
        # Si está vacío o es solo un minus, permitir
        if text == "" or text == "-":
            return

        # Limpiar el texto permitiendo solo números, un único punto decimal y un minus al inicio
        cleaned_text = text
        if text.startswith("-"):
            # Permitir un único punto decimal después del signo negativo
            cleaned_text = "-" + "".join(filter(lambda c: c.isdigit() or c == ".", text[1:]))
        else:
            # Permitir un único punto decimal
            cleaned_text = "".join(filter(lambda c: c.isdigit() or c == ".", text))

        # Asegurarse de que solo haya un punto decimal
        if cleaned_text.count(".") > 1:
            parts = cleaned_text.split(".")
            cleaned_text = parts[0] + "." + "".join(parts[1:])

        # Si el texto ha cambiado, actualizar el editor
        if cleaned_text != text:
            editor.setText(cleaned_text)