import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.mock_data import get_clientes_df, get_proyectos_df, get_metricas_df, ESTADO_COLOR

def show():
    st.markdown("""
    <div style='margin-bottom:28px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>Clientes</h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>Gestión de cartera de clientes</p>
    </div>
    """, unsafe_allow_html=True)

    clientes_df  = get_clientes_df()
    proyectos_df = get_proyectos_df()

    # ── Filtros ──────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns([2,1,1])
    with col_f1:
        buscar = st.text_input("🔍 Buscar cliente", placeholder="Nombre, industria…")
    with col_f2:
        estado_f = st.selectbox("Estado", ["Todos","Activo","Pausado","Inactivo"])
    with col_f3:
        industria_f = st.selectbox("Industria", ["Todas"] + sorted(clientes_df["industria"].unique().tolist()))

    df = clientes_df.copy()
    if buscar:
        df = df[df["nombre"].str.contains(buscar, case=False) |
                df["industria"].str.contains(buscar, case=False)]
    if estado_f != "Todos":
        df = df[df["estado"] == estado_f]
    if industria_f != "Todas":
        df = df[df["industria"] == industria_f]

    st.markdown(f"<div style='color:#9a9b9f;font-size:13px;margin:12px 0;'>{len(df)} clientes encontrados</div>",
                unsafe_allow_html=True)

    # ── Grilla de tarjetas ───────────────────────────────────────
    cols = st.columns(2)
    for i, (_, row) in enumerate(df.iterrows()):
        proy   = proyectos_df[proyectos_df["cliente_id"] == row["id"]]
        n_act  = len(proy[proy["estado"] == "En curso"])
        met    = get_metricas_df(row["id"])
        roas   = met["roas"].mean() if len(met) else 0
        color  = ESTADO_COLOR.get(row["estado"],"#5c5d63")

        with cols[i % 2]:
            st.markdown(f"""
            <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:14px;
                        padding:20px;margin-bottom:14px;'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;'>
                    <div style='display:flex;gap:12px;align-items:center;'>
                        <div style='font-size:36px;'>{row['avatar']}</div>
                        <div>
                            <div style='font-size:16px;font-weight:600;color:#f0f0ec;'>{row['nombre']}</div>
                            <div style='font-size:12px;color:#9a9b9f;'>{row['industria']}</div>
                        </div>
                    </div>
                    <span style='background:{color}22;color:{color};border:1px solid {color}44;
                                 border-radius:20px;padding:4px 12px;font-size:11px;font-weight:500;'>
                        {row['estado']}
                    </span>
                </div>
                <div style='border-top:1px solid #2a2d3a;padding-top:14px;'>
                    <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:14px;'>
                        <div style='text-align:center;background:#252836;border-radius:8px;padding:10px;'>
                            <div style='font-size:10px;color:#5c5d63;margin-bottom:3px;'>MRR</div>
                            <div style='font-size:16px;font-weight:600;color:#f0f0ec;'>${row['valor_mensual']:,}</div>
                        </div>
                        <div style='text-align:center;background:#252836;border-radius:8px;padding:10px;'>
                            <div style='font-size:10px;color:#5c5d63;margin-bottom:3px;'>Proyectos</div>
                            <div style='font-size:16px;font-weight:600;color:#5c9dff;'>{n_act} activos</div>
                        </div>
                        <div style='text-align:center;background:#252836;border-radius:8px;padding:10px;'>
                            <div style='font-size:10px;color:#5c5d63;margin-bottom:3px;'>ROAS prom</div>
                            <div style='font-size:16px;font-weight:600;color:#c8f135;'>{roas:.1f}×</div>
                        </div>
                    </div>
                    <div style='font-size:12px;color:#9a9b9f;display:flex;flex-direction:column;gap:4px;'>
                        <div>📧 {row['email']}</div>
                        <div>📞 {row['telefono']}</div>
                        <div>📅 Cliente desde {row['inicio']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Agregar nuevo cliente (form) ──────────────────────────────
    st.markdown("---")
    with st.expander("➕ Agregar nuevo cliente"):
        with st.form("form_nuevo_cliente"):
            c1, c2 = st.columns(2)
            with c1:
                n_nombre    = st.text_input("Nombre de la empresa")
                n_industria = st.selectbox("Industria", ["Retail","Tecnología","Moda","Gastronomía","B2B SaaS","Salud","Educación","Otro"])
                n_contacto  = st.text_input("Persona de contacto")
            with c2:
                n_email     = st.text_input("Email")
                n_tel       = st.text_input("Teléfono")
                n_valor     = st.number_input("Valor mensual ($)", min_value=0, step=100)
            if st.form_submit_button("Guardar cliente", use_container_width=True):
                st.success(f"✅ Cliente '{n_nombre}' agregado correctamente (demo — sin persistencia real).")
