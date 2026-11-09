"""
MIRAYA core services.
SQLite-backed starter implementation for accounts, wallets, sessions, catalog,
referrals, moderation, admin roles and audit logs.

This module intentionally does NOT claim to provide production payment processing,
real-time voice/video, or clinical therapy. Those require external providers and
security/legal review before launch.
"""
from __future__ import annotations
import os, re, json, hmac, hashlib, secrets, sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

def _setting(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is not None:
        return value
    try:
        import streamlit as st
        return str(st.secrets.get(name, default))
    except Exception:
        return default

DB_PATH = _setting("MIRAYA_DB_PATH", "miraya.sqlite3")
OWNER_LOGIN = _setting("MIRAYA_OWNER_LOGIN", "tarek")
OWNER_PASSWORD = _setting("MIRAYA_OWNER_INITIAL_PASSWORD", "")
PBKDF2_ITERATIONS = 310_000

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _connect():
    con = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=30000")
    return con

@contextmanager
def transaction():
    con = _connect()
    try:
        con.execute("BEGIN IMMEDIATE")
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"

def _verify_password(password: str, stored: str) -> bool:
    try:
        algo, rounds, salt_hex, digest_hex = stored.split("$", 3)
        if algo != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(rounds))
        return hmac.compare_digest(digest.hex(), digest_hex)
    except Exception:
        return False

def init_db():
    with transaction() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          public_id TEXT UNIQUE NOT NULL,
          login_id TEXT UNIQUE NOT NULL,
          display_name TEXT NOT NULL,
          email TEXT UNIQUE,
          phone TEXT UNIQUE,
          password_hash TEXT NOT NULL,
          account_type TEXT NOT NULL DEFAULT 'Standard',
          level INTEGER NOT NULL DEFAULT 1,
          coins INTEGER NOT NULL DEFAULT 0 CHECK(coins>=0),
          diamonds INTEGER NOT NULL DEFAULT 0 CHECK(diamonds>=0),
          social_enabled INTEGER NOT NULL DEFAULT 0,
          assistant_style TEXT NOT NULL DEFAULT 'neutral',
          memory_enabled INTEGER NOT NULL DEFAULT 1,
          status TEXT NOT NULL DEFAULT 'active',
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS wallet_ledger(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL REFERENCES users(id),
          currency TEXT NOT NULL CHECK(currency IN ('coins','diamonds')),
          amount INTEGER NOT NULL,
          balance_after INTEGER NOT NULL,
          withdrawable INTEGER NOT NULL DEFAULT 0,
          reason TEXT NOT NULL,
          reference TEXT,
          actor_user_id INTEGER REFERENCES users(id),
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS journals(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL REFERENCES users(id),
          mood TEXT NOT NULL,
          body TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions(
          id TEXT PRIMARY KEY,
          user_id INTEGER NOT NULL REFERENCES users(id),
          mode TEXT NOT NULL CHECK(mode IN ('text','voice','video','group_voice')),
          status TEXT NOT NULL DEFAULT 'open',
          started_at TEXT NOT NULL,
          ended_at TEXT,
          summary TEXT,
          provider_ref TEXT
        );
        CREATE TABLE IF NOT EXISTS session_messages(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          session_id TEXT NOT NULL REFERENCES sessions(id),
          role TEXT NOT NULL,
          body TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memory_notes(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL REFERENCES users(id),
          note TEXT NOT NULL,
          source_session_id TEXT,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS plans(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          session_count INTEGER NOT NULL,
          price_minor INTEGER NOT NULL,
          currency TEXT NOT NULL DEFAULT 'EGP',
          duration_days INTEGER,
          active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS catalog_items(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          sku TEXT UNIQUE NOT NULL,
          name TEXT NOT NULL,
          category TEXT NOT NULL,
          price_coins INTEGER NOT NULL DEFAULT 0,
          duration_days INTEGER,
          exclusive INTEGER NOT NULL DEFAULT 0,
          active INTEGER NOT NULL DEFAULT 1,
          metadata_json TEXT NOT NULL DEFAULT '{}'
        );
        CREATE TABLE IF NOT EXISTS entitlements(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL REFERENCES users(id),
          item_id INTEGER NOT NULL REFERENCES catalog_items(id),
          gifted_by INTEGER REFERENCES users(id),
          starts_at TEXT NOT NULL,
          expires_at TEXT,
          active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS referrals(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          inviter_id INTEGER NOT NULL REFERENCES users(id),
          invitee_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
          code TEXT NOT NULL,
          reward_applied INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS referral_rules(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          qualified_count INTEGER NOT NULL,
          bonus_sessions INTEGER NOT NULL,
          active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS reports(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          reporter_id INTEGER NOT NULL REFERENCES users(id),
          reported_id INTEGER NOT NULL REFERENCES users(id),
          session_id TEXT,
          reason TEXT NOT NULL,
          details TEXT,
          status TEXT NOT NULL DEFAULT 'pending',
          created_at TEXT NOT NULL,
          reviewed_by INTEGER REFERENCES users(id),
          reviewed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS restrictions(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL REFERENCES users(id),
          scope TEXT NOT NULL,
          reason TEXT NOT NULL,
          starts_at TEXT NOT NULL,
          ends_at TEXT,
          active INTEGER NOT NULL DEFAULT 1,
          created_by INTEGER REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS admin_roles(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
          role_type TEXT NOT NULL CHECK(role_type IN ('ADMIN','MOD')),
          role_number INTEGER NOT NULL,
          label TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS permissions(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          role_id INTEGER NOT NULL REFERENCES admin_roles(id) ON DELETE CASCADE,
          page_key TEXT NOT NULL,
          can_view INTEGER NOT NULL DEFAULT 0,
          can_create INTEGER NOT NULL DEFAULT 0,
          can_edit INTEGER NOT NULL DEFAULT 0,
          can_delete INTEGER NOT NULL DEFAULT 0,
          can_approve INTEGER NOT NULL DEFAULT 0,
          UNIQUE(role_id,page_key)
        );
        CREATE TABLE IF NOT EXISTS audit_log(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          actor_id INTEGER,
          action TEXT NOT NULL,
          target_type TEXT,
          target_id TEXT,
          details_json TEXT NOT NULL DEFAULT '{}',
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS announcements(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          kind TEXT NOT NULL,
          message TEXT NOT NULL,
          visible INTEGER NOT NULL DEFAULT 1,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS app_settings(
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );
        """)
        # Safe defaults; owner is created only when an initial password is configured.
        c.execute("INSERT OR IGNORE INTO referral_rules(qualified_count,bonus_sessions) VALUES(3,1)")
        c.execute("INSERT OR IGNORE INTO referral_rules(qualified_count,bonus_sessions) VALUES(5,2)")
        c.execute("INSERT OR IGNORE INTO referral_rules(qualified_count,bonus_sessions) VALUES(7,3)")
        if OWNER_PASSWORD:
            row = c.execute("SELECT id FROM users WHERE login_id=?", (OWNER_LOGIN,)).fetchone()
            if not row:
                c.execute("""INSERT INTO users(public_id,login_id,display_name,password_hash,account_type,level,coins,diamonds,created_at)
                              VALUES(?,?,?,?,?,?,?,?,?)""",
                          ("MRY-OWNER", OWNER_LOGIN, "مالك مراية", _hash_password(OWNER_PASSWORD), "Owner", 1000, 0, 0, now()))

def create_user(display_name: str, password: str, email: str|None=None, phone: str|None=None,
                social_enabled: bool=False, assistant_style: str="neutral", memory_enabled: bool=True,
                referral_code: str|None=None):
    display_name = display_name.strip()
    if len(display_name) < 2 or len(password) < 10:
        raise ValueError("الاسم مطلوب وكلمة المرور يجب ألا تقل عن 10 أحرف.")
    if not email and not phone:
        raise ValueError("أدخل بريدًا إلكترونيًا أو رقم هاتف موثقًا.")
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("صيغة البريد الإلكتروني غير صحيحة.")
    with transaction() as c:
        login_id = "miraya_" + secrets.token_urlsafe(7).replace("-", "").replace("_", "").lower()
        public_id = "MRY-" + secrets.token_hex(5).upper()
        cur = c.execute("""INSERT INTO users(public_id,login_id,display_name,email,phone,password_hash,
                         social_enabled,assistant_style,memory_enabled,created_at)
                         VALUES(?,?,?,?,?,?,?,?,?,?)""",
                        (public_id,login_id,display_name,email or None,phone or None,_hash_password(password),
                         int(social_enabled),assistant_style,int(memory_enabled),now()))
        uid = cur.lastrowid
        if referral_code:
            inviter = c.execute("SELECT id FROM users WHERE public_id=? OR login_id=?", (referral_code,referral_code)).fetchone()
            if inviter and inviter["id"] != uid:
                c.execute("INSERT OR IGNORE INTO referrals(inviter_id,invitee_id,code,created_at) VALUES(?,?,?,?)",
                          (inviter["id"],uid,referral_code,now()))
        return dict(id=uid, public_id=public_id, login_id=login_id)

def authenticate(login: str, password: str):
    c = _connect()
    try:
        row = c.execute("SELECT * FROM users WHERE login_id=? OR public_id=? OR email=? OR phone=?",
                        (login.strip(),login.strip(),login.strip(),login.strip())).fetchone()
        if not row or row["status"] != "active" or not _verify_password(password,row["password_hash"]):
            return None
        safe = dict(row)
        safe.pop("password_hash", None)
        return safe
    finally:
        c.close()

def get_user(user_id: int):
    c=_connect()
    try:
        r=c.execute("SELECT id,public_id,login_id,display_name,email,phone,account_type,level,coins,diamonds,social_enabled,assistant_style,memory_enabled,status,created_at FROM users WHERE id=?",(user_id,)).fetchone()
        return dict(r) if r else None
    finally: c.close()

def list_users(search: str=""):
    c=_connect()
    try:
        q="%"+search.strip()+"%"
        rows=c.execute("""SELECT id,public_id,login_id,display_name,email,phone,account_type,level,coins,diamonds,status,created_at
                          FROM users WHERE display_name LIKE ? OR public_id LIKE ? OR login_id LIKE ? ORDER BY id DESC LIMIT 500""",(q,q,q)).fetchall()
        return [dict(x) for x in rows]
    finally: c.close()

def _audit(c, actor_id, action, target_type=None, target_id=None, details=None):
    c.execute("INSERT INTO audit_log(actor_id,action,target_type,target_id,details_json,created_at) VALUES(?,?,?,?,?,?)",
              (actor_id,action,target_type,str(target_id) if target_id is not None else None,json.dumps(details or {},ensure_ascii=False),now()))

def adjust_wallet(user_id:int, currency:str, amount:int, reason:str, actor_id:int|None=None,
                  withdrawable:bool=False, reference:str|None=None):
    if currency not in ("coins","diamonds") or not isinstance(amount,int) or amount==0:
        raise ValueError("حركة الرصيد غير صحيحة.")
    with transaction() as c:
        row=c.execute(f"SELECT {currency} FROM users WHERE id=?",(user_id,)).fetchone()
        if not row: raise ValueError("الحساب غير موجود.")
        balance=int(row[currency])+amount
        if balance<0: raise ValueError("الرصيد غير كافٍ.")
        c.execute(f"UPDATE users SET {currency}=? WHERE id=?",(balance,user_id))
        c.execute("""INSERT INTO wallet_ledger(user_id,currency,amount,balance_after,withdrawable,reason,reference,actor_user_id,created_at)
                     VALUES(?,?,?,?,?,?,?,?,?)""",
                  (user_id,currency,amount,balance,int(withdrawable),reason,reference,actor_id,now()))
        _audit(c,actor_id,"wallet_adjust","user",user_id,{"currency":currency,"amount":amount,"withdrawable":withdrawable,"reason":reason})
        return balance

def wallet_history(user_id:int, limit:int=100):
    c=_connect()
    try: return [dict(r) for r in c.execute("SELECT * FROM wallet_ledger WHERE user_id=? ORDER BY id DESC LIMIT ?",(user_id,limit))]
    finally: c.close()

def save_journal(user_id:int,mood:str,body:str):
    if not body.strip(): raise ValueError("اكتب محتوى اليومية أولًا.")
    with transaction() as c:
        c.execute("INSERT INTO journals(user_id,mood,body,created_at) VALUES(?,?,?,?)",(user_id,mood,body,now()))

def get_journals(user_id:int):
    c=_connect()
    try: return [dict(r) for r in c.execute("SELECT * FROM journals WHERE user_id=? ORDER BY id DESC",(user_id,))]
    finally: c.close()

def start_session(user_id:int,mode:str):
    sid=secrets.token_urlsafe(18)
    with transaction() as c:
        c.execute("INSERT INTO sessions(id,user_id,mode,started_at) VALUES(?,?,?,?)",(sid,user_id,mode,now()))
    return sid

def add_session_message(session_id:str,role:str,body:str):
    if role not in ("user","assistant","system"): raise ValueError("نوع الرسالة غير صحيح.")
    with transaction() as c:
        c.execute("INSERT INTO session_messages(session_id,role,body,created_at) VALUES(?,?,?,?)",(session_id,role,body,now()))

def get_session_messages(session_id:str,user_id:int):
    c=_connect()
    try:
        ok=c.execute("SELECT id FROM sessions WHERE id=? AND user_id=?",(session_id,user_id)).fetchone()
        if not ok: raise PermissionError("لا تملك صلاحية الوصول لهذه الجلسة.")
        return [dict(r) for r in c.execute("SELECT role,body,created_at FROM session_messages WHERE session_id=? ORDER BY id",(session_id,))]
    finally: c.close()

def end_session(session_id:str,user_id:int,summary:str=""):
    with transaction() as c:
        cur=c.execute("UPDATE sessions SET status='closed',ended_at=?,summary=? WHERE id=? AND user_id=? AND status='open'",
                      (now(),summary,session_id,user_id))
        if cur.rowcount != 1: raise ValueError("الجلسة غير موجودة أو مغلقة.")

def save_memory_note(user_id:int,note:str,session_id:str|None=None):
    if not note.strip(): return
    with transaction() as c:
        enabled=c.execute("SELECT memory_enabled FROM users WHERE id=?",(user_id,)).fetchone()
        if not enabled or not enabled["memory_enabled"]: return
        c.execute("INSERT INTO memory_notes(user_id,note,source_session_id,created_at) VALUES(?,?,?,?)",(user_id,note,session_id,now()))

def get_memory_notes(user_id:int,limit:int=20):
    c=_connect()
    try: return [dict(r) for r in c.execute("SELECT note,created_at FROM memory_notes WHERE user_id=? ORDER BY id DESC LIMIT ?",(user_id,limit))]
    finally: c.close()

def delete_memory(user_id:int):
    with transaction() as c: c.execute("DELETE FROM memory_notes WHERE user_id=?",(user_id,))

def create_plan(name:str,count:int,price_minor:int,currency="EGP",duration_days=None):
    with transaction() as c:
        c.execute("INSERT INTO plans(name,session_count,price_minor,currency,duration_days) VALUES(?,?,?,?,?)",
                  (name,count,price_minor,currency,duration_days))

def get_plans(active_only=True):
    c=_connect()
    try:
        q="SELECT * FROM plans"+(" WHERE active=1" if active_only else "")+" ORDER BY price_minor"
        return [dict(r) for r in c.execute(q)]
    finally: c.close()

def add_catalog_item(sku,name,category,price_coins,duration_days=None,exclusive=False,metadata=None):
    with transaction() as c:
        c.execute("""INSERT INTO catalog_items(sku,name,category,price_coins,duration_days,exclusive,metadata_json)
                     VALUES(?,?,?,?,?,?,?)""",(sku,name,category,int(price_coins),duration_days,int(exclusive),json.dumps(metadata or {},ensure_ascii=False)))

def get_catalog(include_inactive=False):
    c=_connect()
    try:
        q="SELECT * FROM catalog_items"+("" if include_inactive else " WHERE active=1")+" ORDER BY category,id"
        return [dict(r) for r in c.execute(q)]
    finally: c.close()

def purchase_item(buyer_id:int,sku:str,recipient_public_id:str|None=None):
    with transaction() as c:
        item=c.execute("SELECT * FROM catalog_items WHERE sku=? AND active=1",(sku,)).fetchone()
        if not item: raise ValueError("العنصر غير متاح.")
        buyer=c.execute("SELECT * FROM users WHERE id=?",(buyer_id,)).fetchone()
        recipient=buyer
        if recipient_public_id:
            recipient=c.execute("SELECT * FROM users WHERE public_id=?",(recipient_public_id,)).fetchone()
            if not recipient: raise ValueError("معرف المستلم غير موجود.")
        if item["exclusive"] and buyer["account_type"]!="Owner": raise PermissionError("هذا العنصر حصري للإدارة.")
        if buyer["coins"] < item["price_coins"]: raise ValueError("رصيد الكوينز غير كافٍ.")
        new_balance=buyer["coins"]-item["price_coins"]
        c.execute("UPDATE users SET coins=? WHERE id=?",(new_balance,buyer_id))
        c.execute("""INSERT INTO wallet_ledger(user_id,currency,amount,balance_after,reason,reference,actor_user_id,created_at)
                     VALUES(?,?,?,?,?,?,?,?)""",(buyer_id,"coins",-item["price_coins"],new_balance,"شراء عنصر",sku,buyer_id,now()))
        expires=(datetime.now(timezone.utc)+timedelta(days=item["duration_days"])).isoformat() if item["duration_days"] else None
        c.execute("INSERT INTO entitlements(user_id,item_id,gifted_by,starts_at,expires_at) VALUES(?,?,?,?,?)",
                  (recipient["id"],item["id"],buyer_id if recipient["id"]!=buyer_id else None,now(),expires))
        _audit(c,buyer_id,"purchase","catalog_item",sku,{"recipient":recipient["public_id"]})
        return {"recipient":recipient["public_id"],"balance":new_balance}

def create_report(reporter_id:int,reported_public_id:str,reason:str,details:str=""):
    with transaction() as c:
        target=c.execute("SELECT id FROM users WHERE public_id=?",(reported_public_id,)).fetchone()
        if not target: raise ValueError("المستخدم غير موجود.")
        c.execute("INSERT INTO reports(reporter_id,reported_id,reason,details,created_at) VALUES(?,?,?,?,?)",
                  (reporter_id,target["id"],reason,details,now()))

def get_reports(status="pending"):
    c=_connect()
    try:
        return [dict(r) for r in c.execute("""SELECT r.*,u1.public_id reporter_public_id,u2.public_id reported_public_id
          FROM reports r JOIN users u1 ON u1.id=r.reporter_id JOIN users u2 ON u2.id=r.reported_id
          WHERE r.status=? ORDER BY r.id DESC""",(status,))]
    finally: c.close()

def review_report(report_id:int,reviewer_id:int,status:str):
    if status not in ("reviewed","dismissed","actioned"): raise ValueError("حالة المراجعة غير صحيحة.")
    with transaction() as c:
        c.execute("UPDATE reports SET status=?,reviewed_by=?,reviewed_at=? WHERE id=?",(status,reviewer_id,now(),report_id))
        _audit(c,reviewer_id,"review_report","report",report_id,{"status":status})

def restrict_user(user_id:int,scope:str,reason:str,days:int|None,actor_id:int):
    if scope not in ("account","group_voice","community","store","games"): raise ValueError("نطاق الحظر غير صحيح.")
    ends=(datetime.now(timezone.utc)+timedelta(days=days)).isoformat() if days else None
    with transaction() as c:
        c.execute("INSERT INTO restrictions(user_id,scope,reason,starts_at,ends_at,created_by) VALUES(?,?,?,?,?,?)",
                  (user_id,scope,reason,now(),ends,actor_id))
        if scope=="account":
            c.execute("UPDATE users SET status='suspended' WHERE id=?",(user_id,))
        _audit(c,actor_id,"restrict_user","user",user_id,{"scope":scope,"reason":reason,"days":days})

def set_user_status(user_id:int,status:str,actor_id:int):
    if status not in ("active","suspended","banned"): raise ValueError("حالة الحساب غير صحيحة.")
    with transaction() as c:
        c.execute("UPDATE users SET status=? WHERE id=?",(status,user_id))
        _audit(c,actor_id,"set_user_status","user",user_id,{"status":status})

def assign_admin_role(user_id:int,role_type:str):
    if role_type not in ("ADMIN","MOD"): raise ValueError("نوع الدور غير صحيح.")
    with transaction() as c:
        number=c.execute("SELECT COALESCE(MAX(role_number),0)+1 n FROM admin_roles WHERE role_type=?",(role_type,)).fetchone()["n"]
        label=f"{role_type}-{number:03d}"
        c.execute("INSERT OR REPLACE INTO admin_roles(user_id,role_type,role_number,label) VALUES(?,?,?,?)",
                  (user_id,role_type,number,label))
        c.execute("UPDATE users SET account_type=? WHERE id=?", ("Admin" if role_type == "ADMIN" else "Moderator", user_id))
        return label

def set_permission(role_id:int,page_key:str,view=False,create=False,edit=False,delete=False,approve=False):
    with transaction() as c:
        c.execute("""INSERT INTO permissions(role_id,page_key,can_view,can_create,can_edit,can_delete,can_approve)
          VALUES(?,?,?,?,?,?,?) ON CONFLICT(role_id,page_key) DO UPDATE SET
          can_view=excluded.can_view,can_create=excluded.can_create,can_edit=excluded.can_edit,
          can_delete=excluded.can_delete,can_approve=excluded.can_approve""",
          (role_id,page_key,int(view),int(create),int(edit),int(delete),int(approve)))

def has_permission(user_id:int,page_key:str,action="view"):
    c=_connect()
    try:
        user=c.execute("SELECT account_type FROM users WHERE id=?",(user_id,)).fetchone()
        if not user: return False
        if user["account_type"]=="Owner": return True
        col={"view":"can_view","create":"can_create","edit":"can_edit","delete":"can_delete","approve":"can_approve"}.get(action)
        if not col: return False
        r=c.execute(f"""SELECT p.{col} allowed FROM permissions p JOIN admin_roles a ON a.id=p.role_id
                        WHERE a.user_id=? AND p.page_key=?""",(user_id,page_key)).fetchone()
        return bool(r and r["allowed"])
    finally: c.close()

def get_dashboard_stats():
    c=_connect()
    try:
        return dict(
          users=c.execute("SELECT COUNT(*) n FROM users").fetchone()["n"],
          active_users=c.execute("SELECT COUNT(*) n FROM users WHERE status='active'").fetchone()["n"],
          sessions=c.execute("SELECT COUNT(*) n FROM sessions").fetchone()["n"],
          open_sessions=c.execute("SELECT COUNT(*) n FROM sessions WHERE status='open'").fetchone()["n"],
          pending_reports=c.execute("SELECT COUNT(*) n FROM reports WHERE status='pending'").fetchone()["n"],
          coins=c.execute("SELECT COALESCE(SUM(coins),0) n FROM users").fetchone()["n"],
          diamonds=c.execute("SELECT COALESCE(SUM(diamonds),0) n FROM users").fetchone()["n"],
        )
    finally: c.close()

def owner_grant(user_id:int,coins:int=0,diamonds:int=0,coins_withdrawable=False,actor_id:int|None=None):
    if coins: adjust_wallet(user_id,"coins",coins,"منحة من الإدارة",actor_id,coins_withdrawable)
    if diamonds: adjust_wallet(user_id,"diamonds",diamonds,"منحة من الإدارة",actor_id,False)

def get_user_by_public_id(public_id:str):
    c=_connect()
    try:
        r=c.execute("SELECT id,public_id,login_id,display_name,account_type,level,coins,diamonds,status FROM users WHERE public_id=?",(public_id,)).fetchone()
        return dict(r) if r else None
    finally: c.close()

def create_announcement(kind:str,message:str):
    with transaction() as c:
        c.execute("INSERT INTO announcements(kind,message,created_at) VALUES(?,?,?)",(kind,message,now()))

def get_announcements(limit=30):
    c=_connect()
    try: return [dict(r) for r in c.execute("SELECT * FROM announcements WHERE visible=1 ORDER BY id DESC LIMIT ?",(limit,))]
    finally: c.close()
