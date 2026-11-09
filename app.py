import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة الأساسية لتطبيق مراية
st.set_page_config(
    page_title="مراية | مساحتك الآمنة",
    page_icon="🪞",
    layout="centered"
)

# ملف تخزين الحسابات محلياً (كمرحلة أولى لتأسيس المنظومة)
USERS_FILE = "mraya_users.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        df = pd.DataFrame(columns=["Full_Name", "Login_ID", "Email_Phone", "Account_Type"])
        df.to_csv(USERS_FILE, index=False)
        return df

# حالة تسجيل الدخول في الجلسة
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# --- واجهة الترحيب والتعريف بالموقع (تظهر قبل تسجيل الدخول) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🪞 منصة مراية</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666;'>مساحتك الآمنة للاسترخاء، الدعم النفسي، والنمو الداخلي</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("✨ **جلسات فردية سرية**\n\nتواصل مع الذكاء الاصطناعي المتطور الذي يحتفظ بذاكرة جلساتك السابقة ليرافقك خطوة بخطوة.")
    with col2:
        st.success("👥 **جلسات جماعية اختيارية**\n\nتواصل بأمان تام عبر الغرف الصوتية الجماعية بشخصيات وهمية وأفاتار محمية بالكامل.")
        
    st.markdown("---")
    
    # قسم التسجيل أو تسجيل الدخول
    st.subheader("🔑 انضم إلى عائلة مراية")
    auth_tab1, auth_tab2 = st.tabs(["تسجيل دخول", "حساب جديد"])
    
    with auth_tab1:
        login_input = st.text_input("أدخل معرف مراية الخاص بك (Login ID):", key="login_id_input")
        if st.button("دخول للموقع"):
            users_df = load_users()
            if not users_df.empty and login_input in users_df["Login_ID"].values:
                st.session_state.logged_in = True
                st.session_state.current_user = login_input
                st.success("تم تسجيل الدخول بنجاح! جاري تحويلك...")
                st.rerun()
            else:
                st.error("المعرف غير موجود. تأكد من صحة المعرف أو أنشئ حساباً جديداً.")
                
    with auth_tab2:
        full_name = st.text_input("الاسم الحقيقي أو المستعار:")
        contact_info = st.text_input("البريد الإلكتروني أو رقم الهاتف:")
        
        if st.button("إنشاء حساب فريد جديد"):
            if full_name and contact_info:
                users_df = load_users()
                # توليد معرف فريد غير مكرر للموقع
                base_id = full_name.strip().replace(" ", "_").lower()
                unique_id = f"mraya_{base_id}_{len(users_df) + 1}"
                
                new_user = pd.DataFrame({
                    "Full_Name": [full_name],
                    "Login_ID": [unique_id],
                    "Email_Phone": [contact_info],
                    "Account_Type": ["Standard"]
                })
                
                users_df = pd.concat([users_df, new_user], ignore_index=True)
                users_df.to_csv(USERS_FILE, index=False)
                
                st.success(f"تم إنشاء حسابك بنجاح! معرفك الفريد للموقع هو: **{unique_id}** (احتفظ به لتسجيل الدخول لاحقاً).")
            else:
                st.warning("من فضلك أدخل البيانات المطلوبة.")

# --- الواجهة الداخلية للعميل بعد تسجيل الدخول ---
else:
    st.sidebar.title(f"🪞 أهلاً بك، {st.session_state.current_user}")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("القائمة الرئيسية:", ["الصفحة الرئيسية", "الجلسات النفسية (الثيرابست)", "المجتمع والجلسات الجماعية", "المتجر والألعاب (الكوينز والماس)"])
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    if menu == "الصفحة الرئيسية":
        st.title("🏠 لوحة التحكم الخاصة بك")
        st.write("أهلاً بك في مساحتك الخاصة داخل موقع **مراية**. من هنا يمكنك إدارة جلساتك، تتبع تطورك، واستكشاف المميزات الحصرية.")
        st.info("💡 رصيدك الحالي: 0 كوينز | 0 ماسات | عدد الجلسات المتبقية: مجانية.")
        
    elif menu == "الجلسات النفسية (الثيرابست)":
        st.title("🤖 جلسة الدعم النفسي الذكي")
        st.write("مساحتك الفردية الخاصة جداً. البوت هنا يتذكر كل تفاصيل جلستك السابقة ليقدم لك استمرارية علاجية فريدة.")
        st.text_area("تحدث مع الثيرابست الخاص بك...", placeholder="اكتب ما يدور في ذهنك بحرية تامة...")
        if st.button("إرسال الرسالة"):
            st.info("جارٍ حفظ الذاكرة ومعالجة الرد النفسي...")
            
    elif menu == "المجتمع والجلسات الجماعية":
        st.title("👥 الغرف الصوتية الجماعية الآمنة")
        st.write("هنا يمكنك الانضمام بـ (فيك أكونت) للهلافات الجماعية الصوتية التفاعلية مع الحفاظ على سرية هويتك المطلقة.")
        st.warning("قريباً: تفعيل غرف الفويس الجماعية وأنظمة البلاغات الذكية.")
        
    elif menu == "المتجر والألعاب (الكوينز والماس)":
        st.title("🎮 المتجر وألعاب الحظ والتفاعل")
        st.write("استمتع بألعاب الروليت والبوكر التفاعلية لكسب الماسات، أو تسوق الإطارات والدخلات المتحركة (مثل زئير الأسد والتنين) لتمييز بروفايلك!")
