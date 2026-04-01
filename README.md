# ⚡ Consultify — Plataforma de Marketing

Plataforma integral para consultoras de marketing. Incluye panel interno y portal de clientes.

---

## 🚀 Cómo correrlo localmente

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Correr la app
```bash
streamlit run app.py
```

La app abre en `http://localhost:8501`

---

## 👤 Usuarios de prueba

| Email | Contraseña | Rol |
|-------|-----------|-----|
| admin@consultify.com | admin123 | Administrador |
| maria@consultify.com | maria123 | Equipo interno |
| carlos@consultify.com | carlos123 | Equipo interno |
| cliente1@empresa.com | cliente123 | Portal cliente (Empresa S.A.) |
| cliente2@startup.com | startup123 | Portal cliente (StartUp XYZ) |

---

## 📦 Estructura del proyecto

```
consultify/
├── app.py                  # Entrada principal, login, router
├── requirements.txt
├── data/
│   └── mock_data.py        # Datos de prueba (reemplazar con DB real)
└── pages/
    ├── dashboard.py        # Vista general (equipo interno)
    ├── clientes.py         # Gestión de clientes
    ├── proyectos.py        # Gestión de proyectos
    ├── calendario.py       # Calendario editorial (compartido)
    ├── metricas.py         # Métricas y analíticas de campañas
    ├── portal_cliente.py   # Home del portal cliente
    ├── campanas_cliente.py # Métricas para el cliente
    └── reportes_cliente.py # Reportes y exportación para el cliente
```

---

## 🌐 Deploy gratuito en Streamlit Cloud

1. Subir el proyecto a un repo de GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repo y elegir `app.py` como entry point
4. ¡Listo! Tenés una URL pública para compartir con clientes

---

## 🔧 Próximos pasos (producción)

- **Base de datos**: Reemplazar `mock_data.py` con SQLite / PostgreSQL usando `SQLAlchemy`
- **Autenticación real**: Integrar `streamlit-authenticator` con hashing de contraseñas
- **Notificaciones**: Agregar emails automáticos con `smtplib` o SendGrid
- **Reportes PDF**: Generar PDFs con `reportlab` o `weasyprint`
- **Integración APIs**: Meta Ads, Google Ads, Instagram via APIs oficiales
