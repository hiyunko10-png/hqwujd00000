import json
import threading
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="우리집 오늘판",page_icon="🏡",layout="centered",initial_sidebar_state="collapsed")
st.markdown("""<style>
:root {color-scheme:light!important;--text-color:#23212c;--background-color:#f4f1f8;--secondary-background-color:#ffffff;--primary-color:#7053b5;}
html,body,.stApp,[data-testid="stAppViewContainer"],.main {background:#f4f1f8!important;color:#23212c!important;}
[data-testid="stHeader"] {background:#f4f1f8!important;}
[data-testid="stSidebar"],[data-testid="collapsedControl"] {display:none!important;}
.block-container {max-width:740px;padding:1.5rem 1.15rem 9rem;}
h1,h2,h3,h4,h5,h6,p,label,li,span,[data-testid="stMetricValue"],[data-testid="stMetricLabel"] {color:#23212c;}
h1 {font-size:2.05rem!important;letter-spacing:-1.4px!important;font-weight:850!important;}
h2,h3 {letter-spacing:-.7px!important;}
[data-testid="stMarkdownContainer"] p,[data-testid="stWidgetLabel"] p,[data-testid="stRadio"] label p {color:#23212c!important;}
[data-testid="stCaptionContainer"] p {color:#62586e!important;}
[data-testid="stForm"] {background:#e9dff9!important;border:1px solid #d1bfe9!important;border-radius:24px!important;padding:22px!important;}
[data-testid="stVerticalBlockBorderWrapper"]>[data-testid="stVerticalBlock"] {border-radius:22px;}
[data-testid="stVerticalBlockBorderWrapper"] {border-color:#d8cde5!important;border-radius:22px!important;}
[data-testid="stMetric"] {background:#cdbdf2!important;border:1px solid #bca6e5;border-radius:22px;padding:18px 12px;min-height:114px;}
[data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {background:#c6e8d0!important;border-color:#a6cdb2;}
[data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {background:#ffd9c7!important;border-color:#eac1ac;}
[data-testid="stMetricValue"] {font-size:1.9rem!important;font-weight:800!important;color:#282131!important;}
[data-testid="stMetricLabel"] p {font-size:.82rem!important;color:#45374f!important;}
.stButton button,.stDownloadButton button,[data-testid="stFormSubmitButton"] button,[data-testid="stFileUploader"] button {border-radius:14px!important;min-height:46px;border:1px solid #c4b5d8!important;background:#fff!important;color:#382d48!important;}
button p,button span {color:inherit!important;}
.stButton button:hover,.stDownloadButton button:hover {border-color:#7053b5!important;background:#f0e8ff!important;}
button[kind="primary"],button[kind="primaryFormSubmit"] {background:#65449f!important;color:#fff!important;border-color:#65449f!important;}
button[kind="primary"] p,button[kind="primaryFormSubmit"] p {color:#fff!important;}
[data-baseweb="select"]>div,[data-baseweb="input"],[data-baseweb="base-input"],[data-baseweb="textarea"] {background:#fff!important;color:#282131!important;border-color:#b9a7ce!important;border-radius:12px!important;}
input,textarea,select {background:#fff!important;color:#282131!important;-webkit-text-fill-color:#282131!important;caret-color:#65449f!important;}
input::placeholder,textarea::placeholder {color:#786e82!important;-webkit-text-fill-color:#786e82!important;opacity:1!important;}
[data-baseweb="select"] span,[data-baseweb="select"] div {color:#282131!important;}
[data-baseweb="select"] svg,[data-baseweb="input"] svg {fill:#554365!important;color:#554365!important;}
[data-baseweb="popover"],[data-baseweb="popover"]>div,[data-baseweb="menu"],[role="listbox"],[role="option"] {background:#fff!important;color:#282131!important;}
[role="option"]:hover {background:#e9dff9!important;}
[data-baseweb="calendar"],[data-baseweb="calendar"] div,[data-baseweb="calendar"] button {background:#fff;color:#282131!important;}
[data-testid="stAlert"] {background:#e7e0f1!important;border:1px solid #c9b7de;border-radius:18px;}
[data-testid="stAlert"] p {color:#3c2c51!important;}
[data-testid="stExpander"] {background:#e9e2f3;border-radius:18px;}
[data-testid="stFileUploaderDropzone"] {background:#f8f5fc!important;color:#282131!important;}
.st-key-bottom_nav {position:fixed!important;bottom:0;left:0;right:0;z-index:999;background:#fffdfd!important;border-top:1px solid #d8cde5;padding:10px max(12px,calc((100vw - 700px)/2)) calc(12px + env(safe-area-inset-bottom));box-shadow:0 -5px 24px #36234b12;}
.st-key-bottom_nav [data-testid="stHorizontalBlock"] {gap:6px;flex-wrap:nowrap!important;}
.st-key-bottom_nav [data-testid="stColumn"] {min-width:0!important;flex:1 1 0!important;width:auto!important;}
.st-key-bottom_nav button {width:100%;padding:8px 1px;border:0!important;font-size:13px;background:transparent!important;color:#6e6379!important;}
.st-key-bottom_nav button p {font-size:13px;white-space:nowrap;color:inherit!important;}
.st-key-bottom_nav button[kind="primary"] {background:#e4d7fa!important;color:#4e2f7e!important;}
.home-banner {background:#cdbdf2;border:1px solid #bca6e5;border-radius:26px;padding:24px;margin:12px 0 22px;}
.home-banner .eyebrow {font-size:11px;letter-spacing:2px;color:#514069;font-weight:800;}
.home-banner .headline {font-size:25px;line-height:1.45;color:#2c1d40;font-weight:850;letter-spacing:-1px;margin:8px 0;}
.home-banner .detail {font-size:13px;color:#514069;line-height:1.6;}
@media(max-width:480px){.block-container{padding-top:1rem;}h1{font-size:1.85rem!important;}[data-testid="stMetric"]{padding:13px 8px;min-height:100px;}[data-testid="stMetricValue"]{font-size:1.65rem!important;}[data-testid="stForm"]{padding:16px!important;}}
</style>""",unsafe_allow_html=True)
st.title("우리집 오늘판")
st.caption("OUR FAMILY, OUR LITTLE WORLD")
if 'page' not in st.session_state:st.session_state.page='오늘'
with st.container(key='bottom_nav'):
 nav=st.columns(4)
 for col,(icon,label) in zip(nav,[('☀️','오늘'),('🛒','부탁해'),('📅','이번 주'),('⚙️','설정')]):
  if col.button(icon+' '+label,key='nav_'+label,type='primary' if st.session_state.page==label else 'secondary',use_container_width=True):
   st.session_state.page=label;st.rerun()
page=st.session_state.page
FILE=Path('home_today.json')

@st.cache_resource
def lock():
 return threading.Lock()

def empty():
 return {'members':[],'days':{},'tasks':[]}

def read_disk():
 if not FILE.exists(): return {'revision':0,'data':empty()}
 return json.loads(FILE.read_text(encoding='utf-8'))

def save(data,revision):
 try:
  with lock():
   if read_disk()['revision']!=revision:
    st.warning('다른 가족이 먼저 수정했어요. 최신 화면에서 다시 시도해주세요.')
    st.stop()
   tmp=FILE.with_suffix('.tmp')
   tmp.write_text(json.dumps({'revision':revision+1,'data':data},ensure_ascii=False),encoding='utf-8')
   tmp.replace(FILE)
 except (OSError,ValueError,KeyError):
  st.error('저장하지 못했어요. 새로고침 후 다시 시도해주세요.');st.stop()
 st.rerun()

try:
 with lock(): row=read_disk()
except (OSError,ValueError):
 st.error('저장 파일을 읽지 못했어요. 기존 데이터를 보호하기 위해 실행을 중단합니다.');st.stop()
d=row['data'];revision=row['revision']
# 한국 기준 날짜 (별도 외부 서비스 불필요)
from datetime import timezone
today=datetime.now(timezone(timedelta(hours=9))).date()
if page=='설정':
 st.subheader('⚙️ 가족 설정')
 with st.form('member',clear_on_submit=True):
  name=st.text_input('가족 별명 추가',max_chars=20).strip()
  if st.form_submit_button('추가'):
   if not name:st.warning('별명을 입력해주세요.')
   elif name in d['members']:st.info('이미 등록한 별명이에요.')
   else:d['members'].append(name);save(d,revision)
 st.caption(' · '.join(d['members']) or '별명을 추가하면 바로 시작할 수 있어요.')
 st.caption('공용 공간: 주소를 아는 사람은 열람·수정할 수 있어요. 서버 초기화 시 사라질 수 있으니 백업해주세요.')
 st.download_button('💾 전체 백업',json.dumps(d,ensure_ascii=False,indent=2),'today_backup.json','application/json')
 with st.expander('백업 복원'):
  upload=st.file_uploader('JSON 백업',type=['json'])
  confirm=st.checkbox('현재 내용을 백업으로 교체합니다')
  if st.button('복원',disabled=not confirm):
   try:
    if upload is None:raise ValueError()
    v=json.load(upload)
    assert isinstance(v,dict) and isinstance(v.get('members'),list) and isinstance(v.get('days'),dict) and isinstance(v.get('tasks'),list)
    assert all(isinstance(n,str) and 0<len(n)<=20 for n in v['members'])
    assert len(v['members'])==len(set(v['members']))
    for day,entries in v['days'].items():
     date.fromisoformat(day);assert isinstance(entries,dict)
     for n,e in entries.items():
      assert isinstance(n,str) and isinstance(e,dict) and e.get('meal') in ['먹어요','안 먹어요','아직 몰라요'] and isinstance(e.get('arrival'),str)
    ids=[]
    for t in v['tasks']:
     assert isinstance(t,dict)
     assert all(isinstance(t.get(k),str) for k in ['id','title','category','due','owner','created'])
     assert t['title'] and isinstance(t.get('done'),bool)
     date.fromisoformat(t['due']);ids.append(t['id'])
    assert len(ids)==len(set(ids))
   except (ValueError,TypeError,AssertionError,KeyError):st.error('올바른 백업 파일을 선택해주세요.')
   else:save(v,revision)

if page=='설정':st.stop()
if not d['members']:
 st.info('가족 별명을 추가하면 바로 시작할 수 있어요.')
 if st.button('가족 별명 추가하기',type='primary'):
  st.session_state.page='설정';st.rerun()
 st.subheader('오늘 저녁, 몇 명이 먹을까요?')
 st.write('가족은 저녁 여부와 귀가 시간을 남기고, 필요한 물건이나 집안일은 서로 맡을 수 있어요.')
 st.stop()
actor=st.selectbox('나는 누구인가요?',d['members'])
if page=='오늘':
 st.markdown('<div class="home-banner"><div class="eyebrow">TOGETHER AT HOME</div><div class="headline">오늘도 함께,<br>우리집의 작은 하루 🏡</div><div class="detail">저녁 약속부터 오는 길의 작은 부탁까지.<br>우리 가족의 오늘을 여기에 모아요.</div></div>',unsafe_allow_html=True)
 st.subheader(today.strftime('%m월 %d일')+' · 우리집 오늘')
 key=today.isoformat();entries=d['days'].get(key,{})
 eat=sum(entries.get(n,{}).get('meal')=='먹어요' for n in d['members'])
 no=sum(entries.get(n,{}).get('meal')=='안 먹어요' for n in d['members'])
 unsure=len(d['members'])-eat-no
 cols=st.columns(3)
 cols[0].metric('🍚 저녁 확정',f'{eat}명');cols[1].metric('외식·불참',f'{no}명');cols[2].metric('미정·미응답',f'{unsure}명')
 st.caption('미정·미응답은 식사 불참으로 계산하지 않아요. 응답은 날짜별로 따로 저장됩니다.')
 current=entries.get(actor,{})
 with st.form('status'):
  statuses=['아직 몰라요','먹어요','안 먹어요']
  meal=st.radio('오늘 집에서 저녁 먹나요?',statuses,index=statuses.index(current.get('meal','아직 몰라요')),horizontal=True)
  options=['미정','집에 있어요']+[f'{h:02d}:{m:02d}' for h in range(24) for m in [0,30]]
  old=current.get('arrival','미정')
  arrival=st.selectbox('귀가 예정시간',options,index=options.index(old) if old in options else 0)
  if st.form_submit_button('내 상태 저장',type='primary',use_container_width=True):
   d['days'].setdefault(key,{})[actor]={'meal':meal,'arrival':arrival};save(d,revision)
 st.markdown('#### 가족 소식')
 for n in d['members']:
  e=entries.get(n,{})
  with st.container(border=True):
   st.write(f"**{n}** · 저녁 {e.get('meal','미응답')} · 귀가 {e.get('arrival','미정')}")
 urgent=[t for t in d['tasks'] if not t['done'] and t['due']<=key]
 if urgent:
  st.markdown('#### 오늘까지 챙길 부탁')
  for t in sorted(urgent,key=lambda t:(bool(t['owner']),t['due'])):
   st.write(f"{'⚠️ 기한 지남 · ' if t['due']<key else ''}{t['title']} — {t['owner'] or '🙋 담당자 없음'}")
if page=='부탁해':
 st.markdown('<div class="home-banner" style="background:#c6e8d0;border-color:#a6cdb2"><div class="eyebrow">A LITTLE HELP</div><div class="headline">오는 길에,<br>부탁 하나 해도 될까? 🛍️</div><div class="detail">작은 일을 나누면, 우리 모두의 하루가 가벼워져요.</div></div>',unsafe_allow_html=True)
 st.subheader('🛒 오는 길에 부탁해')
 st.caption('장보기뿐 아니라 반품·준비물·집안일도 함께 챙겨요.')
 with st.form('new_task',clear_on_submit=True):
  title=st.text_input('무엇이 필요한가요?',placeholder='예: 우유 1개 사오기 / 체육복 세탁하기',max_chars=120).strip()
  category=st.selectbox('종류',['장보기','집안일','반품·택배','준비물','기타'])
  due=st.date_input('언제까지?',today)
  if st.form_submit_button('부탁 등록',type='primary'):
   if not title:st.warning('부탁할 내용을 입력해주세요.')
   else:
    d['tasks'].append({'id':uuid.uuid4().hex,'title':title,'category':category,'due':due.isoformat(),'owner':'','done':False,'created':actor});save(d,revision)
 view=st.radio('보기',['할 일 전체','내가 맡은 일','완료한 일'],horizontal=True)
 tasks=[t for t in d['tasks'] if (t['done'] if view=='완료한 일' else not t['done'] and (view!='내가 맡은 일' or t['owner']==actor))]
 tasks.sort(key=lambda t:(bool(t['owner']),t['due']))
 if not tasks:st.success('이 목록에는 남은 부탁이 없어요!')
 for t in tasks:
  with st.container(border=True):
   st.markdown('**'+t['title']+'**')
   st.caption(f"{t['category']} · {t['due']}까지 · 부탁한 가족: {t['created']}")
   st.write('담당: '+(t['owner'] or '아직 없어요 🙋'))
   if not t['done'] and t['due']<today.isoformat():st.warning('기한이 지났어요.')
   x,y=st.columns(2)
   if not t['done']:
    if not t['owner']:
     if x.button('🙋 내가 할게',key='claim'+t['id'],use_container_width=True):t['owner']=actor;save(d,revision)
    elif t['owner']==actor:
     if x.button('맡기 취소',key='release'+t['id'],use_container_width=True):t['owner']='';save(d,revision)
    if t['owner']==actor:
     if y.button('✅ 완료',key='done'+t['id'],use_container_width=True):t['done']=True;save(d,revision)
   else:
    if x.button('다시 할 일로',key='undo'+t['id'],use_container_width=True):t['done']=False;save(d,revision)
if page=='이번 주':
 st.subheader('📅 이번 주에 챙길 일')
 monday=today-timedelta(days=today.weekday())
 for i in range(7):
  day=monday+timedelta(days=i);key=day.isoformat()
  with st.container(border=True):
   st.markdown(f"**{day.strftime('%m/%d')} ({'월화수목금토일'[i]}){' · 오늘' if day==today else ''}**")
   entries=d['days'].get(key,{})
   eating=[n for n in d['members'] if entries.get(n,{}).get('meal')=='먹어요']
   st.caption('저녁 식사 확정: '+(', '.join(eating) or '아직 없음'))
   items=[t for t in d['tasks'] if t['due']==key]
   if not items:st.write('등록된 부탁 없음')
   for t in items:st.write(f"{'✅' if t['done'] else '⬜'} {t['title']} · {t['owner'] or '담당 미정'}")
