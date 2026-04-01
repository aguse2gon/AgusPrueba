import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.mock_data import (get_clientes_df, get_proyectos_df,
                             get_metricas_df, ESTADO_COLOR)

def show():
    st.markdown("""
    <div style='margin-bottom:28px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>
            Dashboard <span style='color:#c8f135;'>⚡</span>
        </h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>
            Resumen general · Consultify Marketing
        </p>
    </div>
    """, unsafe_allow_html=True)

    clientes_df  = get_clientes_df()
    proyectos_df = get_proyectos_df()
    metricas_df  = get_metricas_df()

    # ── KPIs principales ────────────────────────────────────────
    activos     = len(clientes_df[clientes_df["estado"] == "Activo"])
    proyectos_a = len(proyectos_df[proyectos_df["estado"] == "En curso"])
    mrr         = clientes_df[clientes_df["estado"] == "Activo"]["valor_mensual"].sum()
    total_gasto = metricas_df["gasto"].sum()
    total_conv  = metricas_df["conversiones"].sum()

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.metric("Clientes activos",    activos,    "+2 este mes")
    with c2:
        st.metric("Proyectos en curso",  proyectos_a, "↑ 1 nuevo")
    with c3:
        st.metric("MRR",                 f"${mrr:,}", "+12% vs mes ant.")
    with c4:
        st.metric("Conversiones totales", total_conv, "+18% vs mes ant.")

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ── Gráfico de inversión mensual + Proyectos ─────────────────
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown("#### 📈 Inversión & Conversiones por mes")
        mes_df = metricas_df.groupby("mes").agg(
            gasto=("gasto","sum"),
            conversiones=("conversiones","sum")
        ).reset_index()
        orden = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
        mes_df["mes"] = pd.Categorical(mes_df["mes"], categories=orden, ordered=True)
        mes_df = mes_df.sort_values("mes")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mes_df["mes"], y=mes_df["gasto"],
            name="Inversión ($)", marker_color="#c8f135", opacity=.85
        ))
        fig.add_trace(go.Scatter(
            x=mes_df["mes"], y=mes_df["conversiones"]*10,
            name="Conversiones (×10)", line=dict(color="#5c9dff", width=2.5),
            mode="lines+markers", marker=dict(size=7)
        ))
        fig.update_layout(
            plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
            font=dict(color="#9a9b9f", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11)),
            margin=dict(l=0,r=0,t=30,b=0), height=300,
            xaxis=dict(gridcolor="#2a2d3a", color="#9a9b9f"),
            yaxis=dict(gridcolor="#2a2d3a", color="#9a9b9f"),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("#### 📁 Estado de proyectos")
        estado_counts = proyectos_df["estado"].value_counts().reset_index()
        estado_counts.columns = ["estado","count"]
        colors = [ESTADO_COLOR.get(e,"#5c5d63") for e in estado_counts["estado"]]
        fig2 = go.Figure(go.Pie(
            labels=estado_counts["estado"],
            values=estado_counts["count"],
            marker_colors=colors,
            hole=0.6,
            textinfo="label+percent",
            textfont=dict(size=12, color="#f0f0ec"),
        ))
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9a9b9f"),
            showlegend=False,
            margin=dict(l=0,r=0,t=30,b=0), height=300,
            annotations=[dict(text="Proyectos", x=0.5, y=0.5,
                              font=dict(size=13,color="#9a9b9f"), showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tabla de clientes activos ────────────────────────────────
    st.markdown("#### 👥 Clientes activos")
    activos_df = clientes_df[clientes_df["estado"] == "Activo"].copy()

    for _, row in activos_df.iterrows():
        proy = proyectos_df[proyectos_df["cliente_id"] == row["id"]]
        n_proy = len(proy[proy["estado"] == "En curso"])
        met    = get_metricas_df(row["id"])
        avg_roas = met["roas"].mean() if len(met) else 0

        color = ESTADO_COLOR.get(row["estado"], "#5c5d63")
        st.markdown(f"""
        <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:12px;
                    padding:14px 18px;margin-bottom:10px;display:flex;
                    align-items:center;justify-content:space-between;'>
            <div style='display:flex;align-items:center;gap:14px;'>
                <div style='font-size:28px;'>{row['avatar']}</div>
                <div>
                    <div style='font-size:14px;font-weight:600;color:#f0f0ec;'>{row['nombre']}</div>
                    <div style='font-size:12px;color:#9a9b9f;'>{row['industria']} · {row['contacto']}</div>
                </div>
            </div>
            <div style='display:flex;gap:40px;align-items:center;'>
                <div style='text-align:center;'>
                    <div style='font-size:11px;color:#5c5d63;'>MRR</div>
                    <div style='font-size:15px;font-weight:600;color:#f0f0ec;'>${row['valor_mensual']:,}</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:11px;color:#5c5d63;'>Proyectos</div>
                    <div style='font-size:15px;font-weight:600;color:#f0f0ec;'>{n_proy}</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:11px;color:#5c5d63;'>ROAS prom.</div>
                    <div style='font-size:15px;font-weight:600;color:#c8f135;'>{avg_roas:.1f}×</div>
                </div>
                <div style='background:{color}22;color:{color};border:1px solid {color}44;
                            border-radius:20px;padding:4px 12px;font-size:12px;font-weight:500;'>
                    {row['estado']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
