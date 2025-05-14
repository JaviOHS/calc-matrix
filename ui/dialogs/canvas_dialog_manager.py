from ui.dialogs.message_dialog import MessageDialog
from ui.widgets.expression_components.custom_toolbar import CustomNavigationToolbar
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QSizePolicy, QHBoxLayout
from utils.image_utils import create_image_label

class CanvasDialogManager:
    """Gestor para mostrar diálogos con canvas (gráficos) y/o resultados HTML"""
    def __init__(self, parent_widget: QWidget = None):
        self.parent_widget = parent_widget
        self._ode_params = None
    
    def show_canvas_dialog(self, canvas, title="🟢 GRÁFICA DE FUNCIÓN", title_color="#7cb342", image_name="success.png"):
        """Muestra un diálogo con el canvas proporcionado y barra de herramientas"""
        if not canvas:
            return
        
        # Crear un contenedor para el canvas y la barra de herramientas
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.setSpacing(0)
        
        # Configura el canvas para que tenga un tamaño mínimo pero que pueda expandirse
        canvas.setMinimumSize(600, 400)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Añadir una barra de herramientas de Matplotlib
        toolbar = CustomNavigationToolbar(canvas, canvas_container)
        
        # Añadir el toolbar y el canvas al layout
        canvas_layout.addWidget(toolbar)
        canvas_layout.addWidget(canvas)
        
        canvas.draw() # Dibujar el canvas
        
        # Mostrar el diálogo con el contenedor que incluye el canvas y la barra
        dialog = MessageDialog(title=title, title_color=title_color, image_name=image_name, parent=self.parent_widget, custom_widget=canvas_container)
        dialog.exec()

    def show_result_dialog(self, html_content=None, canvas=None, title="🟢 RESULTADO", title_color="#7cb342", toolbar_buttons=None, image_path="assets/images/dialogs/edo.png"):
        if not html_content and not canvas:
            return
            
        # Crear contenedor para el contenido combinado
        combined_widget = QWidget()
        combined_layout = QHBoxLayout(combined_widget)
        combined_layout.setContentsMargins(10, 10, 10, 10)
        combined_layout.setSpacing(15)
        
        # Contenedor izquierdo para HTML y la imagen
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)
        
        # Agregar el resultado HTML si existe
        if html_content:
            html_display = QTextBrowser()
            html_display.setHtml(html_content)
            html_display.setMinimumHeight(150)
            html_display.setMinimumWidth(250)
            html_display.setOpenExternalLinks(True)
            left_layout.addWidget(html_display)
        
        # Agregar imagen debajo del HTML si se proporciona ruta
        if image_path:
            image_label = create_image_label(image_path, width=128, height=128)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            image_container = QWidget()
            image_layout = QHBoxLayout(image_container)
            image_layout.addStretch()
            image_layout.addWidget(image_label)
            image_layout.addStretch()
            left_layout.addWidget(image_container)
            left_layout.addStretch()
        
        # Agregar el contenedor izquierdo al layout principal
        combined_layout.addWidget(left_container)
        
        # Contenedor para el canvas con barra de herramientas
        if canvas:
            canvas_container = QWidget()
            canvas_layout = QVBoxLayout(canvas_container)
            canvas_layout.setContentsMargins(0, 0, 0, 0)
            canvas_layout.setSpacing(0)
            
            # Configurar canvas para que se expanda correctamente
            canvas.setMinimumSize(500, 350)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            # Agregar barra de herramientas
            toolbar = CustomNavigationToolbar(canvas, canvas_container)
            
            # Añadir botones personalizados si se proporcionan
            if toolbar_buttons:
                for icon_name, tooltip, callback in toolbar_buttons:
                    try:
                        toolbar.add_custom_button(icon_name, tooltip, callback)
                    except Exception as e:
                        print(f"No se pudo añadir botón ({icon_name}): {e}")
            
            canvas_layout.addWidget(toolbar)
            canvas_layout.addWidget(canvas)
            
            # Dibujar el canvas
            canvas.draw()
            combined_layout.addWidget(canvas_container)
        
        # Se envía la imagen vacía ya que se está colocando directamente en el layout
        dialog = MessageDialog(title=title, title_color=title_color, image_name=None, parent=self.parent_widget, custom_widget=combined_widget)
        dialog.exec()
    
    def show_ode_solution_dialog(self, canvas, equation, initial_condition, x_range, h, method="euler", sym_model=None, title="🟢 SOLUCIÓN DE EDO", title_color="#7cb342", html_content=None):
        """Muestra un diálogo con la solución de una EDO, aprovechando show_result_dialog"""
        if not canvas:
            return
        
        # Guardar parámetros para la comparación posterior
        self._ode_params = {
            "equation": equation,
            "initial_condition": initial_condition,
            "x_range": x_range,
            "h": h,
            "current_method": method,
            "sym_model": sym_model
        }
        
        # Preparar botones personalizados de la barra de herramientas
        toolbar_buttons = []
        
        # Añadir botón de comparación si tenemos el modelo simbólico
        if sym_model:
            toolbar_buttons.append(
                ("comparative.svg", "Compación de métodos numéricos", self._show_comparison_dialog)
            )
        
        # Título con nombre del método
        method_names = {
            "analytical": "Solución Analítica",
            "euler": "Método de Euler",
            "heun": "Método de Heun",
            "rk4": "Método de Runge-Kutta (4º orden)",
            "taylor": "Método de Taylor (2º orden)"
        }
        method_title = method_names.get(method, method.upper())
        final_title = f"{title} - {method_title}"
        
        # Usar show_result_dialog con los parámetros específicos para EDO
        self.show_result_dialog(html_content=html_content, canvas=canvas, title=final_title, title_color=title_color, toolbar_buttons=toolbar_buttons, image_path="assets/images/dialogs/edo.png")
        
    def _show_comparison_dialog(self):
        """Maneja el evento de clic en el botón de comparación."""
        if not hasattr(self, "_ode_params") or not self._ode_params["sym_model"]:
            return
            
        try:
            # Obtener parámetros guardados
            params = self._ode_params
            sym_model = params["sym_model"]
            
            # Parsear la ecuación antes de llamar al método de comparación
            from utils.parsers.expression_parser import ExpressionParser
            parser = ExpressionParser()
            
            # Obtener la ecuación en formato texto
            equation_text = params["equation"]
            
            # Parsear la ecuación para obtener la tupla (función, texto)
            f, expr_text = parser.parse_ode_for_numerical(equation_text)
            parsed_equation = (f, expr_text)
            
            # Generar comparación con la ecuación parseada
            canvas = sym_model.compare_ode_methods(
                equation=parsed_equation,  # Ahora es una tupla (f, expr_text)
                initial_condition=params["initial_condition"],
                x_range=params["x_range"],
                h=params["h"]
            )
            
            # Mostrar el canvas en un nuevo diálogo
            self.show_canvas_dialog(
                canvas=canvas,
                title="🔍 COMPARACIÓN DE MÉTODOS NUMÉRICOS",
                title_color="#3f51b5",
                image_name="comparative.png"
            )

        except Exception as e:
            MessageDialog(
                title="❌ ERROR",
                message=f"No se pudo realizar la comparación:\n{str(e)}",
                title_color="#d32f2f",
                image_name="error.png",
                parent=self.parent_widget
            ).exec()
