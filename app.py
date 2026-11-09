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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
if "view" not in st.session_state:
    st.session_state.view = "landing"

# --- 1. الصفحة الخارجية الموسوعية والتسويقية (Landing Page) ---
if not st.session_state.logged_in and st.session_state.view == "landing":
    
    # حقن تصميم CSS احترافي يوضح هوية مراية والراحة النفسية
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; }
        .hero-banner {
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
            border-radius: 24px;
            color: white;
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
            margin-bottom: 40px;
        }
        .content-card {
            background-color: #ffffff;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.04);
            height: 100%;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        .content-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        }
        .philosophy-box {
            background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
            padding: 40px;
            border-radius: 20px;
            border-right: 8px solid #10b981;
            margin: 40px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # الشريط العلوي الفخم
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
    
    # البانر الرئيسي الضخم
    st.markdown("""
        <div class="hero-banner">
            <h1 style='font-size: 50px; font-weight: 900; margin-bottom: 20px; color: #ffffff;'>لأن أصدق حديث هو ما تقوله لنفسك..</h1>
            <p style='font-size: 21px; max-width: 900px; margin: 0 auto 35px auto; line-height: 1.8; color: #cbd5e1;'>
                منصة <b>"مراية"</b> ليست مجرد موقع نوت بوك أو تطبيق محادثة عابر، بل هي منظومة علاجية ومجتمعية متكاملة مصممة خصيصاً لتمنحك ملاذاً آمناً وخالياً من الأحكام، تجمع بين الدعم النفسي الفردي المستمر عبر ذكاء اصطناعي فاهم لحالتك، وبين المجتمعات الصوتية السرية المحمية تماماً.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # زر البدء السريع
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🚀 انضم الآن وابدأ جلستك الأولى مجاناً", type="primary", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # قسم فلسفة اسم ومعنى "مراية"
    st.markdown("""
        <div class="philosophy-box">
            <h2 style='color: #065f46; margin-top: 0; font-weight: 800;'>💡 ما هي فلسفة ومعنى "مراية"؟</h2>
            <p style='color: #1e293b; font-size: 18px; line-height: 1.8; margin-bottom: 0;'>
                المرآة لا تكذب، ولا تحكم، ولا تلوم.. بل تعطيك انعكاساً صادقاً لِما بداخل بدقة مطلقة. من هنا جاءت فكرة منصتنا؛ أن تكون المرآة النقية التي تستقبل أفكارك المضطربة، مخاوفك، وهمومك، وتعيد ترتيبها لك عبر ثيرابست ذكي يتذكر كل نبضة وتفصيل في تاريخك النفسي معنا. هنا أنت في أمان تام، لا اسم حقيقي يظهر، ولا وجه يكشف، ولا حكم يلاحقك.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0f172a; font-weight: 800;'>🌟 التفاصيل الكاملة لأقسام وخدمات منصة مراية</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px;'>تعرف على المزايا الحصرية التي تم إعدادها خصيصاً لراحتك وتطويرك النفسي والاجتماعي</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # تفاصيل الخدمات في كروت موسعة
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("""
            <div class="content-card" style='border-right: 6px solid #0284c7;'>
                <h3 style='color: #0369a1; margin-top: 0;'>🤖 1. الثيرابست الذكي (ذاكرة علاجية مستمرة)</h3>
                <p style='color: #475569; font-size: 16px; line-height: 1.8;'>
                    على عكس برامج المحادثة العادية، الثيرابست في "مراية" يحتفظ بسجل كامل وذاكرة ذكية لكل جلساتك السابقة (الأولى، الثانية، والثالثة...). عندما تفتح جلسة جديدة، يستكمل معك الحوار بنفس الإيقاع والنفسية كأنه طبيب معالج يلازمك لشهور، فاهم تفاصيل مشاكلك دون أن تحتاج لتكرار سرد قصتك مراراً وتكراراً.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
            <div class="content-card" style='border-right: 6px solid #10b981;'>
                <h3 style='color: #047857; margin-top: 0;'>🎙️ 2. الغرف الصوتية الجماعية (أمان وسرية تامة)</h3>
                <p style='color: #475569; font-size: 16px; line-height: 1.8;'>
                    إذا اخترت الانضمام للمجتمع، تفتح لك غرف الفويس الجماعية التفاعلية. الدخول يتم بـ (فيك أكونت) وأسماء وهمية وأفاتار محمية بالكامل؛ لا أحد يعرف اسمك الحقيقي أو هويتك. تتحدثون، تتشاركون التجارب الصوتية، وتفرغون ضغوطكم بحرية، مع وجود أنظمة بلاغات ومراجعة دقيقة لضمان الاحترام المتبادل ومنع أي تجاوز.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_f3, col_f4, col_f5 = st.columns(3)
    with col_f3:
        st.markdown("""
            <div class="content-card" style='border-top: 5px solid #8b5cf6; text-align: center;'>
                <h4 style='color: #6d28d9; font-weight: 700;'>💎 نظام المحفظة الثنائية (كوينز و ماسات)</h4>
                <p style='color: #64748b; font-size: 15px; line-height: 1.7;'>
                    رصيد مزدوج متطور؛ <b>الكوينز</b> للشحن الحقيقي عبر الفيزا وجلسات الدعم، و<b>الماس</b> تكتسبه مجاناً من الألعاب والتفاعل لفتح جلسات ومزايا استثنائية.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_f4:
        st.markdown("""
            <div class="content-card" style='border-top: 5px solid #f59e0b; text-align: center;'>
                <h4 style='color: #b45309; font-weight: 700;'>🎨 متجر الهدايا والدخلات الأسطورية</h4>
                <p style='color: #64748b; font-size: 15px; line-height: 1.7;'>
                    ميّز حضورك بدخلات متحركة مذهلة (زئير الأسد، التنين الأسطوري)، إطارات بروفايل مميزة، وأهد أصدقاءك لتظهر في لوحة الشرف (أكثر الأصدقاء كرماً).
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_f5:
        st.markdown("""
            <div class="content-card" style='border-top: 5px solid #ef4444; text-align: center;'>
                <h4 style='color: #b91c1c; font-weight: 700;'>🛡️ ضمانات وحقوق مالية وآمنة</h4>
                <p style='color: #64748b; font-size: 15px; line-height: 1.7;'>
                    نظام أمان صارم ضد الاختراق، مع سياسة واضحة تضمن أن أي رصيد متبقي لأي حساب محظور يتم حفظه ورد حقوقه بالكامل لضمان الأمان القانوني والأخلاقي.
                </p>
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
