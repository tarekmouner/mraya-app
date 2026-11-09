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

# تخصيص التصميم والـ CSS الساحق للقضاء على أي مشاكل بصرية
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
    
    /* تنسيق صندوق حساب الأونر في السايدبار ليكون داكن وواضح[cite: 5, 6] */
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

    /* --- تنسيق مربعات الإدخال (Text/Number Inputs) بشكل احترافي وواضح --- */
    .stTextInput input, .stNumberInput input, .stPasswordInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        padding: 12px 15px !important;
    }

    /* إخفاء النصوص الإرشادية المزعجة لمنع التداخل تماماً[cite: 3, 5] */
    .stTextInput small, .stNumberInput small, .stPasswordInput small {
        display: none !important;
    }

    /* إزالة أي خلفيات بيضاء لرسائل التنبيه والنجاح والخطأ في الصفحة بالكامل */
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
    
    .image-showcase {
        text-align: center;
        padding: 20px;
        background: rgba(15, 23, 42, 0.85);
        border-radius: 28px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin-bottom: 35px;
    }
    </style>
""", unsafe_allow_html=True)

# حقن كود جافاسكريبت لمنع أي تداخل نهائياً في الحقول وتنظيف النصوص الإرشادية
components.html("""
    <script>
    const observer = new MutationObserver(() => {
        const helps = window.parent.document.querySelectorAll('.stTextInput small, .stNumberInput small, .stPasswordInput small');
        helps.forEach(el => el.style.display = 'none');
    });
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
    </script>
""", height=0)

USERS_FILE = "mraya_users.csv"

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_db():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["Full_Name", "Login_ID", "Email_Phone", "Password", "Account_Type", "Coins", "Diamonds"])
        admin_row = pd.DataFrame({
            "Full_Name": ["طارق (الأونر)"],
            "Login_ID": ["tarek_admin"],
            "Email_Phone": ["tarek@mraya.com"],
            "Password": [hash_password("tarek12345")],
            "Account_Type": ["Owner"],
            "Coins": [999999],
            "Diamonds": [999999]
        })
        df = pd.concat([df, admin_row], ignore_index=True)
        df.to_csv(USERS_FILE, index=False)
        return df
    else:
        df = pd.read_csv(USERS_FILE)
        if "tarek_admin" not in df["Login_ID"].values:
            admin_row = pd.DataFrame({
                "Full_Name": ["طارق (الأونر)"],
                "Login_ID": ["tarek_admin"],
                "Email_Phone": ["tarek@mraya.com"],
                "Password": [hash_password("tarek12345")],
                "Account_Type": ["Owner"],
                "Coins": [999999],
                "Diamonds": [999999]
            })
            df = pd.concat([df, admin_row], ignore_index=True)
            df.to_csv(USERS_FILE, index=False)
        return df

users_df = init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
if "view" not in st.session_state:
    st.session_state.view = "landing"

# البحث الذكي عن الصورتين المرفوعتين
logo_img = None
banner_img = None

for f in os.listdir("."):
    if f.endswith(".png") or f.endswith(".jpg"):
        if "مراية" in f and "2" not in f:
            logo_img = f
        elif "2" in f or "banner" in f.lower():
            banner_img = f

files_list = [f for f in os.listdir(".") if f.endswith(".png") or f.endswith(".jpg")]
if not logo_img and files_list:
    logo_img = files_list[0]
if not banner_img and len(files_list) > 1:
    banner_img = files_list[1]
elif not banner_img:
    banner_img = logo_img

# --- 1. الصفحة الرئيسية التسويقية (Landing Page) ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    
    col_logo, col_space, col_auth = st.columns([4, 4, 2])
    with col_logo:
        if logo_img and os.path.exists(logo_img):
            st.image(logo_img, width=260)
        else:
            st.markdown("<h3 style='color: #38bdf8;'>🪞 مراية | MIRAYA</h3>", unsafe_allow_html=True)
            
    with col_auth:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("دخول", use_container_width=True):
                st.session_state.view = "login"
                st.rerun()
        with c2:
            if st.button("حساب جديد", type="primary", use_container_width=True):
                st.session_state.view = "register"
                st.rerun()
                
    st.markdown("<br>", unsafe_allow_html=True)
    
    if banner_img and os.path.exists(banner_img):
        st.markdown('<div class="image-showcase">', unsafe_allow_html=True)
        st.image(banner_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        ba, bb = st.columns(2)
        with ba:
            if st.button("🚀 ابدأ رحلتك مجانًا", type="primary", use_container_width=True):
                st.session_state.view = "register"
                st.rerun()
        with bb:
            if st.button("✨ اكتشف مرايا", use_container_width=True):
                st.session_state.show_discovery = True
                
    if st.session_state.get("show_discovery", False):
        st.markdown("""
            <div class="fancy-card" style="border-right: 6px solid #38bdf8; margin-top: 20px;">
                <h3 style='color: #38bdf8;'>🧭 أهلاً بك في جولة سريعة داخل مراية</h3>
                <p>
                    منصة <b>مراية</b> ليست مجرد موقع تواصل، بل هي بيئة متكاملة تجمع بين:
                    <br>1️⃣ <b>الثيرابست الذكي:</b> لمساعدتك في ترتيب أفكارك وسياق مشاعرك بأمان تام.
                    <br>2️⃣ <b>الجلسات الجماعية:</b> لمشاركة التجارب عبر هويات مستعارة وبسرية مطلقة.
                    <br>3️⃣ <b>المتجر الرقمي:</b> لتخصيص هويتك الفريدة وإرسال الهدايا للأصدقاء.
                    <br><br>استكشف الأقسام أدناه لتتعرف على المزيد، أو أنشئ حسابك المجاني الآن وابدأ رحلتك!
                </p>
            </div>
        """, unsafe_allow_html=True)
                
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-title'>لماذا مرايا؟</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="fancy-card" style="text-align: center;">
            <p style="font-size: 22px !important; color: #ffffff !important; line-height: 2.1; margin: 0; font-weight: 600;">
                لأننا نعلم أن الحديث عن الأمور الشخصية ليس سهلًا دائمًا. أحيانًا تحتاج إلى الكتابة بدلًا من الكلام، وأحيانًا تفضل التحدث بصوتك، وأحيانًا لا تريد سوى أن تجد مساحة تستطيع فيها التعبير عن نفسك دون الشعور بالإحراج.<br><br>
                <b>لهذا لم نصمم مرايا لتكون مجرد نافذة محادثة، بل تجربة متكاملة تمنحك خيارات متعددة للتواصل والتعبير والتطور.</b>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
            <div class="fancy-card">
                <h3 style='color: #38bdf8; font-size: 24px !important; margin-bottom: 20px; font-weight: 800;'>🌟 مميزات أساسية</h3>
                <ul style='color: #f1f5f9; font-size: 20px !important; line-height: 2.4; list-style-type: none; padding: 0; font-weight: 600;'>
                    <li>🔹 مساحة شخصية مستقلة لكل مستخدم.</li>
                    <li>🔹 جلسات فردية خاصة مصممة حولك.</li>
                    <li>🔹 محادثات كتابية، صوتية، ومرئية متطورة.</li>
                    <li>🔹 مساعد ذكي يتذكر سياق محادثاتك السابقة.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
            <div class="fancy-card">
                <h3 style='color: #34d399; font-size: 24px !important; margin-bottom: 20px; font-weight: 800;'>💎 تجربة مجتمعية متكاملة</h3>
                <ul style='color: #f1f5f9; font-size: 20px !important; line-height: 2.4; list-style-type: none; padding: 0; font-weight: 600;'>
                    <li>🔹 إمكانية اختيار المشاركة المجتمعية أو البقاء بمفردك.</li>
                    <li>🔹 نظام عضويات ومزايا قابل للتخصيص.</li>
                    <li>🔹 تجربة شخصية قابلة للتطوير والتغيير.</li>
                    <li>🔹 مكافآت، هدايا، وفعاليات تفاعلية.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>الأسئلة الشائعة</h2>", unsafe_allow_html=True)
    with st.expander("❓ هل استخدام مراية مجاني؟"):
        st.write("تتيح مراية عددًا من الجلسات المجانية الأولية، وبعد استهلاكها يمكنك اختيار إحدى الباقات المتاحة.")
    with st.expander("❓ هل يتذكر المساعد الذكي محادثاتي السابقة؟"):
        st.write("نعم، يستفيد من الذاكرة الشخصية المرتبطة بحسابك وفق إعدادات الأمان والخصوصية.")
    with st.expander("❓ هل مراية بديل عن الطبيب النفسي؟"):
        st.write("مراية منصة للدعم والمساندة الرقمية، وليست بديلًا عن التشخيص أو العلاج لدى متخصص مؤهل.")

    st.markdown("<br>", unsafe_allow_html=True)
    col_end1, col_end2, col_end3 = st.columns([1, 2, 1])
    with col_end2:
        if st.button("✨ أنشئ حسابك الآن مجانًا", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()

# --- 2. صفحة تسجيل الدخول ---
elif not st.session_state.logged_in and st.session_state.view == "login":
    if st.button("⬅️ العودة للصفحة الرئيسية"):
        st.session_state.view = "landing"
        st.rerun()
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🔑 تسجيل الدخول إلى مراية</h2>", unsafe_allow_html=True)
        login_input = st.text_input("معرف مراية (Login ID) أو البريد الإلكتروني:")
        login_pass = st.text_input("كلمة المرور:", type="password")
        
        if st.button("دخول آمن", type="primary", use_container_width=True):
            users_df = pd.read_csv(USERS_FILE)
            hashed_p = hash_password(login_pass)
            user_match = users_df[(users_df["Login_ID"] == login_input) | (users_df["Email_Phone"] == login_input)]
            
            if not user_match.empty:
                stored_pass = str(user_match.iloc[0]["Password"])
                if stored_pass == hashed_p:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_match.iloc[0]["Login_ID"]
                    st.success("تم الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة.")
            else:
                st.error("المعرف أو البريد غير مسجل.")

# --- 3. صفحة إنشاء حساب جديد ---
elif not st.session_state.logged_in and st.session_state.view == "register":
    if st.button("⬅️ العودة للصفحة الرئيسية"):
        st.session_state.view = "landing"
        st.rerun()
    
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>✨ إنشاء حساب جديد في مراية</h2>", unsafe_allow_html=True)
        full_name = st.text_input("الاسم الحقيقي أو المستعار:")
        contact_info = st.text_input("البريد الإلكتروني أو رقم الهاتف:")
        new_pass = st.text_input("كلمة المرور السرية:", type="password")
        confirm_pass = st.text_input("تأكيد كلمة المرور:", type="password")
        
        if st.button("إنشاء الحساب الان", type="primary", use_container_width=True):
            if full_name and contact_info and new_pass:
                if new_pass != confirm_pass:
                    st.warning("كلمات المرور غير متطابقة.")
                else:
                    users_df = pd.read_csv(USERS_FILE)
                    if contact_info in users_df["Email_Phone"].values:
                        st.error("هذا البريد أو الرقم مسجل بالفعل.")
                    else:
                        base_id = full_name.strip().replace(" ", "_").lower()
                        unique_id = f"mraya_{base_id}_{len(users_df) + 1}"
                        
                        new_user = pd.DataFrame({
                            "Full_Name": [full_name],
                            "Login_ID": [unique_id],
                            "Email_Phone": [contact_info],
                            "Password": [hash_password(new_pass)],
                            "Account_Type": ["Standard"],
                            "Coins": [10],
                            "Diamonds": [5]
                        })
                        
                        users_df = pd.concat([users_df, new_user], ignore_index=True)
                        users_df.to_csv(USERS_FILE, index=False)
                        st.success(f"تم إنشاء حسابك بنجاح! المعرف الفريد الخاص بك هو: {unique_id}")
                        st.info("يمكنك الآن الانتقال لصفحة تسجيل الدخول.")

# --- 4. داخل المنصة (الصفحات الداخلية) ---
else:
    users_df = pd.read_csv(USERS_FILE)
    is_owner = (st.session_state.current_user == "tarek_admin")
    
    st.sidebar.title(f"🪞 مراية | {st.session_state.current_user}")
    if is_owner:
        st.sidebar.success("👑 حساب الأونر والمالك")
        
    menu_options = ["لوحة التحكم", "الثيرابست الذكي", "الجلسات الجماعية", "المتجر والألعاب"]
    if is_owner:
        menu_options.append("إدارة المنصة (الأونر) ⚙️")
        
    menu = st.sidebar.radio("التنقل بين الصفحات:", menu_options)
    
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
                    <h3>💰 رصيد محفظتك الرقمية:</h3>
                    <p style="font-size: 24px; color: #38bdf8;"><b>{c} كوينز</b> | 💎 <b>{d} ماسات</b></p>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "الثيرابست الذكي":
        st.title("🤖 الثيرابست الذكي (مساحتك الآمنة للحديث)")
        st.markdown("""
            <div class="fancy-card">
                <p>مرحباً بك في جلسة الدعم النفسي الذكية. هنا يمكنك التحدث بحرية تامة، وسيتذكر النظام سياق محادثاتك وأهدافك السابقة لمساعدتك بشكل أفضل.</p>
            </div>
        """, unsafe_allow_html=True)
        user_msg = st.text_input("اكتب رسالتك أو شعورك الآن:")
        if st.button("إرسال للثيرابست"):
            if user_msg:
                st.info(f"🤖 **رد الثيرابست الذكي:** أسمعك جيداً يا صديقي بخصوص ({user_msg}). دعنا نفكر سوياً كيف نتجاوز هذا الشعور بأمان وسلام داخلي.")

    elif menu == "الجلسات الجماعية":
        st.title("🎙️ الغرف الصوتية الجماعية (بسرية تامة)")
        st.markdown("""
            <div class="fancy-card">
                <p>شارك في غرف الاستماع والنقاش الجماعي باستخدام هويات مستعارة وبأمان مطلق.</p>
            </div>
        """, unsafe_allow_html=True)
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown('<div class="fancy-card"><h3>🎧 غرفة تفريغ الضغوط اليومية</h3><p>المشاركون: 14 شخص</p></div>', unsafe_allow_html=True)
            if st.button("انضم للصوتية 1"):
                st.success("تم انضمامك للغرفة بنجاح!")
        with col_g2:
            st.markdown('<div class="fancy-card"><h3>🌟 غرفة التأمل والسلام الداخلي</h3><p>المشاركون: 8 أشخاص</p></div>', unsafe_allow_html=True)
            if st.button("انضم للصوتية 2"):
                st.success("تم انضمامك للغرفة بنجاح!")

    elif menu == "المتجر والألعاب":
        st.title("🎨 متجر مراية والعناصر الرقمية")
        st.markdown("""
            <div class="fancy-card">
                <p>اقتنِ الإطارات الفاخرة، الدخلات المتحركة، وأرسل الهدايا لأصدقائك عبر معرفاتهم الفريدة.</p>
            </div>
        """, unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown('<div class="fancy-card"><h3>🦁 إطار زئير الأسد الأسطوري</h3><p>السعر: 50 كوينز</p></div>', unsafe_allow_html=True)
            if st.button("شراء الإطار"):
                st.success("تم شراء العنصر بنجاح وأُضيف لبروفايلك!")
        with col_s2:
            st.markdown('<div class="fancy-card"><h3>💎 باقة الماسات الترحيبية</h3><p>احصل على 100 ماسة إضافية</p></div>', unsafe_allow_html=True)
            if st.button("احصل على الماسات"):
                st.success("تم شحن الماسات بنجاح!")

    elif menu == "إدارة المنصة (الأونر) ⚙️" and is_owner:
        st.title("⚙️ لوحة تحكم المالك (طارق)")
        st.markdown('<div class="fancy-card"><p>لوحة التحكم السيادية الخاصة بالأونر لإدارة الحسابات، الأرصدة، والمستخدمين.</p></div>', unsafe_allow_html=True)
        
        st.subheader("📊 قاعدة بيانات المستخدمين المسجلين:")
        st.dataframe(users_df.drop(columns=["Password"]), use_container_width=True)
        
        st.subheader("💰 شحن رصيد فوري لأي مستخدم")
        t_id = st.text_input("أدخل معرف المستخدم (Login ID):")
        c_add = st.number_input("عدد الكوينز للإضافة:", min_value=0, value=100)
        d_add = st.number_input("عدد الماسات للإضافة:", min_value=0, value=50)
        
        if st.button("تنفيذ شحن الرصيد"):
            if t_id in users_df["Login_ID"].values:
                users_df.loc[users_df["Login_ID"] == t_id, "Coins"] += c_add
                users_df.loc[users_df["Login_ID"] == t_id, "Diamonds"] += d_add
                users_df.to_csv(USERS_FILE, index=False)
                st.success(f"تم شحن رصيد المستخدم ({t_id}) بنجاح!")
            else:
                st.error("المعرف غير موجود في النظام.")
