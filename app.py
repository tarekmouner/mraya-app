import streamlit as st
import pandas as pd
import os
import hashlib

# إعدادات الصفحة الأساسية لتطبيق مراية
st.set_page_config(
    page_title="مراية | مساحتك الآمنة",
    page_icon="🪞",
    layout="centered"
)

# ملف تخزين الحسابات محلياً
USERS_FILE = "mraya_users.csv"

# دالة لتشفيّر كلمات المرور لضمان الأمان التام
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        # إنشاء جدول المستخدمين مع حساب الأونر الأساسي بكلمة مرور آمنة
        df = pd.DataFrame(columns=["Full_Name", "Login_ID", "Email_Phone", "Password", "Account_Type", "Coins", "Diamonds"])
        admin_df = pd.DataFrame({
            "Full_Name": ["طارق المطور (الأونر)"],
            "Login_ID": ["tarek_admin"],
            "Email_Phone": ["admin@mraya.com"],
            "Password": [hash_password("tarek12345")], # كلمة مرور الأونر الافتراضية
            "Account_Type": ["Owner"],
            "Coins": [999999],
            "Diamonds": [999999]
        })
        admin_df.to_csv(USERS_FILE, index=False)
        return admin_df

# حالة تسجيل الدخول في الجلسة
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# --- واجهة الترحيب والتعريف بالموقع (قبل تسجيل الدخول) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🪞 منصة مراية</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666;'>مساحتك الآمنة للاسترخاء، الدعم النفسي، والنمو الداخلي</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("✨ **جلسات فردية سرية بذاكرة ذكية**\n\nتواصل مع الثيرابست الذكي الذي يتذكر تفاصيل جلستك السابقة.")
    with col2:
        st.success("👥 **جلسات جماعية اختيارية**\n\nتواصل بأمان تام عبر الغرف الصوتية بشخصيات وهمية وأفاتار محمية.")
        
    st.markdown("---")
    
    st.subheader("🔑 بوابة الأمان وتسجيل الدخول")
    auth_tab1, auth_tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب آمن جديد"])
    
    with auth_tab1:
        st.caption("💡 للأونر: ادخل بالمعرف `tarek_admin` وكلمة المرور `tarek12345`")
        login_input = st.text_input("معرف مراية (Login ID) أو الإيميل:", key="login_id_input")
        login_pass = st.text_input("كلمة المرور السرية:", type="password", key="login_pass_input")
        
        if st.button("دخول آمن للموقع"):
            users_df = load_users()
            hashed_p = hash_password(login_pass)
            
            # التحقق من المعرف وكلمة المرور معاً لضمان مستوى الأمان العالي
            user_match = users_df[(users_df["Login_ID"] == login_input) | (users_df["Email_Phone"] == login_input)]
            
            if not user_match.empty:
                stored_pass = user_match.iloc[0]["Password"]
                if stored_pass == hashed_p:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_match.iloc[0]["Login_ID"]
                    st.success("تم تسجيل الدخول بنجاح! جاري تحويلك...")
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة. حاول مرة أخرى.")
            else:
                st.error("المعرف أو البريد غير مسجل في النظام.")
                
    with auth_tab2:
        full_name = st.text_input("الاسم الحقيقي أو المستعار:")
        contact_info = st.text_input("البريد الإلكتروني أو رقم الهاتف:")
        new_pass = st.text_input("كلمة المرور السرية الجديدة:", type="password", key="new_pass_input")
        confirm_pass = st.text_input("تأكيد كلمة المرور السرية:", type="password", key="confirm_pass_input")
        
        if st.button("إنشاء الحساب الفريد الآمن"):
            if full_name and contact_info and new_pass:
                if new_pass != confirm_pass:
                    st.warning("كلمات المرور غير متطابقة. من فضلك تأكد منهما.")
                else:
                    users_df = load_users()
                    
                    # التحقق من عدم تكرار البريد أو الهاتف
                    if contact_info in users_df["Email_Phone"].values:
                        st.error("هذا البريد أو رقم الهاتف مسجل مسبقاً بحساب آخر!")
                    else:
                        base_id = full_name.strip().replace(" ", "_").lower()
                        unique_id = f"mraya_{base_id}_{len(users_df) + 1}"
                        
                        new_user = pd.DataFrame({
                            "Full_Name": [full_name],
                            "Login_ID": [unique_id],
                            "Email_Phone": [contact_info],
                            "Password": [hash_password(new_pass)],
                            "Account_Type": ["Standard"],
                            "Coins": [10], # هدية ترحيبية
                            "Diamonds": [5]
                        })
                        
                        users_df = pd.concat([users_df, new_user], ignore_index=True)
                        users_df.to_csv(USERS_FILE, index=False)
                        
                        st.success(f"تم إنشاء حسابك الآمن بنجاح! معرفك الفريد للموقع هو: **{unique_id}** (احتفظ به لتسجيل الدخول).")
            else:
                st.warning("من فضلك أدخل جميع البيانات المطلوبة بما فيها كلمة المرور.")

# --- الواجهة الداخلية للعميل بعد تسجيل الدخول ---
else:
    users_df = load_users()
    user_row = users_df[users_df["Login_ID"] == st.session_state.current_user]
    
    is_owner = (st.session_state.current_user == "tarek_admin")
    
    st.sidebar.title(f"🪞 أهلاً بك، {st.session_state.current_user}")
    if is_owner:
        st.sidebar.markdown("👑 **[صلاحيات الأونر والمطور]**")
    st.sidebar.markdown("---")
    
    menu_options = ["الصفحة الرئيسية", "الجلسات النفسية (الثيرابست)", "المجتمع والجلسات الجماعية", "المتجر والألعاب (الكوينز والماس)"]
    if is_owner:
        menu_options.append("لوحة تحكم الأونر ⚙️")
        
    menu = st.sidebar.radio("القائمة الرئيسية:", menu_options)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    if menu == "الصفحة الرئيسية":
        st.title("🏠 لوحة التحكم الخاصة بك")
        st.write(f"أهلاً بك في مساحتك الخاصة داخل موقع **مراية**.")
        if not user_row.empty:
            c = user_row.iloc[0]["Coins"]
            d = user_row.iloc[0]["Diamonds"]
            st.info(f"💡 رصيد محفظتك الحالي: **{c} كوينز** | **{d} ماسات**")
        
    elif menu == "الجلسات النفسية (الثيرابست)":
        st.title("🤖 جلسة الدعم النفسي الذكي")
        st.write("مساحتك الفردية الخاصة جداً. البوت هنا يتذكر تفاصيل جلستك السابقة.")
        st.text_area("تحدث مع الثيرابست الخاص بك...", placeholder="اكتب ما يدور في ذهنك بحرية تامة...")
        if st.button("إرسال الرسالة"):
            st.info("جارٍ حفظ الذاكرة ومعالجة الرد النفسي...")
            
    elif menu == "المجتمع والجلسات الجماعية":
        st.title("👥 الغرف الصوتية الجماعية الآمنة")
        st.write("انضم بـ (فيك أكونت) للجلسات الصوتية التفاعلية مع سرية هويتك المطلقة.")
        st.warning("قريباً: تفعيل غرف الفويس الجماعية.")
        
    elif menu == "المتجر والألعاب (الكوينز والماس)":
        st.title("🎮 المتجر وألعاب الحظ والتفاعل")
        st.write("استمتع بألعاب الروليت والبوكر لكسب الماسات، أو تسوق الإطارات والدخلات المتحركة!")
        
    elif menu == "لوحة تحكم الأونر ⚙️" and is_owner:
        st.title("⚙️ لوحة تحكم الأونر المطلقة (طارق)")
        st.write("من هنا يمكنك التحكم الكامل بالموقع، شحن الأرصدة للأعضاء، وإدارة الهدايا.")
        
        st.subheader("👥 قائمة المستخدمين المسجلين في المنصة")
        # إخفاء خانة كلمة المرور المشفرة من الجدول لأسباب أمنية حقيقية
        safe_df = users_df.drop(columns=["Password"])
        st.dataframe(safe_df)
        
        st.subheader("💰 شحن رصيد أو إرسال هدايا لمستخدم")
        target_id = st.text_input("أدخل معرف المستخدم المراد شحنه (Login ID):")
        add_coins = st.number_input("عدد الكوينز للإضافة:", min_value=0, value=100)
        add_diamonds = st.number_input("عدد الماسات للإضافة:", min_value=0, value=50)
        
        if st.button("تنفيذ الشحن والإهداء"):
            if target_id in users_df["Login_ID"].values:
                users_df.loc[users_df["Login_ID"] == target_id, "Coins"] += add_coins
                users_df.loc[users_df["Login_ID"] == target_id, "Diamonds"] += add_diamonds
                users_df.to_csv(USERS_FILE, index=False)
                st.success(f"تم شحن المستخدم {target_id} بنجاح بـ {add_coins} كوينز و {add_diamonds} ماسات! ✨")
            else:
                st.error("معرف المستخدم غير موجود في النظام.")
