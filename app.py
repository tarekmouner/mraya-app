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

# إدارة التنقل وحالة الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
if "view" not in st.session_state:
    st.session_state.view = "landing"

# --- 1. الصفحة الرئيسية التسويقية المجهزة بالكامل (Landing Page) ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    
    # الهيدر والشريط العلوي الشيك
    col_logo, col_space, col_auth = st.columns([3, 4, 3])
    with col_logo:
        st.markdown("<h1 style='color: #2E5B88; margin:0; font-weight: bold;'>🪞 مــراية</h1>", unsafe_allow_html=True)
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
                
    st.markdown("---")
    
    # البانر الرئيسي الترحيبي والتسويقي
    st.markdown("""
        <div style='text-align: center; padding: 50px 20px; background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 100%); border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 40px;'>
            <h1 style='color: #0f172a; font-size: 45px; font-weight: 800; margin-bottom: 15px;'>عالمك الخاص للتعافي والنقاء النفسي</h1>
            <p style='color: #334155; font-size: 22px; max-width: 850px; margin: 0 auto 30px auto; line-height: 1.6;'>
                منصة <b>"مراية"</b> هي المساحة الآمنة الأولى التي تمنحك صوتاً وحصناً لسرية أفكارك، تجمع بين ذكاء الدعم النفسي الفردي المستمر وتفاعل المجتمعات الصوتية السرية بأمان مطلق.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # زر الدعوة والبدء في منتصف الصفحة
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🚀 ابدأ أولى جلساتك مجاناً الآن", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1e293b;'>🌟 مميزات وحصريات عالم "مراية"</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px;'>كل ما تحتاجه لرحلتك النفسية في مكان واحد</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # الصف الأول للمميزات (المميزات الرئيسية)
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""
            <div style='background-color: #ffffff; padding: 25px; border-radius: 15px; border-right: 6px solid #3b82f6; box-shadow: 0 2px 10px rgba(0,0,0,0.05); height: 100%;'>
                <h3 style='color: #1d4ed8; margin-top: 0;'>🤖 الثيرابست الذكي ذو الذاكرة المستمرة</h3>
                <p style='color: #475569; font-size: 16px; line-height: 1.6;'>
                    لا داعي لإعادة شرح قصتك في كل مرة! يتحدث معالج الذكاء الاصطناعي معك في جلسات فردية سرية جداً، مسترجعاً تفاصيل جلساتك السابقة لمتابعة تطورك النفسي خطوة بخطوة وكأنه مرافقك الشخصي.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
            <div style='background-color: #ffffff; padding: 25px; border-radius: 15px; border-right: 6px solid #10b981; box-shadow: 0 2px 10px rgba(0,0,0,0.05); height: 100%;'>
                <h3 style='color: #047857; margin-top: 0;'>🎙️ الغرف الصوتية الجماعية السرية</h3>
                <p style='color: #475569; font-size: 16px; line-height: 1.6;'>
                    تكلم وفضفض بحرية! انضم إلى جلسات الدعم الجماعية الفويس بأسماء مستعارة وأفاتار محمية بالكامل. افتح أو أغلق الميكروفون وقتما تشاء دون إفشاء هويتك الحقيقية إطلاقاً.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # الصف الثاني للمميزات (المتجر، الألعاب، والأمان)
    f3, f4, f5 = st.columns(3)
    with f3:
        st.markdown("""
            <div style='background-color: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #8b5cf6; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center;'>
                <h4 style='color: #6d28d9;'>💎 محفظة الكوينز والماس</h4>
                <p style='color: #64748b; font-size: 15px;'>نظام رصيد مزدوج؛ اشحن الكوينز بآمان واكسب الماسات من تفاعلك لفتح مميزات حصرية وجلسات إضافية.</p>
            </div>
        """, unsafe_allow_html=True)
    with f4:
        st.markdown("""
            <div style='background-color: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center;'>
                <h4 style='color: #b45309;'>🎨 متجر الإطارات والدخلات</h4>
                <p style='color: #64748b; font-size: 15px;'>ميز حسابك بدخلات أسطورية (زئير الأسد، التنين) وإطارات متحركة، وأهدِ أصدقاءك لتظهر في لوحة الكرماء!</p>
            </div>
        """, unsafe_allow_html=True)
    with f5:
        st.markdown("""
            <div style='background-color: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #ef4444; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center;'>
                <h4 style='color: #b91c1c;'>🛡️ أمان وحماية مطلقة</h4>
                <p style='color: #64748b; font-size: 15px;'>تشفير كامل للبيانات، نظام بلاغات آلي ضد أي تجاوز، وحماية تضمن سرية أسرارك ورصيدك المالي بدقة.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    
    # الفوتر النهائي
    st.markdown("<p style='text-align: center; color: #94a3b8;'>جميع الحقوق محفوظة منصة مراية © 2026 | مساحتك الآمنة دائماً</p>", unsafe_allow_html=True)

# --- 2. صفحة تسجيل الدخول ---
elif not st.session_state.logged_in and st.session_state.view == "login":
    st.button("⬅️ العودة للصفحة الرئيسية", on_click=lambda: st.session_state.update(view="landing"))
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<h2 style='text-align: center; color: #1e293b;'>🔑 تسجيل الدخول إلى مراية</h2>", unsafe_allow_html=True)
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
        st.markdown("<h2 style='text-align: center; color: #1e293b;'>✨ إنشاء حساب جديد في مراية</h2>", unsafe_allow_html=True)
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
