import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة الأساسية لتطبيق مراية
st.set_page_config(
    page_title="مراية | مساحتك الآمنة",
    page_icon="🪞",
    layout="centered"
)

# ملف تخزين الحسابات محلياً
USERS_FILE = "mraya_users.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        df = pd.DataFrame(columns=["Full_Name", "Login_ID", "Email_Phone", "Account_Type", "Coins", "Diamonds"])
        # إنشاء حساب الأونر الأساسي لطارق تلقائياً
        admin_df = pd.DataFrame({
            "Full_Name": ["طارق المطور"],
            "Login_ID": ["tarek_admin"],
            "Email_Phone": ["admin@mraya.com"],
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
        st.info("✨ **جلسات فردية سرية**\n\nتواصل مع الذكاء الاصطناعي المتطور الذي يحتفظ بذاكرة جلساتك السابقة.")
    with col2:
        st.success("👥 **جلسات جماعية اختيارية**\n\nتواصل بأمان تام عبر الغرف الصوتية الجماعية بشخصيات وهمية وأفاتار محمية.")
        
    st.markdown("---")
    
    st.subheader("🔑 انضم إلى عائلة مراية")
    auth_tab1, auth_tab2 = st.tabs(["تسجيل دخول", "حساب جديد"])
    
    with auth_tab1:
        # ملاحظة لطارق: يوزر الادمن الخاص بك هو tarek_admin
        st.caption("💡 للأونر: ادخل بالمعرف `tarek_admin`")
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
                base_id = full_name.strip().replace(" ", "_").lower()
                unique_id = f"mraya_{base_id}_{len(users_df) + 1}"
                
                new_user = pd.DataFrame({
                    "Full_Name": [full_name],
                    "Login_ID": [unique_id],
                    "Email_Phone": [contact_info],
                    "Account_Type": ["Standard"],
                    "Coins": [10], # هدية ترحيبية كوينز
                    "Diamonds": [5]
                })
                
                users_df = pd.concat([users_df, new_user], ignore_index=True)
                users_df.to_csv(USERS_FILE, index=False)
                
                st.success(f"تم إنشاء حسابك بنجاح! معرفك الفريد للموقع هو: **{unique_id}** (احتفظ به لتسجيل الدخول).")
            else:
                st.warning("من فضلك أدخل البيانات المطلوبة.")

# --- الواجهة الداخلية للعميل بعد تسجيل الدخول ---
else:
    users_df = load_users()
    user_row = users_df[users_df["Login_ID"] == st.session_state.current_user]
    
    is_owner = (st.session_state.current_user == "tarek_admin")
    
    st.sidebar.title(f"🪞 أهلاً بك، {st.session_state.current_user}")
    if is_owner:
        st.sidebar.markdown("👑 **[صلاحيات الأونر والمطور]**")
    st.sidebar.markdown("---")
    
    # القائمة بناءً على الصلاحيات
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
        st.dataframe(users_df)
        
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
