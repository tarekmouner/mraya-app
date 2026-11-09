import streamlit as st
import pandas as pd
import os
import hashlib

# إعدادات الصفحة الاحترافية
st.set_page_config(
    page_title="منصة مراية | مساحتك للتعافي والدعم النفسي",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# --- 1. الصفحة الرئيسية التسويقية الاحترافية والفاخرة ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    
    # حقن تصميم CSS لتعديل الشكل العام وجعل الأزرار والعناصر عصرية جداً
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; }
        .hero-box {
            text-align: center;
            padding: 70px 20px;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #3b82f6 100%);
            border-radius: 24px;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            margin-bottom: 40px;
        }
        .feature-card {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.04);
            height: 100%;
            transition: transform 0.3s ease;
            border: 1px solid #e2e8f0;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        </style>
    """, unsafe_allow_html=True)

    # الشريط العلوي مع اللوجو الفخم الجديد (أيقونة مراية عصرية متوهجة)
    col_logo, col_space, col_auth = st.columns([3, 4, 3])
    with col_logo:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: linear-gradient(45deg, #3b82f6, #8b5cf6); padding: 10px; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(59,130,246,0.3);">
                    <span style="font-size: 26px;">🪞</span>
                </div>
                <div>
                    <h2 style="color: #0f172a; margin: 0; font-weight: 900; letter-spacing: 0.5px;">مــرايـة</h2>
                    <span style="color: #64748b; font-size: 12px; font-weight: 600;">MRAYA PLATFORM</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_auth:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("تسجيل الدخول", use_container_width=True):
                st.session_state.view = "login"
                st.rerun()
        with c2:
            if st.button("حساب جديد ✨", type="primary", use_container_width=True):
                st.session_state.view = "register"
                st.rerun()
                
    st.markdown("<br>", unsafe_allow_html=True)
    
    # البانر الرئيسي (Hero Section) الفخم
    st.markdown("""
        <div class="hero-box">
            <h1 style='font-size: 48px; font-weight: 900; margin-bottom: 20px; color: #ffffff;'>عالمك الخاص للتعافي والنقاء النفسي</h1>
            <p style='font-size: 20px; max-width: 850px; margin: 0 auto 35px auto; line-height: 1.7; color: #cbd5e1;'>
                منصة <b>مراية</b> الحصن الرقمي الأكثر أماناً لسرية أفكارك ومشاعركس؛ نجمع بين الذكاء الاصطناعي المتطور للتشخيص والدعم النفسي الفردي، وبين المجتمعات الصوتية الجماعية السرية المحمية تماماً.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # زر البدء السريع
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🚀 ابدأ رحلتك النفسية مجاناً الآن", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0f172a; font-weight: 800;'>🌟 مميزات وحصريات عالم مراية</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px;'>مصممة بعناية فائقة لتلبي كافة احتياجاتك النفسية والاجتماعية في بيئة آمنة</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # شبكة المميزات الكبرى (كروت احترافية)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("""
            <div class="feature-card" style='border-right: 6px solid #3b82f6;'>
                <h3 style='color: #1d4ed8; margin-top: 0;'>🤖 الثيرابست الذكي ذو الذاكرة المستمرة</h3>
                <p style='color: #475569; font-size: 16px; line-height: 1.7;'>
                    لن تحتاج لإعادة شرح تفاصيل حياتك! معالج الذكاء الاصطناعي الخاص بنا يحتفظ بذاكرة ذكية متكاملة لكل جلساتك السابقة، ليتابع حالتك النفسية بدقة وكأنه معالج بشري يرافق خطوتك بخطوة.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
            <div class="feature-card" style='border-right: 6px solid #10b981;'>
                <h3 style='color: #047857; margin-top: 0;'>🎙️ الغرف الصوتية الجماعية السرية</h3>
                <p style='color: #475569; font-size: 16px; line-height: 1.7;'>
                    تكلم وفضفض بكل راحة واطمئنان. شارك في جلسات الدعم الجماعية الصوتية عبر (فيك أكونت) وبأفاتار محمية بالكامل تضمن لك سرية هويتك المطلقة وعدم معرفة أحد بك.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_f3, col_f4, col_f5 = st.columns(3)
    with col_f3:
        st.markdown("""
            <div class="feature-card" style='border-top: 5px solid #8b5cf6; text-align: center;'>
                <h4 style='color: #6d28d9;'>💎 محفظة الكوينز والماس</h4>
                <p style='color: #64748b; font-size: 15px; line-height: 1.6;'>نظام رصيد ثنائي متطور؛ كوينز للشحن الحقيقي، وماسات تكسبها من الألعاب والتفاعل لفتح جلسات ومميزات.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_f4:
        st.markdown("""
            <div class="feature-card" style='border-top: 5px solid #f59e0b; text-align: center;'>
                <h4 style='color: #b45309;'>🎨 متجر الإطارات والدخلات</h4>
                <p style='color: #64748b; font-size: 15px; line-height: 1.6;'>ميز هويتك بدخلات أسطورية (زئير الأسد، التنين) وإطارات متحركة، وأهد أصدقاءك لتتصدر لوحة الشرف والكرماء.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_f5:
        st.markdown("""
            <div class="feature-card" style='border-top: 5px solid #ef4444; text-align: center;'>
                <h4 style='color: #b91c1c;'>🛡️ أمان وحماية مطلقة</h4>
                <p style='color: #64748b; font-size: 15px; line-height: 1.6;'>تشفير شامل للبيانات، نظام بلاغات آلي صارم ضد أي تجاوز، مع حفظ تامة لحقوق الأرصدة المالية للأعضاء.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-weight: 500;'>جميع الحقوق محفوظة منصة مراية © 2026 | مساحتك الآمنة دائماً</p>", unsafe_allow_html=True)

# --- 2. صفحة تسجيل الدخول ---
elif not st.session_state.logged_in and st.session_state.view == "login":
    if st.button("⬅️ العودة للصفحة الرئيسية"):
        st.session_state.view = "landing"
        st.rerun()
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<h2 style='text-align: center; color: #1e293b;'>🔑 تسجيل الدخول إلى مراية</h2>", unsafe_allow_html=True)
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
        st.markdown("<h2 style='text-align: center; color: #1e293b;'>✨ إنشاء حساب جديد في مراية</h2>", unsafe_allow_html=True)
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

# --- 4. داخل المنصة بعد تسجيل الدخول ---
else:
    users_df = pd.read_csv(USERS_FILE)
    is_owner = (st.session_state.current_user == "tarek_admin")
    
    st.sidebar.title(f"🪞 مراية | {st.session_state.current_user}")
    if is_owner:
        st.sidebar.success("👑 حساب الأونر والمالك")
        
    menu_options = ["لوحة التحكم", "الثيرابست الذكي", "الجلسات الجماعية", "المتجر والألعاب"]
    if is_owner:
        menu_options.append("إدارة المنصة (الأونر) ⚙️")
        
    menu = st.sidebar.radio("التنقل:", menu_options)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.view = "landing"
        st.rerun()

    if menu == "لوحة التحكم":
        st.title("🏠 أهلاً بك في مساحتك الآمنة")
        user_row = users_df[users_df["Login_ID"] == st.session_state.current_user]
        if not user_row.empty:
            c = user_row.iloc[0]["Coins"]
            d = user_row.iloc[0]["Diamonds"]
            st.info(f"💰 رصيد محفظتك: **{c} كوينز** | 💎 **{d} ماسات**")
            
    elif menu == "إدارة المنصة (الأونر) ⚙️" and is_owner:
        st.title("⚙️ لوحة تحكم المالك (طارق)")
        st.dataframe(users_df.drop(columns=["Password"]))
        
        st.subheader("شحن رصيد مستخدم")
        t_id = st.text_input("معرف المستخدم (Login ID):")
        c_add = st.number_input("الكوينز:", min_value=0, value=100)
        d_add = st.number_input("الماسات:", min_value=0, value=50)
        
        if st.button("تأكيد الشحن"):
            if t_id in users_df["Login_ID"].values:
                users_df.loc[users_df["Login_ID"] == t_id, "Coins"] += c_add
                users_df.loc[users_df["Login_ID"] == t_id, "Diamonds"] += d_add
                users_df.to_csv(USERS_FILE, index=False)
                st.success("تم الشحن بنجاح!")
            else:
                st.error("المستخدم غير موجود.")
