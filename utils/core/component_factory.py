from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt

def create_info_item(icon, text, description=None):
    """Crea un elemento de información con icono y descripción"""
    feature_item = QFrame()
    feature_item.setObjectName("featureItem")
    feature_layout = QVBoxLayout(feature_item)
    feature_layout.setSpacing(8)
    feature_layout.setContentsMargins(12, 12, 12, description is not None and 12 or 6)
    
    header_layout = QHBoxLayout()
    header_layout.setSpacing(12)
    
    icon_label = QLabel(icon)
    icon_label.setObjectName("featureIcon")
    icon_label.setAlignment(Qt.AlignCenter)
    icon_label.setFixedWidth(40)
    icon_label.setFixedHeight(40)
    icon_label.setAutoFillBackground(True) 

    text_label = QLabel(text)
    text_label.setObjectName("featureText")
    text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    header_layout.addWidget(icon_label)
    header_layout.addWidget(text_label)
    
    feature_layout.addLayout(header_layout)
    
    if description:
        desc_label = QLabel(description)
        desc_label.setObjectName("featureDescription")
        desc_label.setWordWrap(True)
        desc_label.setContentsMargins(12, 0, 0, 0)
        feature_layout.addWidget(desc_label)

    return feature_item
