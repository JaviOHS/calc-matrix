from PySide6.QtWidgets import QHBoxLayout, QLabel
from utils.components.spinbox_utils import create_float_spinbox

def create_range_row(label_text=None, min_label="Min", max_label="Max", default_min=0.0, default_max=1.0, min_control=None, max_control=None, connector="a", spacing=6, label_width=None):
    layout = QHBoxLayout()
    layout.setSpacing(spacing)
    
    # Agregar el label principal si se proporciona
    if label_text:
        main_label = QLabel(label_text)
        if label_width:
            main_label.setFixedWidth(label_width)
        layout.addWidget(main_label)
        
        # OPCIONAL: Añadir stretch después del label principal para separarlo de los controles
        # layout.addStretch(1)
    
    # Crear o usar controles proporcionados
    if min_control is None:
        min_control = create_float_spinbox(default_val=default_min, label_text=min_label)
    else:
        min_control.setValue(default_min)
        
    if max_control is None:
        max_control = create_float_spinbox(default_val=default_max, label_text=max_label)
    else:
        max_control.setValue(default_max)
    
    # Agregar los controles juntos (sin stretch entre ellos)
    layout.addWidget(min_control)
    
    # Conector (si es necesario) - esto mantendrá los controles unidos
    if connector:
        layout.addWidget(QLabel(connector))
    
    layout.addWidget(max_control)
    
    # Añadir stretch al final para empujar todo hacia la izquierda
    layout.addStretch(3)
    
    return layout, min_control, max_control
