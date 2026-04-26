import streamlit as st
import yfinance as yf
import pandas as pd

# CONFIGURACIÓN DE LA TERMINAL V301
st.set_page_config(page_title="SENTINEL V301 - Mando Central", layout="wide")
st.title("🛢️ SENTINEL V301: Operación Insomnio")

def get_data():
    tickers = ["BZ=F", "VIST", "YPF"]
    precios = {}
    
    for t in tickers:
        # Descargamos individualmente con un periodo largo para asegurar datos
        df = yf.download(t, period="5d", interval="1d", progress=False)
        
        # Si la tabla tiene datos, tomamos el último valor de la primera columna
        if not df.empty:
            # .iloc[:,-1] toma el último valor disponible de la primera columna de precios
            precios[t] = float(df.iloc[-1, 0])
        else:
            precios[t] = 0.0
            
    return pd.Series(precios)



# --- MÓDULO 2: CÁLCULO DEL SERRUCHO (RATIO) ---
prices = get_data()
brent = prices['BZ=F']
vista = prices['VIST']
ypf = prices['YPF']

ratio_actual = vista / ypf
ratio_equilibrio = 0.52 # Nuestra base histórica
desvio = ratio_actual - ratio_equilibrio

# --- MÓDULO 3: GESTIÓN DE RIESGO (KELLY CRITERION) ---
# Probabilidad basada en Brent > 105 y Atraso de YPF
prob_exito = 0.92 if (brent > 105 and desvio > 0.04) else 0.50
f_kelly = (prob_exito * 2 - 1) / 2 # Simplificado para el CFO

# --- DASHBOARD DE STREAMLIT ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("BRENT OIL (XBR)", f"u$s {brent:.2f}", delta="ALERTA GEOPOLÍTICA")
    
with col2:
    st.metric("RATIO VIST/YPF", f"{ratio_actual:.3f}", delta=f"{desvio:.3f} (DESVÍO)", delta_color="inverse")

with col3:
    st.metric("SUGERENCIA KELLY", f"{f_kelly*100:.1f}%", "DE TU LIQUIDEZ ($4M)")

# --- SEÑAL DE ACCIÓN ---
if desvio > 0.04:
    st.error("🚨 ZARPAZO DETECTADO: Rotación Inminente a YPF. Vista sobrevaluada vs YPF.")
elif desvio < -0.02:
    st.warning("⚠️ REBOTE VISTA: Oportunidad de recompra en Vista.")
else:
    st.success("✅ MANTENER BÚNKER: El mercado está arbitrado.")
st.sidebar.header("🕹️ Mando del CFO")
noticia_paz = st.sidebar.checkbox("¿Hay rumores de tregua/paz?")
if noticia_paz and brent > 105:
    st.sidebar.info("🤖 V301: Rumores no validados por el precio. Es RUIDO.")
# --- MÓDULO 4: LA CARTA EN LA MANGA (GAMMA/VOLATILIDAD) ---
try:
    hist_brent = yf.download("BZ=F", period="5d", interval="1h")['Adj Close']
    volatilidad_actual = hist_brent.std()
except:
    volatilidad_actual = 0.0 # Respaldo si el mercado está cerrado

# --- MÓDULO 5: DETECTOR DE "SOBRECALENTAMIENTO" ---
# Si el precio sube pero la volatilidad es extrema, es una TRAMPA
es_trampa = True if (desvio > 0.05 and volatilidad_actual > 0.50) else False

# --- ACTUALIZACIÓN DEL DASHBOARD ---
with col1: # Agregamos un indicador de "Clima de Mercado"
    st.metric("VOLATILIDAD (STRESS)", f"{volatilidad_actual:.2f}", "ÍNDICE DE MIEDO")

if es_trampa:
    st.warning("⚠️ CUIDADO: El salto es eufórico y volátil. No comprar, es trampa de apertura.")
elif brent > 105 and volatilidad_actual < 0.20:
    st.success("💎 TENDENCIA SÓLIDA: Subida con baja volatilidad. Es compra institucional real.")
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📊 CARTERA VIVA", "📡 RADAR GEOPOLÍTICO", "📈 ESTRATEGIA LARGO PLAZO"])

with tab1:
    st.subheader("Estado del Búnker")
    # Aquí simulamos tu tenencia actual para ver el P&L en tiempo real
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.info(f"**VISTA:** 102 Nominales (CORE) | Valor: u$s {102 * vista:.2f}")
    with col_c2:
        st.info(f"**YPF:** 101 Nominales (BASE) | Valor: u$s {101 * ypf:.2f}")
    st.write(f"**LIQUIDEZ DISPONIBLE:** $4,000,000 ARS")

with tab2:
    st.subheader("Radar de 'El dinero no duerme'")
    st.write("🚢 **Estrecho de Ormuz:** Bloqueo activo. Impacto alcista: **ALTO**")
    st.write("🇵🇰 **Conflicto Pakistán:** Sin señales de tregua. Riesgo suministro: **88%**")
    st.warning("⚠️ El V301 detecta 'ruido' informativo. Validar con precio del Brent.")

with tab3:
    st.subheader("Rumbo a los u$s 100k - u$s 500k")
    st.success("🎯 **OBJETIVO VISTA:** u$s 85.00 (Target BofA)")
    st.success("🎯 **OBJETIVO YPF:** u$s 52.00 (Recuperación de valor)")
    st.write("💡 **CONSEJO CFO:** No elevar promedio en Vista. Rotar excedentes a YPF mientras el ratio esté arriba de 1.60.")

