MIRAYA — Remaining-code foundation
Important
This package adds a safer SQLite-backed foundation and starter internal screens. It is not a claim that the entire commercial platform is production-ready. In particular, live AI, OTP delivery, card payments, real-time voice/video, recording storage, payout settlement, and regulated games require provider accounts, secrets, server endpoints, tests, and legal/security review.
Preserve your current landing page and its images
Do not replace your current public landing-page block. Keep its image paths and visual markup exactly as they are. This package is intended for the authenticated part of the app and its data layer.
Install
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```
Set environment variables before first run. On Windows PowerShell:
```powershell
$env:MIRAYA_OWNER_LOGIN="tarek"
$env:MIRAYA_OWNER_INITIAL_PASSWORD="159019"
```
Never use the old hard-coded owner password from the CSV prototype.
Initialize database
```bash
python -c "import mraya_core as db; db.init_db(); print('database ready')"
```
Integration with your existing Streamlit app
Back up the current `app.py` and CSV files.
Copy `mraya_core.py` and `mraya_remaining_ui.py` beside `app.py`.
Add `import mraya_core as db` near the imports.
Call `db.init_db()` once near app startup.
Replace the old CSV login check with:
```python
user = db.authenticate(login_input, login_pass)
if user:
    st.session_state["miraya_user"] = user
    st.session_state["logged_in"] = True
    st.rerun()
else:
    st.error("بيانات الدخول غير صحيحة أو الحساب غير نشط.")
```
Replace the old CSV registration block with:
```python
try:
    created = db.create_user(
        display_name=full_name,
        password=new_pass,
        email=contact_info if "@" in contact_info else None,
        phone=contact_info if "@" not in contact_info else None,
        social_enabled=social_choice,
        assistant_style=assistant_style,
        memory_enabled=memory_choice,
        referral_code=referral_code or None,
    )
    st.success(f'تم إنشاء الحساب. اسم دخول مراية: {created["login_id"]} · المعرف العام: {created["public_id"]}')
except Exception as exc:
    st.error(str(exc))
```
In the authenticated branch, call:
```python
db.render_remaining_app(st.session_state["miraya_user"])
```
after adding `from mraya_remaining_ui import render_remaining_app` (or call `render_remaining_app(...)` directly).
The public landing page remains your existing page with the images you already placed. Only switch to the new internal renderer after authentication.
What is implemented in this foundation
SQLite schema with per-user isolation
unique Miraya login IDs and public IDs
PBKDF2 password hashing (replaces unsalted SHA-256)
authentication and account status checks
separate coins and diamonds
append-only wallet ledger with withdrawable flag
owner grants and wallet history
private journal entries
session/message persistence
per-user memory notes with opt-out and delete function
plans and catalog data models
item purchase/gifting with atomic wallet deduction
reports and restrictions
sequential ADMIN-001 / MOD-001 role numbering
per-page permission records and permission-check helper
dashboard counters and audit log
Not yet live / needs external integration
Email/SMS OTP and account recovery: connect an email/SMS provider and implement expiring one-time tokens and rate limits.
AI therapist: connect a server-side AI provider, implement safety policies, crisis routing, consent, and user-controlled memory. This starter only stores sessions and notes; it does not fabricate AI responses.
Voice/video/group rooms: use a real-time media provider (WebRTC/SFU), access tokens, consent, moderation controls, and recording governance. Streamlit buttons are not a voice call.
Card payments: use a supported payment gateway and verify signed server-side webhooks. Never mark an order paid from a browser callback alone.
Withdrawals: build a regulated payout workflow, KYC where required, reconciliation, and legal review. A withdrawable balance flag alone is not a payout system.
Roulette/poker: do not enable cash-equivalent or redeemable chance games without jurisdiction-specific legal approval.
Production deployment: use managed database, HTTPS, secrets manager, backups, monitoring, rate limits, security tests, and privacy/legal review.
Data migration warning
The old CSV prototype contains a hard-coded owner credential and stores all users in flat files. Do not copy its password hashes into production. Export only records you are authorized to migrate, map them into the SQLite schema, and force password reset/re-enrollment. Keep a verified backup before migration.
