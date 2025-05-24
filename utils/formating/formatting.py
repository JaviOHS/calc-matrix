from .base import create_section
from .polynomials import format_polynomial, format_evaluation_result, format_roots_result
from .matrices import format_vector
from .diff_equations import format_diff_eq, format_numerical_method
from .distributions import format_transform_distribution_result, format_monte_carlo_result, format_markov_epidemic_result
from ..patterns import COLORS, ICONS

def format_math_expression(expr, result, operation_type="generic", method=None):
    """Formatea resultados matemáticos según el tipo de operación"""
    if operation_type == "evaluation":
        return format_evaluation_result(expr, result)

    if operation_type == "markov_epidemic":
        return format_markov_epidemic_result(expr, result)
    
    if operation_type in ["vector", "matrix"]:
        formatted_expr = format_polynomial(expr)
        formatted_result = format_vector(result)
        
        return (
            create_section('Operación con Vectores/Matrices:<br>', formatted_expr, COLORS['secondary'], ICONS['matrix']) +
            create_section('Resultado:<br>', formatted_result, COLORS['primary'], ICONS['result'])
        )
    
    if operation_type == "roots":
        return format_roots_result(expr, result)

    
    if operation_type == "monte_carlo":
        return format_monte_carlo_result(result)
    
    if operation_type in ["polynomial", "derivative", "integral"]:
        formatted_expr = format_polynomial(expr)
        formatted_result = format_polynomial(result)
        
        return (
            create_section('Expresión Original:<br>', formatted_expr, COLORS['secondary'], ICONS['operation']) +
            create_section('Resultado Simplificado:<br>', formatted_result, COLORS['primary'], ICONS['result'])
        )
    
    if operation_type == "differential_equation":
        if method in ["euler", "heun", "rk4", "taylor"]:
            method_names = {
                "euler": "Euler",
                "heun": "Heun", 
                "rk4": "Runge-Kutta 4º Orden",
                "taylor": "Taylor 2° orden"
            }
            method_display = method_names.get(method, method.capitalize())
            return format_numerical_method(result, method_display)
        else:
            return format_diff_eq(expr, result)
        
    if operation_type == "transform_distribution":
        # Extraer información de la operación
        generation_method = expr.get("generation_method", "manual")
        transform_method = expr.get("transform_method", "")
        transform_params = expr.get("transform_params", {})
        original_numbers = expr.get("original_numbers", [])
        
        # Formatear usando la función especializada
        return format_transform_distribution_result(
            original_numbers, 
            result, 
            generation_method,
            transform_method, 
            transform_params
        )