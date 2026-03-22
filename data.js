// ===== TOEIC 訓練題庫資料 =====
const TOEIC_DATA = {

    // ===== 各等級核心單字 =====
    vocabulary: {
        450: [
            { word: "schedule", meaning: "時間表；行程", example: "Please check the meeting schedule.", emoji: "📅", image: "calendar with dates marked" },
            { word: "available", meaning: "可用的；有空的", example: "Is this room available tomorrow?", emoji: "✅", image: "open door with green light" },
            { word: "purchase", meaning: "購買", example: "You can purchase tickets online.", emoji: "🛒", image: "shopping cart with items" },
            { word: "deliver", meaning: "遞送", example: "We will deliver the package by Friday.", emoji: "📦", image: "delivery truck" },
            { word: "attend", meaning: "參加；出席", example: "Will you attend the conference?", emoji: "🙋", image: "person raising hand" },
            { word: "confirm", meaning: "確認", example: "Please confirm your reservation.", emoji: "✔️", image: "checkmark on document" },
            { word: "announce", meaning: "宣布", example: "The company announced a new product.", emoji: "📢", image: "megaphone" },
            { word: "recommend", meaning: "推薦", example: "I recommend this restaurant.", emoji: "👍", image: "thumbs up" },
            { word: "require", meaning: "需要；要求", example: "This job requires experience.", emoji: "📋", image: "checklist" },
            { word: "arrange", meaning: "安排", example: "I'll arrange a meeting for next week.", emoji: "🗂️", image: "organized folders" },
            { word: "increase", meaning: "增加", example: "Sales increased by 20%.", emoji: "📈", image: "rising graph" },
            { word: "expect", meaning: "預期；期待", example: "We expect the report by Monday.", emoji: "⏳", image: "hourglass" },
            { word: "receive", meaning: "收到", example: "Did you receive my email?", emoji: "📬", image: "mailbox" },
            { word: "provide", meaning: "提供", example: "We provide free shipping.", emoji: "🤝", image: "handshake" },
            { word: "include", meaning: "包含", example: "The price includes tax.", emoji: "📎", image: "box of items" },
            { word: "apply", meaning: "申請；應用", example: "She applied for the position.", emoji: "📝", image: "application form" },
            { word: "select", meaning: "選擇", example: "Please select your preferred date.", emoji: "👆", image: "pointing finger" },
            { word: "request", meaning: "請求；要求", example: "He requested a day off.", emoji: "🙏", image: "person asking" },
            { word: "complete", meaning: "完成", example: "Please complete the form.", emoji: "🏁", image: "finish flag" },
            { word: "prepare", meaning: "準備", example: "We need to prepare for the presentation.", emoji: "🔧", image: "tools ready" },
        ],
        550: [
            { word: "negotiate", meaning: "協商；談判", example: "They are negotiating the contract terms.", emoji: "🤝", image: "two people discussing" },
            { word: "implement", meaning: "實施；執行", example: "We will implement the new policy next month.", emoji: "⚙️", image: "gears turning" },
            { word: "estimate", meaning: "估計", example: "The estimated cost is $5,000.", emoji: "🔢", image: "calculator" },
            { word: "contribute", meaning: "貢獻；捐獻", example: "She contributed to the project's success.", emoji: "🎁", image: "puzzle piece" },
            { word: "distribute", meaning: "分配；分發", example: "The report will be distributed to all departments.", emoji: "📤", image: "arrows spreading" },
            { word: "demonstrate", meaning: "展示；證明", example: "He demonstrated how to use the software.", emoji: "🖥️", image: "screen presentation" },
            { word: "evaluate", meaning: "評估", example: "We need to evaluate the proposal carefully.", emoji: "🔍", image: "magnifying glass" },
            { word: "generate", meaning: "產生；創造", example: "The campaign generated a lot of interest.", emoji: "💡", image: "lightbulb" },
            { word: "maintain", meaning: "維持；保養", example: "It's important to maintain good customer relations.", emoji: "🔧", image: "wrench" },
            { word: "qualify", meaning: "使合格；有資格", example: "Do you qualify for the discount?", emoji: "🏅", image: "medal" },
            { word: "submit", meaning: "提交", example: "Please submit your application by Friday.", emoji: "📩", image: "sending envelope" },
            { word: "establish", meaning: "建立", example: "The company was established in 1990.", emoji: "🏗️", image: "building foundation" },
            { word: "indicate", meaning: "指出；表明", example: "The survey indicates growing demand.", emoji: "👉", image: "pointing at chart" },
            { word: "transfer", meaning: "轉移；調動", example: "He was transferred to the Tokyo office.", emoji: "✈️", image: "moving arrow" },
            { word: "assume", meaning: "假設；承擔", example: "I assume you've read the report.", emoji: "🤔", image: "thinking person" },
            { word: "resolve", meaning: "解決", example: "We need to resolve this issue quickly.", emoji: "🧩", image: "puzzle fitting" },
            { word: "authorize", meaning: "授權", example: "Only managers are authorized to approve expenses.", emoji: "🔑", image: "key" },
            { word: "ensure", meaning: "確保", example: "Please ensure all documents are signed.", emoji: "🛡️", image: "shield" },
            { word: "acquire", meaning: "獲得；收購", example: "The firm acquired a smaller company.", emoji: "🏢", image: "buildings merging" },
            { word: "allocate", meaning: "分配", example: "Funds were allocated for the project.", emoji: "💰", image: "money divided" },
        ],
        650: [
            { word: "comply", meaning: "遵守", example: "All employees must comply with safety regulations.", emoji: "📜", image: "rulebook" },
            { word: "fluctuate", meaning: "波動", example: "Stock prices fluctuated throughout the day.", emoji: "📊", image: "zigzag graph" },
            { word: "scrutinize", meaning: "仔細檢查", example: "The auditor scrutinized every transaction.", emoji: "🔬", image: "microscope" },
            { word: "consolidate", meaning: "合併；鞏固", example: "The company consolidated its operations.", emoji: "🔗", image: "chains linking" },
            { word: "expedite", meaning: "加速處理", example: "We need to expedite the shipping process.", emoji: "⚡", image: "lightning bolt" },
            { word: "comprehensive", meaning: "全面的", example: "A comprehensive review was conducted.", emoji: "🌐", image: "globe" },
            { word: "consecutive", meaning: "連續的", example: "Sales grew for five consecutive quarters.", emoji: "⏩", image: "dominoes" },
            { word: "preliminary", meaning: "初步的", example: "The preliminary results look promising.", emoji: "🌱", image: "seedling" },
            { word: "sustainable", meaning: "可持續的", example: "We aim for sustainable growth.", emoji: "♻️", image: "recycling" },
            { word: "mandatory", meaning: "強制的", example: "Attendance is mandatory for all staff.", emoji: "⚠️", image: "warning sign" },
            { word: "forthcoming", meaning: "即將到來的", example: "Details about the forthcoming event will follow.", emoji: "🔜", image: "approaching arrow" },
            { word: "subsequent", meaning: "隨後的", example: "Subsequent meetings confirmed the plan.", emoji: "⏭️", image: "next step" },
            { word: "tentative", meaning: "暫定的", example: "We set a tentative date for the launch.", emoji: "❓", image: "question calendar" },
            { word: "adjacent", meaning: "相鄰的", example: "The parking lot is adjacent to the building.", emoji: "🏘️", image: "side by side" },
            { word: "refurbish", meaning: "翻新", example: "The hotel lobby was recently refurbished.", emoji: "🔨", image: "hammer renovation" },
            { word: "oversight", meaning: "監督；疏忽", example: "Due to an oversight, the invoice was not sent.", emoji: "👁️", image: "watching eye" },
            { word: "liability", meaning: "責任；負債", example: "The company has significant liabilities.", emoji: "⚖️", image: "balance scale" },
            { word: "credential", meaning: "資格證明", example: "Please present your credentials at the gate.", emoji: "🪪", image: "ID badge" },
            { word: "incentive", meaning: "獎勵；激勵", example: "The company offers performance incentives.", emoji: "🏆", image: "trophy" },
            { word: "benchmark", meaning: "基準", example: "This serves as a benchmark for future projects.", emoji: "📏", image: "ruler" },
        ],
        750: [
            { word: "deteriorate", meaning: "惡化", example: "The situation could deteriorate further.", emoji: "📉", image: "cracking surface" },
            { word: "unprecedented", meaning: "史無前例的", example: "The company achieved unprecedented growth.", emoji: "🚀", image: "rocket" },
            { word: "meticulous", meaning: "一絲不苟的", example: "She is meticulous about quality control.", emoji: "🎯", image: "bullseye" },
            { word: "proprietary", meaning: "專有的", example: "This is proprietary technology.", emoji: "🔒", image: "padlock" },
            { word: "circumvent", meaning: "規避", example: "They tried to circumvent the regulations.", emoji: "🔄", image: "going around" },
            { word: "substantiate", meaning: "證實", example: "Can you substantiate your claims?", emoji: "📑", image: "evidence stack" },
            { word: "intermittent", meaning: "間歇的", example: "We experienced intermittent connectivity issues.", emoji: "💫", image: "blinking signal" },
            { word: "commensurate", meaning: "相稱的", example: "Salary is commensurate with experience.", emoji: "⚖️", image: "balanced scale" },
            { word: "contingent", meaning: "取決於…的", example: "The deal is contingent on board approval.", emoji: "🔀", image: "fork road" },
            { word: "discrepancy", meaning: "差異；不一致", example: "There is a discrepancy in the financial report.", emoji: "❌", image: "mismatched pieces" },
            { word: "lucrative", meaning: "利潤豐厚的", example: "They secured a lucrative contract.", emoji: "💎", image: "diamond" },
            { word: "implication", meaning: "含意；影響", example: "Consider the implications of this decision.", emoji: "🌊", image: "ripple effect" },
            { word: "procurement", meaning: "採購", example: "The procurement department handles all purchases.", emoji: "🛍️", image: "shopping bags" },
            { word: "reimbursement", meaning: "報銷", example: "Submit receipts for travel reimbursement.", emoji: "🧾", image: "receipt" },
            { word: "stipulate", meaning: "規定", example: "The contract stipulates a 30-day notice period.", emoji: "📃", image: "contract" },
            { word: "amalgamate", meaning: "合併", example: "The two departments were amalgamated.", emoji: "🔗", image: "merging circles" },
            { word: "disseminate", meaning: "散布；傳播", example: "Information was disseminated to all branches.", emoji: "📡", image: "broadcast signal" },
            { word: "corroborate", meaning: "證實", example: "Evidence corroborated his statement.", emoji: "✅", image: "two checkmarks" },
            { word: "remedial", meaning: "補救的", example: "Remedial action was taken immediately.", emoji: "🩹", image: "bandage" },
            { word: "viable", meaning: "可行的", example: "Is this a viable business plan?", emoji: "✨", image: "green light" },
        ],
    },

    // ===== 文法 =====
    grammar: {
        450: [
            { topic: "主詞動詞一致", explanation: "主詞和動詞在數量上必須一致。單數主詞用單數動詞，複數主詞用複數動詞。", questions: [
                { q: "The list of items ______ on the desk.", options: ["is", "are", "were", "have been"], answer: 0, explanation: "主詞是 'list'（單數），不是 'items'，所以用 'is'。" },
                { q: "Every employee ______ required to attend the meeting.", options: ["are", "is", "were", "have"], answer: 1, explanation: "'Every' 後面接單數名詞，動詞也用單數形式。" }
            ]},
            { topic: "時態基礎", explanation: "現在簡單式用於習慣、事實；現在進行式用於正在進行的動作。", questions: [
                { q: "The company ______ new employees every spring.", options: ["is hiring", "hires", "hired", "will hiring"], answer: 1, explanation: "'every spring' 表示習慣性動作，用現在簡單式。" },
                { q: "She ______ on a new project right now.", options: ["works", "is working", "worked", "has work"], answer: 1, explanation: "'right now' 表示正在進行，用現在進行式。" }
            ]}
        ],
        550: [
            { topic: "被動語態", explanation: "被動語態：be + 過去分詞。強調動作的接受者而非執行者。", questions: [
                { q: "The report ______ by the end of this week.", options: ["will complete", "will be completed", "completes", "completing"], answer: 1, explanation: "報告是被完成的，用被動語態。" },
                { q: "All applicants ______ notified of the results.", options: ["will be", "will", "are being to", "have to"], answer: 0, explanation: "申請者是被通知的，用被動語態。" }
            ]},
            { topic: "關係子句", explanation: "who 指人、which 指物、that 兩者皆可、where 指地點。", questions: [
                { q: "The employee ______ submitted the report has been promoted.", options: ["which", "who", "whom", "where"], answer: 1, explanation: "先行詞 employee（人），當主詞用 who。" },
                { q: "The office ______ we held the meeting is on the third floor.", options: ["which", "who", "where", "that"], answer: 2, explanation: "先行詞 office（地點），用 where。" }
            ]}
        ],
        650: [
            { topic: "假設語氣", explanation: "If + 過去式, would + 原形動詞（與現在事實相反）。", questions: [
                { q: "If the company ______ more funds, it could expand overseas.", options: ["has", "had", "have", "having"], answer: 1, explanation: "與現在事實相反的假設用過去式。" },
                { q: "I wish I ______ at the conference last week.", options: ["am", "was", "had been", "would be"], answer: 2, explanation: "與過去事實相反的願望用 had + 過去分詞。" }
            ]},
            { topic: "分詞構句", explanation: "用現在分詞（Ving）或過去分詞（Vpp）開頭簡化從屬子句。", questions: [
                { q: "______ the results, the team decided to change the strategy.", options: ["Review", "Reviewed", "Having reviewed", "To review"], answer: 2, explanation: "先檢視再決定，用 Having reviewed。" },
                { q: "______ in 1995, the company has grown significantly.", options: ["Found", "Founded", "Founding", "Having found"], answer: 1, explanation: "公司是「被」成立的，用過去分詞。" }
            ]}
        ],
        750: [
            { topic: "倒裝句", explanation: "否定副詞放句首時，主詞和助動詞需倒裝。", questions: [
                { q: "Not only ______ the deadline, but she also exceeded expectations.", options: ["she met", "did she meet", "she did meet", "met she"], answer: 1, explanation: "Not only 放句首需倒裝。" },
                { q: "Rarely ______ such a thorough report.", options: ["we see", "do we see", "we do see", "see we"], answer: 1, explanation: "Rarely 放句首需倒裝。" }
            ]},
            { topic: "複雜連接詞", explanation: "notwithstanding, in lieu of, pursuant to 等進階用法。", questions: [
                { q: "______ the recent budget cuts, the project will continue.", options: ["Notwithstanding", "Although", "Despite of", "In spite"], answer: 0, explanation: "Notwithstanding = despite，後接名詞。" },
                { q: "A bonus will be given ______ the completion of the project.", options: ["upon", "while", "during", "for"], answer: 0, explanation: "upon + 名詞 = 在…之時。" }
            ]}
        ]
    },

    // ===== 聽力/閱讀技巧 =====
    listeningTips: {
        450: ["照片描述題：先快速看圖，注意人物動作、位置、物品。","聽到 'Where is...' 的問題，答案通常是地點，不是 Yes/No。","注意聽關鍵字：when, where, who, what, how。","不要因為聽到某個字就急著選，要聽完整個句子。","練習分辨相似音：work/walk, right/light, three/free。"],
        550: ["短對話：注意第二位說話者的回應，答案常在那裡。","聽到轉折詞 but, however, actually 後面通常是重點。","注意說話者的語氣，幫助判斷態度和意圖。","練習聽數字、日期、時間，這些常是考點。","獨白題先看選項，預測內容方向。"],
        650: ["注意間接回答：暗示性的答案。","圖表配合聽力：先看圖表數據，找對應資訊。","練習聽懂改述（paraphrase）。","三人對話區分每個人的立場。","注意暗示與推論題。"],
        750: ["一邊聽一邊做筆記。","注意說話者意圖題。","學會排除法。","熟悉不同英語口音差異。","練習短時間內切換主題的理解能力。"]
    },
    readingTips: {
        450: ["先看題目再讀文章。","信件/Email：注意 From, To, Subject。","注意因果連接詞 because, therefore, so。","不認識的字用上下文猜意思。","表格題：先讀標題和表頭。"],
        550: ["每天練習計時閱讀，目標 150 字/分鐘。","雙篇閱讀：先各讀大意，再找關聯。","注意代名詞 this, that, these 指什麼。","同義替換是核心考法。","識別文章類型：公告、信件、廣告、報導。"],
        650: ["三篇組合：先快速掃過理解關係。","推論題需根據線索推斷。","插入句題看前後文邏輯。","NOT/TRUE 題逐一比對原文。","練習 75 分鐘完成全部閱讀。"],
        750: ["整合多來源資訊，跨文章找答案。","語氣/目的題：作者用意是什麼？","注意例外情況和條件限制。","詞義題：上下文判斷一詞多義。","模擬考試訓練 2 小時專注力。"]
    },

    // ===== 閱讀練習 =====
    readingExercises: {
        450: [{ type: "notice", passage: "NOTICE TO ALL EMPLOYEES\n\nThe company parking lot will be closed for repairs from March 15 to March 20. During this time, employees may use the public parking garage on Oak Street. The company will provide parking vouchers at the front desk. Please pick up your vouchers before March 14.\n\nFor questions, contact the Facilities Department at ext. 2450.", questions: [
            { q: "How long will the parking lot be closed?", options: ["3 days","5 days","6 days","1 week"], answer: 2, explanation: "March 15 到 March 20 是 6 天。" },
            { q: "Where can employees park?", options: ["At home","On Oak Street garage","Train station","Basement"], answer: 1, explanation: "'public parking garage on Oak Street'。" }
        ]}],
        550: [{ type: "email", passage: "From: Sarah Chen <s.chen@globaltech.com>\nTo: All Marketing Staff\nSubject: Q3 Marketing Campaign Update\n\nDear Team,\n\nI'm pleased to report that our Q3 digital marketing campaign has exceeded expectations. Website traffic increased by 35%, and we generated 2,000 new leads. However, our social media engagement was below target by 10%.\n\nFor Q4, I'd like to focus on improving our social media strategy. Please prepare your proposals by October 5.\n\nA planning meeting is scheduled for October 10 at 2 PM in Conference Room B.\n\nBest regards,\nSarah Chen\nMarketing Director", questions: [
            { q: "What was the main problem with Q3?", options: ["Low traffic","Not enough leads","Poor social media","Over budget"], answer: 2, explanation: "'social media engagement was below target by 10%'。" },
            { q: "What should employees do before October 5?", options: ["Attend meeting","Submit proposals","Review data","Contact Sarah"], answer: 1, explanation: "'prepare your proposals by October 5'。" }
        ]}],
        650: [{ type: "article", passage: "Remote Work Trends in 2024\n\nA recent survey found that 62% of companies now offer hybrid work, up from 45% in 2022. In North America, 78% of tech companies have permanent remote policies. However, in manufacturing, only 23% offer remote options.\n\nEmployee satisfaction with hybrid work declined from 84% to 79%, largely due to communication challenges. Companies investing in collaboration tools reported higher satisfaction.\n\nDr. Lopez noted: \"Organizations that find the right balance will have a competitive advantage in attracting talent.\"", questions: [
            { q: "What can be inferred about manufacturing?", options: ["Fully remote","Most jobs need presence","Higher satisfaction","Surveyed more"], answer: 1, explanation: "只有 23% 提供遠端，可推斷大部分需到場。" },
            { q: "What gives companies an advantage?", options: ["All in-office","Fully remote","Right hybrid balance","Cut tool costs"], answer: 2, explanation: "'find the right balance'。" }
        ]}],
        750: [{ type: "double-passage", passage: "PASSAGE 1 - Memo\nTo: Department Heads\nFrom: CFO James Park\n\nStarting FY2025, each department must submit a zero-based budget. Training sessions: November 15-17. Attendance mandatory.\n\n---\n\nPASSAGE 2 - Article\nZero-based budgeting forces managers to justify every dollar. Critics say it's time-consuming and may cut innovation. A McKinley study found 15% cost savings but 7% R&D decline over three years.", questions: [
            { q: "Potential risk of the new policy?", options: ["Miss training","R&D could decrease","Board reversal","Managers refuse"], answer: 1, explanation: "ZBB 導致 R&D 下降 7%。" },
            { q: "What does 'incremental' budgeting mean?", options: ["Project milestones","Based on previous year","Zero spending","Competitor analysis"], answer: 1, explanation: "與 zero-based 對比，是基於前年調整。" }
        ]}]
    },

    // ===== 聽力練習 =====
    listeningExercises: {
        450: [
            { type: "short-dialogue", script: "Woman: Excuse me, where is the nearest post office? Man: It's on Main Street, next to the bank. Woman: Thank you. Is it open on Saturdays? Man: Yes, but only until noon.", questions: [
                { q: "Where is the post office?", options: ["Next to the bank on Main Street","Inside the bank","On Oak Street","Near the station"], answer: 0, explanation: "'on Main Street, next to the bank'。" },
                { q: "When does it close on Saturdays?", options: ["5 PM","3 PM","12 PM","Closed Saturdays"], answer: 2, explanation: "'only until noon' = 中午 12 點。" }
            ]},
            { type: "announcement", script: "Attention shoppers. The store will be closing in 30 minutes. Please bring your final purchases to the checkout counter. We will reopen tomorrow morning at 9 AM. Thank you for shopping with us today.", questions: [
                { q: "What is the announcement about?", options: ["A sale","Store closing","New product","Renovation"], answer: 1, explanation: "通知商店即將關門。" },
                { q: "What time will it open tomorrow?", options: ["8 AM","9 AM","10 AM","7 AM"], answer: 1, explanation: "'reopen tomorrow morning at 9 AM'。" }
            ]}
        ],
        550: [
            { type: "short-dialogue", script: "Man: I'd like to book a conference room for Tuesday afternoon. Woman: I'm sorry, all rooms are booked on Tuesday. How about Wednesday morning? Man: That works. Can I have Room 3B? Woman: Let me check. Yes, Room 3B is available from 9 to 12 on Wednesday.", questions: [
                { q: "Why can't he book Tuesday?", options: ["Being cleaned","All booked","Building closed","No advance call"], answer: 1, explanation: "'all rooms are booked on Tuesday'。" },
                { q: "What room will he use?", options: ["2A","3A","3B","4B"], answer: 2, explanation: "Room 3B 確認可用。" }
            ]},
            { type: "voicemail", script: "Hi, this is Karen from Apex Supplies. I'm calling about your order number 4578. Unfortunately, the printer paper you ordered is temporarily out of stock. We expect it by next Thursday. Would you like to wait, or prefer a substitute? Please call me back at 555-0182.", questions: [
                { q: "What is the problem?", options: ["Wrong item","Out of stock","Cancelled","Price changed"], answer: 1, explanation: "'temporarily out of stock'。" },
                { q: "When will it be available?", options: ["Tomorrow","Next Monday","Next Thursday","Two weeks"], answer: 2, explanation: "'available again by next Thursday'。" }
            ]}
        ],
        650: [
            { type: "meeting", script: "Woman: Before we end, let's discuss the marketing budget. We allocated 50,000 dollars, but given positive Q3 results, I think we should increase it. Man: I agree. Social media ads brought 200 new clients. How much increase? Woman: I propose 75,000. That allows video advertising too. Man: Sounds reasonable. I'll present to finance on Friday.", questions: [
                { q: "What is the proposed new budget?", options: ["$50,000","$65,000","$75,000","$200,000"], answer: 2, explanation: "提議 $75,000。" },
                { q: "New area to expand into?", options: ["Print","Video","Radio","Billboard"], answer: 1, explanation: "'expand into video advertising'。" }
            ]}
        ],
        750: [
            { type: "presentation", script: "Good morning. Our customer satisfaction dropped from 92% to 87%. The primary concern was delivery times — 45% rated it poor. Product quality actually improved by 3 points. We recommend partnering with a second logistics provider. We've contacted two potential partners and expect proposals by month end.", questions: [
                { q: "Biggest customer complaint?", options: ["Quality","Service","Delivery times","Pricing"], answer: 2, explanation: "'primary concern was delivery times'。" },
                { q: "Proposed solution?", options: ["Hire staff","Lower prices","Add logistics partner","Improve quality"], answer: 2, explanation: "'partner with a second logistics provider'。" }
            ]}
        ]
    },

    // ===== Part 分類練習題 =====
    partExercises: {
        1: { name: "照片描述", type: "listening", instructions: "聽一段描述，選出最符合照片的選項。", exercises: [
            { script: "A. The woman is typing on a keyboard. B. The woman is talking on the phone. C. The woman is writing on a whiteboard. D. The woman is reading a book.", scene: "一位女性正在辦公室打電話", questions: [{ q: "What is the woman doing?", options: ["Typing on keyboard","Talking on phone","Writing on whiteboard","Reading a book"], answer: 1, explanation: "描述中 B 最符合場景。" }]},
            { script: "A. The man is standing in front of a building. B. The man is sitting at a desk. C. The man is walking through a park. D. The man is driving a car.", scene: "一位男性坐在辦公桌前工作", questions: [{ q: "What best describes the scene?", options: ["Standing in front of building","Sitting at desk","Walking through park","Driving a car"], answer: 1, explanation: "B 最符合辦公桌工作場景。" }]}
        ]},
        2: { name: "應答問題", type: "listening", instructions: "聽一個問題，選出最恰當的回答。", exercises: [
            { script: "When is the next board meeting?", questions: [{ q: "When is the next board meeting?", options: ["It's on Thursday at 2 PM.","Yes, I'll attend.","In the conference room."], answer: 0, explanation: "When 問時間，回答時間。" }]},
            { script: "Who is responsible for the marketing report?", questions: [{ q: "Who is responsible for the marketing report?", options: ["By next Friday.","Ms. Johnson from the sales team.","It was very comprehensive."], answer: 1, explanation: "Who 問人，回答人名。" }]},
            { script: "Would you like coffee or tea?", questions: [{ q: "Would you like coffee or tea?", options: ["Yes, please.","Coffee would be great.","No, it's not mine."], answer: 1, explanation: "選擇問句需選一個，不能用 Yes/No。" }]}
        ]},
        3: { name: "簡短對話", type: "listening", instructions: "聽一段對話，回答相關問題。", exercises: [
            { script: "Man: Have you seen the new office layout? They moved the IT department to the third floor. Woman: Yes, I heard. It's going to make collaboration with marketing much easier since they're on the same floor now. Man: That's true. But I'm going to miss having them next door.", questions: [
                { q: "Where is IT department now?", options: ["First floor","Second floor","Third floor","Same floor"], answer: 2, explanation: "'moved IT to the third floor'。" },
                { q: "Why is the move good for marketing?", options: ["More space","Same floor as IT","Near cafeteria","Bigger desks"], answer: 1, explanation: "'on the same floor now'。" }
            ]}
        ]},
        4: { name: "簡短獨白", type: "listening", instructions: "聽一段獨白（如語音訊息、公告、演講），回答問題。", exercises: [
            { script: "Good afternoon, everyone. I'd like to welcome you to the annual sales conference. This year, we have three keynote speakers and over 20 breakout sessions. Please note that the networking dinner has been moved from Thursday to Friday evening due to a venue change. Check your updated schedule at the registration desk.", questions: [
                { q: "What event has been rescheduled?", options: ["Keynote speech","Breakout session","Networking dinner","Registration"], answer: 2, explanation: "'networking dinner moved from Thursday to Friday'。" },
                { q: "Where can attendees get updated schedules?", options: ["Online","Email","Registration desk","Conference room"], answer: 2, explanation: "'at the registration desk'。" }
            ]}
        ]},
        5: { name: "句子填空", type: "reading", instructions: "選出最適合填入空格的答案。", exercises: [
            { questions: [
                { q: "The company ______ its quarterly earnings report next Monday.", options: ["releases","will release","released","has released"], answer: 1, explanation: "next Monday 是未來時間，用 will release。" },
                { q: "All employees are required to ______ the safety training by the end of the month.", options: ["complete","completely","completion","completing"], answer: 0, explanation: "to + 原形動詞，用 complete。" },
                { q: "The new software is ______ more efficient than the previous version.", options: ["significant","significantly","significance","signify"], answer: 1, explanation: "修飾形容詞 efficient 用副詞 significantly。" },
                { q: "______ the heavy rain, the outdoor event was postponed.", options: ["Because","Due to","Although","Despite of"], answer: 1, explanation: "Due to + 名詞，表示因為。" }
            ]}
        ]},
        6: { name: "段落填空", type: "reading", instructions: "閱讀短文，選出最適合填入各空格的答案。", exercises: [
            { passage: "Dear Mr. Thompson,\n\nThank you for your interest in the Marketing Manager position. We were impressed by your __(1)__ and would like to invite you for an interview. The interview will __(2)__ on March 25 at our downtown office. Please __(3)__ a copy of your portfolio.\n\nWe look forward to meeting you.", questions: [
                { q: "(1)", options: ["qualifications","qualify","qualified","qualifying"], answer: 0, explanation: "名詞位置用 qualifications。" },
                { q: "(2)", options: ["be held","hold","holding","held"], answer: 0, explanation: "面試是「被舉行」，被動語態。" },
                { q: "(3)", options: ["take","bring","carry","deliver"], answer: 1, explanation: "bring = 帶來，符合語境。" }
            ]}
        ]},
        7: { name: "閱讀理解", type: "reading", instructions: "閱讀文章，回答相關問題。", exercises: [
            { passage: "Greenfield Electronics Annual Report\n\nGreenfield Electronics reported revenue of $2.3 billion for fiscal year 2024, a 12% increase from the previous year. The growth was primarily driven by strong sales in the consumer electronics division, which saw a 25% increase. However, the industrial equipment division experienced a 5% decline due to reduced demand from the manufacturing sector.\n\nThe company plans to invest $150 million in research and development in 2025, focusing on sustainable technology solutions. CEO Amanda Richards stated, \"Innovation remains at the core of our strategy. We are committed to developing products that meet the evolving needs of our customers while minimizing environmental impact.\"", questions: [
                { q: "What was the total revenue?", options: ["$2 billion","$2.3 billion","$2.5 billion","$3 billion"], answer: 1, explanation: "'revenue of $2.3 billion'。" },
                { q: "Which division declined?", options: ["Consumer electronics","Software","Industrial equipment","Services"], answer: 2, explanation: "'industrial equipment division experienced a 5% decline'。" },
                { q: "How much will be invested in R&D?", options: ["$100 million","$125 million","$150 million","$200 million"], answer: 2, explanation: "'invest $150 million in R&D'。" }
            ]}
        ]}
    },

    // ===== 商業情境主題 =====
    topics: [
        { id: "office", name: "辦公室/會議", emoji: "🏢", vocab: ["agenda","minutes","deadline","postpone","delegate"], sentences: ["The meeting has been postponed to next week.","Please review the agenda before the meeting.","She delegated the task to her assistant."] },
        { id: "travel", name: "旅遊/飯店", emoji: "✈️", vocab: ["reservation","itinerary","boarding pass","check-in","accommodation"], sentences: ["I'd like to make a reservation for two nights.","Your boarding pass is ready at the counter.","The accommodation includes breakfast."] },
        { id: "shopping", name: "購物/餐廳", emoji: "🛍️", vocab: ["receipt","refund","warranty","discount","complimentary"], sentences: ["Do you have the receipt for the return?","The warranty covers repairs for one year.","Dessert is complimentary for members."] },
        { id: "hr", name: "人資/招聘", emoji: "👔", vocab: ["resume","interview","candidate","probation","orientation"], sentences: ["Please submit your resume by Friday.","The candidate has extensive experience.","The orientation session is on Monday."] },
        { id: "finance", name: "財務/預算", emoji: "💵", vocab: ["invoice","revenue","expenditure","audit","fiscal"], sentences: ["The invoice is due within 30 days.","Revenue exceeded expectations this quarter.","The annual audit begins next month."] },
        { id: "marketing", name: "行銷/廣告", emoji: "📣", vocab: ["campaign","target audience","brand awareness","launch","promotion"], sentences: ["The new campaign targets young professionals.","Brand awareness increased by 40%.","The product launch is scheduled for May."] }
    ],

    // ===== 速讀文章 =====
    speedReadingTexts: [
        "The quarterly sales report shows a significant improvement in revenue compared to the same period last year. The marketing team's efforts in digital advertising have contributed to a thirty percent increase in online orders. Customer satisfaction ratings also improved following the implementation of the new customer service training program. The management team has approved additional funding for the expansion of the e-commerce platform to further capitalize on this positive trend.",
        "Attention all employees. The company will be implementing a new flexible work policy starting next month. Under the new policy, employees may work from home up to three days per week with manager approval. All team meetings will be held on Tuesdays and Thursdays to ensure in-office collaboration. Please review the detailed policy document that will be sent to your email by the end of this week.",
        "The international trade conference will be held at the Grand Convention Center from October fifteenth to seventeenth. This year's theme focuses on sustainable business practices in global supply chains. Over two hundred speakers from thirty countries will participate in panel discussions and workshops. Early bird registration is available until September first with a twenty percent discount on standard admission fees.",
        "Dear valued customers, we are pleased to announce the opening of our newest branch location in the downtown business district. The new office will provide a full range of financial services including personal banking, business loans, and investment advisory. To celebrate the opening, we are offering special promotional interest rates on savings accounts opened before the end of the month. Visit us at 250 Commerce Street for more details."
    ],

    // ===== 成就定義 =====
    achievements: [
        { id: "first_day", name: "踏出第一步", desc: "完成第一天訓練", icon: "👣", condition: (s) => s.completedDays.length >= 1 },
        { id: "streak_3", name: "三天不懈", desc: "連續完成 3 天訓練", icon: "🔥", condition: (s) => calcStreak(s) >= 3 },
        { id: "streak_7", name: "一週達人", desc: "連續完成 7 天訓練", icon: "⭐", condition: (s) => calcStreak(s) >= 7 },
        { id: "streak_14", name: "半月堅持", desc: "連續完成 14 天訓練", icon: "🌟", condition: (s) => calcStreak(s) >= 14 },
        { id: "streak_30", name: "月度冠軍", desc: "連續完成 30 天訓練", icon: "👑", condition: (s) => calcStreak(s) >= 30 },
        { id: "half_done", name: "半程達標", desc: "完成一半的訓練天數", icon: "🎯", condition: (s) => s.completedDays.length >= s.totalDays / 2 },
        { id: "all_done", name: "訓練完成", desc: "完成所有訓練天數", icon: "🏆", condition: (s) => s.completedDays.length >= s.totalDays },
        { id: "accuracy_80", name: "精準射手", desc: "單日正確率達 80%", icon: "🎯", condition: (s) => (s.bestAccuracy || 0) >= 80 },
        { id: "accuracy_100", name: "完美表現", desc: "單日正確率達 100%", icon: "💯", condition: (s) => (s.bestAccuracy || 0) >= 100 },
        { id: "wrong_10", name: "錯題獵人", desc: "複習 10 題錯題", icon: "📕", condition: (s) => (s.wrongReviewed || 0) >= 10 },
        { id: "speed_200", name: "速讀新手", desc: "閱讀速度達 200 WPM", icon: "⚡", condition: (s) => (s.bestWPM || 0) >= 200 },
        { id: "speed_250", name: "速讀高手", desc: "閱讀速度達 250 WPM", icon: "🚀", condition: (s) => (s.bestWPM || 0) >= 250 },
    ]
};

function calcStreak(state) {
    if (!state.completedDays || state.completedDays.length === 0) return 0;
    const sorted = [...state.completedDays].sort((a, b) => b - a);
    let streak = 1;
    for (let i = 0; i < sorted.length - 1; i++) {
        if (sorted[i] - sorted[i + 1] === 1) streak++;
        else break;
    }
    return streak;
}
