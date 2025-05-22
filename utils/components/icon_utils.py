from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtCore import QSize, Qt

class PainterContext:
    def __init__(self, device):
        self.device = device
        self.painter = QPainter()

    def __enter__(self):
        self.painter.begin(self.device)
        return self.painter

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.painter.end()

def colored_svg_icon(path: str, color: QColor, size: QSize = QSize(24, 24)) -> QIcon:
    """Crea un icono a partir de un archivo SVG y aplica un color."""
    if not path or not color:
        return QIcon()
    
    pixmap = QPixmap(size)
    if pixmap.isNull():
        return QIcon()
        
    pixmap.fill(Qt.transparent)
    
    renderer = QSvgRenderer(path)
    if not renderer.isValid():
        return QIcon()

    with PainterContext(pixmap) as painter:
        if painter and painter.isActive():
            renderer.render(painter)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), color)

    return QIcon(pixmap)

def colored_svg_pixmap(path: str, color: QColor, size: QSize = QSize(32, 32)) -> QPixmap:
    """Crea un pixmap a partir de un archivo SVG y aplica un color."""
    pixmap = QPixmap(size)
    if pixmap.isNull():
        return pixmap
        
    pixmap.fill(Qt.transparent)
    
    renderer = QSvgRenderer(path)
    if not renderer.isValid():
        return pixmap

    with PainterContext(pixmap) as painter:
        if painter and painter.isActive():
            renderer.render(painter)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), color)

    return pixmap