import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

# ─────────────────────────────────────────────
# CONFIG Y ESTILOS GLOBALES
# ─────────────────────────────────────────────

LAT_RESTAURANTE = 4.682
LON_RESTAURANTE = -74.103

st.set_page_config(
    page_title="QuickOps",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700;800&display=swap');

  .stApp { background: #1a1a1a; }

  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #b30000 0%, #e60000 40%, #ff6600 100%) !important;
  }
  [data-testid="stSidebar"] * { color: #fff !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stTextInput label {
      color: #ffe066 !important;
      font-family: 'Nunito', sans-serif;
      font-weight: 800;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 1px;
  }
  [data-testid="stSidebar"] .stSelectbox > div > div,
  [data-testid="stSidebar"] .stTextInput > div > div > input {
      background: rgba(255,255,255,0.15) !important;
      border: 2px solid rgba(255,255,255,0.4) !important;
      color: #fff !important;
      border-radius: 8px !important;
  }

  .sidebar-logo {
      font-family: 'Bangers', cursive;
      font-size: 2.8rem;
      color: #ffe066;
      text-align: center;
      letter-spacing: 4px;
      text-shadow: 3px 3px 0px #b30000, 5px 5px 0px rgba(0,0,0,0.3);
      padding: 10px 0 5px;
      line-height: 1;
  }
  .sidebar-tagline {
      font-family: 'Nunito', sans-serif;
      font-size: 0.75rem;
      color: rgba(255,255,255,0.85);
      text-align: center;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 20px;
  }
  .sidebar-divider {
      border: none;
      border-top: 2px dashed rgba(255,255,255,0.3);
      margin: 12px 0;
  }

  .section-header {
      font-family: 'Bangers', cursive;
      font-size: 2.4rem;
      color: #ffe066;
      letter-spacing: 3px;
      text-shadow: 3px 3px 0px #e60000;
      margin-bottom: 4px;
  }
  .section-sub {
      font-family: 'Nunito', sans-serif;
      color: #aaa;
      font-size: 0.9rem;
      margin-bottom: 20px;
      text-transform: uppercase;
      letter-spacing: 1px;
  }

  .kpi-card {
      background: linear-gradient(135deg, #2a2a2a, #1e1e1e);
      border: 2px solid #e60000;
      border-radius: 16px;
      padding: 22px 20px;
      text-align: center;
      box-shadow: 0 6px 20px rgba(230,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.05);
      position: relative;
      overflow: hidden;
  }
  .kpi-card::before {
      content: '';
      position: absolute;
      top: -30px; right: -30px;
      width: 80px; height: 80px;
      background: rgba(230,0,0,0.12);
      border-radius: 50%;
  }
  .kpi-icon { font-size: 2rem; margin-bottom: 6px; display: block; }
  .kpi-value {
      font-family: 'Bangers', cursive;
      font-size: 2.5rem;
      color: #ffe066;
      letter-spacing: 2px;
      line-height: 1;
  }
  .kpi-label {
      font-family: 'Nunito', sans-serif;
      font-size: 0.78rem;
      color: #aaa;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-top: 4px;
  }

  .badge-success { background: #00b300; color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-family: 'Nunito', sans-serif; font-weight: 700; }
  .badge-warning { background: #ff9900; color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-family: 'Nunito', sans-serif; font-weight: 700; }
  .badge-danger  { background: #e60000; color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-family: 'Nunito', sans-serif; font-weight: 700; }

  .stButton > button {
      background: linear-gradient(135deg, #e60000, #ff6600) !important;
      color: #fff !important;
      font-family: 'Nunito', sans-serif !important;
      font-weight: 800 !important;
      font-size: 0.95rem !important;
      border: none !important;
      border-radius: 10px !important;
      padding: 10px 28px !important;
      letter-spacing: 1px !important;
      text-transform: uppercase !important;
      box-shadow: 0 4px 15px rgba(230,0,0,0.4) !important;
      transition: all 0.2s ease !important;
  }
  .stButton > button:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 6px 20px rgba(230,0,0,0.6) !important;
  }

  .stTextInput > div > div > input,
  .stNumberInput > div > div > input,
  .stTextArea textarea,
  .stSelectbox > div > div {
      background: #2a2a2a !important;
      border: 2px solid #444 !important;
      color: #fff !important;
      border-radius: 10px !important;
  }
  .stTextInput > div > div > input:focus,
  .stNumberInput > div > div > input:focus,
  .stTextArea textarea:focus {
      border-color: #e60000 !important;
      box-shadow: 0 0 0 3px rgba(230,0,0,0.2) !important;
  }
  label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stTextArea label, .stSlider label {
      color: #ccc !important;
      font-family: 'Nunito', sans-serif !important;
      font-weight: 700 !important;
      font-size: 0.85rem !important;
      text-transform: uppercase !important;
      letter-spacing: 1px !important;
  }

  .stDataFrame { border-radius: 12px; overflow: hidden; }
  [data-testid="stDataFrame"] { background: #2a2a2a !important; }
  hr { border-color: #333 !important; }

  .stSuccess, [data-testid="stNotification"] {
      background: #003300 !important;
      border-left: 4px solid #00cc44 !important;
      border-radius: 10px !important;
  }
  .stInfo {
      background: #001a33 !important;
      border-left: 4px solid #0088ff !important;
  }

  .pedido-card {
      background: #2a2a2a;
      border: 1px solid #444;
      border-left: 5px solid #e60000;
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 12px;
  }
  .pedido-card h4 { font-family: 'Nunito', sans-serif; color: #ffe066; font-weight: 800; margin: 0 0 4px; }
  .pedido-card p  { color: #aaa; font-size: 0.85rem; margin: 0; }

  html { scroll-behavior: smooth; }

  [data-testid="metric-container"] {
      background: #2a2a2a;
      border: 1px solid #444;
      border-radius: 12px;
      padding: 16px;
  }
  [data-testid="metric-container"] label { color: #aaa !important; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
      color: #ffe066 !important;
      font-family: 'Bangers', cursive !important;
      font-size: 2rem !important;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ESTADO GLOBAL
# ─────────────────────────────────────────────

if "pedidos"    not in st.session_state: st.session_state.pedidos    = []
if "inventario" not in st.session_state: st.session_state.inventario = {"Pan":50,"Carne":40,"Papas":60,"Bebidas":30}
if "empleados"  not in st.session_state: st.session_state.empleados  = {"Gino Florez":"Gino123","Brenda Torres":"Brenda123","Luisa Giraldo":"123"}
if "turnos"     not in st.session_state: st.session_state.turnos     = []
if "encuestas"  not in st.session_state: st.session_state.encuestas  = []

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def kpi(icon, value, label):
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def header(title, sub=""):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="section-sub">{sub}</div>', unsafe_allow_html=True)

def make_chart(labels, values, color="#e60000", horizontal=False):
    fig, ax = plt.subplots(figsize=(6, 3.2))
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    bar_colors = [color, "#ff6600"] if len(values) == 2 else [color] * len(values)
    if horizontal:
        bars = ax.barh(labels, values, color=bar_colors, height=0.5, edgecolor="none")
        ax.set_xlabel("Cantidad", color="#aaa", fontsize=9)
    else:
        bars = ax.bar(labels, values, color=bar_colors, width=0.5, edgecolor="none")
        ax.set_ylabel("Cantidad", color="#aaa", fontsize=9)
    ax.tick_params(colors="#ccc", labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    ax.yaxis.label.set_color("#aaa")
    ax.xaxis.label.set_color("#aaa")
    for bar in bars:
        if horizontal:
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{int(bar.get_width())}', va='center', color='#ffe066', fontsize=10, fontweight='bold')
        else:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{int(bar.get_height())}', ha='center', color='#ffe066', fontsize=10, fontweight='bold')
    plt.tight_layout()
    return fig

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🍔 QuickOps</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Sistema Operativo Fast Food</div>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    rol = st.selectbox(
        "👤 Selecciona tu rol",
        ["— Seleccionar —", "Gerencia", "Colaborador", "Comercial", "Logística", "Experiencia"]
    )

    if rol not in ["— Seleccionar —"]:
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    clave_ingresada = ""
    nombre_colab = ""
    area_colab = ""

    if rol == "Gerencia":
        clave_ingresada = st.text_input("🔑 Clave gerencial", type="password")
    elif rol == "Colaborador":
        nombre_colab = st.selectbox("👷 Empleado", list(st.session_state.empleados.keys()))
        clave_ingresada = st.text_input("🔑 Clave", type="password")
        area_colab = st.selectbox("🏢 Área de trabajo", ["Caja", "Cocina", "Inventario", "Encuesta"])
    elif rol == "Comercial":
        clave_ingresada = st.text_input("🔑 Clave comercial", type="password")
    elif rol == "Logística":
        clave_ingresada = st.text_input("🔑 Clave logística", type="password")
    elif rol == "Experiencia":
        clave_ingresada = st.text_input("🔑 Clave cliente", type="password")

# ─────────────────────────────────────────────
# PANTALLA DE BIENVENIDA
# ─────────────────────────────────────────────

if rol == "— Seleccionar —":
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px 30px;">
        <div style="font-family:'Bangers',cursive; font-size:5rem; color:#ffe066;
                    text-shadow: 5px 5px 0px #e60000, 8px 8px 0px rgba(0,0,0,0.4);
                    letter-spacing: 8px; line-height:1;">
            🍔 QUICKOPS
        </div>
        <div style="font-family:'Nunito',sans-serif; color:#aaa; font-size:1rem;
                    letter-spacing: 4px; text-transform:uppercase; margin-top:10px;">
            Sistema de Gestión Operacional
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    modulos = [
        ("📊", "Gerencia",     "Dashboard y KPIs"),
        ("🧾", "Colaborador",  "Caja · Cocina · Inventario"),
        ("💰", "Comercial",    "Ventas y estrategias"),
        ("🚚", "Logística",    "Rutas y entregas"),
        ("⭐", "Experiencia",  "Satisfacción del cliente"),
    ]
    for col, (icon, name, desc) in zip([col1,col2,col3,col4,col5], modulos):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">{icon}</span>
                <div style="font-family:'Bangers',cursive; color:#ffe066; font-size:1.3rem; letter-spacing:2px;">{name}</div>
                <div style="font-family:'Nunito',sans-serif; color:#888; font-size:0.72rem; margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)
    st.stop()

# ═════════════════════════════════════════════
# GERENCIA
# ═════════════════════════════════════════════

if rol == "Gerencia":
    if clave_ingresada == "Gerencia123***":
        header("📊 Panel de Gerencia", "Vista ejecutiva · Operaciones en tiempo real")
        tab1, tab2 = st.tabs(["📈 Dashboard", "🕒 Turnos"])

        with tab1:
            total_pedidos = len(st.session_state.pedidos)
            despachados   = len([p for p in st.session_state.pedidos if p["estado"] == "despachado"])
            pendientes    = total_pedidos - despachados
            eficiencia    = round((despachados / total_pedidos * 100) if total_pedidos > 0 else 0, 1)

            c1, c2, c3, c4 = st.columns(4)
            with c1: kpi("📦", total_pedidos, "Pedidos totales")
            with c2: kpi("✅", despachados,   "Despachados")
            with c3: kpi("⏳", pendientes,    "Pendientes")
            with c4: kpi("📈", f"{eficiencia}%", "Eficiencia")

            st.markdown("<br>", unsafe_allow_html=True)
            col_g, col_i = st.columns(2)
            with col_g:
                st.markdown("**Estado de pedidos**")
                st.pyplot(make_chart(["Pendientes", "Despachados"], [pendientes, despachados]))
            with col_i:
                st.markdown("**Inventario actual**")
                st.pyplot(make_chart(list(st.session_state.inventario.keys()), list(st.session_state.inventario.values()), color="#ff6600", horizontal=True))

        with tab2:
            header("🕒 Gestión de Turnos", "Asignación semanal de colaboradores")
            c1, c2, c3 = st.columns(3)
            with c1: empleado = st.text_input("Nombre del empleado")
            with c2: dia = st.selectbox("Día", ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"])
            with c3: horas = st.number_input("Horas de turno", 1, 12)
            if st.button("➕ Registrar turno"):
                if empleado:
                    st.session_state.turnos.append({"empleado": empleado, "dia": dia, "horas": horas})
                    st.success(f"✅ Turno registrado para {empleado}")
                else:
                    st.warning("Ingresa el nombre del empleado.")
            if st.session_state.turnos:
                st.dataframe(pd.DataFrame(st.session_state.turnos), use_container_width=True)
            else:
                st.info("No hay turnos registrados aún.")

    elif clave_ingresada:
        st.error("❌ Clave incorrecta")

# ═════════════════════════════════════════════
# COMERCIAL
# ═════════════════════════════════════════════

elif rol == "Comercial":
    if clave_ingresada == "Comercial123**":
        header("💰 Área Comercial", "Análisis de ventas y estrategias")

        ventas = [15000 if p["tipo"] == "Mesa" else 20000
                  for p in st.session_state.pedidos if p["estado"] == "despachado"]
        total_ventas = sum(ventas)
        num_ventas   = len(ventas)
        promedio     = total_ventas / num_ventas if num_ventas > 0 else 0

        c1, c2, c3 = st.columns(3)
        with c1: kpi("💰", f"${total_ventas:,}", "Ventas totales")
        with c2: kpi("🧾", num_ventas, "N° de ventas")
        with c3: kpi("📈", f"${round(promedio):,}", "Ticket promedio")

        st.markdown("<br>", unsafe_allow_html=True)

        if total_ventas > 200000:
            st.markdown('<span class="badge-success">🚀 Ventas ALTAS — ¡Excelente rendimiento!</span>', unsafe_allow_html=True)
            estado = "alto"
        elif total_ventas > 100000:
            st.markdown('<span class="badge-warning">⚠️ Ventas moderadas — Hay oportunidades de mejora</span>', unsafe_allow_html=True)
            estado = "medio"
        else:
            st.markdown('<span class="badge-danger">❌ Ventas bajas — Se requiere acción inmediata</span>', unsafe_allow_html=True)
            estado = "bajo"

        st.markdown("<br>", unsafe_allow_html=True)
        col_g, col_e = st.columns(2)
        with col_g:
            st.markdown("**Ventas por tipo de pedido**")
            mesa_count = len([p for p in st.session_state.pedidos if p["tipo"] == "Mesa"])
            dom_count  = len([p for p in st.session_state.pedidos if p["tipo"] == "Domicilio"])
            st.pyplot(make_chart(["Mesa", "Domicilio"], [mesa_count, dom_count]))
        with col_e:
            st.markdown("**🚀 Estrategias recomendadas**")
            estrategias = {
                "alto":  [("✔", "Mantener calidad del servicio"), ("✔", "Implementar programa de fidelización"), ("✔", "Promociones por volumen de compra")],
                "medio": [("✔", "Ofertas en horas valle"), ("✔", "Combos promocionales atractivos"), ("✔", "Publicidad activa en redes sociales")],
                "bajo":  [("❗", "Descuentos agresivos en productos clave"), ("❗", "Campaña urgente de marketing"), ("❗", "Revisar precios y tiempos de atención")],
            }
            for icon, txt in estrategias[estado]:
                color = "#00cc44" if icon == "✔" else "#e60000"
                st.markdown(f'<div style="background:#2a2a2a; border-left:4px solid {color}; border-radius:8px; padding:10px 16px; margin-bottom:8px; font-family:Nunito,sans-serif; color:#ddd; font-size:0.9rem;">{icon} {txt}</div>', unsafe_allow_html=True)

    elif clave_ingresada:
        st.error("❌ Clave incorrecta")

# ═════════════════════════════════════════════
# LOGÍSTICA
# ═════════════════════════════════════════════

elif rol == "Logística":
    if clave_ingresada == "Logistica123**":
        header("🚚 Logística y Distribución", "Control de entregas y rutas optimizadas")

        domicilios  = [p for p in st.session_state.pedidos if p["tipo"] == "Domicilio"]
        total       = len(domicilios)
        despachados = len([p for p in domicilios if p["estado"] == "despachado"])
        tiempo_total = sum((p["fin"] - p["inicio"]) for p in domicilios if "fin" in p)
        tiempo_prom  = round(tiempo_total / despachados, 2) if despachados > 0 else 0
        eficiencia   = round((despachados / total * 100) if total > 0 else 0, 1)

        c1, c2, c3 = st.columns(3)
        with c1: kpi("📦", total, "Domicilios totales")
        with c2: kpi("⏱️", f"{tiempo_prom}s", "Tiempo promedio")
        with c3: kpi("📈", f"{eficiencia}%", "Eficiencia")

        st.markdown("<br>", unsafe_allow_html=True)

        if eficiencia > 80:
            st.markdown('<span class="badge-success">✅ Sistema logístico eficiente</span>', unsafe_allow_html=True)
        elif eficiencia > 50:
            st.markdown('<span class="badge-warning">⚠️ Eficiencia media — revisar procesos</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-danger">❌ Baja eficiencia — acción requerida</span>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_m, col_r = st.columns(2)
        with col_m:
            st.markdown("**📍 Mapa de entregas**")
            if domicilios:
                df_clientes = pd.DataFrame(domicilios).rename(columns={"lat": "latitude", "lon": "longitude"})
                df_rest     = pd.DataFrame([{"latitude": LAT_RESTAURANTE, "longitude": LON_RESTAURANTE}])
                st.map(pd.concat([df_rest, df_clientes]))
            else:
                st.info("No hay domicilios registrados aún.")
        with col_r:
            st.markdown("**🛣️ Rutas estimadas**")
            if domicilios:
                rutas = [{"Cliente": p["cliente"],
                          "Dist. km": round(math.sqrt((p["lat"]-LAT_RESTAURANTE)**2+(p["lon"]-LON_RESTAURANTE)**2)*111, 2),
                          "Tiempo (min)": round(math.sqrt((p["lat"]-LAT_RESTAURANTE)**2+(p["lon"]-LON_RESTAURANTE)**2)*111*3, 1)}
                         for p in domicilios]
                st.dataframe(pd.DataFrame(rutas), use_container_width=True)
            else:
                st.info("No hay rutas calculadas.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**🚀 Recomendaciones operativas**")
        recomendaciones = [
            ("✔", "Agrupar pedidos por zona geográfica"),
            ("✔", "Optimizar rutas con menor distancia acumulada"),
            ("✔", "Reducir tiempos de despacho en cocina"),
            ("✔", "Incorporar más repartidores en horas pico"),
        ]
        cols = st.columns(2)
        for i, (icon, txt) in enumerate(recomendaciones):
            with cols[i % 2]:
                st.markdown(f'<div style="background:#2a2a2a; border-left:4px solid #ff6600; border-radius:8px; padding:10px 16px; margin-bottom:10px; font-family:Nunito,sans-serif; color:#ddd; font-size:0.9rem;">{icon} {txt}</div>', unsafe_allow_html=True)

    elif clave_ingresada:
        st.error("❌ Clave incorrecta")

# ═════════════════════════════════════════════
# EXPERIENCIA CLIENTE
# ═════════════════════════════════════════════

elif rol == "Experiencia":
    if clave_ingresada == "Cliente123**":
        header("⭐ Experiencia del Cliente", "Métricas de satisfacción y retroalimentación")

        if st.session_state.encuestas:
            df = pd.DataFrame(st.session_state.encuestas)
            promedio = df["calificacion"].mean()

            c1, c2, c3 = st.columns(3)
            with c1: kpi("⭐", round(promedio, 2), "Satisfacción promedio")
            with c2: kpi("📋", len(df), "Encuestas totales")
            with c3: kpi("😊", f"{round(len(df[df['calificacion']>=4])/len(df)*100,1)}%", "Clientes satisfechos")

            st.markdown("<br>", unsafe_allow_html=True)

            if promedio >= 4:
                st.markdown('<span class="badge-success">🌟 Excelente servicio — Clientes muy satisfechos</span>', unsafe_allow_html=True)
            elif promedio >= 3:
                st.markdown('<span class="badge-warning">⚠️ Servicio aceptable — Margen de mejora</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-danger">❌ Servicio deficiente — Atención urgente</span>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_g, col_c = st.columns(2)
            with col_g:
                st.markdown("**Distribución de calificaciones**")
                dist = df["calificacion"].value_counts().sort_index()
                st.pyplot(make_chart([str(k) for k in dist.index], list(dist.values), color="#ffe066"))
            with col_c:
                st.markdown("**💬 Comentarios recientes**")
                for _, row in df.tail(5).iterrows():
                    stars = "⭐" * int(row["calificacion"])
                    st.markdown(f'<div style="background:#2a2a2a; border-radius:10px; padding:12px 16px; margin-bottom:8px; font-family:Nunito,sans-serif;"><span style="color:#ffe066; font-weight:800;">{row["cliente"]}</span><span style="float:right; font-size:0.8rem;">{stars}</span><p style="color:#aaa; font-size:0.85rem; margin:4px 0 0;">{row["comentario"]}</p></div>', unsafe_allow_html=True)
        else:
            st.info("📋 No hay encuestas registradas aún.")

    elif clave_ingresada:
        st.error("❌ Clave incorrecta")

# ═════════════════════════════════════════════
# COLABORADOR
# ═════════════════════════════════════════════

elif rol == "Colaborador":
    if st.session_state.empleados.get(nombre_colab) == clave_ingresada and clave_ingresada:

        with st.expander("🗓️ Mi horario semanal", expanded=False):
            dias_semana = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
            horario = {dia: "—" for dia in dias_semana}
            for t in st.session_state.turnos:
                if t["empleado"] == nombre_colab:
                    horario[t["dia"]] = f"{t['horas']}h"
            st.table(pd.DataFrame([horario]))

        if area_colab == "Caja":
            header("🧾 Registro de Pedidos", "Nueva orden de cliente")
            c1, c2 = st.columns(2)
            with c1:
                cliente = st.text_input("Nombre del cliente")
                tipo    = st.selectbox("Tipo de pedido", ["Mesa", "Domicilio"])
            with c2:
                if tipo == "Mesa":
                    mesa = st.number_input("Número de mesa", 1, 20)
                    direccion = ""
                else:
                    direccion = st.text_input("Dirección de entrega")
                    mesa = ""
            if st.button("➕ Registrar pedido"):
                if cliente:
                    st.session_state.pedidos.append({
                        "cliente": cliente, "tipo": tipo, "direccion": direccion, "mesa": mesa,
                        "estado": "pendiente", "inicio": time.time(),
                        "lat": LAT_RESTAURANTE + (0.01 * (len(st.session_state.pedidos) % 5)),
                        "lon": LON_RESTAURANTE  + (0.01 * (len(st.session_state.pedidos) % 5))
                    })
                    st.success(f"✅ Pedido de {cliente} registrado correctamente")
                else:
                    st.warning("Ingresa el nombre del cliente.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**📋 Cola de pedidos activa**")
            if st.session_state.pedidos:
                st.dataframe(pd.DataFrame(st.session_state.pedidos)[["cliente","tipo","mesa","direccion","estado"]], use_container_width=True)
            else:
                st.info("No hay pedidos registrados.")

        elif area_colab == "Cocina":
            header("👨‍🍳 Cocina", "Pedidos en espera de despacho")
            pendientes = [(i, p) for i, p in enumerate(st.session_state.pedidos) if p["estado"] == "pendiente"]
            if pendientes:
                for i, p in pendientes:
                    col_info, col_btn = st.columns([4, 1])
                    with col_info:
                        tag     = "🪑 Mesa" if p["tipo"] == "Mesa" else "🛵 Domicilio"
                        detalle = f"Mesa {int(p['mesa'])}" if p["tipo"] == "Mesa" else p["direccion"]
                        st.markdown(f'<div class="pedido-card"><h4>👤 {p["cliente"]}</h4><p>{tag} · {detalle}</p></div>', unsafe_allow_html=True)
                    with col_btn:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("✅ Despachar", key=f"desp_{i}"):
                            st.session_state.pedidos[i]["estado"] = "despachado"
                            st.session_state.pedidos[i]["fin"]    = time.time()
                            st.success(f"Pedido de {p['cliente']} despachado")
                            st.rerun()
            else:
                st.success("🎉 No hay pedidos pendientes — ¡Todo al día!")

        elif area_colab == "Inventario":
            header("📦 Inventario", "Control de stock de productos")
            c1, c2 = st.columns(2)
            with c1:
                producto = st.selectbox("Producto", list(st.session_state.inventario.keys()))
                cantidad = st.number_input("Cantidad a agregar", 1, 100)
                if st.button("📥 Actualizar inventario"):
                    st.session_state.inventario[producto] += cantidad
                    st.success(f"✅ Se agregaron {cantidad} unidades de {producto}")
            with c2:
                st.markdown("**Stock actual**")
                df_inv = pd.DataFrame(list(st.session_state.inventario.items()), columns=["Producto", "Stock"])
                def color_stock(val):
                    if val < 20:  return "color: #e60000; font-weight: bold"
                    elif val < 35: return "color: #ff9900; font-weight: bold"
                    return "color: #00cc44"
                st.dataframe(df_inv.style.applymap(color_stock, subset=["Stock"]), use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.pyplot(make_chart(list(st.session_state.inventario.keys()), list(st.session_state.inventario.values()), color="#ff6600"))

        elif area_colab == "Encuesta":
            header("📝 Encuesta de Satisfacción", "Registro de feedback del cliente")
            c1, c2 = st.columns(2)
            with c1:
                nombre_cliente = st.text_input("Nombre del cliente")
                calificacion   = st.slider("Calificación del servicio", 1, 5, 3)
                st.markdown(f"<span style='font-size:1.5rem;'>{'⭐' * calificacion}</span>", unsafe_allow_html=True)
            with c2:
                comentario = st.text_area("Comentario del cliente", height=120)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Guardar encuesta"):
                    if nombre_cliente:
                        st.session_state.encuestas.append({"cliente": nombre_cliente, "calificacion": calificacion, "comentario": comentario})
                        st.success("✅ Encuesta registrada correctamente")
                    else:
                        st.warning("Ingresa el nombre del cliente.")

    elif clave_ingresada:
        st.error("❌ Clave incorrecta o usuario incorrecto")
