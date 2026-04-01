"""
vistas/notificaciones_panel.py
Panel de gestión y envío de notificaciones por email.
"""
import streamlit as st
import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.database import get_clientes_df, get_proyectos_df, get_contenidos_df
from data.notificaciones import (
    enviar_reporte_semanal, enviar_alerta_aprobacion,
    enviar_aviso_proyecto, enviar_recordatorio_contenidos,
    enviar_evento, verificar_conexion, modo_simulacion
)
from data.mock_data import ESTADO_COLOR

def show():
    st.markdown("""
    <div style='margin-bottom:24px;'>
        <h1 style='font-size:26px;font-weight:600;color:#f0f0ec;margin:0;'>
            Notificaciones
        </h1>
        <p style='color:#9a9b9f;font-size:14px;margin-top:4px;'>
            Emails automáticos y comunicación con clientes
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Badge de estado
    if modo_simulacion():
        st.markdown("""
        <div style='background:#ffa94d22;border:1px solid #ffa94d44;border-radius:8px;
                    padding:10px 16px;margin-bottom:20px;font-size:13px;color:#ffa94d;'>
            ⚠️ <strong>Modo simulación</strong> — los emails NO se envían.
            Completá <code>data/config.py</code> con tu Gmail para activar el envío real.
        </div>
        """, unsafe_allow_html=True)
    else:
        conn = verificar_conexion()
        if conn["ok"]:
            st.markdown("""
            <div style='background:#c8f13522;border:1px solid #c8f13544;border-radius:8px;
                        padding:10px 16px;margin-bottom:20px;font-size:13px;color:#c8f135;'>
                ✅ Gmail conectado — los emails se envían correctamente.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"❌ Error de conexión Gmail: {conn['error']}")

    clientes_df  = get_clientes_df()
    proyectos_df = get_proyectos_df()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Reporte semanal",
        "✅ Aprobar contenido",
        "📁 Cambio de proyecto",
        "📅 Recordatorio",
        "🗓️ Evento / Reunión",
    ])

    # ════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("#### Enviar reporte semanal a un cliente")
        col1, col2 = st.columns(2)
        with col1:
            cli_sel = st.selectbox("Cliente", clientes_df["nombre"].tolist(),
                                   key="rep_cliente")
            cli_row = clientes_df[clientes_df["nombre"] == cli_sel].iloc[0]
            email_destino = st.text_input("Email destinatario",
                                          value=cli_row["email"], key="rep_email")

        with col2:
            st.markdown("**Métricas de la semana**")
            imp   = st.number_input("Impresiones", value=45000, step=1000, key="rep_imp")
            cl    = st.number_input("Clics",        value=1800,  step=100,  key="rep_cl")
            conv  = st.number_input("Conversiones", value=140,   step=10,   key="rep_conv")
            gasto = st.number_input("Inversión ($)", value=3500.0, step=100.0, key="rep_gasto")
            roas  = st.number_input("ROAS",         value=4.2,   step=0.1,  key="rep_roas")

        # Proyectos del cliente seleccionado
        mis_proy = proyectos_df[proyectos_df["cliente_id"] == cli_row["id"]]
        proy_list = mis_proy[["nombre","tipo","progreso","estado"]].to_dict("records")

        st.markdown(f"Se incluirán **{len(proy_list)} proyecto(s)** de {cli_sel}.")

        if st.button("📤 Enviar reporte semanal", use_container_width=True, key="btn_rep"):
            with st.spinner("Enviando..."):
                r = enviar_reporte_semanal(
                    cliente_email=email_destino,
                    cliente_nombre=cli_sel,
                    metricas={"impresiones":imp,"clics":cl,"conversiones":conv,
                               "gasto":gasto,"roas":roas},
                    proyectos=proy_list,
                )
            _mostrar_resultado(r)

    # ════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("#### Alertar al cliente sobre contenidos para aprobar")

        cli_sel2  = st.selectbox("Cliente", clientes_df["nombre"].tolist(), key="apr_cli")
        cli_row2  = clientes_df[clientes_df["nombre"] == cli_sel2].iloc[0]
        email2    = st.text_input("Email", value=cli_row2["email"], key="apr_email")

        contenidos_df = get_contenidos_df(cli_row2["id"])
        pendientes    = contenidos_df[contenidos_df["estado"] == "En revisión"] if not contenidos_df.empty else contenidos_df

        if pendientes.empty:
            st.info(f"No hay contenidos 'En revisión' para {cli_sel2}.")
        else:
            st.markdown(f"**{len(pendientes)} contenido(s) en revisión:**")
            for _, ct in pendientes.iterrows():
                color = ESTADO_COLOR.get(ct["estado"],"#5c5d63")
                st.markdown(f"""
                <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:8px;
                            padding:10px 14px;margin-bottom:6px;font-size:13px;'>
                    📌 <strong style='color:#f0f0ec;'>{ct['titulo']}</strong>
                    <span style='color:#9a9b9f;'> · {ct['tipo']} · {ct['fecha']}</span>
                </div>
                """, unsafe_allow_html=True)

            if st.button("📤 Enviar alerta de aprobación", use_container_width=True, key="btn_apr"):
                cts_list = pendientes[["titulo","tipo","fecha","copy"]].to_dict("records")
                with st.spinner("Enviando..."):
                    r = enviar_alerta_aprobacion(email2, cli_sel2, cts_list)
                _mostrar_resultado(r)

    # ════════════════════════════════════════════════════════════
    with tab3:
        st.markdown("#### Notificar cambio de estado en un proyecto")

        col1, col2 = st.columns(2)
        with col1:
            cli_sel3 = st.selectbox("Cliente", clientes_df["nombre"].tolist(), key="proy_cli")
            cli_row3 = clientes_df[clientes_df["nombre"] == cli_sel3].iloc[0]
            mis_proy3 = proyectos_df[proyectos_df["cliente_id"] == cli_row3["id"]]

            if mis_proy3.empty:
                st.info("Este cliente no tiene proyectos.")
            else:
                proy_sel = st.selectbox("Proyecto", mis_proy3["nombre"].tolist(), key="proy_nombre")
                proy_row = mis_proy3[mis_proy3["nombre"] == proy_sel].iloc[0]
                estado_ant = st.text_input("Estado anterior", value=proy_row["estado"], key="proy_est_ant")

        with col2:
            email3     = st.text_input("Email destinatario", value=cli_row3["email"], key="proy_email")
            estado_new = st.selectbox("Nuevo estado", ["En curso","Completado","Pausado","Cancelado"], key="proy_est_new")
            notas3     = st.text_area("Notas (opcional)", height=80, key="proy_notas")

        if not mis_proy3.empty:
            if st.button("📤 Enviar aviso de cambio", use_container_width=True, key="btn_proy"):
                with st.spinner("Enviando..."):
                    r = enviar_aviso_proyecto(
                        destinatario=email3,
                        cliente_nombre=cli_sel3,
                        proyecto_nombre=proy_sel,
                        estado_anterior=estado_ant,
                        estado_nuevo=estado_new,
                        responsable=proy_row.get("responsable",""),
                        notas=notas3,
                    )
                _mostrar_resultado(r)

    # ════════════════════════════════════════════════════════════
    with tab4:
        st.markdown("#### Recordatorio de contenidos del día siguiente")

        email4 = st.text_input("Email del equipo", placeholder="equipo@consultify.com", key="rec_email")
        manana = datetime.date.today() + datetime.timedelta(days=1)

        contenidos_all = get_contenidos_df()
        if not contenidos_all.empty:
            manana_cts = contenidos_all[contenidos_all["fecha"] == manana]
        else:
            manana_cts = contenidos_all

        if manana_cts.empty:
            st.info(f"No hay contenidos programados para mañana ({manana.strftime('%d/%m/%Y')}).")
        else:
            st.markdown(f"**{len(manana_cts)} contenido(s) para mañana:**")
            for _, ct in manana_cts.iterrows():
                cli_nombre = clientes_df[clientes_df["id"] == ct["cliente_id"]]["nombre"].values
                cli_txt = cli_nombre[0] if len(cli_nombre) else ""
                st.markdown(f"""
                <div style='background:#1d1f28;border:1px solid #2a2d3a;border-radius:8px;
                            padding:10px 14px;margin-bottom:6px;font-size:13px;'>
                    📌 <strong style='color:#f0f0ec;'>{ct['titulo']}</strong>
                    <span style='color:#9a9b9f;'> · {ct['tipo']} · {cli_txt}</span>
                </div>
                """, unsafe_allow_html=True)

            if st.button("📤 Enviar recordatorio", use_container_width=True, key="btn_rec"):
                if not email4:
                    st.error("Ingresá un email.")
                else:
                    cts_list = []
                    for _, ct in manana_cts.iterrows():
                        cli_n = clientes_df[clientes_df["id"] == ct["cliente_id"]]["nombre"].values
                        cts_list.append({
                            "titulo": ct["titulo"], "tipo": ct["tipo"],
                            "cliente": cli_n[0] if len(cli_n) else "",
                            "responsable": ct.get("responsable",""),
                            "copy": ct.get("copy",""),
                        })
                    with st.spinner("Enviando..."):
                        r = enviar_recordatorio_contenidos(email4, cts_list)
                    _mostrar_resultado(r)

    # ════════════════════════════════════════════════════════════
    with tab5:
        st.markdown("#### Enviar invitación a evento o reunión")

        col1, col2 = st.columns(2)
        with col1:
            ev_titulo = st.text_input("Título del evento", placeholder="Reunión de seguimiento Q2", key="ev_titulo")
            ev_fecha  = st.date_input("Fecha", key="ev_fecha")
            ev_hora   = st.time_input("Hora", value=datetime.time(10, 0), key="ev_hora")
            ev_lugar  = st.text_input("Lugar / Link Meet", placeholder="https://meet.google.com/...", key="ev_lugar")

        with col2:
            ev_desc   = st.text_area("Descripción / Agenda", height=100, key="ev_desc")
            ev_emails_raw = st.text_area("Destinatarios (uno por línea)",
                                          placeholder="cliente@empresa.com\nequipo@consultify.com",
                                          height=100, key="ev_emails")

        if st.button("📤 Enviar invitaciones", use_container_width=True, key="btn_ev"):
            emails_lista = [e.strip() for e in ev_emails_raw.strip().splitlines() if e.strip()]
            if not ev_titulo:
                st.error("Ingresá un título para el evento.")
            elif not emails_lista:
                st.error("Ingresá al menos un email destinatario.")
            else:
                with st.spinner(f"Enviando a {len(emails_lista)} destinatario(s)..."):
                    r = enviar_evento(
                        destinatarios=emails_lista,
                        titulo=ev_titulo,
                        fecha=ev_fecha.strftime("%d/%m/%Y"),
                        hora=ev_hora.strftime("%H:%M"),
                        descripcion=ev_desc,
                        lugar=ev_lugar,
                    )
                _mostrar_resultado(r)
                if r.get("detalle"):
                    for d in r["detalle"]:
                        estado = "✅" if d.get("ok") else "❌"
                        st.markdown(f"{estado} `{d['email']}`")


# ── Helper ─────────────────────────────────────────────────────────
def _mostrar_resultado(r: dict):
    if r.get("simulado"):
        st.info("📧 Simulación: el email se habría enviado correctamente. "
                "Configurá Gmail en `data/config.py` para envío real.")
    elif r.get("ok"):
        enviados = r.get("enviados")
        total    = r.get("total")
        if enviados and total:
            st.success(f"✅ Email enviado a {enviados}/{total} destinatarios.")
        else:
            st.success("✅ Email enviado correctamente.")
    else:
        st.error(f"❌ Error al enviar: {r.get('error','Error desconocido')}")
