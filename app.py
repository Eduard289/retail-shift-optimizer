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
    # Si movemos el slider de Ticket Medio, aumentamos las ventas proporcionalmente a las transacciones
    df['Ventas'] = df['Ventas'] + (df['Transacciones'] * sim_aov)
    # Si ajustamos plantilla, multiplicamos las horas reales
    df['Horas_Trabajadas'] = df['Horas_Trabajadas'] * (1 + (sim_personal / 100))
    
    # ------------------------------------------
    # CÁLCULO DE KPIs
    # ------------------------------------------
    df['Ticket_Medio'] = df['Ventas'] / df['Transacciones'].replace(0, 1)
    df['UPT'] = df['Unidades'] / df['Transacciones'].replace(0, 1)
    df['VPH'] = df['Ventas'] / df['Horas_Trabajadas'].replace(0, 1)
    df['Coste_Laboral_Total'] = df['Horas_Trabajadas'] * df['Coste_Hora']
    
    # KPIs Globales Agregados
    ventas_totales = df['Ventas'].sum()
    aov_global = ventas_totales / df['Transacciones'].sum()
    upt_global = df['Unidades'].sum() / df['Transacciones'].sum()
    vph_global = ventas_totales / df['Horas_Trabajadas'].sum()
    coste_laboral_pct = (df['Coste_Laboral_Total'].sum() / ventas_totales) * 100
    conversion_global = (df['Transacciones'].sum() / df['Trafico_Tienda'].sum()) * 100

    st.markdown("---")
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
    # NUEVO: MAPA DE CALOR HORARIO (ZONAS DE PELIGRO)
    # ==========================================
    st.subheader("🔥 Mapa de Calor: Saturación de Tienda (Zonas de Peligro)")
    st.markdown("Identifica las horas críticas donde el ratio **Clientes por Empleado** se dispara, provocando fugas de ventas y caídas de conversión.")
    
    # Extraemos Día y Hora de la marca de tiempo
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Hora'] = df['Fecha'].dt.hour
    df['Dia_Semana'] = df['Fecha'].dt.day_name().map({
        'Monday': '1-Lunes', 'Tuesday': '2-Martes', 'Wednesday': '3-Miércoles', 
        'Thursday': '4-Jueves', 'Friday': '5-Viernes', 'Saturday': '6-Sábado', 'Sunday': '7-Domingo'
    })
    
    # Calculamos la carga de trabajo (Clientes por Empleado)
    df_heat = df.groupby(['Dia_Semana', 'Hora']).agg({'Trafico_Tienda': 'sum', 'Horas_Trabajadas': 'sum'}).reset_index()
    df_heat['Carga_Trabajo'] = df_heat['Trafico_Tienda'] / df_heat['Horas_Trabajadas'].replace(0, 1)
    
    heatmap_data = df_heat.pivot_table(index='Hora', columns='Dia_Semana', values='Carga_Trabajo', aggfunc='mean')
    
    fig_heat = px.imshow(
        heatmap_data, 
        labels=dict(x="Día de la Semana", y="Franja Horaria", color="Clientes por Empleado"),
        color_continuous_scale="Reds", 
        aspect="auto"
    )
    fig_heat.update_layout(height=400, yaxis=dict(tickmode='linear', dtick=1))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # GRÁFICO: MATRIZ DE RENDIMIENTO (CON SOLAPAMIENTO CORREGIDO)
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
    
    # MARCAS DE AGUA CORREGIDAS (Desplazamiento vertical para no pisar las burbujas)
    max_upt, max_aov = df_vendedores['UPT'].max(), df_vendedores['Ticket_Medio'].max()
    min_upt, min_aov = df_vendedores['UPT'].min(), df_vendedores['Ticket_Medio'].min()

    fig_matrix.add_annotation(
        x=max_upt, y=max_aov + (max_aov * 0.05), # Desplazado ligeramente hacia arriba
        text="🌟 ASESORES TOP", showarrow=False, opacity=0.3, font=dict(size=20)
    )
    fig_matrix.add_annotation(
        x=min_upt, y=min_aov - (min_aov * 0.08), # Desplazado ligeramente hacia abajo
        text="📦 DESPACHADORES", showarrow=False, opacity=0.3, font=dict(size=20)
    )
    
    fig_matrix.update_traces(textposition='top center')
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
    
    # Generación de dataset horario (Time-Series) para que el Heatmap funcione
    np.random.seed(42)
    fechas_horas = pd.date_range(start="2026-06-01 10:00", end="2026-06-07 21:00", freq='h')
    vendedores = ['Vendedor 1 (Junior)', 'Vendedor 2 (Senior)', 'Vendedor 3 (Cajero)', 'Vendedor 4 (Asesor)']
    
    datos = []
    for dt in fechas_horas:
        # Simulamos que de 18:00 a 20:00 hay picos de tráfico
        if 18 <= dt.hour <= 20:
            trafico_hora = np.random.randint(60, 150)
        else:
            trafico_hora = np.random.randint(10, 50)
            
        for v in vendedores:
            horas = 1  # 1 hora por registro
            coste_h = 12.50
            
            if "Senior" in v or "Asesor" in v:
                transacciones = np.random.randint(1, 4)
                unidades = transacciones * np.random.uniform(1.8, 3.0)
                ventas = unidades * np.random.uniform(25, 45)
            else:
                transacciones = np.random.randint(3, 7)
                unidades = transacciones * np.random.uniform(1.0, 1.3)
                ventas = unidades * np.random.uniform(10, 20)
                
            datos.append([dt, v, ventas, transacciones, unidades, horas, trafico_hora/4, coste_h])
            
    df_demo = pd.DataFrame(datos, columns=['Fecha', 'Vendedor_ID', 'Ventas', 'Transacciones', 'Unidades', 'Horas_Trabajadas', 'Trafico_Tienda', 'Coste_Hora'])
    
    renderizar_dashboard(df_demo)

else:
    st.warning("🔒 **Modo Zero-Disk Activo:** El procesamiento no dejará huella en disco. Sube el CSV de tu TPV.")
    st.markdown("**Estructura requerida del CSV:** `Fecha` (ej: 2026-06-01 14:00), `Vendedor_ID`, `Ventas`, `Transacciones`, `Unidades`, `Horas_Trabajadas`, `Trafico_Tienda`, `Coste_Hora`")
    
    archivo_subido = st.file_uploader("Arrastra tu archivo aquí", type=["csv"])
    
    if archivo_subido is not None:
        try:
            df_real = pd.read_csv(archivo_subido)
            # Requerimos las mismas columnas para mantener la integridad del dashboard
            columnas_requeridas = ['Fecha', 'Vendedor_ID', 'Ventas', 'Transacciones', 'Unidades', 'Horas_Trabajadas', 'Trafico_Tienda', 'Coste_Hora']
            if all(col in df_real.columns for col in columnas_requeridas):
                st.success("Dataset validado y procesado en RAM con éxito.")
                renderizar_dashboard(df_real)
            else:
                st.error(f"Faltan columnas. El archivo debe contener exactamente: {', '.join(columnas_requeridas)}")
        except Exception as e:
            st.error(f"Error al leer el archivo. Detalle: {e}")
