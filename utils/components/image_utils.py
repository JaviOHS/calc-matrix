from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from utils.core.resources import resource_path

def load_pixmap(image_path, from_resources=True):
    path = resource_path(image_path) if from_resources else image_path
    return QPixmap(path)

def create_image_label(image_path, width=None, height=None, keep_aspect_ratio=True, smooth_transform=True, alignment=Qt.AlignCenter, from_resources=True):
    label = QLabel()
    pixmap = load_pixmap(image_path, from_resources)
    
    # Escalar si se proporcionan dimensiones
    if width is not None or height is not None:
        w = width if width is not None else pixmap.width()
        h = height if height is not None else pixmap.height()
        
        transform_mode = Qt.SmoothTransformation if smooth_transform else Qt.FastTransformation
        aspect_mode = Qt.KeepAspectRatio if keep_aspect_ratio else Qt.IgnoreAspectRatio
        
        pixmap = pixmap.scaled(w, h, aspect_mode, transform_mode)
    
    label.setPixmap(pixmap)
    label.setAlignment(alignment)
    return label

def set_image(label, image_path, width=None, height=None, keep_aspect_ratio=True, smooth_transform=True, from_resources=True):
    pixmap = load_pixmap(image_path, from_resources)
    
    # Escalar si se proporcionan dimensiones
    if width is not None or height is not None:
        w = width if width is not None else pixmap.width()
        h = height if height is not None else pixmap.height()
        
        transform_mode = Qt.SmoothTransformation if smooth_transform else Qt.FastTransformation
        aspect_mode = Qt.KeepAspectRatio if keep_aspect_ratio else Qt.IgnoreAspectRatio
        
        pixmap = pixmap.scaled(w, h, aspect_mode, transform_mode)
    
    label.setPixmap(pixmap)
    return label
