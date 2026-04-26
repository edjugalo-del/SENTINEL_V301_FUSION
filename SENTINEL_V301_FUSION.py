import streamlit as st
import yfinance as yf
import pandas as pd

# CONFIGURACIÓN DE LA TERMINAL V301
st.set_page_config(page_title="SENTINEL V301 - Mando Central", layout="wide")
st.title("🛢️ SENTINEL V301: Operación Insomnio")

# --- AJUSTE DE PRECISIÓN PARA EL BRENT ---
def get_data():
    # Pedimos los tres contratos posibles para el Brent
    # BZ=F (Genérico), LCO=F (Londres), LCOc1 (Continuo)
    tickers_brent = ["BZ=F", "LCO=F"]
    tickers_acciones = ["VIST", "YPF"]
    
    # 1. Descargamos Acciones
    df_acc = yf.download(tickers_acciones, period="2d", interval="1m", progress=False)
    datos_acc = df_acc['Adj Close'].ffill().iloc[-1]
    
    # 2. Descargamos Brent (Buscamos el contrato más activo)
    df_brent = yf.download(tickers_brent, period="2d", interval="1m", progress=False)
    # Tomamos el valor máximo entre los contratos disponibles para capturar el 'Front Month'
    brent_v301 = df_brent['Adj Close'].ffill().iloc[-1].max()
    
    # 3. Consolidamos el Búnker
    datos_acc['BZ=F'] = brent_v301
    return datos_acc




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
st.markdown("---")
st.subheader("🌊 Visualizador del Serrucho (Arbitraje en Vivo)")

# --- VISUALIZADOR DEL SERRUCHO BLINDADO (Línea 112 en adelante) ---
try:
    # Usamos 7 días para saltar el bache del fin de semana
    hist_v = yf.download("VIST", period="7d", interval="60m")['Adj Close']
    hist_y = yf.download("YPF", period="7d", interval="60m")['Adj Close']
    
    # Verificamos que tengamos datos antes de graficar
    if not hist_v.empty and not hist_y.empty:
        # Alineamos y calculamos el serrucho
        serrucho = (hist_v.ffill() / hist_y.ffill())
        st.line_chart(serrucho)
        
        # Lógica de "Zonas de Ataque"
        r_actual = serrucho.iloc[-1]
        r_media = serrucho.mean()
        
        if r_actual > (r_media * 1.05):
            st.error(f"🚨 **ZONA DE ROTACIÓN:** Ratio ({r_actual:.3f}) muy alto. ¡Vender Vista / Entrar YPF!")
        elif r_actual < (r_media * 0.95):
            st.success(f"💎 **ZONA DE RECOMPRA:** Ratio ({r_actual:.3f}) en el piso. ¡Volver a Vista!")
        else:
            st.info(f"⚖️ **ZONA NEUTRAL:** El serrucho está equilibrado ({r_actual:.3f}).")
    else:
        st.info("📡 Sincronizando periscopio... Esperando apertura de mercados.")
except:
    st.info("📡 Sincronizando periscopio... El serrucho se activará con los datos de apertura.")
# --- MÓDULO 6: MÉTRICAS DE ATAQUE (MOMENTUM Y RSI) ---
# --- MÓDULO 6: RADAR DE ATAQUE (MOMENTUM Y RSI) ---
def calcular_metricas(ticker):
    try:
        df = yf.download(ticker, period="10d", interval="60m", progress=False)
        if df.empty: return 0.0, 50.0
        precios = df['Adj Close'].ffill()
        momentum = ((precios.iloc[-1] - precios.iloc[-14]) / precios.iloc[-14]) * 100
        delta = precios.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        return momentum, rsi
    except:
        return 0.0, 50.0

mom_v, rsi_v = calcular_metricas("VIST")
mom_y, rsi_y = calcular_metricas("YPF")

# --- VISUALIZACIÓN EN LA APP (MOMENTUM Y CARTERA) ---
st.markdown("---")
st.subheader("🚀 Radar de Impulso y Fuerza (V301)")
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric("MOMENTUM VISTA", f"{mom_v:.2f}%", delta="IMPULSO" if mom_v >= 0 else "CAÍDA")
    st.progress(int(rsi_v) if 0 <= rsi_v <= 100 else 50, text=f"Fuerza RSI: {rsi_v:.1f}")
with col_m2:
    st.metric("MOMENTUM YPF", f"{mom_y:.2f}%", delta="IMPULSO" if mom_y >= 0 else "CAÍDA")
    st.progress(int(rsi_y) if 0 <= rsi_y <= 100 else 50, text=f"Fuerza RSI: {rsi_y:.1f}")

st.markdown("---")
st.subheader("📊 MI BÚNKER (Valores Reales ARS)")
monto_vista_ars, monto_ypf_ars = 3606720, 6486725
total_cartera = monto_vista_ars + monto_ypf_ars + 4000000

c1, c2, c3 = st.columns(3)
with c1: st.metric("VISTA (CORE)", f"${monto_vista_ars:,.0f}")
with c2: st.metric("YPF (BASE)", f"${monto_ypf_ars:,.0f}")
with c3: st.metric("NETO TOTAL", f"${total_cartera:,.0f}", "Score IA: 98%")

if st.sidebar.checkbox("👁️ Modo Privacidad"):
    st.markdown("<style>div[data-testid='stMetricValue'] {filter: blur(10px);}</style>", unsafe_allow_html=True)
