import streamlit as st
import datetime
import calendar
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.database import get_contenidos_df, get_clientes_df
from data.mock_data import ESTADO_COLOR, TIPO_ICON

def show(cliente_mode=False):
    st.markdown("""
    <div style='margin-bottom:28px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>Calendario Editorial</h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>Planificación de contenidos</p>
    </div>
    """, unsafe_allow_html=True)

    today = datetime.date.today()

    # Inicializar estado del calendario
    if "cal_month" not in st.session_state:
        st.session_state.cal_month = today.month
    if "cal_year" not in st.session_state:
        st.session_state.cal_year = today.year

    clientes_df = get_clientes_df()

    # Filtro de cliente
    if cliente_mode and st.session_state.get("cliente_id"):
        cliente_id_filtro = st.session_state.cliente_id
        contenidos_df = get_contenidos_df(cliente_id_filtro)
    else:
        col_cli, col_esp = st.columns([2, 3])
        with col_cli:
            opciones = ["Todos"] + clientes_df["nombre"].tolist()
            cli_sel  = st.selectbox("Cliente", opciones)
        cliente_id_filtro = None
        if cli_sel != "Todos":
            row = clientes_df[clientes_df["nombre"] == cli_sel]
            if not row.empty:
                cliente_id_filtro = row.iloc[0]["id"]
        contenidos_df = get_contenidos_df(cliente_id_filtro)

    tab_cal, tab_lista, tab_nuevo = st.tabs(["📅 Calendario mensual", "📋 Lista", "➕ Nuevo contenido"])

    with tab_cal:
        # ── Navegación — procesar ANTES de renderizar el título ──
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])

        with col_nav1:
            if st.button("← Mes anterior", use_container_width=True):
                m = st.session_state.cal_month - 1
                y = st.session_state.cal_year
                if m < 1:
                    m = 12; y -= 1
                st.session_state.cal_month = m
                st.session_state.cal_year  = y
                st.rerun()

        with col_nav3:
            if st.button("Mes siguiente →", use_container_width=True):
                m = st.session_state.cal_month + 1
                y = st.session_state.cal_year
                if m > 12:
                    m = 1; y += 1
                st.session_state.cal_month = m
                st.session_state.cal_year  = y
                st.rerun()

        # Título del mes — se lee DESPUÉS de procesar los botones
        with col_nav2:
            meses = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
                     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            st.markdown(f"""
            <div style='text-align:center;font-size:18px;font-weight:600;
                        color:#f0f0ec;padding:6px 0;'>
                {meses[st.session_state.cal_month]} {st.session_state.cal_year}
            </div>
            """, unsafe_allow_html=True)

        cy = st.session_state.cal_year
        cm = st.session_state.cal_month

        # Contenidos del mes
        mes_contenidos = contenidos_df[
            (contenidos_df["fecha"].apply(lambda d: d.month) == cm) &
            (contenidos_df["fecha"].apply(lambda d: d.year)  == cy)
        ] if not contenidos_df.empty else contenidos_df

        # Encabezado días de semana
        dias = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
        cols_h = st.columns(7)
        for i, d in enumerate(dias):
            with cols_h[i]:
                st.markdown(
                    f"<div style='text-align:center;font-size:11px;color:#5c5d63;"
                    f"text-transform:uppercase;letter-spacing:1px;padding:8px 0;'>{d}</div>",
                    unsafe_allow_html=True)

        # Grilla del mes
        for week in calendar.monthcalendar(cy, cm):
            cols_w = st.columns(7)
            for i, day in enumerate(week):
                with cols_w[i]:
                    if day == 0:
                        st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
                        continue
                    date_obj  = datetime.date(cy, cm, day)
                    is_today  = date_obj == today
                    day_items = mes_contenidos[mes_contenidos["fecha"] == date_obj] if not mes_contenidos.empty else []

                    day_bg    = "#252836" if is_today else "#1d1f28"
                    day_color = "#c8f135" if is_today else "#f0f0ec"
                    items_html = ""

                    if len(day_items):
                        for _, ct in day_items.iterrows():
                            ic  = TIPO_ICON.get(ct["tipo"], "📌")
                            c   = ESTADO_COLOR.get(ct["estado"], "#5c5d63")
                            items_html += (
                                f"<div style='font-size:9px;background:{c}22;color:{c};"
                                f"border-radius:3px;padding:1px 4px;margin-top:2px;"
                                f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>"
                                f"{ic} {ct['titulo'][:14]}</div>"
                            )

                    st.markdown(f"""
                    <div style='background:{day_bg};border:1px solid #2a2d3a;border-radius:8px;
                                padding:6px;min-height:80px;margin-bottom:6px;'>
                        <div style='font-size:13px;font-weight:600;color:{day_color};
                                    margin-bottom:3px;'>{day}</div>
                        {items_html}
                    </div>
                    """, unsafe_allow_html=True)

    with tab_lista:
        col_e, col_t = st.columns(2)
        with col_e:
            est_f = st.multiselect("Estado",
                ["Publicado","Aprobado","En revisión","Borrador","Planificado"],
                default=["Publicado","Aprobado","En revisión","Borrador","Planificado"])
        with col_t:
            tip_f = st.multiselect("Tipo", list(TIPO_ICON.keys()),
                                   default=list(TIPO_ICON.keys()))

        if contenidos_df.empty:
            st.info("No hay contenidos cargados.")
        else:
            df_fil = contenidos_df[
                contenidos_df["estado"].isin(est_f) &
                contenidos_df["tipo"].isin(tip_f)
            ].sort_values("fecha")

            for _, row in df_fil.iterrows():
                c   = ESTADO_COLOR.get(row["estado"], "#5c5d63")
                ic  = TIPO_ICON.get(row["tipo"], "📌")
                cli_txt = ""
                if not cliente_mode:
                    cli_nombre = clientes_df[clientes_df["id"] == row["cliente_id"]]["nombre"].values
                    cli_txt = f" · {cli_nombre[0]}" if len(cli_nombre) else ""

                st.markdown(f"""
                <div style='background:#1d1f28;border:1px solid #2a2d3a;
                            border-left:3px solid {c};border-radius:0 10px 10px 0;
                            padding:12px 16px;margin-bottom:8px;
                            display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <div style='font-size:14px;font-weight:500;color:#f0f0ec;'>
                            {ic} {row['titulo']}
                        </div>
                        <div style='font-size:12px;color:#9a9b9f;margin-top:3px;'>
                            📅 {row['fecha']} · {row['tipo']}{cli_txt} · 👤 {row['responsable']}
                        </div>
                        <div style='font-size:12px;color:#5c5d63;margin-top:4px;font-style:italic;'>
                            {row['copy'][:80]}{'...' if len(str(row['copy'])) > 80 else ''}
                        </div>
                    </div>
                    <div style='background:{c}22;color:{c};border:1px solid {c}44;
                                border-radius:20px;padding:4px 12px;font-size:12px;
                                white-space:nowrap;margin-left:12px;'>
                        {row['estado']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_nuevo:
        with st.form("nuevo_contenido"):
            c1, c2 = st.columns(2)
            with c1:
                if not cliente_mode:
                    nc_cliente = st.selectbox("Cliente", clientes_df["nombre"].tolist())
                nc_titulo = st.text_input("Título del contenido")
                nc_tipo   = st.selectbox("Tipo", list(TIPO_ICON.keys()))
                nc_fecha  = st.date_input("Fecha de publicación")
            with c2:
                nc_estado = st.selectbox("Estado",
                    ["Planificado","Borrador","En revisión","Aprobado"])
                nc_resp   = st.selectbox("Responsable", ["María García","Carlos López"])
                nc_copy   = st.text_area("Copy / Texto", height=120,
                                         placeholder="Escribí el texto del contenido…")

            if st.form_submit_button("Guardar contenido", use_container_width=True):
                from data.database import insert_contenido
                import uuid
                cliente_id_nuevo = cliente_id_filtro
                if not cliente_mode:
                    fila = clientes_df[clientes_df["nombre"] == nc_cliente]
                    cliente_id_nuevo = fila.iloc[0]["id"] if not fila.empty else "C001"
                insert_contenido({
                    "id":           f"CT{uuid.uuid4().hex[:6].upper()}",
                    "cliente_id":   cliente_id_nuevo,
                    "fecha":        str(nc_fecha),
                    "titulo":       nc_titulo,
                    "tipo":         nc_tipo,
                    "estado":       nc_estado,
                    "responsable":  nc_resp,
                    "copy":         nc_copy,
                })
                st.success(f"✅ '{nc_titulo}' guardado en la base de datos.")
                st.rerun()