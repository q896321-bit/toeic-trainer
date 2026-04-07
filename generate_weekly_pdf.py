#!/usr/bin/env python3
"""Generate 13 weekly TOEIC study plan PDFs with Chinese support."""

import os
from fpdf import FPDF

FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "weekly-pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Weekly data ──────────────────────────────────────────────

weeks = [
    # ── Phase 1: 打基礎 ──
    {
        "week": 1,
        "phase": "Phase 1：打基礎",
        "title": "基礎詞彙 + 詞性辨識",
        "dates": "Day 1-7（4/7 - 4/13）",
        "goal": "建立 TOEIC 基礎詞彙，學會判斷詞性，熟悉 Part 1-2 題型",
        "daily_time": "每日 60-90 分鐘（早 20 min 單字 / 午 25 min 文法 / 晚 20 min 聽力 / 睡前 10 min 複習）",
        "days": [
            ("Day 1\n(一)", "辦公室用語\noffice, meeting, schedule,\nappointment, deadline,\ncolleague, department,\nmanager, report, memo,\nassign, submit, approve,\npriority, conference",
             "名詞 vs 動詞 vs 形容詞\n\n判斷方法：\n-tion/-ment/-ness → 名詞\n-ful/-ous/-ive → 形容詞\n-ly → 副詞\n-ize/-ify → 動詞",
             "Part 1 照片描述 x5\n\n技巧：看圖先想\n1. 誰在做什麼\n2. 東西在哪裡\n3. 場景描述"),
            ("Day 2\n(二)", "商務信件用語\nletter, confirm, sincerely,\nregarding, enclosed,\nattach, forward, inquire,\nrespond, acknowledge,\nrecipient, correspondence,\nnotify, reference, update",
             "主詞動詞一致\n\nThe manager is...\nThe managers are...\nEveryone has...\nNeither A nor B is...",
             "Part 1 照片描述 x5\n\n注意被動語態描述：\nThe table is covered...\nBooks are placed..."),
            ("Day 3\n(三)", "會議用語\nagenda, proposal, discuss,\nminutes, chairperson,\npostpone, adjourn, resolve,\nconsensus, motion,\nparticipant, unanimous,\nquorum, second, vote",
             "時態：現在簡單式\n\n用於：習慣/事實/排程\nWe meet every Monday.\nThe train leaves at 9.\nShe works in marketing.",
             "Part 2 應答問題 x10\n\n技巧：聽第一個字\nWho → 回答人\nWhere → 回答地點\nWhen → 回答時間"),
            ("Day 4\n(四)", "人事用語\nhire, resume, interview,\ncandidate, qualify,\nexperience, reference,\nposition, promote, resign,\napplicant, recruit, benefit,\nsalary, evaluate",
             "時態：過去簡單式\n\n用於：已完成的事\nWe hired a new manager.\nShe submitted the report\nyesterday.",
             "Part 2 應答問題 x10\n\n注意間接回答：\nQ: Where is the meeting?\nA: Ask Ms. Chen.\n（不直接回答也可能對）"),
            ("Day 5\n(五)", "財務用語\nbudget, invoice, expense,\nrevenue, profit, receipt,\nreimburse, audit, balance,\naccount, transaction,\ndeposit, quarterly, fiscal,\nforecast",
             "時態：未來式\n\nwill + V：臨時決定\nbe going to + V：計畫\nWe will discuss it later.\nI'm going to apply for\nthe position.",
             "Part 1+2 混合 x10\n\n本週複習重點：\n描述圖片 + 快速應答"),
            ("Day 6\n(六)", "【Week 1 總複習】\n\n回顧本週 75 個單字\n用 toeic-trainer 單字卡\n+ 拼寫測驗功能複習\n\n重點複習錯過的單字",
             "時態總複習\n\n做 Part 5 練習題 x15\n（詞性題 + 時態題）\n\n記錄錯題到錯題本",
             "複習本週錯題\n\n重新聽錯過的題目\n分析錯誤原因：\n□ 沒聽到關鍵字\n□ 被相似音誤導\n□ 不熟悉句型"),
            ("Day 7\n(日)", "【休息日】\n\n輕鬆看英文 YouTube\n或影集 30 分鐘\n\n推薦：\n- English with Lucy\n- TED-Ed",
             "不做文法練習\n\n可以翻閱本週\n文法筆記放鬆回顧",
             "不做正式練習\n\n可聽英文歌或\nPodcast 放鬆"),
        ],
    },
    {
        "week": 2,
        "phase": "Phase 1：打基礎",
        "title": "進階詞彙 + 動詞時態",
        "dates": "Day 8-14（4/14 - 4/20）",
        "goal": "擴充生活情境詞彙，掌握 12 種動詞時態，熟悉 Part 3-4",
        "daily_time": "每日 60-90 分鐘",
        "days": [
            ("Day 8\n(一)", "旅遊用語\nitinerary, reservation,\ndeparture, arrival, luggage,\npassport, boarding pass,\ngate, terminal, customs,\ndestination, round-trip,\nconnecting flight, delay,\nconfirmation",
             "現在進行式 vs 現在簡單式\n\nI work here.（事實）\nI'm working on it.（現在進行）\n\n注意：stative verbs\n不用進行式\nknow/want/need/like",
             "Part 3 對話 x3\n\n技巧：先讀題目\n利用 8 秒間隔預讀\n下一組題目和選項"),
            ("Day 9\n(二)", "飯店用語\ncheck-in, vacancy,\naccommodate, suite,\nhousekeeping, complimentary,\namenity, lobby, bellhop,\nconcierge, checkout,\nreservation, front desk,\noccupancy, upgrade",
             "過去進行式 vs 過去簡單式\n\nI was reading when\nhe called.\n\n長動作用進行式\n短動作用簡單式",
             "Part 3 對話 x3\n\n注意聽：\n1. 對話發生地點\n2. 說話者關係\n3. 接下來要做什麼"),
            ("Day 10\n(三)", "購物用語\ndiscount, refund, warranty,\nexchange, receipt, bargain,\ncoupon, merchandise,\npurchase, retail, wholesale,\ncashier, inventory, aisle,\nout of stock",
             "現在完成式\n\nhave/has + p.p.\n\n用於：\n1. 經驗：I have visited...\n2. 持續：She has worked\n   here since 2020.\n3. 剛完成：We have just\n   finished.",
             "Part 3 對話 x3\n\n練習：\n聽完後用英文寫下\n對話大意（2-3 句）"),
            ("Day 11\n(四)", "餐廳用語\nreserve, appetizer, bill,\nentree, beverage, gratuity,\nmenu, specials, portion,\ntakeout, dine-in, waiter,\ncomplimentary, allergy,\nvegetarian",
             "過去完成式\n\nhad + p.p.\n\n用於：過去的過去\nBy the time I arrived,\nthe meeting had already\nstarted.",
             "Part 4 獨白 x2\n\n題型：公告/語音留言\n/廣播/導覽\n\n注意：開頭通常點出\n說話目的"),
            ("Day 12\n(五)", "交通用語\ncommute, transfer, delay,\nplatform, fare, schedule,\nroute, detour, congestion,\npedestrian, intersection,\nexpressway, maintenance,\ntoll, shuttle",
             "完成進行式\n\nhave been + V-ing\n\nI have been working\nhere for 3 years.\n（強調持續進行中）",
             "Part 4 獨白 x2\n\n練習速記：\n邊聽邊記關鍵字\nwho/what/when/where"),
            ("Day 13\n(六)", "【Week 2 總複習】\n\n回顧本週 75 個單字\n+ Week 1 易錯字\n\n累計已學 150 字",
             "動詞時態 12 種總整理\n\n做一張時態整理表\n每種時態寫一個例句\n\n做 Part 5 x15 題",
             "複習本週錯題\n\n特別注意 Part 3-4\n是否能跟上對話速度"),
            ("Day 14\n(日)", "【休息日】\n\n用英文 App 輕鬆學\n推薦：Duolingo 或\nCake（看影片學英文）",
             "休息",
             "聽英文 Podcast 30 min\n推薦：6 Minute English\n(BBC)"),
        ],
    },
    {
        "week": 3,
        "phase": "Phase 1：打基礎",
        "title": "高頻詞彙 + 句型結構",
        "dates": "Day 15-21（4/21 - 4/27）",
        "goal": "掌握被動語態和關係子句，這是 Part 5-6 常考重點",
        "daily_time": "每日 60-90 分鐘",
        "days": [
            ("Day 15\n(一)", "行銷廣告\npromote, launch, campaign,\nadvertise, brand, target,\nmarket share, consumer,\ndemographic, sponsor,\nendorse, publicity, slogan,\nsurvey, feedback",
             "被動語態基礎\n\nbe + p.p.\nThe report was submitted.\nEmails are sent daily.\n\nby + 動作者（可省略）",
             "Part 1+2 混合 x10\n\nPart 1 常考被動：\nThe door is closed.\nCars are parked."),
            ("Day 16\n(二)", "通訊用語\nnotify, forward, attachment,\nbroadcast, subscribe,\nnewsletter, update, memo,\nannouncement, voicemail,\ncirculate, distribute,\nrecipient, cc, draft",
             "被動語態進階\n\n完成式被動：\nhas been completed\n進行式被動：\nis being reviewed\n\n情態動詞被動：\nshould be submitted",
             "Part 3 對話 x3\n\n注意被動語態出現\n在對話中的頻率"),
            ("Day 17\n(三)", "製造用語\nmanufacture, assemble,\ninspect, quality control,\ndefect, shipment, warehouse,\nsupplier, component, raw\nmaterial, production line,\nspecification, comply,\nregulation, recall",
             "關係代名詞\nwho/which/that\n\nThe manager who called\nis from Tokyo.\n\nThe report which/that\nwas submitted...\n\n人用 who，物用 which",
             "Part 3 對話 x3\n\n練習重點：\n聽出對話中的\n因果關係"),
            ("Day 18\n(四)", "法律合約\ncontract, terms, liable,\nagreement, clause, binding,\nviolation, penalty, comply,\nregulation, authorize,\nconfidential, disclose,\nwaiver, amendment",
             "關係子句進階\n\n限定 vs 非限定：\nThe man who called...\nMr. Kim, who called,...\n\n介系詞 + 關係代名詞：\nin which = where\nfor which = why",
             "Part 4 獨白 x2\n\n注意法律/合約\n相關情境詞彙"),
            ("Day 19\n(五)", "科技用語\nupgrade, install, compatible,\nsoftware, hardware, device,\nnetwork, database, server,\ndownload, encrypt, backup,\nmalfunction, troubleshoot,\ntechnician",
             "分詞構句 V-ing / V-ed\n\nHaving finished the report,\nhe left the office.\n\nLocated in downtown,\nthe hotel is convenient.\n\n現在分詞=主動\n過去分詞=被動",
             "Part 4 獨白 x2\n\n練習：聽完後\n口頭複述大意"),
            ("Day 20\n(六)", "【Week 3 總複習】\n\n回顧本週 75 字\n累計已學 225 字\n\n重點複習：\n被動語態 + 關係子句\n相關詞彙",
             "被動 + 關係子句\n綜合練習\n\nPart 5 x20 題\n專攻這兩個文法點",
             "複習本週所有錯題\n\n自我評估：\n□ 聽力有進步嗎\n□ 能聽懂大意嗎"),
            ("Day 21\n(日)", "【休息日】\n\n看一部英文電影\n（開英文字幕）",
             "休息",
             "休息"),
        ],
    },
    {
        "week": 4,
        "phase": "Phase 1：打基礎",
        "title": "衝刺詞彙 + 連接詞 + Phase 1 測驗",
        "dates": "Day 22-30（4/28 - 5/6）",
        "goal": "完成基礎詞彙 300 字，掌握連接詞與介系詞，Phase 1 測驗檢核",
        "daily_time": "每日 60-90 分鐘",
        "days": [
            ("Day 22\n(一)", "醫療健康\nprescription, symptom,\nclinic, pharmacy, diagnosis,\nallergic, treatment, patient,\nappointment, specialist,\ninsurance, emergency,\nrecovery, surgery, physician",
             "連接詞 and/but/or/so\n\n對等連接詞連接\n同層級的元素\n\nI called, but no one\nanswered.",
             "Part 2 x10 + Part 3 x3\n\n注意 but/however\n轉折後才是重點"),
            ("Day 23\n(二)", "環境用語\nsustainable, pollution,\nconserve, renewable, recycle,\nemission, carbon footprint,\necosystem, biodiversity,\nendangered, initiative,\nregulation, compliance,\nwaste, landfill",
             "從屬連接詞\nbecause/although/if/\nwhen/while/unless/\nsince/before/after\n\nAlthough it rained,\nthe event continued.",
             "Part 3 x3 + Part 4 x2\n\n聽從屬子句：\n注意 because/since\n後面的原因"),
            ("Day 24\n(三)", "銀行金融\ndeposit, withdraw, mortgage,\nloan, interest rate, credit,\nstatement, transfer, savings,\naccount, investment,\ndividend, asset, debt,\nbankruptcy",
             "副詞連接詞\nhowever/therefore/\nmoreover/furthermore/\nnevertheless/consequently\n/in addition/meanwhile\n\n注意標點：\n...; however, ...",
             "Part 2 x10\n\n練習：快速反應\n目標 5 秒內選答案"),
            ("Day 25\n(四)", "教育用語\nenroll, certificate, tuition,\nscholarship, curriculum,\nsemester, faculty, dean,\ngraduate, undergraduate,\nregistrar, prerequisite,\nassignment, thesis, diploma",
             "介系詞 in/on/at/by/for\n\n時間：at 9, on Monday,\nin March, in 2026\n\n地點：at the office,\non the 3rd floor,\nin the building",
             "Part 3+4 混合 x5"),
            ("Day 26\n(五)", "房地產\nlease, tenant, renovate,\nproperty, landlord, realtor,\nmortgage, down payment,\nsquare footage, furnished,\nvacancy, utilities, zoning,\nappraisal, commercial",
             "易混淆介系詞片語\n\nin charge of 負責\nin spite of 儘管\nin terms of 就...而言\ndue to 由於\nprior to 在...之前\nregardless of 不管",
             "Part 1-4 綜合 x10\n\n全 Part 混合練習\n模擬真實考試節奏"),
            ("Day 27\n(六)", "【Phase 1 總複習】\n\n所有 300 字快速掃描\n標記不熟的字\n\n用 toeic-trainer 做\n拼寫測驗",
             "全文法重點回顧\n\n製作一頁文法\n重點整理表：\n- 12 種時態\n- 被動語態\n- 關係子句\n- 連接詞\n- 介系詞",
             "全聽力 Part 模擬\nPart 1 x6\nPart 2 x10\nPart 3 x6\nPart 4 x4"),
            ("Day 28\n(日)", "Phase 1 小測驗\n\n閱讀：Part 5 x30 題\n限時 15 分鐘\n\n記錄分數：___/30",
             "Phase 1 小測驗\n\n聽力：Part 1-4 x30 題\n限時 20 分鐘\n\n記錄分數：___/30",
             ""),
            ("Day 29\n(一)", "檢討小測驗\n\n分析錯題：\n□ 單字不認識\n□ 文法不熟\n□ 粗心\n\n補強弱項",
             "整理錯題筆記\n寫出每題錯誤原因\n和正確解法",
             "錯題重聽\n確認每題都聽懂"),
            ("Day 30\n(二)", "【休息日】\n\n調整心態\n準備進入 Phase 2\n\n回顧 Phase 1 成果\n自我鼓勵！",
             "休息",
             "休息"),
        ],
    },
    # ── Phase 2: 題型突破 ──
    {
        "week": 5,
        "phase": "Phase 2：題型突破",
        "title": "Part 5 句子填空突破",
        "dates": "Day 31-37（5/7 - 5/13）",
        "goal": "掌握 Part 5 四大題型（詞性/時態/介系詞/連接詞），目標正確率 70%+",
        "daily_time": "每日 75-100 分鐘（早 15 min 單字 / 午 35 min 閱讀 / 晚 25 min 聽力 / 睡前 10 min 錯題）",
        "days": [
            ("Day 31\n(三)", "Part 5 詞性題 x20\n\n解題步驟：\n1. 看空格位置\n2. 判斷需要什麼詞性\n3. 選正確詞性的選項\n\n不需要讀完全句！",
             "詞性判斷複習\n\n空格前是 the/a → 名詞\n空格前是 be → 形/分詞\n空格修飾名詞 → 形容詞\n空格修飾動詞 → 副詞",
             "Part 1 x10\n\n加強基礎分"),
            ("Day 32\n(四)", "Part 5 時態題 x20\n\n解題步驟：\n1. 找時間線索詞\n   yesterday/last/ago → 過去\n   since/for → 完成式\n   next/tomorrow → 未來\n2. 選正確時態",
             "時態線索詞整理\n\nalready/yet/just → 完成\nwhile/when → 進行\nevery day → 簡單\nby the time → 完成",
             "Part 2 x15\n\n目標：正確率 70%+"),
            ("Day 33\n(五)", "Part 5 介系詞題 x20\n\n高頻搭配：\nresponsible for\nfamiliar with\nresult in\ncomply with\ndepend on\napply for",
             "TOEIC 高頻介系詞\n搭配 30 組整理\n\n寫成小卡片\n反覆記憶",
             "Part 3 x6\n\n練習預讀技巧"),
            ("Day 34\n(六)", "Part 5 連接詞題 x20\n\n判斷句子邏輯：\n因果 → because/therefore\n轉折 → although/however\n條件 → if/unless\n讓步 → despite/in spite of",
             "連接詞 vs 介系詞\n\nalthough + 子句\ndespite + 名詞\n\nbecause + 子句\nbecause of + 名詞",
             "Part 4 x4\n\n練習速記能力"),
            ("Day 35\n(日)", "Part 5 混合題 x30\n【限時 15 分鐘】\n\n目標：30 秒/題\n記錄分數：___/30\n記錄時間：___min",
             "檢討 + 分析\n\n統計各題型正確率：\n詞性：___/___\n時態：___/___\n介系詞：___/___\n連接詞：___/___",
             "Part 1-4 混合 x15\n\n記錄分數：___/15"),
            ("Day 36\n(一)", "【Week 5 複習】\n\n錯題重做\n整理 Part 5 必考重點\n到筆記本",
             "弱項加強\n依上週統計\n集中練最弱的題型",
             "錯題重聽\n分析聽力弱點"),
            ("Day 37\n(二)", "【休息日】",
             "休息",
             "休息"),
        ],
    },
    {
        "week": 6,
        "phase": "Phase 2：題型突破",
        "title": "Part 6 段落填空突破",
        "dates": "Day 38-44（5/14 - 5/20）",
        "goal": "掌握 Part 6 的前後文邏輯判斷和句子插入題型",
        "daily_time": "每日 75-100 分鐘",
        "days": [
            ("Day 38\n(三)", "Part 6 x4 篇\n（email 類）\n\n技巧：\n1. 先快速瀏覽全文\n2. 理解文章主題\n3. 再逐題作答\n\nEmail 常見結構：\n開頭寒暄→主要內容→\n結尾請求/感謝",
             "Email 常用句型\n\nI am writing to...\nPlease find attached...\nI would appreciate...\nShould you have any\nquestions, please...\nWe look forward to...",
             "Part 2 x15\n\n持續練習\n快速反應能力"),
            ("Day 39\n(四)", "Part 6 x4 篇\n（notice/公告類）\n\n句子插入題技巧：\n1. 看前後句的邏輯\n2. 注意代名詞指代\n3. 注意轉折/順序詞",
             "公告常用句型\n\nWe are pleased to\nannounce...\nPlease be advised that...\nEffective immediately...\nFor more information,\ncontact...",
             "Part 3 x6\n\n聽力練習\n注意 implication 題"),
            ("Day 40\n(五)", "Part 6 x4 篇\n（letter/信件類）\n\n連接詞選擇：\n看上文→判斷邏輯→\n選適當連接詞\n\nMoreover（加強）\nHowever（轉折）\nTherefore（因此）",
             "正式信件 vs 非正式\n\n正式：\nDear Mr./Ms.\nI am writing to inform\nSincerely,\n\n非正式：\nHi/Hello\nJust wanted to let you\nknow\nBest,",
             "Part 4 x4\n\n練習獨白類型辨識\n公告/留言/廣播/介紹"),
            ("Day 41\n(六)", "Part 6 x4 篇\n（article/文章類）\n\n時態一致性：\n全文主要時態要一致\n除非有明確時間轉換",
             "文章結構分析\n\n主題句（通常第一句）\n→ 支持細節\n→ 結論/行動呼籲",
             "Part 1-2 混合 x15\n\n維持基礎分"),
            ("Day 42\n(日)", "Part 5+6 綜合\nx40 題\n【限時 20 分鐘】\n\n分數：___/40\n時間：___min",
             "檢討 + 錯題分析\n\nPart 5：___/30\nPart 6：___/10\n\n弱項記錄",
             "Part 3-4 混合 x8\n\n分數：___/8"),
            ("Day 43\n(一)", "【Week 6 複習】\n\n錯題重做\n整理 Part 6 必考重點",
             "Part 5+6 弱項加強",
             "錯題重聽"),
            ("Day 44\n(二)", "【休息日】",
             "休息",
             "休息"),
        ],
    },
    {
        "week": 7,
        "phase": "Phase 2：題型突破",
        "title": "Part 7 閱讀理解突破",
        "dates": "Day 45-51（5/21 - 5/27）",
        "goal": "掌握 Part 7 先看題再讀文的技巧，提升閱讀速度",
        "daily_time": "每日 75-100 分鐘",
        "days": [
            ("Day 45\n(三)", "Part 7 單篇 x3\n（email/letter 類）\n\n核心技巧：\n1. 先看題目（30 秒）\n2. 帶著問題讀文章\n3. 找到答案就選\n   不用讀完全文",
             "常考題型：\n\n1. 主旨題 What is the\n   purpose of the email?\n   → 看開頭第 1-2 句\n\n2. 細節題\n   → 定位關鍵字",
             "Part 3 x6\n\n同樣練習\n先讀題再聽"),
            ("Day 46\n(四)", "Part 7 單篇 x3\n（advertisement 廣告類）\n\n廣告特徵：\n- 產品/服務名稱\n- 特色/優惠\n- 聯絡方式\n- 截止日期\n\n定位關鍵字找答案",
             "常考題型：\n\n3. 推論題\n   What is suggested/\n   implied about...?\n   → 找相關段落推理\n\n4. 同義字題\n   closest in meaning\n   → 看前後文判斷",
             "Part 4 x4\n\n注意廣告類獨白\n的產品/優惠細節"),
            ("Day 47\n(五)", "Part 7 單篇 x3\n（notice/memo 類）\n\nNOT/TRUE 題型：\n1. 逐一比對每個選項\n2. 回文章找證據\n3. 找不到證據的\n   就是 NOT 的答案",
             "閱讀速度訓練\n\n用 toeic-trainer\n閱讀速度功能\n目標：100→120 WPM\n\n技巧：不要回讀\n不要逐字翻譯",
             "Part 2 x15\n\n保持聽力手感"),
            ("Day 48\n(六)", "Part 7 雙篇 x2\n\n雙篇技巧：\n1. 先看題目\n2. 兩篇各讀一次\n3. 交叉比對題：\n   需要結合兩篇\n   的資訊才能答",
             "常見雙篇組合：\n- email + 回覆\n- 廣告 + 評價\n- 通知 + 報名表\n- 文章 + 回應信\n\n注意：人名/日期\n在兩篇中的對應",
             "Part 3 x6\n\n注意三人對話\n誰說了什麼"),
            ("Day 49\n(日)", "Part 7 三篇 x1\n+ 單篇 x2\n\n三篇技巧：\n同雙篇但更複雜\n建議先做有把握的\n單篇題\n\n時間分配很重要！",
             "時間分配練習\n\n整個 Part 7：\n54 題 / 55 分鐘\n\n單篇 2-4 題：3 min\n雙篇 5 題：5 min\n三篇 5 題：5 min",
             "Part 4 x4\n\n練習長獨白\n的資訊擷取"),
            ("Day 50\n(一)", "【Week 7 複習】\n\n錯題重做\nPart 7 各類型\n整理作答策略\n\n閱讀速度檢測\n目標：120 WPM",
             "Part 5+6+7\n弱項分析\n\n統計本週各 Part\n正確率",
             "複習本週錯題\n聽力正確率統計"),
            ("Day 51\n(二)", "【休息日】",
             "休息",
             "休息"),
        ],
    },
    {
        "week": 8,
        "phase": "Phase 2：題型突破",
        "title": "綜合練習 + Phase 2 測驗",
        "dates": "Day 52-60（5/28 - 6/5）",
        "goal": "整合所有題型練習，Phase 2 測驗確認進度，準備模擬衝刺",
        "daily_time": "每日 75-100 分鐘",
        "days": [
            ("Day 52\n(三)", "Part 5 x30 + Part 6 x8\n【限時 25 分鐘】\n\n目標：\nPart 5 每題 30 秒\nPart 6 每題 1 分鐘\n\n分數：___/38",
             "速度分析\n\n如果超時：\n□ Part 5 卡太久\n□ Part 6 讀太慢\n□ 猶豫不決\n\n超過 30 秒就先選\n做記號之後回來",
             "Part 1-2 x20\n\n分數：___/20"),
            ("Day 53\n(四)", "Part 7 單篇 x4\n+ 雙篇 x1\n\n練閱讀耐力\n不要中途休息\n一口氣做完\n\n目標時間：35 min",
             "檢討 + 速度分析\n\n每篇花了多少時間？\n哪種文章最慢？\n\n找出自己的\n閱讀速度瓶頸",
             "Part 3-4 x8\n\n分數：___/8"),
            ("Day 54\n(五)", "個人弱項加強\n\n依錯題本分析\n集中練習最弱的\nPart 和題型\n\n至少做 20 題",
             "文法弱項補強\n\n回顧所有錯題\n中的文法考點\n做額外練習",
             "個人聽力弱項\n\n最弱的 Part\n集中訓練 20 題"),
            ("Day 55\n(六)", "Part 5-7 綜合 x50\n【限時 40 分鐘】\n\n半模擬測驗\n分數：___/50\n時間：___min",
             "檢討半模擬\n\n各 Part 正確率：\nP5：___/20\nP6：___/10\nP7：___/20",
             "Part 1-4 x30\n【限時 25 分鐘】\n\n分數：___/30"),
            ("Day 56\n(日)", "詳細檢討 Day 55\n\n每一題都要分析\n錯誤原因\n\n寫出改進策略",
             "整理考試筆記\n把最重要的\n10 個文法規則\n寫成一頁速查表",
             "Day 55 錯題重聽\n確認都聽懂了"),
            ("Day 57\n(一)", "Phase 2 小測驗\n\n閱讀 100 題\n限時 75 分鐘\n\n嚴格計時！\n分數：___/100",
             "",
             "Phase 2 小測驗\n\n聽力 100 題\n限時 45 分鐘\n\n分數：___/100"),
            ("Day 58\n(二)", "詳細檢討\nPhase 2 測驗\n\n閱讀錯題逐題分析\n找出所有弱點\n\n與 Phase 1 測驗\n比較進步幅度",
             "制定 Phase 3 策略\n\n根據測驗結果：\n□ 需要加強哪個 Part\n□ 哪種題型最弱\n□ 時間分配是否合理",
             "聽力錯題分析\n\n對比 Phase 1：\n□ 進步了哪些\n□ 還需加強哪些"),
            ("Day 59\n(三)", "弱項最後補強\n\n針對測驗發現的\n弱點做集中練習",
             "弱項補強",
             "弱項補強"),
            ("Day 60\n(四)", "【休息日】\n\n準備進入衝刺期\n\n心理建設：\n你已經完成 2/3！",
             "休息",
             "休息"),
        ],
    },
    # ── Phase 3: 模擬衝刺 ──
    {
        "week": 9,
        "phase": "Phase 3：模擬衝刺",
        "title": "第一回模擬考 + 深度檢討",
        "dates": "Day 61-67（6/6 - 6/12）",
        "goal": "完成第一次完整模擬考，深度分析所有錯題，找出最後弱點",
        "daily_time": "每日 90-120 分鐘（早 10 min 單字 / 午 50-60 min 模擬或分項 / 晚 30 min 檢討 / 睡前 15 min 泛聽）",
        "days": [
            ("Day 61\n(五)", "完整模擬考 #1\n\n200 題 / 120 分鐘\n\n嚴格模擬考場：\n- 手機關靜音\n- 不中途休息\n- 用鉛筆畫卡\n- 嚴格計時",
             "聽力 100 題 45 min\n→ 休息 5 min\n→ 閱讀 100 題 75 min\n\n聽力：___/100\n閱讀：___/100\n\n預估總分：___",
             ""),
            ("Day 62\n(六)", "檢討模擬考 #1\n聽力部分\n\n每一題都要：\n1. 重新聽一次\n2. 看原文確認\n3. 分析錯誤原因\n\nPart 1：___/6\nPart 2：___/25\nPart 3：___/39\nPart 4：___/30",
             "聽力錯因分類\n\n□ 單字不認識\n□ 聽不清楚發音\n□ 速度太快跟不上\n□ 被相似音誤導\n□ 沒有預讀題目\n□ 粗心",
             "精聽練習\n\n選 5 題錯題\n反覆聽 3 次以上\n直到完全聽懂"),
            ("Day 63\n(日)", "檢討模擬考 #1\n閱讀部分\n\n每一題都要：\n1. 重新讀文章\n2. 確認答案位置\n3. 分析錯誤原因\n\nPart 5：___/30\nPart 6：___/16\nPart 7：___/54",
             "閱讀錯因分類\n\n□ 單字不認識\n□ 文法觀念錯誤\n□ 文章讀不懂\n□ 時間不夠\n□ 定位不到答案\n□ 粗心",
             "泛聽練習 30 min\n\n聽 BBC 或 VOA\n不需要全聽懂\n培養語感"),
            ("Day 64\n(一)", "弱項 Part 集中訓練\n\n根據模擬考結果\n選最弱的 Part\n做 30 題以上\n\n重點：搞懂為什麼錯",
             "文法弱點補強\n\n回顧模擬考中\n錯的文法考點\n\n再做 15 題相關練習",
             "聽力弱項 Part\n集中練習 15 題"),
            ("Day 65\n(二)", "Part 5 限時 x30\n【嚴格 10 分鐘】\n\n目標：20 秒/題\n快速判斷→快速選\n\nPart 5 越快\nPart 7 時間越多",
             "Part 7 x4 篇\n\n用省下來的時間\n好好讀 Part 7\n\n目標：每篇 3-4 min",
             "Part 3+4 精聽\n選 3 段完整對話\n/獨白\n\n聽→寫筆記→\n對答案→重聽"),
            ("Day 66\n(三)", "Part 3+4 精聽\n\n聽完整段寫筆記\n練習抓關鍵資訊：\nwho/what/when/\nwhere/why/how",
             "閱讀速度訓練\n\n用 toeic-trainer\n目標：130 WPM\n\n逐步提升速度",
             "泛聽 15 min\n放鬆"),
            ("Day 67\n(四)", "【休息日】\n\n看英文影片放鬆\n保持語感就好",
             "休息",
             "休息"),
        ],
    },
    {
        "week": 10,
        "phase": "Phase 3：模擬衝刺",
        "title": "第二回模擬考 + 進步追蹤",
        "dates": "Day 68-74（6/13 - 6/19）",
        "goal": "第二次模擬考，對比第一次找進步點和剩餘弱點",
        "daily_time": "每日 90-120 分鐘",
        "days": [
            ("Day 68\n(五)", "完整模擬考 #2\n\n200 題 / 120 分鐘\n\n同樣嚴格模擬\n\n聽力：___/100\n閱讀：___/100\n預估總分：___",
             "對比模擬考 #1\n\n#1 聽力：___ → #2：___\n#1 閱讀：___ → #2：___\n#1 總分：___ → #2：___\n\n進步了嗎？",
             ""),
            ("Day 69\n(六)", "檢討模擬考 #2\n聽力部分\n\n重點放在：\n#1 錯但 #2 也錯的題\n→ 這是真正的弱點\n\n#1 錯但 #2 對了\n→ 有進步，繼續保持",
             "聽力進步分析\n\nPart 1：#1___→#2___\nPart 2：#1___→#2___\nPart 3：#1___→#2___\nPart 4：#1___→#2___",
             "弱項 Part 加強\n15 題"),
            ("Day 70\n(日)", "檢討模擬考 #2\n閱讀部分\n\n分析閱讀速度：\n75 分鐘內做完了嗎？\n還剩幾題沒做？\n\n速度 vs 正確率\n找到平衡點",
             "閱讀進步分析\n\nPart 5：#1___→#2___\nPart 6：#1___→#2___\nPart 7：#1___→#2___\n\n時間分配改善了嗎？",
             "泛聽 30 min"),
            ("Day 71\n(一)", "Part 6+7 集中訓練\n\nPart 6 x4 篇\nPart 7 單篇 x3\n\n練長文閱讀耐力\n不要中途停下來",
             "閱讀策略微調\n\n如果 Part 7 還是\n時間不夠：\n→ Part 5+6 再加速\n→ Part 7 先做單篇\n→ 三篇最後做",
             "Part 4 x4\n\n獨白類型辨識\n和資訊擷取"),
            ("Day 72\n(二)", "Part 2+3 集中訓練\n\nPart 2 x15\nPart 3 x9（3 組）\n\n練問答反應速度\n聽到就選，不猶豫",
             "Part 2 技巧複習\n\n陷阱：\n1. 相似音選項\n2. 間接回答\n3. Yes/No 不一定對\n\n聽第一個字最重要",
             "Part 3 預讀練習\n\n計時：8 秒內\n讀完 3 題+選項"),
            ("Day 73\n(三)", "易錯文法總複習\n\n把錯題本中\n所有文法錯題\n重新做一遍\n\n高頻單字複習\n300 字快速掃描",
             "製作考前速查卡\n\n把最容易忘的\n10 個文法規則\n+ 20 個高頻搭配\n寫在一張紙上",
             "泛聽 + 跟讀\n30 min\n\n跟著音檔唸\n提升語感"),
            ("Day 74\n(四)", "【休息日】",
             "休息",
             "休息"),
        ],
    },
    {
        "week": 11,
        "phase": "Phase 3：模擬衝刺",
        "title": "第三回模擬考 + 精練",
        "dates": "Day 75-81（6/20 - 6/26）",
        "goal": "第三次模擬考目標：聽力 300+、閱讀 230+、總分 530+",
        "daily_time": "每日 90-120 分鐘",
        "days": [
            ("Day 75\n(五)", "完整模擬考 #3\n\n200 題 / 120 分鐘\n\n目標分數：\n聽力 300+\n閱讀 230+\n總分 530+\n\n實際分數：\n聽力：___\n閱讀：___",
             "三次模擬比較\n\n#1：___→#2：___→#3：___\n\n趨勢分析：\n□ 穩定進步\n□ 停滯需調整\n□ 某 Part 退步",
             ""),
            ("Day 76\n(六)", "檢討模擬考 #3\n全部\n\n這次要特別注意：\n1. 反覆錯的題型\n2. 時間分配問題\n3. 粗心錯誤\n\n找出最後漏洞",
             "最終弱點清單\n\n列出所有還需要\n加強的地方\n（最多 5 項）\n\n這是最後要攻克的",
             "泛聽 30 min"),
            ("Day 77\n(日)", "閱讀速度訓練\n\n用 toeic-trainer\n速讀功能\n目標：150 WPM\n\n練 3-4 篇文章\n不要回頭讀",
             "閱讀理解練習\n\n讀完後回答問題\n不看文章作答\n\n訓練記憶力\n和理解力",
             "聽力泛聽\n練語感"),
            ("Day 78\n(一)", "Part 5 衝刺\nx60 題\n【限時 20 分鐘】\n\n目標：20 秒/題\n正確率 75%+\n\n分數：___/60\n時間：___min",
             "檢討 + 分析\n\n哪些題秒殺？\n哪些題猶豫？\n\n猶豫的題型\n= 還需加強的",
             "Part 2 x20\n快速反應訓練"),
            ("Day 79\n(二)", "Part 7 雙篇 x2\n+ 三篇 x1\n\n這是最易丟分的\n一定要練！\n\n目標：15 min 完成",
             "交叉比對技巧\n\n練習在兩篇/三篇\n之間快速切換\n找對應資訊",
             "Part 3+4 x8\n\n保持手感"),
            ("Day 80\n(三)", "Part 3+4 密集聽力\n\nPart 3 x9\nPart 4 x6\n\n重點：預讀技巧\n每次間隔都要\n先讀下組題目",
             "精聽 + 跟讀\n\n選 3 段錯題\n聽→跟讀→\n再聽→再跟讀\n\n直到能完整\n跟上速度",
             "泛聽 15 min\n放鬆"),
            ("Day 81\n(四)", "【休息日】\n\n最後一週衝刺前\n好好休息\n\n整理所有筆記\n準備最終複習",
             "休息",
             "休息"),
        ],
    },
    {
        "week": 12,
        "phase": "Phase 3：模擬衝刺",
        "title": "最終模擬考 + 考前總複習",
        "dates": "Day 82-88（6/27 - 7/3）",
        "goal": "最後一次模擬考確認狀態，考前減量保持手感，調整身心",
        "daily_time": "逐漸減量：90 min → 60 min → 30 min",
        "days": [
            ("Day 82\n(五)", "完整模擬考 #4\n（最終模擬）\n\n200 題 / 120 分鐘\n\n這是最後一次模擬\n用最佳狀態應考\n\n聽力：___\n閱讀：___\n總分：___",
             "四次模擬總比較\n\n#1→#2→#3→#4\n___→___→___→___\n\n你進步了多少？\n對自己有信心！",
             ""),
            ("Day 83\n(六)", "檢討模擬考 #4\n\n最後一次全面檢討\n\n把所有錯題\n分類整理：\n□ 一定要記住的\n□ 運氣不好的\n□ 可以放棄的",
             "製作考前必看\n重點整理（1 頁）\n\n考前 30 分鐘\n看這張就好：\n- 5 個文法規則\n- 10 個高頻搭配\n- 答題時間分配",
             "泛聽 30 min"),
            ("Day 84\n(日)", "全錯題本複習\n（聽力篇）\n\n重新聽所有\n做錯過的聽力題\n\n確認每一題\n都聽懂了",
             "聽力答題策略\n最終確認\n\nPart 1：看圖想詞\nPart 2：聽首字\nPart 3：預讀題目\nPart 4：邊聽邊選",
             "精聽最弱的\n5 題"),
            ("Day 85\n(一)", "全錯題本複習\n（閱讀篇）\n\n重新做所有\n做錯過的閱讀題\n\n確認每一題\n都理解了",
             "閱讀答題策略\n最終確認\n\nPart 5：30 秒/題\nPart 6：1 分/題\nPart 7：先看題\n\n不確定就先選\n做記號回來看",
             "泛聽 15 min\n放鬆"),
            ("Day 86\n(二)", "高頻單字\n最後快速掃描\n\n300 字清單\n不熟的標記\n考前再看一次",
             "文法重點\n最後快速掃描\n\n看考前重點整理\n確認都記住了",
             "輕鬆聽英文\n歌曲或影片\n30 min"),
            ("Day 87\n(三)", "輕量練習\n\nPart 1 x5\nPart 2 x5\nPart 5 x10\n\n只是保持手感\n不要太累！",
             "考前策略複習\n\n時間分配確認：\n聽力 45 min（自動）\n閱讀 75 min\n P5: 10 min\n P6: 10 min\n P7: 55 min",
             "輕鬆聽英文\n15 min"),
            ("Day 88\n(四)", "【考前放鬆日】\n\n不做新題！\n\n只看考前重點整理\n確認考場資訊\n準備文具（2B鉛筆\n橡皮擦、手錶）",
             "考試注意事項：\n\n□ 帶身分證\n□ 准考證\n□ 2B 鉛筆（多支）\n□ 橡皮擦\n□ 手錶（非智慧型）\n□ 早點睡",
             "完全休息\n不聽英文\n\n早睡！"),
        ],
    },
    {
        "week": 13,
        "phase": "Phase 3：模擬衝刺",
        "title": "考前最後衝刺 + 考試日",
        "dates": "Day 89-90（7/4 - 7/6）",
        "goal": "保持最佳狀態，自信應考，目標 550+！",
        "daily_time": "最少量或休息",
        "days": [
            ("Day 89\n(五)", "【考前一天】\n\n只看考前重點整理\n不做新題目\n\n確認：\n□ 考場怎麼去\n□ 幾點到\n□ 東西都準備好了",
             "心理準備\n\n你已經準備了\n89 天！\n\n相信自己的努力\n放鬆心情",
             "完全休息\n\n早睡早起\n明天全力以赴！"),
            ("Day 90\n(六)", "考試日！\n\n早餐吃飽\n提早到考場\n\n考前 10 分鐘\n深呼吸放鬆\n看一眼重點整理",
             "應考提醒：\n\n1. 不會的先跳過\n2. 絕不留空白\n3. 聽力跟著節奏走\n4. 閱讀注意時間\n5. 相信直覺\n\n你可以的！",
             "考完之後：\n\n恭喜完成 90 天\n訓練計畫！\n\n不管結果如何\n你已經很棒了\n\n目標 550+\n期待好消息！"),
        ],
    },
]


class ToeicPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="A4")
        self.add_font("ch", "", FONT_PATH)
        self.add_font("ch", "B", FONT_PATH)  # bold fallback

    def header_block(self, week_data):
        # Title bar
        self.set_fill_color(41, 98, 255)
        self.set_text_color(255, 255, 255)
        self.set_font("ch", size=18)
        self.cell(0, 14, f"  TOEIC 90 Day Plan  |  Week {week_data['week']}：{week_data['title']}", fill=True, new_x="LMARGIN", new_y="NEXT")

        # Phase + dates bar
        self.set_fill_color(230, 240, 255)
        self.set_text_color(41, 98, 255)
        self.set_font("ch", size=11)
        self.cell(0, 9, f"  {week_data['phase']}  |  {week_data['dates']}  |  {week_data['daily_time']}", fill=True, new_x="LMARGIN", new_y="NEXT")

        # Goal
        self.set_fill_color(255, 248, 220)
        self.set_text_color(180, 120, 0)
        self.set_font("ch", size=10)
        self.cell(0, 8, f"  Goal：{week_data['goal']}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def table_header(self):
        self.set_fill_color(50, 50, 70)
        self.set_text_color(255, 255, 255)
        self.set_font("ch", size=10)
        col_widths = [28, 85, 85, 79]
        headers = ["Day", "Vocabulary / Reading", "Grammar / Strategy", "Listening"]
        for w, h in zip(col_widths, headers):
            self.cell(w, 8, f" {h}", border=1, fill=True)
        self.ln()

    def day_row(self, day_data, row_idx):
        day_label, col1, col2, col3 = day_data
        col_widths = [28, 85, 85, 79]
        contents = [day_label, col1, col2, col3]

        # Calculate row height
        line_counts = []
        for i, text in enumerate(contents):
            lines = text.split("\n") if text else [""]
            # estimate wrapping
            w = col_widths[i] - 4
            total_lines = 0
            for line in lines:
                if not line:
                    total_lines += 1
                else:
                    chars_per_line = max(w // 3, 1)  # rough estimate for CJK
                    total_lines += max(1, -(-len(line) // chars_per_line))
            line_counts.append(total_lines)

        row_h = max(max(line_counts) * 4.5, 18)
        row_h = min(row_h, 52)  # cap height

        # Check if we need a new page
        if self.get_y() + row_h > self.h - 15:
            self.add_page()
            self.table_header()

        x_start = self.get_x()
        y_start = self.get_y()

        # Draw all cell backgrounds first
        if row_idx % 2 == 0:
            self.set_fill_color(248, 249, 252)
        else:
            self.set_fill_color(255, 255, 255)

        for i in range(len(col_widths)):
            cx = x_start + sum(col_widths[:i])
            self.set_draw_color(200, 200, 200)
            self.rect(cx, y_start, col_widths[i], row_h, "DF")

        # Then draw text on top
        for i, (w, text) in enumerate(zip(col_widths, contents)):
            cx = x_start + sum(col_widths[:i])

            # Write text
            self.set_xy(cx + 2, y_start + 1.5)
            if i == 0:
                self.set_font("ch", size=8)
                self.set_text_color(41, 98, 255)
            else:
                self.set_font("ch", size=7)
                self.set_text_color(40, 40, 40)
            self.multi_cell(w - 4, 3.8, text or "", border=0)

        self.set_xy(x_start, y_start + row_h)


def generate_pdfs():
    for week_data in weeks:
        pdf = ToeicPDF()
        pdf.set_auto_page_break(auto=True, margin=12)
        pdf.add_page()
        pdf.header_block(week_data)
        pdf.table_header()

        for idx, day in enumerate(week_data["days"]):
            pdf.day_row(day, idx)

        # Footer with tips
        pdf.ln(5)
        pdf.set_font("ch", size=8)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 5, f"TOEIC 90-Day Plan | Week {week_data['week']} of 13 | Target: 550+ | Tool: https://q896321-bit.github.io/toeic-trainer/",
                 new_x="LMARGIN", new_y="NEXT")

        filename = f"week{week_data['week']:02d}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)
        pdf.output(filepath)
        print(f"Generated: {filename}")

    print(f"\nAll {len(weeks)} weekly PDFs generated in {OUTPUT_DIR}/")


if __name__ == "__main__":
    generate_pdfs()
