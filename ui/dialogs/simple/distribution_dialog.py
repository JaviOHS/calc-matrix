from ui.dialogs.specialized.canvas_dialog import CanvasDialog

class DistributionDialog(CanvasDialog):
    """Diálogo especializado para mostrar resultados de distribuciones"""
    def __init__(self, operation_type, result_data, parent=None):
        dialog_config = {
            "markov_epidemic": {
                "title": "🦠 SIMULACIÓN DE EPIDEMIA",
                "title_color": "#ff8103",
                "image_path": None,
                "min_width": 900,
                "min_height": 600
            },
            "monte_carlo": {
                "title": "📊 INTEGRACIÓN MONTE CARLO",
                "title_color": "#2196F3",
                "image_path": None,
                "min_width": 400,
                "min_height": 400
            },
            "random_numbers": {
                "title": "🎲 GENERACIÓN ALEATORIA",
                "title_color": "#4CAF50",
                "image_path": None,
                "min_width": 400,
                "min_height": 492
            }
        }
        
        # Obtener configuración
        config = dialog_config.get(operation_type, {
            "title": "🟢 RESULTADO", 
            "title_color": "#7cb342",
            "image_path": "assets/images/dialogs/success.png",
            "min_width": 600,
            "min_height": 400
        })
        
        # Extraer datos del resultado
        html_content = result_data.get("html")
        canvas = result_data.get("canvas")
        
        # Inicializar diálogo base con la configuración
        super().__init__(
            title=config["title"], 
            title_color=config["title_color"], 
            html_content=html_content, 
            canvas=canvas, 
            image_path=config["image_path"], 
            parent=parent
        )
        
        # Establecer tamaños mínimos según el tipo de operación
        self.setMinimumSize(config["min_width"], config["min_height"])
        