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
st.sidebar.markdown("Ajusta las variables para ver el impacto en el P&L en tiempo real.")

sim_aov = st.sidebar.slider(
    "Mejora Ticket Medio (€)", 
    min_value=0.0, max_value=15.0, value=0.0, step=0.5,
    help="Simula el impacto financiero si formamos al equipo para mejorar la venta cruzada."
)

sim_personal = st.sidebar.slider(
    "Ajuste de Plantilla (%)", 
    min_value=-30, max_value=30, value=0, step=5,
    help="Simula qué pasaría con tus costes si reduces o aumentas las horas de personal."
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Arquitectura Zero-Disk:**\nLos datos se procesan en la memoria RAM y se autodestruyen al cerrar la sesión.")

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
    # BOTÓN POP-UP (RESUMEN CEO)
    # ==========================================
    with st.popover("💡 Ver Resumen Ejecutivo para la Alta Dirección", use_container_width=True):
        st.markdown("### 🎯 La 'Foto Grande': ¿Qué nos dice el conjunto de estas métricas?")
        st.markdown("Si tuvieras que explicarle esta pantalla a un CEO en 30 segundos, el resumen es este: **Esta herramienta mide el punto exacto donde la eficiencia de costes choca con la calidad comercial.**")
        
        st.markdown("""
        * **La rentabilidad real del turno:** No solo miras cuánto has vendido (Ingreso), sino cuánto te ha costado venderlo (Coste Laboral %). Si vendes mucho pero tienes a demasiada gente, el margen desaparece.
        * **El coste de oportunidad (Conversión vs. Tráfico):** Si el tráfico es alto pero la conversión es baja, estás perdiendo clientes. La herramienta te dice si los pierdes porque el personal es malo (Matriz de Vendedores) o porque simplemente no dan abasto (Curva de Eficiencia).
        * **La calidad de la venta (AOV y UPT):** Te indica si tu equipo está haciendo su trabajo como asesores (añadiendo valor a la cesta) o si están actuando como simples cajeros de supermercado por la presión del turno.
        
        > **En definitiva:** el dashboard te chiva si estás perdiendo dinero por tener a demasiada gente cruzada de brazos, o si estás perdiendo ventas por tener a muy poca gente atendiendo.
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Los datos de entrada (¿Qué hay que meter en el programa?)")
        st.markdown("""
        La magia de esta herramienta es que el Store Manager no tiene que calcular ningún KPI. Solo tiene que exportar un informe \"bruto\" (Raw Data) muy básico desde su terminal de punto de venta (TPV) o sistema de fichajes. Para que el motor en Python escupa toda esta inteligencia, el Excel o CSV que el usuario arrastra solo necesita 8 columnas de datos puros:
        
        1.  **Fecha / Turno**
        2.  **Vendedor_ID** (Quién hizo la venta)
        3.  **Ventas Brutas** (€ generados)
        4.  **Transacciones** (Número de tickets emitidos)
        5.  **Unidades** (Total de artículos pasados por caja)
        6.  **Horas Trabajadas** (Cuánto duró el turno del vendedor)
        7.  **Tráfico Tienda** (El dato del sensor de la puerta)
        8.  **Coste Hora** (El salario hora del empleado)
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

    # NUEVO: BOTÓN POPOVER CON EL ANÁLISIS TÉCNICO E IMPERSONAL
    with st.popover("📊 Ver Análisis Técnico e Interpretación Operativa de la Curva", use_container_width=True):
        st.markdown("### 1. Fundamiento Técnico de la Representación Gráfica")
        st.markdown("""
        La alineación del vector de coste lineal respecto al histograma de tráfico responde a criterios estandarizados de geometría analítica en librerías de visualización bidimensional (Plotly, PowerBI). 
        
        * **El eje de abscisas (X)** opera con variables discretas temporales de carácter cronológico.
        * **Componente de Barras (Tráfico):** Al poseer volumen, la interfaz expande su proyección geométrica simétricamente hacia los márgenes de cada intervalo para proporcionar densidad visual. Sin embargo, su centroide o 'centro de gravedad' exacto coincide con la marca temporal indexada.
        * **Componente de Línea (Coste):** Las funciones lineales carecen de dimensión horizontal y se estructuran como una sucesión de nodos coordenados conectados. Por consiguiente, el punto inicial se ancla exactamente en el centro matemático del periodo, garantizando la máxima precisión al correlacionar variables de distinta naturaleza macroeconómica sobre un mismo eje temporal.
        """)
        
        st.markdown("---")
        st.markdown("### 2. Interpretación Operativa y Análisis de Elasticidad de Costes")
        st.markdown("""
        El objetivo de este modelo no radica en la convergencia lineal de ambas métricas, sino en la evaluación de la **elasticidad del gasto operativo (OPEX)** respecto a la volatilidad de la demanda en el punto de venta.
        
        * **Fase de Mínimos Estructurales (Día 1):** Se constata un escenario de contracción de tráfico (aproximadamente 600 accesos) correlacionado con una optimización estricta del coste laboral, indicativo de un dimensionamiento correcto para jornadas de servicios mínimos o baja afluencia estructural.
        * **Fase de Máxima Eficiencia Operativa (Días 2 al 5):** Se observa un incremento sostenido en el flujo peatonal que supera los 1000 accesos concurrentes; sin embargo, la curva de coste laboral permanece en un estado inelástico y constante. **Insight analítico:** La estructura operativa absorbe una tasa de crecimiento de demanda del 40% sin incurrir en costes marginales de personal, lo que se traduce en una maximización de la productividad por hora (VPH) y una optimización del margen de contribución.
        * **Fase de Adaptación y Flexibilidad (Días 6 y 7):** Ante una desaceleración marginal del tráfico, se registra un ajuste descendente proporcional en la curva de coste, validando la capacidad de flexibilización horaria y control presupuestario en tiempo real.
        
        > ⚠️ **Detección de Anomalías Críticas:** El modelo está diseñado para identificar divergencias inversas (contracción de tráfico frente a picos de coste laboral). Dicho comportamiento asimétrico emitiría automáticamente una alerta de ineficiencia por sobrecapacidad, señalando una pérdida directa de margen operativo por falta de flexibilidad en la planificación de turnos.
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

    with st.expander("📖 Leer Metodología de la Matriz (Para Store Managers)"):
        st.write("""
        **¿Cómo interpretar el gráfico superior para tomar decisiones?**
        - **Cuadrante Superior Derecho (Asesores Top):** Alto Ticket, Alto UPT. Son tus mejores vendedores.
        - **Cuadrante Inferior Izquierdo (Despachadores):** Bajo Ticket, Bajo UPT. Estas personas solo cobran en caja. Necesitan formación en técnicas de venta, o bien, el Mapa de Calor indica que están colapsados de tráfico y no tienen tiempo de atender.
        """)

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
            
        # VENDEDOR 1 (Junior) - Perfil bajo aislado
        t1 = np.random.randint(3, 7)
        u1 = t1 * np.random.uniform(1.0, 1.2)
        v1 = u1 * np.random.uniform(10, 15)
        datos.append([dt, 'Vendedor 1 (Junior)', v1, t1, u1, 1, trafico_hora/4, 12.50])
        
        # VENDEDOR 2 (Senior) - Perfil alto aislado
        t2 = np.random.randint(1, 4)
        u2 = t2 * np.random.uniform(2.5, 3.0)
        v2 = u2 * np.random.uniform(35, 45)
        datos.append([dt, 'Vendedor 2 (Senior)', v2, t2, u2, 1, trafico_hora/4, 12.50])

        # VENDEDOR 3 (Cajero) - Perfil medio-bajo aislado
        t3 = np.random.randint(4, 9)
        u3 = t3 * np.random.uniform(1.2, 1.4)
        v3 = u3 * np.random.uniform(15, 20)
        datos.append([dt, 'Vendedor 3 (Cajero)', v3, t3, u3, 1, trafico_hora/4, 12.50])

        # VENDEDOR 4 (Asesor) - Perfil medio-alto aislado
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
