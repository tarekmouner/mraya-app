import streamlit as st
import pandas as pd
import os
import hashlib

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة مراية | مساحتك الخاصة لفهم نفسك",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تخصيص ثيم الألوان وإلغاء اللون الأبيض تماماً من الأزرار وتوحيد الهوية البصرية
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f8fafc; }
    .stApp { background: linear-gradient(135deg, #0b0f19 0%, #1e1b4b 50%, #0f172a 100%); color: #ffffff; }
    
    /* تعديل الأزرار لمنع ظهور اللون الأبيض نهائياً وتخصيص ألوان متناسقة نيون/بنفسجي */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
        color: #f3f4f6 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5) !important;
    }
    .stButton>button:focus {
        color: #ffffff !important;
    }

    .hero-banner-container {
        text-align: center;
        padding: 15px;
        background: rgba(15, 23, 42, 0.85);
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin-bottom: 30px;
    }
    .content-card {
        background-color: rgba(30, 41, 59, 0.75);
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
    }
    .section-title {
        color: #38bdf8;
        font-weight: 900;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 20px;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

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

# --- 1. الصفحة الرئيسية التسويقية الكاملة (Landing Page) ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    
    # الشريط العلوي مع اللوجو الجديد (الصورة الأساسية)
    col_logo, col_space, col_auth = st.columns([4, 4, 2])
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=280)
        else:
            st.markdown("<h2 style='color: #38bdf8;'>🪞 مــرايــا | MIRAYA</h2>", unsafe_allow_html=True)
            
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
    
    # عرض اللوجو/البانر الأساسي الضخم في واجهة الموقع (نفس الصورة الجديدة)
    if os.path.exists("logo.png"):
        st.markdown('<div class="hero-banner-container">', unsafe_allow_html=True)
        st.image("logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    elif os.path.exists("banner.png"):
        st.markdown('<div class="hero-banner-container">', unsafe_allow_html=True)
        st.image("banner.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="hero-banner-container">
                <h1 style='font-size: 42px; font-weight: 900; margin-bottom: 15px; color: #ffffff;'>احكي. عبّر. اكتشف. وتطوّر.[cite: 5]</h1>
                <p style='font-size: 19px; color: #cbd5e1;'>مرحبًا بك في مرايا، مساحة رقمية صُممت لتكون أقرب مكان يمكنك اللجوء إليه[cite: 5].</p>
            </div>
        """, unsafe_allow_html=True)
    
    # أزرار التوجيه السريع
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        ba, bb = st.columns(2)
        with ba:
            if st.button("ابدأ رحلتك مجانًا", type="primary", use_container_width=True):
                st.session_state.view = "register"
                st.rerun()
        with bb:
            if st.button("اكتشف مرايا", use_container_width=True):
                pass
                
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # لماذا مرايا؟
    st.markdown("<h2 class='section-title'>لماذا مرايا؟</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="content-card" style="text-align: center;">
            <p style="font-size: 18px; color: #e2e8f0; line-height: 1.8; margin: 0;">
                لاننا نعلم أن الحديث عن الأمور الشخصية ليس سهلًا دائمًا[cite: 5]. أحيانًا تحتاج إلى الكتابة بدلًا من الكلام، وأحيانًا تفضل التحدث بصوتك، وأحيانًا لا تريد سوى أن تجد مساحة تستطيع فيها التعبير عن نفسك دون الشعور بالإحراج[cite: 5].<br>
                <b>لهذا لم نصمم مرايا لتكون مجرد نافذة محادثة، بل تجربة متكاملة تمنحك خيارات متعددة للتواصل والتعبير والتطور[cite: 5].</b>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # مميزات المنصة
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
            <div class="content-card">
                <ul style='color: #cbd5e1; font-size: 16px; line-height: 2; list-style-type: none; padding: 0;'>
                    <li>🔹 مساحة شخصية مستقلة لكل مستخدم[cite: 5].</li>
                    <li>🔹 جلسات فردية خاصة مصممة حولك[cite: 5].</li>
                    <li>🔹 محادثات كتابية، صوتية، ومرئية متطورة[cite: 5].</li>
                    <li>🔹 مساعد ذكي يتذكر سياق محادثاتك السابقة[cite: 5].</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
            <div class="content-card">
                <ul style='color: #cbd5e1; font-size: 16px; line-height: 2; list-style-type: none; padding: 0;'>
                    <li>🔹 إمكانية اختيار المشاركة المجتمعية أو البقاء بمفردك[cite: 5].</li>
                    <li>🔹 نظام عضويات ومزايا قابل للتخصيص[cite: 5].</li>
                    <li>🔹 تجربة شخصية قابلة للتطوير والتغيير[cite: 5].</li>
                    <li>🔹 مكافآت، هدايا، وفعاليات تفاعلية[cite: 5].</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # مساراتك وأدواتك
    st.markdown("<h2 class='section-title'>مساراتك وأدواتك داخل المنصة</h2>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #38bdf8;'>🧘 جلسات فردية</h3>
                <p style='color: #94a3b8; font-size: 15px; line-height: 1.7;'>
                    كل شخص مختلف، وكل تجربة تستحق الاهتمام[cite: 5]. ابدأ جلسة فردية خاصة بك ومشاركة ما تشعر به ومناقشة تحدياتك في سرية تامة[cite: 5].
                </p>
            </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #34d399;'>🎙️ طرق تواصل متعددة</h3>
                <p style='color: #94a3b8; font-size: 15px; line-height: 1.7;'>
                    <b>كتابية:</b> اكتب أفكارك بحرية[cite: 5].<br><b>صوتية:</b> تحدث بصوتك لتجربة طبيعية[cite: 5].<br><b>مرئية:</b> تواصل مرئي ضمن التجارب المدعومة[cite: 5].
                </p>
            </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #a78bfa;'>🧠 ذاكرة ذكية</h3>
                <p style='color: #94a3b8; font-size: 15px; line-height: 1.7;'>
                    لا تبدأ من الصفر أبداً[cite: 5]. ذاكرتك الشخصية تساعد المساعد الذكي على استيعاب السياق السابق والأهداف والتحديات[cite: 5].
                </p>
            </div>
        """, unsafe_allow_html=True)

    # مجتمع مراية
    st.markdown("""
        <div class="content-card" style="border-right: 6px solid #34d399; margin-top: 20px;">
            <h3 style='color: #34d399; margin-top: 0;'>👥 مجتمع مراية | لست مضطرًا للبقاء وحدك[cite: 5]</h3>
            <p style='color: #cbd5e1; font-size: 16px; line-height: 1.8;'>
                توفير تجربة مجتمعية اختيارية تتيح لك المشاركة في جلسات جماعية صوتية مع أشخاص آخرين باستخدام <b>هويات مستعارة</b>[cite: 5]. مشاركة اختيارية بالكامل، لا اسم حقيقي يظهر، لا تظهر جلساتك الفردية أبداً، مع نظام بلاغات ومراجعة صارم[cite: 5].
            </p>
        </div>
    """, unsafe_allow_html=True)

    # الشخصية الرقمية والمتجر
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #fbbf24;'>🎨 شخصيتك الرقمية والمتجر</h3>
                <p style='color: #94a3b8; font-size: 15px; line-height: 1.7;'>
                    طور مظهر هويتك بإطارات ثابتة ومتحركة، أشكال وألوان مميزة للأسماء، تصاميم معرفات ID، وخلفيات شخصية ومؤثرات صوتية وبصرية[cite: 5].
                </p>
            </div>
        """, unsafe_allow_html=True)
    with c_s2:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #f472b6;'>🎁 الهدايا ونظام العملات</h3>
                <p style='color: #94a3b8; font-size: 15px; line-height: 1.7;'>
                    أرسل هدية لأي صديق بمعرفه الفريد لتظهر في لوحة أكثر الأصدقاء كرمًا[cite: 5].<br>
                    <b>الكوينز (COINS):</b> للشحن والمزايا المدفوعة[cite: 5].<br>
                    <b>الماسات (DIAMONDS):</b> مكاسب الفعاليات والأنشطة[cite: 5].
                </p>
            </div>
        """, unsafe_allow_html=True)

    # الأمان والرؤية والرسالة
    st.markdown("""
        <div class="content-card" style="background: rgba(15, 23, 42, 0.9); border-left: 6px solid #38bdf8;">
            <h3 style='color: #ffffff; margin-top: 0;'>🛡️ الأمان والخصوصية والرؤية</h3>
            <p style='color: #cbd5e1; font-size: 16px; line-height: 1.8;'>
                <b>رؤيتنا:</b> أن تصبح مراية مساحة رقمية رائدة تمنح الإنسان فرصة أفضل للتعبير عن نفسه وفهم مشاعره[cite: 5].<br>
                <b>رسالتنا:</b> توفير تجربة تجمع بين الذكاء الاصطناعي والتكنولوجيا والتواصل الإنساني ببيئة تراعي الخصوصية التامة[cite: 5].<br>
                نحن نؤمن أن الثقة أساس المشاعر؛ حسابات مستقلة، معرفات فريدة، وفصل تام لبيانات الجلسات الشخصية[cite: 5].
            </p>
        </div>
    """, unsafe_allow_html=True)

    # قسم الأسئلة الشائعة (FAQ)
    st.markdown("<h2 class='section-title'>الأسئلة الشائعة</h2>", unsafe_allow_html=True)
    
    with st.expander("❓ هل استخدام مراية مجاني؟"):
        st.write("تتيح مراية عددًا من الجلسات المجانية الأولية، وبعد استهلاكها يمكنك اختيار إحدى الباقات المتاحة أو استخدام الرصيد المؤهل لفتح جلسات إضافية[cite: 5].")
    with st.expander("❓ هل يجب عليّ المشاركة في الجلسات الجماعية؟"):
        st.write("لا. الجلسات الفردية هي الأساس، والمشاركة المجتمعية اختيارية بالكامل[cite: 5].")
    with st.expander("❓ هل أستطيع التحدث بدلًا من الكتابة؟"):
        st.write("نعم، تتضمن التجربة إمكانية المحادثات الصوتية، مع إمكانية دعم الفيديو وفق الخطة والقدرات المتاحة[cite: 5].")
    with st.expander("❓ هل يتذكر المساعد الذكي محادثاتي السابقة؟"):
        st.write("نعم، يستفيد من الذاكرة الشخصية المرتبطة بحسابك، وفق إعدادات الموافقة والاحتفاظ بالبيانات[cite: 5].")
    with st.expander("❓ هل يستطيع الآخرون رؤية جلساتي؟"):
        st.write("لا تظهر الجلسات الفردية للمستخدمين الآخرين إطلاقاً[cite: 5]. وتُدار صلاحيات الوصول وفق سياسة الخصوصية[cite: 5].")
    with st.expander("❓ هل مراية بديل عن الطبيب النفسي؟"):
        st.write("مراية منصة للدعم والمساندة الرقمية باستخدام الذكاء الاصطناعي، وليست بديلًا عن التشخيص أو العلاج لدى متخصص مؤهل[cite: 5]. وفي حالات الطوارئ أو خطر إيذاء النفس يجب التواصل مع خدمات الطوارئ أو مختص بشري فورًا[cite: 5].")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر الخاتمة
    col_end1, col_end2, col_end3 = st.columns([1, 2, 1])
    with col_end2:
        if st.button("أنشئ حسابك الآن مجانًا", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #38bdf8; font-weight: bold;'>MIRAYA — Your Space. Your Story. Your Reflection.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>جميع الحقوق محفوظة منصة مراية © 2026</p>", unsafe_allow_html=True)

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
