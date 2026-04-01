import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.mock_data import (get_clientes_df, get_proyectos_df,
                             get_metricas_df, get_contenidos_df, ESTADO_COLOR)

def show():
    cliente_id = st.session_state.get("cliente_id", "C001")
    clientes_df = get_clientes_df()
    row = clientes_df[clientes_df["id"] == cliente_id]
    if row.empty:
        st.error("Cliente no encontrado.")
        return
    cliente = row.iloc[0]

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1d1f28,#252836);border:1px solid #2a2d3a;
                border-radius:16px;padding:28px;margin-bottom:28px;'>
        <div style='display:flex;align-items:center;gap:16px;'>
            <div style='font-size:52px;'>{cliente['avatar']}</div>
            <div>
                <div style='font-size:22px;font-weight:600;color:#f0f0ec;'>{cliente['nombre']}</div>
                <div style='font-size:14px;color:#9a9b9f;margin-top:4px;'>{cliente['industria']} · Cliente desde {cliente['inicio']}</div>
                <div style='margin-top:10px;'>
                    <span style='background:#c8f135;color:#0e0f14;border-radius:20px;
                                 padding:4px 14px;font-size:12px;font-weight:600;'>Portal de Cliente</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs del cliente ─────────────────────────────────────────
    proyectos_df = get_proyectos_df()
    mis_proy     = proyectos_df[proyectos_df["cliente_id"] == cliente_id]
    metricas_df  = get_metricas_df(cliente_id)
    contenidos   = get_contenidos_df(cliente_id)

    n_activos  = len(mis_proy[mis_proy["estado"] == "En curso"])
    total_conv = metricas_df["conversiones"].sum() if len(metricas_df) else 0
    avg_roas   = metricas_df["roas"].mean() if len(metricas_df) else 0
    n_posts    = len(contenidos[contenidos["estado"].isin(["Publicado","Aprobado"])])

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Proyectos activos",  n_activos)
    with c2: st.metric("Conversiones totales", f"{total_conv:,}")
    with c3: st.metric("ROAS promedio",       f"{avg_roas:.1f}×")
    with c4: st.metric("Contenidos aprobados", n_posts)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── Mis proyectos ────────────────────────────────────────────
    st.markdown("#### 📁 Mis proyectos")
    for _, p in mis_proy.iterrows():
        color = ESTADO_COLOR.get(p["estado"], "#5c5d63")
        bar_color = "#c8f135" if p["progreso"] >= 80 else "#5c9dff" if p["progreso"] >= 40 else "#ff9f5c"
        st.markdown(f"""
        <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:12px;
                    padding:16px 20px;margin-bottom:10px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>
                <div>
                    <div style='font-size:15px;font-weight:600;color:#f0f0ec;'>{p['nombre']}</div>
                    <div style='font-size:12px;color:#9a9b9f;'>{p['tipo']} · {p['inicio']} → {p['fin']}</div>
                </div>
                <span style='background:{color}22;color:{color};border:1px solid {color}44;
                             border-radius:20px;padding:4px 12px;font-size:12px;'>{p['estado']}</span>
            </div>
            <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                <span style='font-size:12px;color:#9a9b9f;'>Progreso</span>
                <span style='font-size:12px;font-weight:600;color:{bar_color};'>{p['progreso']}%</span>
            </div>
            <div style='background:#252836;border-radius:4px;height:6px;overflow:hidden;'>
                <div style='width:{p["progreso"]}%;height:100%;background:{bar_color};border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Próximos contenidos ───────────────────────────────────────
    st.markdown("#### 📅 Próximos contenidos")
    proximos = contenidos[contenidos["estado"].isin(["Planificado","En revisión","Aprobado"])].sort_values("fecha")
    if proximos.empty:
        st.info("No hay contenidos planificados próximamente.")
    else:
        from data.mock_data import TIPO_ICON
        for _, ct in proximos.head(5).iterrows():
            col  = ESTADO_COLOR.get(ct["estado"],"#5c5d63")
            icon = TIPO_ICON.get(ct["tipo"],"📌")
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:14px;background:#1d1f28;
                        border:1px solid #2a2d3a;border-radius:10px;padding:12px 16px;margin-bottom:8px;'>
                <div style='font-size:22px;'>{icon}</div>
                <div style='flex:1;'>
                    <div style='font-size:14px;font-weight:500;color:#f0f0ec;'>{ct['titulo']}</div>
                    <div style='font-size:12px;color:#9a9b9f;'>{ct['fecha']} · {ct['tipo']}</div>
                </div>
                <span style='background:{col}22;color:{col};border:1px solid {col}44;
                             border-radius:20px;padding:3px 10px;font-size:11px;'>{ct['estado']}</span>
            </div>
            """, unsafe_allow_html=True)
