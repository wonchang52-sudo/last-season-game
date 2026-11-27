import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="너와 나의 마지막 계절", page_icon="🌸", layout="wide")

CHARACTERS = [
    {"name":"김서하","class":"1학년 3반","club":"도서부","personality":"차분하고 다정하지만 자신의 미래 앞에서는 망설임이 많다.","likes":"조용한 장소, 따뜻한 차, 오래된 책","intro":"도서관 창가에서 오래된 책갈피를 정리하고 있다.","line":"“이 책갈피, 누가 꽂아 둔 걸까? 오래전부터 여기 있었던 것 같아.”","choices":[("같이 찾아볼까?","함께라면 금방 찾을 수 있을 거야.",4,2,1),("책갈피가 예쁘네.","오래된 물건에는 이야기가 담겨 있는 것 같아.",2,1,2),("수업 늦겠다. 가자.","아, 응. 다음에 이어서 찾아보자.",-2,-1,0)]},
    {"name":"윤서아","class":"1학년 3반","club":"봉사부","personality":"주변을 잘 챙기지만 정작 자신에게 도움을 청하는 일은 서툴다.","likes":"봉사활동, 산책, 친구들과의 대화","intro":"점심시간, 친구들을 챙기느라 혼자 남아 있다.","line":"“다들 밥은 먹었겠지? 어라, 내 점심은 아직이네.”","choices":[("이번엔 내가 챙겨 줄게.","고마워. 누군가 나를 챙겨 주는 건 오랜만이야.",4,3,1),("같이 먹으러 가자.","좋아! 오늘은 천천히 먹을 수 있겠다.",3,2,0),("바쁘면 나중에 먹어.","응, 조금만 더 정리하고 갈게.",-1,0,0)]},
    {"name":"강하린","class":"1학년 3반","club":"농구부","personality":"활발하고 장난기가 많지만 관계가 변하는 것을 두려워한다.","likes":"농구, 운동장, 아이스크림","intro":"체육관에서 농구공을 튀기고 있다.","line":"“첫날부터 슛 연습 중! 너도 한 번 해 볼래?”","choices":[("좋아, 같이 하자!","하하, 좋아! 오늘은 네가 내 연습 상대야.",4,2,1),("네 슛을 구경할게.","그럼 멋진 슛 보여 줘야겠네!",2,1,1),("난 운동은 별로야.","아쉽네. 다음에 마음 바뀌면 말해!",-1,0,0)]},
    {"name":"최유나","class":"1학년 3반","club":"학술부","personality":"똑똑하고 완벽주의 성향이 있지만 성적에 대한 부담이 크다.","likes":"문제 풀이, 정리된 노트, 조용한 공부","intro":"교실에서 틀린 문제 하나를 오래 바라보고 있다.","line":"“이상하네. 분명 맞게 풀었다고 생각했는데…”","choices":[("같이 풀이를 확인해 보자.","좋아. 다른 관점에서 보면 답이 보일지도 몰라.",4,2,1),("실수해도 괜찮아.","그렇게 말해 주니 조금 마음이 놓인다.",3,3,0),("그 정도는 쉬운 문제잖아.","…알아. 그래서 더 신경 쓰여.",-3,-2,0)]},
    {"name":"한이서","class":"1학년 3반","club":"미술부","personality":"수줍음이 많고 그림을 좋아하지만 자신감이 부족하다.","likes":"수채화, 풍경, 스케치북","intro":"미술실 구석에서 미완성 그림을 그리고 있다.","line":"“아직 완성하지 못했어. 누가 보면 조금 부끄러울 것 같아.”","choices":[("나는 이 그림이 마음에 들어.","정말? 네가 그렇게 말해 주니 용기가 생겨.",4,3,1),("어떤 그림을 그리고 싶었어?","하늘이랑 바다를 함께 담고 싶었어.",3,2,2),("완성되면 보여 줘.","응. 언젠가는 꼭 보여 줄게.",1,1,0)]},
    {"name":"정다은","class":"1학년 3반","club":"사진부","personality":"사교적이며 순간을 사진으로 기록하지만 자신의 모습은 잘 남기지 않는다.","likes":"카메라, 햇살, 친구들의 자연스러운 표정","intro":"복도에서 친구들의 사진을 정리하고 있다.","line":"“사진에는 다들 있는데, 이상하게 내 사진은 별로 없어.”","choices":[("우리 같이 사진 찍자.","좋아! 오늘의 첫 단체 사진이네.",4,2,1),("네가 찍은 사진도 멋져.","고마워. 찍는 사람도 사진 속에 남으면 좋겠다.",3,2,2),("사진은 나중에 봐도 되잖아.","그렇긴 하지만 지금의 순간도 소중한걸.",0,0,0)]},
    {"name":"오채린","class":"1학년 3반","club":"음악부","personality":"자존심이 강하고 피아노 실력이 뛰어나지만 가족의 기대에 부담을 느낀다.","likes":"피아노, 클래식 음악, 악보","intro":"음악실에서 피아노 연주를 멈추고 악보를 덮는다.","line":"“오늘은 손이 잘 안 움직이네. 연습을 더 해야 하나 봐.”","choices":[("잠깐 쉬어도 괜찮아.","…그 말, 듣고 싶었나 봐. 고마워.",4,3,1),("네가 좋아하는 곡을 들려줘.","좋아. 오늘은 내가 정말 좋아하는 곡을 연주할게.",3,2,1),("계속 연습하면 되겠지.","맞아. 하지만 가끔은 그게 쉽지 않아.",0,-1,0)]},
    {"name":"서민지","class":"1학년 3반","club":"게임개발부","personality":"장난스럽고 창의적이며 직접 게임을 만드는 것이 꿈이다.","likes":"게임, 프로그래밍, 새로운 아이디어","intro":"노트북 화면에 직접 만든 게임을 띄워 놓았다.","line":"“내가 만든 게임인데, 주인공 이름을 아직 못 정했어!”","choices":[("내 이름을 써도 돼?","좋아! 그럼 네가 첫 번째 플레이어야.",4,2,1),("게임 아이디어가 재밌다.","진짜? 다음 버전도 같이 테스트해 줘!",3,2,1),("게임은 별로 안 좋아해.","아하, 그럼 다른 이야기 해 보자.",-1,0,0)]},
    {"name":"백소윤","class":"1학년 3반","club":"천문부","personality":"조용하고 별을 관찰하는 것을 좋아한다.","likes":"별자리, 밤하늘, 천문학 책","intro":"창가에서 흐린 하늘을 올려다보고 있다.","line":"“오늘은 구름이 많아서 별을 보기 어렵겠어.”","choices":[("다음에 맑은 날 같이 보자.","약속이야. 맑은 밤을 기다려 볼게.",4,2,2),("별자리를 알려 줄래?","물론이지. 북쪽 하늘부터 알려 줄게.",3,2,1),("별은 잘 모르겠어.","괜찮아. 천천히 알아 가면 돼.",1,1,0)]},
    {"name":"이수빈","class":"1학년 3반","club":"농구부","personality":"솔직하고 승부욕이 강하지만 과거의 실수로 고민한다.","likes":"농구, 기록 갱신, 팀워크","intro":"체육관에서 자유투를 연습하고 있다.","line":"“이번엔 꼭 성공하고 싶어. 지난번 실수가 계속 생각나.”","choices":[("실수보다 다음 슛이 중요해.","맞아. 다음 기회에 집중해 볼게.",4,3,1),("내가 리바운드해 줄게.","좋아! 든든한데?",3,2,1),("긴장하지 마.","말은 쉽지만… 그래도 고마워.",1,1,0)]},
    {"name":"임예린","class":"1학년 3반","club":"봉사부","personality":"차분하고 남을 잘 돕지만 자신의 꿈은 아직 찾는 중이다.","likes":"봉사활동, 식물, 조용한 대화","intro":"교실 화분에 물을 주고 있다.","line":"“작은 화분도 매일 돌봐 주면 조금씩 자라더라.”","choices":[("너도 네 속도로 자라면 돼.","그 말이 참 좋다. 나도 천천히 찾아볼게.",4,3,2),("무슨 꽃을 좋아해?","나는 작고 소박한 꽃이 좋아.",2,2,1),("화분 관리 힘들겠다.","가끔은 그렇지만 보람 있어.",1,1,0)]},
    {"name":"조하은","class":"1학년 3반","club":"음악부","personality":"수줍음이 많고 작곡에 재능이 있지만 곡을 들려주는 것을 어려워한다.","likes":"작곡, 피아노, 조용한 음악실","intro":"악보에 짧은 멜로디를 적고 있다.","line":"“아직 아무에게도 들려주지 않은 멜로디야.”","choices":[("언젠가 꼭 들려줘.","응. 네가 처음 듣는 사람이면 좋겠다.",4,3,1),("어떤 기분을 담았어?","봄이 시작될 때의 설렘을 담았어.",3,2,2),("혼자 간직해도 괜찮아.","고마워. 그래도 언젠가는 용기 내 볼게.",2,2,1)]},
    {"name":"문가영","class":"1학년 3반","club":"방송부","personality":"자신감 있고 밝지만 속마음을 감추곤 한다.","likes":"방송, 진행, 사람들과 어울리기","intro":"방송실에서 첫 멘트를 연습하고 있다.","line":"“안녕하세요! 은월고 방송부의… 아, 또 틀렸네!”","choices":[("실수해도 자연스러웠어.","정말? 조금 긴장이 풀리는 것 같아.",4,2,1),("다시 한번 해 보자.","좋아! 이번엔 더 잘할 수 있어.",3,2,0),("긴장한 것 같은데?","티 났어? 사실 조금 떨려.",1,1,0)]},
    {"name":"신유리","class":"1학년 3반","club":"문예부","personality":"말수가 적고 글로 감정을 표현하는 데 익숙하다.","likes":"시집, 편지, 비 오는 날","intro":"공책에 짧은 문장을 적고 있다.","line":"“말로 하면 어색한 마음도 글로 쓰면 조금 쉬워져.”","choices":[("네 글을 읽어 보고 싶어.","정말? 아직 부족하지만 보여 줄게.",4,3,2),("어떤 이야기를 쓰고 있어?","처음 만난 사람에 관한 이야기야.",3,2,1),("글쓰기는 어렵지 않아?","어렵지만 그래서 더 좋아.",1,1,0)]},
    {"name":"장세아","class":"1학년 3반","club":"학생회","personality":"책임감 있고 침착하지만 혼자 쉬는 법을 잘 모른다.","likes":"계획표, 정리, 조용한 산책","intro":"학생회 자료를 정리하다 잠시 창밖을 바라본다.","line":"“아직 할 일이 남았는데, 잠깐 쉬어도 괜찮을까?”","choices":[("물론이지. 잠깐 같이 쉬자.","고마워. 누군가와 쉬는 것도 괜찮네.",4,3,1),("내가 자료 정리 도와줄게.","정말? 덕분에 금방 끝나겠어.",3,2,1),("학생회장은 바쁘구나.","응. 그래도 내가 선택한 일이니까.",1,1,0)]},
    {"name":"권나연","class":"1학년 3반","club":"댄스부","personality":"사교적이고 춤을 좋아하지만 다른 사람과 자신을 비교한다.","likes":"춤, 음악, 무대","intro":"거울 앞에서 안무를 반복해서 연습하고 있다.","line":"“다른 애들은 금방 하는데 나는 왜 이렇게 어색하지?”","choices":[("네 방식대로 추면 돼.","그 말 들으니까 내 춤을 생각하게 된다.",4,3,1),("같이 연습할까?","좋아! 혼자보다 훨씬 재밌겠다.",3,2,1),("계속 연습하면 되겠지.","응, 조금씩 나아질 거야.",1,1,0)]},
    {"name":"배시은","class":"1학년 3반","club":"미가입","personality":"조용하고 비밀스러운 분위기이며 오래된 사진과 기록에 관심이 있다.","likes":"오래된 사진, 학교 기록, 낡은 편지","intro":"오래된 교내 게시판 앞에서 사진 한 장을 바라보고 있다.","line":"“이 사진… 우리 학교에서 찍은 건데, 날짜가 이상해.”","choices":[("무슨 사진인지 같이 살펴보자.","좋아. 혼자 보는 것보다 나을 것 같아.",4,3,3),("사진 속 장소를 찾아보자.","응. 학교 어딘가에 단서가 있을지도 몰라.",3,2,3),("오래된 사진이네.","그렇지. 그런데 그냥 오래된 사진은 아닌 것 같아.",1,1,1)]},
]

def init_state():
    if "relations" not in st.session_state:
        st.session_state.relations = {c["name"]: {"affection": 0, "trust": 0, "memories": 0} for c in CHARACTERS}
    if "selected" not in st.session_state:
        st.session_state.selected = CHARACTERS[0]["name"]
    if "history" not in st.session_state:
        st.session_state.history = []
    if "scene_count" not in st.session_state:
        st.session_state.scene_count = 0

def stage(value):
    if value < 20: return "낯선 사이"
    if value < 40: return "아는 사이"
    if value < 60: return "친한 친구"
    if value < 75: return "특별한 친구"
    if value < 90: return "사랑의 감정"
    return "깊은 사랑"

def choose(choice):
    c = next(x for x in CHARACTERS if x["name"] == st.session_state.selected)
    rel = st.session_state.relations[c["name"]]
    label, response, a, t, m = choice
    rel["affection"] = max(0, min(100, rel["affection"] + a))
    rel["trust"] = max(0, min(100, rel["trust"] + t))
    rel["memories"] += m
    st.session_state.history.insert(0, f'{c["name"]}: {label} (호감도 {a:+d})')
    st.session_state.history = st.session_state.history[:8]
    st.session_state.last_response = response
    st.session_state.scene_count += 1

init_state()
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Noto Sans KR',sans-serif;}
.stApp {background:linear-gradient(135deg,#fff8fb 0%,#f8f6ff 55%,#f4f8ff 100%);}
.block-container {padding-top:1.4rem;max-width:1180px;}
.hero {background:linear-gradient(115deg,#392c48,#76536f);color:white;padding:25px 30px;border-radius:22px;margin-bottom:18px;box-shadow:0 12px 30px #4d35551c;}
.hero small {letter-spacing:3px;color:#f6dce9;font-weight:600;}
.hero h1 {font-size:2rem;margin:8px 0 4px;font-weight:800;}
.hero p {margin:0;color:#f4eaf2;}
.panel {background:#ffffffd9;border:1px solid #eee4ef;border-radius:18px;padding:19px 20px;box-shadow:0 7px 24px #5b3b5b0c;margin-bottom:13px;}
.muted {color:#847889;font-size:.88rem;}
.dialogue {background:#fff;border:1px solid #f0e4ee;border-radius:16px;padding:20px;min-height:130px;}
.speaker {color:#9b668b;font-weight:800;margin-bottom:8px;}
.dialogue p {font-size:1.05rem;line-height:1.8;color:#342b38;margin:0;}
.heart {color:#dc7199;font-size:1.5rem;}
div.stButton > button {border-radius:12px;border:1px solid #eadce9;background:#fff;color:#4a394b;min-height:48px;font-weight:600;}
div.stButton > button:hover {border-color:#d58eaf;color:#a54f7b;background:#fff8fb;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><small>THE LAST SEASON WITH YOU</small><h1>너와 나의 마지막 계절</h1><p>열일곱 개의 마음, 세 번의 봄, 그리고 오래도록 남을 우리의 이야기</p></div>', unsafe_allow_html=True)

left, right = st.columns([0.95, 2.05], gap="large")
with left:
    st.markdown('<div class="panel"><b>🌷 오늘 누구와 시간을 보낼까?</b><div class="muted">은월고등학교 · 1학년 1학기 · 봄</div></div>', unsafe_allow_html=True)
    selected = st.selectbox("캐릭터", [c["name"] for c in CHARACTERS], index=[c["name"] for c in CHARACTERS].index(st.session_state.selected), label_visibility="collapsed")
    if selected != st.session_state.selected:
        st.session_state.selected = selected
        st.rerun()
    char = next(c for c in CHARACTERS if c["name"] == selected)
    rel = st.session_state.relations[selected]
    st.markdown(f'<div class="panel"><div class="muted">{char["class"]} · {char["club"]}</div><h2 style="margin:5px 0 8px">{char["name"]}</h2><p>{char["personality"]}</p><div class="muted">좋아하는 것</div><b>{char["likes"]}</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="heart">♥ 호감도　<strong>{rel["affection"]}/100</strong></div><div style="color:#a16b8e;font-weight:700;margin:4px 0 10px">{stage(rel["affection"])}</div>', unsafe_allow_html=True)
    st.progress(rel["affection"]/100)
    st.markdown(f'<div class="muted">신뢰도　<strong>{rel["trust"]}/100</strong></div>')
    st.progress(rel["trust"]/100)
    st.markdown(f'<div class="muted">함께 만든 추억　<strong>{rel["memories"]}</strong></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("↻ 전체 진행 초기화", use_container_width=True):
        for key in ["relations","history","scene_count","last_response"]:
            if key in st.session_state: del st.session_state[key]
        st.rerun()

with right:
    st.markdown('<div class="panel"><b>📖 Chapter 01 · 오래된 책갈피</b><div class="muted">4월 · 월요일 · 방과 후</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dialogue"><div class="speaker">{char["name"]}</div><p>{char["intro"]}<br><br>{char["line"]}</p></div>', unsafe_allow_html=True)
    if "last_response" in st.session_state:
        st.success(st.session_state.last_response)
    st.markdown("#### 어떻게 대답할까?")
    for i, choice in enumerate(char["choices"]):
        if st.button(choice[0], key=f'{selected}_{i}', use_container_width=True):
            choose(choice)
            st.rerun()
    st.markdown('<div class="muted" style="margin-top:12px">선택에 따라 호감도, 신뢰도, 추억이 달라져. 호감도는 관계의 감정적 변화를, 신뢰도와 추억은 별도의 이야기 장면을 여는 데 사용돼.</div>', unsafe_allow_html=True)
    with st.expander("🕰️ 최근 선택 기록"):
        if st.session_state.history:
            for item in st.session_state.history: st.write("· " + item)
        else:
            st.caption("아직 선택한 기록이 없어.")
    with st.expander("💾 진행 데이터 내보내기"):
        payload = {"relations": st.session_state.relations, "history": st.session_state.history, "scene_count": st.session_state.scene_count}
        st.download_button("진행 데이터 JSON 다운로드", json.dumps(payload, ensure_ascii=False, indent=2), file_name="last_season_save.json", mime="application/json", use_container_width=True)

st.caption("프로토타입 · 현재 진행 데이터는 브라우저 세션에 유지되며, JSON으로 내보낼 수 있어. 실제 계정 간 저장 기능은 아직 포함되어 있지 않아.")

