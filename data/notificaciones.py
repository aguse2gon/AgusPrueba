"""
data/notificaciones.py
Sistema de notificaciones por email via Gmail SMTP.

CONFIGURACIÓN INICIAL:
1. Ir a https://myaccount.google.com/security
2. Activar "Verificación en 2 pasos"
3. Buscar "Contraseñas de aplicación"
4. Generar una para "Correo" → copiar las 16 letras
5. Pegar esa contraseña en data/config.py → GMAIL_CONFIG["password"]
"""

import smtplib
import datetime
import os, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from data.config import GMAIL_CONFIG
    GMAIL_OK = bool(GMAIL_CONFIG.get("email") and GMAIL_CONFIG.get("password"))
except ImportError:
    GMAIL_OK = False
    GMAIL_CONFIG = {"email": "", "password": "", "nombre_remitente": "Consultify"}


# ── Envío base ────────────────────────────────────────────────────

def _enviar_email(destinatario: str, asunto: str, html: str) -> dict:
    """Envía un email HTML. Retorna {"ok": True} o {"ok": False, "error": ...}"""
    if not GMAIL_OK:
        # Modo simulación: imprime en consola
        print(f"\n📧 [SIMULACIÓN] Email no enviado (sin credenciales)")
        print(f"   Para: {destinatario}")
        print(f"   Asunto: {asunto}\n")
        return {"ok": True, "simulado": True}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"]    = f"{GMAIL_CONFIG.get('nombre_remitente','Consultify')} <{GMAIL_CONFIG['email']}>"
        msg["To"]      = destinatario

        msg.attach(MIMEText(html, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_CONFIG["email"], GMAIL_CONFIG["password"])
            server.sendmail(GMAIL_CONFIG["email"], destinatario, msg.as_string())

        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Templates HTML ────────────────────────────────────────────────

def _base_template(contenido_html: str, titulo: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background: #f4f4f8;
            margin: 0; padding: 0; color: #1a1a2e; }}
    .wrapper {{ max-width: 600px; margin: 32px auto; background: #fff;
                border-radius: 16px; overflow: hidden;
                box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
    .header {{ background: #0e0f14; padding: 28px 32px;
               display: flex; align-items: center; gap: 12px; }}
    .logo-icon {{ background: #c8f135; width: 40px; height: 40px; border-radius: 10px;
                  display: inline-flex; align-items: center; justify-content: center;
                  font-size: 20px; font-weight: 700; color: #0e0f14; }}
    .logo-text {{ color: #f0f0ec; font-size: 18px; font-weight: 600; margin-left: 12px; }}
    .body {{ padding: 32px; }}
    .title {{ font-size: 22px; font-weight: 700; color: #0e0f14; margin-bottom: 8px; }}
    .subtitle {{ font-size: 14px; color: #6b7280; margin-bottom: 28px; }}
    .card {{ background: #f8f9fc; border-radius: 12px; padding: 20px;
             margin-bottom: 16px; border-left: 4px solid #c8f135; }}
    .card-title {{ font-size: 15px; font-weight: 600; color: #0e0f14; margin-bottom: 4px; }}
    .card-sub {{ font-size: 13px; color: #6b7280; }}
    .metric {{ display: inline-block; background: #0e0f14; color: #c8f135;
               border-radius: 8px; padding: 12px 20px; margin: 6px 6px 6px 0;
               text-align: center; min-width: 100px; }}
    .metric-val {{ font-size: 22px; font-weight: 700; display: block; }}
    .metric-lab {{ font-size: 11px; color: #9a9b9f; text-transform: uppercase;
                   letter-spacing: 1px; margin-top: 2px; display: block; }}
    .btn {{ display: inline-block; background: #c8f135; color: #0e0f14;
            padding: 12px 28px; border-radius: 8px; text-decoration: none;
            font-weight: 700; font-size: 14px; margin-top: 20px; }}
    .badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px;
              font-size: 12px; font-weight: 600; }}
    .badge-green  {{ background: #d1fae5; color: #065f46; }}
    .badge-yellow {{ background: #fef3c7; color: #92400e; }}
    .badge-blue   {{ background: #dbeafe; color: #1e40af; }}
    .badge-gray   {{ background: #f3f4f6; color: #374151; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ background: #0e0f14; color: #9a9b9f; padding: 10px 12px;
          text-align: left; font-size: 11px; text-transform: uppercase;
          letter-spacing: 1px; }}
    td {{ padding: 10px 12px; border-bottom: 1px solid #f0f0f4; color: #374151; }}
    tr:last-child td {{ border-bottom: none; }}
    .footer {{ background: #f8f9fc; padding: 20px 32px; text-align: center;
               font-size: 12px; color: #9ca3af; border-top: 1px solid #e5e7eb; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <span class="logo-icon">⚡</span>
      <span class="logo-text">Consultify Marketing</span>
    </div>
    <div class="body">
      <div class="title">{titulo}</div>
      {contenido_html}
    </div>
    <div class="footer">
      Consultify Marketing Platform · {datetime.date.today().strftime('%d/%m/%Y')}<br>
      Este es un email automático, no respondas directamente.
    </div>
  </div>
</body>
</html>
"""


# ── 1. Reporte semanal al cliente ─────────────────────────────────

def enviar_reporte_semanal(cliente_email: str, cliente_nombre: str,
                            metricas: dict, proyectos: list) -> dict:
    """
    metricas: {"impresiones": int, "clics": int, "conversiones": int,
               "gasto": float, "roas": float, "ctr": float}
    proyectos: [{"nombre": str, "progreso": int, "estado": str}, ...]
    """
    proy_rows = ""
    for p in proyectos:
        estado = p.get("estado", "")
        badge_class = ("badge-green" if estado == "Completado" else
                       "badge-blue"  if estado == "En curso"   else "badge-yellow")
        proy_rows += f"""
        <tr>
          <td>{p['nombre']}</td>
          <td>{p.get('tipo','')}</td>
          <td>
            <div style='background:#e5e7eb;border-radius:4px;height:6px;'>
              <div style='width:{p['progreso']}%;background:#c8f135;height:6px;border-radius:4px;'></div>
            </div>
            <span style='font-size:11px;color:#6b7280;'>{p['progreso']}%</span>
          </td>
          <td><span class='badge {badge_class}'>{estado}</span></td>
        </tr>"""

    contenido = f"""
    <div class="subtitle">Resumen de la semana · {cliente_nombre}</div>

    <div style='margin-bottom:24px;'>
      <span class='metric'><span class='metric-val'>{metricas.get('impresiones',0):,}</span><span class='metric-lab'>Impresiones</span></span>
      <span class='metric'><span class='metric-val'>{metricas.get('clics',0):,}</span><span class='metric-lab'>Clics</span></span>
      <span class='metric'><span class='metric-val'>{metricas.get('conversiones',0):,}</span><span class='metric-lab'>Conversiones</span></span>
      <span class='metric'><span class='metric-val'>${metricas.get('gasto',0):,.0f}</span><span class='metric-lab'>Inversión</span></span>
      <span class='metric'><span class='metric-val'>{metricas.get('roas',0):.1f}×</span><span class='metric-lab'>ROAS</span></span>
    </div>

    <div class='card-title' style='margin-bottom:12px;'>Estado de proyectos</div>
    <table>
      <thead><tr><th>Proyecto</th><th>Tipo</th><th>Progreso</th><th>Estado</th></tr></thead>
      <tbody>{proy_rows}</tbody>
    </table>

    <a href='#' class='btn'>Ver reporte completo →</a>
    """

    html = _base_template(contenido, f"📊 Reporte semanal — {cliente_nombre}")
    return _enviar_email(
        destinatario=cliente_email,
        asunto=f"📊 Tu reporte semanal de Consultify — {datetime.date.today().strftime('%d/%m/%Y')}",
        html=html
    )


# ── 2. Alerta contenido listo para aprobar ────────────────────────

def enviar_alerta_aprobacion(cliente_email: str, cliente_nombre: str,
                              contenidos: list) -> dict:
    """
    contenidos: [{"titulo": str, "tipo": str, "fecha": str, "copy": str}, ...]
    """
    items_html = ""
    for ct in contenidos:
        items_html += f"""
        <div class='card'>
          <div class='card-title'>{ct['titulo']}</div>
          <div class='card-sub'>{ct['tipo']} · 📅 {ct['fecha']}</div>
          <div style='font-size:13px;color:#374151;margin-top:8px;
                      font-style:italic;'>"{ct.get('copy','')[:120]}..."</div>
        </div>"""

    contenido = f"""
    <div class="subtitle">Tenés {len(contenidos)} contenido(s) esperando tu aprobación</div>
    {items_html}
    <p style='font-size:14px;color:#374151;margin-top:16px;'>
      Ingresá a tu portal para revisar y aprobar cada pieza antes de su publicación.
    </p>
    <a href='#' class='btn'>Revisar contenidos →</a>
    """

    html = _base_template(contenido, f"✅ Contenidos listos para aprobar")
    return _enviar_email(
        destinatario=cliente_email,
        asunto=f"✅ {len(contenidos)} contenido(s) esperan tu aprobación — Consultify",
        html=html
    )


# ── 3. Aviso cambio de estado de proyecto ────────────────────────

def enviar_aviso_proyecto(destinatario: str, cliente_nombre: str,
                           proyecto_nombre: str, estado_anterior: str,
                           estado_nuevo: str, responsable: str,
                           notas: str = "") -> dict:
    badge_class = ("badge-green"  if estado_nuevo == "Completado" else
                   "badge-blue"   if estado_nuevo == "En curso"   else
                   "badge-yellow" if estado_nuevo == "Pausado"    else "badge-gray")

    contenido = f"""
    <div class="subtitle">Actualización en tu proyecto</div>

    <div class='card'>
      <div class='card-title'>{proyecto_nombre}</div>
      <div class='card-sub'>Cliente: {cliente_nombre} · Responsable: {responsable}</div>
      <div style='margin-top:16px;display:flex;align-items:center;gap:12px;'>
        <span class='badge badge-gray'>{estado_anterior}</span>
        <span style='font-size:18px;'>→</span>
        <span class='badge {badge_class}'>{estado_nuevo}</span>
      </div>
      {f"<p style='font-size:13px;color:#374151;margin-top:12px;'>{notas}</p>" if notas else ""}
    </div>

    <a href='#' class='btn'>Ver proyecto →</a>
    """

    html = _base_template(contenido, f"📁 Proyecto actualizado: {proyecto_nombre}")
    return _enviar_email(
        destinatario=destinatario,
        asunto=f"📁 [{proyecto_nombre}] cambió a {estado_nuevo} — Consultify",
        html=html
    )


# ── 4. Recordatorio contenidos de mañana ─────────────────────────

def enviar_recordatorio_contenidos(destinatario: str, contenidos: list) -> dict:
    """
    contenidos: [{"titulo": str, "tipo": str, "cliente": str,
                  "responsable": str, "copy": str}, ...]
    """
    manana = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
    items_html = ""
    for ct in contenidos:
        items_html += f"""
        <div class='card'>
          <div class='card-title'>{ct['titulo']}</div>
          <div class='card-sub'>
            {ct['tipo']} · 🏢 {ct.get('cliente','')} · 👤 {ct.get('responsable','')}
          </div>
          <div style='font-size:12px;color:#374151;margin-top:6px;font-style:italic;'>
            {ct.get('copy','')[:100]}...
          </div>
        </div>"""

    contenido = f"""
    <div class="subtitle">Publicaciones programadas para mañana {manana}</div>
    {items_html}
    <p style='font-size:14px;color:#374151;margin-top:8px;'>
      Asegurate de que todos los materiales estén listos y aprobados.
    </p>
    <a href='#' class='btn'>Ver calendario →</a>
    """

    html = _base_template(contenido, f"📅 {len(contenidos)} contenido(s) para mañana")
    return _enviar_email(
        destinatario=destinatario,
        asunto=f"📅 Recordatorio: {len(contenidos)} publicación(es) mañana {manana} — Consultify",
        html=html
    )


# ── 5. Evento / reunión importante ───────────────────────────────

def enviar_evento(destinatarios: list, titulo: str, fecha: str,
                  hora: str, descripcion: str, lugar: str = "") -> dict:
    """
    destinatarios: lista de emails
    """
    resultados = []
    contenido = f"""
    <div class="subtitle">Recordatorio de evento</div>

    <div class='card' style='border-left-color:#5c9dff;'>
      <div class='card-title' style='font-size:18px;'>📅 {titulo}</div>
      <div style='margin-top:12px;display:flex;flex-direction:column;gap:6px;'>
        <div style='font-size:14px;'>🗓️ <strong>{fecha}</strong></div>
        <div style='font-size:14px;'>🕐 <strong>{hora}</strong></div>
        {f"<div style='font-size:14px;'>📍 <strong>{lugar}</strong></div>" if lugar else ""}
      </div>
      {f"<p style='font-size:13px;color:#374151;margin-top:12px;'>{descripcion}</p>" if descripcion else ""}
    </div>

    <a href='#' class='btn'>Confirmar asistencia →</a>
    """

    html = _base_template(contenido, f"📅 {titulo}")
    for email in destinatarios:
        r = _enviar_email(
            destinatario=email,
            asunto=f"📅 {titulo} — {fecha} {hora}",
            html=html
        )
        resultados.append({"email": email, **r})

    ok_count = sum(1 for r in resultados if r.get("ok"))
    return {"ok": ok_count == len(destinatarios),
            "enviados": ok_count,
            "total": len(destinatarios),
            "detalle": resultados}


# ── Utilidades ────────────────────────────────────────────────────

def modo_simulacion() -> bool:
    return not GMAIL_OK

def verificar_conexion() -> dict:
    """Verifica que las credenciales de Gmail sean válidas."""
    if not GMAIL_OK:
        return {"ok": False, "error": "Sin credenciales configuradas"}
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_CONFIG["email"], GMAIL_CONFIG["password"])
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
