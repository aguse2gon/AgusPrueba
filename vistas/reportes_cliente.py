import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.mock_data import get_metricas_df, get_proyectos_df, get_clientes_df

def show():
    st.markdown("""
    <div style='margin-bottom:28px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>Mis Reportes</h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>Informes de rendimiento de tus campañas</p>
    </div>
    """, unsafe_allow_html=True)

    cliente_id  = st.session_state.get("cliente_id","C001")
    clientes_df = get_clientes_df()
    cliente     = clientes_df[clientes_df["id"] == cliente_id].iloc[0]
    df          = get_metricas_df(cliente_id)
    proyectos   = get_proyectos_df()
    mis_proy    = proyectos[proyectos["cliente_id"] == cliente_id]

    if df.empty:
        st.warning("No hay datos disponibles aún.")
        return

    # ── Resumen ejecutivo ────────────────────────────────────────
    st.markdown(f"""
    <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:14px;padding:24px;margin-bottom:24px;'>
        <div style='font-size:12px;color:#5c5d63;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;'>Reporte ejecutivo</div>
        <div style='font-size:20px;font-weight:600;color:#f0f0ec;'>{cliente['nombre']}</div>
        <div style='font-size:13px;color:#9a9b9f;margin-top:4px;'>Período acumulado · Todos los proyectos</div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Total invertido",    f"${df['gasto'].sum():,.0f}")
    with c2: st.metric("Conversiones",       f"{df['conversiones'].sum():,}")
    with c3: st.metric("ROAS promedio",      f"{df['roas'].mean():.1f}×")
    with c4: st.metric("Costo por conversión", f"${df['gasto'].sum()/max(df['conversiones'].sum(),1):.2f}")

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── Gráfico de rendimiento ───────────────────────────────────
    st.markdown("#### Rendimiento mensual")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["mes"], y=df["gasto"], name="Inversión ($)",
                         marker_color="#252836", marker_line_color="#c8f135",
                         marker_line_width=1.5))
    fig.add_trace(go.Scatter(x=df["mes"], y=df["conversiones"]*15,
                             name="Conversiones (escala)", mode="lines+markers",
                             line=dict(color="#3ddbb8",width=2.5), marker=dict(size=8)))
    fig.update_layout(
        plot_bgcolor="#1d1f28", paper_bgcolor="#1d1f28",
        font=dict(color="#9a9b9f",size=12),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(size=11)),
        margin=dict(l=0,r=0,t=30,b=0), height=280,
        xaxis=dict(gridcolor="#2a2d3a"), yaxis=dict(gridcolor="#2a2d3a"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Proyectos ────────────────────────────────────────────────
    st.markdown("#### Estado de tus proyectos")
    for _, p in mis_proy.iterrows():
        pct = p["gastado"] / max(p["presupuesto"],1) * 100
        st.markdown(f"""
        <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:10px;
                    padding:14px 18px;margin-bottom:8px;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                <span style='font-size:14px;font-weight:500;color:#f0f0ec;'>{p['nombre']}</span>
                <span style='font-size:13px;color:#9a9b9f;'>{p['tipo']}</span>
            </div>
            <div style='display:flex;gap:24px;font-size:12px;color:#9a9b9f;margin-bottom:8px;'>
                <span>Presupuesto: <b style='color:#f0f0ec;'>${p['presupuesto']:,}</b></span>
                <span>Ejecutado: <b style='color:#c8f135;'>${p['gastado']:,} ({pct:.0f}%)</b></span>
                <span>Progreso: <b style='color:#5c9dff;'>{p['progreso']}%</b></span>
            </div>
            <div style='background:#252836;border-radius:4px;height:5px;'>
                <div style='width:{p["progreso"]}%;height:100%;background:#5c9dff;border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Exportar (demo) ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📥 Exportar reporte")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Descargar PDF (demo)", use_container_width=True):
            st.info("En producción esto generaría un PDF con el reporte completo.")
    with col2:
        import io
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📊 Descargar CSV de métricas", data=csv,
                           file_name=f"metricas_{cliente_id}.csv",
                           mime="text/csv", use_container_width=True)
