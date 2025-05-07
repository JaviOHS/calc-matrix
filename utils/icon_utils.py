from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtCore import QSize, Qt

def colored_svg_icon(path: str, color: QColor, size: QSize = QSize(24, 24)) -> QIcon:
    """
    Devuelve un QIcon coloreado a partir de un archivo SVG.

    Args:
        path (str): Ruta al archivo SVG.
        color (QColor): Color que se aplicará al SVG.
        size (QSize): Tamaño del icono resultante.

    Returns:
        QIcon: El ícono coloreado.
    """
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)

    # Renderiza el SVG al pixmap
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    # Aplica el color con CompositionMode_SourceIn
    painter.begin(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()

    return QIcon(pixmap)

def colored_svg_pixmap(path: str, color: QColor, size: QSize = QSize(32, 32)) -> QPixmap:
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)

    # Renderiza el SVG original
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    # Aplica el color sobre el pixmap
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()

    return pixmap
