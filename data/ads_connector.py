"""
data/ads_connector.py

Conector para Meta Ads y Google Ads.
- Si hay credenciales reales configuradas en config.py → usa la API real
- Si no → usa datos simulados realistas

Para activar APIs reales, completá data/config.py con tus credenciales.
"""
import os
import sys
import datetime
import random
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Intentar cargar config real ───────────────────────────────────
try:
    from data.config import META_CONFIG, GOOGLE_CONFIG
    META_REAL   = bool(META_CONFIG.get("access_token"))
    GOOGLE_REAL = bool(GOOGLE_CONFIG.get("developer_token"))
except ImportError:
    META_REAL   = False
    GOOGLE_REAL = False
    META_CONFIG = {}
    GOOGLE_CONFIG = {}

# ─────────────────────────────────────────────────────────────────
#  META ADS
# ─────────────────────────────────────────────────────────────────

def get_meta_campaigns(account_id: str) -> pd.DataFrame:
    """Retorna campañas activas de una cuenta de Meta Ads."""
    if META_REAL:
        return _meta_campaigns_real(account_id)
    return _meta_campaigns_mock(account_id)

def get_meta_insights(account_id: str, days: int = 30) -> pd.DataFrame:
    """Retorna métricas de los últimos N días de Meta Ads."""
    if META_REAL:
        return _meta_insights_real(account_id, days)
    return _meta_insights_mock(account_id, days)

def create_meta_campaign(account_id: str, nombre: str, objetivo: str,
                          presupuesto_diario: float) -> dict:
    """Crea una campaña en Meta Ads."""
    if META_REAL:
        return _meta_create_real(account_id, nombre, objetivo, presupuesto_diario)
    return _meta_create_mock(nombre, objetivo, presupuesto_diario)

# ── Meta Real ────────────────────────────────────────────────────
def _meta_campaigns_real(account_id):
    try:
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.api import FacebookAdsApi
        FacebookAdsApi.init(
            META_CONFIG["app_id"],
            META_CONFIG["app_secret"],
            META_CONFIG["access_token"]
        )
        account  = AdAccount(f"act_{account_id}")
        campaigns = account.get_campaigns(fields=["id","name","status","objective",
                                                   "daily_budget","lifetime_budget"])
        rows = []
        for c in campaigns:
            rows.append({
                "id":         c["id"],
                "nombre":     c["name"],
                "estado":     c["status"],
                "objetivo":   c.get("objective",""),
                "presupuesto": float(c.get("daily_budget", c.get("lifetime_budget", 0))) / 100,
                "plataforma": "Meta",
            })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

def _meta_insights_real(account_id, days):
    try:
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.api import FacebookAdsApi
        FacebookAdsApi.init(
            META_CONFIG["app_id"],
            META_CONFIG["app_secret"],
            META_CONFIG["access_token"]
        )
        since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        until = datetime.date.today().isoformat()
        account = AdAccount(f"act_{account_id}")
        insights = account.get_insights(
            fields=["impressions","clicks","spend","ctr","cpc","actions","date_start"],
            params={"time_range": {"since": since, "until": until},
                    "time_increment": 1}
        )
        rows = []
        for i in insights:
            conversiones = sum(
                int(a["value"]) for a in i.get("actions", [])
                if a["action_type"] in ("purchase","lead","complete_registration")
            )
            rows.append({
                "fecha":         i["date_start"],
                "impresiones":   int(i.get("impressions", 0)),
                "clics":         int(i.get("clicks", 0)),
                "gasto":         float(i.get("spend", 0)),
                "ctr":           float(i.get("ctr", 0)),
                "cpc":           float(i.get("cpc", 0)),
                "conversiones":  conversiones,
                "plataforma":    "Meta",
            })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

def _meta_create_real(account_id, nombre, objetivo, presupuesto_diario):
    try:
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.adobjects.campaign import Campaign
        from facebook_business.api import FacebookAdsApi
        FacebookAdsApi.init(
            META_CONFIG["app_id"],
            META_CONFIG["app_secret"],
            META_CONFIG["access_token"]
        )
        account  = AdAccount(f"act_{account_id}")
        campaign = account.create_campaign(fields=[], params={
            "name":           nombre,
            "objective":      objetivo,
            "status":         Campaign.Status.paused,
            "daily_budget":   int(presupuesto_diario * 100),
            "special_ad_categories": [],
        })
        return {"ok": True, "id": campaign["id"], "nombre": nombre}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ── Meta Mock ────────────────────────────────────────────────────
def _meta_campaigns_mock(account_id):
    random.seed(hash(account_id) % 9999)
    nombres = ["Campaña Awareness Q1","Retargeting Compradores","Promo Verano",
               "Lead Generation","Conversiones App","Engagement Orgánico"]
    estados = ["ACTIVE","ACTIVE","ACTIVE","PAUSED","ACTIVE","PAUSED"]
    objetivos = ["BRAND_AWARENESS","CONVERSIONS","REACH","LEAD_GENERATION",
                 "APP_INSTALLS","ENGAGEMENT"]
    rows = []
    for i in range(random.randint(3, 5)):
        rows.append({
            "id":          f"META_{account_id}_{i+1}",
            "nombre":      nombres[i],
            "estado":      estados[i],
            "objetivo":    objetivos[i],
            "presupuesto": round(random.uniform(20, 200), 2),
            "plataforma":  "Meta",
        })
    return pd.DataFrame(rows)

def _meta_insights_mock(account_id, days):
    random.seed(hash(account_id) % 9999)
    rows = []
    base_imp  = random.randint(800, 3000)
    base_gasto = random.uniform(30, 150)
    for d in range(days):
        fecha = datetime.date.today() - datetime.timedelta(days=days - d)
        factor = 1 + 0.3 * (d / days)
        imp  = int(base_imp  * factor * random.uniform(0.8, 1.2))
        cl   = int(imp * random.uniform(0.02, 0.07))
        conv = int(cl * random.uniform(0.05, 0.18))
        gasto = round(base_gasto * factor * random.uniform(0.85, 1.15), 2)
        rows.append({
            "fecha":        str(fecha),
            "impresiones":  imp,
            "clics":        cl,
            "gasto":        gasto,
            "ctr":          round(cl / imp * 100, 2) if imp else 0,
            "cpc":          round(gasto / cl, 2) if cl else 0,
            "conversiones": conv,
            "roas":         round((conv * random.uniform(20, 80)) / gasto, 2) if gasto else 0,
            "plataforma":   "Meta",
        })
    return pd.DataFrame(rows)

def _meta_create_mock(nombre, objetivo, presupuesto_diario):
    import uuid
    return {
        "ok":       True,
        "id":       f"META_MOCK_{uuid.uuid4().hex[:8].upper()}",
        "nombre":   nombre,
        "objetivo": objetivo,
        "nota":     "Creado en modo simulación. Conectá credenciales reales para publicar.",
    }

# ─────────────────────────────────────────────────────────────────
#  GOOGLE ADS
# ─────────────────────────────────────────────────────────────────

def get_google_campaigns(customer_id: str) -> pd.DataFrame:
    if GOOGLE_REAL:
        return _google_campaigns_real(customer_id)
    return _google_campaigns_mock(customer_id)

def get_google_insights(customer_id: str, days: int = 30) -> pd.DataFrame:
    if GOOGLE_REAL:
        return _google_insights_real(customer_id, days)
    return _google_insights_mock(customer_id, days)

def create_google_campaign(customer_id: str, nombre: str, tipo: str,
                            presupuesto_diario: float) -> dict:
    if GOOGLE_REAL:
        return _google_create_real(customer_id, nombre, tipo, presupuesto_diario)
    return _google_create_mock(nombre, tipo, presupuesto_diario)

# ── Google Real ──────────────────────────────────────────────────
def _google_campaigns_real(customer_id):
    try:
        from google.ads.googleads.client import GoogleAdsClient
        client = GoogleAdsClient.load_from_dict({
            "developer_token":  GOOGLE_CONFIG["developer_token"],
            "client_id":        GOOGLE_CONFIG["client_id"],
            "client_secret":    GOOGLE_CONFIG["client_secret"],
            "refresh_token":    GOOGLE_CONFIG["refresh_token"],
            "login_customer_id": customer_id,
        })
        ga_service = client.get_service("GoogleAdsService")
        query = """
            SELECT campaign.id, campaign.name, campaign.status,
                   campaign.advertising_channel_type,
                   campaign_budget.amount_micros
            FROM campaign
            WHERE campaign.status != 'REMOVED'
        """
        response = ga_service.search_stream(customer_id=customer_id, query=query)
        rows = []
        for batch in response:
            for row in batch.results:
                rows.append({
                    "id":          str(row.campaign.id),
                    "nombre":      row.campaign.name,
                    "estado":      row.campaign.status.name,
                    "tipo":        row.campaign.advertising_channel_type.name,
                    "presupuesto": row.campaign_budget.amount_micros / 1_000_000,
                    "plataforma":  "Google",
                })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

def _google_insights_real(customer_id, days):
    try:
        from google.ads.googleads.client import GoogleAdsClient
        client = GoogleAdsClient.load_from_dict({
            "developer_token":  GOOGLE_CONFIG["developer_token"],
            "client_id":        GOOGLE_CONFIG["client_id"],
            "client_secret":    GOOGLE_CONFIG["client_secret"],
            "refresh_token":    GOOGLE_CONFIG["refresh_token"],
            "login_customer_id": customer_id,
        })
        ga_service = client.get_service("GoogleAdsService")
        since = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"""
            SELECT segments.date,
                   metrics.impressions, metrics.clicks,
                   metrics.cost_micros, metrics.ctr,
                   metrics.average_cpc, metrics.conversions
            FROM campaign
            WHERE segments.date >= '{since}'
        """
        response = ga_service.search_stream(customer_id=customer_id, query=query)
        rows = []
        for batch in response:
            for row in batch.results:
                gasto = row.metrics.cost_micros / 1_000_000
                rows.append({
                    "fecha":        row.segments.date,
                    "impresiones":  row.metrics.impressions,
                    "clics":        row.metrics.clicks,
                    "gasto":        round(gasto, 2),
                    "ctr":          round(row.metrics.ctr * 100, 2),
                    "cpc":          round(row.metrics.average_cpc / 1_000_000, 2),
                    "conversiones": int(row.metrics.conversions),
                    "plataforma":   "Google",
                })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

def _google_create_real(customer_id, nombre, tipo, presupuesto_diario):
    try:
        from google.ads.googleads.client import GoogleAdsClient
        client = GoogleAdsClient.load_from_dict({
            "developer_token":  GOOGLE_CONFIG["developer_token"],
            "client_id":        GOOGLE_CONFIG["client_id"],
            "client_secret":    GOOGLE_CONFIG["client_secret"],
            "refresh_token":    GOOGLE_CONFIG["refresh_token"],
            "login_customer_id": customer_id,
        })
        budget_service   = client.get_service("CampaignBudgetService")
        campaign_service = client.get_service("CampaignService")

        # Crear presupuesto
        budget_op = client.get_type("CampaignBudgetOperation")
        budget    = budget_op.create
        budget.name               = f"Budget {nombre}"
        budget.amount_micros      = int(presupuesto_diario * 1_000_000)
        budget.delivery_method    = client.enums.BudgetDeliveryMethodEnum.STANDARD
        budget_response = budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[budget_op])
        budget_resource = budget_response.results[0].resource_name

        # Crear campaña
        camp_op = client.get_type("CampaignOperation")
        camp    = camp_op.create
        camp.name                       = nombre
        camp.advertising_channel_type   = getattr(
            client.enums.AdvertisingChannelTypeEnum, tipo, 
            client.enums.AdvertisingChannelTypeEnum.SEARCH)
        camp.status  = client.enums.CampaignStatusEnum.PAUSED
        camp.campaign_budget = budget_resource
        camp.network_settings.target_google_search    = True
        camp.network_settings.target_search_network   = True
        camp_response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[camp_op])
        return {"ok": True, "id": camp_response.results[0].resource_name, "nombre": nombre}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ── Google Mock ──────────────────────────────────────────────────
def _google_campaigns_mock(customer_id):
    random.seed(hash(customer_id) % 7777)
    nombres  = ["Búsqueda - Marca","Display Remarketing","Shopping Productos",
                "YouTube Awareness","Performance Max","Búsqueda - Competencia"]
    estados  = ["ENABLED","ENABLED","PAUSED","ENABLED","ENABLED","PAUSED"]
    tipos    = ["SEARCH","DISPLAY","SHOPPING","VIDEO","PERFORMANCE_MAX","SEARCH"]
    rows = []
    for i in range(random.randint(3, 5)):
        rows.append({
            "id":          f"GADS_{customer_id}_{i+1}",
            "nombre":      nombres[i],
            "estado":      estados[i],
            "tipo":        tipos[i],
            "presupuesto": round(random.uniform(15, 180), 2),
            "plataforma":  "Google",
        })
    return pd.DataFrame(rows)

def _google_insights_mock(customer_id, days):
    random.seed(hash(customer_id) % 7777)
    rows = []
    base_imp   = random.randint(500, 2500)
    base_gasto = random.uniform(20, 120)
    for d in range(days):
        fecha  = datetime.date.today() - datetime.timedelta(days=days - d)
        factor = 1 + 0.25 * (d / days)
        imp    = int(base_imp  * factor * random.uniform(0.8, 1.2))
        cl     = int(imp * random.uniform(0.03, 0.09))
        conv   = int(cl * random.uniform(0.04, 0.15))
        gasto  = round(base_gasto * factor * random.uniform(0.85, 1.15), 2)
        rows.append({
            "fecha":        str(fecha),
            "impresiones":  imp,
            "clics":        cl,
            "gasto":        gasto,
            "ctr":          round(cl / imp * 100, 2) if imp else 0,
            "cpc":          round(gasto / cl, 2) if cl else 0,
            "conversiones": conv,
            "roas":         round((conv * random.uniform(15, 70)) / gasto, 2) if gasto else 0,
            "plataforma":   "Google",
        })
    return pd.DataFrame(rows)

def _google_create_mock(nombre, tipo, presupuesto_diario):
    import uuid
    return {
        "ok":       True,
        "id":       f"GADS_MOCK_{uuid.uuid4().hex[:8].upper()}",
        "nombre":   nombre,
        "tipo":     tipo,
        "nota":     "Creado en modo simulación. Conectá credenciales reales para publicar.",
    }

# ─────────────────────────────────────────────────────────────────
#  COMBINADO — ambas plataformas juntas
# ─────────────────────────────────────────────────────────────────

def get_combined_insights(meta_account_id: str, google_customer_id: str,
                           days: int = 30) -> pd.DataFrame:
    """Une métricas de Meta y Google en un solo DataFrame."""
    meta_df   = get_meta_insights(meta_account_id, days)
    google_df = get_google_insights(google_customer_id, days)
    if "error" in meta_df.columns:   meta_df   = pd.DataFrame()
    if "error" in google_df.columns: google_df = pd.DataFrame()
    if meta_df.empty and google_df.empty:
        return pd.DataFrame()
    return pd.concat([meta_df, google_df], ignore_index=True)

def get_combined_campaigns(meta_account_id: str, google_customer_id: str) -> pd.DataFrame:
    """Une campañas de Meta y Google."""
    meta_df   = get_meta_campaigns(meta_account_id)
    google_df = get_google_campaigns(google_customer_id)
    if "error" in meta_df.columns:   meta_df   = pd.DataFrame()
    if "error" in google_df.columns: google_df = pd.DataFrame()
    return pd.concat([meta_df, google_df], ignore_index=True)

# ─────────────────────────────────────────────────────────────────
#  IDs de cuentas por cliente (mapeo)
# ─────────────────────────────────────────────────────────────────
CUENTAS_ADS = {
    "C001": {"meta": "1234567890", "google": "111-222-3333"},
    "C002": {"meta": "0987654321", "google": "444-555-6666"},
    "C003": {"meta": "1122334455", "google": "777-888-9999"},
    "C004": {"meta": "5544332211", "google": "000-111-2222"},
    "C005": {"meta": "9988776655", "google": "333-444-5555"},
}

def get_cuentas(cliente_id: str) -> dict:
    return CUENTAS_ADS.get(cliente_id, {"meta": "0000000000", "google": "000-000-0000"})

def modo_simulacion() -> bool:
    return not META_REAL and not GOOGLE_REAL
