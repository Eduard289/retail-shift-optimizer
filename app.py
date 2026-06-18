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
# 1. ARQUITECTURA HÍBRIDA (MENU LATERAL)
# ==========================================
st.sidebar.header("⚙️ Entorno de Trabajo")
modo = st.sidebar.radio(
    "Selecciona el modo de procesamiento:",
    ("📊 Modo Demo (Portfolio)", "🔒 Auditoría Zero-Disk (Sube tu CSV)")
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Arquitectura Zero-Disk:**\nLos datos comerciales se procesan exclusivamente en la memoria volátil (RAM) y se autodestruyen al cerrar la sesión. Cumplimiento absoluto de privacidad corporativa.")

# ==========================================
# 2. MOTOR DE CÁLCULO Y DASHBOARD
# ==========================================
def renderizar_dashboard(df):
    st.markdown("---")
    
    # Cálculos dinámicos de columnas
    df['Ticket_Medio'] = df['Ventas'] / df['Transacciones']
    df['UPT'] = df['Unidades'] / df['Transacciones']
    df['VPH'] = df['Ventas'] / df['Horas_Trabajadas']
    df['Coste_Laboral_Total'] = df['Horas_Trabajadas'] * df['Coste_Hora']
    df['Conversion_Pct'] = (df['Transacciones'] / df['Trafico_Tienda']) * 100
    
    # KPIs Globales Agregados
    ventas_totales = df['Ventas'].sum()
    aov_global = ventas_totales / df['Transacciones'].sum()
    upt_global = df['Unidades'].sum() / df['Transacciones'].sum()
    vph_global = ventas_totales / df['Horas_Trabajadas'].sum()
    coste_laboral_pct = (df['Coste_Laboral_Total'].sum() / ventas_totales) * 100
    conversion_global = (df['Transacciones'].sum() / df['Trafico_Tienda'].sum()) * 100

    # ==========================================
    # FILA 1: KPIs FINANCIEROS (Con Tooltips Educativos)
    # ==========================================
    st.markdown("### 📈 Salud Financiera del Turno")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Ingreso Total", f"{ventas_totales:,.0f} €", 
                help="Volumen total de ventas brutas generadas en el periodo analizado.")
    
    col2.metric("Coste Laboral sobre Ventas", f"{coste_laboral_pct:.1f} %", 
                delta="Riesgo si > 15%" if coste_laboral_pct > 15 else "Óptimo", delta_color="inverse",
                help="Porcentaje de los ingresos que se destina a pagar el turno. Un ratio alto en horas valle destruye el P&L (Cuenta de Resultados).")
    
    col3.metric("Tasa de Conversión", f"{conversion_global:.1f} %",
                help="Porcentaje de personas que entraron a la tienda y acabaron comprando. Refleja la capacidad de captación del personal.")
    
    col4.metric("Productividad (VPH)", f"{vph_global:.1f} €/h",
                help="Ventas por Hora-Hombre. Cuántos euros genera cada empleado por cada hora de su turno.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # FILA 2: KPIs COMERCIALES
    # ==========================================
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Ticket Medio (AOV)", f"{aov_global:.2f} €",
                help="Gasto promedio por cliente (Average Order Value).")
    col6.metric("Unidades por Ticket (UPT)", f"{upt_global:.2f}",
                help="Mide la profundidad de la cesta y el éxito del cross-selling (Venta Cruzada).")
    col7.metric("Tráfico Total (Entradas)", f"{df['Trafico_Tienda'].sum():,.0f}",
                help="Dato cruzado con sensores cuenta-personas.")
    col8.metric("Transacciones (Tickets)", f"{df['Transacciones'].sum():,.0f}")

    st.markdown("---")

    # ==========================================
    # GRÁFICO 1: MATRIZ DE RENDIMIENTO POR VENDEDOR
    # ==========================================
    st.subheader("🎯 Auditoría de Rendimiento Individual (Matriz Asesor vs Despachador)")
    st.markdown("Identifica carencias formativas cruzando la capacidad de venta cruzada (UPT) con el Ticket Medio (AOV).")
    
    df_vendedores = df.groupby('Vendedor_ID').agg({
        'Ticket_Medio': 'mean',
        'UPT': 'mean',
        'Ventas': 'sum',
        'Transacciones': 'sum'
    }).reset_index()

    fig_matrix = px.scatter(
        df_vendedores, x='UPT', y='Ticket_Medio', size='Ventas', color='Vendedor_ID',
        hover_name='Vendedor_ID', text='Vendedor_ID', size_max=40,
        labels={'UPT': 'Venta Cruzada (UPT)', 'Ticket_Medio': 'Ticket Medio (€)'}
    )
    
    # Líneas de media para crear los 4 cuadrantes
    fig_matrix.add_hline(y=aov_global, line_dash="dash", annotation_text="Media AOV", annotation_position="bottom right")
    fig_matrix.add_vline(x=upt_global, line_dash="dash", annotation_text="Media UPT", annotation_position="top left")
    
    # Anotaciones de Cuadrantes
    fig_matrix.add_annotation(x=df_vendedores['UPT'].max(), y=df_vendedores['Ticket_Medio'].max(), text="🌟 ASESORES TOP", showarrow=False, opacity=0.3, font=dict(size=20))
    fig_matrix.add_annotation(x=df_vendedores['UPT'].min(), y=df_vendedores['Ticket_Medio'].min(), text="📦 DESPACHADORES", showarrow=False, opacity=0.3, font=dict(size=20))
    
    fig_matrix.update_traces(textposition='top center')
    fig_matrix.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_matrix, use_container_width=True)

    # ==========================================
    # ACORDEÓN: METODOLOGÍA (Pop-up de lectura)
    # ==========================================
    with st.expander("📖 Leer Metodología de la Matriz (Para Store Managers)"):
        st.write("""
        **¿Cómo interpretar el gráfico superior para tomar decisiones?**
        - **Cuadrante Superior Derecho (Asesores Top):** Alto Ticket, Alto UPT. Son tus mejores vendedores. Tienen tiempo para atender al cliente, hacen venta cruzada y cierran ventas de alto valor. Usa a estas personas para formar a los nuevos.
        - **Cuadrante Inferior Izquierdo (Despachadores):** Bajo Ticket, Bajo UPT. Estas personas solo cobran en caja. Si la tienda está vacía y siguen aquí, necesitan formación urgente en técnicas de venta. Si la tienda está saturada, es síntoma de infracobertura (falta personal y solo tienen tiempo para cobrar rápido).
        """)

    # ==========================================
    # GRÁFICO 2: IMPACTO EXÓGENO (TRÁFICO VS COSTE)
    # ==========================================
    st.markdown("---")
    st.subheader("⚖️ Curva de Eficiencia: Tráfico vs Coste Laboral")
    
    df_temporal = df.groupby('Fecha').agg({'Trafico_Tienda': 'sum', 'Coste_Laboral_Total': 'sum'}).reset_index()
    
    fig_eficiencia = go.Figure()
    fig_eficiencia.add_trace(go.Bar(x=df_temporal['Fecha'], y=df_temporal['Trafico_Tienda'], name='Tráfico (Clientes)', marker_color='#3498db'))
    fig_eficiencia.add_trace(go.Scatter(x=df_temporal['Fecha'], y=df_temporal['Coste_Laboral_Total'], name='Coste Laboral (€)', yaxis='y2', mode='lines+markers', line=dict(color='#e74c3c', width=3)))
    
    fig_eficiencia.update_layout(
        yaxis=dict(title='Tráfico Peatonal'),
        yaxis2=dict(title='Coste Laboral (€)', overlaying='y', side='right'),
        height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_eficiencia, use_container_width=True)

# ==========================================
# 3. CONTROLADOR DE FLUJO (DEMO VS REAL)
# ==========================================
if modo == "📊 Modo Demo (Portfolio)":
    st.info("💡 **Modo Demostración:** Dataset sintético pre-cargado. Simula el rendimiento de 4 vendedores con perfiles psicológicos distintos a lo largo de una semana.")
    
    # Generación de dataset inteligente para el portfolio
    np.random.seed(42)
    fechas = pd.date_range(start="2026-06-01", periods=7, freq='D')
    vendedores = ['Vendedor 1 (Junior)', 'Vendedor 2 (Senior)', 'Vendedor 3 (Cajero)', 'Vendedor 4 (Asesor)']
    
    datos = []
    for fecha in fechas:
        trafico_dia = np.random.randint(200, 600)
        for v in vendedores:
            horas = 8
            coste_h = 12.50
            
            # Simulamos perfiles reales
            if "Senior" in v or "Asesor" in v:
                transacciones = np.random.randint(15, 30)
                unidades = transacciones * np.random.uniform(1.8, 3.0) # UPT alto
                ventas = unidades * np.random.uniform(25, 45) # Artículos caros
            else:
                transacciones = np.random.randint(30, 50) # Hace muchos tickets (cajero)
                unidades = transacciones * np.random.uniform(1.0, 1.3) # UPT bajo
                ventas = unidades * np.random.uniform(10, 20) # Artículos baratos
                
            datos.append([fecha, v, ventas, transacciones, unidades, horas, trafico_dia/4, coste_h])
            
    df_demo = pd.DataFrame(datos, columns=['Fecha', 'Vendedor_ID', 'Ventas', 'Transacciones', 'Unidades', 'Horas_Trabajadas', 'Trafico_Tienda', 'Coste_Hora'])
    
    renderizar_dashboard(df_demo)

else:
    st.warning("🔒 **Modo Zero-Disk Activo:** El procesamiento no dejará huella en disco. Sube el CSV de tu TPV.")
    st.markdown("**Estructura requerida del CSV:** `Fecha`, `Vendedor_ID`, `Ventas`, `Transacciones`, `Unidades`, `Horas_Trabajadas`, `Trafico_Tienda`, `Coste_Hora`")
    
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
