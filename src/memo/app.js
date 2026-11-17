

const TYPES = [{id:'mc',name:'객관식'},{id:'sa',name:'단답형'},{id:'ox',name:'OX'},{id:'blank',name:'빈칸'}];
const TNAME = {mc:'객관식',sa:'단답형',ox:'OX',blank:'빈칸 채우기'};
const app = document.getElementById('app');
function km(){ if(window.renderMathInElement){ try{ renderMathInElement(app,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false,output:'mathml'}); }catch(e){} } }
function setHTML(h){ app.innerHTML = h; km(); }
const RAW = q => !!q.raw;
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let storageOK = true;
try{ localStorage.setItem('memquiz_probe', '1'); if(localStorage.getItem('memquiz_probe') !== '1') storageOK = false; localStorage.removeItem('memquiz_probe'); }catch(e){ storageOK = false; }
const store = {
  get(k, d){ try{ const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; }catch(e){ return d; } },
  set(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){ storageOK = false; } }
};
const K = 'memquiz1_';
let stats = store.get(K+'stats', {});   // per question: {c, w, l, t}
let mast = store.get(K+'mast', {});     // per content group: {b: box 0..5, t: last time, n: times asked, w: times missed}
let stars = new Set(store.get(K+'stars', []));
const keyOf = q => q.sec + '|' + q.sub;
BANK.forEach((q, i) => { q.ord = i; if(q.k == null) q.k = q.id; });

/* ---------- per-subject index ---------- */
const SUB = {};
SUBJECTS.forEach(sj => {
  const bank = BANK.filter(q => q.subj === sj.id);
  const con = {}, clist = [];
  bank.forEach(q => { let c = con[q.k]; if(!c){ c = con[q.k] = {k:q.k, sec:q.sec, sub:q.sub, qs:[]}; clist.push(c); } c.qs.push(q); });
  const secname = {};
  const idx = sj.sections.map(s => {
    secname[s.id] = s.name;
    const subs = [], m = {};
    bank.forEach(q => { if(q.sec !== s.id) return; if(!m[q.sub]){ m[q.sub] = {name:q.sub, key:keyOf(q), n:0}; subs.push(m[q.sub]); } m[q.sub].n++; });
    return {id:s.id, name:s.name, subs, n:subs.reduce((a, b) => a + b.n, 0), cons:clist.filter(c => c.sec === s.id)};
  }).filter(s => s.n);
  SUB[sj.id] = {id:sj.id, name:sj.name, bank, con, clist, idx, secname, allkeys:idx.flatMap(s => s.subs.map(x => x.key))};
});
const LIVE = SUBJECTS.filter(s => SUB[s.id].bank.length);

let cfg = Object.assign({subj:null, subs:{}, types:['mc','sa','ox','blank'], count:20, order:'rand', pool:'smart', sa:'type', mode:'learn'}, store.get(K+'cfg', {}));
if(!cfg.subs || Array.isArray(cfg.subs)) cfg.subs = {};
if(!['learn','exam','speed','match'].includes(cfg.mode)) cfg.mode = 'learn';
if(!LIVE.some(s => s.id === cfg.subj)) cfg.subj = LIVE.length ? LIVE[0].id : null;
const SEL = {};
LIVE.forEach(s => { const all = SUB[s.id].allkeys; SEL[s.id] = new Set(cfg.subs[s.id] ? cfg.subs[s.id].filter(k => all.includes(k)) : all); });
let selTypes = new Set(cfg.types);
const openSecs = new Set();
const cur = () => SUB[cfg.subj];
const sel = () => SEL[cfg.subj];
function saveCfg(){ LIVE.forEach(s => cfg.subs[s.id] = [...SEL[s.id]]); cfg.types = [...selTypes]; store.set(K+'cfg', cfg); }

/* ---------- memory model: Leitner boxes with time gaps ----------
   box 0 = currently wrong, 1-2 = learning, 3+ = learned. A correct first answer moves a group up one box,
   any miss sends it back to box 0. A group comes back for review once GAP[box] has passed. */
const GAP = [0, 5*60e3, 30*60e3, 4*3600e3, 24*3600e3, 72*3600e3];
const seen = c => !!mast[c.k] && mast[c.k].n > 0;
const boxOf = c => seen(c) ? mast[c.k].b : -1;
const learned = c => boxOf(c) >= 3;
const due = (c, now) => seen(c) && now - mast[c.k].t >= GAP[Math.min(5, mast[c.k].b)];
function mset(k, fn){ const m = mast[k] || (mast[k] = {b:0, t:0, n:0, w:0}); fn(m); m.t = Date.now(); store.set(K+'mast', mast); }
const dotOf = c => learned(c) ? 'g' : boxOf(c) > 0 ? 'y' : boxOf(c) === 0 ? 'r' : '';

const inScope = q => sel().has(keyOf(q));
const variants = c => c.qs.filter(q => inScope(q) && selTypes.has(q.type));
function shuffle(a){ a = a.slice(); for(let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

// content groups a session would draw from, in the order they would be asked
function candidates(){
  const now = Date.now();
  let cs = cur().clist.filter(c => variants(c).length);
  if(cfg.pool === 'new') cs = cs.filter(c => !seen(c));
  else if(cfg.pool === 'weak') cs = cs.filter(c => seen(c) && !learned(c));
  else if(cfg.pool === 'star') cs = cs.filter(c => variants(c).some(q => stars.has(q.id)));
  if(cfg.pool === 'smart'){
    const t1 = shuffle(cs.filter(c => due(c, now))).sort((a, b) => boxOf(a) - boxOf(b));           // missed / due for review, weakest first
    const t2 = cs.filter(c => !seen(c));                                                             // not studied yet
    const t3 = shuffle(cs.filter(c => seen(c) && !due(c, now))).sort((a, b) => boxOf(a) - boxOf(b) || mast[a.k].t - mast[b.k].t);
    return t1.concat(cfg.order === 'rand' ? shuffle(t2) : t2, t3);
  }
  return cfg.order === 'rand' ? shuffle(cs) : cs;
}

/* ---------- HOME ---------- */
let view = 'home', sess = null, hideAns = true;
function mastBar(cs){
  const n = cs.length || 1;
  const g = cs.filter(learned).length, y = cs.filter(c => boxOf(c) > 0 && !learned(c)).length, r = cs.filter(c => boxOf(c) === 0).length;
  return {g, y, r, rest: cs.length - g - y - r,
    html:`<div class="mast"><i class="g" style="width:${100*g/n}%"></i><i class="y" style="width:${100*y/n}%"></i><i class="r" style="width:${100*r/n}%"></i></div>`};
}
function renderHome(){
  view = 'home';
  if(!cfg.subj){ setHTML('<h1>암기 퀴즈</h1><p class="lead">문제가 없습니다.</p>'); return; }
  const S = cur(), now = Date.now();
  const mb = mastBar(S.clist);
  const dueN = S.clist.filter(c => due(c, now) && !learned(c)).length;
  const cand = candidates();
  const scope = S.bank.filter(inScope);
  const n = cfg.count === 0 ? cand.length : Math.min(cfg.count, cand.length);
  let h = '';
  h += `<h1>${LIVE.length > 1 ? '반복 학습 · 암기 퀴즈' : esc(S.name) + ' 암기 퀴즈'}</h1>`;
  h += `<a class="backlink" href="index.html">← 1-2 기말 복습으로</a>`;
  h += `<p class="lead">문제 ${S.bank.length}개 · 외울 내용 ${S.clist.length}가지</p>`;
  if(!storageOK) h += `<div class="note">이 화면에서는 풀이 기록이 저장되지 않습니다. 틀린 내용 반복은 이번에 켜 둔 동안만 동작합니다. 브라우저(크롬·사파리·삼성 인터넷)로 열면 기록이 저장됩니다.</div>`;
  if(LIVE.length > 1) h += `<div class="card"><h2>과목</h2><div class="seg">` + LIVE.map(s => `<button class="chip ${s.id === cfg.subj ? 'on' : ''}" data-a="subj" data-id="${esc(s.id)}">${esc(s.name)}</button>`).join('') + `</div></div>`;
  h += `<div class="card"><h2>내 암기 상태</h2>${mb.html}<div class="legend"><span class="g">익힘 ${mb.g}</span><span class="y">익히는 중 ${mb.y}</span><span class="r">틀림 ${mb.r}</span><span>아직 안 봄 ${mb.rest}</span></div>${dueN ? `<p class="hint">지금 다시 볼 차례인 내용이 ${dueN}가지 있습니다.</p>` : ''}</div>`;

  h += `<div class="card"><h2>범위</h2><div class="links"><button data-a="all">전체 선택</button><button data-a="none">전체 해제</button></div>`;
  S.idx.forEach(s => {
    const on = s.subs.filter(x => sel().has(x.key)).length;
    const cls = on === 0 ? '' : on === s.subs.length ? 'on' : 'part';
    const sb = mastBar(s.cons);
    const open = openSecs.has(s.id);
    h += `<div class="sec"><div class="sec-head">
      <button class="row" style="flex:1;min-height:54px" data-a="sec" data-id="${esc(s.id)}">
        <span class="box ${cls}">${cls === 'on' ? '✓' : cls === 'part' ? '–' : ''}</span>
        <span class="sec-name">${esc(s.name)}<small>${s.n}문제 · 소주제 ${on}/${s.subs.length} 선택 · 익힘 ${sb.g}/${s.cons.length}</small></span>
      </button>
      <button class="caret" data-a="open" data-id="${esc(s.id)}" aria-label="소주제 펼치기">${open ? '▲' : '▼'}</button></div>`;
    if(open){
      h += `<div class="subs">` + s.subs.map(x => `<button class="chip ${sel().has(x.key) ? 'on' : ''}" data-a="sub" data-k="${esc(x.key)}">${esc(x.name)}<b>${x.n}</b></button>`).join('') + `</div>`;
    }
    h += `</div>`;
  });
  h += `</div>`;

  const seg = (name, key, opts, hint) => `<div class="card"><h2>${name}</h2><div class="seg">` + opts.map(o =>
    `<button class="chip ${cfg[key] === o[0] ? 'on' : ''}" data-a="cfg" data-key="${key}" data-v="${o[0]}">${o[1]}</button>`).join('') + `</div>${hint ? `<p class="hint">${hint}</p>` : ''}</div>`;
  const best = store.get(K+'best', {});
  const modeHint = {
    learn:'틀린 내용은 다른 문제들이 나오다가, 형식과 표현이 바뀐 문제로 다시 나옵니다. 맞히면 끝날 때쯤 한 번 더 확인하고, 그것도 맞혀야 통과입니다.',
    exam:'채점 없이 끝까지 푼 다음 한꺼번에 점수를 봅니다. 여기서 틀린 내용은 반복 학습에서 먼저 나옵니다.',
    speed:'60초 동안 OX 문제를 최대한 많이 맞히는 게임입니다. 틀리면 시간이 멈추고 설명이 나옵니다.' + (best['speed_' + cfg.subj] != null ? ` 최고 기록 ${best['speed_' + cfg.subj]}점.` : ''),
    match:'문제 4개와 답 4개를 짝지어 없애는 게임입니다. 5판을 실수 없이 빨리 끝내 보세요.' + (best['match_' + cfg.subj] != null ? ` 최고 기록 ${best['match_' + cfg.subj]}초.` : '')
  }[cfg.mode];
  h += seg('방식', 'mode', [['learn','반복 학습'],['exam','모의고사'],['speed','스피드 OX'],['match','짝 맞추기']], modeHint);
  const quiz = cfg.mode === 'learn' || cfg.mode === 'exam';
  if(quiz){
    h += `<div class="card"><h2>문제 형식</h2><div class="seg">` + TYPES.map(t => {
      const cnt = scope.filter(q => q.type === t.id).length;
      return `<button class="chip ${selTypes.has(t.id) ? 'on' : ''}" data-a="type" data-id="${t.id}">${t.name}<b>${cnt}</b></button>`;
    }).join('') + `</div><p class="hint">여러 형식을 켜 두면 처음 보는 내용은 고르는 문제(객관식·OX)로, 익숙해질수록 직접 쓰는 문제(빈칸·단답형)로 나옵니다.</p></div>`;
    const poolHint = {smart:'틀렸거나 다시 볼 때가 된 내용 → 아직 안 본 내용 → 이미 익힌 내용 순서로 나옵니다.', new:'한 번도 안 본 내용만 나옵니다.', weak:'봤지만 아직 익히지 못한 내용만 나옵니다.', star:'★ 표시한 문제의 내용만 나옵니다.', all:'선택한 범위 전체에서 나옵니다.'}[cfg.pool];
    h += seg('무엇을 풀까', 'pool', [['smart','추천 순서'],['new','안 본 내용'],['weak','못 익힌 내용'],['star','★ 표시'],['all','전체']], poolHint);
    h += seg('한 번에 풀 양', 'count', [[10,'10'],[20,'20'],[30,'30'],[50,'50'],[0,'전부']]);
    h += seg('순서', 'order', [['rand','무작위'],['seq','자료 순서']]);
    if(cfg.mode === 'learn') h += seg('단답형·빈칸 답하는 방법', 'sa', [['type','직접 입력'],['self','떠올리고 스스로 채점']]);
  }
  h += `<div class="foot"><button data-a="reset">${esc(S.name)} 풀이 기록 지우기</button></div>`;
  let ok, label;
  if(quiz){ ok = n > 0; label = n ? `시작 · ${n}가지` + (cand.length > n ? `<small>조건에 맞는 ${cand.length}가지 중</small>` : '') : '해당하는 내용 없음'; }
  else if(cfg.mode === 'speed'){ const m = scope.filter(q => q.type === 'ox').length; ok = m > 0; label = ok ? `스피드 OX 시작<small>OX 문제 ${m}개</small>` : 'OX 문제 없음'; }
  else { const m = matchPool().length; ok = m >= 4; label = ok ? `짝 맞추기 시작<small>짝지을 내용 ${m}가지</small>` : '짝지을 내용이 부족함'; }
  h += `<div class="bar"><div class="bar-in"><button class="btn ghost side" data-a="study" ${scope.length ? '' : 'disabled'}>요점 보기</button><button class="btn" data-a="start" ${ok ? '' : 'disabled'}>${label}</button></div></div>`;
  setHTML(h);
}

/* ---------- STUDY (read the key points of the selected range, answers hidden until tapped) ---------- */
function factOf(c){
  const by = t => c.qs.find(q => q.type === t);
  let q;
  if((q = by('blank'))) return QT(q).replace(/_{3,}/, `<b>${esc(q.answer)}</b>`);
  if((q = by('sa'))) return `${QT(q)} <b>${esc(answerText(q))}</b>`;
  if((q = by('mc'))) return `${QT(q)} <b>${CH(q, q.answer)}</b>`;
  q = c.qs.find(x => x.type === 'ox' && x.answer === true);
  if(q) return `<b>${QT(q)}</b>`;
  return `<b>${c.qs[0].raw ? (c.qs[0].exp || c.qs[0].q) : esc(c.qs[0].exp || c.qs[0].q)}</b>`;
}
let studyF = 'all';
function renderStudy(){
  view = 'study';
  const S = cur();
  const keep = c => c.qs.some(inScope) && (studyF === 'all' || (studyF === 'wrong' ? boxOf(c) === 0 : (seen(c) && !learned(c))));
  let h = `<div class="sticky"><button class="icon" data-a="home" aria-label="돌아가기">←</button><b style="flex:1">요점 보기</b>
    <button class="chip ${hideAns ? 'on' : ''}" data-a="hide">${hideAns ? '답 가림 · 누르면 보임' : '답 보이는 중'}</button>
    <div class="seg" style="flex:1 0 100%">` + [['all','전체'],['wrong','틀린 것'],['weak','못 익힌 것']].map(o =>
      `<button class="chip ${studyF === o[0] ? 'on' : ''}" data-a="sf" data-v="${o[0]}">${o[1]}</button>`).join('') + `</div></div>`;
  h += `<div class="${hideAns ? 'hideans' : ''}">`;
  let any = false;
  S.idx.forEach(s => {
    const cs = s.cons.filter(keep);
    if(!cs.length) return;
    any = true;
    h += `<h1 style="font-size:18px;margin-top:14px">${esc(s.name)}</h1>`;
    let last = null, open = false;
    cs.forEach(c => {
      if(c.sub !== last){ if(open) h += `</div>`; h += `<h3>${esc(c.sub)}</h3><div class="card">`; open = true; last = c.sub; }
      h += `<button class="fact" data-a="fact"><span class="dot ${dotOf(c)}"></span><span>${factOf(c)}</span></button>`;
    });
    if(open) h += `</div>`;
  });
  if(!any) h += `<p class="lead" style="margin-top:20px">해당하는 내용이 없습니다.</p>`;
  h += `</div>`;
  setHTML(h);
}

/* ---------- SESSION ----------
   queue entries: {k, kind}. kind 'first' = first time this session, 'retry' = missed earlier (asked again a few
   questions later with a different question), 'confirm' = final check at the end after a successful retry. */
function start(cons, mode){
  if(!cons){ cons = candidates(); if(cfg.count) cons = cons.slice(0, cfg.count); }
  if(!cons.length) return false;
  sess = {queue: cons.map(c => ({k:c.k, kind:'first'})), i:0, st:{}, log:[], total:cons.length, cleared:0, streak:0,
    mode: mode || (cfg.mode === 'exam' ? 'exam' : 'learn')};   // learn = missed content comes back, exam = no feedback until the end
  cons.forEach(c => sess.st[c.k] = {used:[], miss:0, first:null, lastType:null});
  prep(); renderQuiz(); window.scrollTo(0, 0);
  return true;
}
// which format to prefer: recognition (pick an answer) for new or just-missed content, recall (write it) once it is familiar
function typePref(e, c){
  if(e.kind === 'retry') return ['mc', 'ox', 'blank', 'sa'];
  if(e.kind === 'confirm') return ['sa', 'blank', 'mc', 'ox'];
  const b = boxOf(c);
  if(b <= 0) return ['mc', 'ox', 'blank', 'sa'];
  if(b <= 2) return ['blank', 'sa', 'mc', 'ox'];
  return ['sa', 'blank', 'mc', 'ox'];
}
function pickVariant(c, st, e){
  let vs = variants(c); if(!vs.length) vs = c.qs;
  let pool = vs.filter(q => !st.used.includes(q.id));                                   // never the same question twice in a session if avoidable
  if(!pool.length){ const last = st.used[st.used.length - 1]; pool = vs.filter(q => q.id !== last); if(!pool.length) pool = vs; }
  if(cfg.pool === 'star' && !st.used.length){ const s = pool.filter(q => stars.has(q.id)); if(s.length) pool = s; }
  if(st.lastType){ const d = pool.filter(q => q.type !== st.lastType); if(d.length) pool = d; }   // change the format when re-asking
  const pref = typePref(e, c).filter(t => pool.some(q => q.type === t));
  if(pref.length > 1){                                                                  // weighted choice of format, favourite first
    const w = [6, 3, 1.5, 1].slice(0, pref.length); let r = Math.random() * w.reduce((a, b) => a + b, 0), t = pref[0];
    for(let i = 0; i < pref.length; i++){ r -= w[i]; if(r <= 0){ t = pref[i]; break; } }
    pool = pool.filter(q => q.type === t);
  }
  const t = q => (stats[q.id] && stats[q.id].t) || 0;
  const min = Math.min.apply(null, pool.map(t));                                        // least recently asked first
  pool = pool.filter(q => t(q) === min);
  return pool[Math.floor(Math.random() * pool.length)];
}
function prep(){
  const e = sess.queue[sess.i], c = cur().con[e.k], st = sess.st[e.k];
  const q = pickVariant(c, st, e);
  st.used.push(q.id); st.lastType = q.type;
  sess.cur = {q, e, done:false, ok:null, picked:null, typed:'', revealed:false,
    order: q.type === 'mc' ? shuffle(q.choices.map((_, i) => i)) : null};
}
// apply the result of the current question: record it and schedule a different-looking repeat if it was missed
function commit(){
  const c = sess.cur; if(!c || !c.done || c.committed) return;
  c.committed = true;
  const q = c.q, e = c.e, st = sess.st[e.k], ok = c.ok;
  const s = stats[q.id] || (stats[q.id] = {c:0, w:0, l:0, t:0});
  if(ok) s.c++; else s.w++; s.l = ok ? 1 : 0; s.t = Date.now(); store.set(K+'stats', stats);
  sess.log.push({q, ok, kind:e.kind, given:c.given});
  if(st.first === null) st.first = ok;
  sess.streak = ok ? sess.streak + 1 : 0;
  const rest = sess.queue.length - (sess.i + 1);
  if(!ok){
    st.miss++;
    mset(e.k, m => { m.b = 0; m.n++; m.w++; });
    // comes back after 2-4 other questions, as a different question about the same content
    if(sess.mode === 'learn') sess.queue.splice(sess.i + 1 + Math.min(2 + Math.floor(Math.random() * 3), rest), 0, {k:e.k, kind:'retry'});
  } else if(e.kind === 'first'){
    mset(e.k, m => { m.b = m.n === 0 ? 2 : Math.min(5, m.b + 1); m.n++; });
    sess.cleared++;
  } else if(e.kind === 'retry'){
    mset(e.k, m => { m.n++; });
    sess.queue.push({k:e.k, kind:'confirm'});
  } else {
    mset(e.k, m => { m.b = 1; m.n++; });
    sess.cleared++;
  }
}
const GREEK = {'α':'알파','β':'베타','γ':'감마','δ':'델타','ρ':'로','σ':'시그마','λ':'람다','μ':'마이크로'};
function norm(s){
  s = String(s).normalize('NFKC').toLowerCase().trim();
  s = s.replace(/[αβγδρσλμ]/g, ch => GREEK[ch]);
  s = s.replace(/([0-9a-z가-힣'′])[-‐‑–—](?=[0-9a-z가-힣])/g, '$1');
  s = s.replace(/[\s.·,;:'"`~!?()\[\]{}<>/\\’‘“”′]/g, '');
  return s;
}
function answersOf(q){
  const out = new Set();
  [q.answer].concat(q.alts || []).forEach(a => { a = String(a); out.add(norm(a)); const b = a.replace(/\([^)]*\)/g, ''); if(b.trim()) out.add(norm(b)); });
  out.delete('');
  return out;
}
function grade(ok){
  const c = sess.cur, q = c.q;
  c.done = true; c.ok = ok;
  c.given = q.type === 'mc' ? (c.picked == null ? '' : q.choices[c.picked]) : q.type === 'ox' ? (c.picked == null ? '' : c.picked ? 'O' : 'X') : c.typed;
  if(sess.mode === 'exam'){ next(); return; }
  renderQuiz();
  const fb = document.querySelector('.fb'); if(fb && fb.getBoundingClientRect().bottom > window.innerHeight - 90) fb.scrollIntoView({block:'center', behavior:'smooth'});
}
function answerText(q){
  if(q.type === 'mc') return q.choices[q.answer];
  if(q.tol != null) return q.answer + (q.unit ? ' ' + q.unit : '');
  if(q.type === 'ox') return q.answer ? 'O (맞는 설명)' : 'X (틀린 설명)';
  return q.answer;
}
function QT(q){ return q.raw ? q.q : esc(q.q); }
function CH(q, i){ return q.raw ? q.choices[i] : esc(q.choices[i]); }
function EX(q){ return q.raw ? q.exp : esc(q.exp); }
function EXTRA(q){ return (q.fig && typeof FIGM !== 'undefined' && FIGM[q.fig] ? '<div class="figbox">' + FIGM[q.fig] + '</div>' : '') + (q.tb || ''); }
function qHtml(q){ return QT(q).replace(/_{3,}/g, '<span class="blankbox"></span>'); }
function renderQuiz(){
  view = 'quiz';
  const c = sess.cur, q = c.q, e = c.e, exam = sess.mode === 'exam';
  const left = sess.queue.length - sess.i - (c.done ? 1 : 0);
  const waiting = sess.queue.slice(sess.i + 1).filter(x => x.kind !== 'first').length;
  let h = `<div class="top">
    <button class="icon" data-a="exit" aria-label="그만하기">✕</button>
    <div class="prog"><div class="prog-n">${exam ? `<span>모의고사 ${sess.i + 1} / ${sess.total}</span><span>채점은 끝난 뒤에</span>`
      : `<span>통과 ${sess.cleared} / ${sess.total}</span><span>${sess.streak >= 3 ? `연속 정답 ${sess.streak} · ` : ''}남은 문제 ${left}${waiting ? ` · 다시 낼 것 ${waiting}` : ''}</span>`}</div>
      <div class="track"><div class="fill" style="width:${100 * (exam ? sess.i : sess.cleared) / sess.total}%"></div></div></div>
    <button class="icon star ${stars.has(q.id) ? 'on' : ''}" data-a="star" aria-label="별표">${stars.has(q.id) ? '★' : '☆'}</button>
  </div>`;
  h += `<div class="meta"><span class="tag">${TNAME[q.type]}</span>${e.kind === 'retry' ? '<span class="tag again">틀렸던 내용 · 다른 문제</span>' : e.kind === 'confirm' ? '<span class="tag again">마지막 확인</span>' : ''}<span class="where">${esc(cur().secname[q.sec] || '')} › ${esc(q.sub)}</span></div>`;
  h += `<p class="q">${qHtml(q)}</p>${EXTRA(q)}`;

  if(q.type === 'mc'){
    h += `<div class="opts">` + c.order.map((ci, n) => {
      let cls = '';
      if(c.done){ cls = ci === q.answer ? 'right' : ci === c.picked ? 'wrong' : 'dim'; }
      return `<button class="opt ${cls}" data-a="pick" data-i="${ci}" ${c.done ? 'disabled' : ''}><span class="n">${n + 1}</span><span>${CH(q, ci)}</span></button>`;
    }).join('') + `</div>`;
  } else if(q.type === 'ox'){
    h += `<div class="ox">` + [true, false].map(v => {
      let cls = '';
      if(c.done){ cls = v === q.answer ? 'right' : v === c.picked ? 'wrong' : 'dim'; }
      return `<button class="opt ${cls}" data-a="ox" data-v="${v ? 1 : 0}" ${c.done ? 'disabled' : ''}>${v ? 'O' : 'X'}</button>`;
    }).join('') + `</div>`;
  } else if(!c.done){
    if(cfg.sa === 'self' && !exam){
      if(!c.revealed) h += `<p class="muted">답을 머릿속으로 떠올린 다음 정답을 확인하세요.</p>`;
      else h += `<div class="fb plain"><div class="mine">정답</div><div class="ans">${esc(q.answer)}</div>${q.exp ? `<div class="exp">${EX(q)}</div>` : ''}</div>`;
    } else {
      h += `<input class="inp" id="inp" type="text" inputmode="text" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" enterkeyhint="done" placeholder="답 입력" value="${esc(c.typed)}">`;
    }
  }

  if(c.done){
    const sa = q.type === 'sa' || q.type === 'blank';
    h += `<div class="fb ${c.ok ? 'ok' : 'no'}"><div class="v">${c.ok ? '정답' : '오답'}</div>`;
    h += `<div class="ans">${q.raw ? answerText(q) : esc(answerText(q))}</div>`;
    if(sa && c.typed) h += `<div class="mine">내가 쓴 답: ${esc(c.typed)}</div>`;
    if(sa && (q.alts || []).length) h += `<div class="mine">인정되는 다른 표기: ${esc(q.alts.join(', '))}</div>`;
    if(q.exp) h += `<div class="exp">${EX(q)}</div>`;
    if(q.src) h += `<div class="src">출처: ${esc(q.src)}</div>`;
    if(!exam){
      if(!c.ok) h += `<div class="later">이 내용은 조금 뒤에 다른 문제로 다시 나옵니다.</div>`;
      else if(e.kind === 'retry') h += `<div class="later">끝나기 전에 한 번 더 확인합니다.</div>`;
    }
    if(sa) h += `<button class="over" data-a="over">${c.ok ? '사실 틀렸음 → 오답으로 바꾸기' : '내 답도 맞음 → 정답으로 바꾸기'}</button>`;
    h += `</div>`;
  }

  let bar = '';
  if(c.done) bar = `<button class="btn" data-a="next">${sess.i + 1 < sess.queue.length || (!c.ok && !exam) || (c.ok && e.kind === 'retry') ? '다음 문제' : '결과 보기'}</button>`;
  else if(q.type === 'sa' || q.type === 'blank'){
    if(cfg.sa === 'self' && !exam) bar = c.revealed
      ? `<button class="btn ghost" data-a="self" data-v="0">틀렸음</button><button class="btn" data-a="self" data-v="1">맞았음</button>`
      : `<button class="btn" data-a="reveal">정답 보기</button>`;
    else bar = `<button class="btn ghost small" data-a="giveup">모르겠음</button><button class="btn" data-a="check">확인</button>`;
  } else bar = `<button class="btn ghost" data-a="giveup">${exam ? '모르겠음 · 넘어가기' : '모르겠음 · 정답 보기'}</button>`;
  h += `<div class="bar"><div class="bar-in">${bar}</div></div>`;
  setHTML(h);
  const inp = document.getElementById('inp');
  if(inp){
    inp.addEventListener('input', () => { c.typed = inp.value; });
    inp.addEventListener('keydown', ev => { if(ev.key === 'Enter' && !ev.isComposing){ ev.preventDefault(); check(); } });
    try{ inp.focus({preventScroll:true}); }catch(err){}
  }
}
function check(){
  const c = sess.cur;
  const inp = document.getElementById('inp'); if(inp){ c.typed = inp.value; inp.blur(); }
  if(!c.typed.trim()) return;
  if(c.q.tol != null){ const v = parseFloat(String(c.typed).replace(/[−–]/g,'-').replace(/,/g,'').replace(/[^0-9eE.+\-]/g,'')); grade(!isNaN(v) && Math.abs(v - c.q.answer) <= c.q.tol + 1e-9); }
  else grade(answersOf(c.q).has(norm(c.typed)));
}
function next(){
  commit();
  if(sess.i + 1 < sess.queue.length){ sess.i++; prep(); renderQuiz(); window.scrollTo(0, 0); }
  else renderResult();
}

/* ---------- RESULT ---------- */
function renderResult(){
  view = 'result';
  if(sess.mode === 'exam'){
    const n = sess.log.length, right = sess.log.filter(x => x.ok).length, wr = sess.log.filter(x => !x.ok);
    let h = `<div class="score"><div class="muted">모의고사 점수</div><div class="big">${right}<small> / ${n}</small></div>
      <div class="muted">정답률 ${n ? Math.round(100 * right / n) : 0}%${n < sess.total ? ` · ${sess.total - n}문제는 풀지 않음` : ''}</div></div>`;
    if(wr.length){
      h += `<div class="card"><h2>틀린 문제 ${wr.length}개</h2>` + wr.map(x =>
        `<div class="wl"><div class="wq">${qHtml(x.q)}</div><div class="we">내 답: ${esc(x.given || '(안 씀)')}</div><div class="wa">${x.q.raw ? answerText(x.q) : esc(answerText(x.q))}</div>${x.q.exp ? `<div class="we">${EX(x.q)}</div>` : ''}</div>`).join('') + `</div>`;
    } else if(n){ h += `<div class="card" style="text-align:center">틀린 문제가 없습니다.</div>`; }
    sess.missed = [...new Set(wr.map(x => x.q.k))];
    h += `<div class="stack">`;
    if(wr.length) h += `<button class="btn" data-a="retry">틀린 ${sess.missed.length}가지 반복 학습으로 익히기</button>`;
    h += `<button class="btn ${wr.length ? 'ghost' : ''}" data-a="again">모의고사 한 번 더</button><button class="btn ghost" data-a="home">처음 화면으로</button></div>`;
    setHTML(h); window.scrollTo(0, 0);
    return;
  }
  const ks = Object.keys(sess.st).filter(k => sess.st[k].first !== null);
  const firstOk = ks.filter(k => sess.st[k].first === true).length;
  const missed = ks.filter(k => sess.st[k].miss > 0);
  const wrongs = sess.log.filter(x => !x.ok);
  let h = `<div class="score"><div class="muted">처음에 바로 맞힌 내용</div><div class="big">${firstOk}<small> / ${ks.length}</small></div>
    <div class="muted">푼 문제 ${sess.log.length}개 · 통과 ${sess.cleared}가지${ks.length < sess.total ? ` · ${sess.total - ks.length}가지는 풀지 않음` : ''}</div></div>`;
  if(wrongs.length){
    h += `<div class="card"><h2>틀렸던 문제 ${wrongs.length}개</h2>` + wrongs.map(x =>
      `<div class="wl"><div class="wq">${qHtml(x.q)}</div><div class="wa">${x.q.raw ? answerText(x.q) : esc(answerText(x.q))}</div>${x.q.exp ? `<div class="we">${EX(x.q)}</div>` : ''}</div>`).join('') + `</div>`;
  } else if(ks.length){ h += `<div class="card" style="text-align:center">틀린 문제가 없습니다.</div>`; }
  h += `<div class="stack">`;
  if(missed.length) h += `<button class="btn" data-a="retry">틀렸던 ${missed.length}가지 다시 학습</button>`;
  h += `<button class="btn ${missed.length ? 'ghost' : ''}" data-a="again">같은 조건으로 이어서 풀기</button><button class="btn ghost" data-a="home">처음 화면으로</button></div>`;
  sess.missed = missed;
  setHTML(h); window.scrollTo(0, 0);
}

/* ---------- GAMES (same question bank, quick-fire formats; misses feed the memory model) ---------- */
let game = null, timer = null;
function stopTimer(){ if(timer){ clearInterval(timer); timer = null; } }
function gameRecord(q, ok){
  const s = stats[q.id] || (stats[q.id] = {c:0, w:0, l:0, t:0});
  if(ok) s.c++; else s.w++; s.l = ok ? 1 : 0; s.t = Date.now(); store.set(K+'stats', stats);
  if(ok) mset(q.k, m => { if(m.n === 0) m.b = 1; m.n++; });
  else mset(q.k, m => { m.b = 0; m.n++; m.w++; });
}
function setBest(key, val, lower){
  const b = store.get(K+'best', {}), old = b[key];
  const better = old == null || (lower ? val < old : val > old);
  if(better){ b[key] = val; store.set(K+'best', b); }
  return {old, better};
}
// speed OX: 60 seconds, as many as possible; a miss pauses the clock and shows the explanation
function startSpeed(){
  const qs = shuffle(cur().bank.filter(q => q.type === 'ox' && inScope(q)));
  if(!qs.length) return;
  const weak = q => (mast[q.k] && mast[q.k].n > 0 && mast[q.k].b === 0) ? 0 : 1;
  qs.sort((a, b) => weak(a) - weak(b));
  game = {type:'speed', qs, i:0, score:0, combo:0, maxCombo:0, wrong:[], left:60, fb:false};
  stopTimer();
  timer = setInterval(() => {
    if(view !== 'speed'){ stopTimer(); return; }
    if(game.fb) return;
    game.left -= 0.1;
    const bar = document.getElementById('tbar'), num = document.getElementById('tnum');
    if(bar) bar.style.width = Math.max(0, 100 * game.left / 60) + '%';
    if(num) num.textContent = Math.max(0, Math.ceil(game.left)) + '초';
    if(game.left <= 0) endGame();
  }, 100);
  renderSpeed(); window.scrollTo(0, 0);
}
function renderSpeed(){
  view = 'speed';
  const g = game, q = g.qs[g.i % g.qs.length];
  let h = `<div class="top"><button class="icon" data-a="quit" aria-label="그만하기">✕</button>
    <div class="prog"><div class="prog-n"><span id="tnum">${Math.max(0, Math.ceil(g.left))}초</span><span>${g.combo >= 2 ? `연속 ${g.combo} · ` : ''}점수 ${g.score}</span></div>
    <div class="track"><div class="fill" id="tbar" style="width:${Math.max(0, 100 * g.left / 60)}%;transition:none"></div></div></div></div>`;
  h += `<div class="meta"><span class="tag">스피드 OX</span><span class="where">${esc(cur().secname[q.sec] || '')} › ${esc(q.sub)}</span></div>`;
  h += `<p class="q">${QT(q)}</p>`;
  h += `<div class="ox">` + [true, false].map(v => {
    const cls = g.fb ? (v === q.answer ? 'right' : 'wrong') : '';
    return `<button class="opt ${cls}" data-a="sox" data-v="${v ? 1 : 0}" ${g.fb ? 'disabled' : ''}>${v ? 'O' : 'X'}</button>`;
  }).join('') + `</div>`;
  if(g.fb){
    h += `<div class="fb no"><div class="v">오답 · 시간 멈춤</div><div class="ans">${q.raw ? answerText(q) : esc(answerText(q))}</div>${q.exp ? `<div class="exp">${EX(q)}</div>` : ''}</div>`;
    h += `<div class="bar"><div class="bar-in"><button class="btn" data-a="scont">계속</button></div></div>`;
  }
  setHTML(h);
}
// matching: 4 questions and their 4 answers per round, 5 rounds
function matchPool(){
  const out = [];
  cur().clist.forEach(c => { const q = c.qs.find(x => (x.type === 'sa' || x.type === 'blank') && inScope(x) && typeof x.answer === 'string' && x.tol == null && x.answer.length <= 18 && x.q.length <= 80); if(q) out.push(q); });
  return out;
}
function startMatch(){
  const pool = shuffle(matchPool());
  if(pool.length < 4) return;
  game = {type:'match', pool, round:0, rounds:5, miss:0, pairs:0, t0:Date.now(), wrong:[], finished:false, cards:null};
  stopTimer();
  timer = setInterval(() => {
    if(view !== 'match'){ stopTimer(); return; }
    const el = document.getElementById('mtime'); if(el) el.textContent = Math.round((Date.now() - game.t0) / 1000) + '초';
  }, 500);
  nextRound(); window.scrollTo(0, 0);
}
function nextRound(){
  const g = game;
  if(g.round >= g.rounds){ g.finished = true; endGame(); return; }
  const pick = [], used = new Set();
  while(pick.length < 4 && g.pool.length){                       // no two cards in a round may share an acceptable answer
    const q = g.pool.pop(), all = [...answersOf(q)];
    if(all.some(a => used.has(a))) continue;
    all.forEach(a => used.add(a)); pick.push(q);
  }
  if(pick.length < 2){ endGame(); return; }
  g.round++;
  g.cards = {qs:pick, order:shuffle(pick.map((_, i) => i)), matched:new Set(), selQ:null, selA:null, bad:null};
  renderMatch();
}
function renderMatch(){
  view = 'match';
  const g = game, cd = g.cards;
  let h = `<div class="top"><button class="icon" data-a="quit" aria-label="그만하기">✕</button>
    <div class="prog"><div class="prog-n"><span>${g.round} / ${g.rounds}판</span><span>실수 ${g.miss} · <span id="mtime">${Math.round((Date.now() - g.t0) / 1000)}초</span></span></div>
    <div class="track"><div class="fill" style="width:${100 * ((g.round - 1) + cd.matched.size / cd.qs.length) / g.rounds}%"></div></div></div></div>`;
  h += `<p class="muted" style="margin:2px 0 10px">문제를 누르고 알맞은 답을 누르세요.</p><div class="mqs">`;
  cd.qs.forEach((q, i) => {
    const cls = cd.matched.has(i) ? 'gone' : cd.bad && cd.bad.q === i ? 'bad' : cd.selQ === i ? 'sel' : '';
    h += `<button class="mq ${cls}" data-a="mq" data-i="${i}" ${cd.matched.has(i) ? 'disabled' : ''}>${qHtml(q)}</button>`;
  });
  h += `</div><div class="mas">`;
  cd.order.forEach(i => {
    const cls = cd.matched.has(i) ? 'gone' : cd.bad && cd.bad.a === i ? 'bad' : cd.selA === i ? 'sel' : '';
    h += `<button class="ma ${cls}" data-a="ma" data-i="${i}" ${cd.matched.has(i) ? 'disabled' : ''}>${esc(cd.qs[i].answer)}</button>`;
  });
  h += `</div>`;
  setHTML(h);
}
function matchTry(){
  const g = game, cd = g.cards;
  const qi = cd.selQ, ai = cd.selA; cd.selQ = cd.selA = null;
  if(qi === ai){
    cd.matched.add(qi); g.pairs++; gameRecord(cd.qs[qi], true);
    renderMatch();
    if(cd.matched.size === cd.qs.length) setTimeout(() => { if(view === 'match' && game === g && g.cards === cd) nextRound(); }, 350);
  } else {
    g.miss++; g.wrong.push(cd.qs[qi]); gameRecord(cd.qs[qi], false);
    const bad = cd.bad = {q:qi, a:ai};
    renderMatch();
    setTimeout(() => { if(view === 'match' && game === g && cd.bad === bad){ cd.bad = null; renderMatch(); } }, 600);
  }
}
function endGame(){
  stopTimer(); view = 'gameover';
  const g = game; let h = '';
  if(g.type === 'speed'){
    const r = setBest('speed_' + cfg.subj, g.score, false);
    h += `<div class="score"><div class="muted">스피드 OX · 60초</div><div class="big">${g.score}<small> 점</small></div>
      <div class="muted">${r.old == null ? '첫 기록' : r.better ? `최고 기록 경신 (이전 ${r.old}점)` : `최고 기록 ${r.old}점`} · 최다 연속 ${g.maxCombo}</div></div>`;
  } else {
    const sec = Math.round((Date.now() - g.t0) / 1000);
    let line = `${g.pairs}쌍 · 실수 ${g.miss}번`;
    if(g.finished){ const r = setBest('match_' + cfg.subj, sec, true); line += ' · ' + (r.old == null ? '첫 기록' : r.better ? `최고 기록 경신 (이전 ${r.old}초)` : `최고 기록 ${r.old}초`); }
    else line += ' · 끝까지 하지 않아 기록되지 않음';
    h += `<div class="score"><div class="muted">짝 맞추기</div><div class="big">${sec}<small> 초</small></div><div class="muted">${line}</div></div>`;
  }
  const wr = [], ids = new Set();
  g.wrong.forEach(q => { if(!ids.has(q.id)){ ids.add(q.id); wr.push(q); } });
  if(wr.length) h += `<div class="card"><h2>틀린 것 ${wr.length}개</h2>` + wr.map(q =>
    `<div class="wl"><div class="wq">${qHtml(q)}</div><div class="wa">${q.raw ? answerText(q) : esc(answerText(q))}</div>${q.exp ? `<div class="we">${EX(q)}</div>` : ''}</div>`).join('') + `</div>`;
  else h += `<div class="card" style="text-align:center">틀린 것이 없습니다.</div>`;
  g.missed = [...new Set(wr.map(q => q.k))];
  h += `<div class="stack">`;
  if(wr.length) h += `<button class="btn" data-a="glearn">틀린 ${g.missed.length}가지 반복 학습으로 익히기</button>`;
  h += `<button class="btn ${wr.length ? 'ghost' : ''}" data-a="gagain">한 판 더</button><button class="btn ghost" data-a="home">처음 화면으로</button></div>`;
  setHTML(h); window.scrollTo(0, 0);
}

/* ---------- EVENTS ---------- */
app.addEventListener('click', ev => {
  const b = ev.target.closest('[data-a]'); if(!b || b.disabled) return;
  const a = b.dataset.a;
  if(view === 'home'){
    const S = cur();
    if(a === 'all'){ SEL[cfg.subj] = new Set(S.allkeys); }
    else if(a === 'none'){ SEL[cfg.subj] = new Set(); }
    else if(a === 'subj'){ cfg.subj = b.dataset.id; openSecs.clear(); }
    else if(a === 'sec'){ const s = S.idx.find(x => x.id === b.dataset.id); const allOn = s.subs.every(x => sel().has(x.key)); s.subs.forEach(x => allOn ? sel().delete(x.key) : sel().add(x.key)); }
    else if(a === 'open'){ const id = b.dataset.id; openSecs.has(id) ? openSecs.delete(id) : openSecs.add(id); }
    else if(a === 'sub'){ const k = b.dataset.k; sel().has(k) ? sel().delete(k) : sel().add(k); }
    else if(a === 'type'){ const t = b.dataset.id; selTypes.has(t) ? selTypes.delete(t) : selTypes.add(t); }
    else if(a === 'cfg'){ const key = b.dataset.key; cfg[key] = key === 'count' ? +b.dataset.v : b.dataset.v; }
    else if(a === 'reset'){
      if(confirm(S.name + ' 과목의 암기 상태, 정답/오답 기록, ★ 표시를 모두 지울까요?')){
        S.clist.forEach(c => delete mast[c.k]); S.bank.forEach(q => { delete stats[q.id]; stars.delete(q.id); });
        store.set(K+'stats', stats); store.set(K+'mast', mast); store.set(K+'stars', [...stars]);
      }
    }
    else if(a === 'study'){ saveCfg(); renderStudy(); window.scrollTo(0, 0); return; }
    else if(a === 'start'){ saveCfg(); if(cfg.mode === 'speed') startSpeed(); else if(cfg.mode === 'match') startMatch(); else start(); return; }
    saveCfg(); renderHome(); return;
  }
  if(view === 'study'){
    if(a === 'home'){ renderHome(); window.scrollTo(0, 0); }
    else if(a === 'hide'){ hideAns = !hideAns; const y = window.scrollY; renderStudy(); window.scrollTo(0, y); }
    else if(a === 'fact'){ b.classList.toggle('show'); }
    else if(a === 'sf'){ studyF = b.dataset.v; renderStudy(); window.scrollTo(0, 0); }
    return;
  }
  if(view === 'speed'){
    const g = game, q = g.qs[g.i % g.qs.length];
    if(a === 'quit'){ endGame(); }
    else if(a === 'sox' && !g.fb){
      const ok = (b.dataset.v === '1') === q.answer; gameRecord(q, ok);
      if(ok){ g.score++; g.combo++; g.maxCombo = Math.max(g.maxCombo, g.combo); g.i++; }
      else { g.combo = 0; g.wrong.push(q); g.fb = true; }
      renderSpeed();
    }
    else if(a === 'scont'){ g.fb = false; g.i++; renderSpeed(); window.scrollTo(0, 0); }
    return;
  }
  if(view === 'match'){
    const cd = game.cards;
    if(a === 'quit'){ endGame(); return; }
    if(a === 'mq'){ cd.bad = null; cd.selQ = cd.selQ === +b.dataset.i ? null : +b.dataset.i; }
    else if(a === 'ma'){ cd.bad = null; cd.selA = cd.selA === +b.dataset.i ? null : +b.dataset.i; }
    else return;
    if(cd.selQ !== null && cd.selA !== null) matchTry(); else renderMatch();
    return;
  }
  if(view === 'gameover'){
    if(a === 'glearn'){ start(shuffle(game.missed.map(k => cur().con[k])), 'learn'); }
    else if(a === 'gagain'){ if(game.type === 'speed') startSpeed(); else startMatch(); }
    else if(a === 'home'){ renderHome(); window.scrollTo(0, 0); }
    return;
  }
  if(view === 'quiz'){
    const c = sess.cur, q = c.q;
    if(a === 'exit'){ commit(); if(sess.log.length) renderResult(); else renderHome(); }
    else if(a === 'star'){ stars.has(q.id) ? stars.delete(q.id) : stars.add(q.id); store.set(K+'stars', [...stars]); renderQuiz(); }
    else if(a === 'pick' && !c.done){ c.picked = +b.dataset.i; grade(c.picked === q.answer); }
    else if(a === 'ox' && !c.done){ c.picked = b.dataset.v === '1'; grade(c.picked === q.answer); }
    else if(a === 'check'){ check(); }
    else if(a === 'giveup' && !c.done){ const inp = document.getElementById('inp'); if(inp) inp.blur(); c.typed = ''; grade(false); }
    else if(a === 'reveal'){ c.revealed = true; renderQuiz(); }
    else if(a === 'self'){ grade(b.dataset.v === '1'); }
    else if(a === 'over' && !c.committed){ c.ok = !c.ok; renderQuiz(); }
    else if(a === 'next'){ next(); }
    return;
  }
  if(view === 'result'){
    if(a === 'retry'){ start(shuffle(sess.missed.map(k => cur().con[k])), 'learn'); }
    else if(a === 'again'){ if(!start()){ renderHome(); window.scrollTo(0, 0); } }
    else if(a === 'home'){ renderHome(); window.scrollTo(0, 0); }
  }
});
document.addEventListener('keydown', ev => {
  if(view !== 'quiz' || !sess) return;
  if(ev.target && ev.target.tagName === 'INPUT') return;
  const c = sess.cur, q = c.q;
  if(c.done && (ev.key === 'Enter' || ev.key === ' ')){ ev.preventDefault(); next(); return; }
  if(!c.done && q.type === 'mc' && /^[1-4]$/.test(ev.key)){ c.picked = c.order[+ev.key - 1]; grade(c.picked === q.answer); }
  if(!c.done && q.type === 'ox' && /^[oOxX]$/.test(ev.key)){ c.picked = /o/i.test(ev.key); grade(c.picked === q.answer); }
});
renderHome();
