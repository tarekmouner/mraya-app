import streamlit as st
import pandas as pd
import os
import hashlib

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة مراية | مساحتك الآمنة للتعافي والدعم النفسي",
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

# --- 1. الصفحة الرئيسية التسويقية الاحترافية العميقة ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    
    # حقن تصميم CSS فاخر يوضح القوة التسويقية والجاذبية البصرية
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; }
        .hero-banner {
            text-align: center;
            padding: 90px 20px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0284c7 100%);
            border-radius: 28px;
            color: white;
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
            margin-bottom: 40px;
        }
        .market-card {
            background-color: #ffffff;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.05);
            height: 100%;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        .market-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        }
        .badge-sales {
            background: #e0f2fe;
            color: #0369a1;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
            display: inline-block;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # الهيدر العلوي
    col_logo, col_space, col_auth = st.columns([3, 4, 3])
    with col_logo:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="background: linear-gradient(45deg, #0284c7, #10b981); padding: 12px; border-radius: 14px; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(2,132,199,0.3);">
                    <span style="font-size: 28px;">🪞</span>
                </div>
                <div>
                    <h1 style="color: #0f172a; margin: 0; font-weight: 900; font-size: 26px; letter-spacing: 0.5px;">مــرايـة</h1>
                    <span style="color: #64748b; font-size: 13px; font-weight: 700; letter-spacing: 1px;">المساحة الآمنة للتعافي والروح</span>
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
    
    # البانر الرئيسي التسويقي الجلاد
    st.markdown("""
        <div class="hero-banner">
            <span class="badge-sales">🔥 المنصة الأولى من نوعها للتعافي النفسي والمجتمعي الآمن</span>
            <h1 style='font-size: 52px; font-weight: 900; margin-bottom: 20px; color: #ffffff; line-height: 1.2;'>لأن أصدق حديث هو ما تقوله لنفسك.. ولأنك تستحق سلاماً داخلياً لا يشاركه أحد معك!</h1>
            <p style='font-size: 21px; max-width: 950px; margin: 0 auto 35px auto; line-height: 1.8; color: #cbd5e1;'>
                أهلاً بك في <b>"مراية"</b>؛ الحصن الرقمي الأقوى عالمياً الذي يجمع لك بين معالج ذكاء اصطناعي فاهم لحالتك بذاكرة لا تنسى، وبين مجتمعات صوتية سرية تفرغ فيها ضغوطك دون أدنى قلق أو خوف من الأحكام الخارجية.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # زر الدعوة والتحويل (Call to Action)
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🚀 انضم الآن واحصل على جلساتك المجانية الفورية", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0f172a; font-weight: 900; font-size: 34px;'>🌟 لماذا يختار الملايين منصة "مراية" لرحلة علاجهم النفسي؟</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 19px;'>إليك القائمة الكاملة للمميزات الاستثنائية التي تم هندستها خصيصاً لتمنحك قيمة لا تقدر بثمن</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # كروت مميزات تسويقية ضخمة وعميقة جداً
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("""
            <div class="market-card" style='border-right: 8px solid #0284c7;'>
                <h3 style='color: #0369a1; margin-top: 0; font-size: 24px; font-weight: 800;'>🤖 1. الثيرابست الذكي الخارق (ذاكرة علاجية لا تنتهي)</h3>
                <p style='color: #475569; font-size: 17px; line-height: 1.9;'>
                    انسَ تماماً العناء المعتاد في إعادة شرح مشاكلك من الصفر! معالج الذكاء الاصطناعي في "مراية" مزود بـ <b>ذاكرة دائمة ومستمرة</b> لجميع جلساتك السابقة (الأولى، الثانية، العاشرة..). حين تفتح جلسة جديدة، يستأنف معك الحوار بنفس النبرة والفهم والعمق النفسي كأنه طبيب بشري يرافق خطواتك لأشهر طويلة، مدركاً أبعاد أزماتك دون أي مجهود إضافي منك.
                </p>
                <ul style='color: #334155; font-size: 16px; line-height: 1.8; margin-top: 15px;'>
                    <li>متابعة دقيقة لتطور حالتك المزاجية والنفسية يوماً بي يوم.</li>
                    <li>تخزين مشفر ومغلق تماماً لا يططلع عليه أي إنسان نهائياً.</li>
                    <li>إجابات احترافية مبنية على أحدث قواعد الدعم النفسي العالمي.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
            <div class="market-card" style='border-right: 8px solid #10b981;'>
                <h3 style='color: #047857; margin-top: 0; font-size: 24px; font-weight: 800;'>🎙️ 2. الغرف الصوتية الجماعية (أمان مطلق وسرية تامة)</h3>
                <p style='color: #475569; font-size: 17px; line-height: 1.8;'>
                    هل تحب أن تشارك همومك وتستمع لتجارب الآخرين دون أن يعرفك أحد؟ انضم فوراً إلى <b>الغرف الصوتية الفويس الجماعية</b>. الدخول يتم عبر حسابات وهمية وأفاتار محمية بالكامل تضمن عدم كشف اسمك أو هويتك الحقيقية بنسبة 100%. فضفض، اضحك، افرغ طاقتك، واعتمد على أقوى أنظمة الرقابة والبلاغات الفورية التي تضمن بيئة نقية تماماً من أي تجاوز.
                </p>
                <ul style='color: #334155; font-size: 16px; line-height: 1.8; margin-top: 15px;'>
                    <li>مطلق الحرية في فتح وإغلاق الميكروفون والتحكم بمشاركتك.</li>
                    <li>أفواتير وأسماء وهمية تحميك من أي إحراج اجتماعي.</li>
                    <li>أنظمة حظر ومراجعة صارمة تضمن الاحترام والأدب المطلق.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_f3, col_f4, col_f5 = st.columns(3)
    with col_f3:
        st.markdown("""
            <div class="market-card" style='border-top: 6px solid #8b5cf6;'>
                <h4 style='color: #6d28d9; font-weight: 800; font-size: 20px;'>💎 نظام المحفظة الثنائية المزدوجة</h4>
                <p style='color: #64748b; font-size: 16px; line-height: 1.8;'>
                    فصلنا تماماً بين المتعة والعلاج! امتلك <b>الكوينز</b> للشحن الحقيقي عبر الفيزا وجلسات الدعم، و<b>الماس</b> الذي تكتسبه مجاناً من الألعاب والتفاعل لفتح جلسات ومميزات استثنائية دون أي تكلفة إضافية.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_f4:
        st.markdown("""
            <div class="market-card" style='border-top: 6px solid #f59e0b;'>
                <h4 style='color: #b45309; font-weight: 800; font-size: 20px;'>🎨 متجر الهدايا والدخلات الأسطورية</h4>
                <p style='color: #64748b; font-size: 16px; line-height: 1.8;'>
                    ميّز حسابك وبروفايلك بدخلات متحركة مذهلة (زئير الأسد، التنين الأسطوري)، إطارات بروفايل فاخرة، وأهدِ أصدقاءك بالآي دي لتتصدر فوراً <b>لوحة الشرف (أكثر الأصدقاء كرماً)</b> وتحفز الجميع!
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_f5:
        st.markdown("""
            <div class="market-card" style='border-top: 6px solid #ef4444;'>
                <h4 style='color: #b91c1c; font-weight: 800; font-size: 20px;'>🛡️ أمان مالي وحقوق محفوظة 100%</h4>
                <p style='color: #64748b; font-size: 16px; line-height: 1.8;'>
                    نؤمن أن حقوق الناس خط أحمر. حتى في أشد حالات الحظر لأي حساب مخالف، يتيح لك النظام استرداد أرصدتك المالية وعدم ضياع أي حقوق مالية لأي عميل، لضمان أعلى معايير الشفافية والثقة.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # قسم إضافي لدعم الثقة (Social Proof / Sales Boost)
    st.markdown("""
        <div style='background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%); padding: 50px; border-radius: 24px; text-align: center; border: 2px dashed #38bdf8;'>
            <h2 style='color: #0369a1; font-weight: 900; margin-bottom: 15px;'>✨ هل أنت مستعد لتجربة تغيير حقيقي في حياتك؟</h2>
            <p style='color: #334155; font-size: 19px; max-width: 800px; margin: 0 auto 25px auto; line-height: 1.7;'>
                انضم الآن لمجتمع "مراية"، احصل على رصيدك الترحيبي المجاني، وابدأ جلستك الخاصة مع الثيرابست الذكي في ثوانٍ معدودة.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-weight: 600;'>جميع الحقوق محفوظة منصة مراية © 2026 | مساحتك الآمنة دائماً</p>", unsafe_allow_html=True)

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
