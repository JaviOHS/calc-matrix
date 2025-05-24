from .base import create_section, clean_number
from .polynomials import format_polynomial
from ..patterns import COLORS, ICONS

from utils.core.font_weight_manager import FontWeightManager
bold = FontWeightManager.get_weight("strong")

def format_transform_distribution_result(original_data, transformed_data, method, transform_method, transform_params):
    """Formatea el resultado de la transformación de distribuciones"""
    # Límite de datos a mostrar
    max_display = 900
    display_all = len(original_data) <= max_display
    
    # Nombres amigables para los métodos
    method_display = method.capitalize().replace("_", " ")
    transform_display = transform_method.capitalize().replace("_", " ")
    
    # Formatear parámetros como texto
    params_text = ", ".join([f"{k}={clean_number(v)}" for k, v in transform_params.items()])
    
    # Construir información de operación
    operation_info = (
        f"<div style='margin-bottom: 2px;'>"
        f"<ul>"
        f"<li><b>Método generador:</b> {method_display}</li>"
        f"<li><b>Transformación:</b> {transform_display} {f'({params_text})' if params_text else ''}</li>"
        # f"<li><b>Total generado:</b> {len(original_data)} números</li>"
        f"</ul>"
        f"</div>"
    )
    
    # Construir la tabla HTML con estilo similar a métodos numéricos
    table_html = (
        "<div style='margin: 15px 0; padding: 15px; border-radius: 8px; "
        "display: flex; justify-content: center; align-items: center;'>"
        "<table style='width: 80%; border-collapse: collapse; text-align: center;'>"
        "<thead>"
        "<tr>"
        "<th style='padding: 12px; border-bottom: 2px solid #ff8103; "
        f"color: #2196F3; font-weight: {bold}; width: 50%; text-align: center;'>Uniforme [0,1]</th>"
        "<th style='padding: 12px; border-bottom: 2px solid #ff8103; "
        f"color: #9C27B0; font-weight: {bold}; width: 50%; text-align: center;'>" + transform_display + "</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
    )
    
    # Añadir filas de datos
    for i, (orig, trans) in enumerate(zip(original_data, transformed_data)):
        if i >= max_display and not display_all:
            table_html += (
                "<tr>"
                "<td colspan='2' style='padding: 8px; border-bottom: 1px solid #EEEEEE; "
                "color: #777777; font-style: italic; text-align: center;'>... " + str(len(original_data) - max_display) + " valores más ...</td>"
                "</tr>"
            )
            break
        
        table_html += (
            "<tr>"
            f"<td style='padding: 8px; border-bottom: 1px solid #EEEEEE; text-align: center;'>{clean_number(orig)}</td>"
            f"<td style='padding: 8px; border-bottom: 1px solid #EEEEEE; text-align: center;'>{clean_number(trans)}</td>"
            "</tr>"
        )
    
    table_html += (
        "</tbody>"
        "</table>"
        "</div>"
    )
    
    # Crear las secciones con el diseño estándar de la aplicación
    return (
        create_section(
            'Configuración:', 
            operation_info, 
            COLORS['secondary'], 
            ICONS['operation']
        ) +
        create_section(
            'Tabla de transformación:', 
            table_html, 
            COLORS['primary'], 
            ICONS['result']
        )
    )

def format_markov_epidemic_result(params, epidemic_data):
        """Formatea el resultado de la simulación de epidemias"""
        # Calcular el R₀ (número reproductivo básico)
        r0 = params['beta'] / params['gamma']
        
        # Preparar la sección de parámetros con mejor formato y colores
        params_html = (
            f"<div style='padding: 15px;'>"
            f"<ul style='list-style-type: '📌'; padding: 0; margin: 0;'>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Método:</span> {params['algorithm'].replace('_', ' ').capitalize()}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Semilla:</span> {params['seed']}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Población total:</span> {params['population']}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Infectados iniciales:</span> {params['initial_infected']}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Recuperados iniciales:</span> {params['initial_recovered']}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Susceptibles iniciales:</span> {params['population'] - params['initial_infected'] - params['initial_recovered']}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Tasa de infección (β):</span> {params['beta']:.3f}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Tasa de recuperación (γ):</span> {params['gamma']:.3f}</li>"
            f"<li style='margin: 5px 0;'><span style='font-weight: {bold};'>Número reproductivo (R₀):</span> {r0:.2f}</li>"
            f"</ul>"
            f"</div>"
        )

        # Análisis con mejor formato visual
        analysis_html = (
            f"<div style='padding: 15px; border-radius: 8px;'>"
        )

        # Pico de infección
        infected = epidemic_data.get('infected', [])
        times = epidemic_data.get('times', [])
        if infected:
            max_infected = max(infected)
            max_infected_day = times[infected.index(max_infected)]
            analysis_html += (
                f"<div style='margin: 8px 0; padding: 8px; border-left: 3px solid #CE723B;'>"
                f"<p style='margin: 0;'><span style='color: #f44336; font-weight: {bold};'>🤒 Pico de infección:</span> "
                f"{int(max_infected)} personas (Día {max_infected_day:.0f})</p>"
                f"</div>"
            )

        # Análisis del R₀
        analysis_html += (
            f"<div style='margin: 8px 0; padding: 8px;'>"
            f"<p style='margin: 0;'><span style='font-weight: {bold};'>📊 Análisis del R₀:</span><br>"
            f"<span style='color: {'#ff8103' if r0 > 1 else '#4FC1FF'};'>"
            f"{'La epidemia está en fase de crecimiento' if r0 > 1 else 'La epidemia está en fase de retroceso'}"
            f"</span> (R₀ = {r0:.2f})</p>"
            f"</div>"
        )

        # Duración de la epidemia
        duration = next((t for t, i in zip(times, infected) if i < 1), params['days'])
        analysis_html += (
            f"<div style='margin: 8px 0; padding: 8px;'>"
            f"<p style='margin: 0;'><span style='font-weight: {bold};'>⏳ Duración estimada:</span> {duration:.0f} días</p>"
            f"</div>"
        )

        # Porcentaje final
        final_infected = epidemic_data.get('recovered', [])[-1]
        final_infected_percentage = (final_infected / params['population']) * 100
        analysis_html += (
            f"<div style='margin: 8px 0; padding: 8px;'>"
            f"<p style='margin: 0;'><span style='font-weight: {bold};'>📈 Población infectada total:</span> {final_infected_percentage:.2f}%</p>"
            f"</div>"
            f"</div>"
        )

        return (
            create_section(
                "Parámetros de la simulación:", 
                params_html, 
                COLORS['secondary'], 
                ICONS['operation']
            ) +
            create_section(
                "Análisis de resultados:", 
                analysis_html,
                COLORS['primary'], 
                ICONS['result']
            )
        )

def format_monte_carlo_result(result):
    """Formatea el resultado de la integración Monte Carlo"""
    # Extraer los datos relevantes
    success = result.get("success", False)
    integral_result = result.get("result", "N/A")
    error = result.get("error", "N/A")
    n_points = result.get("n_points", "N/A")
    a = result.get("a", "N/A")
    b = result.get("b", "N/A")
    expression = result.get("expression", "N/A")
    # Crear secciones para los parámetros y resultados
    params_html = (
        f"<div style='margin-left: 2px;'>"
        f"<ul>"
        f"<li><b>Límites:</b> [a = {clean_number(a)}, b = {clean_number(b)}]</li>"
        f"<li><b>Número de puntos:</b> {clean_number(n_points)}</li>"
        f"<li><b>Expresión:</b> {format_polynomial(expression)}</li>"
        f"</ul>"
        f"</div>"
    )
    result_html = (
        f"<div style='margin-left: 2px;'>"
        f"<ul>"
        f"<li><b>Resultado de la integral:</b> {clean_number(integral_result)}</li>"
        f"<li><b>Error estimado:</b> {clean_number(error)}</li>"
        f"</ul>"
        f"</div>"
    )
    # Combinar las secciones en un formato final
    return (
        create_section("Parámetros de entrada:", params_html, COLORS["secondary"], ICONS["operation"]) +
        create_section("Resultado:", result_html, COLORS["primary"], ICONS["result"])
    )
