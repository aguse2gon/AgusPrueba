import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Consultify",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

/* ══ SIDEBAR FIJA — no se puede cerrar ══ */
section[data-testid="stSidebar"] {
    transform: translateX(0) !important;
    visibility: visible !important;
    min-width: 240px !important;
    max-width: 240px !important;
    width: 240px !important;
}
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"],
button[aria-label="Collapse sidebar"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

/* ══ Fondo ══ */
.stApp, [data-testid="stAppViewContainer"] { background: #080910 !important; }

/* ══ Sidebar ══ */
section[data-testid="stSidebar"] > div:first-child {
    background: #0d0e16 !important;
    border-right: 1px solid rgba(200,241,53,0.1) !important;
    padding: 0 !important;
}

/* ══ Texto ══ */
p, span, div, label { color: #e8e9f0; }

/* ══ Nav buttons (sidebar) ══ */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #5a5c6e !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 13.5px !important;
    font-weight: 400 !important;
    padding: 9px 14px !important;
    text-align: left !important;
    width: 100% !important;
    transition: all .18s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(200,241,53,0.07) !important;
    color: #e8e9f0 !important;
}

/* ══ Botones principales ══ */
.main .stButton > button {
    background: #c8f135 !important;
    color: #080910 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all .18s ease !important;
    letter-spacing: 0.3px !important;
}
.main .stButton > button:hover {
    background: #d4f54d !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(200,241,53,0.2) !important;
}

/* ══ Inputs ══ */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
textarea {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #e8e9f0 !important;
    font-size: 14px !important;
}
[data-testid="stTextInput"] input:focus, textarea:focus {
    border-color: rgba(200,241,53,0.35) !important;
    box-shadow: 0 0 0 3px rgba(200,241,53,0.07) !important;
}

/* Labels en mayúscula pequeña */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label,
[data-testid="stMultiselect"] label {
    color: #3e4055 !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 500 !important;
}

/* ══ Métricas ══ */
[data-testid="stMetric"] {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    transition: border-color .2s, transform .2s !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(200,241,53,0.18) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricLabel"] {
    color: #3e4055 !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] {
    color: #e8e9f0 !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
}

/* ══ Tabs ══ */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    gap: 2px !important;
}
[data-baseweb="tab"] {
    color: #3e4055 !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 16px !important;
    transition: color .18s !important;
    background: transparent !important;
}
[data-baseweb="tab"]:hover { color: #e8e9f0 !important; }
[aria-selected="true"] {
    color: #c8f135 !important;
    border-bottom: 2px solid #c8f135 !important;
    font-weight: 500 !important;
}

/* ══ Alerts ══ */
[data-testid="stSuccess"] {
    background: rgba(200,241,53,0.07) !important;
    border: 1px solid rgba(200,241,53,0.2) !important;
    border-radius: 10px !important; color: #c8f135 !important;
}
[data-testid="stWarning"] {
    background: rgba(255,169,77,0.07) !important;
    border: 1px solid rgba(255,169,77,0.2) !important;
    border-radius: 10px !important;
}
[data-testid="stError"] {
    background: rgba(255,92,92,0.07) !important;
    border: 1px solid rgba(255,92,92,0.2) !important;
    border-radius: 10px !important;
}
[data-testid="stInfo"] {
    background: rgba(92,157,255,0.07) !important;
    border: 1px solid rgba(92,157,255,0.2) !important;
    border-radius: 10px !important;
}

/* ══ Selectbox — fondo oscuro ══ */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] > div > div > div,
[data-baseweb="select"] > div:first-child,
[data-baseweb="select"] > div {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #e8e9f0 !important;
}
/* Dropdown abierto */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"],
[data-baseweb="menu"] ul {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}
/* Opciones del dropdown */
[data-baseweb="menu"] li,
[role="option"] {
    background: #13141f !important;
    color: #e8e9f0 !important;
}
[data-baseweb="menu"] li:hover,
[role="option"]:hover {
    background: rgba(200,241,53,0.08) !important;
    color: #c8f135 !important;
}
/* Multiselect */
[data-testid="stMultiselect"] > div > div {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}
[data-testid="stMultiselect"] span[data-baseweb="tag"] {
    background: rgba(200,241,53,0.12) !important;
    color: #c8f135 !important;
    border-radius: 6px !important;
}
/* Date input */
[data-testid="stDateInput"] > div > div {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #e8e9f0 !important;
}
/* Number input */
[data-testid="stNumberInput"] > div > div {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}

/* ══ Forms ══ */
[data-testid="stForm"] {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

/* ══ Scrollbar ══ */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-thumb { background: rgba(200,241,53,0.15); border-radius: 2px; }

/* ══ Ocultar Streamlit UI ══ */
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important; visibility: hidden !important;
}

/* ══ Padding contenido ══ */
[data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 32px 40px 48px !important;
    max-width: 1200px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Auto-migrar ───────────────────────────────────────────────────
from data.database import db_exists, get_usuario

# Soporte para Streamlit Cloud secrets
try:
    if st.secrets.get("GMAIL_EMAIL"):
        import data.config as _cfg
        _cfg.GMAIL_CONFIG["email"]    = st.secrets["GMAIL_EMAIL"]
        _cfg.GMAIL_CONFIG["password"] = st.secrets["GMAIL_PASSWORD"]
except Exception:
    pass
if not db_exists():
    with st.spinner("⚡ Iniciando base de datos..."):
        from migrar_datos import migrar
        migrar()
    st.rerun()

# ── Helpers de UI ─────────────────────────────────────────────────
def page_header(titulo: str, subtitulo: str = ""):
    st.markdown(f"""
    <div style='margin-bottom:28px;padding-bottom:20px;
                border-bottom:1px solid rgba(255,255,255,0.05);'>
        <h1 style='font-family:Syne,sans-serif;font-size:26px;font-weight:700;
                   color:#e8e9f0;margin:0;letter-spacing:-0.3px;'>{titulo}</h1>
        {f"<p style='color:#3e4055;font-size:13px;margin-top:5px;'>{subtitulo}</p>" if subtitulo else ""}
    </div>
    """, unsafe_allow_html=True)

# Inyectar en session_state para que los módulos puedan usar page_header
if "page_header" not in st.session_state:
    st.session_state["_ui"] = True

# ── Login ─────────────────────────────────────────────────────────
def login():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("""
        <div style='display:flex;flex-direction:column;align-items:center;
                    padding:60px 0 32px;'>
            <div style='width:54px;height:54px;background:#c8f135;border-radius:14px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:26px;margin-bottom:16px;
                        box-shadow:0 0 40px rgba(200,241,53,0.2);'>⚡</div>
            <h1 style='font-family:Syne,sans-serif;font-size:30px;font-weight:800;
                       color:#e8e9f0;margin:0;letter-spacing:-0.5px;'>Consultify</h1>
            <p style='color:#3e4055;font-size:13px;margin-top:6px;margin-bottom:32px;'>
                Plataforma de Marketing
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email    = st.text_input("Email", placeholder="tu@email.com")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.form_submit_button("Ingresar →", use_container_width=True):
                user = get_usuario(email)
                if user and user["password"] == password:
                    st.session_state.logged_in   = True
                    st.session_state.user_email  = email
                    st.session_state.user_role   = user["role"]
                    st.session_state.user_nombre = user["nombre"]
                    st.session_state.cliente_id  = user.get("cliente_id")
                    st.rerun()
                else:
                    st.error("Email o contraseña incorrectos.")

        st.markdown("""
        <div style='margin-top:16px;padding:14px 16px;background:#13141f;
                    border-radius:11px;border:1px solid rgba(255,255,255,0.05);
                    font-size:12px;'>
            <div style='font-size:10px;color:#3e4055;text-transform:uppercase;
                        letter-spacing:1.2px;font-weight:500;margin-bottom:10px;'>
                Accesos de prueba
            </div>
            <div style='color:#5a5c6e;line-height:2;'>
                🔑 <code style='color:#c8f135;background:rgba(200,241,53,0.08);
                   padding:1px 6px;border-radius:4px;'>admin@consultify.com</code>
                   admin123<br>
                👤 <code style='color:#c8f135;background:rgba(200,241,53,0.08);
                   padding:1px 6px;border-radius:4px;'>maria@consultify.com</code>
                   maria123<br>
                🏢 <code style='color:#c8f135;background:rgba(200,241,53,0.08);
                   padding:1px 6px;border-radius:4px;'>cliente1@empresa.com</code>
                   cliente123
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
def sidebar_nav():
    with st.sidebar:
        role_label = {"admin":"Administrador","interno":"Equipo interno",
                      "cliente":"Cliente"}.get(st.session_state.user_role,"")
        initials   = "".join(w[0].upper() for w in
                             st.session_state.user_nombre.split()[:2])

        st.markdown(f"""
        <div style='padding:22px 18px 16px;
                    border-bottom:1px solid rgba(200,241,53,0.08);margin-bottom:6px;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:18px;'>
                <div style='width:32px;height:32px;background:#c8f135;border-radius:8px;
                            display:flex;align-items:center;justify-content:center;
                            font-size:16px;flex-shrink:0;'>⚡</div>
                <div>
                    <div style='font-family:Syne,sans-serif;font-size:15px;font-weight:700;
                                color:#e8e9f0;'>Consultify</div>
                    <div style='font-size:9px;color:#2a2c38;text-transform:uppercase;
                                letter-spacing:1.5px;'>Marketing</div>
                </div>
            </div>
            <div style='background:#13141f;border-radius:10px;padding:10px 12px;
                        border:1px solid rgba(255,255,255,0.04);
                        display:flex;align-items:center;gap:9px;'>
                <div style='width:30px;height:30px;border-radius:50%;background:#c8f135;
                            display:flex;align-items:center;justify-content:center;
                            font-size:11px;font-weight:700;color:#080910;flex-shrink:0;'>
                    {initials}
                </div>
                <div style='min-width:0;'>
                    <div style='font-size:12.5px;font-weight:500;color:#e8e9f0;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>
                        {st.session_state.user_nombre}
                    </div>
                    <div style='font-size:10px;color:#c8f135;'>{role_label}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        role = st.session_state.user_role
        if role in ("admin","interno"):
            pages = {
                "📊  Dashboard":      "dashboard",
                "👥  Clientes":       "clientes",
                "📁  Proyectos":      "proyectos",
                "📅  Calendario":     "calendario",
                "📈  Métricas":       "metricas",
                "🎯  Ads Manager":    "ads",
                "🔔  Notificaciones": "notificaciones",
            }
            if role == "admin":
                pages["⚙️  Configuración"] = "config"
        else:
            pages = {
                "🏠  Mi Portal":      "portal_cliente",
                "📊  Mis Campañas":   "campanas_cliente",
                "🎯  Mis Ads":        "ads_cliente",
                "📅  Calendario":     "calendario_cliente",
                "📄  Reportes":       "reportes_cliente",
            }

        if "page" not in st.session_state:
            st.session_state.page = list(pages.values())[0]

        st.markdown("""
        <div style='padding:4px 18px 4px;'>
            <span style='font-size:9px;color:#2a2c38;text-transform:uppercase;
                         letter-spacing:1.5px;font-weight:500;'>Menú</span>
        </div>
        """, unsafe_allow_html=True)

        for label, page_key in pages.items():
            is_active = st.session_state.get("page") == page_key
            if is_active:
                st.markdown(f"""
                <div style='margin:1px 10px;background:rgba(200,241,53,0.1);
                            border:1px solid rgba(200,241,53,0.18);
                            border-radius:10px;padding:9px 14px;
                            font-size:13.5px;color:#c8f135;font-weight:500;
                            cursor:default;user-select:none;'>
                    {label}
                </div>
                """, unsafe_allow_html=True)
            else:
                col = st.columns([1])[0]
                with col:
                    if st.button(label, key=f"nav_{page_key}",
                                 use_container_width=True):
                        st.session_state.page = page_key
                        st.rerun()

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🚪  Cerrar sesión", key="logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ── Router ────────────────────────────────────────────────────────
def main():
    if not st.session_state.get("logged_in"):
        login()
        return

    sidebar_nav()
    page = st.session_state.get("page","dashboard")

    if page == "dashboard":
        from vistas import dashboard;            dashboard.show()
    elif page == "clientes":
        from vistas import clientes;             clientes.show()
    elif page == "proyectos":
        from vistas import proyectos;            proyectos.show()
    elif page == "calendario":
        from vistas import calendario;           calendario.show()
    elif page == "metricas":
        from vistas import metricas;             metricas.show()
    elif page == "ads":
        from vistas import ads;                  ads.show()
    elif page == "notificaciones":
        from vistas import notificaciones_panel; notificaciones_panel.show()
    elif page == "portal_cliente":
        from vistas import portal_cliente;       portal_cliente.show()
    elif page == "campanas_cliente":
        from vistas import campanas_cliente;     campanas_cliente.show()
    elif page == "ads_cliente":
        from vistas import ads
        ads.show(cliente_id_forzado=st.session_state.get("cliente_id"))
    elif page == "calendario_cliente":
        from vistas import calendario;           calendario.show(cliente_mode=True)
    elif page == "reportes_cliente":
        from vistas import reportes_cliente;     reportes_cliente.show()
    elif page == "config":
        _config_page()

def _config_page():
    st.markdown("""
    <h1 style='font-family:Syne,sans-serif;font-size:26px;font-weight:700;
               color:#e8e9f0;margin-bottom:6px;'>Configuración</h1>
    <p style='color:#3e4055;font-size:13px;margin-bottom:24px;'>
        Sistema, usuarios y APIs externas
    </p>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["👤 Usuarios","🗄️ Base de datos","🔑 APIs"])
    with tab1:
        from data.database import get_all_usuarios_df
        st.dataframe(get_all_usuarios_df(), use_container_width=True, hide_index=True)
    with tab2:
        from data.database import DB_PATH
        size = os.path.getsize(DB_PATH)/1024 if os.path.exists(DB_PATH) else 0
        st.metric("Tamaño BD", f"{size:.1f} KB")
        st.code(DB_PATH)
        if st.button("🔄 Re-ejecutar migración"):
            from migrar_datos import migrar; migrar()
            st.success("✅ Hecho.")
    with tab3:
        from data.ads_connector import META_REAL, GOOGLE_REAL
        from data.notificaciones import GMAIL_OK
        c1,c2,c3 = st.columns(3)
        with c1:
            st.success("✅ Gmail conectado") if GMAIL_OK else st.warning("⚠️ Gmail sin config")
        with c2:
            st.success("✅ Meta Ads") if META_REAL else st.warning("⚠️ Meta — simulación")
        with c3:
            st.success("✅ Google Ads") if GOOGLE_REAL else st.warning("⚠️ Google — simulación")

if __name__ == "__main__":
    main()
