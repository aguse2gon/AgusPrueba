import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.mock_data import get_proyectos_df, get_clientes_df, ESTADO_COLOR

def show():
    st.markdown("""
    <div style='margin-bottom:28px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>Proyectos</h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>Seguimiento de todos los proyectos activos</p>
    </div>
    """, unsafe_allow_html=True)

    proyectos_df = get_proyectos_df()
    clientes_df  = get_clientes_df()

    # Enriquecer con nombre de cliente
    clientes_map = dict(zip(clientes_df["id"], clientes_df["nombre"]))
    avatar_map   = dict(zip(clientes_df["id"], clientes_df["avatar"]))
    proyectos_df["cliente_nombre"] = proyectos_df["cliente_id"].map(clientes_map)
    proyectos_df["cliente_avatar"] = proyectos_df["cliente_id"].map(avatar_map)
    proyectos_df["pct_gasto"]      = (proyectos_df["gastado"] / proyectos_df["presupuesto"] * 100).round(0)

    # ── Vista tabs ────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["📋 Lista", "➕ Nuevo proyecto"])

    with tab1:
        # Filtros
        col_f1, col_f2 = st.columns([2,1])
        with col_f1:
            cliente_f = st.selectbox("Cliente", ["Todos"] + sorted(clientes_df["nombre"].tolist()))
        with col_f2:
            estado_f = st.selectbox("Estado", ["Todos","En curso","Completado","Pausado"])

        df = proyectos_df.copy()
        if cliente_f != "Todos":
            df = df[df["cliente_nombre"] == cliente_f]
        if estado_f != "Todos":
            df = df[df["estado"] == estado_f]

        # Kanban-style por estado
        for estado in ["En curso","Completado","Pausado"]:
            grupo = df[df["estado"] == estado]
            if grupo.empty:
                continue
            color = ESTADO_COLOR.get(estado,"#5c5d63")
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;margin:20px 0 12px;'>
                <div style='width:10px;height:10px;border-radius:50%;background:{color};'></div>
                <span style='font-size:14px;font-weight:600;color:#f0f0ec;'>{estado}</span>
                <span style='background:{color}22;color:{color};border-radius:20px;
                             padding:2px 10px;font-size:12px;'>{len(grupo)}</span>
            </div>
            """, unsafe_allow_html=True)

            for _, row in grupo.iterrows():
                bar_color = "#c8f135" if row["progreso"] >= 80 else "#5c9dff" if row["progreso"] >= 40 else "#ff9f5c"
                gasto_color = "#ff5c5c" if row["pct_gasto"] > 90 else "#ffa94d" if row["pct_gasto"] > 70 else "#3ddbb8"

                st.markdown(f"""
                <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:12px;
                            padding:16px 20px;margin-bottom:10px;'>
                    <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;'>
                        <div>
                            <div style='font-size:15px;font-weight:600;color:#f0f0ec;'>{row['nombre']}</div>
                            <div style='font-size:12px;color:#9a9b9f;margin-top:2px;'>
                                {row['cliente_avatar']} {row['cliente_nombre']} · {row['tipo']} · 👤 {row['responsable']}
                            </div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='font-size:11px;color:#5c5d63;'>Período</div>
                            <div style='font-size:12px;color:#9a9b9f;'>{row['inicio']} → {row['fin']}</div>
                        </div>
                    </div>
                    <div style='margin-bottom:10px;'>
                        <div style='display:flex;justify-content:space-between;margin-bottom:5px;'>
                            <span style='font-size:12px;color:#9a9b9f;'>Progreso general</span>
                            <span style='font-size:12px;font-weight:600;color:{bar_color};'>{row['progreso']}%</span>
                        </div>
                        <div style='background:#252836;border-radius:4px;height:6px;overflow:hidden;'>
                            <div style='width:{row["progreso"]}%;height:100%;background:{bar_color};
                                        border-radius:4px;transition:width .3s;'></div>
                        </div>
                    </div>
                    <div style='display:flex;gap:24px;'>
                        <div>
                            <span style='font-size:11px;color:#5c5d63;'>Presupuesto</span>
                            <span style='font-size:13px;font-weight:500;color:#f0f0ec;margin-left:8px;'>${row['presupuesto']:,}</span>
                        </div>
                        <div>
                            <span style='font-size:11px;color:#5c5d63;'>Gastado</span>
                            <span style='font-size:13px;font-weight:500;color:{gasto_color};margin-left:8px;'>
                                ${row['gastado']:,} ({row['pct_gasto']:.0f}%)
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        with st.form("nuevo_proyecto"):
            c1, c2 = st.columns(2)
            with c1:
                np_nombre   = st.text_input("Nombre del proyecto")
                np_cliente  = st.selectbox("Cliente", clientes_df["nombre"].tolist())
                np_tipo     = st.selectbox("Tipo", ["Redes Sociales","Performance","Full 360°","Web","Influencers","Branding","Email Marketing"])
                np_resp     = st.selectbox("Responsable", ["María García","Carlos López"])
            with c2:
                np_inicio   = st.date_input("Fecha de inicio")
                np_fin      = st.date_input("Fecha de fin")
                np_ppto     = st.number_input("Presupuesto ($)", min_value=0, step=500)
                np_objetivo = st.text_area("Objetivos", height=100)

            if st.form_submit_button("Crear proyecto", use_container_width=True):
                st.success(f"✅ Proyecto '{np_nombre}' creado correctamente (demo).")
