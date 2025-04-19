from model.polynomial_model import Polynomial

class PolynomialManager:
    def __init__(self):
        self.polynomials = []
    
    def add_polynomial(self, polynomial):
        if not isinstance(polynomial, Polynomial):
            raise TypeError("Se intentó agregar algo que no es un polinomio.")
        self.polynomials.append(polynomial)

    def divide(self):
        if len(self.polynomials) != 2:
            raise ValueError("Se necesitan exactamente dos polinomios para dividir.")
        dividend = self.polynomials[0]
        divisor = self.polynomials[1]
        return dividend.divide(divisor)  # Para división de 2 polinomios 
    
    def validate_polynomials(self):
        if not self.polynomials:
            error_message = "No hay polinomios disponibles para la operación."
            raise ValueError(error_message)
        
    def evaluate_all(self, x):
        self.validate_polynomials()
        return [(f"P{i+1}", poly.evaluate(x)) for i, poly in enumerate(self.polynomials)]
    
    def compute_derivatives(self):
        self.validate_polynomials()
        return [poly.derivative() for poly in self.polynomials]
    
    def compute_integrals(self, constant=0):
        self.validate_polynomials()
        return [poly.integral(constant) for poly in self.polynomials]
