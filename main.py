<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>범퍼 수정일지</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',-apple-system,sans-serif;background:#f4f5f7;min-height:100vh;-webkit-text-size-adjust:100%;}
.ah{background:#0f3460;padding:13px 16px 0;position:sticky;top:0;z-index:200;}
.at{font-size:16px;font-weight:700;color:#fff;}
.hr{display:flex;align-items:center;justify-content:space-between;margin-top:5px;}
.db{background:rgba(255,255,255,0.15);color:#fff;font-size:12px;font-weight:600;padding:4px 12px;border-radius:14px;}
.fb{background:#1a7f4b;color:#fff;font-size:12px;font-weight:700;padding:4px 12px;border-radius:14px;cursor:pointer;}
.tabs{display:flex;border-top:1px solid rgba(255,255,255,0.15);margin-top:8px;}
.tab{flex:1;text-align:center;padding:9px 0;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);cursor:pointer;border-bottom:2px solid transparent;-webkit-tap-highlight-color:transparent;}
.tab.active{color:#fff;border-bottom-color:#e84040;}

/* 공장선택 */
.ss{display:flex;flex-direction:column;align-items:center;padding:52px 24px 32px;min-height:calc(100vh - 56px);}
.fbtn{background:#fff;border:1.5px solid #e2e8f0;border-radius:16px;padding:18px 20px;cursor:pointer;margin-bottom:12px;width:100%;transition:all .13s;-webkit-tap-highlight-color:transparent;}
.fbtn:active{transform:scale(0.98);background:#f0f4ff;border-color:#0f3460;}
.fbtn-name{font-size:16px;font-weight:700;color:#1e293b;}
.fbtn-sub{font-size:12px;color:#94a3b8;margin-top:3px;}

/* 폼 */
.fs{display:none;flex-direction:column;padding-bottom:40px;}
.bb{display:flex;align-items:center;gap:6px;padding:10px 16px;background:#fff;border-bottom:1px solid #e8edf5;cursor:pointer;}
.ba{font-size:16px;color:#0f3460;font-weight:700;}
.bt{font-size:13px;font-weight:600;color:#0f3460;}
.scroll-body{flex:1;padding:10px 14px;display:flex;flex-direction:column;gap:8px;}
.card{background:#fff;border:1px solid #eaedf2;border-radius:16px;padding:13px 15px;}
.sl{font-size:10px;font-weight:700;color:#94a3b8;letter-spacing:.05em;margin-bottom:8px;display:flex;align-items:center;gap:6px;}
.sl-sub{font-size:10px;font-weight:400;color:#b0bac6;}
.sl-badge{font-size:9px;background:#f1f5f9;color:#64748b;padding:1px 6px;border-radius:6px;}
.bg{display:flex;gap:7px;}
.bs{flex:1;padding:10px 6px;text-align:center;font-size:13px;font-weight:700;border:1.5px solid #e2e8f0;border-radius:10px;background:#fff;color:#94a3b8;cursor:pointer;transition:all .12s;-webkit-tap-highlight-color:transparent;}
.bs.on{background:#0f3460;border-color:#0f3460;color:#fff;}
.act-row{display:flex;gap:8px;}
.act{flex:1;padding:13px;text-align:center;font-size:14px;font-weight:700;border:1.5px solid #e2e8f0;border-radius:10px;background:#fff;color:#64748b;cursor:pointer;transition:all .13s;-webkit-tap-highlight-color:transparent;}
.act.sel-fix{background:#1a7f4b;border-color:#1a7f4b;color:#fff;}
.act.sel-swp{background:#e84040;border-color:#e84040;color:#fff;}
select.inp,input.inp,textarea.inp{width:100%;padding:11px 13px;font-size:14px;border:1px solid #e2e8f0;border-radius:10px;background:#fff;color:#222;outline:none;font-family:inherit;-webkit-appearance:none;appearance:none;transition:border-color .12s;}
select.inp{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2394a3b8' d='M6 8L1 3h10z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 13px center;}
select:focus,input:focus,textarea:focus{border-color:#0f3460;box-shadow:0 0 0 3px rgba(15,52,96,.08);}
textarea.inp{resize:none;line-height:1.55;height:60px;}
input.cno-inp{width:100%;padding:11px 13px;font-size:16px;font-weight:700;font-family:'Courier New',monospace;letter-spacing:3px;border:1px solid #e2e8f0;border-radius:10px;background:#fff;color:#0f3460;outline:none;-webkit-appearance:none;text-align:center;}
input.cno-inp:focus{border-color:#0f3460;box-shadow:0 0 0 3px rgba(15,52,96,.08);}
.resp-row{display:flex;gap:7px;}
.rb{flex:1;padding:11px 4px;text-align:center;font-size:13px;font-weight:700;border:1.5px solid #e2e8f0;border-radius:10px;background:#fff;color:#94a3b8;cursor:pointer;transition:all .12s;-webkit-tap-highlight-color:transparent;}
.rb.on{background:#0f3460;border-color:#0f3460;color:#fff;}
.photo-zone{border:2px dashed #c7d2fe;border-radius:12px;padding:16px;background:#f8f9ff;display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;-webkit-tap-highlight-color:transparent;}
.photo-text{font-size:13px;font-weight:700;color:#4f46e5;}
.photo-sub{font-size:11px;color:#94a3b8;}
.photo-preview{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;}
.photo-thumb{width:64px;height:64px;border-radius:8px;object-fit:cover;border:1px solid #e2e8f0;}
.sub-btn{display:block;width:100%;padding:15px;background:#374151;border:none;border-radius:14px;color:#fff;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;margin-top:4px;-webkit-tap-highlight-color:transparent;}
.sub-btn:active{opacity:.88;}
.extra{margin-top:8px;display:none;}
.extra.show{display:block;}
.hint{font-size:11px;color:#94a3b8;margin-bottom:5px;}

/* 오늘 목록 탭 */
.list-screen{display:none;padding:12px 14px;flex-direction:column;gap:8px;}
.list-item{background:#fff;border:1px solid #eaedf2;border-radius:14px;padding:13px 15px;display:flex;align-items:flex-start;gap:10px;}
.li-num{width:28px;height:28px;border-radius:50%;background:#0f3460;color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;}
.li-body{flex:1;min-width:0;}
.li-top{display:flex;align-items:center;gap:6px;margin-bottom:4px;}
.li-tag{font-size:10px;font-weight:700;padding:2px 7px;border-radius:6px;}
.li-tag.fix{background:#e6f5ee;color:#1a7f4b;}
.li-tag.swp{background:#fef0ee;color:#e84040;}
.li-title{font-size:13px;font-weight:700;color:#1e293b;}
.li-sub{font-size:11px;color:#94a3b8;margin-top:2px;}
.li-time{font-size:10px;color:#b0bac6;margin-top:3px;}
.empty-state{display:flex;flex-direction:column;align-items:center;padding:60px 20px;color:#94a3b8;}
.empty-icon{font-size:40px;margin-bottom:12px;}
.empty-text{font-size:14px;font-weight:600;margin-bottom:4px;}
.empty-sub{font-size:12px;}

/* 수정기록 탭 */
.history-screen{display:none;padding:12px 14px;flex-direction:column;gap:6px;}
.hist-date-hdr{font-size:11px;font-weight:700;color:#94a3b8;padding:4px 2px;margin-top:4px;}

/* 토스트 */
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(70px);background:#1a1a2e;color:#fff;font-size:13px;font-weight:700;padding:12px 24px;border-radius:50px;white-space:nowrap;pointer-events:none;transition:transform .25s cubic-bezier(.34,1.56,.64,1);z-index:999;}
.toast.show{transform:translateX(-50%) translateY(0);}
</style>
</head>
<body>

<div class="ah">
  <div class="at">범퍼 수정일지</div>
  <div class="hr">
    <div class="db" id="top-date"></div>
    <div class="fb" id="fac-badge" onclick="goSetup()">공장 선택</div>
  </div>
  <div class="tabs" id="tabs" style="display:none;">
    <div class="tab active" id="tab-input" onclick="showTab('input')">입력</div>
    <div class="tab" id="tab-list" onclick="showTab('list')">오늘 목록 <span id="list-cnt" style="background:rgba(255,255,255,0.2);padding:1px 6px;border-radius:8px;font-size:10px;">0</span></div>
    <div class="tab" id="tab-hist" onclick="showTab('hist')">수정 기록</div>
  </div>
</div>

<!-- 공장 선택 -->
<div class="ss" id="setup-screen">
  <div style="font-size:48px;margin-bottom:18px;">🏭</div>
  <div style="font-size:18px;font-weight:700;color:#1e293b;margin-bottom:8px;">소속 공장을 선택하세요</div>
  <div style="font-size:13px;color:#94a3b8;text-align:center;line-height:1.7;margin-bottom:32px;">한 번 선택하면 이후 입력 시<br>자동으로 적용됩니다</div>
  <div style="width:100%;max-width:400px;">
    <div class="fbtn" onclick="setF('1공장')"><div class="fbtn-name">KIA 광주 1공장</div><div class="fbtn-sub">OV1 · SP3</div></div>
    <div class="fbtn" onclick="setF('2공장')"><div class="fbtn-name">KIA 광주 2공장</div><div class="fbtn-sub">NQ5 PE</div></div>
    <div class="fbtn" onclick="setF('3공장')"><div class="fbtn-name">KIA 광주 3공장</div><div class="fbtn-sub">PU</div></div>
  </div>
</div>

<!-- 입력 폼 -->
<div class="fs" id="form-screen">
  <div class="bb" onclick="goSetup()"><div class="ba">←</div><div class="bt">공장 변경</div></div>
  <div class="scroll-body" id="form-body">
    <div class="card">
      <div class="sl">차종</div>
      <div class="bg" id="model-grp"></div>
    </div>
    <div class="card">
      <div class="sl">구분</div>
      <div class="bg" id="pos-grp">
        <div class="bs" onclick="pickB('pos-grp',this)">FRT</div>
        <div class="bs" onclick="pickB('pos-grp',this)">RR</div>
        <div class="bs" id="cpad-btn" style="display:none;" onclick="pickB('pos-grp',this)">C·PAD</div>
      </div>
    </div>
    <div class="card">
      <div class="sl">C/NO</div>
      <input class="cno-inp" id="cno-inp" type="text" inputmode="numeric" maxlength="4" placeholder="0001" autocomplete="off"
        oninput="onCnoInput(this)" onblur="onCnoBlur(this)" onfocus="onCnoFocus(this)">
    </div>
    <div class="card">
      <div class="sl">색상 코드</div>
      <select class="inp" id="color-sel"><option value="">선택하세요</option></select>
    </div>
    <div class="card">
      <div class="sl">조치사항</div>
      <div class="act-row">
        <div class="act" id="act-fix" onclick="pickAct('fix')">수정</div>
        <div class="act" id="act-swp" onclick="pickAct('swp')">교환</div>
      </div>
    </div>
    <div class="card" id="defect-card" style="display:none;">
      <div class="sl">불량 유형</div>
      <select class="inp" id="defect-sel" onchange="onDefect(this.value)"><option value="">대분류 선택</option></select>
      <div class="extra" id="sub-paint"><div class="hint">세부 항목</div>
        <select class="inp"><option value="">선택하세요</option><option>티이물</option><option>박리</option><option>기타</option></select>
      </div>
      <div class="extra" id="sub-assembly"><div class="hint">부품명</div><input class="inp" type="text" placeholder="부품명 입력"></div>
      <div class="extra" id="sub-etc"><div class="hint">직접 입력</div><input class="inp" id="etc-txt" type="text" placeholder="불량 내용 입력"></div>
      <div class="extra" id="sub-part-frt">
        <div class="hint">교환 부품 (FRT)</div>
        <select class="inp" onchange="onPartOther(this,'other-frt')">
          <option value="">부품 선택</option>
          <option>BUMPER ASSY-FR (프론트 범퍼 앗세이)</option>
          <option>COVER-FR BUMPER UPR (페이스)</option><option>COVER-FR BUMPER LWR (로워)</option>
          <option>GRILLE-RADIATOR (라디에이터그릴)</option><option>PIECE-RADIATOR GRILLE (그릴 피스)</option>
          <option>COVER-RADIATOR GRILLE UPR (어퍼커버)</option>
          <option>MOLDING-FR BUMPER LH (몰딩 LH)</option><option>MOLDING-FR BUMPER RH (몰딩 RH)</option>
          <option>GRILLE-FR BUMPER (그릴)</option><option>SKID PLATE-FR BUMPER (프론트 스키드)</option>
          <option>CAP-FR HOOK (후크캡)</option><option>LIP BUMPER (에어립)</option>
          <option value="기타">기타 (직접 입력)</option>
        </select>
        <div class="extra" id="other-frt"><input class="inp" style="margin-top:7px;" type="text" placeholder="FRT 부품명 직접 입력"></div>
      </div>
      <div class="extra" id="sub-part-rr">
        <div class="hint">교환 부품 (RR)</div>
        <select class="inp" onchange="onPartOther(this,'other-rr')">
          <option value="">부품 선택</option>
          <option>BUMPER ASSY-RR (리어 범퍼 앗세이)</option>
          <option>COVER-RR BUMPER UPR LH (어퍼커버 LH)</option><option>COVER-RR BUMPER UPR RH (어퍼커버 RH)</option>
          <option>COVER-RR BUMPER LWR (리어로워)</option><option>SKID PLATE-RR BUMPER (리어 스키드)</option>
          <option>CAP-RR HOOK (후크캡)</option><option value="기타">기타 (직접 입력)</option>
        </select>
        <div class="extra" id="other-rr"><input class="inp" style="margin-top:7px;" type="text" placeholder="RR 부품명 직접 입력"></div>
      </div>
      <div class="extra" id="sub-part-both">
        <div class="hint">교환 부품 (FRT)</div>
        <select class="inp" style="margin-bottom:7px;" onchange="onPartOther(this,'other-both-frt')">
          <option value="">부품 선택</option>
          <option>BUMPER ASSY-FR (프론트 범퍼 앗세이)</option>
          <option>COVER-FR BUMPER UPR (페이스)</option><option>COVER-FR BUMPER LWR (로워)</option>
          <option>GRILLE-RADIATOR (라디에이터그릴)</option><option>PIECE-RADIATOR GRILLE (그릴 피스)</option>
          <option>COVER-RADIATOR GRILLE UPR (어퍼커버)</option>
          <option>MOLDING-FR BUMPER LH (몰딩 LH)</option><option>MOLDING-FR BUMPER RH (몰딩 RH)</option>
          <option>GRILLE-FR BUMPER (그릴)</option><option>SKID PLATE-FR BUMPER (프론트 스키드)</option>
          <option>CAP-FR HOOK (후크캡)</option><option>LIP BUMPER (에어립)</option>
          <option value="기타">기타 (직접 입력)</option>
        </select>
        <div class="extra" id="other-both-frt"><input class="inp" style="margin-bottom:7px;" type="text" placeholder="FRT 부품명 직접 입력"></div>
        <div class="hint">교환 부품 (RR)</div>
        <select class="inp" onchange="onPartOther(this,'other-both-rr')">
          <option value="">부품 선택</option>
          <option>BUMPER ASSY-RR (리어 범퍼 앗세이)</option>
          <option>COVER-RR BUMPER UPR LH (어퍼커버 LH)</option><option>COVER-RR BUMPER UPR RH (어퍼커버 RH)</option>
          <option>COVER-RR BUMPER LWR (리어로워)</option><option>SKID PLATE-RR BUMPER (리어 스키드)</option>
          <option>CAP-RR HOOK (후크캡)</option><option value="기타">기타 (직접 입력)</option>
        </select>
        <div class="extra" id="other-both-rr"><input class="inp" style="margin-top:7px;" type="text" placeholder="RR 부품명 직접 입력"></div>
      </div>
    </div>
    <div class="card">
      <div class="sl">책임구 <span class="sl-sub">( 알카 귀책처 )</span></div>
      <div class="resp-row">
        <div class="rb" onclick="pickR(this)">캠스</div>
        <div class="rb" onclick="pickR(this)">기아</div>
        <div class="rb" onclick="pickR(this)">복합</div>
      </div>
    </div>
    <div class="card">
      <div class="sl">불량 사진 <span class="sl-badge">선택</span></div>
      <div class="photo-zone" onclick="document.getElementById('photo-input').click()">
        <div style="font-size:24px;">📷</div>
        <div class="photo-text">사진 촬영 / 선택</div>
        <div class="photo-sub">최대 3장 · 탭하여 추가</div>
        <div class="photo-preview" id="photo-preview"></div>
      </div>
      <input type="file" id="photo-input" accept="image/*" multiple style="display:none;" onchange="onPhoto(this)">
    </div>
    <div class="card">
      <div class="sl">비고 <span class="sl-badge">선택</span></div>
      <textarea class="inp" id="memo" placeholder="추가 내용 입력..."></textarea>
    </div>
    <button class="sub-btn" onclick="submitForm()">제출하기</button>
  </div>
</div>

<!-- 오늘 목록 -->
<div class="list-screen" id="list-screen">
  <div id="list-body"></div>
</div>

<!-- 수정 기록 -->
<div class="history-screen" id="hist-screen">
  <div id="hist-body"></div>
</div>

<div class="toast" id="toast"></div>

<script>
const API = 'https://bumper-repair-api.onrender.com';
const COLORS = {
  '1공장':['SWP','BU3','FSB','KDG','KLG','EBB','OVR','MRM','IEG','IEB','ISG','ISM','BJG','GBG','1D','M3R','PLU','B3A'],
  '2공장':['SWP','KDG','FSB','BB2','C7A','HRB','JUG','KLG','MGG','UD','KLT'],
  '3공장':['UD','MA','BPY']
};
const CAR = {'1공장':['OV1','SP3'],'2공장':['NQ5 PE'],'3공장':['PU']};
const DEFECTS_FIX = ['찍힘','긁힘','파손','도장불량','조립불량','고무링말림','티이물','기타'];
const DEFECTS_SWP = ['찍힘','긁힘','파손','도장불량','조립불량','이종','기타'];

let curF='', curAct='', curTab='input';
let todayRecords = [];
let photoFiles = [];

// 날짜
const D=new Date(), DY=['일','월','화','수','목','금','토'];
document.getElementById('top-date').textContent =
  D.getFullYear()+'.'+String(D.getMonth()+1).padStart(2,'0')+'.'+String(D.getDate()).padStart(2,'0')+' ('+DY[D.getDay()]+')';

// 탭 전환
function showTab(t) {
  curTab = t;
  ['input','list','hist'].forEach(n => {
    document.getElementById('tab-'+n).classList.toggle('active', n===t);
  });
  document.getElementById('form-screen').style.display = t==='input' ? 'flex' : 'none';
  document.getElementById('list-screen').style.display = t==='list' ? 'flex' : 'none';
  document.getElementById('hist-screen').style.display = t==='hist' ? 'flex' : 'none';
  if(t==='list') renderList();
  if(t==='hist') loadHistory();
}

// 공장 선택
function setF(f) {
  curF = f;
  document.getElementById('fac-badge').textContent = f;
  document.getElementById('setup-screen').style.display = 'none';
  document.getElementById('tabs').style.display = 'flex';
  showTab('input');
  document.getElementById('form-screen').style.display = 'flex';
  document.getElementById('cpad-btn').style.display = f==='3공장'?'flex':'none';
  const mg = document.getElementById('model-grp');
  mg.innerHTML = '';
  CAR[f].forEach((m,i) => {
    const d = document.createElement('div');
    d.className = 'bs'+(i===0?' on':'');
    d.textContent = m;
    d.onclick = function(){pickB('model-grp',this);};
    mg.appendChild(d);
  });
  const cs = document.getElementById('color-sel');
  cs.innerHTML = '<option value="">선택하세요</option>';
  COLORS[f].forEach(c => { const o=document.createElement('option');o.textContent=c;cs.appendChild(o); });
  curAct = '';
  document.getElementById('act-fix').className='act';
  document.getElementById('act-swp').className='act';
  document.getElementById('defect-card').style.display='none';
  document.getElementById('cno-inp').value='';
  document.getElementById('memo').value='';
  loadHistory();
}
function goSetup() {
  document.getElementById('setup-screen').style.display='flex';
  document.getElementById('form-screen').style.display='none';
  document.getElementById('list-screen').style.display='none';
  document.getElementById('hist-screen').style.display='none';
  document.getElementById('tabs').style.display='none';
}

// C/NO
function onCnoInput(el){el.value=el.value.replace(/[^0-9]/g,'').slice(0,4);}
function onCnoFocus(el){const n=parseInt(el.value||'0',10);el.value=n>0?String(n):'';el.placeholder='숫자 입력';}
function onCnoBlur(el){const r=el.value.replace(/[^0-9]/g,'');if(!r||r==='0000'){el.value='';el.placeholder='0001';return;}const n=Math.min(9999,Math.max(1,parseInt(r,10)));el.value=String(n).padStart(4,'0');}

function pickB(g,el){document.querySelectorAll('#'+g+' .bs').forEach(b=>b.classList.remove('on'));el.classList.add('on');if(g==='pos-grp'&&curAct==='swp'){const v=document.getElementById('defect-sel').value;if(v&&v!=='기타')updatePartDD();}}
function pickR(el){document.querySelectorAll('.rb').forEach(b=>b.classList.remove('on'));el.classList.add('on');}
function pickAct(t){
  curAct=t;
  document.getElementById('act-fix').className='act'+(t==='fix'?' sel-fix':'');
  document.getElementById('act-swp').className='act'+(t==='swp'?' sel-swp':'');
  const list=t==='fix'?DEFECTS_FIX:DEFECTS_SWP;
  const sel=document.getElementById('defect-sel');
  sel.innerHTML='<option value="">대분류 선택</option>';
  list.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;sel.appendChild(o);});
  document.getElementById('defect-card').style.display='block';
  hideAllSub();
}
function hideAllSub(){['sub-paint','sub-assembly','sub-etc','sub-part-frt','sub-part-rr','sub-part-both','other-frt','other-rr','other-both-frt','other-both-rr'].forEach(id=>document.getElementById(id).className='extra');}
function onDefect(v){
  hideAllSub();
  if(curAct==='fix'){
    if(v==='도장불량')document.getElementById('sub-paint').className='extra show';
    else if(v==='조립불량')document.getElementById('sub-assembly').className='extra show';
    else if(v==='기타')document.getElementById('sub-etc').className='extra show';
  } else if(curAct==='swp'){
    if(v==='기타'){document.getElementById('sub-etc').className='extra show';return;}
    if(v)updatePartDD();
  }
}
function updatePartDD(){
  const pos=(document.querySelector('#pos-grp .bs.on')||{}).textContent||'';
  ['sub-part-frt','sub-part-rr','sub-part-both'].forEach(id=>document.getElementById(id).className='extra');
  if(pos==='FRT')document.getElementById('sub-part-frt').className='extra show';
  else if(pos==='RR')document.getElementById('sub-part-rr').className='extra show';
  else document.getElementById('sub-part-both').className='extra show';
}
function onPartOther(sel,id){document.getElementById(id).className='extra'+(sel.value==='기타'?' show':'');}

// 사진
function onPhoto(input){
  const files=Array.from(input.files).slice(0,3);
  photoFiles=files;
  const preview=document.getElementById('photo-preview');
  preview.innerHTML='';
  files.forEach(f=>{
    const reader=new FileReader();
    reader.onload=e=>{const img=document.createElement('img');img.className='photo-thumb';img.src=e.target.result;preview.appendChild(img);};
    reader.readAsDataURL(f);
  });
}

// 제출
async function submitForm(){
  const model=(document.querySelector('#model-grp .bs.on')||{}).textContent||'';
  const pos=(document.querySelector('#pos-grp .bs.on')||{}).textContent||'';
  const resp=(document.querySelector('.rb.on')||{}).textContent||'';
  const defect=document.getElementById('defect-sel').value;
  const cno=document.getElementById('cno-inp').value;
  const color=document.getElementById('color-sel').value;
  const memo=document.getElementById('memo').value;

  if(!model){showToast('차종을 선택해주세요');return;}
  if(!pos){showToast('구분을 선택해주세요');return;}
  if(!cno){showToast('C/NO를 입력해주세요');return;}
  if(!color){showToast('색상 코드를 선택해주세요');return;}
  if(!curAct){showToast('조치사항을 선택해주세요');return;}
  if(!defect){showToast('불량 유형을 선택해주세요');return;}
  if(!resp){showToast('책임구를 선택해주세요');return;}

  const now=new Date();
  const timeStr=String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0');
  const record={
    factory:curF, model, position:pos, cno, color,
    action:curAct==='fix'?'수정':'교환',
    defect, resp, memo, time:timeStr,
    id: Date.now()
  };

  todayRecords.push(record);
  document.getElementById('list-cnt').textContent=todayRecords.length;

  try {
    await fetch(API+'/submit',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(record)
    });
  } catch(e){}

  showToast('제출 완료! ✓');
  setTimeout(resetForm, 1500);
}

function resetForm(){
  document.querySelectorAll('.bs.on,.rb.on').forEach(e=>e.classList.remove('on'));
  document.getElementById('cno-inp').value='';
  document.getElementById('color-sel').value='';
  document.getElementById('memo').value='';
  document.getElementById('photo-preview').innerHTML='';
  photoFiles=[];
  curAct='';
  document.getElementById('act-fix').className='act';
  document.getElementById('act-swp').className='act';
  document.getElementById('defect-card').style.display='none';
  hideAllSub();
  // 차종 첫번째 다시 선택
  const first=document.querySelector('#model-grp .bs');
  if(first)first.classList.add('on');
  window.scrollTo({top:0,behavior:'smooth'});
}

// 오늘 목록 렌더
function renderList(){
  const body=document.getElementById('list-body');
  if(!todayRecords.length){
    body.innerHTML='<div class="empty-state"><div class="empty-icon">📋</div><div class="empty-text">아직 입력된 내역이 없어요</div><div class="empty-sub">입력 탭에서 수정일지를 작성해주세요</div></div>';
    return;
  }
  body.innerHTML=todayRecords.map((r,i)=>`
    <div class="list-item">
      <div class="li-num">${i+1}</div>
      <div class="li-body">
        <div class="li-top">
          <span class="li-tag ${r.action==='수정'?'fix':'swp'}">${r.action}</span>
          <span class="li-title">${r.model} · ${r.position} · ${r.defect}</span>
        </div>
        <div class="li-sub">C/NO ${r.cno} · ${r.color} · ${r.resp}</div>
        ${r.memo?'<div class="li-sub">'+r.memo+'</div>':''}
        <div class="li-time">${r.time}</div>
      </div>
    </div>
  `).join('');
}

// 수정 기록 (API)
async function loadHistory(){
  const body=document.getElementById('hist-body');
  body.innerHTML='<div class="empty-state"><div class="empty-icon" style="font-size:24px;">⏳</div><div class="empty-text">불러오는 중...</div></div>';
  try {
    const res=await fetch(API+'/records?factory='+encodeURIComponent(curF)+'&limit=50');
    const data=await res.json();
    if(!data.length){
      body.innerHTML='<div class="empty-state"><div class="empty-icon">📂</div><div class="empty-text">수정 기록이 없어요</div></div>';
      return;
    }
    let lastDate='';
    body.innerHTML=data.map((r,i)=>{
      const d=r.created_at?r.created_at.slice(0,10):'';
      const dateHdr=d!==lastDate?`<div class="hist-date-hdr">${d}</div>`:'';
      lastDate=d;
      return dateHdr+`
        <div class="list-item">
          <div class="li-num">${i+1}</div>
          <div class="li-body">
            <div class="li-top">
              <span class="li-tag ${r.action==='수정'?'fix':'swp'}">${r.action}</span>
              <span class="li-title">${r.model||''} · ${r.position||''} · ${r.defect||''}</span>
            </div>
            <div class="li-sub">C/NO ${r.cno||''} · ${r.color||''} · ${r.resp||''}</div>
            ${r.memo?'<div class="li-sub">'+r.memo+'</div>':''}
            <div class="li-time">${r.created_at?r.created_at.slice(11,16):''}</div>
          </div>
        </div>`;
    }).join('');
  } catch(e){
    body.innerHTML='<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-text">기록을 불러올 수 없어요</div><div class="empty-sub">네트워크를 확인해주세요</div></div>';
  }
}

function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000);}
</script>
</body>
</html>
