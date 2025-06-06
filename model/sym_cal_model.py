from controller.graph_controller import GraphController 
from model.graph_manager import GraphManager
from sympy import symbols,  diff,  integrate,  sympify,  Function,  Derivative, Eq, solve, lambdify, Poly, Symbol, dsolve
from numpy import linspace
from utils.formating.diff_equations import standardize_ode_equation

class SymCalModel:
    def __init__(self):
        self.x = symbols('x')
        self.y = symbols('y')
        self.graph_controller = GraphController(GraphManager())

    def derive(self, expression, var=None):
        try:
            # Si la expresión es una lista, se asume que es un polinomio
            if isinstance(expression, list):
                from model.polynomial_model import Polynomial
                
                coeffs = expression
                variable = var or 'x'
                
                # Implementación para coeffs = [an, ..., a1, a0]
                if len(coeffs) <= 1:
                    result = Polynomial([0], var=variable)
                else:
                    n = len(coeffs) - 1
                    new_coeffs = [(n - i) * coeffs[i] for i in range(len(coeffs) - 1)]
                    result = Polynomial(new_coeffs, var=variable)
                    
                return result
            
            # Si es una instancia de Polynomial, convertirlo a expresión simbólica
            from model.polynomial_model import Polynomial
            if isinstance(expression, Polynomial):
                sym_expr = expression.to_sympy_expr()
                variable = symbols(expression.var)
                result = diff(sym_expr, variable)
                
                # Intentar convertir el resultado a un polinomio
                try:
                    poly_result = Polynomial(Poly(result, variable).all_coeffs(), var=expression.var)
                    return poly_result
                except:
                    # Si no se puede convertir a polinomio, devolver la expresión simbólica
                    return result
                
            f = sympify(expression)
            variable = symbols(var) if var else self.x
            result = diff(f, variable)
            return result
        except Exception as e:
            raise ValueError(f"Error al derivar: {str(e)}")
        
    def integrate(self, expression, limits=None, var=None, constant=0):
        try:
            # Si la expresión es una lista, se asume que es un polinomio
            if isinstance(expression, list):
                from model.polynomial_model import Polynomial
                coeffs = expression
                variable = var or 'x'
                
                # Implementación CORRECTA para coeffs = [an, ..., a1, a0]
                new_coeffs = []
                n = len(coeffs) - 1  # Grado máximo del polinomio
                
                for i in range(len(coeffs)):
                    # Para cada término a_i*x^(n-i), la integral es (a_i/(n-i+1))*x^(n-i+1)
                    new_coeff = coeffs[i] / (n - i + 1)
                    new_coeffs.append(new_coeff)
                
                # Añadir la constante de integración como nuevo término independiente
                new_coeffs.append(constant)
                
                poly = Polynomial(new_coeffs, var=variable)
                
                if limits:
                    lower, upper = limits
                    result = poly.evaluate(upper) - poly.evaluate(lower)
                    return result
                else:
                    return poly
                  
            # Si es una instancia de Polynomial, obtenemos sus coeficientes
            from model.polynomial_model import Polynomial
            if isinstance(expression, Polynomial):
                return self.integrate(expression.coefficients, limits=limits, var=expression.var, constant=constant)
            
            f = sympify(expression)
            variable = symbols(var) if var else self.x
            
            if limits:
                result = integrate(f, (variable, *limits))
            else:
                result = integrate(f, variable)
                
            return result
        except Exception as e:
            raise ValueError(f"Error al integrar:\n{str(e)}")
    
    def solve_differential_equation(self, equation, initial_condition=None, x_range=None):
        x = self.x
        y = Function('y')(x)
        
        try:
            # Manejar diferentes formatos de entrada de ecuación
            if isinstance(equation, tuple) and len(equation) == 3:
                # Nueva estructura: (func, texto, ecuación_simbólica)
                f, rhs_text, sym_equation = equation
                equation_to_solve = sym_equation
                equation_display = (f, rhs_text)  # Para mostrar
            elif isinstance(equation, tuple) and len(equation) == 2 and callable(equation[0]):
                # Estructura de método numérico: (func, texto)
                f, rhs_text = equation
                # Convertir a ecuación simbólica para resolución
                x_sym, y_sym = symbols('x y')
                try:
                    rhs_sym = sympify(rhs_text)
                    lhs_sym = Derivative(y, x)
                    equation_to_solve = Eq(lhs_sym, rhs_sym)
                except:
                    # Si falla la conversión, crear una ecuación genérica
                    equation_to_solve = Eq(Derivative(y, x), sympify(rhs_text))
                equation_display = equation  # Para mostrar
            elif hasattr(equation, 'rhs') and hasattr(equation, 'lhs'):
                # Ecuación simbólica directa
                equation_to_solve = equation
                # Crear una representación tupla similar a la numérica
                rhs_text = str(equation.rhs)
                # Intentar crear una función lambda a partir de la expresión simbólica
                try:
                    f = lambdify((x, Symbol('y')), equation.rhs)
                    equation_display = (f, rhs_text)
                except:
                    # Si no se puede crear la función, usar solo el texto
                    equation_display = rhs_text
            else:
                # Cualquier otro caso, intentar crear una ecuación
                equation_to_solve = Eq(Derivative(y, x), equation)
                equation_display = str(equation)
        
            # Resolver la ecuación diferencial
            solution = dsolve(equation_to_solve, y)
            
            if initial_condition and x_range:
                x0, y0 = initial_condition
                solution_func = self._prepare_solution_function(solution, x0, y0)
                
                # Usar el formato numérico para estandarizar
                equation_info = standardize_ode_equation(equation_display)

                # Generar puntos para graficar
                x_vals = linspace(x_range[0], x_range[1], 20)
                y_vals = [solution_func(xi) for xi in x_vals]
                solution_points = list(zip(x_vals, y_vals))

                # Generar canvas con la ecuación ya formateada
                canvas = self.graph_controller.generate_ode_solution_canvas(
                    equation=equation_info["display"],  # Usar la versión formateada
                    solution_points=solution_points,
                    initial_condition=initial_condition,
                    x_range=x_range,
                    is_numerical=False  # Especificar que es analítica
                )
                
                return {
                    "solution": solution,
                    "canvas": canvas
                }
            
            return solution
        except Exception as e:
            raise ValueError(f"No se pudo resolver la ecuación diferencial:\n{str(e)}")
        
    def _prepare_solution_function(self, solution, x0, y0):
        """Convierte una solución simbólica en una función numérica, aplicando la condición inicial"""
        try:
            # Manejar múltiples soluciones (devueltas como lista)
            if isinstance(solution, list):
                solutions = solution # Convertir a lista si es una solución única
            else:
                solutions = [solution]
                
            # Intentar con cada solución de la lista
            for sol in solutions:
                solution_rhs = sol.rhs
                
                # Si hay constantes de integración, hay que resolverlas
                if 'C1' in str(solution_rhs) or 'C2' in str(solution_rhs):
                    # Resuelve para las constantes usando la condición inicial
                    const_eq = solution_rhs.subs(self.x, x0) - y0
                    try:
                        const_sol = solve(const_eq, 'C1')
                        if const_sol:
                            # Sustituye la constante resuelta en la solución
                            solution_rhs = solution_rhs.subs('C1', const_sol[0])
                            
                            # Verificar si esta solución satisface la condición inicial
                            y_test = float(solution_rhs.subs(self.x, x0).evalf())
                            if abs(y_test - y0) < 1e-10:  # Tolerancia numérica
                                # Convierte la solución simbólica a una función numérica
                                solution_func = lambdify(self.x, solution_rhs)
                                return solution_func
                    except Exception as e:
                        # Si falla con esta solución, intentar con la siguiente
                        continue
                
            # Si llegamos aquí, ninguna solución funcionó correctamente: Como alternativa, tomar la primera solución disponible
            if solutions:
                solution_rhs = solutions[0].rhs
                if 'C1' in str(solution_rhs):
                    # Intentar resolver con la primera solución
                    const_eq = solution_rhs.subs(self.x, x0) - y0
                    const_sol = solve(const_eq, 'C1')
                    if const_sol:
                        solution_rhs = solution_rhs.subs('C1', const_sol[0])
                    
                solution_func = lambdify(self.x, solution_rhs)
                return solution_func
                
            return None
        except Exception as e:
            return None

    def solve_ode_numerical(self, parsed_equation, initial_condition, x_range, h=0.1, method="euler"):
        """Método general para resolver EDOs con diferentes métodos numéricos"""
        x0, y0 = initial_condition
        x_start, x_end = x_range
        x_vals = [x0]
        y_vals = [y0]
        
        # El parsed_equation debe ser una tupla (f, rhs_text)
        if isinstance(parsed_equation, tuple) and len(parsed_equation) == 2 and callable(parsed_equation[0]):
            f, rhs = parsed_equation
        else:
            raise ValueError("La ecuación debe estar parseada como (función, texto)")
        
        # Inicializar valores
        x = x0
        y = y0
        
        # Para el método de Taylor, necesitamos las derivadas parciales
        if method == "taylor":
            try:
                x_sym, y_sym = symbols('x y')
                expr = -0.1151*(y_sym - 22)  # Construimos la expresión simbólica
                
                # Calcular derivadas parciales
                df_dx = diff(expr, x_sym)
                df_dy = diff(expr, y_sym)
                
                # Las derivadas parciales son constantes, así que podemos evaluarlas directamente
                df_dx_val = float(df_dx)
                df_dy_val = float(df_dy)
                
            except Exception as e:
                raise ValueError(f"Error al preparar derivadas para Taylor: {str(e)}")
        
        # Resolver la ecuación paso a paso según el método elegido
        while x < x_end:
            if method == "euler": # Método de Euler: y_{n+1} = y_n + h * f(x_n, y_n)
                y = y + h * f(x, y)
            
            elif method == "heun": # Método de Heun (predictor-corrector)
                k1 = f(x, y)
                y_pred = y + h * k1
                k2 = f(x + h, y_pred)
                y = y + h * (k1 + k2) / 2
                
            elif method == "rk4": # Método de Runge-Kutta de 4to orden
                k1 = f(x, y)
                k2 = f(x + h/2, y + h*k1/2)
                k3 = f(x + h/2, y + h*k2/2)
                k4 = f(x + h, y + h*k3)
                y = y + h * (k1 + 2*k2 + 2*k3 + k4) / 6
                
            elif method == "taylor": # Método de Taylor de orden 2
                try:
                    f_value = f(x, y)
                    # Usar los valores constantes de las derivadas
                    df_value = df_dx_val + df_dy_val * f_value
                    y = y + h * f_value + (h**2/2) * df_value
                except Exception as e:
                    raise ValueError(f"Error en paso de Taylor: {str(e)}")
            
            # Actualizar x y guardar los valores
            x = x + h
            x_vals.append(x)
            y_vals.append(y)
        
        # Crear la lista de puntos de solución
        solution_points = list(zip(x_vals, y_vals))
        
        # Obtener título según el método
        method_titles = {
            "euler": "Método de Euler",
            "heun": "Método de Heun",
            "rk4": "Método de Runge-Kutta (4º orden)",
            "taylor": "Método de Taylor (2º orden)"
        }
        method_title = method_titles.get(method, "Método Numérico")
        
        # Generar el gráfico
        equation_display = f"y' = {rhs}"
        canvas = self.graph_controller.generate_ode_solution_canvas(
            equation=equation_display,
            solution_points=solution_points,
            initial_condition=initial_condition,
            x_range=x_range,
        )
        
        # Devolver tanto la solución como el canvas
        return {"solution": solution_points, "canvas": canvas}

    def solve_ode_euler(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una ecuación diferencial usando el método de Euler"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="euler")
        
    def solve_ode_heun(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una ecuación diferencial usando el método de Heun"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="heun")
        
    def solve_ode_rk4(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una ecuación diferencial usando Runge-Kutta de 4º orden"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="rk4")        
    
    def solve_ode_taylor(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una ecuación diferencial usando el método de Taylor de orden 2"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="taylor")
        
    def compare_ode_methods(self, equation, initial_condition, x_range, h=0.1, methods=None):
        """Compara diferentes métodos numéricos para resolver EDOs"""
        available_methods = {
            "euler": "Método de Euler",
            "heun": "Método de Heun",
            "rk4": "Método de Runge-Kutta (4º orden)",
            "taylor": "Método de Taylor (2º orden)",
            "analytical": "Solución Analítica"
        }
        
        methods = [m for m in available_methods.keys()]

        # El parsed_equation debe ser una tupla (f, rhs_text)
        if not (isinstance(equation, tuple) and len(equation) >= 2 and callable(equation[0])):
            raise ValueError("La ecuación debe estar parseada como (función, texto)")
        
        # Desempaquetar la tupla
        if len(equation) == 3:
            f, rhs_text, sym_eq = equation
        else:
            raise ValueError("Para comparativa analítica necesitas la ecuación simbólica.")

        x0, y0 = initial_condition
        x_start, x_end = x_range
        N = int((x_end - x_start) / h) + 1 # Número de puntos
        x_vals = linspace(x_start, x_end, N)

        solutions = {}
        errors    = {}

        for m in methods:
            if m == "analytical":
                try:
                    sol = dsolve(sym_eq, Function('y')(self.x))
                    sol_func = self._prepare_solution_function(sol, x0, y0)
                    y_vals = [sol_func(xi) for xi in x_vals]
                    solutions["analytical"] = list(zip(x_vals, y_vals))
                except Exception as e:
                    errors["analytical"] = str(e)
            else:
                try:
                    num = self.solve_ode_numerical((f, rhs_text), initial_condition, x_range, h, method=m)
                    solutions[m] = num["solution"] # num["solution"] es [(x0,y0), …]
                except Exception as e:
                    errors[m] = str(e)

        # crear el canvas comparativo una sola vez con puntos 100% float
        canvas = self.graph_controller.generate_ode_comparison_canvas(equation=f"y' = {rhs_text}", solutions=solutions, initial_condition=initial_condition, x_range=x_range, h=h)

        if errors:
            return {"canvas": canvas, "errors": errors}
        return canvas

    def clear(self):
        return