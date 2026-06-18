import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Retail Shift Optimizer", layout="wide", page_icon="👥")

st.title("👥 Retail Shift & Performance Optimizer")
st.markdown("Motor analítico Zero-Disk para el dimensionamiento de plantillas, auditoría de rendimiento por vendedor y optimización del Coste Laboral sobre Ventas.")

# ==========================================
# 1. ARQUITECTURA HÍBRIDA & SIMULADOR WHAT-IF
# ==========================================
st.sidebar.header("⚙️ Entorno de Trabajo")
modo = st.sidebar.radio(
    "Selecciona el modo de procesamiento:",
    ("📊 Modo Demo (Portfolio)", "🔒 Auditoría Zero-Disk (Sube tu CSV)")
)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Simulador What-If")
st.sidebar.markdown("Ajusta las variables para visualizar el impacto en el P&L en tiempo real.")

sim_aov = st.sidebar.slider(
    "Mejora Ticket Medio (€)", 
    min_value=0.0, max_value=15.0, value=0.0, step=0.5,
    help="Simula el impacto financiero derivado de una mejora en las ratios de venta cruzada de la plantilla."
)

sim_personal = st.sidebar.slider(
    "Ajuste de Plantilla (%)", 
    min_value=-30, max_value=30, value=0, step=5,
    help="Simula el impacto en costes operativos derivado de la reducción o ampliación de la cobertura horaria."
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Arquitectura Zero-Disk:**\nLos datos comerciales se procesan exclusivamente en la memoria RAM y se autodestruyen al finalizar la sesión.")

# ==========================================
# 2. MOTOR DE CÁLCULO Y DASHBOARD
# ==========================================
def renderizar_dashboard(df):
    
    # ------------------------------------------
    # APLICACIÓN DEL SIMULADOR WHAT-IF
    # ------------------------------------------
    df['Ventas'] = df['Ventas'] + (df['Transacciones'] * sim_aov)
    df['Horas_Trabajadas'] = df['Horas_Trabajadas'] * (1 + (sim_personal / 100))
    
    # ------------------------------------------
    # CÁLCULO DE KPIs
    # ------------------------------------------
    df['Ticket_Medio'] = df['Ventas'] / df['Transacciones'].replace(0, 1)
    df['UPT'] = df['Unidades'] / df['Transacciones'].replace(0, 1)
    df['VPH'] = df['Ventas'] / df['Horas_Trabajadas'].replace(0, 1)
    df['Coste_Laboral_Total'] = df['Horas_Trabajadas'] * df['Coste_Hora']
    
    ventas_totales = df['Ventas'].sum()
    aov_global = ventas_totales / df['Transacciones'].sum()
    upt_global = df['Unidades'].sum() / df['Transacciones'].sum()
    vph_global = ventas_totales / df['Horas_Trabajadas'].sum()
    coste_laboral_pct = (df['Coste_Laboral_Total'].sum() / ventas_totales) * 100
    conversion_global = (df['Transacciones'].sum() / df['Trafico_Tienda'].sum()) * 100

    st.markdown("---")
    
    # ==========================================
    # BOTÓN POP-UP (RESUMEN EJECUTIVO Y DATA PIPELINE)
    # ==========================================
    with st.popover("💡 Ver Resumen Ejecutivo y Metodología de Ingesta de Datos", use_container_width=True):
        st.markdown("### 🎯 Visión Macroestratégica: Interpretación del Conjunto de Métricas")
        st.markdown("El presente cuadro de mando cuantifica el punto de equilibrio exacto entre la eficiencia operativa de costes y la excelencia en el servicio comercial. Constituye una herramienta de auditoría directiva diseñada para evaluar los siguientes vectores:")
        
        st.markdown("""
        * **Rentabilidad Operativa del Turno:** Trasciende el volumen bruto de ingresos para ponderar el impacto del Coste Laboral (OPEX) sobre las ventas. Un sobredimensionamiento de la plantilla durante valles de demanda erosiona directamente el margen de contribución.
        * **Coste de Oportunidad (Tasa de Conversión vs. Tráfico Peatonal):** Una alta densidad de tráfico correlacionada con una baja conversión indica una fuga sistémica de capital. El modelo segmenta el origen de esta pérdida: ineficiencia en las competencias de venta del personal (auditable en la Matriz de Rendimiento) o saturación operativa por falta de cobertura (auditable en la Curva de Eficiencia).
        * **Calidad Transaccional (AOV y UPT):** Evalúa el grado de asesoramiento comercial. Determina si el equipo opera bajo un enfoque de 'venta cruzada' (incrementando la profundidad de la cesta) o si, debido a la presión operativa, el servicio se degrada a un mero modelo de despacho transaccional.
        
        > **Conclusión Ejecutiva:** El sistema diagnostica con precisión matemática la pérdida de rentabilidad derivada de una sobrecapacidad laboral (exceso de costes operativos) o la pérdida de volumen de negocio por infracobertura (insuficiencia de personal en sala).
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Requisitos de Ingesta de Datos (Data Pipeline)")
        st.markdown("""
        La arquitectura del modelo abstrae al usuario operativo de cualquier cálculo de KPIs. El sistema requiere únicamente la exportación de un conjunto de datos brutos (Raw Data) procedente de los sistemas de planificación de recursos empresariales (ERP) o Terminales de Punto de Venta (TPV). 
        
        Para la correcta ejecución del motor algorítmico, el archivo (formato CSV) debe estructurar la información en las siguientes 8 variables absolutas:
        
        1.  **Fecha / Turno:** Marca temporal de la transacción.
        2.  **Vendedor_ID:** Identificador único del empleado asociado a la transacción.
        3.  **Ventas Brutas:** Volumen económico generado (EUR).
        4.  **Transacciones:** Volumen absoluto de tickets emitidos.
        5.  **Unidades:** Volumen de artículos físicos procesados.
        6.  **Horas Trabajadas:** Carga lectiva del turno por empleado.
        7.  **Tráfico Tienda:** Volumen peatonal registrado por la sensórica de acceso.
        8.  **Coste Hora:** Valor salarial unitario de la fuerza laboral.
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # KPIs GLOBALES
    # ==========================================
    st.markdown("### 📈 Salud Financiera del Turno")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ingreso Total", f"{ventas_totales:,.0f} €", help="Volumen total de ventas brutas.")
    col2.metric("Coste Laboral s/ Ventas", f"{coste_laboral_pct:.1f} %", 
                delta="Riesgo si > 15%" if coste_laboral_pct > 15 else "Óptimo", delta_color="inverse")
    col3.metric("Tasa de Conversión", f"{conversion_global:.1f} %")
    col4.metric("Productividad (VPH)", f"{vph_global:.1f} €/h")

    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Ticket Medio (AOV)", f"{aov_global:.2f} €")
    col6.metric("Unidades por Ticket (UPT)", f"{upt_global:.2f}")
    col7.metric("Tráfico Total (Entradas)", f"{df['Trafico_Tienda'].sum():,.0f}")
    col8.metric("Transacciones (Tickets)", f"{df['Transacciones'].sum():,.0f}")

    st.markdown("---")

    # ==========================================
    # MAPA DE CALOR HORARIO
    # ==========================================
    st.subheader("🔥 Mapa de Calor: Saturación de Tienda (Zonas de Peligro)")
    st.markdown("Identifica las horas críticas donde el ratio **Clientes por Empleado** se dispara, provocando fugas de ventas y caídas de conversión.")
    
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Hora'] = df['Fecha'].dt.hour
    df['Dia_Semana'] = df['Fecha'].dt.day_name().map({
        'Monday': '1-Lunes', 'Tuesday': '2-Martes', 'Wednesday': '3-Miércoles', 
        'Thursday': '4-Jueves', 'Friday': '5-Viernes', 'Saturday': '6-Sábado', 'Sunday': '7-Domingo'
    })
    
    df_heat = df.groupby(['Dia_Semana', 'Hora']).agg({'Trafico_Tienda': 'sum', 'Horas_Trabajadas': 'sum'}).reset_index()
    df_heat['Carga_Trabajo'] = df_heat['Trafico_Tienda'] / df_heat['Horas_Trabajadas'].replace(0, 1)
    
    heatmap_data = df_heat.pivot_table(index='Hora', columns='Dia_Semana', values='Carga_Trabajo', aggfunc='mean')
    
    fig_heat = px.imshow(
        heatmap_data, 
        labels=dict(x="Día de la Semana", y="Franja Horaria", color="Clientes por Empleado"),
        color_continuous_scale="Reds", aspect="auto"
    )
    fig_heat.update_layout(height=400, yaxis=dict(tickmode='linear', dtick=1))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # CURVA DE EFICIENCIA (TRÁFICO VS COSTE)
    # ==========================================
    st.subheader("⚖️ Curva de Eficiencia: Tráfico vs Coste Laboral")
    
    df_temporal = df.groupby(df['Fecha'].dt.date).agg({'Trafico_Tienda': 'sum', 'Coste_Laboral_Total': 'sum'}).reset_index()
    
    fig_eficiencia = go.Figure()
    fig_eficiencia.add_trace(go.Bar(x=df_temporal['Fecha'], y=df_temporal['Trafico_Tienda'], name='Tráfico (Clientes)', marker_color='#3498db'))
    fig_eficiencia.add_trace(go.Scatter(x=df_temporal['Fecha'], y=df_temporal['Coste_Laboral_Total'], name='Coste Laboral (€)', yaxis='y2', mode='lines+markers', line=dict(color='#e74c3c', width=3)))
    
    fig_eficiencia.update_layout(
        yaxis=dict(title='Tráfico Peatonal'),
        yaxis2=dict(title='Coste Laboral (€)', overlaying='y', side='right'),
        height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_eficiencia, use_container_width=True)

    with st.popover("📊 Ver Análisis Técnico e Interpretación Operativa de la Curva", use_container_width=True):
        st.markdown("### 1. Fundamento Técnico de la Representación Gráfica")
        st.markdown("""
        La alineación del vector de coste lineal respecto al histograma de tráfico responde a criterios estandarizados de geometría analítica en librerías de visualización bidimensional. 
        
        * **El eje de abscisas (X)** opera con variables discretas temporales de carácter cronológico.
        * **Componente de Barras (Tráfico):** Su centroide o 'centro de gravedad' exacto coincide con la marca temporal indexada.
        * **Componente de Línea (Coste):** Las funciones lineales se estructuran como una sucesión de nodos coordenados conectados. Por consiguiente, el punto inicial se ancla exactamente en el centro matemático del periodo, garantizando la máxima precisión al correlacionar variables macroeconómicas sobre un mismo eje temporal.
        """)
        
        st.markdown("---")
        st.markdown("### 2. Interpretación Operativa y Análisis de Elasticidad de Costes")
        st.markdown("""
        El objetivo de este modelo radica en la evaluación de la **elasticidad del gasto operativo (OPEX)** respecto a la volatilidad de la demanda en el punto de venta.
        
        * **Fase de Mínimos Estructurales (Valle temporal):** Se constata un escenario de contracción de tráfico correlacionado con una optimización estricta del coste laboral, indicativo de un dimensionamiento correcto para jornadas de baja afluencia estructural.
        * **Fase de Máxima Eficiencia Operativa (Zonas de pico):** Se observa un incremento sostenido en el flujo peatonal frente a una curva de coste laboral inelástica. **Insight analítico:** La estructura operativa absorbe una alta tasa de crecimiento de demanda sin incurrir en costes marginales, traduciéndose en una maximización de la productividad por hora (VPH).
        * **Fase de Adaptación y Flexibilidad:** Ante una desaceleración marginal del tráfico, se registra un ajuste descendente proporcional en la curva de coste, validando la capacidad de control presupuestario.
        
        > ⚠️ **Detección de Anomalías Críticas:** Una divergencia inversa (contracción de tráfico frente a picos de coste laboral) emitiría una alerta de ineficiencia por sobrecapacidad, señalando una pérdida directa de margen operativo.
        """)

    st.markdown("---")

    # ==========================================
    # MATRIZ DE RENDIMIENTO (SOLAPAMIENTO CORREGIDO)
    # ==========================================
    st.subheader("🎯 Auditoría de Rendimiento Individual (Matriz Asesor vs Despachador)")
    st.markdown("Identifica carencias formativas cruzando la capacidad de venta cruzada (UPT) con el Ticket Medio (AOV).")
    
    df_vendedores = df.groupby('Vendedor_ID').agg({
        'Ticket_Medio': 'mean', 'UPT': 'mean', 'Ventas': 'sum', 'Transacciones': 'sum'
    }).reset_index()

    fig_matrix = px.scatter(
        df_vendedores, x='UPT', y='Ticket_Medio', size='Ventas', color='Vendedor_ID',
        hover_name='Vendedor_ID', text='Vendedor_ID', size_max=40,
        labels={'UPT': 'Venta Cruzada (UPT)', 'Ticket_Medio': 'Ticket Medio (€)'}
    )
    
    fig_matrix.add_hline(y=aov_global, line_dash="dash", annotation_text="Media AOV", annotation_position="bottom right")
    fig_matrix.add_vline(x=upt_global, line_dash="dash", annotation_text="Media UPT", annotation_position="top left")
    
    fig_matrix.update_traces(textposition='top center', textfont=dict(color='#ffffff'))
    
    fig_matrix.add_annotation(
        x=df_vendedores['UPT'].max(), y=df_vendedores['Ticket_Medio'].max() + 5, 
        text="🌟 ASESORES TOP", showarrow=False, opacity=0.3, font=dict(size=20)
    )
    fig_matrix.add_annotation(
        x=df_vendedores['UPT'].min(), y=df_vendedores['Ticket_Medio'].min() - 5, 
        text="📦 DESPACHADORES", showarrow=False, opacity=0.3, font=dict(size=20)
    )
    
    fig_matrix.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_matrix, use_container_width=True)

    # ==========================================
    # FOOTER CORPORATIVO (FIRMA)
    # ==========================================
    st.markdown("""
        <hr style="margin-top: 4rem; margin-bottom: 2rem; border: 0; border-top: 1px solid #333;">
        <div style='text-align: center; color: #a3a3a3; font-family: "Cardo", serif; padding-bottom: 2rem;'>
            <span style='font-size: 1.1rem; letter-spacing: 1px;'>Desarrollado por <strong>Jose Luis Asenjo</strong></span> <br> 
            <span style='font-size: 0.95rem; font-style: italic; color: #d4af37;'>Retail & Software Engineer</span>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. CONTROLADOR DE FLUJO (DEMO VS REAL)
# ==========================================
if modo == "📊 Modo Demo (Portfolio)":
    st.info("💡 **Modo Demostración:** El dataset simula una semana de tráfico horario (10:00 a 21:00) con 4 vendedores de distintos perfiles.")
    
    np.random.seed(42)
    fechas_horas = pd.date_range(start="2026-06-01 10:00", end="2026-06-07 21:00", freq='h')
    
    datos = []
    for dt in fechas_horas:
        if 18 <= dt.hour <= 20:
            trafico_hora = np.random.randint(60, 150)
        else:
            trafico_hora = np.random.randint(10, 50)
            
        # VENDEDOR 1 (Junior)
        t1 = np.random.randint(3, 7)
        u1 = t1 * np.random.uniform(1.0, 1.2)
        v1 = u1 * np.random.uniform(10, 15)
        datos.append([dt, 'Vendedor 1 (Junior)', v1, t1, u1, 1, trafico_hora/4, 12.50])
        
        # VENDEDOR 2 (Senior)
        t2 = np.random.randint(1, 4)
        u2 = t2 * np.random.uniform(2.5, 3.0)
        v2 = u2 * np.random.uniform(35, 45)
        datos.append([dt, 'Vendedor 2 (Senior)', v2, t2, u2, 1, trafico_hora/4, 12.50])

        # VENDEDOR 3 (Cajero)
        t3 = np.random.randint(4, 9)
        u3 = t3 * np.random.uniform(1.2, 1.4)
        v3 = u3 * np.random.uniform(15, 20)
        datos.append([dt, 'Vendedor 3 (Cajero)', v3, t3, u3, 1, trafico_hora/4, 12.50])

        # VENDEDOR 4 (Asesor)
        t4 = np.random.randint(2, 5)
        u4 = t4 * np.random.uniform(1.8, 2.2)
        v4 = u4 * np.random.uniform(25, 30)
        datos.append([dt, 'Vendedor 4 (Asesor)', v4, t4, u4, 1, trafico_hora/4, 12.50])
            
    df_demo = pd.DataFrame(datos, columns=['Fecha', 'Vendedor_ID', 'Ventas', 'Transacciones', 'Unidades', 'Horas_Trabajadas', 'Trafico_Tienda', 'Coste_Hora'])
    renderizar_dashboard(df_demo)

else:
    st.warning("🔒 **Modo Zero-Disk Activo:** El procesamiento no dejará huella en disco. Sube el CSV de tu TPV.")
    st.markdown("**Estructura requerida del CSV:** `Fecha` (ej: 2026-06-01 14:00), `Vendedor_ID`, `Ventas`, `Transacciones`, `Unidades`, `Horas_Trabajadas`, `Trafico_Tienda`, `Coste_Hora`")
    
    archivo_subido = st.file_uploader("Arrastra tu archivo aquí", type=["csv"])
    
    if archivo_subido is not None:
        try:
            df_real = pd.read_csv(archivo_subido)
            columnas_requeridas = ['Fecha', 'Vendedor_ID', 'Ventas', 'Transacciones', 'Unidades', 'Horas_Trabajadas', 'Trafico_Tienda', 'Coste_Hora']
            if all(col in df_real.columns for col in columnas_requeridas):
                st.success("Dataset validado y procesado en RAM con éxito.")
                renderizar_dashboard(df_real)
            else:
                st.error(f"Faltan columnas. El archivo debe contener exactamente: {', '.join(columnas_requeridas)}")
        except Exception as e:
            st.error(f"Error al leer el archivo. Detalle: {e}")
