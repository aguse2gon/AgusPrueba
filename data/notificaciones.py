"""
data/notificaciones.py - Sistema de emails via Gmail SMTP
"""
import smtplib, datetime, os, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GMAIL_OK = False
GMAIL_CONFIG = {"email":"","password":"","nombre_remitente":"Consultify Marketing"}

try:
    import streamlit as st
    if hasattr(st,'secrets') and st.secrets.get("GMAIL_EMAIL"):
        GMAIL_CONFIG["email"]    = st.secrets["GMAIL_EMAIL"]
        GMAIL_CONFIG["password"] = st.secrets["GMAIL_PASSWORD"]
        GMAIL_OK = True
except Exception:
    pass

if not GMAIL_OK:
    try:
        from data.config import GMAIL_CONFIG as _gc
        GMAIL_CONFIG.update(_gc)
        GMAIL_OK = bool(GMAIL_CONFIG.get("email") and GMAIL_CONFIG.get("password"))
    except ImportError:
        pass


def _enviar_email(destinatario:str, asunto:str, html:str) -> dict:
    if not GMAIL_OK:
        print(f"[SIMULACIÓN] → {destinatario}: {asunto}")
        return {"ok":True,"simulado":True}
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"]    = f"{GMAIL_CONFIG.get('nombre_remitente','Consultify')} <{GMAIL_CONFIG['email']}>"
        msg["To"]      = destinatario
        msg.attach(MIMEText(html,"html","utf-8"))
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com",465,timeout=10) as s:
                s.login(GMAIL_CONFIG["email"],GMAIL_CONFIG["password"])
                s.sendmail(GMAIL_CONFIG["email"],destinatario,msg.as_string())
        except Exception:
            with smtplib.SMTP("smtp.gmail.com",587,timeout=10) as s:
                s.ehlo(); s.starttls()
                s.login(GMAIL_CONFIG["email"],GMAIL_CONFIG["password"])
                s.sendmail(GMAIL_CONFIG["email"],destinatario,msg.as_string())
        return {"ok":True}
    except smtplib.SMTPAuthenticationError:
        return {"ok":False,"error":"Error autenticación. Usá una Contraseña de Aplicación de 16 letras desde myaccount.google.com/apppasswords"}
    except Exception as e:
        return {"ok":False,"error":str(e)}


def _base_template(contenido_html:str, titulo:str) -> str:
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"/>
<style>
body{{font-family:'Helvetica Neue',Arial,sans-serif;background:#f4f4f8;margin:0;padding:0;color:#1a1a2e}}
.wrapper{{max-width:600px;margin:32px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)}}
.header{{background:#0e0f14;padding:28px 32px}}
.logo-icon{{background:#c8f135;width:40px;height:40px;border-radius:10px;display:inline-flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;color:#0e0f14}}
.logo-text{{color:#f0f0ec;font-size:18px;font-weight:600;margin-left:12px;vertical-align:middle}}
.body{{padding:32px}}
.title{{font-size:22px;font-weight:700;color:#0e0f14;margin-bottom:8px}}
.subtitle{{font-size:14px;color:#6b7280;margin-bottom:28px}}
.card{{background:#f8f9fc;border-radius:12px;padding:20px;margin-bottom:16px;border-left:4px solid #c8f135}}
.card-title{{font-size:15px;font-weight:600;color:#0e0f14;margin-bottom:4px}}
.card-sub{{font-size:13px;color:#6b7280}}
.metric{{display:inline-block;background:#0e0f14;color:#c8f135;border-radius:8px;padding:12px 20px;margin:6px 6px 6px 0;text-align:center;min-width:100px}}
.metric-val{{font-size:22px;font-weight:700;display:block}}
.metric-lab{{font-size:11px;color:#9a9b9f;text-transform:uppercase;letter-spacing:1px;margin-top:2px;display:block}}
.btn{{display:inline-block;background:#c8f135;color:#0e0f14;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px;margin-top:20px}}
.badge{{display:inline-block;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600}}
.badge-green{{background:#d1fae5;color:#065f46}}
.badge-yellow{{background:#fef3c7;color:#92400e}}
.badge-blue{{background:#dbeafe;color:#1e40af}}
.badge-gray{{background:#f3f4f6;color:#374151}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:#0e0f14;color:#9a9b9f;padding:10px 12px;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:1px}}
td{{padding:10px 12px;border-bottom:1px solid #f0f0f4;color:#374151}}
tr:last-child td{{border-bottom:none}}
.footer{{background:#f8f9fc;padding:20px 32px;text-align:center;font-size:12px;color:#9ca3af;border-top:1px solid #e5e7eb}}
</style></head><body>
<div class="wrapper">
<div class="header"><span class="logo-icon">⚡</span><span class="logo-text">Consultify Marketing</span></div>
<div class="body"><div class="title">{titulo}</div>{contenido_html}</div>
<div class="footer">Consultify Marketing Platform · {datetime.date.today().strftime('%d/%m/%Y')}<br>Email automático, no respondas directamente.</div>
</div></body></html>"""


def enviar_reporte_semanal(cliente_email,cliente_nombre,metricas,proyectos):
    rows=""
    for p in proyectos:
        e=p.get("estado",""); bc=("badge-green" if e=="Completado" else "badge-blue" if e=="En curso" else "badge-yellow")
        rows+=f"<tr><td>{p['nombre']}</td><td>{p.get('tipo','')}</td><td><div style='background:#e5e7eb;border-radius:4px;height:6px;'><div style='width:{p['progreso']}%;background:#c8f135;height:6px;border-radius:4px;'></div></div><span style='font-size:11px;color:#6b7280;'>{p['progreso']}%</span></td><td><span class='badge {bc}'>{e}</span></td></tr>"
    c=f"""<div class="subtitle">Resumen · {cliente_nombre}</div>
    <div style='margin-bottom:24px;'>
    <span class='metric'><span class='metric-val'>{metricas.get('impresiones',0):,}</span><span class='metric-lab'>Impresiones</span></span>
    <span class='metric'><span class='metric-val'>{metricas.get('clics',0):,}</span><span class='metric-lab'>Clics</span></span>
    <span class='metric'><span class='metric-val'>{metricas.get('conversiones',0):,}</span><span class='metric-lab'>Conversiones</span></span>
    <span class='metric'><span class='metric-val'>${metricas.get('gasto',0):,.0f}</span><span class='metric-lab'>Inversión</span></span>
    <span class='metric'><span class='metric-val'>{metricas.get('roas',0):.1f}×</span><span class='metric-lab'>ROAS</span></span>
    </div>
    <table><thead><tr><th>Proyecto</th><th>Tipo</th><th>Progreso</th><th>Estado</th></tr></thead><tbody>{rows}</tbody></table>
    <a href='#' class='btn'>Ver reporte completo →</a>"""
    return _enviar_email(cliente_email,f"📊 Reporte semanal Consultify — {datetime.date.today().strftime('%d/%m/%Y')}",_base_template(c,f"📊 Reporte semanal — {cliente_nombre}"))


def enviar_alerta_aprobacion(cliente_email,cliente_nombre,contenidos):
    items="".join(f"<div class='card'><div class='card-title'>{ct['titulo']}</div><div class='card-sub'>{ct['tipo']} · 📅 {ct['fecha']}</div><div style='font-size:13px;color:#374151;margin-top:8px;font-style:italic;'>\"{ct.get('copy','')[:120]}...\"</div></div>" for ct in contenidos)
    c=f"<div class='subtitle'>Tenés {len(contenidos)} contenido(s) esperando aprobación</div>{items}<a href='#' class='btn'>Revisar →</a>"
    return _enviar_email(cliente_email,f"✅ {len(contenidos)} contenido(s) para aprobar — Consultify",_base_template(c,"✅ Contenidos para aprobar"))


def enviar_aviso_proyecto(destinatario,cliente_nombre,proyecto_nombre,estado_anterior,estado_nuevo,responsable,notas=""):
    bc=("badge-green" if estado_nuevo=="Completado" else "badge-blue" if estado_nuevo=="En curso" else "badge-yellow" if estado_nuevo=="Pausado" else "badge-gray")
    c=f"""<div class='subtitle'>Actualización de proyecto</div>
    <div class='card'><div class='card-title'>{proyecto_nombre}</div><div class='card-sub'>Cliente: {cliente_nombre} · Responsable: {responsable}</div>
    <div style='margin-top:16px;display:flex;align-items:center;gap:12px;'><span class='badge badge-gray'>{estado_anterior}</span><span style='font-size:18px;'>→</span><span class='badge {bc}'>{estado_nuevo}</span></div>
    {f"<p style='font-size:13px;color:#374151;margin-top:12px;'>{notas}</p>" if notas else ""}</div>
    <a href='#' class='btn'>Ver proyecto →</a>"""
    return _enviar_email(destinatario,f"📁 [{proyecto_nombre}] → {estado_nuevo}",_base_template(c,f"📁 {proyecto_nombre}"))


def enviar_recordatorio_contenidos(destinatario,contenidos):
    manana=(datetime.date.today()+datetime.timedelta(days=1)).strftime("%d/%m/%Y")
    items="".join(f"<div class='card'><div class='card-title'>{ct['titulo']}</div><div class='card-sub'>{ct['tipo']} · {ct.get('cliente','')} · 👤 {ct.get('responsable','')}</div></div>" for ct in contenidos)
    c=f"<div class='subtitle'>Publicaciones para mañana {manana}</div>{items}<a href='#' class='btn'>Ver calendario →</a>"
    return _enviar_email(destinatario,f"📅 {len(contenidos)} publicación(es) mañana — Consultify",_base_template(c,f"📅 Recordatorio {manana}"))


def enviar_evento(destinatarios,titulo,fecha,hora,descripcion,lugar=""):
    c=f"""<div class='subtitle'>Recordatorio de evento</div>
    <div class='card' style='border-left-color:#5c9dff;'>
    <div class='card-title' style='font-size:18px;'>📅 {titulo}</div>
    <div style='margin-top:12px;'><div>🗓️ <strong>{fecha}</strong></div><div>🕐 <strong>{hora}</strong></div>
    {f"<div>📍 <strong>{lugar}</strong></div>" if lugar else ""}</div>
    {f"<p style='font-size:13px;color:#374151;margin-top:12px;'>{descripcion}</p>" if descripcion else ""}
    </div><a href='#' class='btn'>Confirmar →</a>"""
    html=_base_template(c,f"📅 {titulo}")
    res=[{"email":e,**_enviar_email(e,f"📅 {titulo} — {fecha} {hora}",html)} for e in destinatarios]
    ok=sum(1 for r in res if r.get("ok"))
    return {"ok":ok==len(destinatarios),"enviados":ok,"total":len(destinatarios),"detalle":res}


def modo_simulacion(): return not GMAIL_OK

def verificar_conexion():
    if not GMAIL_OK:
        return {"ok":False,"error":"Sin credenciales. Completá data/config.py o Streamlit secrets."}
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465,timeout=10) as s:
            s.login(GMAIL_CONFIG["email"],GMAIL_CONFIG["password"])
        return {"ok":True}
    except smtplib.SMTPAuthenticationError:
        return {"ok":False,"error":"Contraseña incorrecta. Usá Contraseña de Aplicación desde myaccount.google.com/apppasswords"}
    except Exception as e:
        return {"ok":False,"error":str(e)}
