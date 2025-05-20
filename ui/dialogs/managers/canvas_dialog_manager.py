from ui.dialogs.simple.message_dialog import MessageDialog
from ui.dialogs.specialized.canvas_dialog import CanvasDialog
from utils.parsers.expression_parser import ExpressionParser

class CanvasDialogManager:
    """Gestor para mostrar diálogos con canvas (gráficos) y/o resultados HTML"""
    def __init__(self, parent_widget=None):
        self.parent_widget = parent_widget
        self._ode_params = None
    
    def show_canvas_dialog(self, canvas, title="🟢 GRÁFICA DE FUNCIÓN", title_color="#7cb342", image_name="success.png"):
        """Muestra un diálogo con el canvas proporcionado"""
        if not canvas:
            return
        
        # Construir ruta completa para la imagen
        image_path = f"assets/images/dialogs/{image_name}" if image_name else None
        
        # Usar el nuevo diálogo de canvas
        dialog = CanvasDialog(
            title=title, 
            title_color=title_color,
            canvas=canvas,
            image_path=image_path, 
            parent=self.parent_widget
        )
        dialog.exec()

    def show_result_dialog(self, html_content=None, canvas=None, title="🟢 RESULTADO", title_color="#7cb342", toolbar_buttons=None, image_path="assets/images/dialogs/edo.png"):
        """Muestra un diálogo con HTML y/o canvas"""
        if not html_content and not canvas:
            return
        
        # Usar la clase CanvasDialog directamente
        dialog = CanvasDialog(
            title=title,
            title_color=title_color,
            html_content=html_content,
            canvas=canvas,
            image_path=image_path,
            parent=self.parent_widget,
            toolbar_buttons=toolbar_buttons
        )
        dialog.exec()
    
    def show_ode_solution_dialog(self, canvas, equation, initial_condition, x_range, h, method="euler", sym_model=None, title="🟢 SOLUCIÓN DE EDO", title_color="#7cb342", html_content=None):
        """Muestra un diálogo con la solución de una EDO"""
        if not canvas:
            return
        
        # Guardar parámetros para comparación posterior
        self._ode_params = {
            "equation": equation,
            "initial_condition": initial_condition,
            "x_range": x_range,
            "h": h,
            "current_method": method,
            "sym_model": sym_model
        }
        
        # Botones personalizados para la toolbar
        toolbar_buttons = []
        if sym_model:
            toolbar_buttons.append(
                ("comparative.svg", "Comparación de métodos numéricos", self._show_comparison_dialog)
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
        
        # Mostrar diálogo
        self.show_result_dialog(
            html_content=html_content, 
            canvas=canvas, 
            title=final_title, 
            title_color=title_color, 
            toolbar_buttons=toolbar_buttons, 
            image_path="assets/images/dialogs/edo.png"
        )
    
    def _show_comparison_dialog(self):
        """Maneja el evento de clic en el botón de comparación."""
        if not hasattr(self, "_ode_params") or not self._ode_params["sym_model"]:
            return
            
        try:
            # Obtener parámetros guardados
            params = self._ode_params
            sym_model = params["sym_model"]
            
            # Parsear la ecuación
            parser = ExpressionParser()
            equation_text = params["equation"]
            f, expr_text = parser.parse_ode_for_numerical(equation_text)
            parsed_equation = (f, expr_text)
            
            # Generar comparación
            canvas = sym_model.compare_ode_methods(
                equation=parsed_equation,
                initial_condition=params["initial_condition"],
                x_range=params["x_range"],
                h=params["h"]
            )
            
            # Mostrar resultado en un nuevo diálogo
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