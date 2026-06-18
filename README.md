# 👥 Retail Shift & Performance Optimizer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Data_Viz-3F4F75?style=for-the-badge&logo=plotly)

Motor analítico predictivo para el dimensionamiento de plantillas y la auditoría de rendimiento comercial en entornos Retail. Desarrollado con una arquitectura **Zero-Disk**, el sistema cuantifica el punto de equilibrio exacto entre la eficiencia de costes laborales (OPEX) y la calidad del servicio al cliente.

---

## 🎯 Visión Macroestratégica

El presente ecosistema analítico trasciende la simple visualización de ingresos brutos para diagnosticar y modelar la **elasticidad del gasto operativo**. La herramienta permite a Directores de Operaciones y Store Managers detectar con precisión matemática:
* **Fugas de rentabilidad:** Derivadas de una sobrecapacidad laboral (exceso de plantilla en horas valle).
* **Costes de Oportunidad:** Pérdida de conversiones o caídas en el Ticket Medio debido a infracobertura operativa en picos de demanda.

---

## 🛡️ Arquitectura Zero-Disk (In-Memory Processing)

El diseño de la aplicación responde a los más altos estándares de privacidad corporativa. La herramienta opera bajo un modelo **Stateless / Zero-Disk**:
1. El usuario inyecta el conjunto de datos (Raw Data) del terminal TPV.
2. El procesamiento matricial y la agregación de KPIs se ejecutan estrictamente en la memoria volátil (RAM) del servidor.
3. No se realiza escritura en bases de datos externas ni discos físicos.
4. Al cerrar la sesión, la estructura de datos se autodestruye mediante el recolector de basura (*Garbage Collection*), garantizando el cumplimiento íntegro del marco normativo de protección de datos (RGPD) e inteligencia comercial corporativa.

---

## ⚙️ Capacidades Analíticas y Módulos Core

### 1. Simulador Dinámico What-If
Módulo interactivo que permite recalcular en tiempo real el P&L (Cuenta de Resultados) del turno modificando variables estratégicas:
* Impacto porcentual de ampliación/reducción de cobertura laboral.
* Estimación de ingresos derivados de programas de formación en *Cross-Selling* (Venta Cruzada).

### 2. Curva de Eficiencia (Tráfico vs. Coste Laboral)
Representación geométrica que evalúa la capacidad de absorción de la demanda. Identifica divergencias anómalas mediante la superposición del volumen peatonal (histograma) frente al vector inelástico del coste laboral por horas.

### 3. Matriz de Auditoría Individual (Performance Matrix)
Modelo de clasificación geométrica (Scatter Plot) para la fuerza de ventas. Clasifica automáticamente al personal cruzando la profundidad de la cesta (UPT) con el Ticket Medio (AOV), discriminando perfiles estratégicos (*Asesores Premium*) frente a perfiles puramente transaccionales (*Despachadores/Cajeros*).

### 4. Heatmap de Saturación Operativa
Identificación algorítmica de puntos críticos de colapso. El mapa de calor dimensiona la carga de trabajo real calculando la ratio de **Clientes concurrentes por Empleado activo** según la franja horaria y el día de la semana.

---

## 📊 Requisitos de Ingesta (Data Pipeline)

El modelo está diseñado para abstraer al equipo de tienda de procesos de cálculo complejos. Solo requiere la importación de un archivo `.csv` plano con la siguiente estructura de 8 vectores:

| Variable | Descripción Técnica |
| :--- | :--- |
| `Fecha` | Marca temporal (*Timestamp*) en formato `YYYY-MM-DD HH:MM`. |
| `Vendedor_ID` | Identificador único alfanumérico del empleado. |
| `Ventas` | Volumen económico bruto generado (EUR). |
| `Transacciones` | Volumen absoluto de tickets o cobros emitidos. |
| `Unidades` | Sumatoria de artículos físicos consolidados. |
| `Horas_Trabajadas` | Carga lectiva horaria (int/float) del turno asociado. |
| `Trafico_Tienda` | Volumen peatonal registrado por sensórica de acceso. |
| `Coste_Hora` | Valor salarial unitario de la fuerza laboral operativa. |

---

## 🛠️ Instalación y Despliegue Local

Para ejecutar este entorno analítico en una máquina local o servidor aislado:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TuUsuario/retail-shift-optimizer.git](https://github.com/TuUsuario/retail-shift-optimizer.git)
   cd retail-shift-optimizer

Instalar dependencias necesarias:
Se recomienda el uso de un entorno virtual (venv o conda).

pip install -r requirements.txt

Lanzar el servidor de Streamlit:

streamlit run app.py

Autor
Jose Luis Asenjo Retail & Software Engineer Desarrollo de modelos de inteligencia comercial y ecosistemas asíncronos en Python centrados en el rendimiento, la privacidad y la analítica avanzada.
