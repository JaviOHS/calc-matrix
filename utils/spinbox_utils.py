from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox
from PySide6.QtCore import Qt

def configure_spinbox(spinbox, min_val=-1000, max_val=1000, decimals=2, default_val=0, width=70, step=0.5):
    spinbox.setRange(min_val, max_val)
    spinbox.setDecimals(decimals)
    spinbox.setValue(default_val)
    spinbox.setSingleStep(step)
    spinbox.setFixedWidth(width)
    spinbox.setAlignment(Qt.AlignCenter)
    spinbox.setObjectName("input_double_spinbox")
    return spinbox

def create_spinbox(min_val=-1000, max_val=1000, decimals=2, default_val=0, width=70, step=0.5):
    spinbox = QDoubleSpinBox()
    return configure_spinbox(spinbox, min_val, max_val, decimals, default_val, width, step)

def configure_int_spinbox(spinbox, min_val=1, max_val=100, default_val=4, width=70, step=1):
    spinbox.setRange(min_val, max_val)
    spinbox.setValue(default_val)
    spinbox.setSingleStep(step)
    spinbox.setFixedWidth(width)
    spinbox.setAlignment(Qt.AlignCenter)
    spinbox.setObjectName("input_int_spinbox")
    return spinbox

def create_int_spinbox(min_val=1, max_val=100, default_val=4, width=70, step=1):
    spinbox = QSpinBox()
    return configure_int_spinbox(spinbox, min_val, max_val, default_val, width, step)
