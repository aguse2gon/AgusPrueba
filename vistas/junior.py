"""
vistas/junior.py
Panel para perfil Junior — solo proyectos asignados y calendario.
Sin acceso a métricas, clientes ni ads.
"""
import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.database import get_proyectos_df, get_contenidos_df, get_clientes_df
from data.mock_data import ESTADO_COLOR, TIPO_ICON

def show():
    nombre = st.session_state.get("user_nombre","")
    initials = "".join(w[0].upper() for w in nombre.split()[:2])

    st.markdown(f"""
    <div style='margin-bottom:28px;padding-bottom:20px;
                border-bottom:1px solid rgba(255,255,255,0.05);'>
        <div style='display:flex;align-items:center;gap:14px;'>
            <div style='width:44px;height:44px;background:#c8f135;border-radius:12px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:16px;font-weight:700;color:#080910;'>{initials}</div>
            <div>
                <h1 style='font-family:Syne,sans-serif;font-size:22px;font-weight:700;
                           color:#e8e9f0;margin:0;'>Hola, {nombre.split()[0]} 👋</h1>
                <p style='color:#3e4055;font-size:13px;margin:3px 0 0;'>
                    Tus proyectos y calendario del día
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    proyectos_df = get_proyectos_df()
    clientes_df  = get_clientes_df()
    contenidos_df = get_contenidos_df()

    # Filtrar proyectos asignados al usuario
    user_nombre = st.session_state.get("user_nombre","")
    mis_proy = proyectos_df[
        proyectos_df["responsable"].str.contains(user_nombre.split()[0], case=False, na=False)
    ] if not proyectos_df.empty else proyectos_df

    # Si no hay proyectos asignados mostrar todos (modo demo)
    if mis_proy.empty:
        mis_proy = proyectos_df

    clientes_map = dict(zip(clientes_df["id"], clientes_df["nombre"])) if not clientes_df.empty else {}
    avatar_map   = dict(zip(clientes_df["id"], clientes_df["avatar"]))  if not clientes_df.empty else {}

    tab1, tab2 = st.tabs(["📁 Mis proyectos", "📅 Mis contenidos"])

    # ── Proyectos ─────────────────────────────────────────────────
    with tab1:
        activos   = mis_proy[mis_proy["estado"] == "En curso"]
        otros     = mis_proy[mis_proy["estado"] != "En curso"]

        # KPIs rápidos
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Proyectos asignados", len(mis_proy))
        with c2: st.metric("En curso",            len(activos))
        with c3:
            avg_prog = int(activos["progreso"].mean()) if not activos.empty else 0
            st.metric("Progreso promedio", f"{avg_prog}%")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if mis_proy.empty:
            st.info("No tenés proyectos asignados aún.")
        else:
            for _, p in mis_proy.iterrows():
                color      = ESTADO_COLOR.get(p["estado"],"#5c5d63")
                bar_color  = "#c8f135" if p["progreso"]>=80 else "#5c9dff" if p["progreso"]>=40 else "#ff9f5c"
                gasto_pct  = (p["gastado"]/max(p["presupuesto"],1)*100)
                cli_nombre = clientes_map.get(p["cliente_id"],"")
                cli_avatar = avatar_map.get(p["cliente_id"],"🏢")
                gasto_col  = "#ff5c5c" if gasto_pct>90 else "#ffa94d" if gasto_pct>70 else "#3ddbb8"

                st.markdown(f"""
                <div style='background:#13141f;border:1px solid rgba(255,255,255,0.05);
                            border-radius:14px;padding:18px 20px;margin-bottom:12px;'>
                    <div style='display:flex;justify-content:space-between;
                                align-items:flex-start;margin-bottom:14px;'>
                        <div>
                            <div style='font-family:Syne,sans-serif;font-size:15px;
                                        font-weight:600;color:#e8e9f0;'>{p['nombre']}</div>
                            <div style='font-size:12px;color:#3e4055;margin-top:3px;'>
                                {cli_avatar} {cli_nombre} · {p['tipo']}
                            </div>
                        </div>
                        <span style='background:{color}20;color:{color};
                                     border:1px solid {color}40;border-radius:20px;
                                     padding:4px 12px;font-size:11px;white-space:nowrap;'>
                            {p['estado']}
                        </span>
                    </div>
                    <div style='margin-bottom:10px;'>
                        <div style='display:flex;justify-content:space-between;margin-bottom:5px;'>
                            <span style='font-size:11px;color:#3e4055;text-transform:uppercase;
                                         letter-spacing:1px;'>Progreso</span>
                            <span style='font-size:12px;font-weight:600;color:{bar_color};'>
                                {p['progreso']}%</span>
                        </div>
                        <div style='background:#1d1f2e;border-radius:4px;height:5px;'>
                            <div style='width:{p["progreso"]}%;height:100%;
                                        background:{bar_color};border-radius:4px;'></div>
                        </div>
                    </div>
                    <div style='display:flex;gap:20px;font-size:12px;'>
                        <span style='color:#3e4055;'>📅 {p['inicio']} → {p['fin']}</span>
                        <span style='color:{gasto_col};'>
                            💰 ${p['gastado']:,} / ${p['presupuesto']:,}
                            ({gasto_pct:.0f}%)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Contenidos asignados ──────────────────────────────────────
    with tab2:
        import datetime
        today = datetime.date.today()

        if contenidos_df.empty:
            st.info("No hay contenidos en el calendario.")
        else:
            # Filtrar por responsable
            mis_cts = contenidos_df[
                contenidos_df["responsable"].str.contains(
                    user_nombre.split()[0], case=False, na=False)
            ] if not contenidos_df.empty else contenidos_df

            if mis_cts.empty:
                mis_cts = contenidos_df  # modo demo

            # Separar en secciones
            hoy_cts     = mis_cts[mis_cts["fecha"] == today]
            proximos    = mis_cts[(mis_cts["fecha"] > today) &
                                  (mis_cts["fecha"] <= today + datetime.timedelta(days=7))]
            pendientes  = mis_cts[mis_cts["estado"].isin(["En revisión","Borrador"])]

            def render_contenidos(df, titulo):
                if df.empty:
                    return
                st.markdown(f"""
                <div style='font-size:10px;color:#3e4055;text-transform:uppercase;
                            letter-spacing:1.2px;font-weight:500;
                            margin:16px 0 8px;'>{titulo}</div>
                """, unsafe_allow_html=True)
                for _, ct in df.iterrows():
                    c   = ESTADO_COLOR.get(ct["estado"],"#5c5d63")
                    ic  = TIPO_ICON.get(ct["tipo"],"📌")
                    cli = clientes_map.get(ct["cliente_id"],"")
                    st.markdown(f"""
                    <div style='background:#13141f;border:1px solid rgba(255,255,255,0.05);
                                border-left:3px solid {c};border-radius:0 10px 10px 0;
                                padding:12px 16px;margin-bottom:7px;
                                display:flex;justify-content:space-between;align-items:center;'>
                        <div>
                            <div style='font-size:14px;font-weight:500;color:#e8e9f0;'>
                                {ic} {ct['titulo']}
                            </div>
                            <div style='font-size:12px;color:#3e4055;margin-top:3px;'>
                                📅 {ct['fecha']} · {ct['tipo']} · 🏢 {cli}
                            </div>
                        </div>
                        <span style='background:{c}20;color:{c};border:1px solid {c}40;
                                     border-radius:20px;padding:3px 10px;font-size:11px;
                                     white-space:nowrap;margin-left:10px;'>{ct['estado']}</span>
                    </div>
                    """, unsafe_allow_html=True)

            if not hoy_cts.empty:
                render_contenidos(hoy_cts, f"📌 Hoy — {today.strftime('%d/%m/%Y')}")
            if not proximos.empty:
                render_contenidos(proximos, "📅 Próximos 7 días")
            if not pendientes.empty:
                render_contenidos(pendientes, "✏️ Pendientes de revisión / borrador")
            if hoy_cts.empty and proximos.empty and pendientes.empty:
                st.info("No tenés contenidos pendientes. ¡Todo al día! 🎉")
