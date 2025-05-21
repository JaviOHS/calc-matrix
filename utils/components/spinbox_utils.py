from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox, QLabel, QWidget, QHBoxLayout
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

def create_float_spinbox(min_val=-1000, max_val=1000, decimals=2, default_val=0, width=70, step=0.5, label_text=None):
    container = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    
    spinbox = QDoubleSpinBox()
    spinbox = configure_spinbox(spinbox, min_val, max_val, decimals, default_val, width, step)
    
    if label_text:
        label = QLabel(label_text)
        layout.addWidget(label)
    
    layout.addWidget(spinbox)
    layout.addStretch()
    
    container.setLayout(layout)
    container.spinbox = spinbox
    return container

def configure_int_spinbox(spinbox, min_val=1, max_val=100, default_val=4, width=70, step=1):
    spinbox.setRange(min_val, max_val)
    spinbox.setValue(default_val)
    spinbox.setSingleStep(step)
    spinbox.setFixedWidth(width)
    spinbox.setAlignment(Qt.AlignCenter)
    spinbox.setObjectName("input_int_spinbox")
    return spinbox

def create_int_spinbox(min_val=1, max_val=100, default_val=4, width=70, step=1, label_text=None):
    container = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    
    spinbox = QSpinBox()
    spinbox = configure_int_spinbox(spinbox, min_val, max_val, default_val, width, step)
    
    if label_text:
        label = QLabel(label_text)
        layout.addWidget(label)
    
    layout.addWidget(spinbox)
    layout.addStretch()
    
    container.setLayout(layout)
    container.spinbox = spinbox
    return container
