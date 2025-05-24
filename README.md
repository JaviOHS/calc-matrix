<div align="center">

  <img src="assets/images/intro/about.png" alt="CalcMatrix Logo" width="160" style="margin-top: 20px;"/>

  <h1>🧮 CalcMatrix</h1>

  <p><strong>Una calculadora visual y potente para álgebra lineal, polinomios, cálculo y gráficos.</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.x-blue" alt="Python">
    <img src="https://img.shields.io/badge/PySide/PyQt-6-brightgreen" alt="PySide/PyQt">
    <img src="https://img.shields.io/badge/NumPy-%5E1.26-orange" alt="NumPy">
    <img src="https://img.shields.io/badge/SymPy-%5E1.12-yellow" alt="SymPy">
    <img src="https://img.shields.io/badge/Matplotlib-%5E3.8-red" alt="Matplotlib">
  </p>

</div>

---

## ✨ Características Principales

Desarrollada en **Python** con interfaz gráfica **PySide/PyQt**. Esta app integra lo mejor de:
- 🧮 **NumPy** para operaciones numéricas.
- 🧠 **SymPy** para cálculo simbólico.
- 📊 **Matplotlib** para gráficos 2D y 3D.

---

## 🧩 Módulos Disponibles

### 🔷 Matrices
- ➕ Suma, ➖ Resta, ✖️ Cuadrática
- 🔄 Inversa y Determinante (hasta 10x10)
- 🧩 Resolución de sistemas lineales `Ax = b`

### 📊 Polinomios
- 🧠 Operaciones combinadas con paréntesis
- ❌ Raíces
- 📉 Derivada | 📈 Integral
- 🧮 Evaluación de `x`

### 📐 Vectores
- ➕➖✖️➗ Operaciones básicas (misma dimensión)
- 📏 Magnitud
- 🔘 Producto Punto
- 🔁 Producto Cruzado

### 📈 Gráficos
- 🟦 2D: función + intervalo X  
- 🟥 3D: función + rangos X/Y

### 🔬 Cálculo Simbólico
- 📉 Derivadas simbólicas
- 📈 Integrales definidas
- 🔄 Ecuaciones diferenciales ordinarias

---

## 🚀 Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/JaviOHS/calc-matrix.git

# 2. Entra al proyecto
cd calc-matrix

# 3. Crea y activa un entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 4. Instala las dependencias
pip install -r requirements.txt

# 5. Ejecuta la app
python main.py
```

---

## 📦 Dependencias Principales

- `PySide6`
- `numpy >= 1.26`
- `sympy >= 1.12`
- `matplotlib >= 3.8`

---

## 🧪 Crear Ejecutable `.exe`

Puedes empaquetar la aplicación como un ejecutable para su distribución. Sigue estos pasos:

```bash
# 1. Activa el entorno virtual
# (debe tener todas las dependencias ya instaladas)
.venv\Scripts\activate

# 2. Instala PyInstaller dentro del entorno virtual
pip install pyinstaller

# 3. Ejecuta el empaquetado con el archivo .spec
pyinstaller CalcMatrix.spec --clean
```

Esto generará una carpeta `dist/CalcMatrix v1.2/` que contiene el ejecutable `CalcMatrix v1.2.exe` con todos los recursos y dependencias incluidos (no requiere instalación de Python en el equipo destino).

---

## 🛠️ Crear Instalador con Inno Setup

Puedes generar un instalador `.exe` para distribuir la aplicación utilizando **Inno Setup**. Sigue estos pasos:

### 1. Descarga e instala Inno Setup
- Descarga Inno Setup desde su [sitio oficial](https://jrsoftware.org/isinfo.php).
- Instálalo en tu equipo.

### 2. Configura el archivo de script
- Asegúrate de que el archivo `CalcMatrix.iss` esté correctamente configurado en la raíz del proyecto. Este archivo ya está incluido en el repositorio y contiene la configuración necesaria para empaquetar la aplicación.

### 3. Genera el instalador
- Abre Inno Setup y carga el archivo `CalcMatrix.iss`.
- Haz clic en **Compile** (o presiona `F9`) para generar el instalador.

Esto generará un archivo ejecutable instalador en la carpeta `installer/` con el nombre `CalcMatrixInstaller.exe`.

### 4. Distribuye el instalador
El archivo generado incluye todos los recursos necesarios para instalar y ejecutar la aplicación en cualquier equipo con Windows.

```plaintext
installer/
└── CalcMatrixInstaller.exe
```

---

## 🛠️ Estado del Proyecto

🔹 Versión 1.2 — en constante desarrollo.  
🔹 Mejoras visuales y de rendimiento en camino.  

---

## 🌐 Repositorio

🔗 [github.com/JaviOHS/calc-matrix](https://github.com/JaviOHS/calc-matrix)

---