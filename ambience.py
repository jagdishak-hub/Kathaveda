"""Small, opt-in garden soundscape generated in the browser; no audio tracking or downloads."""
import base64
import streamlit as st

def ambience_ui():
 html='''
 <style>
 body{margin:0;font-family:system-ui;color:#31533c;background:transparent}
 .box{display:flex;align-items:center;gap:10px;padding:7px 9px;border:1px solid #b9d7bd;border-radius:14px;background:#f7fff4cc}
 button{cursor:pointer;border:0;border-radius:999px;padding:7px 12px;background:#38744b;color:white;font-weight:700}
 small{line-height:1.25}.leaf{font-size:20px;animation:sway 2.4s ease-in-out infinite alternate}@keyframes sway{to{transform:rotate(12deg)}}
 @media(prefers-reduced-motion:reduce){.leaf{animation:none}}
 </style><div class="box"><span class="leaf">🌿</span><button id="sound">Play garden sounds</button><small>Soft flute & birds<br>optional · generated here</small></div>
 <script>
 let ctx,timer,on=false,nodes=[];const button=document.getElementById('sound');
 function tone(freq,when,duration,volume,type='sine'){
  const o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.value=freq;
  g.gain.setValueAtTime(0,when);g.gain.linearRampToValueAtTime(volume,when+.08);g.gain.exponentialRampToValueAtTime(.0001,when+duration);
  o.connect(g).connect(ctx.destination);o.start(when);o.stop(when+duration+.05);nodes.push(o)
 }
 function garden(){if(!on)return;const now=ctx.currentTime;[392,440,523,440].forEach((f,i)=>tone(f,now+i*1.15,.95,.025));tone(1250,now+.4,.18,.012,'sine');tone(1550,now+.58,.13,.01,'sine');tone(1180,now+3.0,.16,.009,'sine')}
 button.onclick=()=>{on=!on;if(on){ctx=ctx||new(window.AudioContext||window.webkitAudioContext)();garden();timer=setInterval(garden,5200);button.textContent='Pause garden sounds'}else{clearInterval(timer);nodes.forEach(n=>{try{n.stop()}catch(e){}});nodes=[];button.textContent='Play garden sounds'}};
 </script>'''
 st.iframe('data:text/html;base64,'+base64.b64encode(html.encode()).decode(),height=68)
