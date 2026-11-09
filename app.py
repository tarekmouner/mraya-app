import streamlit as st
import pandas as pd
import os
import hashlib
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة مراية | مساحتك الخاصة لفهم نفسك",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم والـ CSS الشامل لتدمير أي لون أبيض في المنصة بالكامل
st.markdown("""
    <style>
    /* فرض اتجاه اللغة العربية من اليمين لليسار لكافة العناصر */
    html, body, [class*="css"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* خلفية المنصة الرئيسية */
    .main { background-color: #0b0f19; color: #ffffff; }
    .stApp { background: linear-gradient(135deg, #070913 0%, #0f172a 50%, #1e1b4b 100%); color: #ffffff; }
    
    /* --- تنسيق القائمة الجانبية (Sidebar) بالكامل --- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
        border-left: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .stRadio label p {
        color: #f8fafc !important;
        font-size: 19px !important;
        font-weight: 600 !important;
    }
    
    /* صندوق حساب الأونر في السايدبار */
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div.stSuccess,
    section[data-testid="stSidebar"] .stAlert,
    section[data-testid="stSidebar"] div[data-baseweb="notification"] {
        background-color: #1e293b !important;
        border: 1px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div.stSuccess *,
    section[data-testid="stSidebar"] .stAlert *,
    section[data-testid="stSidebar"] div[data-baseweb="notification"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
        background-color: transparent !important;
    }

    /* --- القضاء على أي خلفية بيضاء في المربعات أو الأوتوفيل --- */
    input, textarea, select, [data-baseweb="select"], [data-baseweb="popover"], [data-baseweb="menu"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    input:-webkit-autofill,
    input:-webkit-autofill:hover, 
    input:-webkit-autofill:focus, 
    input:-webkit-autofill:active {
        -webkit-box-shadow: 0 0 0 30px #1e293b inset !important;
        -webkit-text-fill-color: #ffffff !important;
        background-color: #1e293b !important;
        color: #ffffff !important;
    }

    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #1e293b !important;
        border-radius: 12px !important;
        border: 2px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    
    div[data-baseweb="input"] input, div[data-baseweb="base-input"] input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* إخفاء أي نصوص مساعدة نهائياً */
    .stTextInput small, .stNumberInput small, .stPasswordInput small, [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* إزالة أي خلفيات بيضاء لرسائل التنبيه والنجاح والخطأ */
    div.stSuccess, div.stInfo, div.stWarning, div.stError, div.stAlert {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
    }
    div.stSuccess *, div.stInfo *, div.stWarning *, div.stError *, div.stAlert * {
        color: #ffffff !important;
        font-weight: 700 !important;
        background-color: transparent !important;
    }

    /* تكبير وتوضيح الخطوط في المنصة ككل */
    body, p, span, li, label, div {
        font-size: 20px !important;
        color: #f8fafc !important;
        line-height: 2.0 !important;
        font-weight: 500 !important;
    }
    
    /* أزرار واضحة وقوية */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        padding: 12px 28px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #6d28d9 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-2px);
    }

    /* الكروت الاحترافية (Fancy Cards) */
    .fancy-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        backdrop-filter: blur(12px);
        text-align: right !important;
        position: relative;
        overflow: hidden;
    }
    .fancy-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #38bdf8, #8b5cf6, #ec4899);
    }
    
    /* عناوين رئيسية واضحة */
    .section-title {
        color: #38bdf8;
        font-weight: 900;
        font-size: 34px !important;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 25px;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "mraya_users.csv"
JOURNAL_FILE = "mraya_journal.csv"
AI_MEMORY_FILE = "mraya_ai_memory.csv"

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_db():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["Full_Name", "Login_ID", "Phone_Email", "Password", "Account_Type", "Coins", "Diamonds", "Level"])
        admin_row = pd.DataFrame({
            "Full_Name": ["طارق (الأونر)"],
            "Login_ID": ["mraya_tarek_admin"],
            "Phone_Email": ["tarek@mraya.com"],
            "Password": [hash_password("tarek12345")],
            "Account_Type": ["Owner"],
            "Coins": [999999],
            "Diamonds": [999999],
            "Level": [999]
        })
        df = pd.concat([df, admin_row], ignore_index=True)
        df.to_csv(USERS_FILE, index=False)
    else:
        df = pd.read_csv(USERS_FILE)
        if "mraya_tarek_admin" not in df["Login_ID"].values:
            admin_row = pd.DataFrame({
                "Full_Name": ["طارق (الأونر)"],
                "Login_ID": ["mraya_tarek_admin"],
                "Phone_Email": ["tarek@mraya.com"],
                "Password": [hash_password("tarek12345")],
                "Account_Type": ["Owner"],
                "Coins": [999999],
                "Diamonds": [999999],
                "Level": [999]
            })
            df = pd.concat([df, admin_row], ignore_index=True)
            df.to_csv(USERS_FILE, index=False)

    if not os.path.exists(JOURNAL_FILE):
        pd.DataFrame(columns=["Login_ID", "Date", "Mood", "Content"]).to_csv(JOURNAL_FILE, index=False)
    if not os.path.exists(AI_MEMORY_FILE):
        pd.DataFrame(columns=["Login_ID", "Chat_History"]).to_csv(AI_MEMORY_FILE, index=False)

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
if "view" not in st.session_state:
    st.session_state.view = "landing"

# --- 1. الصفحة الرئيسية (Landing Page) ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    col1, col2 = st.columns([6, 2])
    with col1:
        st.markdown("<h1 style='color: #38bdf8;'>🪞 منصة مراية | مساحتك الآمنة لفهم نفسك</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 22px;'>مساحة سرية بالكامل لتفريغ مشاعرك، التحدث مع الثيرابست الذكي بذاكرة خاصة، والانضمام لمجتمعات الدعم بأمان مطلق.</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("تسجيل الدخول", use_container_width=True):
            st.session_state.view = "login"
            st.rerun()
        if st.button("حساب جديد", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()

    st.markdown("<h2 class='section-title'>مميزات منصة مراية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="fancy-card"><h3>🤖 ثيرابست ذكي بذاكرة</h3><p>يتذكر تفاصيل مشاكلك وجلساتك السابقة ليكمل معك بوعي تام.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="fancy-card"><h3>🔒 سرية تامة وأمان</h3><p>أول ما تسجل بيتعمل لك آي دي فريد خاص باسم الموقع، ومحدش بيشوف أسرارك نهائياً.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="fancy-card"><h3>💎 متجر وهدايا</h3><p>أطراف متحركة، دخلات أسطورية، ولوحة شرف لأكثر الأصدقاء كرماً.</p></div>', unsafe_allow_html=True)

# --- 2. صفحة تسجيل الدخول ---
elif not st.session_state.logged_in and st.session_state.view == "login":
    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.view = "landing"
        st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🔑 تسجيل الدخول إلى مراية</h2>", unsafe_allow_html=True)
        login_id_input = st.text_input("معرف مراية الفريد (Login ID) أو الهاتف/الإيميل:")
        password_input = st.text_input("كلمة المرور:", type="password")
        
        if st.button("دخول آمن", type="primary", use_container_width=True):
            users_df = pd.read_csv(USERS_FILE)
            hashed_p = hash_password(password_input)
            match = users_df[(users_df["Login_ID"] == login_id_input) | (users_df["Phone_Email"] == login_id_input)]
            
            if not match.empty:
                if str(match.iloc[0]["Password"]) == hashed_p:
                    st.session_state.logged_in = True
                    st.session_state.current_user = match.iloc[0]["Login_ID"]
                    st.success("تم الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة.")
            else:
                st.error("المعرف أو الهاتف غير مسجل.")

# --- 3. صفحة حساب جديد ---
elif not st.session_state.logged_in and st.session_state.view == "register":
    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.view = "landing"
        st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>✨ إنشاء حساب جديد في مراية</h2>", unsafe_allow_html=True)
        full_name = st.text_input("الاسم الحقيقي أو المستعار:")
        phone_email = st.text_input("رقم الهاتف أو البريد الإلكتروني:")
        new_pass = st.text_input("كلمة المرور:", type="password")
        
        if st.button("إنشاء الحساب الان", type="primary", use_container_width=True):
            if full_name and phone_email and new_pass:
                users_df = pd.read_csv(USERS_FILE)
                if phone_email in users_df["Phone_Email"].values:
                    st.error("هذا البريد أو الرقم مسجل مسبقاً.")
                else:
                    base_id = full_name.strip().replace(" ", "_").lower()
                    unique_id = f"mraya_{base_id}_{len(users_df) + 1}"
                    
                    new_user = pd.DataFrame({
                        "Full_Name": [full_name],
                        "Login_ID": [unique_id],
                        "Phone_Email": [phone_email],
                        "Password": [hash_password(new_pass)],
                        "Account_Type": ["Standard"],
                        "Coins": [10],
                        "Diamonds": [5],
                        "Level": [1]
                    })
                    
                    users_df = pd.concat([users_df, new_user], ignore_index=True)
                    users_df.to_csv(USERS_FILE, index=False)
                    st.success(f"تم إنشاء حسابك بنجاح! معرفك الفريد هو: {unique_id}")
                    st.info("يمكنك الآن الانتقال لصفحة تسجيل الدخول.")

# --- 4. داخل المنصة ---
else:
    users_df = pd.read_csv(USERS_FILE)
    is_owner = (st.session_state.current_user == "mraya_tarek_admin")
    
    st.sidebar.title(f"🪞 مراية | {st.session_state.current_user}")
    if is_owner:
        st.sidebar.success("👑 حساب الأونر والمالك")
        
    menu_options = [
        "لوحة التحكم", 
        "الثيرابست الذكي (بذاكرة)", 
        "مفكرة المشاعر السرية 📖", 
        "إدارة المنصة (الأونر) ⚙️" if is_owner else None
    ]
    menu_options = [m for m in menu_options if m]
    
    menu = st.sidebar.radio("التنقل:", menu_options)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.view = "landing"
        st.rerun()

    if menu == "لوحة التحكم":
        st.title("🏠 لوحة التحكم الشخصية")
        user_row = users_df[users_df["Login_ID"] == st.session_state.current_user]
        if not user_row.empty:
            c = user_row.iloc[0]["Coins"]
            d = user_row.iloc[0]["Diamonds"]
            name = user_row.iloc[0]["Full_Name"]
            
            st.markdown(f"""
                <div class="fancy-card">
                    <h2>أهلاً بك، {name} 👋</h2>
                    <p>معرفك الفريد في المنصة: <b>{st.session_state.current_user}</b></p>
                    <hr style="border-color: rgba(255,255,255,0.1);">
                    <h3>💰 رصيد المحفظة:</h3>
                    <p style="font-size: 24px; color: #38bdf8;"><b>{c} كوينز</b> | 💎 <b>{d} ماسات</b></p>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "الثيرابست الذكي (بذاكرة)":
        st.title("🤖 الثيرابست الذكي (مساحتك الآمنة)")
        st.markdown('<div class="fancy-card"><p>هذا البوت يتذكر تفاصيل جلستك السابقة ليتابع معك بدقة متناهية.</p></div>', unsafe_allow_html=True)
        
        # استرجاع الذاكرة المخزنة لهذا المستخدم
        mem_df = pd.read_csv(AI_MEMORY_FILE)
        user_mem = mem_df[mem_df["Login_ID"] == st.session_state.current_user]
        
        history = user_mem.iloc[0]["Chat_History"] if not user_mem.empty else "لا توجد جلسات سابقة. هذه هي الجلسة الأولى."
        
        st.info(f"🧠 **ذاكرة البوت الحالية معك:** {history}")
        
        user_msg = st.text_input("اكتب رسالتك أو شعورك الآن:")
        if st.button("إرسال للثيرابست"):
            if user_msg:
                new_history = f"آخر موضوع ناقشته العميل: {user_msg}"
                if user_mem.empty:
                    new_row = pd.DataFrame({"Login_ID": [st.session_state.current_user], "Chat_History": [new_history]})
                    mem_df = pd.concat([mem_df, new_row], ignore_index=True)
                else:
                    mem_df.loc[mem_df["Login_ID"] == st.session_state.current_user, "Chat_History"] = new_history
                mem_df.to_csv(AI_MEMORY_FILE, index=False)
                
                st.success(f"🤖 **رد الثيرابست الذكي:** أسمعك جيداً بخصوص ({user_msg}). لقد سجلت ذلك في ذاكرتي وسنتابع منه في جلستنا القادمة!")

    elif menu == "مفكرة المشاعر السرية 📖":
        st.title("📖 مفكرتك السرية")
        st.markdown('<div class="fancy-card"><p>سجل يومياتك بسرية تامة لا يطلع عليها أحد سواك.</p></div>', unsafe_allow_html=True)
        mood = st.selectbox("المزاج:", ["😊 سعيد", "😌 هادئ", "🤔 عميق", "🌧️ متوتر"])
        content = st.text_area("اكتب أفكارك:")
        if st.button("حفظ اليومية"):
            if content:
                j_df = pd.read_csv(JOURNAL_FILE)
                new_j = pd.DataFrame({
                    "Login_ID": [st.session_state.current_user],
                    "Date": [str(pd.Timestamp.now().date())],
                    "Mood": [mood],
                    "Content": [content]
                })
                j_df = pd.concat([j_df, new_j], ignore_index=True)
                j_df.to_csv(JOURNAL_FILE, index=False)
                st.success("تم الحفظ بسرية تامة!")

    elif menu == "إدارة المنصة (الأونر) ⚙️" and is_owner:
        st.title("⚙️ لوحة تحكم الأونر (طارق)")
        st.markdown('<div class="fancy-card"><p>التحكم الشامل في الأكونتات والبحث السريع.</p></div>', unsafe_allow_html=True)
        search = st.text_input("بحث بالاسم أو المعرف:")
        filtered = users_df[users_df["Full_Name"].str.contains(search, case=False, na=False) | users_df["Login_ID"].str.contains(search, case=False, na=False)] if search else users_df
        
        for idx, row in filtered.iterrows():
            st.markdown(f"""
                <div class="fancy-card" style="padding: 15px;">
                    <b>👤 الاسم:</b> {row['Full_Name']} | <b>🔑 المعرف:</b> {row['Login_ID']} | <b>💰 كوينز:</b> {row['Coins']}
                </div>
            """, unsafe_allow_html=True)
