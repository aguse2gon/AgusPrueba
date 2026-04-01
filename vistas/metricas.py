import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.mock_data import get_metricas_df, get_clientes_df

def show(cliente_id=None):
    st.markdown("""
    <div style='margin-bottom:28px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>Métricas de Campañas</h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>Análisis de rendimiento y KPIs</p>
    </div>
    """, unsafe_allow_html=True)

    clientes_df = get_clientes_df()

    # Si viene de portal cliente
    if cliente_id:
        cli_sel_id = cliente_id
        cli_nombre = clientes_df[clientes_df["id"] == cliente_id]["nombre"].values[0]
    else:
        col_cli, _ = st.columns([2,3])
        with col_cli:
            cli_opt   = clientes_df["nombre"].tolist()
            cli_sel   = st.selectbox("Seleccioná un cliente", cli_opt)
            cli_row   = clientes_df[clientes_df["nombre"] == cli_sel].iloc[0]
            cli_sel_id = cli_row["id"]
            cli_nombre = cli_sel

    df = get_metricas_df(cli_sel_id)

    if df.empty:
        st.warning("No hay datos de métricas para este cliente.")
        return

    # ── KPIs ─────────────────────────────────────────────────────
    total_imp  = df["impresiones"].sum()
    total_cl   = df["clics"].sum()
    total_conv = df["conversiones"].sum()
    avg_ctr    = df["ctr"].mean()
    avg_roas   = df["roas"].mean()
    total_inv  = df["gasto"].sum()

    st.markdown(f"<div style='font-size:15px;font-weight:500;color:#9a9b9f;margin-bottom:16px;'>📊 {cli_nombre}</div>",
                unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.metric("Impresiones",  f"{total_imp:,}")
    with c2: st.metric("Clics",        f"{total_cl:,}")
    with c3: st.metric("Conversiones", f"{total_conv:,}")
    with c4: st.metric("CTR prom.",    f"{avg_ctr:.1f}%")
    with c5: st.metric("ROAS prom.",   f"{avg_roas:.1f}×")
    with c6: st.metric("Inversión",    f"${total_inv:,.0f}")

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── Gráficos ─────────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### CTR por mes")
        fig = go.Figure(go.Bar(
            x=df["mes"], y=df["ctr"],
            marker_color="#c8f135", text=df["ctr"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside", textfont=dict(color="#c8f135", size=12)
        ))
        fig.update_layout(
            plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
            font=dict(color="#9a9b9f",size=12),
            margin=dict(l=0,r=0,t=10,b=0), height=260,
            xaxis=dict(gridcolor="#2a2d3a"), yaxis=dict(gridcolor="#2a2d3a"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### ROAS por mes")
        fig2 = go.Figure(go.Scatter(
            x=df["mes"], y=df["roas"],
            mode="lines+markers+text",
            line=dict(color="#9b7eff", width=2.5),
            marker=dict(size=8, color="#9b7eff"),
            text=df["roas"].apply(lambda x: f"{x:.1f}×"),
            textposition="top center",
            textfont=dict(color="#9b7eff", size=12),
            fill="tozeroy", fillcolor="rgba(155,126,255,0.08)"
        ))
        fig2.update_layout(
            plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
            font=dict(color="#9a9b9f",size=12),
            margin=dict(l=0,r=0,t=10,b=0), height=260,
            xaxis=dict(gridcolor="#2a2d3a"), yaxis=dict(gridcolor="#2a2d3a"),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Embudo de conversión ─────────────────────────────────────
    st.markdown("#### 🎯 Embudo de conversión (total período)")
    etapas = ["Impresiones","Clics","Conversiones"]
    vals   = [total_imp, total_cl, total_conv]
    fig3 = go.Figure(go.Funnel(
        y=etapas, x=vals,
        textinfo="value+percent initial",
        marker_color=["#5c9dff","#c8f135","#3ddbb8"],
        textfont=dict(color="#0e0f14", size=13, family="DM Sans")
    ))
    fig3.update_layout(
        plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
        font=dict(color="#9a9b9f", size=12),
        margin=dict(l=0,r=0,t=10,b=0), height=220
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── Tabla detallada ──────────────────────────────────────────
    st.markdown("#### 📋 Detalle mensual")
    df_display = df[["mes","impresiones","clics","conversiones","ctr","cpc","roas","gasto"]].copy()
    df_display.columns = ["Mes","Impresiones","Clics","Conversiones","CTR %","CPC $","ROAS ×","Gasto $"]
    st.dataframe(
        df_display.style.format({
            "Impresiones": "{:,}","Clics":"{:,}","Conversiones":"{:,}",
            "CTR %":"{:.1f}","CPC $":"${:.2f}","ROAS ×":"{:.1f}","Gasto $":"${:,.0f}"
        }),
        use_container_width=True, hide_index=True
    )
