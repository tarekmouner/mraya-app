"""MIRAYA entertainment games. No wagering, cash value, or wallet integration."""
from __future__ import annotations
import sqlite3, random
from datetime import datetime, timezone
from collections import Counter
import streamlit as st
import mraya_core as db

GAMES = {"wheel":"عجلة مراية", "memory":"تحدي الذاكرة", "quiz":"اختبار المعلومات", "poker":"بوكر تدريبية"}
PROMPTS = ["اذكر ثلاث حاجات ممتن لوجودها اليوم.","خد نفسًا عميقًا وبطّله ببطء خمس مرات.","ما عادة صغيرة تحب تبدأها هذا الأسبوع؟","اختار أغنية بتحسن مزاجك.","اكتب لنفسك رسالة تشجيع من سطر واحد.","ما مكان بتحس فيه بالراحة؟","قول لنفسك حاجة إيجابية تستحق تسمعها.","خد دقيقة بعيدًا عن الشاشة وريح عينيك."]
QUIZ = [
("كم عدد ألوان قوس قزح التقليدية؟",["5","6","7","8"],2,"قوس قزح يتكون تقليديًا من سبعة ألوان."),
("أي كوكب يُعرف بالكوكب الأحمر؟",["الزهرة","المريخ","زحل","عطارد"],1,"المريخ يبدو أحمر بسبب أكاسيد الحديد على سطحه."),
("كم دقيقة في الساعة؟",["30","45","60","90"],2,"الساعة الواحدة تساوي 60 دقيقة."),
("ما أكبر محيط على الأرض؟",["الأطلسي","الهندي","المتجمد الشمالي","الهادئ"],3,"المحيط الهادئ هو الأكبر مساحة."),
("أي عضو يضخ الدم في جسم الإنسان؟",["الرئة","القلب","الكبد","الكلى"],1,"القلب يضخ الدم إلى أنحاء الجسم.")]

def _conn():
    c=sqlite3.connect(db.DB_PATH,timeout=30); c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c

def init_games():
    with _conn() as c:
        c.executescript("CREATE TABLE IF NOT EXISTS game_settings(game_key TEXT PRIMARY KEY,enabled INTEGER NOT NULL DEFAULT 1); CREATE TABLE IF NOT EXISTS game_history(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL REFERENCES users(id),game_key TEXT NOT NULL,score INTEGER NOT NULL DEFAULT 0,detail TEXT NOT NULL DEFAULT '',created_at TEXT NOT NULL);")
        for key in GAMES: c.execute("INSERT OR IGNORE INTO game_settings(game_key,enabled) VALUES(?,1)",(key,))

def enabled_games():
    init_games()
    with _conn() as c: return {r['game_key']:bool(r['enabled']) for r in c.execute('SELECT * FROM game_settings')}

def set_game_enabled(key,enabled):
    if key not in GAMES: raise ValueError('لعبة غير معروفة')
    init_games()
    with _conn() as c: c.execute('UPDATE game_settings SET enabled=? WHERE game_key=?',(int(bool(enabled)),key))

def record(uid,key,score,detail=''):
    init_games()
    with _conn() as c: c.execute('INSERT INTO game_history(user_id,game_key,score,detail,created_at) VALUES(?,?,?,?,?)',(uid,key,max(0,int(score)),str(detail)[:300],datetime.now(timezone.utc).isoformat()))

def history(uid,limit=30):
    init_games()
    with _conn() as c: return [dict(r) for r in c.execute('SELECT game_key,score,detail,created_at FROM game_history WHERE user_id=? ORDER BY id DESC LIMIT ?',(uid,limit))]

def leaderboard(limit=10):
    init_games()
    with _conn() as c: return [dict(r) for r in c.execute('SELECT u.display_name,SUM(h.score) points,COUNT(*) games FROM game_history h JOIN users u ON u.id=h.user_id GROUP BY h.user_id ORDER BY points DESC,games DESC LIMIT ?',(limit,))]

def _header():
    st.markdown('''<style>.game-hero{background:linear-gradient(135deg,#20172f,#49305d 55%,#8b668d);padding:24px;border-radius:20px;color:white;margin:8px 0 18px}.game-hero h2{color:white;margin:0 0 8px}div.stButton>button{border-radius:12px;min-height:42px}</style>''',unsafe_allow_html=True)
    st.markdown('<div class="game-hero"><h2>🎮 عالم ألعاب مراية</h2><div>وقت لطيف، تحديات خفيفة، ومساحة للمرح — من غير مراهنات أو أموال.</div></div>',unsafe_allow_html=True)

def _wheel(uid):
    st.subheader('🎡 عجلة مراية'); st.write('لف العجلة وخد سؤالًا لطيفًا أو تحديًا بسيطًا لنفسك.')
    if st.button('لف العجلة',key='miraya_spin'):
        st.session_state['wheel_result']=random.choice(PROMPTS); record(uid,'wheel',10,'تم تدوير العجلة')
    if st.session_state.get('wheel_result'):
        st.success(st.session_state['wheel_result']); st.caption('10 نقاط ترفيهية لتسجيل النشاط فقط، لا تتحول إلى كوينز أو ماسات.')

def _memory(uid):
    st.subheader('🧠 تحدي الذاكرة'); st.write('اكشف البطاقات وحاول مطابقة الرموز المتشابهة.')
    symbols=['🌙','🌸','⭐','🪞','🍀','🌈']
    if st.button('ابدأ جولة جديدة',key='memory_new'):
        deck=symbols*2; random.shuffle(deck); st.session_state.memory_deck=deck; st.session_state.memory_open=[]; st.session_state.memory_found=[]; st.session_state.memory_moves=0; st.session_state.memory_done=False; st.session_state.memory_wait=False
    if 'memory_deck' not in st.session_state: st.info('اضغط «ابدأ جولة جديدة» لبدء اللعب.'); return
    deck=st.session_state.memory_deck; opened=st.session_state.memory_open; found=st.session_state.memory_found
    cols=st.columns(4)
    for i,sym in enumerate(deck):
        with cols[i%4]:
            label=sym if i in found or i in opened else '❔'
            if st.button(label,key=f'mem_{i}',disabled=(i in found or i in opened or len(opened)>=2 or st.session_state.memory_done),use_container_width=True):
                opened.append(i)
                if len(opened)==2:
                    st.session_state.memory_moves+=1; a,b=opened
                    if deck[a]==deck[b]: found.extend([a,b]); st.session_state.memory_open=[]
                    else: st.session_state.memory_wait=True
                st.rerun()
    if st.session_state.get('memory_wait') and st.button('إخفاء البطاقتين ومتابعة اللعب',key='memory_hide'):
        st.session_state.memory_open=[]; st.session_state.memory_wait=False; st.rerun()
    st.caption(f'المحاولات: {st.session_state.memory_moves} · الأزواج: {len(found)//2} من 6')
    if len(found)==12 and not st.session_state.memory_done:
        st.session_state.memory_done=True; score=max(10,100-st.session_state.memory_moves*5); record(uid,'memory',score,f'أنهى اللعبة في {st.session_state.memory_moves} محاولة'); st.balloons(); st.success(f'ممتاز! أنهيت الجولة وحصلت على {score} نقطة ترفيهية.')

def _quiz(uid):
    st.subheader('✨ اختبار المعلومات')
    if 'quiz_idx' not in st.session_state or st.session_state.get('quiz_finished'):
        if st.button('ابدأ الاختبار',key='quiz_start'):
            st.session_state.quiz_order=random.sample(range(len(QUIZ)),len(QUIZ)); st.session_state.quiz_idx=0; st.session_state.quiz_score=0; st.session_state.quiz_finished=False; st.session_state.quiz_feedback=None; st.rerun()
        return
    idx=st.session_state.quiz_order[st.session_state.quiz_idx]; q,opts,answer,explain=QUIZ[idx]
    st.progress(st.session_state.quiz_idx/len(QUIZ),text=f'السؤال {st.session_state.quiz_idx+1} من {len(QUIZ)}'); choice=st.radio(q,opts,key=f'quiz_choice_{st.session_state.quiz_idx}')
    if st.button('تأكيد الإجابة',key=f'quiz_submit_{st.session_state.quiz_idx}'):
        correct=opts.index(choice)==answer
        if correct: st.session_state.quiz_score+=1
        st.session_state.quiz_feedback=(correct,explain)
    if st.session_state.get('quiz_feedback'):
        ok,ex=st.session_state.quiz_feedback; st.success('إجابة صحيحة!' if ok else 'مش مشكلة، دي فرصة للتعلم.'); st.caption(ex)
        if st.button('السؤال التالي',key=f'quiz_next_{st.session_state.quiz_idx}'):
            st.session_state.quiz_feedback=None; st.session_state.quiz_idx+=1
            if st.session_state.quiz_idx>=len(QUIZ):
                score=st.session_state.quiz_score*20; record(uid,'quiz',score,f'إجابات صحيحة: {st.session_state.quiz_score}/{len(QUIZ)}'); st.session_state.quiz_finished=True
            st.rerun()
    if st.session_state.get('quiz_finished'): st.success(f'نتيجتك: {st.session_state.quiz_score} من {len(QUIZ)}')

def _poker_rank(cards):
    vals=[v for v,s in cards]; suits=[s for v,s in cards]; groups=sorted(Counter(vals).values(),reverse=True); unique=sorted(set(vals)); straight=(len(unique)==5 and unique[-1]-unique[0]==4) or set(unique)=={2,3,4,5,14}; flush=len(set(suits))==1
    if straight and flush: return 'تشكيلة متتالية من نفس النوع',100
    if groups==[4,1]: return 'أربع ورقات متشابهة',90
    if groups==[3,2]: return 'ثلاثة وزوج',80
    if flush: return 'خمس ورقات من نفس النوع',70
    if straight: return 'تسلسل من خمس ورقات',60
    if groups==[3,1,1]: return 'ثلاث ورقات متشابهة',50
    if groups==[2,2,1]: return 'زوجان',40
    if groups==[2,1,1,1]: return 'زوج واحد',30
    return 'أعلى ورقة',20

def _poker(uid):
    st.subheader('🃏 بوكر تدريبية'); st.warning('وضع تدريبي مجاني: لا توجد رهانات أو شراء رقائق أو جوائز قابلة للتحويل أو سحب.')
    suits=['♠','♥','♦','♣']; labels={11:'J',12:'Q',13:'K',14:'A'}
    if st.button('وزّع خمس ورقات',key='poker_deal'):
        hand=random.sample([(v,s) for v in range(2,15) for s in suits],5); name,score=_poker_rank(hand); st.session_state.poker_hand=hand; st.session_state.poker_rank=(name,score); record(uid,'poker',score,f'نتيجة التدريب: {name}')
    if st.session_state.get('poker_hand'):
        cols=st.columns(5)
        for col,(v,s) in zip(cols,st.session_state.poker_hand):
            color='#c33' if s in ['♥','♦'] else '#222'; col.markdown(f'<div style="border:1px solid #aaa;border-radius:12px;padding:22px 4px;text-align:center;font-size:27px;background:white;color:{color}"><b>{labels.get(v,v)}{s}</b></div>',unsafe_allow_html=True)
        name,score=st.session_state.poker_rank; st.success(f'التشكيلة: {name}'); st.caption(f'{score} نقطة تدريبية في سجل الألعاب فقط.')

def render_games(user):
    _header(); uid=int(user['id']); active=enabled_games(); choices=[(k,v) for k,v in GAMES.items() if active.get(k,True)]
    if not choices: st.info('الألعاب متوقفة مؤقتًا. ارجع لاحقًا!'); return
    selected=st.selectbox('اختار اللعبة',[v for k,v in choices],key='miraya_game_select'); key=next(k for k,v in choices if v==selected)
    if key=='wheel': _wheel(uid)
    elif key=='memory': _memory(uid)
    elif key=='quiz': _quiz(uid)
    elif key=='poker': _poker(uid)
    st.divider(); a,b=st.columns(2)
    with a:
        st.subheader('🏆 لوحة الترتيب'); rows=leaderboard()
        if rows: st.dataframe(rows,use_container_width=True,hide_index=True)
        else: st.caption('ابدأ اللعب لتظهر النتائج هنا.')
    with b:
        st.subheader('🕹️ سجل لعبك'); rows=history(uid)
        if rows:
            for row in rows[:8]: st.caption(f"{GAMES.get(row['game_key'],row['game_key'])} · {row['score']} نقطة · {row['created_at'][:10]}")
        else: st.caption('لا توجد جولات مسجلة بعد.')

def render_game_admin():
    st.subheader('⚙️ إدارة الألعاب'); st.caption('يمكن للمالك تشغيل أو إيقاف كل لعبة. النقاط ترفيهية ولا تؤثر على المحافظ.')
    current=enabled_games()
    for key,name in GAMES.items():
        value=st.toggle(name,value=current.get(key,True),key=f'game_toggle_{key}')
        if value!=current.get(key,True): set_game_enabled(key,value); st.success(f'تم تحديث حالة {name}.')
