"""Streamlit screens to add after login. Keeps the existing public landing page untouched."""
import streamlit as st
import pandas as pd
import mraya_core as db
import mraya_games as games

def render_remaining_app(user):
    """user is the authenticated dict returned by mraya_core.authenticate()."""
    uid=user["id"]
    st.sidebar.caption(f'{user["display_name"]} · {user["public_id"]}')
    pages=["لوحة حسابي","مفكرة المشاعر","جلسة كتابية تجريبية","الألعاب 🎮","المتجر","محفظتي","الإحالات","الإبلاغ عن مستخدم"]
    if user["account_type"]=="Owner":
        pages += ["إدارة المستخدمين","إدارة الأرصدة","إدارة الألعاب","البلاغات","الإعدادات والإحصائيات"]
    page=st.sidebar.radio("التنقل",pages)

    if page=="لوحة حسابي":
        fresh=db.get_user(uid)
        a,b,c=st.columns(3)
        a.metric("الكوينز",fresh["coins"])
        b.metric("الماسات",fresh["diamonds"])
        c.metric("المستوى",fresh["level"])
        st.write("معرف مراية الخاص بك:",fresh["login_id"])
        st.write("المعرف العام:",fresh["public_id"])
        st.info("الجلسات الفردية هي الأساس. الانضمام للمجتمع اختياري.")

    elif page=="مفكرة المشاعر":
        mood=st.selectbox("كيف تشعر الآن؟",["هادئ","سعيد","قلق","حزين","غاضب","مرهق","مشاعر مختلطة"])
        body=st.text_area("اكتب ما ترغب في الاحتفاظ به في مفكرتك")
        if st.button("حفظ اليومية"):
            db.save_journal(uid,mood,body); st.success("تم الحفظ.")
        st.subheader("يومياتي السابقة")
        for x in db.get_journals(uid):
            with st.expander(f'{x["mood"]} · {x["created_at"][:16]}'):
                st.write(x["body"])

    elif page=="جلسة كتابية تجريبية":
        st.warning("هذه شاشة اختبار لتخزين الجلسات فقط؛ لا يوجد اتصال بمساعد ذكاء اصطناعي حتى تضيف مفتاح مزود AI وتفعّل سياسة الأمان.")
        mode=st.selectbox("نوع الجلسة",["text","voice","video"])
        if "mraya_active_session" not in st.session_state:
            if st.button("بدء جلسة"):
                st.session_state.mraya_active_session=db.start_session(uid,mode)
                st.rerun()
        else:
            sid=st.session_state.mraya_active_session
            messages=db.get_session_messages(sid,uid)
            for m in messages:
                st.markdown(f'**{m["role"]}:** {m["body"]}')
            msg=st.text_area("رسالتك")
            if st.button("حفظ الرسالة"):
                db.add_session_message(sid,"user",msg); st.success("حُفظت الرسالة.")
            if st.button("إنهاء الجلسة"):
                db.end_session(sid,uid); del st.session_state["mraya_active_session"]; st.rerun()

    elif page=="الألعاب 🎮":
        games.render_games(user)

    elif page=="إدارة الألعاب" and user["account_type"]=="Owner":
        games.render_game_admin()

    elif page=="المتجر":
        items=db.get_catalog()
        if not items: st.info("لا توجد منتجات مفعّلة بعد. أضف المنتجات من إدارة المتجر.")
        for item in items:
            with st.container(border=True):
                st.subheader(item["name"])
                st.write(f'{item["category"]} · {item["price_coins"]} كوينز')
                recipient=st.text_input("معرف المستلم (اتركه فارغًا للشراء لنفسك)",key=f'rec_{item["id"]}')
                if st.button("شراء / إهداء",key=f'buy_{item["id"]}'):
                    try:
                        result=db.purchase_item(uid,item["sku"],recipient or None)
                        st.success(f'تمت العملية. المستلم: {result["recipient"]}')
                    except Exception as e: st.error(str(e))

    elif page=="محفظتي":
        fresh=db.get_user(uid)
        st.metric("كوينز",fresh["coins"]); st.metric("ماسات",fresh["diamonds"])
        st.dataframe(pd.DataFrame(db.wallet_history(uid)),use_container_width=True)

    elif page=="الإحالات":
        st.write("شارك معرفك العام كرمز دعوة:",user["public_id"])
        st.caption("مكافآت الإحالة تُضاف بعد تفعيل قواعد تحقق مكافحة الحسابات الوهمية في مرحلة الإطلاق.")

    elif page=="الإبلاغ عن مستخدم":
        target=st.text_input("المعرف العام للمستخدم")
        reason=st.selectbox("سبب البلاغ",["إساءة لفظية","تحرش أو تهديد","انتحال هوية","محتوى غير مناسب","أخرى"])
        details=st.text_area("تفاصيل إضافية")
        if st.button("إرسال البلاغ"):
            try: db.create_report(uid,target,reason,details); st.success("تم إرسال البلاغ للمراجعة.")
            except Exception as e: st.error(str(e))

    elif page=="إدارة المستخدمين" and user["account_type"]=="Owner":
        q=st.text_input("بحث بالاسم أو المعرف")
        rows=db.list_users(q)
        st.dataframe(pd.DataFrame(rows),use_container_width=True)
        if rows:
            selected=st.selectbox("اختر مستخدمًا",rows,format_func=lambda x:f'{x["display_name"]} · {x["public_id"]}')
            status=st.selectbox("حالة الحساب",["active","suspended","banned"])
            if st.button("تحديث حالة الحساب"):
                db.set_user_status(selected["id"],status,uid); st.success("تم التحديث.")
            role=st.selectbox("الدور الإداري",["لا شيء","ADMIN","MOD"])
            if st.button("تعيين الدور") and role!="لا شيء":
                st.success(db.assign_admin_role(selected["id"],role))

    elif page=="إدارة الأرصدة" and user["account_type"]=="Owner":
        target=db.list_users(st.text_input("ابحث عن المستخدم"))
        if target:
            chosen=st.selectbox("المستخدم",target,format_func=lambda x:f'{x["display_name"]} · {x["public_id"]}')
            coins=st.number_input("كوينز للإضافة أو الخصم",step=1,value=0)
            diamonds=st.number_input("ماسات للإضافة أو الخصم",step=1,value=0)
            withdraw=st.checkbox("الكوينز الممنوحة قابلة للسحب (فقط عند وجود سياسة وتسوية مالية معتمدة)")
            if st.button("تنفيذ حركة الرصيد"):
                try:
                    db.owner_grant(chosen["id"],int(coins),int(diamonds),withdraw,uid)
                    st.success("تم تحديث الأرصدة وتسجيل الحركات.")
                except Exception as e: st.error(str(e))

    elif page=="البلاغات" and user["account_type"]=="Owner":
        reports=db.get_reports()
        st.dataframe(pd.DataFrame(reports),use_container_width=True)
        if reports:
            r=st.selectbox("بلاغ للمراجعة",reports,format_func=lambda x:f'#{x["id"]} · {x["reason"]}')
            status=st.selectbox("قرار المراجعة",["reviewed","dismissed","actioned"])
            if st.button("حفظ قرار المراجعة"):
                db.review_report(r["id"],uid,status); st.success("تم حفظ القرار.")

    elif page=="الإعدادات والإحصائيات" and user["account_type"]=="Owner":
        st.json(db.get_dashboard_stats())
        st.caption("إدارة المنتجات والباقات والصلاحيات التفصيلية وإعدادات المزودين تُستكمل بعد إدخال بيانات التشغيل ومراجعة صلاحيات الأدوار.")
