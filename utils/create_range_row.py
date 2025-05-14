from PySide6.QtWidgets import QHBoxLayout, QLabel
from utils.spinbox_utils import create_spinbox

def create_range_row(label_text=None, min_label="Min", max_label="Max", default_min=0.0, default_max=1.0, min_control=None, max_control=None, connector="a",spacing=6, label_width=None):
    """
    Crea una fila de controles para un rango (min/max) con etiquetas personalizables
    
    Args:
        label_text: Etiqueta principal de la fila (opcional)
        min_label: Etiqueta para el valor mínimo
        max_label: Etiqueta para el valor máximo
        default_min: Valor predeterminado para mínimo
        default_max: Valor predeterminado para máximo
        min_control: Control mínimo existente (si es None, se creará uno)
        max_control: Control máximo existente (si es None, se creará uno)
        connector: Texto a mostrar entre controles min y max (predeterminado: "a")
        spacing: Espaciado entre elementos
        label_width: Ancho fijo para la etiqueta principal (opcional)
        
    Returns:
        Tuple of (layout, min_control, max_control)
    """
    layout = QHBoxLayout()
    layout.setSpacing(spacing)
    
    # Etiqueta principal si se proporciona
    if label_text:
        label = QLabel(f"{label_text}:")
        if label_width:
            label.setFixedWidth(label_width)
        layout.addWidget(label)
    
    # Crear o usar controles proporcionados
    if min_control is None:
        min_control = create_spinbox(default_val=default_min)
    else:
        min_control.setValue(default_min)
        
    if max_control is None:
        max_control = create_spinbox(default_val=default_max)
    else:
        max_control.setValue(default_max)
    
    # Agregar control mínimo con etiqueta
    if min_label:
        layout.addWidget(QLabel(min_label))
    layout.addWidget(min_control)
    
    # Conector (si es necesario)
    if connector:
        layout.addWidget(QLabel(connector))
    
    # Agregar control máximo con etiqueta
    if max_label:
        layout.addWidget(QLabel(max_label))
    layout.addWidget(max_control)
    
    layout.addStretch()
    return layout, min_control, max_control
