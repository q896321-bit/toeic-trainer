// ===== TTS Module =====
const TTS = {
    supported: "speechSynthesis" in window,
    rate: 0.9,
    speak(text, lang = "en-US", rate = null) {
        if (!this.supported) return null;
        this.stop();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = lang; u.rate = rate || this.rate; u.pitch = 1;
        const voices = speechSynthesis.getVoices();
        const v = voices.find(v => v.lang.startsWith("en-US")) || voices.find(v => v.lang.startsWith("en"));
        if (v) u.voice = v;
        speechSynthesis.speak(u);
        return u;
    },
    speakSlow(text) { return this.speak(text, "en-US", 0.6); },
    stop() { if (this.supported) speechSynthesis.cancel(); },
    btn(text, slow) {
        const b = document.createElement("button");
        b.className = "audio-btn";
        b.innerHTML = slow ? "🐢" : "🔊";
        b.title = slow ? "慢速播放" : "播放發音";
        b.addEventListener("click", e => {
            e.stopPropagation();
            b.classList.add("playing");
            const u = slow ? this.speakSlow(text) : this.speak(text);
            if (u) { u.onend = () => b.classList.remove("playing"); u.onerror = () => b.classList.remove("playing"); }
        });
        return b;
    }
};
if (TTS.supported) { speechSynthesis.getVoices(); speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices(); }

// ===== State =====
const STATE_KEY = "toeic_trainer_state";
const WRONG_KEY = "toeic_wrong_answers";

function loadState() { const s = localStorage.getItem(STATE_KEY); return s ? JSON.parse(s) : null; }
function saveState(s) { localStorage.setItem(STATE_KEY, JSON.stringify(s)); }
function clearState() { localStorage.removeItem(STATE_KEY); }
function loadWrong() { const w = localStorage.getItem(WRONG_KEY); return w ? JSON.parse(w) : []; }
function saveWrong(w) { localStorage.setItem(WRONG_KEY, JSON.stringify(w)); }
function addWrong(item) { const w = loadWrong(); w.push({ ...item, date: new Date().toISOString() }); saveWrong(w); }

// ===== Session tracking for daily report =====
let sessionStats = { correct: 0, wrong: 0, startTime: null, categories: {} };

function resetSession() {
    sessionStats = { correct: 0, wrong: 0, startTime: Date.now(), categories: { listening: {c:0,w:0}, reading: {c:0,w:0}, grammar: {c:0,w:0}, vocab: {c:0,w:0} } };
}

function recordAnswer(category, correct, wrongItem) {
    if (correct) {
        sessionStats.correct++;
        if (sessionStats.categories[category]) sessionStats.categories[category].c++;
    } else {
        sessionStats.wrong++;
        if (sessionStats.categories[category]) sessionStats.categories[category].w++;
        if (wrongItem) addWrong({ ...wrongItem, category });
    }
}

// ===== Navigation =====
function showPage(id) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.getElementById(id).classList.add("active");
    document.querySelectorAll(".nav-btn").forEach(b => {
        b.classList.toggle("active", b.dataset.page === id);
    });
    window.scrollTo(0, 0);
    TTS.stop();
}

// ===== Timer Module =====
function createTimer(displayId, toggleId) {
    let interval = null, seconds = 0, running = false;
    const display = document.getElementById(displayId);
    const toggle = document.getElementById(toggleId);

    function update() { const m = Math.floor(seconds/60); const s = seconds%60; display.textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`; }

    toggle.onclick = () => {
        if (running) { clearInterval(interval); toggle.innerHTML = "⏱️ 繼續"; running = false; }
        else { interval = setInterval(() => { seconds++; update(); }, 1000); toggle.innerHTML = "⏸ 暫停"; running = true; }
    };

    return { getSeconds: () => seconds, reset() { clearInterval(interval); seconds = 0; running = false; update(); toggle.innerHTML = "⏱️ 開始計時"; } };
}

// ===== Setup =====
let selectedTarget = null, selectedDays = null;

function initSetup() {
    document.querySelectorAll("#target-score-group .option-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll("#target-score-group .option-btn").forEach(b => b.classList.remove("selected"));
            btn.classList.add("selected");
            selectedTarget = parseInt(btn.dataset.value);
            checkReady();
        });
    });
    document.querySelectorAll("#training-days-group .option-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll("#training-days-group .option-btn").forEach(b => b.classList.remove("selected"));
            btn.classList.add("selected");
            selectedDays = parseInt(btn.dataset.value);
            checkReady();
        });
    });
    document.getElementById("start-btn").addEventListener("click", startTraining);
}

function checkReady() { document.getElementById("start-btn").disabled = !(selectedTarget && selectedDays); }

function startTraining() {
    const cL = parseInt(document.getElementById("current-listening").value) || 0;
    const cR = parseInt(document.getElementById("current-reading").value) || 0;
    const state = {
        targetScore: selectedTarget, totalDays: selectedDays,
        currentListening: cL, currentReading: cR, currentTotal: cL + cR,
        completedDays: [], startDate: new Date().toISOString(),
        unlockedAchievements: [], bestAccuracy: 0, wrongReviewed: 0, bestWPM: 0,
        plan: generatePlan(selectedTarget, selectedDays, cL, cR)
    };
    saveState(state);
    document.getElementById("bottom-nav").classList.remove("hidden");
    loadDashboard(state);
}

// ===== Plan Generation =====
function analyzeWeakness(target, cL, cR) {
    const half = target / 2, lGap = half - cL, rGap = half - cR, total = lGap + rGap;
    if (total <= 0) return { lr: 0.5, rr: 0.5, focus: "balanced", msg: "已達目標！挑戰更高分。" };
    const lr = Math.max(0.25, Math.min(0.75, lGap / total)), rr = 1 - lr;
    let focus, msg;
    if (lGap > rGap * 1.5) { focus = "listening"; msg = `聽力差距較大（差${lGap}分），加強聽力，比重 ${Math.round(lr*100)}%：${Math.round(rr*100)}%。`; }
    else if (rGap > lGap * 1.5) { focus = "reading"; msg = `閱讀差距較大（差${rGap}分），加強閱讀，比重 ${Math.round(lr*100)}%：${Math.round(rr*100)}%。`; }
    else { focus = "balanced"; msg = "聽力與閱讀差距相近，均衡訓練。"; }
    return { lr, rr, focus, msg };
}

function generatePlan(target, days, cL, cR) {
    const a = analyzeWeakness(target, cL, cR);
    const levels = []; if (target>=450) levels.push(450); if (target>=550) levels.push(550); if (target>=650) levels.push(650); if (target>=750) levels.push(750);
    const plan = [];
    for (let i = 0; i < days; i++) {
        const phase = i < days*0.3 ? "foundation" : i < days*0.7 ? "intensive" : "review";
        const d = i + 1;
        const vL = levels[i % levels.length], vP = TOEIC_DATA.vocabulary[vL], vs = (i*4)%vP.length;
        const vocab = []; for (let v=0;v<4;v++) vocab.push(vP[(vs+v)%vP.length]);
        const gL = levels[Math.floor(i/3)%levels.length], gP = TOEIC_DATA.grammar[gL];
        const grammar = gP[Math.floor(i/3)%gP.length];
        const tL = levels[Math.floor(i/2)%levels.length];
        const lT = TOEIC_DATA.listeningTips[tL], rT = TOEIC_DATA.readingTips[tL];
        const rEL = levels[Math.floor(i/4)%levels.length], rEP = TOEIC_DATA.readingExercises[rEL];
        const lEL = levels[Math.floor(i/3)%levels.length], lEP = TOEIC_DATA.listeningExercises[lEL];
        const title = phase === "foundation" ? `基礎建構 Day ${d}` : phase === "intensive" ? `強化訓練 Day ${d}` : `衝刺複習 Day ${d}`;
        plan.push({ day: d, phase, title, description: "單字+文法+聽力+閱讀",
            vocab, vocabLevel: vL, grammar, grammarLevel: gL,
            listenTip: lT[i%lT.length], readTip: rT[i%rT.length],
            readExercise: rEP[i%rEP.length], listenExercise: lEP[i%lEP.length],
        });
    }
    plan.analysisMessage = a.msg; plan.analysisFocus = a.focus;
    return plan;
}

// ===== Dashboard =====
function loadDashboard(state) {
    showPage("dashboard-page");
    document.getElementById("bottom-nav").classList.remove("hidden");
    document.getElementById("stat-target").textContent = state.targetScore + " 分";
    const done = state.completedDays.length;
    document.getElementById("stat-progress").textContent = `${done}/${state.totalDays}`;
    document.getElementById("stat-streak").textContent = calcStreak(state) + " 天";
    document.getElementById("progress-bar").style.width = (done/state.totalDays*100) + "%";

    const focus = state.plan.analysisFocus || "balanced";
    let tags = focus === "listening" ? '<span class="analysis-tag tag-listening">重點：聽力</span>'
        : focus === "reading" ? '<span class="analysis-tag tag-reading">重點：閱讀</span>'
        : '<span class="analysis-tag tag-listening">聽力</span><span class="analysis-tag tag-reading">閱讀</span>';
    tags += '<span class="analysis-tag tag-vocab">單字</span><span class="analysis-tag tag-grammar">文法</span>';
    document.getElementById("analysis-content").innerHTML = `<p>${state.plan.analysisMessage||""}</p><div style="margin-top:8px">${tags}</div>`;

    const list = document.getElementById("daily-list"); list.innerHTML = "";
    const next = done + 1;
    state.plan.forEach(dp => {
        if (!dp || !dp.day) return;
        const comp = state.completedDays.includes(dp.day), curr = dp.day===next, lock = dp.day>next;
        const el = document.createElement("div");
        el.className = `day-item${comp?" completed":""}${curr?" current":""}${lock?" locked":""}`;
        el.innerHTML = `<div class="day-num">${comp?"✓":dp.day}</div><div class="day-info"><div class="day-title">${dp.title}</div><div class="day-desc">${dp.description}</div></div><div class="day-status">${comp?"":curr?"→":"🔒"}</div>`;
        if (!lock) el.addEventListener("click", () => openTraining(state, dp));
        list.appendChild(el);
    });

    document.getElementById("reset-btn").onclick = () => {
        if (confirm("確定重新設定？進度會清除。")) {
            clearState(); selectedTarget = null; selectedDays = null;
            document.querySelectorAll(".option-btn").forEach(b=>b.classList.remove("selected"));
            document.getElementById("current-listening").value = "";
            document.getElementById("current-reading").value = "";
            document.getElementById("start-btn").disabled = true;
            document.getElementById("bottom-nav").classList.add("hidden");
            showPage("setup-page");
        }
    };
}

// ===== Daily Training =====
let dayTimer;
function openTraining(state, dp) {
    showPage("training-page");
    resetSession();
    if (dayTimer) dayTimer.reset();
    dayTimer = createTimer("timer-display", "timer-toggle");

    document.getElementById("training-day-title").textContent = dp.title;
    const c = document.getElementById("training-content"); c.innerHTML = "";

    c.appendChild(buildVocab(dp));
    c.appendChild(buildListening(dp));
    c.appendChild(buildGrammar(dp));
    const lt = document.createElement("div"); lt.className = "training-section"; lt.innerHTML = `<h3>💡 聽力技巧</h3><div class="tip-box">${dp.listenTip}</div>`; c.appendChild(lt);
    c.appendChild(buildReading(dp));
    const rt = document.createElement("div"); rt.className = "training-section"; rt.innerHTML = `<h3>💡 閱讀技巧</h3><div class="tip-box">${dp.readTip}</div>`; c.appendChild(rt);
    setupQuiz(c);

    const btn = document.getElementById("complete-day-btn");
    const comp = state.completedDays.includes(dp.day);
    btn.textContent = comp ? "✓ 已完成" : "完成今日訓練";
    btn.disabled = comp; btn.style.background = comp ? "var(--success)" : "";

    btn.onclick = () => {
        if (!state.completedDays.includes(dp.day)) {
            state.completedDays.push(dp.day);
            const total = sessionStats.correct + sessionStats.wrong;
            const acc = total > 0 ? Math.round(sessionStats.correct / total * 100) : 0;
            if (acc > (state.bestAccuracy||0)) state.bestAccuracy = acc;
            checkAchievements(state);
            saveState(state);
            btn.textContent = "✓ 已完成"; btn.disabled = true; btn.style.background = "var(--success)";
            showDailyReport(acc, dayTimer.getSeconds());
        }
    };

    document.getElementById("back-btn").onclick = () => { TTS.stop(); loadDashboard(state); };
}

// --- Vocab ---
function buildVocab(dp) {
    const s = document.createElement("div"); s.className = "training-section";
    s.innerHTML = `<h3>📖 單字練習（${dp.vocabLevel} 分級）</h3><p class="section-hint">點擊卡片翻面 ｜ 🔊 發音 ｜ 🐢 慢速</p>`;
    const g = document.createElement("div"); g.className = "vocab-grid";
    dp.vocab.forEach(v => {
        const card = document.createElement("div"); card.className = "vocab-card";
        card.innerHTML = `<div class="vocab-emoji">${v.emoji}</div><div class="word">${v.word}</div><div class="meaning">${v.meaning}</div><div class="vocab-image-hint">${v.image}</div>`;
        const ab = document.createElement("div"); ab.className = "vocab-audio-btns";
        ab.appendChild(TTS.btn(v.word, false)); ab.appendChild(TTS.btn(v.word, true));
        card.appendChild(ab);
        card.addEventListener("click", e => { if (!e.target.closest(".audio-btn")) card.classList.toggle("revealed"); });
        g.appendChild(card);
    });
    s.appendChild(g);

    // Examples
    const ex = document.createElement("div"); ex.className = "vocab-examples"; ex.innerHTML = "<h4>📌 例句聽讀</h4>";
    dp.vocab.forEach(v => {
        const row = document.createElement("div"); row.className = "example-row";
        row.innerHTML = `<div class="example-text"><strong>${v.word}</strong>: ${v.example}</div>`;
        const btns = document.createElement("div"); btns.className = "example-audio-btns";
        btns.appendChild(TTS.btn(v.example, false)); btns.appendChild(TTS.btn(v.example, true));
        row.appendChild(btns); ex.appendChild(row);
    });
    s.appendChild(ex);

    // Spelling test trigger
    const spBtn = document.createElement("button"); spBtn.className = "spelling-trigger-btn";
    spBtn.textContent = "✏️ 開始拼寫測驗"; spBtn.onclick = () => openSpellingTest(dp.vocab);
    s.appendChild(spBtn);

    return s;
}

// --- Spelling Test ---
function openSpellingTest(vocabList) {
    const modal = document.getElementById("spelling-modal"); modal.classList.remove("hidden");
    const body = document.getElementById("spelling-body"); body.innerHTML = "";
    vocabList.forEach((v, i) => {
        const item = document.createElement("div"); item.className = "spelling-item";
        item.innerHTML = `
            <div class="spelling-prompt">${v.emoji} <strong>${v.meaning}</strong></div>
            <div class="spelling-input-row">
                <input class="spelling-input" type="text" placeholder="輸入英文拼寫..." data-answer="${v.word}" autocomplete="off" autocapitalize="off">
                <button class="spelling-check-btn">確認</button>
            </div>
            <div class="spelling-result" style="display:none"></div>
        `;

        const input = item.querySelector("input");
        const checkBtn = item.querySelector(".spelling-check-btn");
        const result = item.querySelector(".spelling-result");

        // Also add audio hint button
        const hintBtn = document.createElement("button"); hintBtn.className = "audio-btn"; hintBtn.innerHTML = "🔊";
        hintBtn.title = "聽提示發音"; hintBtn.style.marginLeft = "4px";
        hintBtn.onclick = (e) => { e.stopPropagation(); TTS.speak(v.word); };
        item.querySelector(".spelling-input-row").appendChild(hintBtn);

        function check() {
            const ans = input.value.trim().toLowerCase();
            if (!ans) return;
            if (ans === v.word.toLowerCase()) {
                result.textContent = "✅ 正確！"; result.className = "spelling-result correct";
                recordAnswer("vocab", true);
            } else {
                result.textContent = `❌ 正確答案：${v.word}`; result.className = "spelling-result wrong";
                recordAnswer("vocab", false, { question: v.meaning, yourAnswer: ans, correctAnswer: v.word, explanation: v.example });
            }
            result.style.display = "block"; input.disabled = true; checkBtn.disabled = true;
        }
        checkBtn.onclick = check;
        input.onkeydown = (e) => { if (e.key === "Enter") check(); };
        body.appendChild(item);
    });

    document.getElementById("spelling-close-btn").onclick = () => modal.classList.add("hidden");
}

// --- Listening ---
function buildListening(dp) {
    const s = document.createElement("div"); s.className = "training-section listening-section";
    const ex = dp.listenExercise;
    s.innerHTML = "<h3>🎧 聽力測驗</h3><p class='section-hint'>先聽音檔作答，答完再看原文</p>";
    const ctrl = document.createElement("div"); ctrl.className = "listening-controls";

    const playBtn = document.createElement("button"); playBtn.className = "listen-play-btn";
    playBtn.innerHTML = "▶️ 播放音檔";
    playBtn.onclick = () => { const u = TTS.speak(ex.script); playBtn.innerHTML = "🔊 播放中..."; if(u) u.onend = () => playBtn.innerHTML = "▶️ 再聽一次"; };
    ctrl.appendChild(playBtn);

    const slowBtn = document.createElement("button"); slowBtn.className = "listen-play-btn listen-slow-btn";
    slowBtn.innerHTML = "🐢 慢速播放";
    slowBtn.onclick = () => { const u = TTS.speakSlow(ex.script); slowBtn.innerHTML = "🔊 播放中..."; if(u) u.onend = () => slowBtn.innerHTML = "🐢 慢速再聽"; };
    ctrl.appendChild(slowBtn);
    s.appendChild(ctrl);

    const qDiv = document.createElement("div");
    qDiv.innerHTML = ex.questions.map((q,i) => `<div class="quiz-item"><div class="quiz-question">${i+1}. ${q.q}</div><div class="quiz-options" data-answer="${q.answer}" data-explanation="${esc(q.explanation)}" data-category="listening">${q.options.map((o,j)=>`<div class="quiz-option" data-index="${j}">${String.fromCharCode(65+j)}. ${o}</div>`).join("")}</div><div class="quiz-explanation"></div></div>`).join("");
    s.appendChild(qDiv);

    const tBtn = document.createElement("button"); tBtn.className = "transcript-toggle"; tBtn.textContent = "📝 顯示原文";
    const tDiv = document.createElement("div"); tDiv.className = "transcript-content"; tDiv.textContent = ex.script; tDiv.style.display = "none";
    tBtn.onclick = () => { const v = tDiv.style.display !== "none"; tDiv.style.display = v?"none":"block"; tBtn.textContent = v?"📝 顯示原文":"📝 隱藏原文"; };
    s.appendChild(tBtn); s.appendChild(tDiv);
    return s;
}

// --- Grammar ---
function buildGrammar(dp) {
    const s = document.createElement("div"); s.className = "training-section";
    s.innerHTML = `<h3>📝 文法：${dp.grammar.topic}（${dp.grammarLevel}分級）</h3><p style="font-size:0.9rem;margin-bottom:16px">${dp.grammar.explanation}</p>` +
        dp.grammar.questions.map((q,i) => `<div class="quiz-item"><div class="quiz-question">${i+1}. ${q.q}</div><div class="quiz-options" data-answer="${q.answer}" data-explanation="${esc(q.explanation)}" data-category="grammar">${q.options.map((o,j)=>`<div class="quiz-option" data-index="${j}">${String.fromCharCode(65+j)}. ${o}</div>`).join("")}</div><div class="quiz-explanation"></div></div>`).join("");
    return s;
}

// --- Reading ---
function buildReading(dp) {
    const s = document.createElement("div"); s.className = "training-section";
    const p = dp.readExercise.passage;
    s.innerHTML = `<h3>📄 閱讀練習</h3><div class="reading-passage-wrapper"><div class="reading-passage">${p.replace(/\n/g,"<br>")}</div><div class="reading-audio-bar"><span class="audio-label">聽文章朗讀</span></div></div>` +
        dp.readExercise.questions.map((q,i) => `<div class="quiz-item"><div class="quiz-question">${i+1}. ${q.q}</div><div class="quiz-options" data-answer="${q.answer}" data-explanation="${esc(q.explanation)}" data-category="reading">${q.options.map((o,j)=>`<div class="quiz-option" data-index="${j}">${String.fromCharCode(65+j)}. ${o}</div>`).join("")}</div><div class="quiz-explanation"></div></div>`).join("");
    setTimeout(() => {
        const bar = s.querySelector(".reading-audio-bar");
        if (bar) { bar.appendChild(TTS.btn(p, false)); bar.appendChild(TTS.btn(p, true)); }
    }, 0);
    return s;
}

// --- Quiz interaction with wrong-answer tracking ---
function setupQuiz(container) {
    container.querySelectorAll(".quiz-options").forEach(opts => {
        const ci = parseInt(opts.dataset.answer);
        const expl = opts.dataset.explanation;
        const cat = opts.dataset.category || "reading";
        const explEl = opts.nextElementSibling;
        const questionText = opts.previousElementSibling?.textContent || "";

        opts.querySelectorAll(".quiz-option").forEach(opt => {
            opt.addEventListener("click", () => {
                if (opt.classList.contains("disabled")) return;
                opts.querySelectorAll(".quiz-option").forEach(o => o.classList.add("disabled"));
                const idx = parseInt(opt.dataset.index);
                if (idx === ci) {
                    opt.classList.add("correct");
                    recordAnswer(cat, true);
                } else {
                    opt.classList.add("wrong");
                    opts.querySelector(`[data-index="${ci}"]`).classList.add("correct");
                    const correctText = opts.querySelector(`[data-index="${ci}"]`).textContent;
                    recordAnswer(cat, false, { question: questionText, yourAnswer: opt.textContent, correctAnswer: correctText, explanation: expl });
                }
                explEl.textContent = expl; explEl.style.display = "block";
            });
        });
    });
}

function esc(str) { const d = document.createElement("div"); d.textContent = str; return d.innerHTML; }

// ===== Daily Report (Feature 5) =====
function showDailyReport(accuracy, timeSeconds) {
    const modal = document.getElementById("report-modal"); modal.classList.remove("hidden");
    const body = document.getElementById("report-body");
    const mins = Math.floor(timeSeconds / 60), secs = timeSeconds % 60;
    const total = sessionStats.correct + sessionStats.wrong;

    let grade, gradeClass;
    if (accuracy >= 90) { grade = "🌟 優秀！"; gradeClass = "excellent"; }
    else if (accuracy >= 70) { grade = "👍 不錯！"; gradeClass = "good"; }
    else if (accuracy >= 50) { grade = "💪 加油！"; gradeClass = "fair"; }
    else { grade = "📚 需要加強"; gradeClass = "poor"; }

    // Find weakest category
    let weakest = "", worstRate = 1;
    const catNames = { listening: "聽力", reading: "閱讀", grammar: "文法", vocab: "單字" };
    for (const [k, v] of Object.entries(sessionStats.categories)) {
        const t = v.c + v.w;
        if (t > 0) { const r = v.c / t; if (r < worstRate) { worstRate = r; weakest = catNames[k]; } }
    }

    body.innerHTML = `
        <div class="report-grade ${gradeClass}">${grade}</div>
        <div class="report-stat-row"><span class="report-label">正確率</span><span class="report-value">${accuracy}%</span></div>
        <div class="report-stat-row"><span class="report-label">答對 / 總題數</span><span class="report-value">${sessionStats.correct} / ${total}</span></div>
        <div class="report-stat-row"><span class="report-label">花費時間</span><span class="report-value">${mins} 分 ${secs} 秒</span></div>
        <div class="report-stat-row"><span class="report-label">聽力</span><span class="report-value">${sessionStats.categories.listening.c}/${sessionStats.categories.listening.c+sessionStats.categories.listening.w}</span></div>
        <div class="report-stat-row"><span class="report-label">閱讀</span><span class="report-value">${sessionStats.categories.reading.c}/${sessionStats.categories.reading.c+sessionStats.categories.reading.w}</span></div>
        <div class="report-stat-row"><span class="report-label">文法</span><span class="report-value">${sessionStats.categories.grammar.c}/${sessionStats.categories.grammar.c+sessionStats.categories.grammar.w}</span></div>
        ${weakest ? `<div class="report-weak">⚠️ 建議加強：<strong>${weakest}</strong>（正確率最低）</div>` : ""}
    `;
    document.getElementById("report-close-btn").onclick = () => modal.classList.add("hidden");
}

// ===== Part Practice (Feature 2 + Feature 6 Topics) =====
function initParts() {
    document.querySelectorAll(".part-card").forEach(card => {
        card.addEventListener("click", () => openPartDetail(parseInt(card.dataset.part)));
    });

    // Topics grid
    const grid = document.getElementById("topics-grid");
    TOEIC_DATA.topics.forEach(t => {
        const el = document.createElement("div"); el.className = "topic-card";
        el.innerHTML = `<div class="topic-emoji">${t.emoji}</div><div class="topic-name">${t.name}</div>`;
        el.addEventListener("click", () => openTopicDetail(t));
        grid.appendChild(el);
    });

    document.getElementById("part-back-btn").addEventListener("click", () => showPage("parts-page"));
}

let partTimer;
function openPartDetail(partNum) {
    showPage("part-detail-page");
    if (partTimer) partTimer.reset();
    partTimer = createTimer("part-timer-display", "part-timer-toggle");

    const part = TOEIC_DATA.partExercises[partNum];
    document.getElementById("part-detail-title").textContent = `Part ${partNum}：${part.name}`;
    const content = document.getElementById("part-detail-content"); content.innerHTML = "";

    const info = document.createElement("div"); info.className = "card";
    info.innerHTML = `<p>${part.instructions}</p>`; content.appendChild(info);

    part.exercises.forEach((ex, ei) => {
        const section = document.createElement("div"); section.className = "training-section";

        if (part.type === "listening") {
            const script = ex.script;
            section.innerHTML = `<h3>題組 ${ei+1}</h3>`;
            if (ex.scene) { section.innerHTML += `<p class="section-hint">場景：${ex.scene}</p>`; }
            const ctrl = document.createElement("div"); ctrl.className = "listening-controls";
            const pb = document.createElement("button"); pb.className = "listen-play-btn"; pb.innerHTML = "▶️ 播放";
            pb.onclick = () => { const u = TTS.speak(script); pb.innerHTML = "🔊 播放中..."; if(u) u.onend = () => pb.innerHTML = "▶️ 再聽"; };
            ctrl.appendChild(pb);
            const sb = document.createElement("button"); sb.className = "listen-play-btn listen-slow-btn"; sb.innerHTML = "🐢 慢速";
            sb.onclick = () => { const u = TTS.speakSlow(script); sb.innerHTML = "🔊 播放中..."; if(u) u.onend = () => sb.innerHTML = "🐢 慢速"; };
            ctrl.appendChild(sb);
            section.appendChild(ctrl);
        } else {
            section.innerHTML = `<h3>題組 ${ei+1}</h3>`;
            if (ex.passage) { section.innerHTML += `<div class="reading-passage">${ex.passage.replace(/\n/g,"<br>")}</div>`; }
        }

        const qHtml = ex.questions.map((q,i) => `<div class="quiz-item"><div class="quiz-question">${i+1}. ${q.q}</div><div class="quiz-options" data-answer="${q.answer}" data-explanation="${esc(q.explanation)}" data-category="${part.type}">${q.options.map((o,j)=>`<div class="quiz-option" data-index="${j}">${String.fromCharCode(65+j)}. ${o}</div>`).join("")}</div><div class="quiz-explanation"></div></div>`).join("");
        const qDiv = document.createElement("div"); qDiv.innerHTML = qHtml; section.appendChild(qDiv);
        content.appendChild(section);
    });

    setupQuiz(content);
}

function openTopicDetail(topic) {
    showPage("part-detail-page");
    document.getElementById("part-detail-title").textContent = `${topic.emoji} ${topic.name}`;
    const content = document.getElementById("part-detail-content"); content.innerHTML = "";

    // Vocab
    const vs = document.createElement("div"); vs.className = "training-section";
    vs.innerHTML = `<h3>📖 主題單字</h3>`;
    const vg = document.createElement("div"); vg.className = "vocab-grid";
    topic.vocab.forEach(w => {
        const card = document.createElement("div"); card.className = "vocab-card"; card.style.minHeight = "80px";
        card.innerHTML = `<div class="word">${w}</div>`;
        const ab = document.createElement("div"); ab.className = "vocab-audio-btns";
        ab.appendChild(TTS.btn(w, false)); ab.appendChild(TTS.btn(w, true));
        card.appendChild(ab);
        vg.appendChild(card);
    });
    vs.appendChild(vg);
    content.appendChild(vs);

    // Sentences
    const ss = document.createElement("div"); ss.className = "training-section";
    ss.innerHTML = `<h3>📌 常用句型</h3>`;
    topic.sentences.forEach(sent => {
        const row = document.createElement("div"); row.className = "example-row";
        row.innerHTML = `<div class="example-text">${sent}</div>`;
        const btns = document.createElement("div"); btns.className = "example-audio-btns";
        btns.appendChild(TTS.btn(sent, false)); btns.appendChild(TTS.btn(sent, true));
        row.appendChild(btns); ss.appendChild(row);
    });
    content.appendChild(ss);
}

// ===== Wrong Answer Book (Feature 3) =====
function initWrong() {
    document.querySelectorAll(".wrong-filters .filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".wrong-filters .filter-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            renderWrong(btn.dataset.filter);
        });
    });
    document.getElementById("clear-wrong-btn").addEventListener("click", () => {
        if (confirm("確定清空錯題本？")) { saveWrong([]); renderWrong("all"); }
    });
}

function renderWrong(filter = "all") {
    const wrongs = loadWrong();
    const filtered = filter === "all" ? wrongs : wrongs.filter(w => w.category === filter);

    // Stats
    const stats = document.getElementById("wrong-stats");
    const catCount = {};
    wrongs.forEach(w => { catCount[w.category] = (catCount[w.category]||0) + 1; });
    stats.innerHTML = `
        <div class="wrong-stat"><div class="wrong-stat-num">${wrongs.length}</div><div class="wrong-stat-label">總錯題</div></div>
        <div class="wrong-stat"><div class="wrong-stat-num">${catCount.listening||0}</div><div class="wrong-stat-label">聽力</div></div>
        <div class="wrong-stat"><div class="wrong-stat-num">${catCount.reading||0}</div><div class="wrong-stat-label">閱讀</div></div>
        <div class="wrong-stat"><div class="wrong-stat-num">${catCount.grammar||0}</div><div class="wrong-stat-label">文法</div></div>
    `;

    const list = document.getElementById("wrong-list"); list.innerHTML = "";
    if (filtered.length === 0) { list.innerHTML = '<p style="text-align:center;color:var(--text-light);padding:40px">沒有錯題紀錄 👍</p>'; return; }

    const catColors = { listening: "tag-listening", reading: "tag-reading", grammar: "tag-grammar", vocab: "tag-vocab" };
    const catNames = { listening: "聽力", reading: "閱讀", grammar: "文法", vocab: "單字" };

    filtered.slice().reverse().forEach(w => {
        const el = document.createElement("div"); el.className = "wrong-item";
        el.innerHTML = `
            <div class="wrong-item-header"><span class="wrong-item-tag analysis-tag ${catColors[w.category]||""}">${catNames[w.category]||w.category}</span><span style="font-size:0.75rem;color:var(--text-light)">${new Date(w.date).toLocaleDateString()}</span></div>
            <div class="wrong-item-q">${w.question}</div>
            <div class="wrong-item-your">你的答案：${w.yourAnswer}</div>
            <div class="wrong-item-correct">正確答案：${w.correctAnswer}</div>
            ${w.explanation ? `<div class="wrong-item-explain">💡 ${w.explanation}</div>` : ""}
        `;
        list.appendChild(el);
    });

    // Track review for achievements
    const state = loadState();
    if (state) { state.wrongReviewed = (state.wrongReviewed||0) + filtered.length; checkAchievements(state); saveState(state); }
}

// ===== Speed Reader (Feature 7) =====
let speedWPM = 150, speedInterval = null, speedWordIndex = 0, speedWords = [], speedCurrentText = "";

function initSpeed() {
    document.querySelectorAll("#wpm-group .option-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll("#wpm-group .option-btn").forEach(b => b.classList.remove("selected"));
            btn.classList.add("selected");
            speedWPM = parseInt(btn.dataset.value);
        });
    });

    // Listen buttons
    const listenBtn = document.getElementById("speed-listen-btn");
    const listenSlowBtn = document.getElementById("speed-listen-slow-btn");

    listenBtn.addEventListener("click", () => {
        if (!speedCurrentText) return;
        TTS.stop();
        listenBtn.classList.add("playing");
        listenBtn.innerHTML = "🔊 播放中...";
        const u = TTS.speak(speedCurrentText);
        if (u) {
            u.onend = () => { listenBtn.classList.remove("playing"); listenBtn.innerHTML = "🔊 再聽一遍"; };
            u.onerror = () => { listenBtn.classList.remove("playing"); listenBtn.innerHTML = "🔊 再聽一遍"; };
        }
    });

    listenSlowBtn.addEventListener("click", () => {
        if (!speedCurrentText) return;
        TTS.stop();
        listenSlowBtn.classList.add("playing");
        listenSlowBtn.innerHTML = "🐢 播放中...";
        const u = TTS.speakSlow(speedCurrentText);
        if (u) {
            u.onend = () => { listenSlowBtn.classList.remove("playing"); listenSlowBtn.innerHTML = "🐢 慢速再聽"; };
            u.onerror = () => { listenSlowBtn.classList.remove("playing"); listenSlowBtn.innerHTML = "🐢 慢速再聽"; };
        }
    });

    document.getElementById("speed-start-btn").addEventListener("click", startSpeedRead);
    document.getElementById("speed-stop-btn").addEventListener("click", stopSpeedRead);
    loadSpeedText();
}

function loadSpeedText() {
    const texts = TOEIC_DATA.speedReadingTexts;
    speedCurrentText = texts[Math.floor(Math.random() * texts.length)];
    speedWords = speedCurrentText.split(/\s+/);
    const el = document.getElementById("speed-text");
    el.innerHTML = speedWords.map((w, i) => `<span class="speed-word" data-idx="${i}">${w} </span>`).join("");
    speedWordIndex = 0;
    document.getElementById("speed-result").classList.add("hidden");
    // Reset listen buttons text
    document.getElementById("speed-listen-btn").innerHTML = "🔊 先聽一遍正確發音";
    document.getElementById("speed-listen-slow-btn").innerHTML = "🐢 慢速聽";
}

function startSpeedRead() {
    TTS.stop(); // Stop any playing audio
    loadSpeedText();
    const msPerWord = 60000 / speedWPM;
    const startTime = Date.now();
    document.getElementById("speed-start-btn").disabled = true;
    document.getElementById("speed-stop-btn").disabled = false;
    speedWordIndex = 0;

    speedInterval = setInterval(() => {
        const el = document.querySelector(`.speed-word[data-idx="${speedWordIndex}"]`);
        if (!el) { finishSpeedRead(startTime); return; }
        document.querySelectorAll(".speed-word.highlight").forEach(w => { w.classList.remove("highlight"); w.classList.add("past"); });
        el.classList.add("highlight");
        el.scrollIntoView({ behavior: "smooth", block: "center" });
        speedWordIndex++;
    }, msPerWord);
}

function stopSpeedRead() {
    clearInterval(speedInterval);
    document.getElementById("speed-start-btn").disabled = false;
    document.getElementById("speed-stop-btn").disabled = true;
}

function finishSpeedRead(startTime) {
    clearInterval(speedInterval);
    const elapsed = (Date.now() - startTime) / 1000 / 60;
    const actualWPM = Math.round(speedWords.length / elapsed);

    const result = document.getElementById("speed-result");
    result.classList.remove("hidden");
    result.innerHTML = `
        <h3>🎉 完成！</h3>
        <p>單字數：${speedWords.length}</p>
        <p>實際速度：<strong>${actualWPM} WPM</strong></p>
        <p>目標速度：${speedWPM} WPM</p>
        <button id="speed-replay-btn" class="listen-play-btn" style="margin-top:12px;width:100%">🔊 再聽一遍正確發音</button>
        <button id="speed-next-btn" class="primary-btn" style="margin-top:8px">🔄 換一篇新文章</button>
    `;

    // Replay button inside result
    document.getElementById("speed-replay-btn").addEventListener("click", () => {
        const btn = document.getElementById("speed-replay-btn");
        btn.innerHTML = "🔊 播放中...";
        btn.classList.add("playing");
        const u = TTS.speak(speedCurrentText);
        if (u) {
            u.onend = () => { btn.innerHTML = "🔊 再聽一遍正確發音"; btn.classList.remove("playing"); };
            u.onerror = () => { btn.innerHTML = "🔊 再聽一遍正確發音"; btn.classList.remove("playing"); };
        }
    });

    // Next article button
    document.getElementById("speed-next-btn").addEventListener("click", () => {
        TTS.stop();
        loadSpeedText();
    });

    document.getElementById("speed-start-btn").disabled = false;
    document.getElementById("speed-stop-btn").disabled = true;

    const state = loadState();
    if (state) {
        if (actualWPM > (state.bestWPM||0)) state.bestWPM = actualWPM;
        checkAchievements(state); saveState(state);
    }
}

// ===== Achievements (Feature 8) =====
function renderAchievements() {
    const state = loadState();
    if (!state) return;

    const unlocked = state.unlockedAchievements || [];
    const total = TOEIC_DATA.achievements.length;

    document.getElementById("achievement-summary").innerHTML = `
        <div class="achievement-summary-item"><div class="achievement-summary-num">${unlocked.length}/${total}</div><div class="achievement-summary-label">已解鎖</div></div>
        <div class="achievement-summary-item"><div class="achievement-summary-num">${calcStreak(state)}</div><div class="achievement-summary-label">連續天數</div></div>
        <div class="achievement-summary-item"><div class="achievement-summary-num">${state.bestAccuracy||0}%</div><div class="achievement-summary-label">最佳正確率</div></div>
    `;

    const grid = document.getElementById("achievements-grid"); grid.innerHTML = "";
    TOEIC_DATA.achievements.forEach(a => {
        const u = unlocked.find(x => x.id === a.id);
        const card = document.createElement("div");
        card.className = `achievement-card ${u ? "unlocked" : "locked"}`;
        card.innerHTML = `
            <div class="achievement-icon">${a.icon}</div>
            <div class="achievement-name">${a.name}</div>
            <div class="achievement-desc">${a.desc}</div>
            ${u ? `<div class="achievement-date">✅ ${new Date(u.date).toLocaleDateString()}</div>` : ""}
        `;
        grid.appendChild(card);
    });
}

function checkAchievements(state) {
    if (!state.unlockedAchievements) state.unlockedAchievements = [];
    const ids = state.unlockedAchievements.map(a => a.id);
    TOEIC_DATA.achievements.forEach(a => {
        if (!ids.includes(a.id) && a.condition(state)) {
            state.unlockedAchievements.push({ id: a.id, date: new Date().toISOString() });
        }
    });
}

// ===== Layout Mode Toggle (Mobile / Desktop) =====
function initLayout() {
    const saved = localStorage.getItem("toeic_layout");
    const btn = document.getElementById("layout-btn");
    const viewport = document.querySelector('meta[name="viewport"]');

    function applyLayout(mode) {
        if (mode === "desktop") {
            document.documentElement.setAttribute("data-layout", "desktop");
            viewport.setAttribute("content", "width=1024");
            btn.innerHTML = "📱";
            btn.title = "切換手機模式";
            btn.classList.add("active-mode");
        } else {
            document.documentElement.removeAttribute("data-layout");
            viewport.setAttribute("content", "width=device-width, initial-scale=1.0");
            btn.innerHTML = "💻";
            btn.title = "切換電腦模式";
            btn.classList.remove("active-mode");
        }
        localStorage.setItem("toeic_layout", mode);
    }

    // Apply saved preference
    if (saved) applyLayout(saved);

    btn.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-layout");
        const next = current === "desktop" ? "mobile" : "desktop";
        applyLayout(next);
        showToast(next === "desktop" ? "已切換為電腦模式" : "已切換為手機模式");
    });
}

// ===== Dark Mode (Feature: Theme Toggle) =====
function initTheme() {
    const saved = localStorage.getItem("toeic_theme");
    if (saved === "dark" || (!saved && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
        document.documentElement.setAttribute("data-theme", "dark");
        document.getElementById("theme-btn").innerHTML = "☀️";
    }
    document.getElementById("theme-btn").addEventListener("click", () => {
        const isDark = document.documentElement.getAttribute("data-theme") === "dark";
        if (isDark) {
            document.documentElement.removeAttribute("data-theme");
            document.getElementById("theme-btn").innerHTML = "🌙";
            localStorage.setItem("toeic_theme", "light");
        } else {
            document.documentElement.setAttribute("data-theme", "dark");
            document.getElementById("theme-btn").innerHTML = "☀️";
            localStorage.setItem("toeic_theme", "dark");
        }
    });
}

// ===== Share (Feature: Share Link) =====
function initShare() {
    document.getElementById("share-btn").addEventListener("click", async () => {
        const url = window.location.href;
        const shareData = { title: "TOEIC 訓練計畫", text: "免費 TOEIC 多益訓練，依目標分數自動配置每日練習！", url };

        if (navigator.share) {
            try { await navigator.share(shareData); } catch (e) { /* user cancelled */ }
        } else {
            try {
                await navigator.clipboard.writeText(url);
                showToast("已複製連結！可以分享給朋友");
            } catch {
                prompt("複製此連結分享：", url);
            }
        }
    });
}

function showToast(msg) {
    const t = document.createElement("div"); t.className = "share-toast"; t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2200);
}

// ===== Init =====
document.addEventListener("DOMContentLoaded", () => {
    initLayout();
    initTheme();
    initShare();
    initSetup();
    initParts();
    initWrong();
    initSpeed();

    // Nav
    document.querySelectorAll(".nav-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const page = btn.dataset.page;
            showPage(page);
            if (page === "wrong-page") renderWrong("all");
            if (page === "achievements-page") renderAchievements();
        });
    });

    const state = loadState();
    if (state) {
        document.getElementById("bottom-nav").classList.remove("hidden");
        loadDashboard(state);
    } else {
        showPage("setup-page");
    }
});
