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

# تخصيص ثيم مريح للعين، اتجاه عربي سليم (RTL)، وتكبير الخطوط ووضوحها
st.markdown("""
    <style>
    /* فرض اتجاه اللغة العربية من اليمين لليسار لجميع العناصر */
    html, body, [class*="css"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* خلفية هادئة وناعمة جداً مريحة للعين */
    .main { background-color: #0f172a; color: #f1f5f9; }
    .stApp { background: linear-gradient(135deg, #090d16 0%, #111827 50%, #0f172a 100%); color: #f1f5f9; }
    
    /* تكبير وتوضيح الخطوط لراحة القراءة */
    body, p, span, li, label, div {
        font-size: 18px !important;
        color: #e2e8f0 !important;
        line-height: 1.9 !important;
    }
    
    /* أزرار منسقة وراقية بدون ألوان فاقعة وبدون أبيض */
    .stButton>button {
        background: linear-gradient(135deg, #1e40af 0%, #6d28d9 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
        box-shadow: 0 0 12px rgba(96, 165, 250, 0.3) !important;
    }

    /* كروت محتوى فخمة وناعمة */
    .content-card {
        background-color: rgba(30, 41, 59, 0.7);
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        text-align: right !important;
    }
    
    /* عناوين واضحة ومريحة */
    .section-title {
        color: #60a5fa;
        font-weight: 900;
        font-size: 30px !important;
        text-align: center;
        margin-top: 50px;
        margin-bottom: 25px;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.2);
    }
    
    /* صندوق البانر العلوي */
    .hero-banner-container {
        text-align: center;
        padding: 20px;
        background: rgba(15, 23, 42, 0.9);
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        border: 1px solid rgba(109, 40, 217, 0.3);
        margin-bottom: 35px;
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
    
    # الشريط العلوي مع اللوجو الفخم الخاص بك
    col_logo, col_space, col_auth = st.columns([4, 4, 2])
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=280)
        else:
            st.warning("⚠️ يرجى التأكد من رفع صورة logo.png في مستودع GitHub في نفس مجلد الملفات الرئيسي")
            
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
    
    # عرض الصورة الأساسية كبانر تسويقي فخم في واجهة الموقع
    if os.path.exists("logo.png"):
        st.markdown('<div class="hero-banner-container">', unsafe_allow_html=True)
        st.image("logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
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
            <p style="font-size: 20px !important; color: #f1f5f9 !important; line-height: 1.9; margin: 0;">
                لأننا نعلم أن الحديث عن الأمور الشخصية ليس سهلًا دائمًا. أحيانًا تحتاج إلى الكتابة بدلًا من الكلام، وأحيانًا تفضل التحدث بصوتك، وأحيانًا لا تريد سوى أن تجد مساحة تستطيع فيها التعبير عن نفسك دون الشعور بالإحراج.<br><br>
                <b>لهذا لم نصمم مرايا لتكون مجرد نافذة محادثة، بل تجربة متكاملة تمنحك خيارات متعددة للتواصل والتعبير والتطور.</b>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # مميزات المنصة
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
            <div class="content-card">
                <ul style='color: #e2e8f0; font-size: 18px !important; line-height: 2.2; list-style-type: none; padding: 0;'>
                    <li>🔹 مساحة شخصية مستقلة لكل مستخدم.</li>
                    <li>🔹 جلسات فردية خاصة مصممة حولك.</li>
                    <li>🔹 محادثات كتابية، صوتية، ومرئية متطورة.</li>
                    <li>🔹 مساعد ذكي يتذكر سياق محادثاتك السابقة.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
            <div class="content-card">
                <ul style='color: #e2e8f0; font-size: 18px !important; line-height: 2.2; list-style-type: none; padding: 0;'>
                    <li>🔹 إمكانية اختيار المشاركة المجتمعية أو البقاء بمفردك.</li>
                    <li>🔹 نظام عضويات ومزايا قابل للتخصيص.</li>
                    <li>🔹 تجربة شخصية قابلة للتطوير والتغيير.</li>
                    <li>🔹 مكافآت، هدايا، وفعاليات تفاعلية.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # مساراتك وأدواتك
    st.markdown("<h2 class='section-title'>مساراتك وأدواتك داخل المنصة</h2>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #60a5fa; font-size: 22px !important; margin-bottom: 15px;'>🧘 جلسات فردية</h3>
                <p style='color: #cbd5e1; font-size: 17px !important; line-height: 1.8;'>
                    كل شخص مختلف، وكل تجربة تستحق الاهتمام. ابدأ جلسة فردية خاصة بك ومشاركة ما تشعر به ومناقشة تحدياتك في سرية تامة.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #34d399; font-size: 22px !important; margin-bottom: 15px;'>🎙️ طرق تواصل متعددة</h3>
                <p style='color: #cbd5e1; font-size: 17px !important; line-height: 1.8;'>
                    <b>كتابية:</b> اكتب أفكارك بحرية.<br><b>صوتية:</b> تحدث بصوتك لتجربة طبيعية.<br><b>مرئية:</b> تواصل مرئي ضمن التجارب المدعومة.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #a78bfa; font-size: 22px !important; margin-bottom: 15px;'>🧠 ذاكرة ذكية</h3>
                <p style='color: #cbd5e1; font-size: 17px !important; line-height: 1.8;'>
                    لا تبدأ من الصفر أبداً. ذاكرتك الشخصية تساعد المساعد الذكي على استيعاب السياق السابق والأهداف والتحديات.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # مجتمع مراية
    st.markdown("""
        <div class="content-card" style="border-right: 6px solid #34d399; margin-top: 20px;">
            <h3 style='color: #34d399; font-size: 22px !important; margin-top: 0; margin-bottom: 15px;'>👥 مجتمع مراية | لست مضطرًا للبقاء وحدك</h3>
            <p style='color: #e2e8f0; font-size: 18px !important; line-height: 1.9;'>
                توفير تجربة مجتمعية اختيارية تتيح لك المشاركة في جلسات جماعية صوتية مع أشخاص آخرين باستخدام <b>هويات مستعارة</b>. مشاركة اختيارية بالكامل، لا اسم حقيقي يظهر، لا تظهر جلساتك الفردية أبداً، مع نظام بلاغات ومراجعة صارم.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # الشخصية الرقمية والمتجر
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #fbbf24; font-size: 22px !important; margin-bottom: 15px;'>🎨 شخصيتك الرقمية والمتجر</h3>
                <p style='color: #cbd5e1; font-size: 17px !important; line-height: 1.8;'>
                    طور مظهر هويتك بإطارات ثابتة ومتحركة، أشكال وألوان مميزة للأسماء، تصاميم معرفات ID، وخلفيات شخصية ومؤثرات صوتية وبصرية.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with c_s2:
        st.markdown("""
            <div class="content-card">
                <h3 style='color: #f472b6; font-size: 22px !important; margin-bottom: 15px;'>🎁 الهدايا ونظام العملات</h3>
                <p style='color: #cbd5e1; font-size: 17px !important; line-height: 1.8;'>
                    أرسل هدية لأي صديق بمعرفه الفريد لتظهر في لوحة أكثر الأصدقاء كرمًا.<br>
                    <b>الكوينز (COINS):</b> للشحن والمزايا المدفوعة.<br>
                    <b>الماسات (DIAMONDS):</b> مكاسب الفعاليات والأنشطة.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # الأمان والرؤية والرسالة
    st.markdown("""
        <div class="content-card" style="background: rgba(15, 23, 42, 0.95); border-right: 6px solid #60a5fa;">
            <h3 style='color: #ffffff; font-size: 22px !important; margin-top: 0; margin-bottom: 15px;'>🛡️ الأمان والخصوصية والرؤية</h3>
            <p style='color: #e2e8f0; font-size: 18px !important; line-height: 1.9;'>
                <b>رؤيتنا:</b> أن تصبح مراية مساحة رقمية رائدة تمنح الإنسان فرصة أفضل للتعبير عن نفسه وفهم مشاعره.<br>
                <b>رسالتنا:</b> توفير تجربة تجمع بين الذكاء الاصطناعي والتكنولوجيا والتواصل الإنساني ببيئة تراعي الخصوصية التامة.<br>
                نحن نؤمن أن الثقة أساس المشاعر؛ حسابات مستقلة، معرفات فريدة، وفصل تام لبيانات الجلسات الشخصية.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # قسم الأسئلة الشائعة (FAQ)
    st.markdown("<h2 class='section-title'>الأسئلة الشائعة</h2>", unsafe_allow_html=True)
    
    with st.expander("❓ هل استخدام مراية مجاني؟"):
        st.write("تتيح مراية عددًا من الجلسات المجانية الأولية، وبعد استهلاكها يمكنك اختيار إحدى الباقات المتاحة أو استخدام الرصيد المؤهل لفتح جلسات إضافية.")
    with st.expander("❓ هل يجب عليّ المشاركة في الجلسات الجماعية؟"):
        st.write("لا. الجلسات الفردية هي الأساس، والمشاركة المجتمعية اختيارية بالكامل.")
    with st.expander("❓ هل أستطيع التحدث بدلًا من الكتابة؟"):
        st.write("نعم، تتضمن التجربة إمكانية المحادثات الصوتية، مع إمكانية دعم الفيديو وفق الخطة والقدرات المتاحة.")
    with st.expander("❓ هل يتذكر المساعد الذكي محادثاتي السابقة؟"):
        st.write("نعم، يستفيد من الذاكرة الشخصية المرتبطة بحسابك، وفق إعدادات الموافقة والاحتفاظ بالبيانات.")
    with st.expander("❓ هل يستطيع الآخرون رؤية جلساتي؟"):
        st.write("لا تظهر الجلسات الفردية للمستخدمين الآخرين إطلاقاً. وتُدار صلاحيات الوصول وفق سياسة الخصوصية.")
    with st.expander("❓ هل مراية بديل عن الطبيب النفسي؟"):
        st.write("مراية منصة للدعم والمساندة الرقمية باستخدام الذكاء الاصطناعي، وليست بديلًا عن التشخيص أو العلاج لدى متخصص مؤهل. وفي حالات الطوارئ أو خطر إيذاء النفس يجب التواصل مع خدمات الطوارئ أو مختص بشري فورًا.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر الخاتمة
    col_end1, col_end2, col_end3 = st.columns([1, 2, 1])
    with col_end2:
        if st.button("أنشئ حسابك الآن مجانًا", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #60a5fa; font-weight: bold;'>MIRAYA — Your Space. Your Story. Your Reflection.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px;'>جميع الحقوق محفوظة منصة مراية © 2026</p>", unsafe_allow_html=True)

# --- 2. صفحة تسجيل الدخول ---
elif not st.session_state.logged_in and st.session_state.view == "login":
    if st.button("⬅️ العودة للصفحة الرئيسية"):
        st.session_state.view = "landing"
        st.rerun()
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<h2 style='text-align: center; color: #60a5fa;'>🔑 تسجيل الدخول إلى مراية</h2>", unsafe_allow_html=True)
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
        st.markdown("<h2 style='text-align: center; color: #60a5fa;'>✨ إنشاء حساب جديد في مراية</h2>", unsafe_allow_html=True)
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
