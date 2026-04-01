import pandas as pd
import datetime

# ── CLIENTES ─────────────────────────────────────────────────────
CLIENTES = [
    {"id":"C001","nombre":"Empresa S.A.","industria":"Retail","contacto":"Juan Pérez",
     "email":"juan@empresa.com","telefono":"+54 11 4500-1234","estado":"Activo",
     "valor_mensual":4500,"inicio":"2023-03-15","avatar":"🏢"},
    {"id":"C002","nombre":"StartUp XYZ","industria":"Tecnología","contacto":"Ana Rodríguez",
     "email":"ana@startup.com","telefono":"+54 11 5500-5678","estado":"Activo",
     "valor_mensual":2800,"inicio":"2023-07-01","avatar":"🚀"},
    {"id":"C003","nombre":"Moda & Co.","industria":"Moda","contacto":"Sofía Luna",
     "email":"sofia@moda.com","telefono":"+54 11 4800-9012","estado":"Activo",
     "valor_mensual":3200,"inicio":"2024-01-10","avatar":"👗"},
    {"id":"C004","nombre":"FoodBrand","industria":"Gastronomía","contacto":"Pedro Gómez",
     "email":"pedro@food.com","telefono":"+54 11 4200-3456","estado":"Pausado",
     "valor_mensual":1800,"inicio":"2023-11-20","avatar":"🍔"},
    {"id":"C005","nombre":"TechSolve","industria":"B2B SaaS","contacto":"Laura Vega",
     "email":"laura@techsolve.com","telefono":"+54 11 6100-7890","estado":"Activo",
     "valor_mensual":6000,"inicio":"2024-02-01","avatar":"💻"},
]

def get_clientes_df():
    return pd.DataFrame(CLIENTES)

# ── PROYECTOS ────────────────────────────────────────────────────
PROYECTOS = [
    {"id":"P001","cliente_id":"C001","nombre":"Campaña Verano 2025","tipo":"Redes Sociales",
     "estado":"En curso","progreso":72,"inicio":"2025-01-01","fin":"2025-03-31",
     "presupuesto":8000,"gastado":5760,"responsable":"María García"},
    {"id":"P002","cliente_id":"C001","nombre":"Rediseño Web","tipo":"Web",
     "estado":"En curso","progreso":45,"inicio":"2025-02-01","fin":"2025-04-30",
     "presupuesto":5000,"gastado":2250,"responsable":"Carlos López"},
    {"id":"P003","cliente_id":"C002","nombre":"Lanzamiento App","tipo":"Full 360°",
     "estado":"En curso","progreso":30,"inicio":"2025-02-15","fin":"2025-05-31",
     "presupuesto":12000,"gastado":3600,"responsable":"María García"},
    {"id":"P004","cliente_id":"C003","nombre":"Influencer Campaign","tipo":"Influencers",
     "estado":"Completado","progreso":100,"inicio":"2024-11-01","fin":"2025-01-31",
     "presupuesto":6000,"gastado":5800,"responsable":"Carlos López"},
    {"id":"P005","cliente_id":"C005","nombre":"Lead Generation Q1","tipo":"Performance",
     "estado":"En curso","progreso":60,"inicio":"2025-01-15","fin":"2025-03-31",
     "presupuesto":9000,"gastado":5400,"responsable":"María García"},
    {"id":"P006","cliente_id":"C004","nombre":"Rebranding","tipo":"Branding",
     "estado":"Pausado","progreso":20,"inicio":"2025-01-01","fin":"2025-06-30",
     "presupuesto":7000,"gastado":1400,"responsable":"Carlos López"},
]

def get_proyectos_df():
    return pd.DataFrame(PROYECTOS)

# ── MÉTRICAS DE CAMPAÑAS ─────────────────────────────────────────
def get_metricas_df(cliente_id=None):
    data = [
        {"cliente_id":"C001","mes":"Ene","impresiones":42000,"clics":1890,"conversiones":142,
         "ctr":4.5,"cpc":2.1,"roas":3.8,"gasto":3969},
        {"cliente_id":"C001","mes":"Feb","impresiones":51000,"clics":2346,"conversiones":198,
         "ctr":4.6,"cpc":1.9,"roas":4.2,"gasto":4457},
        {"cliente_id":"C001","mes":"Mar","impresiones":47000,"clics":2209,"conversiones":176,
         "ctr":4.7,"cpc":2.0,"roas":4.0,"gasto":4418},
        {"cliente_id":"C002","mes":"Ene","impresiones":28000,"clics":980,"conversiones":64,
         "ctr":3.5,"cpc":2.8,"roas":2.9,"gasto":2744},
        {"cliente_id":"C002","mes":"Feb","impresiones":35000,"clics":1365,"conversiones":89,
         "ctr":3.9,"cpc":2.5,"roas":3.3,"gasto":3413},
        {"cliente_id":"C002","mes":"Mar","impresiones":40000,"clics":1680,"conversiones":118,
         "ctr":4.2,"cpc":2.3,"roas":3.7,"gasto":3864},
        {"cliente_id":"C003","mes":"Ene","impresiones":65000,"clics":2275,"conversiones":205,
         "ctr":3.5,"cpc":1.8,"roas":5.1,"gasto":4095},
        {"cliente_id":"C003","mes":"Feb","impresiones":72000,"clics":2736,"conversiones":246,
         "ctr":3.8,"cpc":1.7,"roas":5.5,"gasto":4651},
        {"cliente_id":"C005","mes":"Ene","impresiones":18000,"clics":1260,"conversiones":95,
         "ctr":7.0,"cpc":4.2,"roas":6.1,"gasto":5292},
        {"cliente_id":"C005","mes":"Feb","impresiones":22000,"clics":1650,"conversiones":132,
         "ctr":7.5,"cpc":3.9,"roas":6.8,"gasto":6435},
        {"cliente_id":"C005","mes":"Mar","impresiones":26000,"clics":2080,"conversiones":168,
         "ctr":8.0,"cpc":3.7,"roas":7.2,"gasto":7696},
    ]
    df = pd.DataFrame(data)
    if cliente_id:
        df = df[df["cliente_id"] == cliente_id]
    return df

# ── CALENDARIO EDITORIAL ─────────────────────────────────────────
today = datetime.date.today()
year  = today.year
month = today.month

CONTENIDOS = [
    {"id":"CT001","cliente_id":"C001","fecha":datetime.date(year,month,3),
     "titulo":"Post verano colección","tipo":"Instagram","estado":"Publicado",
     "responsable":"María","copy":"¡Llegó el verano! 🌞 Descubrí nuestra nueva colección..."},
    {"id":"CT002","cliente_id":"C001","fecha":datetime.date(year,month,7),
     "titulo":"Reel promo descuento","tipo":"Reel","estado":"Publicado",
     "responsable":"Carlos","copy":"30% OFF en toda la tienda. Solo por 48hs ⏰"},
    {"id":"CT003","cliente_id":"C002","fecha":datetime.date(year,month,10),
     "titulo":"Lanzamiento feature nueva","tipo":"LinkedIn","estado":"Aprobado",
     "responsable":"María","copy":"Estamos emocionados de anunciar nuestra nueva función..."},
    {"id":"CT004","cliente_id":"C001","fecha":datetime.date(year,month,14),
     "titulo":"Stories día del amor","tipo":"Stories","estado":"Aprobado",
     "responsable":"Carlos","copy":"¿Ya sabés qué regalarle? 💝 Tenemos la opción perfecta"},
    {"id":"CT005","cliente_id":"C003","fecha":datetime.date(year,month,16),
     "titulo":"Collab influencer @moda","tipo":"Instagram","estado":"En revisión",
     "responsable":"María","copy":"La influencer @modaarg usa nuestra nueva línea..."},
    {"id":"CT006","cliente_id":"C002","fecha":datetime.date(year,month,18),
     "titulo":"Case study cliente éxito","tipo":"Blog","estado":"Borrador",
     "responsable":"Carlos","copy":"Cómo TechSolve aumentó un 40% su eficiencia con..."},
    {"id":"CT007","cliente_id":"C005","fecha":datetime.date(year,month,20),
     "titulo":"Webinar generación leads","tipo":"LinkedIn","estado":"Planificado",
     "responsable":"María","copy":"Te invitamos a nuestro webinar gratuito sobre..."},
    {"id":"CT008","cliente_id":"C001","fecha":datetime.date(year,month,22),
     "titulo":"Post nuevo producto","tipo":"Instagram","estado":"Planificado",
     "responsable":"Carlos","copy":"Algo nuevo se viene... 👀 Mantenete atento"},
    {"id":"CT009","cliente_id":"C003","fecha":datetime.date(year,month,25),
     "titulo":"Promo fin de mes","tipo":"Stories","estado":"Planificado",
     "responsable":"María","copy":"Últimos días del mes. ¡Aprovechá los descuentos!"},
    {"id":"CT010","cliente_id":"C005","fecha":datetime.date(year,month,28),
     "titulo":"Newsletter semanal","tipo":"Email","estado":"Planificado",
     "responsable":"Carlos","copy":"Novedades de la semana: nuevas integraciones disponibles..."},
]

def get_contenidos_df(cliente_id=None):
    df = pd.DataFrame(CONTENIDOS)
    if cliente_id:
        df = df[df["cliente_id"] == cliente_id]
    return df

# ── COLORES DE ESTADO ────────────────────────────────────────────
ESTADO_COLOR = {
    "Publicado":   "#c8f135",
    "Aprobado":    "#3ddbb8",
    "En revisión": "#ffa94d",
    "Borrador":    "#9a9b9f",
    "Planificado": "#5c9dff",
    "En curso":    "#5c9dff",
    "Completado":  "#c8f135",
    "Pausado":     "#ffa94d",
    "Activo":      "#3ddbb8",
}

TIPO_ICON = {
    "Instagram":"📸","Reel":"🎬","Stories":"⭕","LinkedIn":"💼",
    "Blog":"✍️","Email":"📧","Facebook":"👤","Twitter":"🐦",
}
