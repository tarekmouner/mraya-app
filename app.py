import streamlit as st
import pandas as pd
import os
import hashlib

# إعدادات الصفحة
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
        # إنشاء حساب الأونر تلقائياً وبأمان في قاعدة البيانات
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
        # التأكد من وجود حساب الأونر
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

# إدارة التنقل وحالة الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
if "view" not in st.session_state:
    st.session_state.view = "landing" # الخيارات: landing, login, register

# --- 1. الصفحة الرئيسية التسويقية (Landing Page) ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    
    # الهيدر والشريط العلوي
    col_logo, col_space, col_auth = st.columns([2, 5, 3])
    with col_logo:
        st.markdown("<h2 style='color: #2E5B88; margin:0;'>🪞 مــراية</h2>", unsafe_allow_html=True)
    with col_auth:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("تسجيل الدخول", use_container_width=True):
                st.session_state.view = "login"
                st.rerun()
        with c2:
            if st.button("حساب جديد", type="primary", use_container_width=True):
                st.session_state.view = "register"
                st.rerun()
                
    st.markdown("---")
    
    # البانر الرئيسي (Hero Section)
    st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 100%); border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: #1e3a8a; font-size: 42px;'>مساحتك الآمنة للتنفس، التعافي، والنمو الداخلي</h1>
            <p style='color: #475569; font-size: 20px; max-width: 800px; margin: 20px auto;'>
                منصة مراية تجمع بين الذكاء الاصطناعي المتطور للدعم النفسي الفردي المستمر، وبين المجتمعات التفاعلية والغرف الصوتية السرية التامة.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # زر جذب سريع في منتصف الصفحة
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("✨ ابدأ رحلتك النفسية مجاناً الآن ✨", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()
            
    st.markdown("### 🌟 ماذا تقدم لك منصة مراية؟")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # عرض المميزات كروت مبهرة
    f1, f2, f3 = st.columns(3)
    with f1:
        st.subheader("🤖 الثيرابست الذكي")
        st.write("جلسات فردية مغلقة مع ذكاء اصطناعي يحتفظ بذاكرة جلساتك السابقة لمتابعة حالتك النفسية بدقة دون نسيان أي تفصيل.")
    with f2:
        st.subheader("🎙️ غرف صوتية جماعية")
        st.write("شارك همومك واستمع للآخرين في جلسات صوتية جماعية بأسماء وهمية وأفاتار محمية لضمان الخصوصية المطلقة.")
    with f3:
        st.subheader("🎮 مجتمع وهدايا وتفاعل")
        st.write("متجر مخصص للتصاميم والأشكال، ألعاب تفاعلية، ونظام نقاط لكسب الكوينز والماس وتكريم أصدقائك.")

# --- 2. صفحة تسجيل الدخول ---
elif not st.session_state.logged_in and st.session_state.view == "login":
    st.button("⬅️ العودة للصفحة الرئيسية", on_click=lambda: st.session_state.update(view="landing"))
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<h2 style='text-align: center;'>🔑 تسجيل الدخول إلى مراية</h2>", unsafe_allow_html=True)
        login_input = st.text_input("معرف مراية (Login ID) أو البريد الإلكتروني:")
        login_pass = st.text_input("كلمة المرور:", type="password")
        
        if st.button("دخول", type="primary", use_container_width=True):
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
    st.button("⬅️ العودة للصفحة الرئيسية", on_click=lambda: st.session_state.update(view="landing"))
    
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown("<h2 style='text-align: center;'>✨ إنشاء حساب جديد في مراية</h2>", unsafe_allow_html=True)
        full_name = st.text_input("الاسم:")
        contact_info = st.text_input("البريد الإلكتروني أو رقم الهاتف:")
        new_pass = st.text_input("كلمة المرور:", type="password")
        confirm_pass = st.text_input("تأكيد كلمة المرور:", type="password")
        
        if st.button("إنشاء الحساب", type="primary", use_container_width=True):
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
                        st.success(f"تم إنشاء حسابك بنجاح! المعرف الخاص بك هو: {unique_id}")
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
        st.title("🏠 أهلاً بك في مراية")
        user_row = users_df[users_df["Login_ID"] == st.session_state.current_user]
        if not user_row.empty:
            c = user_row.iloc[0]["Coins"]
            d = user_row.iloc[0]["Diamonds"]
            st.info(f"💰 محفظتك: **{c} كوينز** | 💎 **{d} ماسات**")
            
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
