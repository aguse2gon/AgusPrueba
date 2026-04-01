"""
data/database.py
Gestor central de la base de datos SQLite para Consultify.
"""
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "consultify.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ── Crear tablas ──────────────────────────────────────────────────
def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS clientes (
        id              TEXT PRIMARY KEY,
        nombre          TEXT NOT NULL,
        industria       TEXT,
        contacto        TEXT,
        email           TEXT,
        telefono        TEXT,
        estado          TEXT DEFAULT 'Activo',
        valor_mensual   REAL DEFAULT 0,
        inicio          TEXT,
        avatar          TEXT DEFAULT '🏢'
    );

    CREATE TABLE IF NOT EXISTS proyectos (
        id              TEXT PRIMARY KEY,
        cliente_id      TEXT NOT NULL,
        nombre          TEXT NOT NULL,
        tipo            TEXT,
        estado          TEXT DEFAULT 'En curso',
        progreso        INTEGER DEFAULT 0,
        inicio          TEXT,
        fin             TEXT,
        presupuesto     REAL DEFAULT 0,
        gastado         REAL DEFAULT 0,
        responsable     TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );

    CREATE TABLE IF NOT EXISTS metricas (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id      TEXT NOT NULL,
        mes             TEXT,
        impresiones     INTEGER DEFAULT 0,
        clics           INTEGER DEFAULT 0,
        conversiones    INTEGER DEFAULT 0,
        ctr             REAL DEFAULT 0,
        cpc             REAL DEFAULT 0,
        roas            REAL DEFAULT 0,
        gasto           REAL DEFAULT 0,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );

    CREATE TABLE IF NOT EXISTS contenidos (
        id              TEXT PRIMARY KEY,
        cliente_id      TEXT NOT NULL,
        fecha           TEXT,
        titulo          TEXT NOT NULL,
        tipo            TEXT,
        estado          TEXT DEFAULT 'Planificado',
        responsable     TEXT,
        copy            TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );

    CREATE TABLE IF NOT EXISTS usuarios (
        email           TEXT PRIMARY KEY,
        password        TEXT NOT NULL,
        role            TEXT DEFAULT 'interno',
        nombre          TEXT,
        cliente_id      TEXT
    );
    """)
    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente.")

# ── CLIENTES ──────────────────────────────────────────────────────
def get_clientes_df():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM clientes", conn)
    conn.close()
    return df

def get_cliente(cliente_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM clientes WHERE id=?", (cliente_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def insert_cliente(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT OR REPLACE INTO clientes
        (id, nombre, industria, contacto, email, telefono, estado, valor_mensual, inicio, avatar)
        VALUES (:id,:nombre,:industria,:contacto,:email,:telefono,:estado,:valor_mensual,:inicio,:avatar)
    """, data)
    conn.commit(); conn.close()

def update_cliente(cliente_id, data: dict):
    data["id"] = cliente_id
    conn = get_conn()
    conn.execute("""
        UPDATE clientes SET nombre=:nombre, industria=:industria, contacto=:contacto,
        email=:email, telefono=:telefono, estado=:estado, valor_mensual=:valor_mensual
        WHERE id=:id
    """, data)
    conn.commit(); conn.close()

def delete_cliente(cliente_id):
    conn = get_conn()
    conn.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
    conn.commit(); conn.close()

# ── PROYECTOS ─────────────────────────────────────────────────────
def get_proyectos_df(cliente_id=None):
    conn = get_conn()
    if cliente_id:
        df = pd.read_sql("SELECT * FROM proyectos WHERE cliente_id=?", conn, params=(cliente_id,))
    else:
        df = pd.read_sql("SELECT * FROM proyectos", conn)
    conn.close()
    return df

def insert_proyecto(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT OR REPLACE INTO proyectos
        (id, cliente_id, nombre, tipo, estado, progreso, inicio, fin, presupuesto, gastado, responsable)
        VALUES (:id,:cliente_id,:nombre,:tipo,:estado,:progreso,:inicio,:fin,:presupuesto,:gastado,:responsable)
    """, data)
    conn.commit(); conn.close()

def update_proyecto_progreso(proyecto_id, progreso, gastado):
    conn = get_conn()
    conn.execute("UPDATE proyectos SET progreso=?, gastado=? WHERE id=?",
                 (progreso, gastado, proyecto_id))
    conn.commit(); conn.close()

def update_proyecto_estado(proyecto_id, estado):
    conn = get_conn()
    conn.execute("UPDATE proyectos SET estado=? WHERE id=?", (estado, proyecto_id))
    conn.commit(); conn.close()

# ── MÉTRICAS ──────────────────────────────────────────────────────
def get_metricas_df(cliente_id=None):
    conn = get_conn()
    if cliente_id:
        df = pd.read_sql("SELECT * FROM metricas WHERE cliente_id=?", conn, params=(cliente_id,))
    else:
        df = pd.read_sql("SELECT * FROM metricas", conn)
    conn.close()
    return df

def insert_metrica(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT INTO metricas
        (cliente_id, mes, impresiones, clics, conversiones, ctr, cpc, roas, gasto)
        VALUES (:cliente_id,:mes,:impresiones,:clics,:conversiones,:ctr,:cpc,:roas,:gasto)
    """, data)
    conn.commit(); conn.close()

# ── CONTENIDOS ────────────────────────────────────────────────────
def get_contenidos_df(cliente_id=None):
    conn = get_conn()
    if cliente_id:
        df = pd.read_sql("SELECT * FROM contenidos WHERE cliente_id=?", conn, params=(cliente_id,))
    else:
        df = pd.read_sql("SELECT * FROM contenidos", conn)
    conn.close()
    if not df.empty:
        import datetime
        df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    return df

def insert_contenido(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT OR REPLACE INTO contenidos
        (id, cliente_id, fecha, titulo, tipo, estado, responsable, copy)
        VALUES (:id,:cliente_id,:fecha,:titulo,:tipo,:estado,:responsable,:copy)
    """, data)
    conn.commit(); conn.close()

def update_contenido_estado(contenido_id, estado):
    conn = get_conn()
    conn.execute("UPDATE contenidos SET estado=? WHERE id=?", (estado, contenido_id))
    conn.commit(); conn.close()

def delete_contenido(contenido_id):
    conn = get_conn()
    conn.execute("DELETE FROM contenidos WHERE id=?", (contenido_id,))
    conn.commit(); conn.close()

# ── USUARIOS ──────────────────────────────────────────────────────
def get_usuario(email):
    conn = get_conn()
    row = conn.execute("SELECT * FROM usuarios WHERE email=?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None

def insert_usuario(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT OR REPLACE INTO usuarios (email, password, role, nombre, cliente_id)
        VALUES (:email,:password,:role,:nombre,:cliente_id)
    """, data)
    conn.commit(); conn.close()

def get_all_usuarios_df():
    conn = get_conn()
    df = pd.read_sql("SELECT email, role, nombre, cliente_id FROM usuarios", conn)
    conn.close()
    return df

# ── Utilidades ────────────────────────────────────────────────────
def db_exists():
    return os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0

def tabla_vacia(tabla):
    conn = get_conn()
    count = conn.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
    conn.close()
    return count == 0
