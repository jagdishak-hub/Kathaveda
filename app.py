import csv,io,base64
from pathlib import Path
import streamlit as st
from knowledge import works,audit
from games_ui import games_ui
from settings_ui import profile_ui,settings_ui
from experience_ui import explore_library,stories_experience,reflect_experience
from learn_ui import learn_and_chant
from converse_ui import converse_ui

ROOT=Path(__file__).parent
st.set_page_config(page_title='Tattvika · Read, understand, chant and reflect',page_icon='🪷',layout='wide',initial_sidebar_state='collapsed')
st.markdown('''<style>
.stApp{background:radial-gradient(circle at 85% 4%,#fff7cb 0 3%,transparent 3.2%),linear-gradient(145deg,#f8fff1 0%,#edf8e8 48%,#fbf3df 100%);background-attachment:fixed}
.block-container{max-width:1320px;padding-top:1.1rem;padding-bottom:3rem}h1,h2,h3{color:#285c3a;font-family:Georgia,serif}p{line-height:1.65}
button{border-radius:999px!important}div[data-testid="stVerticalBlockBorderWrapper"]{background:#fffefa;border-radius:20px;border:1px solid #d4e3cb;box-shadow:0 8px 24px #28452f0c}
.rr-brand{display:flex;align-items:center;gap:16px;min-height:82px}.rr-brand img{width:76px;height:76px;object-fit:contain;filter:drop-shadow(0 5px 10px #294a2a20)}.rr-brand h1{font-size:2rem!important;margin:0!important;line-height:1}.rr-brand p{margin:7px 0 0;color:#607663;letter-spacing:.08em;font-size:.84rem;text-transform:uppercase}.rr-nav-rule{height:1px;background:linear-gradient(90deg,transparent,#9ebd91,transparent);margin:8px 0 24px}
.tv-kicker{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:#827451;font-weight:800}.tv-section-hero,.tv-reader-hero{padding:28px 32px;border-radius:26px;background:linear-gradient(125deg,#f3f9e9,#fff7de 58%,#f1ead8);border:1px solid #d9e4c9;margin:8px 0 20px}.tv-section-hero h2,.tv-reader-hero h2{font-size:2.15rem!important;margin:.3rem 0}.tv-section-hero p,.tv-reader-hero p{max-width:900px;color:#53695a;font-size:1.03rem}.tv-library-card{min-height:285px;padding:20px;border-radius:22px;background:#fffefa;border:1px solid #d7e2ce;box-shadow:0 8px 24px #28452f0c;margin-bottom:12px}
.stProgress>div>div{background:linear-gradient(90deg,#4e8c55,#d3a741)!important}@media(max-width:800px){.rr-brand img{width:58px;height:58px}.rr-brand h1{font-size:1.55rem!important}.rr-brand p{font-size:.68rem}.tv-section-hero,.tv-reader-hero{padding:22px}}
</style>''',unsafe_allow_html=True)

logo_data=base64.b64encode((ROOT/'assets/logo.svg').read_bytes()).decode()
from ambience import ambience_ui
brand,sound=st.columns([5,2])
with brand:
    st.markdown(f'<div class="rr-brand"><img alt="Tattvika logo" src="data:image/svg+xml;base64,{logo_data}"><div><h1>Tattvika</h1><p>Scripture · stories · chanting · reflection</p></div></div>',unsafe_allow_html=True)
with sound:ambience_ui()
from navigation import top_navigation
page=top_navigation()
st.markdown('<div class="rr-nav-rule"></div>',unsafe_allow_html=True)

if page=='Settings':profile_ui(location=st)

if page=='Home':
    from home_ui import home_ui
    home_ui()
elif page=='Reading room':
    explore_library()
elif page=='Story garden':
    stories_experience()
elif page=='Situations':
    reflect_experience()
elif page=='Learn & chant':
    learn_and_chant()
elif page=='Games':
    games_ui()
elif page=='Converse':
    converse_ui()
elif page=='Study my text':
    from upload_ui import upload_ui
    upload_ui()
elif page=='Settings':
    settings_ui()
elif page=='Coverage & sources':
    st.markdown('''<div class="tv-section-hero"><div class="tv-kicker">SOURCES & INTEGRITY</div><h2>See exactly what Tattvika contains.</h2><p>This audit page is intentionally separate from the reading flow. Coverage, edition, source and review status remain inspectable without sending a learner away from a verse or story.</p></div>''',unsafe_allow_html=True)
    report=audit()
    st.dataframe(report,hide_index=True,width='stretch')
    output=io.StringIO();writer=csv.DictWriter(output,fieldnames=report[0].keys());writer.writeheader();writer.writerows(report)
    st.download_button('Download coverage report',output.getvalue(),'tattvika-coverage.csv','text/csv')
    st.warning('A catalogue title does not automatically mean a complete critical edition. Tattvika reports the coverage actually stored in this build.')
    for w in works():
        with st.expander(w['title']+' · edition and rights'):
            for label,key in [('Edition','edition'),('Coverage','coverage'),('Source','sourceName'),('Rights','rights'),('Review','note')]:st.write('**'+label+'**: '+w.get(key,'Not recorded'))
            if w.get('sourceUrl'):st.link_button('Open source edition',w['sourceUrl'])
