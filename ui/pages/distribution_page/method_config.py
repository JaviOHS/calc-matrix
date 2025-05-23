METHOD_CONFIG = {
    "mersenne": {
        "display_name": "Mersenne Twister",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:", "type": "int", "default": 5, "min": 1, "max": 1000},
            {"name": "seed",  "label": "🌱 Semilla:",   "type": "int", "default": 12345, "min": 1, "max": 999999}
        ]
    },
    "xorshift": {
        "display_name": "Xorshift",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:", "type": "int", "default": 5, "min": 1, "max": 1000},
            {"name": "seed",  "label": "🌱 Semilla:",   "type": "int", "default": 12345, "min": 1, "max": 999999}
        ]
    },
    "congruencial": {
        "display_name": "Congruencia Lineal",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:",           "type": "int", "default": 5,         "min": 1,       "max": 1000},
            {"name": "seed",  "label": "🌱 Semilla:",             "type": "int", "default": 12345,     "min": 1,       "max": 999999},
            {"name": "a",     "label": "🔢 Multiplicador (a):",  "type": "int", "default": 1664525,   "min": 1,       "max": 999999999},
            {"name": "c",     "label": "➕ Incremento (c):",     "type": "int", "default": 1013904223,"min": 0,       "max": 999999999}
        ]
    },
    "congruencial_multiplicativo": {
        "display_name": "Congruencial Multiplicativo",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:",          "type": "int", "default": 5,        "min": 1,       "max": 1000},
            {"name": "seed",  "label": "🌱 Semilla:",            "type": "int", "default": 12345,    "min": 1,       "max": 999999},
            {"name": "a",     "label": "🔢 Multiplicador (a):", "type": "int", "default": 1664525,  "min": 1,       "max": 999999999}
        ]
    },
    "lfsr": {
        "display_name": "LFSR",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:", "type": "int", "default": 5,     "min": 1,  "max": 1000},
            {"name": "seed",  "label": "🌱 Semilla:",   "type": "int", "default": 12345, "min": 1,  "max": 999999},
            {"name": "taps",  "label": "🔧 Taps:",      "type": "int", "default": 3,     "min": 1,  "max": 32}
        ]
    },
    "productos_medios": {
        "display_name": "Productos Medios",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:", "type": "int", "default": 5,    "min": 1,    "max": 1000},
            {"name": "seed",  "label": "🌱 Semilla:",   "type": "int", "default": 1234, "min": 1000, "max": 9999}
        ]
    },
    "productos_cuadraticos": {
        "display_name": "Productos Cuadráticos",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:", "type": "int", "default": 5,    "min": 1,    "max": 1000},
            {"name": "seed",  "label": "🌱 Semilla:",   "type": "int", "default": 1234, "min": 1000, "max": 9999}
        ]
    },
    "ruido_fisico": {
        "display_name": "Ruido Físico",
        "fields": [
            {"name": "count", "label": "🔢 Cantidad:", "type": "int", "default": 5, "min": 1, "max": 1000}
        ]
    }
}

MONTE_CARLO_CONFIG = {
    "fields": [
        {"name": "lower_limit", "label": "🔢 Límites: x =", "type": "float", "default": 0, "min": -1000, "max": 1000, "width": 60},
        {"name": "upper_limit", "label": "→", "type": "float", "default": 1, "min": -1000, "max": 1000, "width": 60},
        {"name": "points", "label": "📊 Número de puntos:", "type": "int", "default": 10000, "min": 100, "max": 1000000, "step": 1000, "width": 100},
        {"name": "seed", "label": "🔑 Semilla:", "type": "int", "default": 42, "min": 0, "max": 999999, "width": 100}
    ]
}

MARKOV_CONFIG = {
    "population_params": [
        {"name": "population", "label": "👥 Población total:", "type": "int", "default": 45000, "min": 10, "max": 1000000, "step": 100, "width": 100},
        {"name": "initial_infected", "label": "🦠 Infectados iniciales:", "type": "int", "default": 20, "min": 1, "max": 1000, "width": 80},
        {"name": "initial_recovered", "label": "💪 Recuperados iniciales:", "type": "int", "default": 0, "min": 0, "max": 100, "width": 80}
    ],
    "rate_params": [
        {"name": "beta", "label": "🔄 Beta (tasa de infección):", "type": "float", "default": 0.45, "min": 0.0, "max": 1.0, "step": 0.001, "decimals": 3, "width": 80},
        {"name": "gamma", "label": "💊 Gamma (tasa de recuperación):", "type": "float", "default": 0.25, "min": 0.0, "max": 1.0, "step": 0.05, "width": 80}
    ],
    "simulation_params": [
        {"name": "days", "label": "📅 Días a simular:", "type": "int", "default": 30, "min": 1, "max": 365, "width": 80},
        {"name": "dt", "label": "⏱️ Intervalo de tiempo (dt):", "type": "float", "default": 0.1, "min": 0.01, "max": 1.0, "width": 80},
        {"name": "seed", "label": "🔑 Semilla:", "type": "int", "default": 42, "min": 0, "max": 999999, "width": 80}
    ]
}

TRANSFORM_CONFIG = {
    "normal": {
        "display_name": "Normal (Box-Muller)",
        "fields": []
    },
    "exponential": {
        "display_name": "Exponencial",
        "fields": [
            {"name": "lambda", "label": "λ (lambda):", "type": "float", "default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1, "decimals": 2, "width": 80}
        ]
    },
    "poisson": {
        "display_name": "Poisson",
        "fields": [
            {"name": "lambda", "label": "λ (lambda):", "type": "float", "default": 1.0, "min": 0.1, "max": 20.0, "step": 0.1, "decimals": 2, "width": 80}
        ]
    },
    "binomial": {
        "display_name": "Binomial",
        "fields": [
            {"name": "n", "label": "n (intentos):", "type": "int", "default": 10, "min": 1, "max": 1000, "step": 1, "width": 80},
            {"name": "p", "label": "p (probabilidad):", "type": "float", "default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "decimals": 2, "width": 80}
        ]
    },
    "gamma": {
        "display_name": "Gamma",
        "fields": [
            {"name": "alpha", "label": "α (forma):", "type": "float", "default": 1.0, "min": 1.0, "max": 10.0, "step": 0.1, "decimals": 2, "width": 80},
            {"name": "beta", "label": "β (escala):", "type": "float", "default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1, "decimals": 2, "width": 80}
        ]
    },
    "beta": {
        "display_name": "Beta",
        "fields": [
            {"name": "alpha", "label": "α (forma 1):", "type": "float", "default": 2.0, "min": 0.1, "max": 10.0, "step": 0.1, "decimals": 2, "width": 80},
            {"name": "beta", "label": "β (forma 2):", "type": "float", "default": 2.0, "min": 0.1, "max": 10.0, "step": 0.1, "decimals": 2, "width": 80}
        ]
    }
}