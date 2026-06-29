import pandas as pd, json

path = r'C:\Users\s9qer6\_Claude\RTCF\COZY FLEURIST - Pétales FR.xlsx'
df = pd.read_excel(path, sheet_name='Fleurs', header=None)

players = [str(df.iloc[0,i]).strip() for i in range(1,df.shape[1])
           if str(df.iloc[0,i]).strip() not in ('','nan','NaN')]

def short_name(n):
    p = n.split('/')[-1].strip() if '/' in n else n
    return p.split()[0] if p else n[:10]

flowers = []
for r in range(2, df.shape[0]):
    name = str(df.iloc[r,0]).strip()
    if not name or name in ('nan','NaN'): continue
    owned = [j for j in range(len(players)) if str(df.iloc[r,j+1]).strip()=='X']
    flowers.append({'n':name,'o':owned})

INITIAL = json.dumps({'players':players,'shorts':[short_name(p) for p in players],'flowers':flowers},ensure_ascii=False)

# ── CSS ─────────────────────────────────────────────────────────────────────
CSS = """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html{height:100%}
body{height:100vh;height:100dvh;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;background:#F7F9FC;color:#111827;display:flex;flex-direction:column;font-size:14px}
main{flex:1;overflow:hidden;position:relative;min-height:0}
/* Mode paysage mobile : UI compacte */
@media(orientation:landscape)and(max-height:520px){
  .hdr{height:40px}
  .bnav{height:48px}
  .fab{bottom:56px}
  .sticky-top{padding-top:6px;padding-bottom:6px}
  .profbar{padding:6px 13px;margin-bottom:6px}
  .progcard{padding:8px 14px;margin-bottom:6px}
  .prog-bar-lg{margin-top:5px}
  .scroll-area{padding-top:8px;padding-bottom:8px}
}
.view{position:absolute;inset:0;overflow:hidden;display:flex;flex-direction:column;opacity:0;pointer-events:none;transition:opacity .18s}
.view.active{opacity:1;pointer-events:auto}
.sticky-top{flex-shrink:0;background:#F7F9FC;padding:14px clamp(16px,4vw,64px) 12px;border-bottom:1px solid #E8ECF2}
.scroll-area{flex:1 1 0;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;touch-action:pan-y;overscroll-behavior-y:contain;padding:14px clamp(16px,4vw,64px) 20px}
.hdr{background:linear-gradient(135deg,#C2185B,#6D28D9);color:#fff;height:52px;padding:0 clamp(16px,4vw,64px);display:flex;align-items:center;gap:10px;flex-shrink:0;z-index:30}
.hdr-logo{font-size:.95rem;font-weight:700;flex:1;letter-spacing:-.02em}
.sync-dot{width:9px;height:9px;border-radius:50%;background:#10B981;flex-shrink:0;transition:background .4s;cursor:default}
.slbl{font-size:.68rem;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:.08em;margin:16px 0 8px}
.slbl:first-child{margin-top:0}
.card{background:#fff;border:1px solid #E8ECF2;border-radius:10px;padding:14px 16px;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:10px}
.litem{background:#fff;border:1px solid #E8ECF2;border-radius:10px;padding:11px 13px;margin-bottom:6px;cursor:pointer;display:flex;align-items:center;gap:11px;transition:border-color .12s,background .12s}
.litem:hover{border-color:#C2185B;background:#FFF0F5}
.litem:active{background:#FCE4EC}
.litem-ico{width:34px;height:34px;border-radius:8px;background:#F1F5F9;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0}
.litem-body{flex:1;min-width:0}
.litem-name{font-size:.875rem;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#111827}
.litem-sub{font-size:.72rem;color:#9CA3AF;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.litem-right{display:flex;align-items:center;gap:7px;flex-shrink:0}
.chevron{color:#E8ECF2;font-size:.8rem}
.badge{border-radius:5px;padding:2px 7px;font-size:.7rem;font-weight:600;font-variant-numeric:tabular-nums}
.b-pk{background:#FCE4EC;color:#880E4F}
.b-gr{background:#D1FAE5;color:#047857}
.b-0{background:#F1F5F9;color:#9CA3AF}
.b-am{background:#FEF3C7;color:#B45309}
.bar{height:3px;border-radius:2px;background:#F1F5F9;margin-top:6px;overflow:hidden}
.bar-fill{height:100%;border-radius:2px;transition:width .4s ease}
.bpk{background:linear-gradient(135deg,#C2185B,#6D28D9)}
.bgr{background:linear-gradient(90deg,#059669,#34D399)}
.sbox{position:relative}
.sinput{width:100%;border:1px solid #E8ECF2;border-radius:10px;padding:9px 12px 9px 36px;font-size:.875rem;background:#fff;color:#111827;outline:none;box-shadow:0 1px 3px rgba(0,0,0,.07);transition:border-color .15s}
.sinput:focus{border-color:#C2185B;box-shadow:0 0 0 3px rgba(194,24,91,.1)}
.sico{position:absolute;left:11px;top:50%;transform:translateY(-50%);font-size:.8rem;color:#9CA3AF;pointer-events:none}
.fchips{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;margin-top:8px;scrollbar-width:none}
.fchips::-webkit-scrollbar{display:none}
.fchip{border:1px solid #E8ECF2;border-radius:5px;padding:4px 10px;font-size:.72rem;background:#fff;color:#4B5563;cursor:pointer;white-space:nowrap;font-weight:500;transition:.12s}
.fchip.active{background:#C2185B;border-color:#C2185B;color:#fff;font-weight:600}
.fsort{display:flex;justify-content:flex-end;margin-top:6px}
.ppgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.ppbtn{background:#fff;border:1px solid #E8ECF2;border-radius:10px;padding:14px 10px;cursor:pointer;text-align:center;transition:.12s;box-shadow:0 1px 3px rgba(0,0,0,.07);width:100%}
.ppbtn:hover{border-color:#C2185B;background:#FFF0F5}
.ppbtn-ico{font-size:1.5rem;margin-bottom:5px}
.ppbtn-name{font-size:.82rem;font-weight:700;color:#111827}
.ppbtn-full{font-size:.67rem;color:#9CA3AF;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.profbar{display:flex;align-items:center;gap:11px;background:#fff;border:1px solid #E8ECF2;border-radius:10px;padding:11px 13px;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:10px}
.profavo{width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#C2185B,#6D28D9);display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:700;color:#fff;flex-shrink:0}
.profinfo{flex:1;min-width:0}
.profname{font-size:.875rem;font-weight:700;color:#111827}
.proffull{font-size:.7rem;color:#9CA3AF;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chg-btn{background:transparent;border:1px solid #E8ECF2;color:#9CA3AF;border-radius:6px;padding:4px 10px;font-size:.72rem;cursor:pointer;font-weight:500;white-space:nowrap}
.chg-btn:hover{border-color:#C2185B;color:#C2185B}
.progcard{background:#fff;border:1px solid #E8ECF2;border-radius:10px;padding:14px 16px;margin-bottom:10px;box-shadow:0 1px 3px rgba(0,0,0,.07)}
.prog-nums{display:flex;align-items:baseline;gap:6px;margin-bottom:4px}
.prog-big{font-size:1.6rem;font-weight:800;color:#111827;line-height:1}
.prog-total{font-size:.8rem;color:#9CA3AF}
.prog-pct{font-size:.82rem;font-weight:600;color:#C2185B;margin-left:auto}
.prog-bar-lg{height:6px;border-radius:3px;background:#F1F5F9;margin-top:8px;overflow:hidden}
.prog-fill-lg{height:100%;border-radius:3px;background:linear-gradient(135deg,#C2185B,#6D28D9);transition:width .5s ease}
.prog-sub{font-size:.7rem;color:#9CA3AF;margin-top:5px}
.qtoggle{border:1px solid transparent;border-radius:6px;padding:5px 11px;cursor:pointer;font-size:.75rem;font-weight:600;white-space:nowrap;transition:.12s;flex-shrink:0;min-width:84px;text-align:center}
.qtoggle.on{background:#D1FAE5;border-color:#059669;color:#047857}
.qtoggle.off{background:#FCE4EC;border-color:#C2185B;color:#880E4F}
.qtoggle:active{opacity:.75;transform:scale(.96)}
.bnav{height:60px;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);border-top:1px solid #E8ECF2;display:flex;flex-shrink:0;z-index:30}
.nbtn{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border:none;background:none;cursor:pointer;color:#9CA3AF;transition:.12s;padding:6px 0}
.nbtn.active{color:#C2185B}
.nico{font-size:1.2rem;line-height:1;transition:transform .12s}
.nbtn.active .nico{transform:scale(1.1)}
.nlbl{font-size:.6rem;font-weight:600;letter-spacing:.02em}
.fab{position:fixed;bottom:74px;right:20px;height:46px;padding:0 20px;border-radius:23px;border:none;background:linear-gradient(135deg,#C2185B,#6D28D9);color:#fff;font-size:.82rem;font-weight:700;box-shadow:0 4px 14px rgba(194,24,91,.4);cursor:pointer;z-index:40;display:flex;align-items:center;gap:6px;transition:transform .12s,opacity .2s}
.fab:active{transform:scale(.95)}
.fab.hidden{opacity:0;pointer-events:none;transform:scale(.8)}
.shbg{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:60;opacity:0;pointer-events:none;transition:opacity .22s}
.shbg.open{opacity:1;pointer-events:auto}
.sheet{position:fixed;bottom:0;left:0;right:0;background:#fff;border-radius:16px 16px 0 0;z-index:61;padding:0 18px 34px;transform:translateY(105%);transition:transform .3s cubic-bezier(.4,0,.2,1);max-height:88vh;overflow-y:auto;box-shadow:0 -4px 24px rgba(0,0,0,.12)}
.sheet.open{transform:translateY(0)}
.sh-handle{width:36px;height:3px;background:#E8ECF2;border-radius:2px;margin:12px auto 18px}
.sh-title{font-size:.95rem;font-weight:700;margin-bottom:14px;color:#111827}
.sh-input{width:100%;border:1px solid #E8ECF2;border-radius:10px;padding:10px 13px;font-size:.875rem;background:#F7F9FC;color:#111827;outline:none;margin-bottom:12px}
.sh-input:focus{border-color:#C2185B;box-shadow:0 0 0 3px rgba(194,24,91,.1)}
.sh-btns{display:flex;gap:8px}
.picker-inp{width:100%;border:1px solid #E8ECF2;border-radius:10px;padding:9px 13px 9px 36px;font-size:.875rem;background:#F7F9FC;color:#111827;outline:none;margin-bottom:10px}
.picker-inp:focus{border-color:#C2185B}
.picker-list{max-height:52vh;overflow-y:auto;-webkit-overflow-scrolling:touch}
.picker-item{display:flex;align-items:center;gap:9px;padding:9px 0;border-bottom:1px solid #F1F5F9;cursor:pointer}
.picker-item:last-child{border-bottom:none}
.picker-name{flex:1;font-size:.82rem;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#111827}
.picker-add{background:#D1FAE5;color:#047857;border:1px solid #059669;border-radius:5px;padding:4px 10px;font-size:.72rem;font-weight:600;cursor:pointer;flex-shrink:0}
.picker-new{background:#FFF0F5;border:1px solid #FCE4EC;border-radius:10px;padding:11px 13px;margin-top:6px;cursor:pointer;font-size:.82rem;line-height:1.5;color:#4B5563}
.picker-new strong{color:#C2185B}
.picker-empty{text-align:center;color:#9CA3AF;padding:20px 0;font-size:.82rem}
.dview{position:fixed;inset:0;background:#F7F9FC;z-index:50;transform:translateX(105%);transition:transform .28s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;overflow:hidden}
.dview.open{transform:translateX(0)}
.dhdr{background:linear-gradient(135deg,#C2185B,#6D28D9);color:#fff;height:52px;padding:0 14px;display:flex;align-items:center;gap:10px;flex-shrink:0}
.back-btn{background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.2);color:#fff;border-radius:6px;padding:5px 12px;cursor:pointer;font-size:.75rem;font-weight:600}
.dtitle{flex:1;font-size:.9rem;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.del-btn{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.2);color:#fff;border-radius:6px;padding:5px 9px;cursor:pointer;font-size:.8rem}
.del-btn:hover{background:rgba(185,28,28,.5)}
.dbody{flex:1;overflow-y:auto;padding:14px}
.chip-grid{display:flex;flex-wrap:wrap;gap:5px}
.ochip{border:1px solid #E8ECF2;border-radius:5px;padding:5px 10px;font-size:.75rem;font-weight:500;cursor:pointer;transition:.12s;background:#fff;color:#4B5563}
.ochip.on{background:#D1FAE5;border-color:#059669;color:#047857;font-weight:600}
.ochip:active{transform:scale(.94)}
.mg-sec{margin-bottom:20px}
.mg-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;padding-right:14px}
.mg-title{font-size:.82rem;font-weight:700;color:#111827}
.add-btn{background:#FCE4EC;color:#880E4F;border:1px solid #C2185B;border-radius:6px;padding:5px 11px;font-size:.72rem;font-weight:600;cursor:pointer}
.add-btn:hover{background:#C2185B;color:#fff}
.mgitem{background:#fff;border:1px solid #E8ECF2;border-radius:6px;padding:9px 12px;margin-bottom:5px;display:flex;align-items:center;gap:9px}
.mgname{flex:1;font-size:.8rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#111827}
.del{background:#FEE2E2;color:#B91C1C;border:1px solid #FECACA;border-radius:5px;padding:4px 9px;font-size:.72rem;cursor:pointer;font-weight:600;flex-shrink:0}
.del:hover{background:#B91C1C;color:#fff}
.btn{border:none;border-radius:6px;padding:11px 18px;font-size:.82rem;font-weight:600;cursor:pointer;transition:.12s}
.btn:active{opacity:.8}
.btn-pk{background:linear-gradient(135deg,#C2185B,#6D28D9);color:#fff;flex:1}
.btn-ghost{background:#F7F9FC;border:1px solid #E8ECF2;color:#4B5563}
.btn-red{background:#B91C1C;color:#fff;flex:1}
.btn-outline{display:block;width:100%;background:#fff;border:1px solid #E8ECF2;color:#4B5563;border-radius:10px;padding:10px 16px;font-size:.8rem;cursor:pointer;font-weight:500;text-align:center;margin-bottom:7px;transition:.12s}
.btn-outline:hover{border-color:#C2185B;color:#C2185B;background:#FFF0F5}
.cfbg{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:100;display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;pointer-events:none;transition:opacity .18s}
.cfbg.open{opacity:1;pointer-events:auto}
.cfbox{background:#fff;border-radius:14px;padding:22px 20px;max-width:310px;width:100%;box-shadow:0 20px 40px rgba(0,0,0,.2)}
.cftitle{font-size:.9rem;font-weight:700;margin-bottom:5px;color:#111827}
.cfmsg{font-size:.78rem;color:#4B5563;margin-bottom:18px;line-height:1.55}
.cfbtns{display:flex;gap:8px}
.toast{position:fixed;bottom:70px;left:50%;transform:translateX(-50%) translateY(50px);background:rgba(17,24,39,.92);color:#fff;border-radius:8px;padding:9px 18px;font-size:.8rem;font-weight:500;z-index:200;transition:transform .25s,opacity .25s;opacity:0;white-space:nowrap;pointer-events:none;max-width:88vw;overflow:hidden;text-overflow:ellipsis}
.toast.show{transform:translateX(-50%) translateY(0);opacity:1}
.b-N{background:#D1FAE5;color:#047857}
.b-R{background:#BAE6FD;color:#0369A1}
.b-SR{background:#EDE9FE;color:#5B21B6}
.b-SSR{background:#FEF9C3;color:#A16207}
.b-UR{background:#FEE2E2;color:#B91C1C}
.pts{font-size:.68rem;font-weight:700;color:#5B21B6;background:#EDE9FE;border-radius:4px;padding:2px 6px;flex-shrink:0;min-width:46px;text-align:center;display:inline-block}
.badge-r{min-width:36px;text-align:center;display:inline-block;font-weight:700}
.edit-lbl{font-size:.72rem;color:#C2185B;cursor:pointer;text-decoration:underline dotted;text-underline-offset:3px;flex-shrink:0}
.rsel{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:10px}
.rsel-btn{border:1px solid #E8ECF2;border-radius:5px;padding:5px 11px;font-size:.75rem;font-weight:600;cursor:pointer;background:#fff;color:#4B5563;transition:.12s}
.rsel-btn.on{border-color:#C2185B;background:#FCE4EC;color:#880E4F}
.empty{text-align:center;color:#9CA3AF;padding:28px 10px;font-size:.82rem}
::-webkit-scrollbar{width:7px;height:7px}
::-webkit-scrollbar-track{background:#F1F5F9;border-radius:4px}
::-webkit-scrollbar-thumb{background:#C2185B55;border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:#C2185B}
"""

# ── HTML ─────────────────────────────────────────────────────────────────────
BODY = """
<div id="loading" style="position:fixed;inset:0;background:#F7F9FC;display:flex;align-items:center;justify-content:center;z-index:300">
  <div style="text-align:center">
    <div style="font-size:2.8rem;margin-bottom:12px">🌸</div>
    <div style="font-size:.9rem;color:#9CA3AF;font-family:'Segoe UI',sans-serif">Chargement…</div>
  </div>
</div>
<div class="hdr">
  <span class="hdr-logo">🌸 Les Glycines</span>
  <span id="sync-dot" class="sync-dot" title="Synchronisé"></span>
</div>

<main>
  <!-- PROFIL -->
  <div class="view active" id="v-profil"></div>

  <!-- FLEURS -->
  <div class="view" id="v-fleurs">
    <div class="sticky-top">
      <div class="sbox"><span class="sico">🔍</span>
        <input class="sinput" id="fleurs-q" type="search" placeholder="Rechercher une fleur…" oninput="renderFleurs()">
      </div>
      <div class="fchips" id="fleurs-chips"></div>
      <div class="fsort"><button class="fchip fsort-btn" id="fleurs-sort" onclick="toggleFleursSort()"></button></div>
    </div>
    <div class="scroll-area">
      <div id="fleurs-list"></div>
    </div>
  </div>

  <!-- ÉQUIPE -->
  <div class="view" id="v-equipe">
    <div class="sticky-top">
      <div class="sbox"><span class="sico">🔍</span>
        <input class="sinput" id="eq-q" type="search" placeholder="Rechercher une joueuse…" oninput="renderEquipe()">
      </div>
    </div>
    <div class="scroll-area" id="eq-list"></div>
  </div>

  <!-- GÉRER -->
  <div class="view" id="v-gerer">
    <div class="sticky-top">
      <div class="mg-hdr"><span class="mg-title">Joueuses</span>
        <button class="add-btn" onclick="openSheet('player')">+ Ajouter</button></div>
      <div class="sbox"><span class="sico">🔍</span>
        <input class="sinput" id="mgp-q" type="search" placeholder="Filtrer les joueuses…" oninput="renderManage()"></div>
    </div>
    <div class="scroll-area">
      <div id="mg-players"></div>
      <div style="border-top:1px solid #E8ECF2;margin:18px 0 14px"></div>
      <div class="mg-sec">
        <div class="mg-hdr"><span class="mg-title">Fleurs</span>
          <button class="add-btn" onclick="openSheet('flower')">+ Ajouter</button></div>
        <div class="sbox" style="margin-bottom:8px"><span class="sico">🔍</span>
          <input class="sinput" id="mgf-q" type="search" placeholder="Filtrer les fleurs…" oninput="renderManage()"></div>
        <div id="mg-flowers"></div>
      </div>
      <div style="border-top:1px solid #E8ECF2;margin:18px 0 14px"></div>
      <div class="mg-sec">
        <div class="mg-hdr"><span class="mg-title">Données</span></div>
        <button class="btn-outline" onclick="doImport()">📂 Importer un fichier JSON</button>
        <button class="btn-outline" style="color:#B91C1C;border-color:#FECACA" onclick="resetData()">↺ Réinitialiser vers les données initiales</button>
      </div>
    </div>
  </div>
</main>

<nav class="bnav">
  <button class="nbtn active" data-tab="profil" onclick="goTab('profil')">
    <span class="nico">👤</span><span class="nlbl">Profil</span>
  </button>
  <button class="nbtn" data-tab="fleurs" onclick="goTab('fleurs')">
    <span class="nico">🌸</span><span class="nlbl">Fleurs</span>
  </button>
  <button class="nbtn" data-tab="equipe" onclick="goTab('equipe')">
    <span class="nico">👥</span><span class="nlbl">Équipe</span>
  </button>
  <button class="nbtn" data-tab="gerer" onclick="goTab('gerer')">
    <span class="nico">⚙️</span><span class="nlbl">Gérer</span>
  </button>
</nav>

<button class="fab hidden" id="fab" onclick="onFab()"><span>＋</span> <span id="fab-lbl">Nouvelle fleur</span></button>

<div class="shbg" id="shbg" onclick="closeSheet()"></div>
<div class="sheet" id="sheet"><div class="sh-handle"></div><div id="sh-body"></div></div>

<div class="dview" id="dv-flower">
  <div class="dhdr">
    <button class="back-btn" onclick="closeDetail('flower')">‹ Retour</button>
    <span class="dtitle" id="fd-title"></span>
    <button class="del-btn" onclick="askDel('flower')">🗑</button>
  </div>
  <div class="dbody" id="fd-body"></div>
</div>

<div class="dview" id="dv-player">
  <div class="dhdr">
    <button class="back-btn" onclick="closeDetail('player')">‹ Retour</button>
    <span class="dtitle" id="pd-title"></span>
    <button class="del-btn" onclick="askDel('player')">🗑</button>
  </div>
  <div class="dbody" id="pd-body"></div>
</div>

<div class="cfbg" id="cfbg">
  <div class="cfbox">
    <div class="cftitle" id="cf-title"></div>
    <div class="cfmsg" id="cf-msg"></div>
    <div class="cfbtns">
      <button class="btn btn-ghost" onclick="closeCf()">Annuler</button>
      <button class="btn btn-red" id="cf-ok">Supprimer</button>
    </div>
  </div>
</div>
"""

# ── JS ────────────────────────────────────────────────────────────────────────
JS = r"""
const INITIAL = %%DATA%%;
const SK = 'rtcf_v3', ME_KEY = 'rtcf_me';
const SUPA_URL = 'https://qbuxhzvnbnjuibbusomn.supabase.co';
const SUPA_KEY = 'sb_publishable_0QYFdSbpvQQPBmlINtn2fw_Qeo4kDR4';
let lastUpdAt = null;
const ADMIN_PINS = {'p1':'0909'}; // ID → PIN (complété au chargement)
const ADMIN_NAME_PINS = {'CourtofBloom':'1910','Selkyy1':'1975'};
function resolveAdminNames(){
  D.players.forEach(p=>{
    const key=Object.keys(ADMIN_NAME_PINS).find(k=>p.name.replace(/\s/g,'').toLowerCase().includes(k.toLowerCase())||p.short.toLowerCase()===k.toLowerCase());
    if(key&&!(p.id in ADMIN_PINS)) ADMIN_PINS[p.id]=ADMIN_NAME_PINS[key];
  });
}
let pinUnlocked = false;
let D, myId=null, curTab='profil', curFId=null, curPId=null;
let fleursF='all', fleursSort='name', moiF='all', moiQ='';

// ── Supabase ──────────────────────────────────────────────────────────────────
function setSyncDot(status){
  const el=document.getElementById('sync-dot'); if(!el) return;
  const colors={loading:'#F59E0B',saving:'#F59E0B',ok:'#10B981',error:'#EF4444',offline:'#9CA3AF'};
  const labels={loading:'Chargement…',saving:'Synchronisation…',ok:'Synchronisé ✓',error:'Erreur de synchronisation',offline:'Mode hors ligne'};
  el.style.background=colors[status]||'#9CA3AF';
  el.title=labels[status]||'';
}
async function supaFetch(){
  const r=await fetch(`${SUPA_URL}/rest/v1/rtcf_data?id=eq.1`,
    {headers:{'apikey':SUPA_KEY,'Authorization':'Bearer '+SUPA_KEY}});
  const rows=await r.json();
  return rows&&rows[0]?rows[0]:null;
}
async function supaSave(data){
  await fetch(`${SUPA_URL}/rest/v1/rtcf_data`,{
    method:'POST',
    headers:{'apikey':SUPA_KEY,'Authorization':'Bearer '+SUPA_KEY,
      'Content-Type':'application/json','Prefer':'resolution=merge-duplicates'},
    body:JSON.stringify({id:1,payload:data,updated_at:new Date().toISOString()})
  });
}
async function checkSync(){
  try{
    const r=await fetch(`${SUPA_URL}/rest/v1/rtcf_data?id=eq.1&select=updated_at`,
      {headers:{'apikey':SUPA_KEY,'Authorization':'Bearer '+SUPA_KEY}});
    const rows=await r.json();
    if(rows&&rows[0]&&rows[0].updated_at!==lastUpdAt){
      const row=await supaFetch();
      if(row&&row.payload){
        D=row.payload; lastUpdAt=row.updated_at;
        localStorage.setItem(SK,JSON.stringify(D));
        refreshAll();
        showToast('🔄 Données mises à jour');
        logEvent('sync_update');
      }
    }
  }catch(e){}
}

// ── IT Logging ────────────────────────────────────────────────────────────────
function logEvent(event,detail){
  try{
    const pname=myId&&D?((D.players||[]).find(x=>x.id===myId)||{}).name||null:null;
    fetch(`${SUPA_URL}/rest/v1/rtcf_logs`,{
      method:'POST',
      headers:{'apikey':SUPA_KEY,'Authorization':'Bearer '+SUPA_KEY,'Content-Type':'application/json'},
      body:JSON.stringify({
        event,
        player_id:myId||null,
        player_name:pname,
        ua:navigator.userAgent,
        screen:screen.width+'x'+screen.height,
        lang:navigator.language,
        detail:detail||null
      })
    }).catch(()=>{});
  }catch(e){}
}

// ── Data ─────────────────────────────────────────────────────────────────────
async function initData(){
  setSyncDot('loading');
  try{
    const row=await supaFetch();
    if(row&&row.payload){
      D=row.payload; lastUpdAt=row.updated_at;
      localStorage.setItem(SK,JSON.stringify(D));
      setSyncDot('ok');
      logEvent('sync_ok');
    } else {
      // Première utilisation : on pousse les données initiales vers Supabase
      const local=localStorage.getItem(SK);
      D=local?JSON.parse(local):fromInit();
      await supaSave(D);
      const row2=await supaFetch();
      if(row2) lastUpdAt=row2.updated_at;
      setSyncDot('ok');
      logEvent('sync_ok','first_init');
    }
  } catch(e){
    // Fallback hors ligne
    const local=localStorage.getItem(SK);
    D=local?JSON.parse(local):fromInit();
    setSyncDot('offline');
    logEvent('sync_offline');
  }
  myId=localStorage.getItem(ME_KEY);
  if(myId&&!D.players.find(p=>p.id===myId)) myId=null;
}
function fromInit(){
  return{version:3,
    players:INITIAL.players.map((nm,i)=>({id:'p'+i,name:nm,short:INITIAL.shorts[i]})),
    flowers:INITIAL.flowers.map((f,i)=>({id:'f'+i,name:f.n,rarity:null,points:null,owned:f.o.map(pi=>'p'+pi)}))};
}
function save(){
  localStorage.setItem(SK,JSON.stringify(D));
  setSyncDot('saving');
  supaSave(D)
    .then(async()=>{
      // Récupère le vrai updated_at pour éviter de déclencher checkSync sur notre propre save
      const r=await fetch(`${SUPA_URL}/rest/v1/rtcf_data?id=eq.1&select=updated_at`,
        {headers:{'apikey':SUPA_KEY,'Authorization':'Bearer '+SUPA_KEY}});
      const rows=await r.json();
      if(rows&&rows[0]) lastUpdAt=rows[0].updated_at;
      setSyncDot('ok');
    })
    .catch(()=>{setSyncDot('error');logEvent('sync_error');});
}
function isAdmin(){ return myId&&myId in ADMIN_PINS; }
function updateNav(){
  const btn=document.querySelector('.nbtn[data-tab="gerer"]');
  if(btn) btn.style.display=isAdmin()?'':'none';
}
function setMe(id){
  myId=id; pinUnlocked=false;
  localStorage.setItem(ME_KEY,id);
  logEvent('profile_select');
  updateFab(); updateNav(); refreshAll();
}
function clearMe(){
  logEvent('profile_clear');
  myId=null; pinUnlocked=false;
  localStorage.removeItem(ME_KEY);
  updateFab(); updateNav(); refreshAll();
}
function updateFab(){
  const fab=document.getElementById('fab');
  const lbl=document.getElementById('fab-lbl');
  if(curTab==='fleurs'){fab.classList.remove('hidden');lbl.textContent='Ajouter au catalogue';}
  else fab.classList.add('hidden');
}

// ── CRUD ─────────────────────────────────────────────────────────────────────
function addPlayer(nm){
  nm=nm.trim(); if(!nm) return;
  const p=nm.includes('/')?nm.split('/').pop().trim():nm;
  D.players.push({id:'p_'+Date.now(),name:nm,short:p.split(' ')[0]});
  save(); refreshAll();
}
function removePlayer(id){
  D.players=D.players.filter(p=>p.id!==id);
  D.flowers.forEach(f=>{f.owned=f.owned.filter(pid=>pid!==id);});
  if(myId===id){myId=null;localStorage.removeItem(ME_KEY);}
  save(); refreshAll();
}
function addFlower(nm,rarity,points){
  nm=nm.trim(); if(!nm) return;
  D.flowers.push({id:'f_'+Date.now(),name:nm,rarity:rarity||null,points:points!=null?points:null,owned:[]});
  D.flowers.sort((a,b)=>a.name.localeCompare(b.name,'fr',{sensitivity:'base'}));
  save(); refreshAll();
}
function editFlower(id,nm,rarity,points){
  const f=D.flowers.find(x=>x.id===id); if(!f) return;
  if(nm.trim()) f.name=nm.trim();
  f.rarity=rarity||null;
  f.points=points!=null?points:null;
  D.flowers.sort((a,b)=>a.name.localeCompare(b.name,'fr',{sensitivity:'base'}));
  save(); renderFlower(id); refreshAll();
}
function removeFlower(id){
  D.flowers=D.flowers.filter(f=>f.id!==id);
  save(); refreshAll();
}
function toggleOwn(fid,pid){
  const f=D.flowers.find(x=>x.id===fid); if(!f) return;
  const i=f.owned.indexOf(pid);
  if(i>=0) f.owned.splice(i,1); else f.owned.push(pid);
  save();
}
function resetData(){
  confirm2('Réinitialiser les données ?',
    'Toutes les modifications seront perdues et remplacées par les données initiales.',
    ()=>{D=fromInit();save();refreshAll();closeCf();showToast('Données réinitialisées');});
}

// ── Utils ────────────────────────────────────────────────────────────────────
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');}
function pseudo(n){return n.includes('/')?n.split('/')[0].trim():n;}
function pOwned(pid){return D.flowers.filter(f=>f.owned.includes(pid)).length;}
function pPct(pid){return D.flowers.length?pOwned(pid)/D.flowers.length*100:0;}
function fPct(f){return D.players.length?f.owned.length/D.players.length*100:0;}
function bcls(f){const m={N:'b-N',R:'b-R',SR:'b-SR',SSR:'b-SSR',UR:'b-UR'};return m[f.rarity]||'b-0';}
function rarityLabel(r){return r||'—'}
function ptsLabel(p){return p!=null?p+'pts':''}

// ── Toast ────────────────────────────────────────────────────────────────────
function showToast(msg){
  let t=document.getElementById('_toast');
  if(!t){t=document.createElement('div');t.id='_toast';t.className='toast';document.body.appendChild(t);}
  t.textContent=msg; t.classList.remove('show');
  clearTimeout(t._t);
  requestAnimationFrame(()=>requestAnimationFrame(()=>t.classList.add('show')));
  t._t=setTimeout(()=>t.classList.remove('show'),2800);
}


// ── PROFIL TAB ───────────────────────────────────────────────────────────────
function renderProfil(){
  const el=document.getElementById('v-profil');
  if(!myId||!D.players.find(p=>p.id===myId)){renderOnboarding(el);return;}
  const me=D.players.find(p=>p.id===myId);
  const nF=D.flowers.length,nP=D.players.length;
  const owned=D.flowers.filter(f=>f.owned.includes(myId));
  const missing=D.flowers.filter(f=>!f.owned.includes(myId));
  const pct=nF?owned.length/nF*100:0;
  let shown=moiF==='owned'?owned:moiF==='missing'?missing:D.flowers;
  if(moiQ){const q=norm(moiQ);shown=shown.filter(f=>norm(f.name).includes(q));}
  const initials=pseudo(me.name).split(' ').map(w=>w[0]||'').join('').slice(0,2).toUpperCase()||me.short.slice(0,2).toUpperCase();
  const myLabel=me.label===undefined?me.short:me.label;

  el.innerHTML=`
    <div class="sticky-top">
      <div class="profbar">
        <div class="profavo">${initials}</div>
        <div class="profinfo">
          <div class="profname">${esc(pseudo(me.name))}</div>
          ${myLabel?`<div class="proffull" onclick="openEditLabel()" title="Modifier prénom">${esc(myLabel)} <span class="edit-lbl">modifier</span></div>`:'<div class="proffull" onclick="openEditLabel()"><span class="edit-lbl">+ Ajouter un prénom</span></div>'}
        </div>
        <button class="chg-btn" onclick="clearMe()">Changer</button>
      </div>
      <div class="progcard">
        <div class="prog-nums">
          <span class="prog-big">${owned.length}</span>
          <span class="prog-total">/ ${nF} fleurs</span>
          <span class="prog-pct">${pct.toFixed(1)}%</span>
        </div>
        <div class="prog-bar-lg"><div class="prog-fill-lg" style="width:${pct.toFixed(1)}%"></div></div>
        <div class="prog-sub">${missing.length} fleur${missing.length!==1?'s':''} manquante${missing.length!==1?'s':''}</div>
      </div>
      <div class="fchips">
        <button class="fchip${moiF==='all'?' active':''}" onclick="setMoiF('all')">Toutes</button>
        <button class="fchip${moiF==='owned'?' active':''}" onclick="setMoiF('owned')">Ma collection (${owned.length})</button>
        <button class="fchip${moiF==='missing'?' active':''}" onclick="setMoiF('missing')">Manquantes (${missing.length})</button>
      </div>
      <div class="sbox" style="margin-top:8px"><span class="sico">🔍</span>
        <input class="sinput" id="moi-q" type="search" placeholder="Rechercher…" value="${esc(moiQ)}" oninput="moiQ=this.value;renderProfil()"></div>
    </div>
    <div class="scroll-area">
    ${shown.length?shown.map(f=>{
      const has=f.owned.includes(myId);
      return `<div class="litem" onclick="openFlower('${f.id}')">
        <div class="litem-ico" style="${has?'background:#D1FAE5;color:#047857':''}">${has?'✓':'🌸'}</div>
        <div class="litem-body"><div class="litem-name">${esc(f.name)}</div></div>
        <div class="litem-right">
          ${f.points!=null?`<span class="pts">${f.points}pts</span>`:'<span class="pts" style="opacity:0;pointer-events:none">—pts</span>'}
          ${f.rarity?`<span class="badge badge-r ${bcls(f)}">${f.rarity}</span>`:'<span class="badge badge-r b-0" style="opacity:0;pointer-events:none">—</span>'}
          <span class="chevron">›</span>
        </div>
      </div>`;
    }).join(''):'<div class="empty">Aucune fleur trouvée</div>'}
    </div>`;
}

function renderOnboarding(el){
  el.innerHTML=`
    <div class="scroll-area">
      <div style="text-align:center;padding:32px 0 24px">
        <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#C2185B,#6D28D9);color:#fff;font-size:1.4rem;display:flex;align-items:center;justify-content:center;margin:0 auto 14px">🌸</div>
        <div style="font-size:1rem;font-weight:700;margin-bottom:6px;color:#111827">Choisir mon profil</div>
        <div style="font-size:.8rem;color:#9CA3AF;max-width:240px;margin:0 auto 24px;line-height:1.5">
          Sélectionne ton compte pour suivre ta collection personnelle
        </div>
      </div>
      <div class="ppgrid">
        ${D.players.map(p=>{const lbl=p.label===undefined?p.short:p.label;return`
          <button class="ppbtn" onclick="setMe('${p.id}')">
            <div class="ppbtn-ico">👤</div>
            <div class="ppbtn-name">${esc(pseudo(p.name))}</div>
            ${lbl?`<div class="ppbtn-full">${esc(lbl)}</div>`:''}
          </button>`}).join('')}
      </div>
    </div>`;
}

function setMoiF(f){moiF=f;renderProfil();}
function openEditLabel(){
  const me=D.players.find(p=>p.id===myId); if(!me) return;
  const cur=me.label===undefined?me.short:(me.label||'');
  document.getElementById('sh-body').innerHTML=`
    <div class="sh-title">Modifier ton prénom affiché</div>
    <p style="font-size:.8rem;color:#9CA3AF;margin-bottom:12px">Laisse vide pour le masquer</p>
    <input class="sh-input" id="sh-label-inp" type="text" maxlength="40"
      placeholder="Prénom (facultatif)" value="${esc(cur)}">
    <div class="sh-btns">
      <button class="btn btn-ghost" onclick="closeSheet()">Annuler</button>
      <button class="btn btn-pk" onclick="saveMyLabel()">Enregistrer</button>
    </div>`;
  document.getElementById('shbg').classList.add('open');
  document.getElementById('sheet').classList.add('open');
  setTimeout(()=>{const el=document.getElementById('sh-label-inp');if(el)el.focus();},340);
}
function saveMyLabel(){
  const me=D.players.find(p=>p.id===myId); if(!me) return;
  const val=(document.getElementById('sh-label-inp')?.value||'').trim();
  me.label=val||null;
  save(); closeSheet(); renderProfil(); showToast('✓ Nom mis à jour');
}

// ── PICKER ────────────────────────────────────────────────────────────────────
function openPicker(){
  document.getElementById('sh-body').innerHTML=`
    <div class="sh-title">🌸 Nouvelle fleur débloquée</div>
    <div class="sbox" style="margin-bottom:10px"><span class="sico">🔍</span>
      <input class="picker-inp" id="picker-q" type="text" placeholder="Rechercher parmi les fleurs manquantes…" oninput="renderPicker()"></div>
    <div class="picker-list" id="picker-list"></div>`;
  document.getElementById('shbg').classList.add('open');
  document.getElementById('sheet').classList.add('open');
  renderPicker();
  setTimeout(()=>{const el=document.getElementById('picker-q');if(el)el.focus();},340);
}
function renderPicker(){
  const raw=(document.getElementById('picker-q')||{}).value||'';
  const q=norm(raw);
  const notOwned=D.flowers.filter(f=>!f.owned.includes(myId));
  const filtered=q?notOwned.filter(f=>norm(f.name).includes(q)):notOwned;
  const exactMatch=D.flowers.some(f=>norm(f.name)===norm(raw.trim()));
  const nP=D.players.length;
  const el=document.getElementById('picker-list');if(!el) return;
  let html='';
  if(filtered.length){
    html=filtered.slice(0,60).map(f=>`
      <div class="picker-item">
        <span class="picker-name">${esc(f.name)}</span>
        <span class="badge b-0" style="flex-shrink:0;margin-right:4px">${f.owned.length}/${nP}</span>
        <button class="picker-add" data-fid="${f.id}" onclick="pickerAdd(this)">+ J'ai !</button>
      </div>`).join('');
    if(filtered.length>60) html+=`<div class="picker-empty">+${filtered.length-60} autres — affine la recherche</div>`;
  } else if(q){
    html='<div class="picker-empty">Aucune fleur manquante correspondante</div>';
  } else {
    html='<div class="picker-empty">🎉 Tu as déjà toutes les fleurs répertoriées !</div>';
  }
  if(raw.trim()&&!exactMatch){
    html+=`<div class="picker-new" onclick="pickerCreate()">
      ✨ <strong>Créer</strong> « ${esc(raw.trim())} » et l'ajouter à ma collection</div>`;
  }
  el.innerHTML=html;
}
function pickerAdd(btn){
  const fid=btn.dataset.fid,f=D.flowers.find(x=>x.id===fid);
  if(!f||!myId) return;
  if(!f.owned.includes(myId)){f.owned.push(myId);save();}
  closeSheet(); showToast('✓ '+f.name+' ajoutée !');
  renderProfil();refreshAll();
}
function pickerCreate(){
  const raw=(document.getElementById('picker-q')||{}).value||'';
  const name=raw.trim();if(!name||!myId) return;
  const id='f_'+Date.now();
  D.flowers.push({id,name,owned:[myId]});
  D.flowers.sort((a,b)=>a.name.localeCompare(b.name,'fr',{sensitivity:'base'}));
  save();closeSheet();showToast('✨ "'+name+'" créée et ajoutée !');
  refreshAll();
}

// ── FLEURS TAB ────────────────────────────────────────────────────────────────
function buildFleursChips(){
  const chips=[{k:'all',l:'Toutes'},{k:'N',l:'N'},{k:'R',l:'R'},{k:'SR',l:'SR'},{k:'SSR',l:'SSR'},{k:'UR',l:'UR'}];
  document.getElementById('fleurs-chips').innerHTML=chips.map(c=>
    `<button class="fchip${fleursF===c.k?' active':''}" onclick="setFleursF('${c.k}')">${c.l}</button>`).join('');
  updateFleursSortBtn();
}
function setFleursF(k){fleursF=k;buildFleursChips();renderFleurs();}
function updateFleursSortBtn(){
  const b=document.getElementById('fleurs-sort'); if(!b) return;
  b.textContent=fleursSort==='points'?'Tri : Points ↓':'Tri : A→Z';
  b.classList.toggle('active',fleursSort==='points');
}
function toggleFleursSort(){fleursSort=fleursSort==='points'?'name':'points';updateFleursSortBtn();renderFleurs();}
function renderFleurs(){
  const q=norm(document.getElementById('fleurs-q').value);
  const nP=D.players.length;
  const fl=D.flowers.filter(f=>{
    if(q&&!norm(f.name).includes(q)) return false;
    if(fleursF!=='all'&&f.rarity!==fleursF) return false;
    return true;
  });
  if(fleursSort==='points') fl.sort((a,b)=>(b.points??-1)-(a.points??-1)||a.name.localeCompare(b.name,'fr',{sensitivity:'base'}));
  else fl.sort((a,b)=>a.name.localeCompare(b.name,'fr',{sensitivity:'base'}));
  const el=document.getElementById('fleurs-list');
  if(!fl.length){el.innerHTML='<div class="empty">Aucune fleur trouvée</div>';return;}
  el.innerHTML=fl.map(f=>{
    const p=fPct(f),isMine=myId&&f.owned.includes(myId);
    return `<div class="litem" onclick="openFlower('${f.id}')">
      <div class="litem-ico" style="${isMine?'background:#D1FAE5;color:#047857':''}">🌸</div>
      <div class="litem-body">
        <div class="litem-name">${esc(f.name)}</div>
        <div class="bar"><div class="bar-fill bpk" style="width:${p.toFixed(1)}%"></div></div>
      </div>
      <div class="litem-right">
        ${f.points!=null?`<span class="pts">${f.points}pts</span>`:'<span class="pts" style="opacity:0;pointer-events:none">—pts</span>'}
        ${f.rarity?`<span class="badge badge-r ${bcls(f)}">${f.rarity}</span>`:'<span class="badge badge-r b-0" style="opacity:0;pointer-events:none">—</span>'}
        ${myId?`<button class="qtoggle ${isMine?'on':'off'}" onclick="event.stopPropagation();toggleMyFlower('${f.id}')">${isMine?'✓ J\'ai':'+ Ajouter'}</button>`:''}
      </div>
    </div>`;
  }).join('');
}
function toggleMyFlower(fid){
  if(!myId) return;
  const f=D.flowers.find(x=>x.id===fid); if(!f) return;
  const had=f.owned.includes(myId);
  toggleOwn(fid,myId);
  showToast(had?'Retirée de ta collection':'✓ '+f.name+' ajoutée !');
  renderFleurs(); renderProfil();
}

// ── ÉQUIPE TAB ────────────────────────────────────────────────────────────────
function renderEquipe(){
  const q=norm(document.getElementById('eq-q').value);
  const nF=D.flowers.length;
  const pl=[...D.players]
    .filter(p=>!q||norm(p.name).includes(q)||norm(p.short).includes(q))
    .map(p=>({...p,c:pOwned(p.id),pct:pPct(p.id)}))
    .sort((a,b)=>b.c-a.c);
  const el=document.getElementById('eq-list');
  if(!pl.length){el.innerHTML='<div class="empty">Aucune joueuse trouvée</div>';return;}
  el.innerHTML=pl.map((p,i)=>`
    <div class="litem" onclick="openPlayer('${p.id}')">
      <div class="litem-ico" style="${p.id===myId?'background:#FCE4EC;color:#880E4F':''}">${i===0?'🥇':i===1?'🥈':i===2?'🥉':'👤'}</div>
      <div class="litem-body">
        <div class="litem-name">${esc(pseudo(p.name))}${p.id===myId?' <span style="font-size:.68rem;color:#C2185B;font-weight:600">(moi)</span>':''}</div>
        ${(p.label===undefined?p.short:p.label)?`<div class="litem-sub">${esc(p.label===undefined?p.short:p.label)}</div>`:''}
        <div class="bar"><div class="bar-fill bgr" style="width:${p.pct.toFixed(1)}%"></div></div>
      </div>
      <div class="litem-right">
        <span class="badge b-pk">${p.c}/${nF}</span>
        <span class="chevron">›</span>
      </div>
    </div>`).join('');
}

// ── GÉRER TAB ─────────────────────────────────────────────────────────────────
function renderManage(){
  const qp=norm(document.getElementById('mgp-q').value);
  const qf=norm(document.getElementById('mgf-q').value);
  const pls=D.players.filter(p=>!qp||norm(p.name).includes(qp)||norm(p.short).includes(qp));
  const fls=D.flowers.filter(f=>!qf||norm(f.name).includes(qf));
  document.getElementById('mg-players').innerHTML=pls.map(p=>
    `<div class="mgitem"><span class="mgname">${esc(p.name)}</span>
      ${p.id===myId?'<span style="font-size:.75rem;color:#9CA3AF">(toi)</span>':`<button class="del" data-id="${p.id}" onclick="askDelPlayer(this)">Supprimer</button>`}
    </div>`).join('')||'<div class="empty" style="padding:8px 0">Aucune joueuse</div>';
  document.getElementById('mg-flowers').innerHTML=fls.map(f=>
    `<div class="mgitem"><span class="mgname">${esc(f.name)}</span>
      <button class="del" data-id="${f.id}" onclick="askDelFlower(this)">Supprimer</button>
    </div>`).join('')||'<div class="empty" style="padding:8px 0">Aucune fleur</div>';
}

function refreshAll(){renderProfil();renderFleurs();renderEquipe();renderManage();}

// ── DETAIL VIEWS ──────────────────────────────────────────────────────────────
function openFlower(id){
  curFId=id;renderFlower(id);
  document.getElementById('dv-flower').classList.add('open');
}
function renderFlower(id){
  const f=D.flowers.find(x=>x.id===id);if(!f) return;
  const nP=D.players.length,c=f.owned.length,p=fPct(f);
  const isMine=myId&&f.owned.includes(myId);
  document.getElementById('fd-title').textContent=f.name;
  document.getElementById('fd-body').innerHTML=`
    <div class="card" style="text-align:center;margin-bottom:14px">
      <div style="font-size:1.8rem;margin-bottom:8px">🌸</div>
      <div style="font-weight:700;font-size:.95rem;margin-bottom:6px">${esc(f.name)}</div>
      <div style="display:flex;align-items:center;justify-content:center;gap:7px;margin-bottom:8px">
        <span class="badge ${bcls(f)}">${rarityLabel(f.rarity)}</span>
        ${f.points!=null?`<span class="pts">${f.points} pts</span>`:''}
      </div>
      <div style="font-size:.75rem;color:#9CA3AF">${c} joueuse${c!==1?'s':''} sur ${nP} — ${p.toFixed(1)}%</div>
      <div class="bar" style="margin-top:10px"><div class="bar-fill bpk" style="width:${p.toFixed(1)}%"></div></div>
      ${isMine?'<div style="margin-top:10px;font-size:.78rem;color:#047857;font-weight:600">✓ Tu possèdes cette fleur</div>':''}
      ${isAdmin()&&pinUnlocked?`<button class="btn btn-ghost" style="margin-top:12px;font-size:.78rem" onclick="openEditFlower('${id}')">✏️ Modifier</button>`:''}
    </div>
    <div class="slbl">Possédée par</div>
    <div style="display:flex;flex-wrap:wrap;gap:5px">
      ${D.players.filter(pl=>f.owned.includes(pl.id)).map(pl=>
        `<span class="badge b-gr">${esc(pl.short)}</span>`).join('')||'<span style="font-size:.8rem;color:#9CA3AF">Personne pour l\'instant</span>'}
    </div>`;
}
function openPlayer(id){
  curPId=id;renderPlayerDetail(id);
  document.getElementById('dv-player').classList.add('open');
}
function renderPlayerDetail(id){
  const p=D.players.find(x=>x.id===id);if(!p) return;
  const nF=D.flowers.length,c=pOwned(id),pct=pPct(id);
  const initials=pseudo(p.name).split(' ').map(w=>w[0]||'').join('').slice(0,2).toUpperCase()||p.short.slice(0,2).toUpperCase();
  const pLabel=p.label===undefined?p.short:p.label;
  document.getElementById('pd-title').textContent=pseudo(p.name)+(id===myId?' (moi)':'');
  document.getElementById('pd-body').innerHTML=`
    <div class="card" style="text-align:center;margin-bottom:14px">
      <div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#C2185B,#6D28D9);color:#fff;font-size:1.1rem;font-weight:700;display:flex;align-items:center;justify-content:center;margin:0 auto 10px">${initials}</div>
      <div style="font-weight:700;font-size:.95rem">${esc(pseudo(p.name))}</div>
      ${pLabel?`<div style="font-size:.75rem;color:#9CA3AF;margin-top:2px">${esc(pLabel)}</div>`:''}
      <div style="display:flex;align-items:baseline;justify-content:center;gap:6px;margin-top:12px">
        <span style="font-size:1.6rem;font-weight:800">${c}</span>
        <span style="font-size:.8rem;color:#9CA3AF">/ ${nF} fleurs</span>
        <span style="font-size:.85rem;font-weight:600;color:#C2185B">${pct.toFixed(1)}%</span>
      </div>
      <div class="bar" style="margin-top:8px"><div class="bar-fill bgr" style="width:${pct.toFixed(1)}%"></div></div>
    </div>
    <div class="slbl">Collection</div>
    ${D.flowers.filter(f=>f.owned.includes(id)).map(f=>`
      <div class="litem" onclick="openFlower('${f.id}')">
        <div class="litem-ico" style="background:#D1FAE5;color:#047857">✓</div>
        <div class="litem-body"><div class="litem-name">${esc(f.name)}</div></div>
        <div class="litem-right">
          ${f.points!=null?`<span class="pts">${f.points}pts</span>`:'<span class="pts" style="opacity:0;pointer-events:none">—pts</span>'}
          ${f.rarity?`<span class="badge badge-r ${bcls(f)}">${f.rarity}</span>`:'<span class="badge badge-r b-0" style="opacity:0;pointer-events:none">—</span>'}
          <span class="chevron">›</span>
        </div>
      </div>`).join('')||'<div class="empty">Aucune fleur pour l\'instant</div>'}`;
}
function closeDetail(t){document.getElementById('dv-'+t).classList.remove('open');}

// ── TABS ──────────────────────────────────────────────────────────────────────
function goTab(t){
  if(t==='gerer'){
    if(!isAdmin()) return;
    if(!pinUnlocked){ openPinSheet(); return; }
  }
  curTab=t;
  document.querySelectorAll('.view').forEach(v=>v.classList.toggle('active',v.id==='v-'+t));
  document.querySelectorAll('.nbtn').forEach(b=>b.classList.toggle('active',b.dataset.tab===t));
  updateFab();
}
function openPinSheet(){
  document.getElementById('sh-body').innerHTML=`
    <div class="sh-title">🔒 Accès administrateur</div>
    <p style="font-size:.82rem;color:#9CA3AF;margin-bottom:14px">Entrez le code PIN pour accéder à la gestion</p>
    <input class="sh-input" id="pin-inp" type="password" inputmode="numeric" maxlength="4"
      placeholder="Code PIN" onkeydown="if(event.key==='Enter')submitPin()">
    <div id="pin-err" style="color:#B91C1C;font-size:.78rem;margin-bottom:10px;display:none">Code incorrect ❌</div>
    <div class="sh-btns">
      <button class="btn btn-ghost" onclick="closeSheet()">Annuler</button>
      <button class="btn btn-pk" onclick="submitPin()">Confirmer</button>
    </div>`;
  document.getElementById('shbg').classList.add('open');
  document.getElementById('sheet').classList.add('open');
  setTimeout(()=>{const el=document.getElementById('pin-inp');if(el)el.focus();},340);
}
function submitPin(){
  const val=document.getElementById('pin-inp')?.value;
  if(val===ADMIN_PINS[myId]){
    pinUnlocked=true; closeSheet(); goTab('gerer');
  } else {
    const inp=document.getElementById('pin-inp');
    const err=document.getElementById('pin-err');
    if(inp){inp.value='';inp.style.borderColor='#B91C1C';}
    if(err) err.style.display='';
  }
}
function onFab(){
  if(curTab==='fleurs') openSheet('flower');
}

// ── SHEET ─────────────────────────────────────────────────────────────────────
const RARITIES=['N','R','SR','SSR','UR'];
const POINTS_VALS=[9,14,21,23,25,28,30];
let shMode=null,shRarity=null,shPoints=null;

function rselHTML(selId,vals,cur){
  const clearOn=(cur===null||cur===undefined)?'on':'';
  const clearBtn=`<button class="rsel-btn ${clearOn}" data-sel="${selId}" data-val="" onclick="shSel(this)">—</button>`;
  return clearBtn+vals.map(v=>`<button class="rsel-btn${cur===v?' on':''}" data-sel="${selId}" data-val="${v}" onclick="shSel(this)">${v}</button>`).join('');
}
function shSel(btn){
  const selId=btn.dataset.sel, raw=btn.dataset.val;
  const val=raw===''?null:(!isNaN(raw)?Number(raw):raw);
  if(selId==='rarity') shRarity=val; else shPoints=val;
  document.querySelectorAll(`.rsel-btn[data-sel="${selId}"]`).forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
}

function openSheet(mode,prefill){
  shMode=mode; shRarity=prefill?.rarity||null; shPoints=prefill?.points||null;
  const isF=mode==='flower';
  document.getElementById('sh-body').innerHTML= isF ? `
    <div class="sh-title">🌸 ${prefill?'Modifier la fleur':'Ajouter une fleur'}</div>
    <input class="sh-input" id="sh-inp" type="text" placeholder="Nom de la fleur…" value="${esc(prefill?.name||'')}"
      onkeydown="if(event.key==='Enter')submitSheet()">
    <div class="slbl" style="margin-top:4px">Rareté</div>
    <div class="rsel">${rselHTML('rarity',RARITIES,shRarity)}</div>
    <div class="slbl">Points</div>
    <div class="rsel">${rselHTML('points',POINTS_VALS,shPoints)}</div>
    <div class="sh-btns">
      <button class="btn btn-ghost" onclick="closeSheet()">Annuler</button>
      <button class="btn btn-pk" onclick="submitSheet()">Valider</button>
    </div>` : `
    <div class="sh-title">Ajouter une joueuse</div>
    <input class="sh-input" id="sh-inp" type="text" placeholder="Pseudo / Prénom  ex: TheaLrd / Théa"
      onkeydown="if(event.key==='Enter')submitSheet()">
    <div class="sh-btns">
      <button class="btn btn-ghost" onclick="closeSheet()">Annuler</button>
      <button class="btn btn-pk" onclick="submitSheet()">Ajouter</button>
    </div>`;
  document.getElementById('shbg').classList.add('open');
  document.getElementById('sheet').classList.add('open');
  setTimeout(()=>{const el=document.getElementById('sh-inp');if(el)el.focus();},340);
}
function closeSheet(){
  document.getElementById('shbg').classList.remove('open');
  document.getElementById('sheet').classList.remove('open');
}
function submitSheet(){
  const v=document.getElementById('sh-inp')?.value;
  if(shMode==='flower') addFlower(v,shRarity,shPoints);
  else if(shMode==='edit-flower') editFlower(shMode._id,v,shRarity,shPoints);
  else addPlayer(v);
  closeSheet();
}
function openEditFlower(id){
  const f=D.flowers.find(x=>x.id===id); if(!f) return;
  shMode={type:'edit-flower',_id:id};
  shRarity=f.rarity; shPoints=f.points;
  document.getElementById('sh-body').innerHTML=`
    <div class="sh-title">✏️ Modifier ${esc(f.name)}</div>
    <input class="sh-input" id="sh-inp" type="text" placeholder="Nom de la fleur…" value="${esc(f.name)}">
    <div class="slbl" style="margin-top:4px">Rareté</div>
    <div class="rsel">${rselHTML('rarity',RARITIES,shRarity)}</div>
    <div class="slbl">Points</div>
    <div class="rsel">${rselHTML('points',POINTS_VALS,shPoints)}</div>
    <div class="sh-btns">
      <button class="btn btn-ghost" onclick="closeSheet()">Annuler</button>
      <button class="btn btn-pk" onclick="saveFlowerEdit('${id}')">Enregistrer</button>
    </div>`;
  document.getElementById('shbg').classList.add('open');
  document.getElementById('sheet').classList.add('open');
  setTimeout(()=>{const el=document.getElementById('sh-inp');if(el)el.focus();},340);
}
function saveFlowerEdit(id){
  const nm=document.getElementById('sh-inp')?.value||'';
  editFlower(id,nm,shRarity,shPoints);
  closeSheet(); showToast('✓ Fleur mise à jour');
}

// ── CONFIRM ───────────────────────────────────────────────────────────────────
let cfCb=null;
function confirm2(t,m,cb){
  document.getElementById('cf-title').textContent=t;
  document.getElementById('cf-msg').textContent=m;
  cfCb=cb;document.getElementById('cfbg').classList.add('open');
}
function closeCf(){document.getElementById('cfbg').classList.remove('open');cfCb=null;}
document.getElementById('cf-ok').onclick=()=>{if(cfCb)cfCb();};
function askDel(type){
  if(type==='flower'&&curFId){const f=D.flowers.find(x=>x.id===curFId);if(f)askDelFlowerById(curFId,f.name);}
  else if(type==='player'&&curPId){const p=D.players.find(x=>x.id===curPId);if(p)askDelPlayerById(curPId,p.short);}
}
function askDelFlower(btn){const id=btn.dataset.id,f=D.flowers.find(x=>x.id===id);if(f)askDelFlowerById(id,f.name);}
function askDelPlayer(btn){const id=btn.dataset.id,p=D.players.find(x=>x.id===id);if(p)askDelPlayerById(id,p.short);}
function askDelFlowerById(id,name){
  confirm2('Supprimer cette fleur ?',
    '"'+name+'" sera supprimée définitivement.',
    ()=>{removeFlower(id);closeDetail('flower');closeCf();showToast('Fleur supprimée');});
}
function askDelPlayerById(id,name){
  if(id===myId){showToast('Tu ne peux pas supprimer ton propre profil.');return;}
  confirm2('Supprimer cette joueuse ?',
    '"'+name+'" et toute sa collection seront supprimées.',
    ()=>{removePlayer(id);closeDetail('player');closeCf();showToast('Joueuse supprimée');});
}

// ── IMPORT ────────────────────────────────────────────────────────────────────
function doImport(){
  const inp=document.createElement('input');inp.type='file';inp.accept='.json';
  inp.onchange=e=>{
    const file=e.target.files[0];if(!file) return;
    const r=new FileReader();
    r.onload=ev=>{
      try{
        const data=JSON.parse(ev.target.result);
        if(!data.players||!data.flowers) throw new Error('Format invalide');
        D=data;D.version=3;save();refreshAll();
        showToast('✓ Données importées avec succès');
      }catch(err){alert('Erreur : '+err.message);}
    };
    r.readAsText(file);
  };
  inp.click();
}

// ── INIT ──────────────────────────────────────────────────────────────────────
(async()=>{
  try{
    await initData();
    resolveAdminNames();
    logEvent('page_load');
  }catch(e){
    // Sécurité : si tout plante, on charge quand même depuis le cache local
    const local=localStorage.getItem(SK);
    D=local?JSON.parse(local):fromInit();
    setSyncDot('offline');
    logEvent('page_load','fallback_error');
  }finally{
    buildFleursChips();
    refreshAll();
    updateFab();
    updateNav();
    document.getElementById('loading').style.display='none';
  }
  setInterval(checkSync,30000);
})();
"""

html = (
    '<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0">\n'
    '<meta name="robots" content="noindex, nofollow">\n'
    '<meta name="theme-color" content="#C2185B">\n'
    '<title>Les Glycines</title>\n'
    '<style>' + CSS + '</style>\n'
    '</head>\n<body>\n'
    + BODY +
    '\n<script>\n'
    + JS.replace('%%DATA%%', INITIAL) +
    '\n</script>\n</body>\n</html>'
)

out = r'C:\Users\s9qer6\_Claude\RTCF\index.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"OK — {len(players)} joueuses, {len(flowers)} fleurs — {len(html)//1024}KB")
