import streamlit as st
import yfinance as yf
import pandas as pd

# CONFIGURACIÓN DE LA TERMINAL V301
st.set_page_config(page_title="SENTINEL V301 - Mando Central", layout="wide")
st.title("🛢️ SENTINEL V301: Operación Insomnio")

def get_data():
    tickers = ["BZ=F", "VIST", "YPF"]
    # Pedimos los últimos 5 días para asegurar que siempre encuentre un cierre
    df = yf.download(tickers, period="5d", interval="1m")
    # Rellenamos los huecos del fin de semana con el último precio conocido
    df_filled = df['Adj Close'].ffill()
    # Retornamos la última fila con datos reales
    return df_filled.iloc[-1]

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
# Medimos la desviación estándar (miedo) de los últimos 20 minutos
hist_brent = yf.download("BZ=F", period="1d", interval="1m")['Adj Close']
volatilidad_actual = hist_brent.std()

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

