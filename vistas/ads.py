"""
vistas/ads.py
Panel de Meta Ads + Google Ads
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.ads_connector import (
    get_combined_insights, get_combined_campaigns,
    get_meta_campaigns, get_google_campaigns,
    get_meta_insights, get_google_insights,
    create_meta_campaign, create_google_campaign,
    get_cuentas, modo_simulacion,
)
from data.database import get_clientes_df

ESTADO_COLOR = {
    "ACTIVE":   "#c8f135", "ENABLED": "#c8f135",
    "PAUSED":   "#ffa94d",
    "ARCHIVED": "#5c5d63", "REMOVED": "#ff5c5c",
}
OBJETIVO_ICON = {
    "BRAND_AWARENESS":"🎯","CONVERSIONS":"💰","REACH":"📡",
    "LEAD_GENERATION":"🧲","APP_INSTALLS":"📱","ENGAGEMENT":"❤️",
    "SEARCH":"🔍","DISPLAY":"🖼️","SHOPPING":"🛒",
    "VIDEO":"🎬","PERFORMANCE_MAX":"⚡",
}

def show(cliente_id_forzado=None):
    st.markdown("""
    <div style='margin-bottom:24px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>
            Gestión de Ads
        </h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>
            Meta Ads · Google Ads — métricas y campañas
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Badge modo simulación
    if modo_simulacion():
        st.markdown("""
        <div style='background:#ffa94d22;border:1px solid #ffa94d44;border-radius:8px;
                    padding:10px 16px;margin-bottom:20px;font-size:13px;color:#ffa94d;
                    display:flex;align-items:center;gap:8px;'>
            ⚠️ <strong>Modo simulación</strong> — datos de prueba.
            Completá <code>data/config.py</code> para conectar APIs reales.
        </div>
        """, unsafe_allow_html=True)

    # ── Selector de cliente ───────────────────────────────────────
    clientes_df = get_clientes_df()
    if cliente_id_forzado:
        cliente_id = cliente_id_forzado
        cli_nombre = clientes_df[clientes_df["id"] == cliente_id]["nombre"].values[0]
    else:
        col_cli, col_days, _ = st.columns([2, 1, 2])
        with col_cli:
            cli_sel    = st.selectbox("Cliente", clientes_df["nombre"].tolist())
            cli_row    = clientes_df[clientes_df["nombre"] == cli_sel].iloc[0]
            cliente_id = cli_row["id"]
            cli_nombre = cli_sel
        with col_days:
            days = st.selectbox("Período", [7, 14, 30, 60, 90], index=2,
                                format_func=lambda x: f"Últimos {x} días")

    if not cliente_id_forzado:
        pass
    else:
        days = 30

    cuentas    = get_cuentas(cliente_id)
    meta_id    = cuentas["meta"]
    google_id  = cuentas["google"]

    # ── Tabs ──────────────────────────────────────────────────────
    tab_overview, tab_meta, tab_google, tab_crear = st.tabs([
        "📊 Overview", "📘 Meta Ads", "🔵 Google Ads", "➕ Nueva campaña"
    ])

    # ════════════════════════════════════════════════════════════
    with tab_overview:
        combined = get_combined_insights(meta_id, google_id, days)

        if combined.empty:
            st.warning("No hay datos disponibles.")
        else:
            # KPIs totales
            tot_imp  = combined["impresiones"].sum()
            tot_cl   = combined["clics"].sum()
            tot_conv = combined["conversiones"].sum()
            tot_gasto = combined["gasto"].sum()
            avg_ctr  = combined["ctr"].mean()
            avg_roas = combined["roas"].mean() if "roas" in combined.columns else 0

            c1,c2,c3,c4,c5,c6 = st.columns(6)
            with c1: st.metric("Impresiones",   f"{tot_imp:,}")
            with c2: st.metric("Clics",         f"{tot_cl:,}")
            with c3: st.metric("Conversiones",  f"{tot_conv:,}")
            with c4: st.metric("Inversión",     f"${tot_gasto:,.0f}")
            with c5: st.metric("CTR prom.",     f"{avg_ctr:.2f}%")
            with c6: st.metric("ROAS prom.",    f"{avg_roas:.1f}×")

            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

            # Gráfico comparativo por plataforma
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown("#### Gasto diario por plataforma")
                fig = px.line(
                    combined, x="fecha", y="gasto", color="plataforma",
                    color_discrete_map={"Meta":"#1877F2","Google":"#c8f135"},
                    markers=True,
                )
                fig.update_layout(
                    plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
                    font=dict(color="#9a9b9f", size=12),
                    legend=dict(orientation="h", y=1.1),
                    margin=dict(l=0,r=0,t=30,b=0), height=280,
                    xaxis=dict(gridcolor="#2a2d3a"),
                    yaxis=dict(gridcolor="#2a2d3a"),
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_r:
                st.markdown("#### Inversión total por plataforma")
                por_plat = combined.groupby("plataforma").agg(
                    gasto=("gasto","sum"),
                    conversiones=("conversiones","sum"),
                ).reset_index()
                fig2 = go.Figure(go.Bar(
                    x=por_plat["plataforma"],
                    y=por_plat["gasto"],
                    marker_color=["#1877F2","#c8f135"],
                    text=por_plat["gasto"].apply(lambda x: f"${x:,.0f}"),
                    textposition="outside",
                    textfont=dict(color="#f0f0ec", size=12),
                ))
                fig2.update_layout(
                    plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
                    font=dict(color="#9a9b9f", size=12),
                    margin=dict(l=0,r=0,t=30,b=0), height=280,
                    xaxis=dict(gridcolor="#2a2d3a"),
                    yaxis=dict(gridcolor="#2a2d3a"),
                    showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True)

            # Conversiones acumuladas
            st.markdown("#### Conversiones acumuladas")
            combined_sorted = combined.sort_values("fecha")
            combined_sorted["conv_acum"] = combined_sorted.groupby("plataforma")["conversiones"].cumsum()
            fig3 = px.area(
                combined_sorted, x="fecha", y="conv_acum", color="plataforma",
                color_discrete_map={"Meta":"#1877F2","Google":"#34A853"},
            )
            fig3.update_layout(
                plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
                font=dict(color="#9a9b9f", size=12),
                legend=dict(orientation="h", y=1.05),
                margin=dict(l=0,r=0,t=30,b=0), height=240,
                xaxis=dict(gridcolor="#2a2d3a"),
                yaxis=dict(gridcolor="#2a2d3a"),
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ════════════════════════════════════════════════════════════
    with tab_meta:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:16px;'>
            <div style='width:32px;height:32px;background:#1877F2;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:16px;'>f</div>
            <div>
                <div style='font-size:15px;font-weight:600;color:#f0f0ec;'>Meta Ads</div>
                <div style='font-size:12px;color:#9a9b9f;'>Cuenta: {meta_id}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        meta_camps = get_meta_campaigns(meta_id)
        meta_ins   = get_meta_insights(meta_id, days)

        if not meta_camps.empty and "error" not in meta_camps.columns:
            st.markdown("##### Campañas activas")
            for _, c in meta_camps.iterrows():
                color = ESTADO_COLOR.get(c["estado"], "#5c5d63")
                icon  = OBJETIVO_ICON.get(c.get("objetivo",""), "🎯")
                st.markdown(f"""
                <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:10px;
                            padding:14px 18px;margin-bottom:8px;
                            display:flex;justify-content:space-between;align-items:center;'>
                    <div style='display:flex;align-items:center;gap:12px;'>
                        <div style='font-size:22px;'>{icon}</div>
                        <div>
                            <div style='font-size:14px;font-weight:500;color:#f0f0ec;'>{c['nombre']}</div>
                            <div style='font-size:12px;color:#9a9b9f;'>{c.get('objetivo','')} · Presupuesto diario: ${c['presupuesto']:.2f}</div>
                        </div>
                    </div>
                    <span style='background:{color}22;color:{color};border:1px solid {color}44;
                                 border-radius:20px;padding:4px 12px;font-size:12px;'>{c['estado']}</span>
                </div>
                """, unsafe_allow_html=True)

        if not meta_ins.empty and "error" not in meta_ins.columns:
            st.markdown("##### Métricas diarias")
            fig = go.Figure()
            fig.add_trace(go.Bar(x=meta_ins["fecha"], y=meta_ins["gasto"],
                                  name="Gasto", marker_color="#1877F2", opacity=.8))
            fig.add_trace(go.Scatter(x=meta_ins["fecha"], y=meta_ins["clics"],
                                      name="Clics", line=dict(color="#c8f135", width=2),
                                      mode="lines", yaxis="y2"))
            fig.update_layout(
                plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
                font=dict(color="#9a9b9f", size=11),
                margin=dict(l=0,r=0,t=20,b=0), height=260,
                legend=dict(orientation="h", y=1.1),
                xaxis=dict(gridcolor="#2a2d3a"),
                yaxis=dict(gridcolor="#2a2d3a", title="Gasto $"),
                yaxis2=dict(overlaying="y", side="right", gridcolor="#2a2d3a", title="Clics"),
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True)

    # ════════════════════════════════════════════════════════════
    with tab_google:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:16px;'>
            <div style='width:32px;height:32px;background:#34A853;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:16px;'>G</div>
            <div>
                <div style='font-size:15px;font-weight:600;color:#f0f0ec;'>Google Ads</div>
                <div style='font-size:12px;color:#9a9b9f;'>Customer ID: {google_id}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        google_camps = get_google_campaigns(google_id)
        google_ins   = get_google_insights(google_id, days)

        if not google_camps.empty and "error" not in google_camps.columns:
            st.markdown("##### Campañas activas")
            for _, c in google_camps.iterrows():
                color = ESTADO_COLOR.get(c["estado"], "#5c5d63")
                icon  = OBJETIVO_ICON.get(c.get("tipo",""), "🔍")
                st.markdown(f"""
                <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:10px;
                            padding:14px 18px;margin-bottom:8px;
                            display:flex;justify-content:space-between;align-items:center;'>
                    <div style='display:flex;align-items:center;gap:12px;'>
                        <div style='font-size:22px;'>{icon}</div>
                        <div>
                            <div style='font-size:14px;font-weight:500;color:#f0f0ec;'>{c['nombre']}</div>
                            <div style='font-size:12px;color:#9a9b9f;'>{c.get('tipo','')} · Presupuesto diario: ${c['presupuesto']:.2f}</div>
                        </div>
                    </div>
                    <span style='background:{color}22;color:{color};border:1px solid {color}44;
                                 border-radius:20px;padding:4px 12px;font-size:12px;'>{c['estado']}</span>
                </div>
                """, unsafe_allow_html=True)

        if not google_ins.empty and "error" not in google_ins.columns:
            st.markdown("##### Métricas diarias")
            fig = go.Figure()
            fig.add_trace(go.Bar(x=google_ins["fecha"], y=google_ins["gasto"],
                                  name="Gasto", marker_color="#34A853", opacity=.8))
            fig.add_trace(go.Scatter(x=google_ins["fecha"], y=google_ins["clics"],
                                      name="Clics", line=dict(color="#c8f135", width=2),
                                      mode="lines", yaxis="y2"))
            fig.update_layout(
                plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
                font=dict(color="#9a9b9f", size=11),
                margin=dict(l=0,r=0,t=20,b=0), height=260,
                legend=dict(orientation="h", y=1.1),
                xaxis=dict(gridcolor="#2a2d3a"),
                yaxis=dict(gridcolor="#2a2d3a", title="Gasto $"),
                yaxis2=dict(overlaying="y", side="right", gridcolor="#2a2d3a", title="Clics"),
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True)

    # ════════════════════════════════════════════════════════════
    with tab_crear:
        st.markdown("#### Crear nueva campaña")
        plataforma = st.radio("Plataforma", ["Meta Ads", "Google Ads"], horizontal=True)

        with st.form("form_nueva_campana"):
            c1, c2 = st.columns(2)
            with c1:
                nc_nombre = st.text_input("Nombre de la campaña")
                nc_ppto   = st.number_input("Presupuesto diario ($)", min_value=1.0,
                                             value=50.0, step=5.0)
            with c2:
                if plataforma == "Meta Ads":
                    nc_objetivo = st.selectbox("Objetivo", [
                        "CONVERSIONS","BRAND_AWARENESS","REACH",
                        "LEAD_GENERATION","APP_INSTALLS","ENGAGEMENT"
                    ])
                else:
                    nc_objetivo = st.selectbox("Tipo de campaña", [
                        "SEARCH","DISPLAY","SHOPPING","VIDEO","PERFORMANCE_MAX"
                    ])
                nc_notas = st.text_area("Notas internas", height=80)

            submitted = st.form_submit_button("🚀 Crear campaña", use_container_width=True)
            if submitted:
                if not nc_nombre:
                    st.error("Ingresá un nombre para la campaña.")
                else:
                    with st.spinner("Creando campaña..."):
                        if plataforma == "Meta Ads":
                            result = create_meta_campaign(meta_id, nc_nombre,
                                                          nc_objetivo, nc_ppto)
                        else:
                            result = create_google_campaign(google_id, nc_nombre,
                                                            nc_objetivo, nc_ppto)
                    if result.get("ok"):
                        st.success(f"✅ Campaña **{nc_nombre}** creada correctamente.")
                        if result.get("nota"):
                            st.info(result["nota"])
                        st.json(result)
                    else:
                        st.error(f"❌ Error: {result.get('error','Error desconocido')}")
