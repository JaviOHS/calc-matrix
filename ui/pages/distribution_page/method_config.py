METHOD_CONFIG = {
    "mersenne": {
        "display_name": "Mersenne Twister",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000},
            {"name": "seed", "label": "🌱 Semilla:", "default": 12345, "min": 1, "max": 999999}
        ]
    },
    "xorshift": {
        "display_name": "Xorshift",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000},
            {"name": "seed", "label": "🌱 Semilla:", "default": 12345, "min": 1, "max": 999999}
        ]
    },
    "congruencial": {
        "display_name": "Congruencia Lineal",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000},
            {"name": "seed", "label": "🌱 Semilla:", "default": 12345, "min": 1, "max": 999999},
            {"name": "a", "label": "🔢 Multiplicador (a):", "default": 1664525, "min": 1, "max": 999999999},
            {"name": "c", "label": "➕ Incremento (c):", "default": 1013904223, "min": 0, "max": 999999999}
        ]
    },
    "congruencial_multiplicativo": {
        "display_name": "Congruencial Multiplicativo",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000},
            {"name": "seed", "label": "🌱 Semilla:", "default": 12345, "min": 1, "max": 999999},
            {"name": "a", "label": "🔢 Multiplicador (a):", "default": 1664525, "min": 1, "max": 999999999}
        ]
    },
    "lfsr": {
        "display_name": "LFSR",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000},
            {"name": "seed", "label": "🌱 Semilla:", "default": 12345, "min": 1, "max": 999999},
            {"name": "taps", "label": "🔧 Taps:", "default": 3, "min": 1, "max": 32}
        ]
    },
    "productos_medios": {
        "display_name": "Productos Medios",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000},
            {"name": "seed", "label": "🌱 Semilla:", "default": 1234, "min": 1000, "max": 9999}
        ]
    },
    "productos_cuadraticos": {
        "display_name": "Productos Cuadráticos",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000},
            {"name": "seed", "label": "🌱 Semilla:", "default": 1234, "min": 1000, "max": 9999}
        ]
    },
    "ruido_fisico": {
        "display_name": "Ruido Físico",
        "fields": [
            {"name": "count", "label": "📌 Cantidad:", "default": 5, "min": 1, "max": 1000}
        ]
    }
}