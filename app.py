import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Retail Shift Optimizer", layout="wide", page_icon="👥")

st.title("👥 Retail Shift & Demand Optimizer")
st.markdown("Motor analítico para el dimensionamiento óptimo de plantillas (Staffing) basado en el impacto real sobre el Ticket Medio (AOV) y Ventas por Empleado (VPH).")

# ==========================================
# 1. ARQUITECTURA HÍBRIDA (MENU LATERAL)
# ==========================================
st.sidebar.header("⚙️ Entorno de Trabajo")
modo = st.sidebar.radio(
    "Selecciona el modo de procesamiento:",
    ("📊 Modo Demo (Portfolio)", "🔒 Auditoría Zero-Disk (Sube tu CSV)")
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Arquitectura Zero-Disk:**\nLos datos comerciales se procesan exclusivamente en la memoria volátil (RAM) y se autodestruyen al cerrar la sesión.")

# ==========================================
# 2. MOTOR DE CÁLCULO DE KPIs
# ==========================================
def renderizar_dashboard(df):
    st.markdown("---")
    
    # Cálculos dinámicos de columnas
    df['Ticket_Medio'] = df['Ventas'] / df['Transacciones']
    df['VPH'] = df['Ventas'] / df['Empleados']
    
    # KPIs Globales
    aov_global = df['Ventas'].sum() / df['Transacciones'].sum()
    vph_global = df['Ventas'].sum() / df['Empleados'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingreso Total Procesado", f"{df['Ventas'].sum():,.2f} €")
    col2.metric("Ticket Medio Global (AOV)", f"{aov_global:.2f} €")
    col3.metric("Productividad Global (VPH)", f"{vph_global:.2f} €/Emp")

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico 1: Impacto del Personal en el Ticket Medio
    st.subheader("📉 Impacto de la Cobertura en la Venta Cruzada (AOV)")
    st.markdown("Analiza cómo la falta de personal reduce la capacidad de atención al cliente y tumba el Ticket Medio.")
    
    # Agrupamos los datos por número de empleados para ver la tendencia
    df_agrupado = df.groupby('Empleados')['Ticket_Medio'].mean().reset_index()
    
    fig_aov = px.bar(
        df_agrupado, x='Empleados', y='Ticket_Medio',
        text_auto='.2f', color='Ticket_Medio',
        color_continuous_scale='Blues',
        labels={'Ticket_Medio': 'Ticket Medio Promedio (€)', 'Empleados': 'Empleados en Turno'}
    )
    fig_aov.update_layout(xaxis_type='category', showlegend=False)
    st.plotly_chart(fig_aov, use_container_width=True)

    # Gráfico 2: Evolución Temporal del VPH
    st.subheader("⏱️ Evolución de Ventas por Hora-Hombre (VPH)")
    fig_vph = px.line(
        df, x='Fecha', y='VPH', 
        markers=True, line_shape='spline',
        labels={'VPH': 'Productividad (€/Empleado)', 'Fecha': 'Día/Turno'}
    )
    fig_vph.update_traces(line_color='#d4af37')
    st.plotly_chart(fig_vph, use_container_width=True)

# ==========================================
# 3. CONTROLADOR DE FLUJO (DEMO VS REAL)
# ==========================================
if modo == "📊 Modo Demo (Portfolio)":
    st.info("💡 **Modo Demostración Activo:** Generando dataset sintético basado en patrones reales de retail para evaluar el comportamiento del algoritmo.")
    
    # Generación de dataset inteligente para el portfolio
    np.random.seed(42)
    fechas = pd.date_range(start="2026-06-01", periods=14, freq='D')
    empleados = np.random.choice([2, 3, 4, 5], size=14)
    transacciones = np.random.randint(100, 300, size=14)
    
    # Truco matemático: Simulamos que con pocos empleados, el ticket baja porque no hay venta cruzada
    ventas = transacciones * (15 + (empleados * 2.5) + np.random.normal(0, 2, 14))
    
    df_demo = pd.DataFrame({
        'Fecha': fechas,
        'Ventas': ventas,
        'Transacciones': transacciones,
        'Empleados': empleados
    })
    
    renderizar_dashboard(df_demo)

else:
    st.warning("🔒 **Modo Zero-Disk Activo:** El procesamiento en la nube no dejará huella en disco. Sube el registro del TPV.")
    archivo_subido = st.file_uploader("Sube un archivo CSV con columnas: Fecha, Ventas, Transacciones, Empleados", type=["csv"])
    
    if archivo_subido is not None:
        try:
            df_real = pd.read_csv(archivo_subido)
            # Verificación básica de estructura
            columnas_requeridas = ['Fecha', 'Ventas', 'Transacciones', 'Empleados']
            if all(col in df_real.columns for col in columnas_requeridas):
                st.success("Dataset validado y procesado en RAM con éxito.")
                renderizar_dashboard(df_real)
            else:
                st.error(f"El archivo debe contener exactamente estas columnas: {', '.join(columnas_requeridas)}")
        except Exception as e:
            st.error(f"Error al leer el archivo. Asegúrate de que es un CSV válido. Detalle: {e}")
