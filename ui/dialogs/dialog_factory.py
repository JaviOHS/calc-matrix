from ui.dialogs.simple.message_dialog import MessageDialog
from ui.dialogs.specialized.canvas_dialog import CanvasDialog

class DialogFactory:
    """Fábrica para crear y mostrar diálogos especializados según el tipo de resultado"""
    @staticmethod
    def show_message_dialog(title, message, title_color=None, image_name=None, parent=None):
        """Muestra un diálogo de mensaje simple"""
        dialog = MessageDialog(title=title,title_color=title_color,message=message,image_name=image_name,parent=parent)
        dialog.exec()
    
    @staticmethod
    def show_canvas_dialog(canvas, operation_type=None, parent=None, **kwargs):
        """Muestra un diálogo con canvas según el tipo de operación"""
        dialog_config = {"title": "🟢 GRÁFICA DE FUNCIÓN","title_color": "#7cb342","image_path": "assets/images/dialogs/success.png"} 
        dialog_config["title"]="📊 GRÁFICA DE FUNCIÓN 2D" if operation_type == "2d_graph" else "📊 GRÁFICA DE FUNCIÓN 3D"
        
        dialog = CanvasDialog(title=dialog_config["title"],title_color=dialog_config["title_color"],canvas=canvas,image_path=dialog_config["image_path"],parent=parent)
        dialog.exec()
    
    @staticmethod
    def show_result_dialog(result, operation_type=None, parent=None, **kwargs):
        """Muestra un diálogo con el resultado según su tipo y la operación"""
        if operation_type == "differential_equation":
            required_params = ["equation", "initial_condition", "method", "x_range"]
            has_required_params = all(param in kwargs for param in required_params)

            if (hasattr(result, 'draw') or 
                (isinstance(result, dict) and "canvas" in result)):
                
                canvas = result if hasattr(result, 'draw') else result["canvas"]
                html_content = result.get("html") if isinstance(result, dict) else None
                
                if has_required_params:
                    method = kwargs.get("method", "euler")
                    method_names = {"analytical": "Solución Analítica", "euler": "Método de Euler", "heun": "Método de Heun", "rk4": "Método de Runge-Kutta (4º orden)", "taylor": "Método de Taylor (2º orden)"}
                    method_title = method_names.get(method, method.upper())
                    
                    dialog = CanvasDialog(
                        title=f"🟢 SOLUCIÓN DE EDO - {method_title}",
                        title_color="#4caf50",
                        html_content=html_content,
                        canvas=canvas,
                        image_path="assets/images/dialogs/edo.png",
                        parent=parent
                    )
                    
                    # Añadir botón de comparación si hay modelo simbólico
                    if kwargs.get("sym_model"):
                        toolbar_buttons = [
                            ("comparative.svg", "Comparación de métodos numéricos", 
                            lambda: DialogFactory._show_ode_comparison(kwargs))
                        ]
                        dialog.add_toolbar_buttons(toolbar_buttons)
                    
                    dialog.exec()
                    return
                
        # Resultados de operaciones con canvas
        if isinstance(result, dict) and "canvas" in result:
            html_content = result.get("html")
            canvas = result["canvas"]
            dialog = CanvasDialog(title=f"🟢 RESULTADO", title_color="#7cb342", html_content=html_content,canvas=canvas, image_path="assets/images/dialogs/error.png", parent=parent)
            dialog.exec()
            return
            
        # En caso de que el resultado tenga un método draw
        if hasattr(result, 'draw'):
            DialogFactory.show_canvas_dialog(canvas=result, operation_type=operation_type, parent=parent, **kwargs)
            return
        
        # Para resultados con canvas genéricos
        if isinstance(result, dict) and "canvas" in result:
            html_content = result.get("html")
            canvas = result["canvas"]
            dialog = CanvasDialog(title=f"🟢 RESULTADO CON CANVAS GENÉRICO", title_color="#7cb342", html_content=html_content, canvas=canvas, image_path="assets/images/dialogs/success.png", parent=parent)
            dialog.exec()
            return
            
        # Para resultados de solo HTML
        html_content = result if isinstance(result, str) else None
        if html_content:
            dialog = MessageDialog(title=f"🟢 RESULTADO DE {operation_type.replace('_', ' ').upper()}",  title_color="#7cb342",  message=html_content,  image_name=None,  parent=parent)
            dialog.exec()
            return
            
        # Fallback para cualquier otro tipo de resultado
        dialog = MessageDialog(title="⚠️ RESULTADO NO RECONOCIDO", title_color="#ff9800", message=f"No se pudo mostrar el resultado de tipo: {type(result).__name__}", image_name="error.png", parent=parent)
        dialog.exec()
    
    @staticmethod
    def _show_ode_comparison(params):
        """Muestra un diálogo de comparación de métodos ODE"""
        try:
            from utils.parsers.expression_parser import ExpressionParser

            # Obtener parámetros
            sym_model = params.get("sym_model")
            equation_text = params.get("equation")
            initial_condition = params.get("initial_condition")
            x_range = params.get("x_range")
            h = params.get("h", 0.1)
            parent = params.get("parent")
            
            if not all([sym_model, equation_text, initial_condition, x_range]):
                raise ValueError("Faltan parámetros necesarios para la comparación")
                
            # Parsear la ecuación
            parser = ExpressionParser()
            f, expr_text = parser.parse_ode_for_numerical(equation_text)
            parsed_equation = (f, expr_text)
            
            # Generar comparación
            canvas = sym_model.compare_ode_methods(equation=parsed_equation, initial_condition=initial_condition, x_range=x_range, h=h)
            
            # Mostrar resultado
            dialog = CanvasDialog(title="🔍 COMPARACIÓN DE MÉTODOS NUMÉRICOS", title_color="#3f51b5", canvas=canvas, image_path="assets/images/dialogs/comparative.png", parent=parent)
            dialog.exec()
            
        except Exception as e:
            DialogFactory.show_message_dialog(title="❌ ERROR", message=f"No se pudo realizar la comparación:\n{str(e)}", title_color="#d32f2f", image_name="error.png", parent=params.get("parent"))