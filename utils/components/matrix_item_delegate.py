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
            
        # Limpiar el texto de cualquier caracter no numérico excepto el minus al inicio
        cleaned_text = text
        if text.startswith("-"):
            cleaned_text = "-" + "".join(filter(str.isdigit, text[1:]))
        else:
            cleaned_text = "".join(filter(str.isdigit, text))
            
        # Si el texto ha cambiado, actualizar el editor
        if cleaned_text != text:
            editor.setText(cleaned_text)