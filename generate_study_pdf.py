#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOEIC 13-Week Study PDF Generator
Target: 450 -> 550+  (Listening 275, Reading 175 -> boost reading)
Uses fpdf2 with Chinese font support.
"""

import os
from fpdf import FPDF

OUTPUT_DIR = "/Users/tom/toeic-trainer/weekly-pdf"
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

# ---------------------------------------------------------------------------
# PDF Builder
# ---------------------------------------------------------------------------

class ToeicPDF(FPDF):
    def __init__(self, week_num, week_title):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.week_num = week_num
        self.week_title = week_title
        self.add_font("chi", "", FONT_PATH)
        self.add_font("chi", "B", FONT_PATH)
        self.set_auto_page_break(auto=True, margin=20)

    # helpers
    def _sep(self):
        self.set_draw_color(160, 160, 160)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)

    def cover_page(self):
        self.add_page()
        self.ln(60)
        self.set_font("chi", "B", 24)
        self.cell(0, 14, f"TOEIC Weekly Study Guide", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(6)
        self.set_font("chi", "B", 20)
        self.cell(0, 12, f"Week {self.week_num}: {self.week_title}", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(10)
        self.set_font("chi", "", 12)
        self.cell(0, 10, "目標分數：550+  |  目前程度：450 (L275 / R175)", new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(0, 10, "每日建議學習時間：60-90 分鐘", new_x="LMARGIN", new_y="NEXT", align="C")

    def section_title(self, title):
        if self.get_y() > 250:
            self.add_page()
        self.ln(4)
        self.set_font("chi", "B", 14)
        self.set_fill_color(230, 240, 250)
        self.cell(0, 10, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def sub_title(self, title):
        if self.get_y() > 260:
            self.add_page()
        self.ln(2)
        self.set_font("chi", "B", 11)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font("chi", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def small(self, text):
        self.set_font("chi", "", 8)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def vocab_table(self, words):
        """words: list of (english, pos, chinese, example_en, example_zh)"""
        self.set_font("chi", "B", 9)
        self.set_fill_color(70, 130, 180)
        self.set_text_color(255, 255, 255)
        self.cell(35, 7, " Word", border=1, fill=True)
        self.cell(14, 7, "POS", border=1, fill=True, align="C")
        self.cell(30, 7, " 中文", border=1, fill=True)
        self.cell(101, 7, " Example Sentence", border=1, fill=True)
        self.ln()
        self.set_text_color(0, 0, 0)
        self.set_font("chi", "", 8)
        fill = False
        for w in words:
            eng, pos, zh, ex_en, ex_zh = w
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            h = 6
            x0 = self.get_x()
            y0 = self.get_y()
            self.cell(35, h, f" {eng}", border=1, fill=True)
            self.cell(14, h, pos, border=1, fill=True, align="C")
            self.cell(30, h, f" {zh}", border=1, fill=True)
            self.cell(101, h, f" {ex_en}", border=1, fill=True)
            self.ln()
            self.set_font("chi", "", 7)
            self.set_text_color(100, 100, 100)
            self.cell(79, 5, "")
            self.cell(101, 5, f" {ex_zh}")
            self.ln()
            self.set_text_color(0, 0, 0)
            self.set_font("chi", "", 8)
            fill = not fill

    def grammar_block(self, text):
        self.set_font("chi", "", 10)
        lm = self.l_margin
        for line in text.split("\n"):
            if self.get_y() > 272:
                self.add_page()
            self.set_x(lm)
            stripped = line.strip()
            if stripped == "":
                self.ln(2)
            elif stripped.startswith("##"):
                self.set_font("chi", "B", 11)
                self.multi_cell(w=0, h=7, text=stripped.replace("##", "").strip())
                self.set_font("chi", "", 10)
            elif stripped.startswith("EX:"):
                self.set_font("chi", "", 9)
                self.set_text_color(0, 80, 0)
                self.multi_cell(w=0, h=6, text=stripped)
                self.set_text_color(0, 0, 0)
                self.set_font("chi", "", 10)
            else:
                self.multi_cell(w=0, h=6, text=stripped)

    def part5_questions(self, questions):
        """questions: list of (stem, A, B, C, D)"""
        for i, q in enumerate(questions, 1):
            if self.get_y() > 230:
                self.add_page()
            stem, a, b, c, d = q
            self.set_font("chi", "B", 10)
            self.multi_cell(0, 6, f"{i}. {stem}")
            self.set_font("chi", "", 9.5)
            lm = self.l_margin
            y = self.get_y()
            self.set_xy(lm + 8, y)
            self.multi_cell(80, 6, f"(A) {a}")
            y_after_a = self.get_y()
            self.set_xy(lm + 90, y)
            self.multi_cell(80, 6, f"(B) {b}")
            y_after_b = self.get_y()
            y2 = max(y_after_a, y_after_b)
            self.set_xy(lm + 8, y2)
            self.multi_cell(80, 6, f"(C) {c}")
            y_after_c = self.get_y()
            self.set_xy(lm + 90, y2)
            self.multi_cell(80, 6, f"(D) {d}")
            y_after_d = self.get_y()
            self.set_y(max(y_after_c, y_after_d))
            self.ln(3)

    def reading_passage(self, title, passage, questions):
        """questions: list of (stem, A, B, C, D)"""
        self.sub_title(title)
        self.set_font("chi", "", 10)
        self.set_fill_color(250, 250, 245)
        x = self.get_x()
        self.multi_cell(170, 6, passage, border=1, fill=True)
        self.ln(3)
        self.sub_title("Questions:")
        self.part5_questions(questions)

    def answer_key(self, part5_answers, reading_answers):
        """answers: list of (answer_letter, explanation)"""
        self.add_page()
        self.section_title("Answer Key 解答與詳解")
        if part5_answers:
            self.sub_title("Part 5 Practice Answers:")
            self.set_font("chi", "", 9)
            for i, (ans, expl) in enumerate(part5_answers, 1):
                if self.get_y() > 268:
                    self.add_page()
                self.set_font("chi", "B", 9)
                self.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
                self.set_font("chi", "", 9)
                self.multi_cell(0, 5, f"   {expl}")
                self.ln(1)
        if reading_answers:
            self.ln(3)
            self.sub_title("Reading Comprehension Answers:")
            self.set_font("chi", "", 9)
            for i, (ans, expl) in enumerate(reading_answers, 1):
                if self.get_y() > 268:
                    self.add_page()
                self.set_font("chi", "B", 9)
                self.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
                self.set_font("chi", "", 9)
                self.multi_cell(0, 5, f"   {expl}")
                self.ln(1)


def build_week(num, title, vocab_days, grammar, part5, reading_title, reading_passage, reading_qs, p5_answers, rd_answers):
    pdf = ToeicPDF(num, title)
    pdf.cover_page()

    # Vocabulary
    pdf.add_page()
    pdf.section_title("Vocabulary 核心單字")
    day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for d in range(5):
        pdf.sub_title(f"Day {d+1} ({day_labels[d]})")
        pdf.vocab_table(vocab_days[d])
        pdf.ln(2)

    # Grammar
    pdf.add_page()
    pdf.section_title("Grammar 文法重點")
    pdf.grammar_block(grammar)

    # Part 5
    pdf.add_page()
    pdf.section_title("Part 5 Practice 實戰練習")
    pdf.body("Choose the best answer to complete each sentence.")
    pdf.part5_questions(part5)

    # Reading
    pdf.add_page()
    pdf.section_title("Reading Comprehension 閱讀理解")
    pdf.reading_passage(reading_title, reading_passage, reading_qs)

    # Answers
    pdf.answer_key(p5_answers, rd_answers)

    path = os.path.join(OUTPUT_DIR, f"week{num:02d}.pdf")
    pdf.output(path)
    print(f"  [OK] {path}")


# =====================================================================
#  WEEK DATA
# =====================================================================

def week01():
    title = "Office Vocabulary + Parts of Speech"
    vocab_days = [
        [
            ("agenda", "n.", "議程", "Please review the agenda before the meeting.", "請在會議前檢閱議程。"),
            ("colleague", "n.", "同事", "My colleague will handle the project.", "我的同事將處理這個專案。"),
            ("deadline", "n.", "截止日期", "The deadline for the report is Friday.", "報告的截止日期是星期五。"),
            ("memorandum", "n.", "備忘錄", "A memorandum was sent to all staff.", "一份備忘錄已發送給全體員工。"),
            ("supervisor", "n.", "主管", "Please ask your supervisor for approval.", "請向你的主管申請核准。"),
            ("procedure", "n.", "程序", "Follow the standard procedure.", "遵循標準程序。"),
            ("appointment", "n.", "預約；任命", "I have an appointment at 3 p.m.", "我下午三點有預約。"),
            ("efficient", "adj.", "有效率的", "She is an efficient worker.", "她是一位有效率的員工。"),
            ("requirement", "n.", "要求；需求", "This job has strict requirements.", "這份工作有嚴格的要求。"),
            ("organize", "v.", "組織；安排", "Can you organize the files?", "你能整理這些檔案嗎？"),
            ("document", "n.", "文件", "Sign the document before noon.", "請在中午前簽署文件。"),
            ("submit", "v.", "提交", "Submit your report by Monday.", "請在星期一前提交報告。"),
            ("approve", "v.", "批准", "The manager approved the budget.", "經理批准了預算。"),
            ("revise", "v.", "修改", "Please revise the proposal.", "請修改提案。"),
            ("department", "n.", "部門", "She works in the marketing department.", "她在行銷部門工作。"),
        ],
        [
            ("supply", "n./v.", "供應；供給", "Office supplies are in the cabinet.", "辦公用品在櫃子裡。"),
            ("equipment", "n.", "設備", "New equipment was installed today.", "新設備今天安裝了。"),
            ("available", "adj.", "可用的", "Is the meeting room available?", "會議室可以使用嗎？"),
            ("assign", "v.", "分配", "She was assigned to the new project.", "她被分配到新專案。"),
            ("accomplish", "v.", "完成", "We accomplished our goals.", "我們達成了目標。"),
            ("budget", "n.", "預算", "We need to stay within budget.", "我們需要控制在預算內。"),
            ("conference", "n.", "會議", "The annual conference is in May.", "年度會議在五月。"),
            ("negotiate", "v.", "談判", "They negotiated a new contract.", "他們協商了一份新合約。"),
            ("postpone", "v.", "延期", "The meeting was postponed.", "會議被延期了。"),
            ("responsibility", "n.", "責任", "It is your responsibility to check.", "檢查是你的責任。"),
            ("candidate", "n.", "候選人", "We interviewed three candidates.", "我們面試了三位候選人。"),
            ("implement", "v.", "實施", "We will implement the new policy.", "我們將實施新政策。"),
            ("inventory", "n.", "庫存", "Check the inventory list.", "檢查庫存清單。"),
            ("maintain", "v.", "維持", "Maintain a clean workspace.", "維持整潔的工作空間。"),
            ("notify", "v.", "通知", "Please notify all employees.", "請通知所有員工。"),
        ],
        [
            ("quarterly", "adj.", "每季的", "The quarterly report is due.", "季報即將到期。"),
            ("productive", "adj.", "有生產力的", "It was a productive meeting.", "這是一場有成效的會議。"),
            ("coordinate", "v.", "協調", "She coordinates the schedule.", "她協調時程安排。"),
            ("executive", "n.", "主管；執行者", "The executive approved the plan.", "主管批准了計畫。"),
            ("reference", "n.", "參考；推薦信", "Use this as a reference.", "用這個作為參考。"),
            ("survey", "n.", "調查", "Employees completed the survey.", "員工完成了調查。"),
            ("division", "n.", "部門；分公司", "He transferred to another division.", "他調到另一個部門。"),
            ("resign", "v.", "辭職", "She decided to resign.", "她決定辭職。"),
            ("promote", "v.", "升遷；促銷", "He was promoted to manager.", "他被升遷為經理。"),
            ("evaluate", "v.", "評估", "We need to evaluate the results.", "我們需要評估結果。"),
            ("annual", "adj.", "每年的", "The annual review is next week.", "年度考核在下週。"),
            ("compliment", "n./v.", "讚美", "She received many compliments.", "她收到很多讚美。"),
            ("correspondence", "n.", "信件往來", "Handle the correspondence promptly.", "迅速處理信件往來。"),
            ("extension", "n.", "延長；分機", "May I have an extension?", "我可以延期嗎？"),
            ("recruit", "v.", "招募", "We need to recruit new staff.", "我們需要招募新員工。"),
        ],
        [
            ("commute", "v./n.", "通勤", "He commutes by train daily.", "他每天搭火車通勤。"),
            ("workspace", "n.", "工作空間", "She organized her workspace.", "她整理了工作空間。"),
            ("attendance", "n.", "出席", "Attendance is mandatory.", "出席是必須的。"),
            ("invoice", "n.", "發票；帳單", "Please send the invoice.", "請寄送發票。"),
            ("reimburse", "v.", "報銷", "The company will reimburse you.", "公司會報銷你的費用。"),
            ("collaborate", "v.", "合作", "Teams must collaborate closely.", "團隊必須密切合作。"),
            ("preliminary", "adj.", "初步的", "Here are the preliminary results.", "這是初步結果。"),
            ("expertise", "n.", "專業知識", "She has expertise in finance.", "她在財務方面有專業知識。"),
            ("initiative", "n.", "主動性；計畫", "He took the initiative.", "他採取了主動。"),
            ("mandatory", "adj.", "強制的", "Training is mandatory for all.", "訓練對所有人是強制的。"),
            ("feedback", "n.", "回饋", "We value your feedback.", "我們重視您的回饋。"),
            ("orientation", "n.", "新人訓練；方向", "New employee orientation is Monday.", "新員工訓練在星期一。"),
            ("regulation", "n.", "規定", "Follow all safety regulations.", "遵守所有安全規定。"),
            ("transaction", "n.", "交易", "The transaction was completed.", "交易已完成。"),
            ("verify", "v.", "確認；核實", "Please verify the information.", "請確認資訊。"),
        ],
        [
            ("confidential", "adj.", "機密的", "This document is confidential.", "這份文件是機密的。"),
            ("headquarters", "n.", "總部", "The headquarters is in Taipei.", "總部在台北。"),
            ("merger", "n.", "合併", "The merger was announced today.", "合併今天宣布了。"),
            ("subsidiary", "n.", "子公司", "They opened a new subsidiary.", "他們開設了新的子公司。"),
            ("turnover", "n.", "人員流動率；營業額", "Staff turnover is high.", "員工流動率很高。"),
            ("compensation", "n.", "薪酬；補償", "The compensation package is fair.", "薪酬方案是公平的。"),
            ("outstanding", "adj.", "傑出的；未完成的", "She did an outstanding job.", "她做得非常出色。"),
            ("proficiency", "n.", "熟練度", "Language proficiency is required.", "需要語言熟練度。"),
            ("benchmark", "n.", "基準", "Set a benchmark for performance.", "設定績效基準。"),
            ("logistics", "n.", "物流；後勤", "The logistics team handled shipping.", "物流團隊處理出貨。"),
            ("specification", "n.", "規格", "Check the product specifications.", "檢查產品規格。"),
            ("comply", "v.", "遵守", "You must comply with the rules.", "你必須遵守規定。"),
            ("delegate", "v.", "委派", "Learn to delegate tasks.", "學會委派任務。"),
            ("fluctuate", "v.", "波動", "Prices fluctuate daily.", "價格每天波動。"),
            ("streamline", "v.", "簡化流程", "We need to streamline the process.", "我們需要簡化流程。"),
        ],
    ]

    grammar = """## 詞性辨識 (Parts of Speech) — TOEIC Part 5 最重要的題型

在 TOEIC Part 5 中，約有 30-40% 的題目考的是「詞性」。你需要根據空格的位置判斷該填入名詞、動詞、形容詞還是副詞。

## 常見名詞字尾 (Noun Suffixes)
-tion / -sion：information, decision, production
-ment：management, equipment, requirement
-ness：effectiveness, awareness, willingness
-ity / -ty：productivity, responsibility, security
-ance / -ence：attendance, experience, preference
-er / -or：supervisor, manager, director
-ee：employee, trainee, interviewee

EX: The _______ of the new policy was announced yesterday.  → implementation (名詞)
EX: 新政策的實施昨天被宣佈了。

## 常見動詞字尾 (Verb Suffixes)
-ize：organize, authorize, maximize
-ify：simplify, notify, verify
-ate：evaluate, negotiate, collaborate
-en：strengthen, widen, shorten

EX: We need to _______ the production process.  → simplify (動詞)
EX: 我們需要簡化生產流程。

## 常見形容詞字尾 (Adjective Suffixes)
-ful：helpful, successful, meaningful
-less：careless, wireless, countless
-able / -ible：available, accessible, responsible
-ive：productive, effective, competitive
-ous：various, previous, numerous
-al：annual, additional, professional
-ent / -ant：efficient, significant, relevant

EX: The manager made an _______ decision.  → effective (形容詞)
EX: 經理做了一個有效的決定。

## 常見副詞字尾 (Adverb Suffixes)
-ly：efficiently, significantly, approximately

EX: The project was completed _______.  → successfully (副詞)
EX: 專案被成功地完成了。

## 判斷技巧
1. 空格前有 a/an/the/this/that → 後面需要名詞
2. 空格前有 be 動詞 (is/are/was/were) → 後面可能是形容詞或過去分詞
3. 空格修飾動詞 → 需要副詞
4. 空格在名詞前 → 需要形容詞
5. 空格前有 very/quite/extremely → 後面是形容詞或副詞

EX: The report was _______ written. → professionally (副詞修飾過去分詞)
EX: 報告被專業地撰寫了。"""

    part5 = [
        ("The company needs to hire an experienced _______ for the position.", "apply", "applicant", "application", "applicable"),
        ("Ms. Chen will _______ the annual conference.", "organization", "organize", "organized", "organizational"),
        ("The new software is extremely _______ for data analysis.", "use", "usefully", "useful", "usage"),
        ("All employees must _______ the safety training.", "completion", "completely", "complete", "completeness"),
        ("The _______ of the building was delayed by rain.", "construct", "constructive", "constructively", "construction"),
        ("Mr. Wang _______ submitted the report before the deadline.", "success", "successful", "successfully", "succeed"),
        ("The marketing team presented a very _______ proposal.", "create", "creation", "creatively", "creative"),
        ("Employee _______ has improved since the new policy.", "satisfy", "satisfactory", "satisfaction", "satisfactorily"),
        ("The manager asked for _______ information about the project.", "addition", "additional", "additionally", "add"),
        ("The company plans to _______ its operations in Asia.", "expansion", "expansive", "expand", "expansively"),
        ("The annual report provides a _______ overview of company finances.", "comprehend", "comprehensive", "comprehension", "comprehensively"),
        ("Please _______ all documents before the audit.", "verification", "verifiable", "verify", "verified"),
        ("_______ to the workshop is limited to 30 people.", "Attend", "Attentive", "Attendance", "Attentively"),
        ("The new printer is more _______ than the old one.", "efficiency", "efficient", "efficiently", "efficiencies"),
        ("The team worked _______ to meet the deadline.", "diligence", "diligent", "diligently", "diligencies"),
        ("Her _______ in marketing helped the company grow.", "expert", "expertly", "expertise", "expertize"),
        ("The factory must _______ with environmental regulations.", "compliance", "compliant", "compliantly", "comply"),
        ("A _______ increase in sales was reported last quarter.", "significance", "significant", "significantly", "signify"),
        ("The company offers _______ benefits to all employees.", "compete", "competitive", "competition", "competitively"),
        ("The decision was made _______ by the board of directors.", "unanimous", "unanimity", "unanimously", "unanimousness"),
    ]

    reading_title = "Email: Office Renovation Notice"
    reading_pass = """From: facilities@globaltech.com
To: all-staff@globaltech.com
Subject: Office Renovation Schedule

Dear All Staff,

We are writing to inform you that the third-floor office area will undergo renovation starting Monday, March 10. The renovation is expected to be completed by Friday, March 28.

During this period, employees who normally work on the third floor will be temporarily relocated to the fifth floor. Please note the following:

1. All personal belongings should be removed from your desks by Friday, March 7.
2. Temporary workstations will be assigned on a first-come, first-served basis.
3. The main conference room (Room 305) will be unavailable during the renovation.
4. Alternative meeting rooms can be booked through the online reservation system.

We apologize for any inconvenience. The renovation will result in a more modern and efficient workspace for everyone. If you have any questions, please contact the Facilities Department at extension 2240.

Best regards,
Tom Lin
Facilities Manager"""

    reading_qs = [
        ("What is the purpose of this email?", "To announce a company merger", "To inform staff about office renovation", "To introduce a new employee", "To request budget approval"),
        ("When will the renovation be completed?", "March 7", "March 10", "March 28", "March 30"),
        ("Where will third-floor employees work during the renovation?", "At home", "On the fifth floor", "On the second floor", "In the conference room"),
        ("What should employees do by March 7?", "Book a meeting room", "Submit a report", "Remove personal belongings from desks", "Contact the Facilities Department"),
        ("How can employees book alternative meeting rooms?", "By calling extension 2240", "Through the online reservation system", "By emailing Tom Lin", "By visiting the front desk"),
    ]

    p5_answers = [
        ("B", "空格前有 an experienced（冠詞+形容詞），後面需要名詞。applicant（申請者）是名詞。"),
        ("B", "空格前有 will（助動詞），後面需要原形動詞。organize 是動詞。"),
        ("C", "空格前有 is extremely（be 動詞+副詞），後面需要形容詞。useful 是形容詞。"),
        ("C", "空格前有 must（助動詞），後面需要原形動詞。complete 是動詞。"),
        ("D", "空格前有 The（冠詞），後面需要名詞。construction 是名詞。"),
        ("C", "空格修飾動詞 submitted，需要副詞。successfully 是副詞。"),
        ("D", "空格前有 very（程度副詞），後面需要形容詞。creative 是形容詞。"),
        ("C", "空格前有 Employee（名詞作形容詞用），整個作主詞需要名詞。satisfaction 是名詞。"),
        ("B", "空格後有名詞 information，前面需要形容詞。additional 是形容詞。"),
        ("C", "空格前有 to（不定詞），後面需要原形動詞。expand 是動詞。"),
        ("B", "空格後有名詞 overview，前面需要形容詞。comprehensive 是形容詞。"),
        ("C", "空格前有 Please（祈使句），後面需要原形動詞。verify 是動詞。"),
        ("C", "空格是主詞位置（後面有 is），需要名詞。Attendance 是名詞。"),
        ("B", "空格前有 more...than（比較級），需要形容詞。efficient 是形容詞。"),
        ("C", "空格修飾動詞 worked，需要副詞。diligently 是副詞。"),
        ("C", "空格前有 Her（所有格），後面需要名詞。expertise 是名詞。"),
        ("D", "空格前有 must（助動詞），後面需要原形動詞。comply 是動詞。"),
        ("B", "空格後有名詞 increase，前面需要形容詞。significant 是形容詞。"),
        ("B", "空格後有名詞 benefits，前面需要形容詞。competitive 是形容詞。"),
        ("C", "空格修飾動詞 was made，需要副詞。unanimously 是副詞。"),
    ]

    rd_answers = [
        ("B", "信件主旨為 Office Renovation Schedule，內容在通知員工辦公室翻修事宜。"),
        ("C", "信中提到 expected to be completed by Friday, March 28。"),
        ("B", "信中提到 temporarily relocated to the fifth floor。"),
        ("C", "信中提到 All personal belongings should be removed from your desks by Friday, March 7。"),
        ("B", "信中提到 Alternative meeting rooms can be booked through the online reservation system。"),
    ]

    build_week(1, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week02():
    title = "Travel/Hotel Vocabulary + Verb Tenses"
    vocab_days = [
        [
            ("reservation", "n.", "預訂", "I made a reservation for two nights.", "我預訂了兩晚。"),
            ("itinerary", "n.", "行程表", "Please check your itinerary.", "請檢查你的行程表。"),
            ("departure", "n.", "出發", "The departure time is 8 a.m.", "出發時間是早上八點。"),
            ("destination", "n.", "目的地", "Our destination is Tokyo.", "我們的目的地是東京。"),
            ("accommodation", "n.", "住宿", "The accommodation was excellent.", "住宿非常好。"),
            ("luggage", "n.", "行李", "Please collect your luggage.", "請領取你的行李。"),
            ("boarding", "n.", "登機", "Boarding begins at gate 12.", "在12號登機門開始登機。"),
            ("check-in", "n.", "報到；入住", "Check-in starts at 3 p.m.", "入住從下午三點開始。"),
            ("round-trip", "adj.", "來回的", "I bought a round-trip ticket.", "我買了一張來回票。"),
            ("complimentary", "adj.", "免費贈送的", "Breakfast is complimentary.", "早餐是免費附贈的。"),
            ("currency", "n.", "貨幣", "You can exchange currency here.", "你可以在這裡換匯。"),
            ("customs", "n.", "海關", "Go through customs first.", "先通過海關。"),
            ("domestic", "adj.", "國內的", "This is a domestic flight.", "這是國內航班。"),
            ("confirm", "v.", "確認", "Please confirm your booking.", "請確認你的預訂。"),
            ("transfer", "v./n.", "轉乘；轉帳", "Transfer at the next station.", "在下一站轉乘。"),
        ],
        [
            ("vacancy", "n.", "空房；職缺", "Are there any vacancies?", "還有空房嗎？"),
            ("receptionist", "n.", "接待員", "Ask the receptionist for help.", "向接待員尋求幫助。"),
            ("suite", "n.", "套房", "We booked a deluxe suite.", "我們預訂了豪華套房。"),
            ("amenity", "n.", "設施；便利設施", "The hotel has many amenities.", "飯店有很多設施。"),
            ("concierge", "n.", "禮賓人員", "The concierge recommended a restaurant.", "禮賓人員推薦了一家餐廳。"),
            ("housekeeping", "n.", "房務", "Call housekeeping for towels.", "打電話給房務要毛巾。"),
            ("brochure", "n.", "手冊", "Pick up a travel brochure.", "拿一本旅遊手冊。"),
            ("excursion", "n.", "短途旅行", "We joined a city excursion.", "我們參加了城市短途旅行。"),
            ("scenic", "adj.", "風景優美的", "Take the scenic route.", "走風景優美的路線。"),
            ("souvenir", "n.", "紀念品", "She bought some souvenirs.", "她買了一些紀念品。"),
            ("reimburse", "v.", "報銷", "The company will reimburse travel costs.", "公司會報銷旅費。"),
            ("valid", "adj.", "有效的", "Is your passport valid?", "你的護照還有效嗎？"),
            ("expire", "v.", "過期", "My visa will expire soon.", "我的簽證即將過期。"),
            ("delay", "n./v.", "延誤", "The flight was delayed.", "航班延誤了。"),
            ("cancel", "v.", "取消", "We had to cancel the trip.", "我們不得不取消旅行。"),
        ],
        [
            ("overseas", "adj./adv.", "海外的", "She works overseas.", "她在海外工作。"),
            ("refund", "n./v.", "退款", "Can I get a refund?", "我可以退款嗎？"),
            ("passport", "n.", "護照", "Bring your passport to the airport.", "帶護照去機場。"),
            ("terminal", "n.", "航站樓", "Go to Terminal 2.", "前往第二航站樓。"),
            ("aisle", "n.", "走道", "I prefer an aisle seat.", "我偏好走道座位。"),
            ("baggage", "n.", "行李", "Baggage claim is on level 1.", "行李提領在一樓。"),
            ("turbulence", "n.", "亂流", "We experienced some turbulence.", "我們遇到了亂流。"),
            ("layover", "n.", "中途停留", "We have a 3-hour layover.", "我們有三小時的中途停留。"),
            ("voucher", "n.", "兌換券", "Use this voucher for a free meal.", "用這張兌換券免費用餐。"),
            ("upgrade", "v./n.", "升級", "I was upgraded to first class.", "我被升級到頭等艙。"),
            ("inn", "n.", "旅館；小飯店", "We stayed at a cozy inn.", "我們住在一間舒適的旅館。"),
            ("lodge", "n./v.", "小旅館；投宿", "The mountain lodge was beautiful.", "山上的小旅館很漂亮。"),
            ("sightseeing", "n.", "觀光", "We went sightseeing downtown.", "我們去市區觀光。"),
            ("pedestrian", "n.", "行人", "Watch out for pedestrians.", "注意行人。"),
            ("prohibit", "v.", "禁止", "Smoking is prohibited here.", "這裡禁止吸菸。"),
        ],
        [
            ("fare", "n.", "票價；車資", "The bus fare is $2.50.", "公車票價是 2.5 美元。"),
            ("courtesy", "n.", "禮貌；禮遇", "A courtesy shuttle is available.", "有免費接駁車可搭乘。"),
            ("adjacent", "adj.", "鄰近的", "The restaurant is adjacent to the hotel.", "餐廳在飯店旁邊。"),
            ("convenient", "adj.", "方便的", "The hotel is in a convenient location.", "飯店位置很方便。"),
            ("duration", "n.", "期間", "The duration of the flight is 4 hours.", "飛行時間為四小時。"),
            ("occupancy", "n.", "住用率；入住人數", "Maximum occupancy is 4 persons.", "最大入住人數為四人。"),
            ("banquet", "n.", "宴會", "The banquet hall seats 200 guests.", "宴會廳可容納200位賓客。"),
            ("hospitality", "n.", "款待；餐旅業", "She works in the hospitality industry.", "她在餐旅業工作。"),
            ("complaint", "n.", "投訴", "File a complaint at the front desk.", "在前台提出投訴。"),
            ("directory", "n.", "名錄；目錄", "Check the hotel directory for services.", "查看飯店目錄了解服務。"),
            ("shuttle", "n.", "接駁車", "The airport shuttle runs every hour.", "機場接駁車每小時一班。"),
            ("porter", "n.", "行李員", "The porter carried our bags.", "行李員幫我們提行李。"),
            ("continental", "adj.", "歐式的", "Continental breakfast is included.", "歐式早餐包含在內。"),
            ("surcharge", "n.", "附加費", "There is a surcharge for late checkout.", "延遲退房有附加費。"),
            ("vacancy", "n.", "空缺", "No vacancy during peak season.", "旺季沒有空房。"),
        ],
        [
            ("embark", "v.", "登船；開始", "Passengers will embark at noon.", "乘客將在中午登船。"),
            ("disembark", "v.", "下船；下飛機", "Please disembark from the front exit.", "請從前方出口下機。"),
            ("expedition", "n.", "遠征；探險", "They organized an expedition.", "他們組織了一次探險。"),
            ("cruise", "n.", "郵輪旅行", "We booked a Caribbean cruise.", "我們訂了加勒比海郵輪之旅。"),
            ("landlord", "n.", "房東", "Contact the landlord for details.", "聯繫房東了解詳情。"),
            ("tenant", "n.", "房客", "The tenant signed a lease.", "房客簽了租約。"),
            ("detour", "n.", "繞路", "There was a detour due to construction.", "因施工需要繞路。"),
            ("intersection", "n.", "十字路口", "Turn left at the intersection.", "在十字路口左轉。"),
            ("commuter", "n.", "通勤者", "Commuters prefer the express train.", "通勤者偏好快車。"),
            ("metropolitan", "adj.", "大都市的", "The metropolitan area is growing.", "大都會區正在成長。"),
            ("navigate", "v.", "導航", "Use GPS to navigate.", "用 GPS 導航。"),
            ("expedition", "n.", "探險", "Join the mountain expedition.", "加入登山探險。"),
            ("reclaim", "v.", "領回", "Reclaim your baggage at carousel 5.", "在5號轉盤領回行李。"),
            ("reimburse", "v.", "報銷", "Submit receipts to be reimbursed.", "提交收據以獲得報銷。"),
            ("relocate", "v.", "搬遷", "The office will relocate next month.", "辦公室下個月搬遷。"),
        ],
    ]

    grammar = """## 動詞時態 (Verb Tenses) — TOEIC 必考重點

TOEIC Part 5 經常考時態的選擇。關鍵是找到「時間線索詞」。

## 一、簡單現在式 (Simple Present)
用法：表示習慣、事實、規律性的動作
時間線索：every day, always, usually, often, sometimes, rarely

EX: The store opens at 9 a.m. every day.
EX: 這家店每天早上九點開門。

EX: She usually takes the bus to work.
EX: 她通常搭公車上班。

注意：第三人稱單數要加 -s / -es
he works, she goes, it runs

## 二、簡單過去式 (Simple Past)
用法：表示過去已完成的動作
時間線索：yesterday, last week/month/year, ago, in 2020

EX: The company hired 20 new employees last month.
EX: 公司上個月雇用了 20 名新員工。

EX: She submitted the report two days ago.
EX: 她兩天前提交了報告。

注意：不規則動詞需背誦 (go-went, take-took, make-made, see-saw)

## 三、簡單未來式 (Simple Future)
用法：表示未來的計畫或預測
時間線索：tomorrow, next week/month/year, soon, in the future

結構1：will + 原形動詞
結構2：be going to + 原形動詞

EX: The meeting will begin at 2 p.m. tomorrow.
EX: 會議明天下午兩點開始。

EX: We are going to launch a new product next month.
EX: 我們下個月將推出新產品。

## 四、TOEIC 常見陷阱

1. 時間副詞決定時態：
   Since 2020 → 用現在完成式
   Last year → 用簡單過去式
   Next Friday → 用簡單未來式
   Every Monday → 用簡單現在式

2. 條件句中 if/when 子句用現在式代替未來式：
EX: If the weather is nice, we will have the event outdoors.
EX: 如果天氣好，我們將在戶外舉辦活動。
（if 子句用 is，不用 will be）

3. 主詞動詞一致：
EX: The list of items was sent to the manager.
EX: 清單已寄給經理了。
（主詞是 list，不是 items，所以用 was）"""

    part5 = [
        ("Ms. Lee _______ to the office every morning at 8:30.", "arrives", "arrived", "will arrive", "arriving"),
        ("The flight _______ two hours ago due to bad weather.", "delays", "delayed", "was delayed", "will delay"),
        ("The new policy _______ into effect next Monday.", "goes", "went", "will go", "going"),
        ("Last year, the company _______ a record profit.", "achieves", "achieved", "will achieve", "has achieved"),
        ("The train to Kaohsiung _______ at 10:15 every morning.", "depart", "departs", "departed", "will depart"),
        ("The hotel _______ a complimentary breakfast yesterday.", "provides", "provided", "will provide", "has provided"),
        ("If you _______ early, you can get a window seat.", "arrive", "arrived", "will arrive", "arriving"),
        ("The tourism industry _______ significantly since 2020.", "changes", "changed", "has changed", "will change"),
        ("Mr. Park _______ to Seoul for a business meeting tomorrow.", "travels", "traveled", "will travel", "has traveled"),
        ("The receptionist always _______ guests with a smile.", "greet", "greets", "greeted", "greeting"),
        ("The renovation _______ by the end of this month.", "completes", "completed", "will be completed", "completing"),
        ("We _______ the contract before the deadline last Friday.", "sign", "signed", "will sign", "signing"),
        ("Passengers _______ their boarding passes before entering the gate.", "show", "showed", "must show", "showing"),
        ("The airline _______ free meals on international flights.", "offer", "offers", "offered", "will offering"),
        ("The company _______ three new branches next year.", "opens", "opened", "will open", "opening"),
        ("She _______ for the company for over ten years now.", "works", "worked", "has worked", "will work"),
        ("When the manager _______, please inform her about the change.", "arrives", "arrived", "will arrive", "arriving"),
        ("The shuttle bus _______ every 30 minutes from the airport.", "run", "runs", "ran", "running"),
        ("By tomorrow, we _______ all the arrangements.", "finish", "finished", "will have finished", "finishing"),
        ("The conference _______ place in the grand ballroom last Saturday.", "takes", "took", "will take", "has taken"),
    ]

    reading_title = "Notice: Hotel Renovation and Guest Information"
    reading_pass = """GRAND PACIFIC HOTEL
Guest Notice

Dear Valued Guests,

Thank you for choosing the Grand Pacific Hotel for your stay. We would like to inform you about our ongoing renovation project.

The swimming pool and fitness center on the 2nd floor will be closed for renovations from April 1 to April 30. During this time, guests may use the facilities at our partner hotel, the Ocean View Resort, located just 5 minutes away by our complimentary shuttle bus.

The shuttle service operates every 30 minutes from 7:00 a.m. to 10:00 p.m. daily. Simply show your room key card to the shuttle driver.

As compensation for any inconvenience, all guests staying during the renovation period will receive:
- A 15% discount on room rates
- A complimentary upgrade to the next room category (subject to availability)
- Free access to the hotel spa

We sincerely apologize for any inconvenience and appreciate your understanding. Please contact the front desk at extension 0 if you have any questions.

Warm regards,
Sarah Chen
General Manager
Grand Pacific Hotel"""

    reading_qs = [
        ("What facilities are being renovated?", "The lobby and restaurant", "The swimming pool and fitness center", "The spa and sauna", "The parking garage"),
        ("How long will the renovation last?", "Two weeks", "One month", "Two months", "One week"),
        ("How can guests use the partner hotel's facilities?", "By paying an extra fee", "By showing their room key card on the shuttle", "By making a reservation online", "By contacting the front desk"),
        ("Which of the following is NOT mentioned as compensation?", "Room rate discount", "Free breakfast", "Complimentary upgrade", "Free spa access"),
        ("How often does the shuttle bus run?", "Every 15 minutes", "Every 30 minutes", "Every hour", "Twice a day"),
    ]

    p5_answers = [
        ("A", "every morning 是現在式的時間線索，主詞 Ms. Lee 是第三人稱，用 arrives。"),
        ("C", "two hours ago 是過去式線索，且航班「被延誤」需用被動語態 was delayed。"),
        ("C", "next Monday 是未來式線索，用 will go。"),
        ("B", "Last year 是過去式線索，用 achieved。"),
        ("B", "every morning 是現在式線索，主詞 The train 是第三人稱，用 departs。"),
        ("B", "yesterday 是過去式線索，用 provided。"),
        ("A", "if 條件句中用現在式代替未來式，用 arrive。"),
        ("C", "since 2020 是現在完成式的線索，用 has changed。"),
        ("C", "tomorrow 是未來式線索，用 will travel。"),
        ("B", "always 是現在式線索，主詞第三人稱，用 greets。"),
        ("C", "by the end of this month 表未來完成，翻修「被完成」用 will be completed。"),
        ("B", "last Friday 是過去式線索，用 signed。"),
        ("C", "描述規定/義務用 must show。"),
        ("B", "描述航空公司的一般事實，主詞 The airline 第三人稱，用 offers。"),
        ("C", "next year 是未來式線索，用 will open。"),
        ("C", "for over ten years now 是現在完成式線索，用 has worked。"),
        ("A", "When 引導的時間子句用現在式代替未來式，用 arrives。"),
        ("B", "every 30 minutes 是現在式線索，主詞第三人稱，用 runs。"),
        ("C", "By tomorrow 表示「到明天為止」，用未來完成式 will have finished。"),
        ("B", "last Saturday 是過去式線索，用 took。"),
    ]

    rd_answers = [
        ("B", "文中提到 The swimming pool and fitness center on the 2nd floor will be closed for renovations。"),
        ("B", "翻修期間為 April 1 to April 30，共一個月。"),
        ("B", "文中提到 Simply show your room key card to the shuttle driver。"),
        ("B", "文中提到的補償有折扣、升等、免費水療，但沒有提到免費早餐。"),
        ("B", "文中提到 The shuttle service operates every 30 minutes。"),
    ]

    build_week(2, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week03():
    title = "Shopping/Dining Vocabulary + Perfect Tenses"
    vocab_days = [
        [
            ("purchase", "v./n.", "購買", "She purchased a new laptop.", "她購買了一台新筆電。"),
            ("receipt", "n.", "收據", "Keep the receipt for returns.", "保留收據以便退貨。"),
            ("discount", "n./v.", "折扣", "There is a 20% discount today.", "今天有八折優惠。"),
            ("merchandise", "n.", "商品", "All merchandise is on sale.", "所有商品都在特賣。"),
            ("warranty", "n.", "保固", "The warranty lasts two years.", "保固期為兩年。"),
            ("coupon", "n.", "折價券", "Use this coupon at checkout.", "結帳時使用這張折價券。"),
            ("retail", "n./adj.", "零售", "The retail price is $50.", "零售價是50美元。"),
            ("wholesale", "n./adj.", "批發", "We buy at wholesale prices.", "我們以批發價購買。"),
            ("inventory", "n.", "庫存", "The item is not in inventory.", "這件商品沒有庫存。"),
            ("transaction", "n.", "交易", "The transaction was successful.", "交易成功了。"),
            ("refund", "n./v.", "退款", "I would like to request a refund.", "我想申請退款。"),
            ("exchange", "v./n.", "兌換；交換", "Can I exchange this for a larger size?", "我可以換大一號的嗎？"),
            ("browse", "v.", "瀏覽", "Feel free to browse around.", "請隨意看看。"),
            ("bargain", "n./v.", "便宜貨；討價還價", "This jacket is a real bargain.", "這件夾克真的很划算。"),
            ("cashier", "n.", "收銀員", "Pay at the cashier.", "在收銀台付款。"),
        ],
        [
            ("appetizer", "n.", "開胃菜", "We ordered two appetizers.", "我們點了兩道開胃菜。"),
            ("entree", "n.", "主菜", "The entree comes with a salad.", "主菜附沙拉。"),
            ("beverage", "n.", "飲料", "Beverages are not included.", "飲料不包含在內。"),
            ("reservation", "n.", "預訂", "Do you have a reservation?", "您有預訂嗎？"),
            ("complimentary", "adj.", "免費附贈的", "Dessert is complimentary tonight.", "今晚甜點免費。"),
            ("cuisine", "n.", "料理；菜系", "This restaurant serves Italian cuisine.", "這家餐廳提供義大利料理。"),
            ("ingredient", "n.", "食材", "Fresh ingredients are used daily.", "每天使用新鮮食材。"),
            ("portion", "n.", "份量", "The portions are very generous.", "份量非常大。"),
            ("dietary", "adj.", "飲食的", "Please note any dietary restrictions.", "請註明任何飲食限制。"),
            ("banquet", "n.", "宴會", "The banquet is on Friday.", "宴會在星期五。"),
            ("catering", "n.", "外燴服務", "We hired a catering company.", "我們請了外燴公司。"),
            ("gratuity", "n.", "小費", "A 15% gratuity is included.", "含15%小費。"),
            ("utensil", "n.", "餐具", "Disposable utensils are provided.", "提供免洗餐具。"),
            ("gourmet", "adj./n.", "美食的；美食家", "This is a gourmet restaurant.", "這是一家高級餐廳。"),
            ("savory", "adj.", "鹹味的；美味的", "Try the savory dishes.", "試試鹹味的菜餚。"),
        ],
        [
            ("consumer", "n.", "消費者", "Consumers demand better quality.", "消費者要求更好的品質。"),
            ("vendor", "n.", "供應商；攤販", "The vendor delivered the goods.", "供應商送了貨。"),
            ("aisle", "n.", "走道", "The cereal is in aisle 5.", "穀片在第五走道。"),
            ("checkout", "n.", "結帳", "The checkout line is long.", "結帳排隊很長。"),
            ("complain", "v.", "抱怨", "She complained about the service.", "她抱怨服務。"),
            ("defective", "adj.", "有缺陷的", "The product was defective.", "產品有缺陷。"),
            ("guarantee", "n./v.", "保證", "We guarantee customer satisfaction.", "我們保證顧客滿意。"),
            ("manufacturer", "n.", "製造商", "Contact the manufacturer directly.", "直接聯繫製造商。"),
            ("promote", "v.", "促銷；升遷", "The store is promoting a new brand.", "商店在促銷新品牌。"),
            ("seasonal", "adj.", "季節性的", "Seasonal products are discounted.", "季節性商品有折扣。"),
            ("organic", "adj.", "有機的", "Organic food is more expensive.", "有機食品比較貴。"),
            ("nutritious", "adj.", "營養的", "Choose nutritious meals.", "選擇營養的餐點。"),
            ("appetizing", "adj.", "開胃的", "The food looks appetizing.", "食物看起來很開胃。"),
            ("recommendation", "n.", "推薦", "What is your recommendation?", "你有什麼推薦？"),
            ("specialty", "n.", "特色菜；專長", "The chef's specialty is pasta.", "主廚的特色菜是義大利麵。"),
        ],
        [
            ("affordable", "adj.", "負擔得起的", "The prices are very affordable.", "價格非常實惠。"),
            ("economical", "adj.", "經濟的；節省的", "This car is economical on fuel.", "這台車很省油。"),
            ("luxurious", "adj.", "奢華的", "The hotel offers luxurious rooms.", "飯店提供奢華的房間。"),
            ("boutique", "n.", "精品店", "She shops at a boutique.", "她在精品店購物。"),
            ("patron", "n.", "顧客；贊助者", "Patrons receive special discounts.", "老顧客可獲得特別折扣。"),
            ("reimburse", "v.", "報銷", "We will reimburse shipping costs.", "我們會報銷運費。"),
            ("subscription", "n.", "訂閱", "Cancel your subscription anytime.", "隨時取消訂閱。"),
            ("assortment", "n.", "各式各樣", "We have a wide assortment of teas.", "我們有各式各樣的茶。"),
            ("perishable", "adj.", "易腐壞的", "Store perishable items in the fridge.", "易腐壞的物品放冰箱。"),
            ("delicacy", "n.", "珍饈；佳餚", "Try the local delicacy.", "試試當地美食。"),
            ("sustainable", "adj.", "永續的", "We use sustainable packaging.", "我們使用永續包裝。"),
            ("authentic", "adj.", "道地的", "This is authentic Thai food.", "這是道地的泰國菜。"),
            ("appetizer", "n.", "開胃菜", "The soup is a popular appetizer.", "這道湯是受歡迎的開胃菜。"),
            ("dine", "v.", "用餐", "We dined at a fancy restaurant.", "我們在高級餐廳用餐。"),
            ("accommodate", "v.", "容納；配合", "The restaurant accommodates 100 guests.", "餐廳可容納100位客人。"),
        ],
        [
            ("premium", "adj./n.", "高級的；保費", "Premium members get free shipping.", "高級會員免運費。"),
            ("outlet", "n.", "暢貨中心；插座", "Visit the factory outlet for deals.", "去暢貨中心找便宜。"),
            ("stationery", "n.", "文具", "Buy stationery at the shop.", "在店裡買文具。"),
            ("renovate", "v.", "翻修", "The restaurant was recently renovated.", "餐廳最近翻修了。"),
            ("oversee", "v.", "監督", "She oversees the catering team.", "她監督外燴團隊。"),
            ("elaborate", "adj.", "精緻的；詳盡的", "The menu is very elaborate.", "菜單非常精緻。"),
            ("expedite", "v.", "加速", "Please expedite the delivery.", "請加速送貨。"),
            ("perishable", "adj.", "易腐壞的", "Label all perishable goods.", "標示所有易腐壞商品。"),
            ("surplus", "n./adj.", "剩餘", "Surplus stock is on sale.", "剩餘庫存特價中。"),
            ("liability", "n.", "責任；負債", "The company denied liability.", "公司否認責任。"),
            ("itemize", "v.", "逐條列出", "Please itemize the expenses.", "請逐條列出費用。"),
            ("procurement", "n.", "採購", "The procurement process takes time.", "採購流程需要時間。"),
            ("quotation", "n.", "報價", "We received three quotations.", "我們收到三份報價。"),
            ("markup", "n.", "加價", "The markup on this item is 30%.", "這件商品加價30%。"),
            ("depreciation", "n.", "折舊", "Calculate the depreciation rate.", "計算折舊率。"),
        ],
    ]

    grammar = """## 完成式 (Perfect Tenses) — TOEIC 高頻考點

完成式表達「到某個時間點為止已經完成」的動作。TOEIC 最常考現在完成式。

## 一、現在完成式 (Present Perfect)
結構：have/has + 過去分詞 (p.p.)
用法：從過去到現在持續的狀態或經驗

時間線索：since, for, already, yet, ever, never, recently, so far, up to now, just

EX: She has worked at this company since 2018.
EX: 她從2018年起就在這家公司工作。

EX: We have already completed the project.
EX: 我們已經完成了這個專案。

EX: Have you ever visited Japan?
EX: 你曾經去過日本嗎？

## 二、過去完成式 (Past Perfect)
結構：had + 過去分詞 (p.p.)
用法：表示「過去的過去」，在過去某個時間點之前已完成的動作

時間線索：by the time, before, after, when (搭配過去式主句)

EX: The meeting had already started when I arrived.
EX: 當我到達時，會議已經開始了。

EX: She had finished the report before the deadline.
EX: 她在截止日期前就完成了報告。

## 三、未來完成式 (Future Perfect)
結構：will have + 過去分詞 (p.p.)
用法：表示在未來某個時間點之前將會完成的動作

時間線索：by tomorrow, by next week, by the end of...

EX: We will have finished the renovation by December.
EX: 我們將在十二月前完成翻修。

EX: By next year, she will have been here for 10 years.
EX: 到明年，她就在這裡十年了。

## 四、for vs. since 的區別
for + 一段時間 (for three years, for two months)
since + 時間點 (since 2020, since last Monday)

EX: I have lived here for five years. (住了五年)
EX: I have lived here since 2021. (從2021年開始住)

## 五、TOEIC 常考陷阱
1. since 後面用過去式：Since the store opened in 2015, it has attracted many customers.
2. 不要混淆 already (已經，用在肯定句) 和 yet (還，用在否定句和疑問句)
3. just 表示「剛剛」，常與現在完成式搭配：The manager has just left."""

    part5 = [
        ("The company has _______ many changes since last year.", "undergo", "underwent", "undergone", "undergoing"),
        ("By the time the manager arrived, the staff had already _______ the meeting room.", "prepare", "prepared", "preparing", "preparation"),
        ("Ms. Kim has worked in sales _______ over ten years.", "since", "for", "during", "while"),
        ("The restaurant has been popular _______ it first opened.", "for", "during", "since", "while"),
        ("We have not _______ received the shipment yet.", "still", "already", "yet", "ever"),
        ("By next month, the store will have _______ in business for 20 years.", "be", "been", "being", "was"),
        ("The customer had _______ a complaint before receiving the refund.", "file", "filed", "filing", "files"),
        ("_______ you ever eaten at that restaurant?", "Did", "Do", "Have", "Were"),
        ("The chef has just _______ a new menu for the season.", "create", "creates", "created", "creating"),
        ("Sales have _______ by 15% since the new marketing campaign.", "increase", "increased", "increasing", "increases"),
        ("The shop had already _______ when we arrived at 9 p.m.", "close", "closes", "closed", "closing"),
        ("They have _______ offered discounts to loyal customers.", "recent", "recently", "recency", "recenter"),
        ("By Friday, we will have _______ all the inventory.", "count", "counted", "counting", "counts"),
        ("The prices have not changed _______ January.", "for", "since", "during", "from"),
        ("She has _______ the best salesperson three years in a row.", "be", "been", "being", "was"),
        ("Before the store closed, many customers had already _______ their purchases.", "make", "made", "making", "makes"),
        ("We have _______ to find a better supplier so far.", "fail", "failed", "failing", "fails"),
        ("The manager has already _______ the new menu.", "approve", "approved", "approving", "approves"),
        ("By the end of this year, we will have _______ over 1000 customers.", "serve", "served", "serving", "serves"),
        ("The company has _______ three new stores since 2023.", "open", "opened", "opening", "opens"),
    ]

    reading_title = "Advertisement: Grand Opening Sale"
    reading_pass = """FRESH MART SUPERMARKET - GRAND OPENING!

We are excited to announce the grand opening of Fresh Mart Supermarket at 258 Oak Street, Downtown Plaza. Join us on Saturday, June 15, for an unforgettable shopping experience!

GRAND OPENING SPECIALS (June 15-30):
- 30% off all fresh produce
- Buy one, get one free on selected beverages
- Free reusable shopping bags for the first 200 customers
- Live cooking demonstrations every Saturday from 11 a.m. to 2 p.m.

STORE FEATURES:
- Over 5,000 products including organic and locally sourced items
- In-store bakery with freshly baked bread daily
- Full-service deli counter
- Online ordering with same-day delivery available

STORE HOURS:
Monday to Saturday: 7:00 a.m. - 10:00 p.m.
Sunday: 8:00 a.m. - 8:00 p.m.

Sign up for our loyalty program and receive an additional 5% off your first purchase! Visit www.freshmart.com or ask any staff member for details.

Fresh Mart - Where Freshness Meets Value!"""

    reading_qs = [
        ("When is the grand opening of Fresh Mart?", "June 1", "June 15", "June 30", "July 1"),
        ("How long will the grand opening specials last?", "One day", "One week", "About two weeks", "One month"),
        ("What will the first 200 customers receive?", "A discount coupon", "Free produce", "Free reusable shopping bags", "A gift card"),
        ("What is NOT mentioned as a store feature?", "In-store bakery", "Online ordering", "Free parking", "Deli counter"),
        ("How can customers get an extra 5% discount?", "By shopping on opening day", "By buying organic products", "By signing up for the loyalty program", "By spending over $100"),
    ]

    p5_answers = [
        ("C", "has + 過去分詞，undergo 的過去分詞是 undergone。"),
        ("B", "had already + 過去分詞，prepare 的過去分詞是 prepared。"),
        ("B", "over ten years 是一段時間，用 for。"),
        ("C", "it first opened 是時間點，用 since。"),
        ("C", "have not received... yet 是標準用法，yet 用在否定句。注意 still 不用於此結構。"),
        ("B", "will have + 過去分詞，be 的過去分詞是 been。"),
        ("B", "had + 過去分詞，file 的過去分詞是 filed。"),
        ("C", "Have you ever + 過去分詞 是現在完成式的疑問句。"),
        ("C", "has just + 過去分詞，create 的過去分詞是 created。"),
        ("B", "have + 過去分詞，increase 的過去分詞是 increased。"),
        ("C", "had already + 過去分詞，close 的過去分詞是 closed。"),
        ("B", "修飾動詞 offered 需要副詞 recently。"),
        ("B", "will have + 過去分詞，count 的過去分詞是 counted。"),
        ("B", "January 是時間點，用 since。"),
        ("B", "has + 過去分詞，be 的過去分詞是 been。"),
        ("B", "had already + 過去分詞，make 的過去分詞是 made。"),
        ("B", "have + 過去分詞，fail 的過去分詞是 failed。"),
        ("B", "has already + 過去分詞，approve 的過去分詞是 approved。"),
        ("B", "will have + 過去分詞，serve 的過去分詞是 served。"),
        ("B", "has + 過去分詞，open 的過去分詞是 opened。"),
    ]

    rd_answers = [
        ("B", "文中提到 Join us on Saturday, June 15。"),
        ("C", "特賣期間為 June 15-30，約兩週。"),
        ("C", "文中提到 Free reusable shopping bags for the first 200 customers。"),
        ("C", "文中提到了 bakery、online ordering、deli counter，但沒有提到 free parking。"),
        ("C", "文中提到 Sign up for our loyalty program and receive an additional 5% off。"),
    ]

    build_week(3, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week04():
    title = "Communication Vocabulary + Passive Voice"
    vocab_days = [
        [
            ("announce", "v.", "宣布", "The CEO announced the new policy.", "執行長宣布了新政策。"),
            ("broadcast", "v./n.", "廣播", "The news was broadcast live.", "新聞被現場直播。"),
            ("clarify", "v.", "澄清", "Could you clarify this point?", "你能澄清這一點嗎？"),
            ("correspond", "v.", "通信；對應", "We correspond by email.", "我們透過電郵通信。"),
            ("distribute", "v.", "分發", "Flyers were distributed to residents.", "傳單已分發給居民。"),
            ("editorial", "n./adj.", "社論；編輯的", "She wrote an editorial.", "她寫了一篇社論。"),
            ("enclose", "v.", "附上；圍起", "I have enclosed the documents.", "我已附上文件。"),
            ("inquire", "v.", "詢問", "She inquired about the schedule.", "她詢問了時程。"),
            ("manuscript", "n.", "手稿", "Submit the manuscript by Friday.", "請在星期五前提交手稿。"),
            ("negotiate", "v.", "談判；協商", "They negotiated a better deal.", "他們協商了更好的條件。"),
            ("persuade", "v.", "說服", "He persuaded the client to sign.", "他說服客戶簽約。"),
            ("publish", "v.", "出版；發布", "The report was published online.", "報告在網上發布。"),
            ("subscriber", "n.", "訂閱者", "We have 10,000 subscribers.", "我們有一萬名訂閱者。"),
            ("transmit", "v.", "傳送", "Data is transmitted securely.", "資料被安全傳送。"),
            ("verify", "v.", "確認", "Please verify your email address.", "請確認你的電子郵件地址。"),
        ],
        [
            ("acknowledge", "v.", "承認；確認收到", "Please acknowledge receipt of this email.", "請確認收到此郵件。"),
            ("brief", "v./adj.", "簡報；簡短的", "She briefed the team on the plan.", "她向團隊簡報了計畫。"),
            ("circulation", "n.", "流通量；循環", "The magazine has a large circulation.", "這本雜誌發行量大。"),
            ("convey", "v.", "傳達", "Please convey my thanks to him.", "請代我向他致謝。"),
            ("confidential", "adj.", "機密的", "This information is confidential.", "此資訊為機密。"),
            ("disclaimer", "n.", "免責聲明", "Read the disclaimer carefully.", "仔細閱讀免責聲明。"),
            ("draft", "n./v.", "草稿；起草", "I finished the first draft.", "我完成了初稿。"),
            ("endorse", "v.", "背書；認可", "The celebrity endorsed the product.", "名人為產品代言。"),
            ("forward", "v.", "轉寄", "Please forward this to the team.", "請將此轉寄給團隊。"),
            ("headline", "n.", "標題", "The headline attracted attention.", "標題吸引了注意力。"),
            ("interpret", "v.", "口譯；解讀", "She interpreted for the delegates.", "她為代表們口譯。"),
            ("proofread", "v.", "校對", "Please proofread the document.", "請校對文件。"),
            ("quote", "v./n.", "引用；報價", "He quoted the company policy.", "他引用了公司政策。"),
            ("summarize", "v.", "總結", "Please summarize the main points.", "請總結要點。"),
            ("unanimous", "adj.", "一致的", "The decision was unanimous.", "決定是一致通過的。"),
        ],
        [
            ("agenda", "n.", "議程", "The agenda includes five topics.", "議程包含五個主題。"),
            ("attachment", "n.", "附件", "Please see the attachment.", "請看附件。"),
            ("brochure", "n.", "手冊", "We designed a new brochure.", "我們設計了新手冊。"),
            ("collaboration", "n.", "合作", "This requires team collaboration.", "這需要團隊合作。"),
            ("comprehensive", "adj.", "全面的", "A comprehensive report was prepared.", "一份全面的報告已準備好。"),
            ("deliberate", "adj./v.", "故意的；審議", "It was a deliberate decision.", "這是一個深思熟慮的決定。"),
            ("elaborate", "v./adj.", "詳述；精緻的", "Please elaborate on your idea.", "請詳述你的想法。"),
            ("facilitate", "v.", "促進", "She facilitated the discussion.", "她促進了討論。"),
            ("initiative", "n.", "主動性；倡議", "Take the initiative to solve it.", "主動解決它。"),
            ("liaison", "n.", "聯絡人", "He is the liaison between teams.", "他是團隊間的聯絡人。"),
            ("milestone", "n.", "里程碑", "This is a major milestone.", "這是一個重大里程碑。"),
            ("consensus", "n.", "共識", "We reached a consensus.", "我們達成了共識。"),
            ("correspondence", "n.", "通信", "Handle the correspondence daily.", "每天處理通信。"),
            ("spokesperson", "n.", "發言人", "The spokesperson made a statement.", "發言人發表了聲明。"),
            ("testimony", "n.", "證詞", "He gave his testimony in court.", "他在法庭作證。"),
        ],
        [
            ("address", "v.", "處理；發表演說", "The CEO addressed the issue.", "執行長處理了這個問題。"),
            ("allocate", "v.", "分配", "Funds were allocated to research.", "資金被分配到研究。"),
            ("comply", "v.", "遵守", "All staff must comply with rules.", "所有員工必須遵守規定。"),
            ("consent", "n./v.", "同意", "We need your written consent.", "我們需要你的書面同意。"),
            ("delegate", "v./n.", "委派；代表", "Delegate tasks to your team.", "將任務委派給團隊。"),
            ("disclose", "v.", "揭露", "The company disclosed the results.", "公司揭露了結果。"),
            ("enforce", "v.", "執行；強制", "The new rules will be enforced.", "新規定將被執行。"),
            ("implement", "v.", "實施", "The plan was implemented quickly.", "計畫迅速實施。"),
            ("mediate", "v.", "調解", "She mediated the dispute.", "她調解了紛爭。"),
            ("notify", "v.", "通知", "We will notify you by email.", "我們會透過電郵通知你。"),
            ("petition", "n./v.", "請願", "They signed a petition.", "他們簽署了請願書。"),
            ("protocol", "n.", "協議；禮儀", "Follow the safety protocol.", "遵循安全協議。"),
            ("ratify", "v.", "批准", "The agreement was ratified.", "協議已被批准。"),
            ("stipulate", "v.", "規定", "The contract stipulates payment terms.", "合約規定付款條件。"),
            ("unanimous", "adj.", "全體一致的", "The vote was unanimous.", "投票結果全體一致。"),
        ],
        [
            ("articulate", "v./adj.", "清楚表達；清晰的", "She articulated her ideas clearly.", "她清楚表達了她的想法。"),
            ("bilateral", "adj.", "雙邊的", "A bilateral agreement was signed.", "簽署了雙邊協議。"),
            ("concise", "adj.", "簡潔的", "Keep the message concise.", "保持訊息簡潔。"),
            ("diplomatic", "adj.", "外交的；圓融的", "She gave a diplomatic response.", "她給了圓融的回應。"),
            ("eloquent", "adj.", "雄辯的", "The speaker was very eloquent.", "演講者非常有口才。"),
            ("facilitate", "v.", "促進", "Technology facilitates communication.", "科技促進了溝通。"),
            ("impartial", "adj.", "公正的", "The judge was impartial.", "法官是公正的。"),
            ("legitimate", "adj.", "合法的；正當的", "This is a legitimate concern.", "這是正當的顧慮。"),
            ("memorandum", "n.", "備忘錄", "A memorandum was circulated.", "備忘錄已傳閱。"),
            ("outreach", "n.", "外展服務", "Community outreach is important.", "社區外展服務很重要。"),
            ("precede", "v.", "在...之前", "A welcome speech preceded the event.", "歡迎致詞在活動之前。"),
            ("repeal", "v.", "廢除", "The law was repealed.", "法律被廢除了。"),
            ("solicit", "v.", "徵求", "We solicited feedback from clients.", "我們徵求客戶回饋。"),
            ("tentative", "adj.", "暫定的", "This is a tentative schedule.", "這是暫定的時程表。"),
            ("convene", "v.", "召開", "The board will convene next Monday.", "董事會下週一召開。"),
        ],
    ]

    grammar = """## 被動語態 (Passive Voice) — TOEIC 必考文法

主動語態：主詞做動作 (The manager signed the contract.)
被動語態：主詞接受動作 (The contract was signed by the manager.)

## 一、被動語態的基本結構
be 動詞 + 過去分詞 (p.p.)

各時態的被動形式：
簡單現在式：am/is/are + p.p.
簡單過去式：was/were + p.p.
簡單未來式：will be + p.p.
現在完成式：have/has been + p.p.
現在進行式：am/is/are being + p.p.

EX: The report is written by Ms. Chen every month. (現在式被動)
EX: 報告每個月由陳小姐撰寫。

EX: The contract was signed yesterday. (過去式被動)
EX: 合約昨天被簽署了。

EX: The new policy will be announced next week. (未來式被動)
EX: 新政策下週將被宣布。

EX: The documents have been reviewed. (現在完成式被動)
EX: 文件已被審閱。

## 二、何時使用被動語態
1. 不知道或不重要誰做的：The window was broken. (窗戶被打破了)
2. 強調動作的接受者：The award was given to Mr. Park. (獎項頒給了朴先生)
3. 正式公文或公告：Applications must be submitted by May 1. (申請必須在五月一日前提交)

## 三、TOEIC 常考被動語態句型
1. be supposed to = 應該被期望：Employees are supposed to arrive by 9.
2. be required to = 被要求：All visitors are required to sign in.
3. be expected to = 被期望：Sales are expected to increase.
4. be scheduled to = 被安排：The meeting is scheduled to start at 2.
5. be designed to = 被設計來：The program is designed to improve efficiency.

EX: All employees are required to attend the training session.
EX: 所有員工都被要求參加培訓。

## 四、by 以外的介係詞搭配被動語態
be interested in (對...感興趣)
be satisfied with (對...滿意)
be involved in (參與...)
be known for (以...聞名)
be concerned about (對...擔心)
be composed of (由...組成)

EX: The committee is composed of five members.
EX: 委員會由五名成員組成。"""

    part5 = [
        ("The new schedule _______ to all employees yesterday.", "distributed", "was distributed", "distributing", "has distributed"),
        ("Applications must _______ by the end of this month.", "submit", "submitted", "be submitted", "submitting"),
        ("The building _______ designed by a famous architect.", "is", "was", "has", "had"),
        ("All customers are _______ to provide identification.", "require", "required", "requiring", "requirement"),
        ("The meeting has been _______ until next Monday.", "postpone", "postponing", "postponed", "postponement"),
        ("The results will _______ published in the next issue.", "be", "been", "being", "is"),
        ("The bridge is currently being _______ due to safety concerns.", "repair", "repaired", "repairing", "repairs"),
        ("Ms. Park was _______ as the new department head.", "appoint", "appointing", "appointment", "appointed"),
        ("The email was _______ to the wrong address by mistake.", "send", "sent", "sending", "sends"),
        ("The project is expected _______ completed by December.", "be", "to be", "being", "been"),
        ("The documents should be _______ before the meeting.", "review", "reviewing", "reviewed", "reviews"),
        ("The award ceremony is _______ to take place next Saturday.", "schedule", "scheduling", "scheduled", "schedules"),
        ("All complaints will be _______ within 48 hours.", "address", "addressing", "addressed", "addresses"),
        ("The proposal was _______ by the board of directors.", "approve", "approving", "approved", "approval"),
        ("Employees are _______ to wear safety equipment.", "require", "requiring", "required", "requirement"),
        ("The conference room is being _______ for the event.", "prepare", "prepared", "preparing", "preparation"),
        ("This product was _______ in Japan.", "manufacture", "manufactured", "manufacturing", "manufacturer"),
        ("The tickets have already been _______.", "sell", "sold", "selling", "sells"),
        ("The memo is _______ to inform staff of the changes.", "design", "designing", "designed", "designs"),
        ("New employees are _______ with a welcome package.", "provide", "providing", "provided", "provision"),
    ]

    reading_title = "Memo: New Internal Communication Policy"
    reading_pass = """MEMORANDUM

TO: All Department Managers
FROM: Linda Park, Director of Human Resources
DATE: September 3
RE: Updated Internal Communication Policy

Effective October 1, the company will implement a new internal communication policy to improve efficiency and reduce misunderstandings.

Key Changes:
1. All official announcements must be communicated through the company intranet. Email chains for company-wide announcements will no longer be permitted.
2. Department meetings are required to be held at least twice a month. Meeting minutes must be uploaded to the shared drive within 24 hours.
3. A new instant messaging platform, TeamConnect, will be introduced for daily communication between colleagues. Training sessions on the new platform will be held during the last week of September.
4. Confidential information must not be shared through any unofficial channels, including personal email accounts and social media.

All managers are expected to brief their teams on these changes before the implementation date. A detailed guide has been attached to this memo for your reference.

If you have any questions or concerns, please do not hesitate to contact the HR department at hr@company.com or extension 3500.

Thank you for your cooperation."""

    reading_qs = [
        ("What is the purpose of this memo?", "To announce staff promotions", "To introduce a new communication policy", "To schedule a company event", "To request budget proposals"),
        ("When will the new policy take effect?", "September 3", "September 30", "October 1", "October 15"),
        ("How often must department meetings be held?", "Once a week", "At least twice a month", "Every day", "Once a month"),
        ("What should managers do before October 1?", "Submit their budgets", "Brief their teams on the changes", "Complete an online survey", "Hire new staff"),
        ("What is TeamConnect?", "A video conferencing tool", "An instant messaging platform", "An email service", "A project management tool"),
    ]

    p5_answers = [
        ("B", "主詞 schedule 是「被分發」，yesterday 是過去式，用 was distributed。"),
        ("C", "must 後接原形，Applications「被提交」用被動 be submitted。"),
        ("B", "The building 是「被設計」的，配合 by a famous architect 判斷為被動過去式 was。"),
        ("B", "are required to 是常見被動語態搭配，意思是「被要求」。"),
        ("C", "has been + p.p.，postpone 的過去分詞是 postponed。"),
        ("A", "will + 原形，被動用 will be published。"),
        ("B", "is being + p.p. 是現在進行式被動，用 repaired。"),
        ("D", "was + p.p.，appoint 的過去分詞是 appointed。"),
        ("B", "was + p.p.，send 的過去分詞是 sent。"),
        ("B", "is expected to be 是固定搭配。"),
        ("C", "should be + p.p.，review 的過去分詞是 reviewed。"),
        ("C", "is scheduled to 是固定被動搭配，意思是「被安排」。"),
        ("C", "will be + p.p.，address 的過去分詞是 addressed。"),
        ("C", "was + p.p.，approve 的過去分詞是 approved。"),
        ("C", "are required to 是常見被動語態，required 是過去分詞。"),
        ("B", "is being + p.p.，prepare 的過去分詞是 prepared。"),
        ("B", "was + p.p.，manufacture 的過去分詞是 manufactured。"),
        ("B", "have been + p.p.，sell 的過去分詞是 sold。"),
        ("C", "is designed to 是固定被動搭配。"),
        ("C", "are provided with 是常見被動語態搭配。"),
    ]

    rd_answers = [
        ("B", "備忘錄主旨為 Updated Internal Communication Policy。"),
        ("C", "文中提到 Effective October 1。"),
        ("B", "文中提到 Department meetings are required to be held at least twice a month。"),
        ("B", "文中提到 All managers are expected to brief their teams on these changes before the implementation date。"),
        ("B", "文中提到 A new instant messaging platform, TeamConnect。"),
    ]

    build_week(4, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week05():
    title = "Manufacturing/Tech Vocabulary + Relative Clauses"
    vocab_days = [
        [
            ("assemble", "v.", "組裝", "Workers assemble the parts by hand.", "工人手工組裝零件。"),
            ("automate", "v.", "自動化", "The factory automated its production line.", "工廠將生產線自動化。"),
            ("component", "n.", "零件", "Each component is inspected carefully.", "每個零件都被仔細檢查。"),
            ("defect", "n.", "缺陷", "The product was recalled due to a defect.", "產品因缺陷而被召回。"),
            ("efficiency", "n.", "效率", "We improved production efficiency.", "我們提高了生產效率。"),
            ("facility", "n.", "設施；工廠", "The new facility opens next month.", "新設施下個月啟用。"),
            ("generate", "v.", "產生", "Solar panels generate electricity.", "太陽能板產生電力。"),
            ("hazardous", "adj.", "危險的", "Handle hazardous materials carefully.", "小心處理危險物質。"),
            ("innovation", "n.", "創新", "Innovation drives our company forward.", "創新推動公司前進。"),
            ("malfunction", "n./v.", "故障", "The machine malfunctioned.", "機器故障了。"),
            ("output", "n.", "產出", "Daily output increased by 20%.", "每日產出增加了20%。"),
            ("precision", "n.", "精確度", "This requires high precision.", "這需要高精確度。"),
            ("prototype", "n.", "原型", "We built a working prototype.", "我們製作了可運作的原型。"),
            ("specification", "n.", "規格", "Check the technical specifications.", "檢查技術規格。"),
            ("warehouse", "n.", "倉庫", "The products are stored in the warehouse.", "產品儲存在倉庫裡。"),
        ],
        [
            ("algorithm", "n.", "演算法", "The algorithm processes data quickly.", "演算法快速處理資料。"),
            ("bandwidth", "n.", "頻寬", "Upgrade your bandwidth for faster speed.", "升級頻寬以加快速度。"),
            ("compatible", "adj.", "相容的", "Is this software compatible with Mac?", "這個軟體和 Mac 相容嗎？"),
            ("database", "n.", "資料庫", "Update the customer database.", "更新客戶資料庫。"),
            ("encrypt", "v.", "加密", "All data is encrypted for security.", "所有資料都加密以確保安全。"),
            ("firmware", "n.", "韌體", "Update the device firmware.", "更新裝置韌體。"),
            ("glitch", "n.", "小故障", "There was a glitch in the system.", "系統出現了小故障。"),
            ("hardware", "n.", "硬體", "We need new hardware.", "我們需要新硬體。"),
            ("interface", "n.", "介面", "The user interface is intuitive.", "使用者介面很直覺。"),
            ("malware", "n.", "惡意軟體", "Install protection against malware.", "安裝惡意軟體防護。"),
            ("network", "n.", "網路", "The network is down.", "網路斷了。"),
            ("optimize", "v.", "最佳化", "Optimize the website for mobile.", "為行動裝置最佳化網站。"),
            ("peripheral", "n./adj.", "周邊設備", "Connect the peripheral devices.", "連接周邊設備。"),
            ("server", "n.", "伺服器", "The server crashed yesterday.", "伺服器昨天當機了。"),
            ("upgrade", "v./n.", "升級", "We need to upgrade the software.", "我們需要升級軟體。"),
        ],
        [
            ("blueprint", "n.", "藍圖", "Review the building blueprint.", "審查建築藍圖。"),
            ("calibrate", "v.", "校準", "Calibrate the instruments regularly.", "定期校準儀器。"),
            ("compliance", "n.", "合規", "Ensure compliance with safety standards.", "確保符合安全標準。"),
            ("diagnostic", "adj./n.", "診斷的", "Run a diagnostic test.", "執行診斷測試。"),
            ("emission", "n.", "排放", "Reduce carbon emissions.", "減少碳排放。"),
            ("fabricate", "v.", "製造；捏造", "The parts are fabricated locally.", "零件在當地製造。"),
            ("implement", "v.", "實施", "Implement the new system.", "實施新系統。"),
            ("logistics", "n.", "物流", "The logistics team handles shipping.", "物流團隊處理運送。"),
            ("module", "n.", "模組", "Install the new software module.", "安裝新的軟體模組。"),
            ("obsolete", "adj.", "過時的", "This technology is obsolete.", "這項技術已過時。"),
            ("patent", "n.", "專利", "They filed for a patent.", "他們申請了專利。"),
            ("quality", "n.", "品質", "Quality control is essential.", "品質管控是必要的。"),
            ("robust", "adj.", "強健的", "The system is robust and reliable.", "系統強健且可靠。"),
            ("simulate", "v.", "模擬", "We simulated the test conditions.", "我們模擬了測試條件。"),
            ("turbine", "n.", "渦輪", "The wind turbine generates power.", "風力渦輪產生電力。"),
        ],
        [
            ("batch", "n.", "批次", "The first batch is ready.", "第一批次已準備好。"),
            ("capacity", "n.", "容量；產能", "The factory is at full capacity.", "工廠已滿產能。"),
            ("deploy", "v.", "部署", "Deploy the new software update.", "部署新的軟體更新。"),
            ("durable", "adj.", "耐用的", "This material is very durable.", "這種材料非常耐用。"),
            ("ergonomic", "adj.", "符合人體工學的", "Use ergonomic chairs.", "使用人體工學椅子。"),
            ("integrate", "v.", "整合", "Integrate the new system.", "整合新系統。"),
            ("inventory", "n.", "庫存", "Check the inventory levels.", "檢查庫存量。"),
            ("maintenance", "n.", "維護", "Schedule regular maintenance.", "安排定期維護。"),
            ("overhaul", "v./n.", "大修", "The engine needs an overhaul.", "引擎需要大修。"),
            ("procurement", "n.", "採購", "The procurement process is strict.", "採購流程很嚴格。"),
            ("reliability", "n.", "可靠性", "Reliability is our top priority.", "可靠性是我們的首要目標。"),
            ("streamline", "v.", "精簡", "Streamline the manufacturing process.", "精簡製造流程。"),
            ("throughput", "n.", "產量；處理量", "Increase system throughput.", "提高系統處理量。"),
            ("vendor", "n.", "供應商", "Select a reliable vendor.", "選擇可靠的供應商。"),
            ("yield", "n./v.", "產量；產出", "The yield improved this quarter.", "本季產量提升了。"),
        ],
        [
            ("benchmark", "n.", "基準", "Set performance benchmarks.", "設定績效基準。"),
            ("cyber", "adj.", "網路的", "Cyber security is critical.", "網路安全至關重要。"),
            ("disruptive", "adj.", "顛覆性的", "AI is a disruptive technology.", "AI是顛覆性的技術。"),
            ("ecosystem", "n.", "生態系統", "Build a tech ecosystem.", "建立科技生態系統。"),
            ("infrastructure", "n.", "基礎建設", "Improve the IT infrastructure.", "改善IT基礎建設。"),
            ("latency", "n.", "延遲", "Low latency is essential for gaming.", "低延遲對遊戲很重要。"),
            ("middleware", "n.", "中介軟體", "Install the middleware layer.", "安裝中介軟體層。"),
            ("protocol", "n.", "協議", "Follow the network protocol.", "遵循網路協議。"),
            ("redundancy", "n.", "冗餘", "Build redundancy into the system.", "在系統中建立冗餘。"),
            ("scalable", "adj.", "可擴展的", "The solution must be scalable.", "解決方案必須可擴展。"),
            ("sustainable", "adj.", "永續的", "Adopt sustainable practices.", "採用永續作法。"),
            ("troubleshoot", "v.", "排除故障", "She troubleshot the network issue.", "她排除了網路問題。"),
            ("utility", "n.", "公用事業；效用", "Pay the utility bills.", "支付水電費。"),
            ("versatile", "adj.", "多功能的", "This tool is very versatile.", "這工具非常多功能。"),
            ("wireframe", "n.", "線框圖", "Create a wireframe for the app.", "為應用程式建立線框圖。"),
        ],
    ]

    grammar = """## 關係子句 (Relative Clauses) — TOEIC 常考句型

關係子句用來修飾名詞，相當於形容詞的功能。

## 一、關係代名詞
who：修飾「人」（當主詞）
whom：修飾「人」（當受詞）
which：修飾「物」
that：修飾「人或物」（限定用法）
whose：表示「所有格」（...的）

EX: The employee who submitted the report was promoted.
EX: 提交報告的那位員工被升遷了。(who 代替 the employee，當主詞)

EX: The product which was released last month is very popular.
EX: 上個月發布的產品非常受歡迎。(which 代替 the product)

EX: The manager whose office is on the 5th floor will attend.
EX: 辦公室在五樓的那位經理會出席。(whose = the manager's)

## 二、限定 vs. 非限定關係子句
限定子句（不加逗號）：提供必要的辨識資訊
非限定子句（加逗號）：提供額外補充資訊

EX: The workers who completed the training will receive a certificate.
EX: 完成訓練的工人將獲得證書。（限定：只有完成的才會拿到）

EX: Mr. Chen, who has 20 years of experience, will lead the project.
EX: 陳先生有20年經驗，他將領導這個專案。（非限定：補充說明）

注意：非限定子句不能用 that，只能用 who/which。

## 三、關係副詞
where：代替地點
when：代替時間
why：代替原因

EX: The factory where the parts are made is in Taichung.
EX: 零件生產的工廠在台中。

EX: Monday is the day when the weekly meeting is held.
EX: 星期一是舉行週會的日子。

## 四、TOEIC 常考重點
1. 判斷空格後是否缺主詞：缺主詞用 who/which/that
2. 判斷空格後是否缺受詞：缺受詞用 whom/which/that（或省略）
3. 空格後有名詞（所有格概念）：用 whose
4. 注意 that 不能用在非限定子句（有逗號的情況）

EX: The report _______ was submitted yesterday contained errors.
EX: → which/that（缺主詞）

EX: The technician _______ we hired is very experienced.
EX: → whom/that/省略（缺受詞）"""

    part5 = [
        ("The engineer _______ designed the system received an award.", "who", "whom", "whose", "which"),
        ("The software _______ we purchased last year needs updating.", "who", "whose", "what", "that"),
        ("The factory, _______ is located in Taoyuan, produces electronics.", "that", "which", "who", "what"),
        ("Employees _______ complete the training will receive a bonus.", "who", "whom", "whose", "which"),
        ("The company _______ products are sold worldwide is expanding.", "who", "which", "whose", "whom"),
        ("The warehouse _______ we store raw materials is being renovated.", "which", "where", "who", "when"),
        ("The technician _______ fixed the machine is very skilled.", "whom", "whose", "who", "which"),
        ("This is the device _______ can process data 10 times faster.", "who", "whom", "that", "whose"),
        ("Ms. Lee, _______ joined the company in 2015, was promoted.", "that", "which", "whom", "who"),
        ("The deadline by _______ all reports must be submitted is Friday.", "that", "which", "who", "where"),
        ("The office _______ the meeting will be held has been changed.", "which", "who", "where", "when"),
        ("Workers _______ safety training has expired must retake the course.", "who", "whom", "which", "whose"),
        ("The prototype _______ the team developed won first prize.", "who", "whom", "whose", "that"),
        ("July is the month _______ the annual inspection takes place.", "which", "where", "when", "who"),
        ("The supervisor, _______ has been with the company for 15 years, will retire.", "that", "whom", "which", "who"),
        ("The parts _______ were ordered last week have not arrived yet.", "who", "whose", "that", "whom"),
        ("The reason _______ the machine stopped has been identified.", "which", "where", "who", "why"),
        ("The manager _______ I spoke to approved the request.", "who", "which", "whom", "whose"),
        ("The company released a product _______ features include voice recognition.", "who", "whose", "which", "whom"),
        ("The building _______ the server room is located has backup power.", "when", "which", "who", "where"),
    ]

    reading_title = "Article: New Manufacturing Facility Opens"
    reading_pass = """TECHPRO INDUSTRIES OPENS STATE-OF-THE-ART FACILITY

TechPro Industries announced the opening of its new manufacturing facility in Hsinchu Science Park on March 15. The 50,000-square-meter facility, which cost approximately $200 million to build, is expected to create over 500 new jobs in the region.

The facility features fully automated production lines that use advanced robotics and artificial intelligence to improve efficiency and reduce defects. According to CEO David Wang, "This facility represents our commitment to innovation and quality. We expect to increase our annual output by 40% while reducing production costs by 15%."

The new facility will primarily produce semiconductor components for the automotive and telecommunications industries. Production is scheduled to begin in April, with full capacity expected by the third quarter.

TechPro Industries, which was founded in 1998, has grown to become one of the leading manufacturers of electronic components in Asia. The company currently operates three other facilities in Taiwan and one in Vietnam.

Local government officials attended the opening ceremony and praised TechPro for its contribution to the local economy. Mayor Chen stated that the new facility would significantly boost employment and bring economic benefits to the surrounding community."""

    reading_qs = [
        ("Where is the new TechPro facility located?", "Taipei", "Hsinchu Science Park", "Vietnam", "Kaohsiung"),
        ("How many new jobs is the facility expected to create?", "Over 200", "Over 300", "Over 500", "Over 1000"),
        ("What does the facility primarily produce?", "Consumer electronics", "Medical devices", "Semiconductor components", "Solar panels"),
        ("When is the facility expected to reach full capacity?", "March", "April", "By the second quarter", "By the third quarter"),
        ("How many facilities does TechPro currently operate in total?", "Three", "Four", "Five", "Six"),
    ]

    p5_answers = [
        ("A", "先行詞是 The engineer（人），空格後缺主詞（designed 的主詞），用 who。"),
        ("D", "先行詞是 The software（物），空格後有主詞 we，用 that（也可用 which）。"),
        ("B", "有逗號的非限定子句不能用 that，先行詞是 The factory（物），用 which。"),
        ("A", "先行詞是 Employees（人），空格後缺主詞，用 who。"),
        ("C", "空格後有名詞 products（所有格概念），用 whose。"),
        ("B", "先行詞是 The warehouse（地點），用 where。"),
        ("C", "先行詞是 The technician（人），空格後缺主詞，用 who。"),
        ("C", "先行詞是 the device（物），空格後缺主詞，用 that。"),
        ("D", "有逗號的非限定子句，先行詞是 Ms. Lee（人），用 who。"),
        ("B", "介係詞 by 後面接 which（物），不能用 that。"),
        ("C", "先行詞是 The office（地點），用 where。"),
        ("D", "空格後有名詞 safety training（所有格概念），用 whose。"),
        ("D", "先行詞是 The prototype（物），空格後有主詞 the team，用 that。"),
        ("C", "先行詞是 the month（時間），用 when。"),
        ("D", "有逗號的非限定子句，先行詞是 The supervisor（人），用 who。"),
        ("C", "先行詞是 The parts（物），空格後缺主詞，用 that。"),
        ("D", "先行詞是 The reason（原因），用 why。"),
        ("C", "先行詞是 The manager（人），空格是 spoke to 的受詞，用 whom。"),
        ("B", "空格後有名詞 features（所有格概念），用 whose。"),
        ("D", "先行詞是 The building（地點），用 where。"),
    ]

    rd_answers = [
        ("B", "文中提到 its new manufacturing facility in Hsinchu Science Park。"),
        ("C", "文中提到 is expected to create over 500 new jobs。"),
        ("C", "文中提到 will primarily produce semiconductor components。"),
        ("D", "文中提到 with full capacity expected by the third quarter。"),
        ("C", "文中提到目前有 three other facilities in Taiwan and one in Vietnam，加上新設施共五座。但注意本題問 currently operate，新設施尚未全面運營，所以答案可能被理解為四座。然而加上剛開幕的新設施共五座。"),
    ]

    build_week(5, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


# =====================================================================
# Main entry
# =====================================================================

def week06():
    title = "Finance/Banking Vocabulary + Conjunctions"
    vocab_days = [
        [
            ("account", "n.", "帳戶", "Open a savings account.", "開一個儲蓄帳戶。"),
            ("balance", "n.", "餘額", "Check your account balance.", "查看你的帳戶餘額。"),
            ("deposit", "n./v.", "存款", "I deposited $500 today.", "我今天存了500美元。"),
            ("withdraw", "v.", "提款", "She withdrew cash from the ATM.", "她從ATM提了現金。"),
            ("loan", "n.", "貸款", "He applied for a bank loan.", "他申請了銀行貸款。"),
            ("mortgage", "n.", "房貸", "They took out a mortgage.", "他們申請了房貸。"),
            ("interest", "n.", "利息；興趣", "The interest rate is 3%.", "利率是3%。"),
            ("dividend", "n.", "股利", "Shareholders received dividends.", "股東收到了股利。"),
            ("revenue", "n.", "營收", "Annual revenue exceeded $10 million.", "年營收超過一千萬美元。"),
            ("expenditure", "n.", "支出", "Government expenditure increased.", "政府支出增加了。"),
            ("audit", "n./v.", "稽核", "The company passed the audit.", "公司通過了稽核。"),
            ("fiscal", "adj.", "財政的", "The fiscal year ends in March.", "財政年度在三月結束。"),
            ("inflation", "n.", "通膨", "Inflation is at a 10-year high.", "通膨達到十年新高。"),
            ("asset", "n.", "資產", "The company sold some assets.", "公司出售了一些資產。"),
            ("liability", "n.", "負債", "The firm reduced its liabilities.", "公司減少了負債。"),
        ],
        [
            ("bankrupt", "adj.", "破產的", "The company went bankrupt.", "公司破產了。"),
            ("collateral", "n.", "擔保品", "The bank requires collateral.", "銀行要求擔保品。"),
            ("commodity", "n.", "商品；原物料", "Oil is a valuable commodity.", "石油是有價值的原物料。"),
            ("currency", "n.", "貨幣", "Foreign currency exchange rates.", "外幣匯率。"),
            ("deduction", "n.", "扣除", "Tax deductions are available.", "有稅務扣除可使用。"),
            ("equity", "n.", "股權；淨值", "Home equity has increased.", "房屋淨值增加了。"),
            ("forecast", "n./v.", "預測", "The economic forecast is positive.", "經濟預測是正面的。"),
            ("gross", "adj.", "毛額的；總的", "Gross profit rose by 8%.", "毛利增長了8%。"),
            ("hedge", "v./n.", "避險", "Investors hedge against risk.", "投資者進行避險。"),
            ("installment", "n.", "分期付款", "Pay in monthly installments.", "按月分期付款。"),
            ("ledger", "n.", "帳簿", "Record transactions in the ledger.", "在帳簿中記錄交易。"),
            ("maturity", "n.", "到期日", "The bond reaches maturity in 2030.", "債券在2030年到期。"),
            ("portfolio", "n.", "投資組合", "Diversify your portfolio.", "分散你的投資組合。"),
            ("reimburse", "v.", "報銷", "We will reimburse your expenses.", "我們會報銷你的費用。"),
            ("subsidy", "n.", "補助金", "The government offers subsidies.", "政府提供補助金。"),
        ],
        [
            ("accrue", "v.", "累積", "Interest accrues monthly.", "利息每月累積。"),
            ("amortize", "v.", "分期攤還", "Amortize the loan over 20 years.", "分20年攤還貸款。"),
            ("appraisal", "n.", "評估", "Get a property appraisal.", "進行房產評估。"),
            ("broker", "n.", "經紀人", "Contact your insurance broker.", "聯繫你的保險經紀人。"),
            ("capitalize", "v.", "資本化", "Capitalize on market opportunities.", "把握市場機會。"),
            ("consolidate", "v.", "合併", "Consolidate your debts.", "合併你的債務。"),
            ("depreciate", "v.", "折舊；貶值", "The car depreciated quickly.", "車子很快就折舊了。"),
            ("diversify", "v.", "多角化", "Diversify your investments.", "分散你的投資。"),
            ("exempt", "adj.", "免除的", "Some items are tax-exempt.", "有些物品免稅。"),
            ("fluctuate", "v.", "波動", "Stock prices fluctuate daily.", "股價每天波動。"),
            ("lucrative", "adj.", "有利可圖的", "It is a lucrative business.", "這是有利可圖的生意。"),
            ("monetary", "adj.", "貨幣的", "The central bank sets monetary policy.", "央行制定貨幣政策。"),
            ("net", "adj.", "淨的", "Net income increased by 12%.", "淨收入增加了12%。"),
            ("premium", "n.", "保費；溢價", "Insurance premiums went up.", "保費上漲了。"),
            ("solvent", "adj.", "有償付能力的", "The company remains solvent.", "公司仍具有償付能力。"),
        ],
        [
            ("allocate", "v.", "分配", "Allocate funds to each department.", "將資金分配給各部門。"),
            ("authorize", "v.", "授權", "The bank authorized the payment.", "銀行授權了付款。"),
            ("breakeven", "n./adj.", "損益平衡", "We reached breakeven in year two.", "我們在第二年達到損益平衡。"),
            ("deficit", "n.", "赤字", "The budget deficit is growing.", "預算赤字在增長。"),
            ("endowment", "n.", "捐款基金", "The university received an endowment.", "大學收到了捐款基金。"),
            ("fiduciary", "adj.", "受託的", "A fiduciary duty to clients.", "對客戶的受託責任。"),
            ("guarantee", "n./v.", "保證", "A money-back guarantee.", "退款保證。"),
            ("insolvency", "n.", "無力償還", "The company faced insolvency.", "公司面臨無力償還。"),
            ("leverage", "n./v.", "槓桿", "Use financial leverage wisely.", "明智地使用財務槓桿。"),
            ("overhead", "n.", "經常性開支", "Reduce overhead costs.", "降低經常性開支。"),
            ("principal", "n.", "本金；校長", "Pay off the principal first.", "先還本金。"),
            ("quarters", "n.", "季度", "Earnings improved in Q3.", "第三季獲利改善。"),
            ("securities", "n.", "證券", "Trade government securities.", "交易政府證券。"),
            ("tariff", "n.", "關稅", "New tariffs were imposed.", "新關稅被施加了。"),
            ("venture", "n.", "創投；企業", "A joint venture was formed.", "成立了合資企業。"),
        ],
        [
            ("acquisition", "n.", "收購", "The acquisition cost $2 billion.", "收購花了20億美元。"),
            ("benchmark", "n.", "基準", "Use the index as a benchmark.", "以指數作為基準。"),
            ("comply", "v.", "遵守", "Comply with financial regulations.", "遵守金融法規。"),
            ("disclosure", "n.", "揭露", "Full disclosure is required.", "需要充分揭露。"),
            ("eligible", "adj.", "有資格的", "You are eligible for a loan.", "你有資格申請貸款。"),
            ("franchise", "n.", "加盟", "Open a restaurant franchise.", "開一間加盟餐廳。"),
            ("incentive", "n.", "獎勵；誘因", "Tax incentives attract investors.", "稅務獎勵吸引投資者。"),
            ("liquidate", "v.", "清算", "The firm was liquidated.", "公司被清算了。"),
            ("merger", "n.", "合併", "The merger was approved.", "合併案獲得批准。"),
            ("prospectus", "n.", "公開說明書", "Read the prospectus carefully.", "仔細閱讀公開說明書。"),
            ("quota", "n.", "配額", "Meet the sales quota.", "達到銷售配額。"),
            ("recession", "n.", "經濟衰退", "The economy is in recession.", "經濟正在衰退。"),
            ("surplus", "n.", "盈餘", "The budget shows a surplus.", "預算顯示有盈餘。"),
            ("transaction", "n.", "交易", "Complete the transaction online.", "在線上完成交易。"),
            ("yield", "n.", "殖利率", "Bond yields are rising.", "債券殖利率正在上升。"),
        ],
    ]

    grammar = """## 連接詞 (Conjunctions) — TOEIC Part 5 & 6 常考

連接詞用來連接字詞、片語或子句。TOEIC 最常考的是連接兩個子句的連接詞。

## 一、對等連接詞 (Coordinating Conjunctions)
and（而且）, but（但是）, or（或者）, so（所以）, yet（然而）, nor（也不）

EX: The product is affordable and reliable.
EX: 產品價格實惠且可靠。

EX: Sales increased, but profits declined.
EX: 銷售額增加，但利潤下降。

## 二、從屬連接詞 (Subordinating Conjunctions)

表示原因：because / since / as（因為）
EX: The project was delayed because the budget was cut.
EX: 專案被延遲，因為預算被削減了。

表示讓步：although / though / even though（雖然）
EX: Although the price increased, demand remained strong.
EX: 雖然價格上漲，需求仍然強勁。

表示條件：if / unless / provided that（如果/除非/只要）
EX: You will receive a bonus if you meet the target.
EX: 如果你達到目標，你會收到獎金。

表示時間：when / while / before / after / until / as soon as
EX: Please submit the form before the deadline.
EX: 請在截止日期前提交表格。

## 三、TOEIC 最常考的混淆題

1. because vs. because of
because + 子句（主詞 + 動詞）
because of + 名詞/名詞片語

EX: The event was canceled because it rained heavily.
EX: The event was canceled because of heavy rain.
EX: 活動因為大雨而取消。

2. although vs. despite / in spite of
although + 子句
despite / in spite of + 名詞/名詞片語

EX: Although the economy is weak, sales improved.
EX: Despite the weak economy, sales improved.
EX: 儘管經濟疲弱，銷售仍然改善。

3. so vs. so that
so = 所以（表結果）
so that = 為了（表目的）

EX: It rained, so the event was moved indoors.
EX: 下雨了，所以活動移到室內。
EX: We left early so that we could avoid traffic.
EX: 我們提早離開，以避免塞車。

## 四、常考句型
not only ... but also（不僅...而且）
either ... or（不是...就是）
neither ... nor（既不...也不）
both ... and（兩者都）

EX: The company is not only profitable but also environmentally responsible.
EX: 公司不僅有獲利，而且對環境負責。"""

    part5 = [
        ("Sales increased _______ the marketing campaign was very effective.", "because", "because of", "despite", "although"),
        ("_______ the high cost, many customers still purchased the product.", "Because", "Although", "Despite", "Since"),
        ("The bank was closed, _______ we could not deposit the check.", "but", "so", "or", "yet"),
        ("_______ you have any questions, please contact customer service.", "Although", "Despite", "If", "Because of"),
        ("She finished the report on time _______ she was very busy.", "because", "so", "although", "if"),
        ("The company will expand _______ internationally and domestically.", "either", "neither", "both", "not only"),
        ("We need to cut costs; _______, we will reduce overtime hours.", "moreover", "therefore", "however", "although"),
        ("_______ the deadline was extended, the team still could not finish.", "If", "Because", "Even though", "So that"),
        ("The meeting was postponed _______ the severe weather conditions.", "because", "although", "due to", "so"),
        ("You must submit the application _______ you want to be considered.", "unless", "if", "despite", "although"),
        ("_______ revenue increased, the company's profits still declined.", "Because", "Although", "If", "So"),
        ("The CEO will attend the conference, _______ the CFO will stay behind.", "and", "but", "or", "so"),
        ("The new policy will take effect _______ it is approved by the board.", "unless", "if", "once", "despite"),
        ("We arrived late _______ the traffic was terrible.", "despite", "although", "because", "so"),
        ("The company offers _______ health insurance _______ retirement benefits.", "both / and", "either / or", "neither / nor", "not / but"),
        ("Prices will remain stable _______ the economy improves.", "unless", "if", "because", "despite"),
        ("She studied finance _______ she could work in banking.", "so", "so that", "because of", "despite"),
        ("_______ interest rates rose, borrowing costs increased significantly.", "Although", "Despite", "If", "As"),
        ("The investment is risky, _______ the potential returns are high.", "so", "because", "yet", "if"),
        ("The bank will not approve the loan _______ you provide collateral.", "if", "because", "unless", "although"),
    ]

    reading_title = "Letter: Bank Account Changes"
    reading_pass = """PACIFIC NATIONAL BANK
Customer Service Department
100 Finance Street, Taipei 10050

March 20, 2026

Dear Valued Customer,

We are writing to inform you of important changes to our savings account terms and conditions, effective May 1, 2026.

Key Changes:
1. The minimum balance requirement for the Premium Savings Account will increase from $5,000 to $8,000. Accounts that fall below this amount will be charged a monthly maintenance fee of $15.
2. Interest rates for all savings accounts will be adjusted. The new annual rate for Premium accounts is 2.5%, and for Standard accounts, it is 1.8%.
3. Free ATM withdrawals will be limited to 10 per month. A fee of $2.50 will be charged for each additional withdrawal.
4. Online banking and mobile app transfers will remain free of charge.

We understand these changes may affect your banking experience. To help you transition smoothly, we are offering the following:
- Existing Premium account holders who maintain the new minimum balance will receive a $50 bonus credit.
- Customers who set up automatic deposit of $500 or more monthly will be exempt from the maintenance fee for the first six months.

For questions or to schedule a consultation with a banking advisor, please call 0800-123-456 or visit any of our 45 branches nationwide.

Sincerely,
Jennifer Wu
Vice President, Customer Relations
Pacific National Bank"""

    reading_qs = [
        ("What is the main purpose of this letter?", "To promote a new credit card", "To notify customers of account changes", "To announce branch closures", "To introduce a new banking app"),
        ("What is the new minimum balance for Premium Savings Accounts?", "$2,500", "$5,000", "$8,000", "$15,000"),
        ("How many free ATM withdrawals per month will be allowed?", "5", "8", "10", "15"),
        ("Who will receive a $50 bonus credit?", "All customers", "New customers", "Premium holders who maintain the new minimum balance", "Customers who open a new account"),
        ("What remains free of charge?", "ATM withdrawals", "Online and mobile transfers", "Account maintenance", "Paper statements"),
    ]

    p5_answers = [
        ("A", "空格後是子句 the marketing campaign was very effective，用 because + 子句。"),
        ("C", "空格後是名詞片語 the high cost，用 Despite + 名詞片語。"),
        ("B", "前句是原因（銀行關了），後句是結果（無法存支票），用 so。"),
        ("C", "如果你有問題，用 If（條件）。"),
        ("C", "她按時完成，但她很忙，前後語意相反，用 although（雖然）。"),
        ("C", "both ... and 是固定搭配。"),
        ("B", "前句是原因（削減成本），後句是結果（減少加班），用 therefore（因此）。注意 therefore 是副詞連接詞。"),
        ("C", "即使延長了截止日期，還是無法完成。語意讓步，用 Even though。"),
        ("C", "空格後是名詞片語 the severe weather conditions，用 due to + 名詞片語。"),
        ("B", "如果你想被考慮，用 if（條件）。"),
        ("B", "營收增加但利潤下降，語意相反，用 Although（雖然）。"),
        ("B", "CEO 會出席但 CFO 會留下，語意相反，用 but。"),
        ("C", "一旦被董事會批准就生效，用 once（一旦）。"),
        ("C", "我們遲到了，因為交通很糟，用 because + 子句。"),
        ("A", "both ... and 表示兩者都提供。"),
        ("A", "除非經濟改善，否則價格穩定。用 unless（除非）。"),
        ("B", "她學金融是為了能在銀行工作，表目的用 so that。"),
        ("D", "利率上升，借貸成本增加。As = 因為/當...時。"),
        ("C", "投資有風險，但潛在回報高。語意相反用 yet（然而）。"),
        ("C", "除非你提供擔保品，否則銀行不會批准。用 unless（除非）。"),
    ]

    rd_answers = [
        ("B", "信件主要目的是通知客戶帳戶條款的變更。"),
        ("C", "文中提到 minimum balance requirement will increase from $5,000 to $8,000。"),
        ("C", "文中提到 Free ATM withdrawals will be limited to 10 per month。"),
        ("C", "文中提到 Existing Premium account holders who maintain the new minimum balance will receive a $50 bonus credit。"),
        ("B", "文中提到 Online banking and mobile app transfers will remain free of charge。"),
    ]

    build_week(6, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week07():
    title = "HR/Education Vocabulary + Prepositions"
    vocab_days = [
        [
            ("applicant", "n.", "申請者", "The applicant submitted a resume.", "申請者提交了履歷。"),
            ("benefit", "n.", "福利；好處", "The company offers great benefits.", "公司提供很好的福利。"),
            ("certificate", "n.", "證書", "She earned a teaching certificate.", "她取得了教學證書。"),
            ("curriculum", "n.", "課程", "The curriculum was updated.", "課程被更新了。"),
            ("enrollment", "n.", "註冊", "Enrollment opens in September.", "九月開始報名。"),
            ("faculty", "n.", "教職員", "The faculty meeting is at noon.", "教職員會議在中午。"),
            ("graduate", "v./n.", "畢業", "She graduated with honors.", "她以優異成績畢業。"),
            ("intern", "n.", "實習生", "The intern starts on Monday.", "實習生星期一開始。"),
            ("mentor", "n./v.", "導師", "She mentored the new employees.", "她指導新員工。"),
            ("orientation", "n.", "新人訓練", "New employee orientation is Thursday.", "新員工訓練在週四。"),
            ("probation", "n.", "試用期", "The probation period is 3 months.", "試用期為三個月。"),
            ("qualification", "n.", "資格", "List your qualifications.", "列出你的資格。"),
            ("recruit", "v.", "招募", "We are recruiting new staff.", "我們正在招募新員工。"),
            ("resume", "n.", "履歷", "Submit your resume online.", "在線上提交履歷。"),
            ("tenure", "n.", "任期", "Her tenure as CEO lasted 5 years.", "她擔任CEO的任期為五年。"),
        ],
        [
            ("appraisal", "n.", "考核", "Annual performance appraisals are due.", "年度績效考核到期了。"),
            ("commend", "v.", "表揚", "The manager commended the team.", "經理表揚了團隊。"),
            ("designate", "v.", "指定", "She was designated team leader.", "她被指定為團隊領導。"),
            ("eligible", "adj.", "有資格的", "Are you eligible for the position?", "你有資格擔任這個職位嗎？"),
            ("grievance", "n.", "申訴", "File a grievance with HR.", "向人事部提出申訴。"),
            ("incentive", "n.", "獎勵", "Performance incentives motivate staff.", "績效獎勵激勵員工。"),
            ("layoff", "n.", "裁員", "The company announced layoffs.", "公司宣布裁員。"),
            ("maternity", "n.", "產假", "She is on maternity leave.", "她在休產假。"),
            ("overtime", "n.", "加班", "He works overtime frequently.", "他經常加班。"),
            ("pension", "n.", "退休金", "The pension plan is generous.", "退休金計畫很優厚。"),
            ("seniority", "n.", "年資", "Promotion is based on seniority.", "升遷根據年資。"),
            ("stipend", "n.", "津貼", "Interns receive a monthly stipend.", "實習生領月津貼。"),
            ("termination", "n.", "終止", "The termination was effective immediately.", "解僱立即生效。"),
            ("vacancy", "n.", "空缺", "There is a vacancy in marketing.", "行銷部門有一個空缺。"),
            ("waive", "v.", "放棄；免除", "The fee has been waived.", "費用已被免除。"),
        ],
        [
            ("accreditation", "n.", "認證", "The program received accreditation.", "該課程獲得認證。"),
            ("alumnus", "n.", "校友", "He is an alumnus of NTU.", "他是台大的校友。"),
            ("commencement", "n.", "畢業典禮", "Commencement is in June.", "畢業典禮在六月。"),
            ("dissertation", "n.", "論文", "She is writing her dissertation.", "她正在寫論文。"),
            ("elective", "n.", "選修課", "Choose two elective courses.", "選擇兩門選修課。"),
            ("fellowship", "n.", "獎學金；研究金", "He won a research fellowship.", "他獲得了研究獎學金。"),
            ("lectur", "n.", "講座", "Attend the guest lecture.", "參加客座講座。"),
            ("prerequisite", "n.", "先決條件", "Math is a prerequisite.", "數學是先決條件。"),
            ("scholarship", "n.", "獎學金", "She received a full scholarship.", "她獲得全額獎學金。"),
            ("semester", "n.", "學期", "The fall semester begins in September.", "秋季學期九月開始。"),
            ("syllabus", "n.", "課程大綱", "Review the syllabus carefully.", "仔細閱讀課程大綱。"),
            ("thesis", "n.", "論文", "His thesis was on AI.", "他的論文主題是AI。"),
            ("tuition", "n.", "學費", "Tuition has increased.", "學費漲了。"),
            ("undergraduate", "n./adj.", "大學生的", "She is an undergraduate student.", "她是大學生。"),
            ("vocational", "adj.", "職業的", "Attend a vocational school.", "就讀職業學校。"),
        ],
        [
            ("assess", "v.", "評估", "Assess the candidate's skills.", "評估候選人的技能。"),
            ("compensate", "v.", "補償", "They were compensated fairly.", "他們獲得公平的補償。"),
            ("delegate", "v.", "委派", "Delegate tasks effectively.", "有效地委派任務。"),
            ("empower", "v.", "授權", "Empower employees to decide.", "授權員工做決定。"),
            ("foster", "v.", "培養", "Foster a positive work environment.", "培養正面的工作環境。"),
            ("harassment", "n.", "騷擾", "Report any harassment immediately.", "立即舉報任何騷擾。"),
            ("initiative", "n.", "主動", "Take initiative in your work.", "在工作中展現主動性。"),
            ("jurisdiction", "n.", "管轄權", "This is under HR jurisdiction.", "這在人事部管轄範圍內。"),
            ("mandatory", "adj.", "強制的", "Attendance is mandatory.", "出席是強制的。"),
            ("novice", "n.", "新手", "Training is designed for novices.", "培訓專為新手設計。"),
            ("onboarding", "n.", "入職", "The onboarding process is smooth.", "入職流程很順利。"),
            ("proficiency", "n.", "熟練度", "Demonstrate English proficiency.", "展示英語熟練度。"),
            ("retention", "n.", "留才", "Employee retention is a priority.", "員工留才是優先事項。"),
            ("severance", "n.", "遣散費", "He received severance pay.", "他收到遣散費。"),
            ("turnover", "n.", "流動率", "High turnover is costly.", "高流動率代價很高。"),
        ],
        [
            ("allocate", "v.", "分配", "Allocate resources for training.", "分配培訓資源。"),
            ("benchmark", "n.", "基準", "Set salary benchmarks.", "設定薪資基準。"),
            ("compliance", "n.", "合規", "Ensure labor law compliance.", "確保遵守勞動法規。"),
            ("diversity", "n.", "多樣性", "Promote workplace diversity.", "推動職場多樣性。"),
            ("ethics", "n.", "道德規範", "Follow the code of ethics.", "遵守道德規範。"),
            ("freelance", "adj./v.", "自由接案的", "She works as a freelancer.", "她從事自由接案工作。"),
            ("hierarchical", "adj.", "階層式的", "The company has a hierarchical structure.", "公司有階層式結構。"),
            ("impartial", "adj.", "公正的", "HR must remain impartial.", "人事部必須保持公正。"),
            ("mediator", "n.", "調解人", "A mediator resolved the conflict.", "調解人解決了衝突。"),
            ("outsource", "v.", "外包", "The company outsources IT support.", "公司外包IT支援。"),
            ("protocol", "n.", "規程", "Follow the hiring protocol.", "遵循聘僱規程。"),
            ("sabbatical", "n.", "學術休假", "She took a one-year sabbatical.", "她休了一年的學術休假。"),
            ("subordinate", "n.", "部屬", "He manages five subordinates.", "他管理五位部屬。"),
            ("telecommute", "v.", "遠距工作", "She telecommutes twice a week.", "她每週遠距工作兩天。"),
            ("workforce", "n.", "勞動力", "The workforce is aging.", "勞動力正在老化。"),
        ],
    ]

    grammar = """## 介係詞 (Prepositions) — TOEIC 必考高頻考點

TOEIC Part 5 幾乎每次都考介係詞。需要記住固定搭配。

## 一、時間介係詞 in / on / at
at + 特定時間：at 3 p.m., at noon, at midnight, at the end of
on + 特定日期/星期：on Monday, on March 5, on weekends
in + 月份/年份/季節/較長時間：in March, in 2026, in the morning

EX: The meeting is at 2 p.m. on Friday.
EX: 會議在星期五下午兩點。

EX: She joined the company in January.
EX: 她在一月份加入公司。

注意：this, next, last, every 前面不加介係詞
正確：She will arrive next Monday. (不用 on next Monday)

## 二、地點介係詞 in / on / at
at + 特定地點/地址：at the office, at 100 Main Street
on + 街道/樓層/表面：on Oak Street, on the 3rd floor
in + 城市/國家/封閉空間：in Taipei, in Taiwan, in the room

EX: The conference will be held at the Grand Hotel.
EX: 會議將在圓山飯店舉行。

## 三、TOEIC 高頻介係詞搭配

by + 時間期限 = 在...之前
EX: Submit the report by Friday. (在星期五之前)

for + 一段時間 = 持續...
EX: He has worked here for 10 years. (工作了十年)

during + 期間 = 在...期間
EX: The office is closed during the holiday. (假日期間)

within + 時間範圍 = 在...之內
EX: Reply within 24 hours. (在24小時內回覆)

## 四、動詞 + 介係詞固定搭配
apply for (申請)
depend on (依賴)
consist of (由...組成)
result in (導致)
comply with (遵守)
participate in (參加)
agree with / on / to
  agree with + 人 (同意某人)
  agree on + 事 (就某事達成一致)
  agree to + 提議 (同意某提議)

EX: All employees must comply with the new regulations.
EX: 所有員工必須遵守新規定。

## 五、形容詞 + 介係詞固定搭配
responsible for (對...負責)
familiar with (熟悉)
interested in (對...感興趣)
capable of (有能力的)
eligible for (有資格的)
satisfied with (對...滿意)
aware of (意識到)
subject to (受...影響)

EX: She is responsible for training new employees.
EX: 她負責培訓新員工。"""

    part5 = [
        ("The training session will be held _______ March 15.", "in", "on", "at", "by"),
        ("The office is located _______ the third floor.", "in", "on", "at", "by"),
        ("Please submit the application _______ the end of this month.", "in", "on", "at", "by"),
        ("She has been working in HR _______ over five years.", "since", "for", "during", "while"),
        ("The workshop will take place _______ the conference center.", "in", "on", "at", "by"),
        ("All staff must comply _______ the new dress code.", "to", "for", "in", "with"),
        ("He is responsible _______ managing the department budget.", "of", "for", "to", "with"),
        ("The position is open to candidates who are familiar _______ Excel.", "to", "for", "in", "with"),
        ("Applications must be received _______ 48 hours.", "by", "within", "for", "during"),
        ("The company invested heavily _______ employee training.", "on", "for", "in", "at"),
        ("She was promoted _______ senior manager last month.", "for", "as", "to", "in"),
        ("The meeting is scheduled _______ 10:00 a.m.", "in", "on", "at", "by"),
        ("Employees who participate _______ the program will receive a bonus.", "at", "for", "in", "to"),
        ("The change will go into effect _______ January 1.", "in", "on", "at", "by"),
        ("He applied _______ the position of marketing director.", "to", "for", "in", "at"),
        ("We are satisfied _______ the results of the survey.", "to", "for", "in", "with"),
        ("The training course consists _______ ten modules.", "in", "for", "of", "with"),
        ("She is capable _______ handling multiple projects.", "in", "for", "of", "with"),
        ("The decision depends _______ the board's approval.", "in", "for", "on", "to"),
        ("All employees are subject _______ the company's policies.", "for", "in", "with", "to"),
    ]

    reading_title = "Notice: Employee Training Program"
    reading_pass = """GLOBALTECH CORPORATION
Human Resources Department

NOTICE: PROFESSIONAL DEVELOPMENT PROGRAM 2026

We are pleased to announce the launch of our updated Professional Development Program for all full-time employees. This program is designed to enhance skills, support career growth, and improve overall job performance.

Program Highlights:

1. Online Learning Platform
   All employees now have free access to SkillUp Online, which offers over 2,000 courses in business, technology, and leadership. To register, visit skillup.globaltech.com and use your employee ID.

2. Mentorship Program
   Senior employees are encouraged to volunteer as mentors. Each mentoring pair will meet at least twice a month for a minimum of six months. Interested employees should apply by March 31.

3. Tuition Reimbursement
   Full-time employees who have been with the company for at least one year are eligible for tuition reimbursement of up to $3,000 per year for approved courses related to their job responsibilities.

4. Quarterly Workshops
   Four workshops will be offered each quarter on topics including project management, communication skills, and data analysis. Registration is on a first-come, first-served basis.

To learn more about any of these programs, please contact the HR department at hr@globaltech.com or attend our information session on February 15 at 3:00 p.m. in Conference Room A.

Maria Santos
Director of Human Resources"""

    reading_qs = [
        ("Who is eligible for the Professional Development Program?", "Part-time employees", "All full-time employees", "Only managers", "New employees only"),
        ("How many courses does SkillUp Online offer?", "Over 200", "Over 1,000", "Over 2,000", "Over 5,000"),
        ("How often should mentoring pairs meet?", "Once a week", "At least twice a month", "Once a month", "Every day"),
        ("What is the maximum tuition reimbursement per year?", "$1,000", "$2,000", "$3,000", "$5,000"),
        ("When is the information session?", "February 15", "March 15", "March 31", "April 1"),
    ]

    p5_answers = [
        ("B", "March 15 是特定日期，用 on。"),
        ("B", "the third floor 用 on（在...樓層）。"),
        ("D", "by the end of = 在...結束之前。"),
        ("B", "over five years 是一段時間，用 for。"),
        ("C", "at the conference center，特定地點用 at。"),
        ("D", "comply with 是固定搭配，遵守。"),
        ("B", "responsible for 是固定搭配，對...負責。"),
        ("D", "familiar with 是固定搭配，熟悉。"),
        ("B", "within 48 hours = 在48小時之內。"),
        ("C", "invest in 是固定搭配，投資於。"),
        ("C", "be promoted to = 被升遷為。"),
        ("C", "10:00 a.m. 是特定時間，用 at。"),
        ("C", "participate in 是固定搭配，參加。"),
        ("B", "January 1 是特定日期，用 on。"),
        ("B", "apply for 是固定搭配，申請。"),
        ("D", "satisfied with 是固定搭配，對...滿意。"),
        ("C", "consist of 是固定搭配，由...組成。"),
        ("C", "capable of 是固定搭配，有能力。"),
        ("C", "depend on 是固定搭配，依賴。"),
        ("D", "subject to 是固定搭配，受...影響。"),
    ]

    rd_answers = [
        ("B", "文中提到 for all full-time employees。"),
        ("C", "文中提到 which offers over 2,000 courses。"),
        ("B", "文中提到 Each mentoring pair will meet at least twice a month。"),
        ("C", "文中提到 tuition reimbursement of up to $3,000 per year。"),
        ("A", "文中提到 attend our information session on February 15。"),
    ]

    build_week(7, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week08():
    title = "Marketing/Advertising Vocabulary + Adverb Connectors"
    vocab_days = [
        [
            ("advertise", "v.", "廣告", "We advertise on social media.", "我們在社群媒體上打廣告。"),
            ("brand", "n.", "品牌", "Build a strong brand image.", "建立強大的品牌形象。"),
            ("campaign", "n.", "活動", "The marketing campaign was successful.", "行銷活動很成功。"),
            ("demographics", "n.", "人口統計", "Study the target demographics.", "研究目標人口統計。"),
            ("endorse", "v.", "代言", "A celebrity endorsed the product.", "名人為產品代言。"),
            ("flyer", "n.", "傳單", "Distribute flyers in the mall.", "在商場發傳單。"),
            ("generate", "v.", "產生", "Generate more leads.", "產生更多潛在客戶。"),
            ("headline", "n.", "標題", "Write a catchy headline.", "寫一個吸引人的標題。"),
            ("incentive", "n.", "獎勵措施", "Offer incentives to customers.", "提供顧客獎勵措施。"),
            ("jingle", "n.", "廣告歌", "The jingle is very catchy.", "廣告歌很洗腦。"),
            ("launch", "v./n.", "推出", "We will launch the product in May.", "我們將在五月推出產品。"),
            ("market share", "n.", "市佔率", "Increase our market share.", "提高我們的市佔率。"),
            ("niche", "n.", "利基市場", "Target a niche market.", "瞄準利基市場。"),
            ("outreach", "n.", "推廣", "Expand customer outreach.", "擴大客戶推廣。"),
            ("promotion", "n.", "促銷；升遷", "A buy-one-get-one promotion.", "買一送一促銷。"),
        ],
        [
            ("analytics", "n.", "分析", "Use data analytics for insights.", "使用數據分析獲得洞見。"),
            ("billboard", "n.", "看板", "Rent a billboard on the highway.", "在高速公路租看板。"),
            ("conversion", "n.", "轉換", "Improve the conversion rate.", "提高轉換率。"),
            ("differentiate", "v.", "區別", "Differentiate from competitors.", "與競爭者區別。"),
            ("engagement", "n.", "互動", "Increase social media engagement.", "增加社群媒體互動。"),
            ("franchise", "n.", "加盟", "Open a franchise store.", "開一家加盟店。"),
            ("giveaway", "n.", "贈品活動", "Host a social media giveaway.", "舉辦社群贈品活動。"),
            ("influencer", "n.", "網紅", "Partner with an influencer.", "與網紅合作。"),
            ("keyword", "n.", "關鍵字", "Optimize for target keywords.", "針對目標關鍵字最佳化。"),
            ("loyalty", "n.", "忠誠度", "Build customer loyalty.", "建立客戶忠誠度。"),
            ("merchandise", "n.", "商品", "Branded merchandise is popular.", "品牌商品很受歡迎。"),
            ("newsletter", "n.", "電子報", "Subscribe to our newsletter.", "訂閱我們的電子報。"),
            ("positioning", "n.", "定位", "Brand positioning is key.", "品牌定位是關鍵。"),
            ("revenue", "n.", "營收", "Advertising revenue grew 20%.", "廣告營收成長20%。"),
            ("survey", "n.", "調查", "Conduct a customer survey.", "進行客戶調查。"),
        ],
        [
            ("acquisition", "n.", "獲取（客戶）", "Customer acquisition costs are high.", "客戶獲取成本很高。"),
            ("benchmark", "n.", "基準", "Set benchmarks for performance.", "設定績效基準。"),
            ("click-through", "n.", "點擊率", "The click-through rate improved.", "點擊率改善了。"),
            ("demographic", "adj.", "人口統計的", "Analyze demographic data.", "分析人口統計資料。"),
            ("exposure", "n.", "曝光", "Gain more media exposure.", "獲得更多媒體曝光。"),
            ("focus group", "n.", "焦點團體", "Organize a focus group.", "組織焦點團體。"),
            ("segment", "n./v.", "區隔", "Segment the market by age.", "依年齡區隔市場。"),
            ("slogan", "n.", "標語", "Create a memorable slogan.", "創造令人難忘的標語。"),
            ("sponsor", "v./n.", "贊助", "The company sponsored the event.", "公司贊助了活動。"),
            ("strategy", "n.", "策略", "Develop a new marketing strategy.", "制定新的行銷策略。"),
            ("target", "v./n.", "鎖定目標", "Target young consumers.", "鎖定年輕消費者。"),
            ("testimonial", "n.", "推薦書", "Customer testimonials boost sales.", "客戶推薦書促進銷售。"),
            ("trend", "n.", "趨勢", "Follow the latest trends.", "跟隨最新趨勢。"),
            ("viral", "adj.", "爆紅的", "The ad went viral.", "這則廣告爆紅了。"),
            ("wholesale", "n./adj.", "批發", "Sell at wholesale prices.", "以批發價銷售。"),
        ],
        [
            ("brochure", "n.", "手冊", "Design a product brochure.", "設計產品手冊。"),
            ("circulation", "n.", "發行量", "The magazine's circulation is high.", "雜誌發行量很大。"),
            ("clientele", "n.", "客戶群", "Attract a wealthy clientele.", "吸引富裕的客戶群。"),
            ("commission", "n.", "佣金", "Sales staff earn commission.", "銷售人員賺取佣金。"),
            ("consultant", "n.", "顧問", "Hire a marketing consultant.", "聘請行銷顧問。"),
            ("coupon", "n.", "折價券", "Distribute coupons online.", "在線上發放折價券。"),
            ("exclusive", "adj.", "獨家的", "An exclusive offer for members.", "會員獨家優惠。"),
            ("inventory", "n.", "庫存", "Clear excess inventory.", "清除多餘庫存。"),
            ("markup", "n.", "加價率", "The markup is 50%.", "加價率是50%。"),
            ("prospect", "n.", "潛在客戶", "Contact potential prospects.", "聯繫潛在客戶。"),
            ("rebate", "n.", "回扣", "Claim a mail-in rebate.", "申請郵寄回扣。"),
            ("retail", "n./adj.", "零售", "The retail price is $99.", "零售價是99美元。"),
            ("ROI", "n.", "投資報酬率", "Calculate the ROI.", "計算投資報酬率。"),
            ("trademark", "n.", "商標", "Register the trademark.", "註冊商標。"),
            ("venture", "n.", "企業；冒險", "A new business venture.", "新的商業冒險。"),
        ],
        [
            ("aggregate", "v./adj.", "匯總", "Aggregate the data.", "匯總數據。"),
            ("brand awareness", "n.", "品牌知名度", "Boost brand awareness.", "提升品牌知名度。"),
            ("compelling", "adj.", "令人信服的", "A compelling advertisement.", "一則令人信服的廣告。"),
            ("disrupt", "v.", "顛覆", "Disrupt the traditional market.", "顛覆傳統市場。"),
            ("flagship", "n./adj.", "旗艦", "Visit our flagship store.", "參觀我們的旗艦店。"),
            ("leverage", "v.", "善用", "Leverage social media.", "善用社群媒體。"),
            ("metrics", "n.", "指標", "Track marketing metrics.", "追蹤行銷指標。"),
            ("optimize", "v.", "最佳化", "Optimize the ad budget.", "最佳化廣告預算。"),
            ("penetration", "n.", "滲透率", "Market penetration is low.", "市場滲透率低。"),
            ("prototype", "n.", "原型", "Test the product prototype.", "測試產品原型。"),
            ("scalable", "adj.", "可擴展的", "A scalable business model.", "可擴展的商業模式。"),
            ("saturated", "adj.", "飽和的", "The market is saturated.", "市場已飽和。"),
            ("streamline", "v.", "精簡", "Streamline marketing operations.", "精簡行銷作業。"),
            ("synergy", "n.", "綜效", "Create synergy between teams.", "在團隊間創造綜效。"),
            ("visibility", "n.", "能見度", "Increase online visibility.", "增加線上能見度。"),
        ],
    ]

    grammar = """## 副詞連接詞 (Adverb Connectors / Transition Words) — TOEIC Part 5 & 6 高頻考點

副詞連接詞用來連接兩個句子，表達邏輯關係。注意：它們不是連接詞，不能直接連接兩個子句，需要用句號或分號分開。

## 一、表示「然而/但是」(Contrast)
however（然而）
nevertheless（儘管如此）
nonetheless（儘管如此）
on the other hand（另一方面）
instead（相反地）
conversely（相反地）

EX: The product is expensive. However, it is very popular.
EX: 產品很貴。然而，它非常受歡迎。

EX: Sales declined last quarter; nevertheless, the company remained profitable.
EX: 上季銷售下滑；儘管如此，公司仍然有獲利。

## 二、表示「因此/所以」(Result)
therefore（因此）
consequently（結果）
as a result（結果）
accordingly（因此）
thus（因此）
hence（因此）

EX: The budget was cut. Therefore, several projects were canceled.
EX: 預算被削減了。因此，幾個專案被取消了。

## 三、表示「此外/而且」(Addition)
moreover（此外）
furthermore（此外）
in addition（此外）
additionally（此外）
also（也）
besides（此外）

EX: The hotel has a pool. Moreover, it offers free breakfast.
EX: 飯店有游泳池。此外，它提供免費早餐。

## 四、表示「例如」(Example)
for example（例如）
for instance（例如）
specifically（具體來說）
in particular（特別是）

EX: The company has many benefits. For example, employees receive free meals.
EX: 公司有很多福利。例如，員工可以免費用餐。

## 五、TOEIC 考題陷阱：連接詞 vs. 副詞連接詞

連接詞 (Conjunction)：連接兩個子句
although, because, while, if, when

副詞連接詞 (Adverb Connector)：連接兩個句子
however, therefore, moreover, nevertheless

重要區別：
正確：Although sales declined, profits increased. (用逗號連接)
正確：Sales declined. However, profits increased. (用句號分開)
錯誤：Sales declined, however profits increased. (不能用逗號)

EX: 題目出現兩個完整子句且中間有逗號：選 although (連接詞)
EX: 題目出現兩個句子且中間有句號或分號：選 however (副詞連接詞)

## 六、記憶口訣
意思相近但用法不同的配對：
although（連接詞）= however（副詞連接詞）= despite（介係詞）
because（連接詞）= therefore（副詞連接詞）= because of（介係詞）
and（連接詞）= moreover（副詞連接詞）= in addition to（介係詞）"""

    part5 = [
        ("Sales have increased significantly. _______, the company plans to expand.", "Although", "Despite", "Therefore", "However"),
        ("The product is affordable; _______, it is also very durable.", "moreover", "however", "therefore", "instead"),
        ("_______ the high demand, we were unable to fulfill all orders.", "Therefore", "However", "Despite", "Moreover"),
        ("The report contained several errors. _______, it had to be revised.", "Moreover", "However", "Consequently", "Nevertheless"),
        ("_______ the weather was terrible, the outdoor event was not canceled.", "Therefore", "Although", "However", "Moreover"),
        ("We have reduced costs. _______, profits have improved.", "Nevertheless", "Although", "Despite", "As a result"),
        ("The new product received positive reviews; _______, sales have been disappointing.", "therefore", "moreover", "however", "consequently"),
        ("She is an excellent manager. _______, she has strong leadership skills.", "However", "Nevertheless", "Furthermore", "Instead"),
        ("_______ the marketing campaign was expensive, it failed to increase sales.", "Moreover", "Although", "Therefore", "Additionally"),
        ("The deadline was extended; _______, the team had more time to prepare.", "however", "nevertheless", "therefore", "moreover"),
        ("The restaurant is popular for its food. _______, it is known for excellent service.", "However", "Nevertheless", "In addition", "Instead"),
        ("He was offered a promotion; _______, he decided to resign.", "therefore", "moreover", "additionally", "however"),
        ("_______ implementing the new system, we need to train all staff.", "However", "Therefore", "Before", "Moreover"),
        ("The old model is no longer available. _______, we recommend the newer version.", "Although", "Despite", "However", "Instead"),
        ("Profits declined last quarter. _______, the company increased its advertising budget.", "Nevertheless", "Therefore", "Moreover", "Consequently"),
        ("The hotel is conveniently located; _______, it offers competitive rates.", "however", "instead", "furthermore", "therefore"),
        ("_______ the economic downturn, the company managed to grow.", "Although", "Despite", "Therefore", "Moreover"),
        ("The meeting was canceled. _______, all participants were notified by email.", "However", "Accordingly", "Moreover", "Nevertheless"),
        ("She has extensive experience. _______, she holds an MBA degree.", "However", "Instead", "Additionally", "Nevertheless"),
        ("The proposal was well-written; _______, it was rejected by the committee.", "therefore", "moreover", "consequently", "nevertheless"),
    ]

    reading_title = "Article: New Marketing Strategy Announcement"
    reading_pass = """BRIGHTSTAR ELECTRONICS ANNOUNCES NEW MARKETING STRATEGY

Brightstar Electronics, one of the leading consumer electronics companies in Asia, announced a major shift in its marketing strategy during its annual shareholder meeting on Tuesday.

CEO Lisa Huang revealed that the company will significantly reduce its spending on traditional advertising channels, such as television and print media, and redirect those funds toward digital marketing. "Our research shows that 75% of our target customers are between the ages of 18 and 35, and they spend an average of four hours per day on social media platforms," Huang explained.

The new strategy includes:
- Partnering with popular social media influencers to promote products
- Launching an interactive mobile app that offers virtual product demonstrations
- Creating a customer loyalty program with exclusive online discounts
- Investing $5 million in video content production for platforms like YouTube and Instagram

The company expects these changes to reduce marketing costs by approximately 30% while reaching a broader audience. Marketing Director James Park noted that early trials of the influencer partnership program showed a 45% increase in brand engagement among younger consumers.

Industry analysts have responded positively to the announcement. "Brightstar is making a smart move by adapting to changing consumer habits," said market analyst David Chen. "Companies that fail to embrace digital marketing risk falling behind their competitors."

The new strategy will be fully implemented by the third quarter of this year."""

    reading_qs = [
        ("What change is Brightstar making to its marketing strategy?", "Increasing TV advertising", "Shifting from traditional to digital marketing", "Reducing all marketing spending", "Focusing only on print media"),
        ("Why is Brightstar targeting social media platforms?", "They are cheaper than TV", "Most target customers spend time on them", "The CEO prefers social media", "Competitors do not use social media"),
        ("How much will Brightstar invest in video content?", "$3 million", "$5 million", "$10 million", "$30 million"),
        ("What result did early trials of the influencer program show?", "A 30% cost reduction", "A 45% increase in brand engagement", "A 75% increase in sales", "No significant change"),
        ("When will the new strategy be fully implemented?", "By the first quarter", "By the second quarter", "By the third quarter", "By the end of the year"),
    ]

    p5_answers = [
        ("C", "銷售增加，所以公司計畫擴展。兩句之間是因果關係，用 Therefore。"),
        ("A", "前句說產品實惠，後句補充說耐用。語意是「此外」，用 moreover。"),
        ("C", "空格後是名詞片語 the high demand，用介係詞 Despite。"),
        ("C", "報告有錯誤，結果必須修改。因果關係用 Consequently。"),
        ("B", "空格後有兩個子句用逗號連接，需要連接詞。天氣糟糕但活動沒取消，用 Although。"),
        ("D", "成本降低，結果利潤改善。因果關係用 As a result。"),
        ("C", "好評但銷售令人失望，語意相反。分號後用副詞連接詞 however。"),
        ("C", "優秀的經理，此外還有領導力。補充關係用 Furthermore。"),
        ("B", "空格後有兩個子句用逗號連接，需要連接詞。花很多錢但沒效果，用 Although。"),
        ("C", "延長截止日期，所以有更多時間。因果關係用 therefore。"),
        ("C", "食物受歡迎，此外服務也好。補充關係用 In addition。"),
        ("D", "被提供升遷但決定辭職。語意相反用 however。"),
        ("C", "在實施新系統之前需要培訓。Before 是介係詞/連接詞。"),
        ("D", "舊型號不可用，我們推薦新版本。用 Instead（反而/取而代之）。"),
        ("A", "利潤下降，然而公司增加廣告預算。語意相反用 Nevertheless。"),
        ("C", "位置方便，此外價格有競爭力。補充關係用 furthermore。"),
        ("B", "空格後是名詞片語 the economic downturn，用介係詞 Despite。"),
        ("B", "會議取消，因此通知了所有參與者。因果關係用 Accordingly。"),
        ("C", "有豐富經驗，此外還有MBA。補充關係用 Additionally。"),
        ("D", "提案寫得好但被拒絕。語意相反用 nevertheless。"),
    ]

    rd_answers = [
        ("B", "文中提到公司將 reduce spending on traditional advertising 並轉向 digital marketing。"),
        ("B", "文中提到 75% of target customers 在社群媒體上花大量時間。"),
        ("B", "文中提到 Investing $5 million in video content production。"),
        ("B", "文中提到 a 45% increase in brand engagement among younger consumers。"),
        ("C", "文中提到 The new strategy will be fully implemented by the third quarter。"),
    ]

    build_week(8, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week09():
    title = "Healthcare/Environment Vocabulary + Participles"
    vocab_days = [
        [
            ("ailment", "n.", "小病", "Treat common ailments quickly.", "迅速治療常見小病。"),
            ("diagnosis", "n.", "診斷", "The doctor made a diagnosis.", "醫生做了診斷。"),
            ("prescription", "n.", "處方", "Pick up the prescription at the pharmacy.", "在藥局領處方。"),
            ("symptom", "n.", "症狀", "What are your symptoms?", "你的症狀是什麼？"),
            ("therapy", "n.", "治療", "Physical therapy helps recovery.", "物理治療有助恢復。"),
            ("dosage", "n.", "劑量", "Follow the recommended dosage.", "遵循建議劑量。"),
            ("clinic", "n.", "診所", "Visit the clinic for a checkup.", "到診所做檢查。"),
            ("insurance", "n.", "保險", "Do you have health insurance?", "你有健康保險嗎？"),
            ("patient", "n.", "病人", "The patient is recovering well.", "病人恢復得很好。"),
            ("physician", "n.", "內科醫師", "Consult a physician.", "諮詢內科醫師。"),
            ("supplement", "n.", "補充品", "Take vitamin supplements.", "服用維生素補充品。"),
            ("outbreak", "n.", "爆發", "An outbreak of the flu was reported.", "報導了流感爆發。"),
            ("vaccine", "n.", "疫苗", "Get the vaccine annually.", "每年接種疫苗。"),
            ("hygiene", "n.", "衛生", "Maintain good hygiene.", "維持良好衛生。"),
            ("wellness", "n.", "健康", "Promote employee wellness.", "促進員工健康。"),
        ],
        [
            ("conservation", "n.", "保育", "Wildlife conservation is important.", "野生動物保育很重要。"),
            ("emission", "n.", "排放", "Reduce greenhouse gas emissions.", "減少溫室氣體排放。"),
            ("renewable", "adj.", "再生的", "Use renewable energy sources.", "使用再生能源。"),
            ("sustainable", "adj.", "永續的", "Adopt sustainable practices.", "採用永續作法。"),
            ("pollution", "n.", "污染", "Air pollution is a concern.", "空氣污染令人擔憂。"),
            ("biodegradable", "adj.", "可生物分解的", "Use biodegradable packaging.", "使用可生物分解的包裝。"),
            ("carbon", "n.", "碳", "Reduce your carbon footprint.", "減少你的碳足跡。"),
            ("deforestation", "n.", "森林砍伐", "Stop deforestation immediately.", "立即停止森林砍伐。"),
            ("ecosystem", "n.", "生態系統", "Protect the marine ecosystem.", "保護海洋生態系統。"),
            ("fossil fuel", "n.", "化石燃料", "Reduce dependence on fossil fuels.", "減少對化石燃料的依賴。"),
            ("habitat", "n.", "棲息地", "Protect natural habitats.", "保護自然棲息地。"),
            ("recycle", "v.", "回收", "Recycle paper and plastic.", "回收紙張和塑膠。"),
            ("toxic", "adj.", "有毒的", "Dispose of toxic waste properly.", "正確處理有毒廢物。"),
            ("drought", "n.", "乾旱", "The drought affected crops.", "乾旱影響了農作物。"),
            ("erosion", "n.", "侵蝕", "Soil erosion is a problem.", "土壤侵蝕是個問題。"),
        ],
        [
            ("allergen", "n.", "過敏原", "Check for common allergens.", "檢查常見過敏原。"),
            ("chronic", "adj.", "慢性的", "She has a chronic condition.", "她有慢性疾病。"),
            ("contagious", "adj.", "傳染的", "The disease is highly contagious.", "這種疾病高度傳染。"),
            ("epidemic", "n.", "流行病", "An epidemic spread quickly.", "流行病迅速蔓延。"),
            ("immunity", "n.", "免疫力", "Build up your immunity.", "增強你的免疫力。"),
            ("nutrient", "n.", "營養素", "Get essential nutrients from food.", "從食物中獲取必要營養素。"),
            ("organic", "adj.", "有機的", "Buy organic produce.", "購買有機農產品。"),
            ("pharmaceutical", "adj./n.", "製藥的", "The pharmaceutical industry is growing.", "製藥業正在成長。"),
            ("rehabilitation", "n.", "復健", "He is in rehabilitation.", "他正在復健。"),
            ("sanitation", "n.", "公共衛生", "Improve sanitation in the area.", "改善該地區的公共衛生。"),
            ("sedentary", "adj.", "久坐的", "Avoid a sedentary lifestyle.", "避免久坐的生活方式。"),
            ("sterilize", "v.", "消毒", "Sterilize all equipment.", "消毒所有設備。"),
            ("quarantine", "n./v.", "隔離", "The patient was quarantined.", "病人被隔離了。"),
            ("contaminate", "v.", "污染", "The water was contaminated.", "水被污染了。"),
            ("hazardous", "adj.", "危險的", "Wear protection for hazardous materials.", "處理危險物質要穿防護裝備。"),
        ],
        [
            ("biodiversity", "n.", "生物多樣性", "Preserve biodiversity.", "保存生物多樣性。"),
            ("compost", "n./v.", "堆肥", "Compost food waste.", "將廚餘堆肥。"),
            ("depleted", "adj.", "耗盡的", "Natural resources are depleted.", "自然資源被耗盡了。"),
            ("endangered", "adj.", "瀕危的", "Protect endangered species.", "保護瀕危物種。"),
            ("greenhouse", "n.", "溫室", "The greenhouse effect is real.", "溫室效應是真實的。"),
            ("landfill", "n.", "掩埋場", "Reduce waste going to landfills.", "減少送到掩埋場的廢物。"),
            ("ozone", "n.", "臭氧", "The ozone layer is thinning.", "臭氧層正在變薄。"),
            ("pesticide", "n.", "農藥", "Reduce pesticide use.", "減少農藥使用。"),
            ("reforestation", "n.", "造林", "Support reforestation projects.", "支持造林計畫。"),
            ("solar", "adj.", "太陽的", "Install solar panels.", "安裝太陽能板。"),
            ("vegetation", "n.", "植被", "Protect local vegetation.", "保護當地植被。"),
            ("watershed", "n.", "分水嶺；流域", "Protect the watershed area.", "保護流域地區。"),
            ("wind turbine", "n.", "風力渦輪", "Build more wind turbines.", "建造更多風力渦輪。"),
            ("zero-waste", "adj.", "零廢棄的", "Aim for zero-waste production.", "目標零廢棄生產。"),
            ("ecological", "adj.", "生態的", "Conduct an ecological study.", "進行生態研究。"),
        ],
        [
            ("ambulance", "n.", "救護車", "Call an ambulance immediately.", "立刻叫救護車。"),
            ("clinical", "adj.", "臨床的", "A clinical trial was conducted.", "進行了臨床試驗。"),
            ("deficiency", "n.", "缺乏", "Iron deficiency is common.", "缺鐵很常見。"),
            ("epidemic", "n.", "流行病", "Combat the obesity epidemic.", "對抗肥胖流行病。"),
            ("genetic", "adj.", "基因的", "Genetic research is advancing.", "基因研究正在進步。"),
            ("holistic", "adj.", "全面的", "A holistic approach to health.", "全面的健康方法。"),
            ("incurable", "adj.", "無法治癒的", "Some diseases are incurable.", "有些疾病無法治癒。"),
            ("malpractice", "n.", "醫療過失", "A malpractice lawsuit was filed.", "提起了醫療過失訴訟。"),
            ("outpatient", "n./adj.", "門診的", "An outpatient procedure.", "門診手術。"),
            ("pathogen", "n.", "病原體", "Identify the pathogen.", "辨識病原體。"),
            ("prognosis", "n.", "預後", "The prognosis is good.", "預後良好。"),
            ("remedy", "n.", "療法", "A natural remedy for colds.", "感冒的自然療法。"),
            ("side effect", "n.", "副作用", "Watch for side effects.", "注意副作用。"),
            ("transplant", "n./v.", "移植", "A heart transplant was performed.", "進行了心臟移植。"),
            ("vulnerable", "adj.", "脆弱的", "Elderly people are more vulnerable.", "老年人更脆弱。"),
        ],
    ]

    grammar = """## 分詞 (Participles) — TOEIC Part 5 高頻考點

分詞有兩種：現在分詞 (V-ing) 和過去分詞 (V-ed/p.p.)，可當形容詞使用。

## 一、現在分詞 vs. 過去分詞作形容詞

現在分詞 (-ing)：表示「令人...的」，描述事物的特性
過去分詞 (-ed)：表示「感到...的」，描述人的感受

EX: The movie was boring. (電影很無聊 — 描述電影的特性)
EX: I was bored during the movie. (看電影時我很無聊 — 描述人的感受)

EX: The news is surprising. (這消息令人驚訝)
EX: We were surprised by the news. (我們對這消息感到驚訝)

## 二、常考的分詞形容詞配對
interesting / interested (有趣的 / 感興趣的)
exciting / excited (令人興奮的 / 感到興奮的)
confusing / confused (令人困惑的 / 感到困惑的)
disappointing / disappointed (令人失望的 / 感到失望的)
satisfying / satisfied (令人滿意的 / 感到滿意的)
exhausting / exhausted (令人疲憊的 / 感到疲憊的)
motivating / motivated (激勵人的 / 受到激勵的)
overwhelming / overwhelmed (壓倒性的 / 感到不堪負荷的)

EX: The training was very motivating. (訓練很激勵人)
EX: The employees felt motivated after the training. (員工在訓練後感到受激勵)

## 三、分詞片語（簡化形容詞子句）
現在分詞片語：主動意義
過去分詞片語：被動意義

EX: The man standing by the door is the manager.
EX: = The man who is standing by the door is the manager.
EX: 站在門邊的那個人是經理。

EX: The report written by Ms. Chen was very detailed.
EX: = The report which was written by Ms. Chen was very detailed.
EX: 由陳小姐撰寫的報告非常詳細。

## 四、分詞構句
用分詞片語開頭，簡化副詞子句。

主動：V-ing ..., 主詞 + 動詞
被動：V-ed/p.p. ..., 主詞 + 動詞

EX: Having completed the project, the team celebrated.
EX: 完成專案後，團隊慶祝了。

EX: Located in the city center, the hotel attracts many tourists.
EX: 位於市中心，這家飯店吸引了很多觀光客。

## 五、TOEIC 判斷技巧
1. 描述「人的感受」→ 用 -ed (I am interested)
2. 描述「事物的特性」→ 用 -ing (The book is interesting)
3. 名詞前面修飾 → 判斷主動（-ing）或被動（-ed）
   a growing company (成長中的公司 — 主動)
   a used car (二手車 — 被動)"""

    part5 = [
        ("The customers were _______ with the quality of the service.", "satisfying", "satisfied", "satisfy", "satisfaction"),
        ("The conference was very _______; everyone learned a lot.", "informing", "informed", "informative", "information"),
        ("The _______ results of the study were published last week.", "surprising", "surprised", "surprise", "surprisingly"),
        ("All employees _______ in the program will receive a certificate.", "participating", "participated", "participate", "participation"),
        ("The document _______ by the legal team needs your signature.", "reviewing", "reviewed", "review", "reviews"),
        ("The manager was _______ by the team's poor performance.", "disappointing", "disappointed", "disappoint", "disappointment"),
        ("_______ in 1990, the company has grown significantly.", "Founding", "Founded", "Found", "Foundation"),
        ("The _______ demand for eco-friendly products has increased sales.", "growing", "grown", "grew", "growth"),
        ("Patients _______ for allergies should avoid certain foods.", "treating", "treated", "treat", "treatment"),
        ("The new policy has been very _______ for employees.", "confusing", "confused", "confuse", "confusion"),
        ("_______ near the hospital, the clinic is easy to find.", "Locating", "Located", "Locate", "Location"),
        ("She felt _______ after working 12 hours straight.", "exhausting", "exhausted", "exhaust", "exhaustion"),
        ("The _______ report contained valuable information.", "detailing", "detailed", "detail", "details"),
        ("The audience was deeply _______ by the speaker's presentation.", "moving", "moved", "move", "movement"),
        ("Products _______ in our factory meet international standards.", "manufacturing", "manufactured", "manufacture", "manufacturer"),
        ("The rising pollution levels are _______ to residents.", "concerning", "concerned", "concern", "concerns"),
        ("_______ the potential risks, the company decided to proceed.", "Recognizing", "Recognized", "Recognize", "Recognition"),
        ("The _______ workers were given additional safety training.", "injuring", "injured", "injure", "injury"),
        ("We need a _______ plan for waste management.", "comprehending", "comprehended", "comprehensive", "comprehension"),
        ("_______ with state-of-the-art technology, the lab is impressive.", "Equipping", "Equipped", "Equip", "Equipment"),
    ]

    reading_title = "Notice: Community Health Fair"
    reading_pass = """GREENVILLE COMMUNITY HEALTH FAIR

Date: Saturday, April 19, 2026
Time: 9:00 a.m. - 4:00 p.m.
Location: Greenville Community Center, 500 Park Avenue

The Greenville Department of Health is pleased to announce the 15th Annual Community Health Fair. This free event is open to all residents and offers a wide range of health services and educational resources.

SERVICES OFFERED:
- Free blood pressure and cholesterol screenings
- Blood sugar testing for diabetes risk assessment
- Vision and hearing tests
- Flu vaccinations (for adults 18 and over; limited supply)
- Free dental checkups provided by Greenville Dental Clinic

HEALTH EDUCATION BOOTHS:
- Nutrition and healthy eating habits
- Mental health awareness and stress management
- Exercise programs for all ages
- Environmental health: How air quality affects your well-being
- Smoking cessation resources

SPECIAL EVENTS:
- 10:00 a.m.: Opening remarks by Mayor Davis
- 11:00 a.m.: Cooking demonstration featuring healthy recipes
- 1:00 p.m.: Panel discussion on healthcare access in rural communities
- 3:00 p.m.: Yoga and meditation session (bring your own mat)

Free parking is available in the community center parking lot. Public transportation: Take Bus Route 15 to Park Avenue stop.

For more information, call (555) 234-5678 or visit www.greenvillehealth.gov.

Pre-registration is not required, but recommended to ensure access to all services."""

    reading_qs = [
        ("What is the admission fee for the health fair?", "$5", "$10", "It is free", "$15"),
        ("Who can receive flu vaccinations at the event?", "Children only", "Adults 18 and over", "Senior citizens only", "All ages"),
        ("What is happening at 1:00 p.m.?", "A cooking demonstration", "Opening remarks", "A panel discussion on healthcare access", "A yoga session"),
        ("What should participants bring for the yoga session?", "Water bottles", "Exercise clothes", "Their own mat", "A towel"),
        ("Is pre-registration required?", "Yes, it is mandatory", "Yes, and there is a fee", "No, but it is recommended", "No information is given"),
    ]

    p5_answers = [
        ("B", "customers 是「人」，感到滿意用過去分詞 satisfied。"),
        ("C", "注意 informative 才是「資訊豐富的」的正確形容詞。informing 是「通知的」。"),
        ("A", "results 是「物」，令人驚訝用現在分詞 surprising。"),
        ("A", "employees 主動參加，用現在分詞 participating 作分詞片語。"),
        ("B", "document 被審閱，用過去分詞 reviewed 作分詞片語。"),
        ("B", "manager 是「人」，感到失望用過去分詞 disappointed。"),
        ("B", "company 被創立，用過去分詞 Founded 開頭的分詞構句。"),
        ("A", "demand 主動增長，用現在分詞 growing。"),
        ("B", "Patients 被治療，用過去分詞 treated。"),
        ("A", "policy 是「物」，令人困惑用現在分詞 confusing。"),
        ("B", "clinic 被位於某處，用過去分詞 Located。"),
        ("B", "She 是「人」，感到疲憊用過去分詞 exhausted。"),
        ("B", "report 是詳細的，detailed 是形容詞。"),
        ("B", "audience 是「人」，被感動用過去分詞 moved。"),
        ("B", "Products 被製造，用過去分詞 manufactured。"),
        ("A", "pollution levels 是「物」，令人擔憂用現在分詞 concerning。"),
        ("A", "company 主動認識到風險，用現在分詞 Recognizing 開頭的分詞構句。"),
        ("B", "workers 被受傷（受傷的），用過去分詞 injured。"),
        ("C", "comprehensive 是「全面的」形容詞，注意這不是典型的分詞但是常見的詞性題。"),
        ("B", "lab 被配備技術，用過去分詞 Equipped。"),
    ]

    rd_answers = [
        ("C", "文中提到 This free event is open to all residents。"),
        ("B", "文中提到 Flu vaccinations (for adults 18 and over)。"),
        ("C", "1:00 p.m. 是 Panel discussion on healthcare access in rural communities。"),
        ("C", "文中提到 bring your own mat。"),
        ("C", "文中提到 Pre-registration is not required, but recommended。"),
    ]

    build_week(9, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week10():
    title = "Real Estate/Legal Vocabulary + Conditionals"
    vocab_days = [
        [
            ("lease", "n./v.", "租約", "Sign a one-year lease.", "簽一年租約。"),
            ("tenant", "n.", "房客", "The tenant pays rent monthly.", "房客每月付房租。"),
            ("landlord", "n.", "房東", "Contact the landlord for repairs.", "聯繫房東修繕。"),
            ("mortgage", "n.", "房貸", "Apply for a mortgage.", "申請房貸。"),
            ("property", "n.", "房產", "The property is for sale.", "這間房產出售中。"),
            ("real estate", "n.", "不動產", "She works in real estate.", "她從事不動產業。"),
            ("appraisal", "n.", "鑑價", "Get a property appraisal.", "進行房產鑑價。"),
            ("closing", "n.", "成交", "The closing date is May 1.", "成交日是五月一日。"),
            ("commission", "n.", "佣金", "The agent earns a commission.", "仲介賺取佣金。"),
            ("commercial", "adj.", "商業的", "Commercial property for rent.", "商業房產出租。"),
            ("deed", "n.", "契約", "Sign the property deed.", "簽署房產契約。"),
            ("deposit", "n.", "押金", "Pay a security deposit.", "支付保證金。"),
            ("evict", "v.", "驅逐", "The tenant was evicted.", "房客被驅逐了。"),
            ("inspect", "v.", "檢查", "Inspect the property before buying.", "購買前檢查房產。"),
            ("renovate", "v.", "翻修", "Renovate the kitchen.", "翻修廚房。"),
        ],
        [
            ("attorney", "n.", "律師", "Consult an attorney.", "諮詢律師。"),
            ("clause", "n.", "條款", "Read every clause carefully.", "仔細閱讀每一條款。"),
            ("contract", "n.", "合約", "Sign the employment contract.", "簽署雇用合約。"),
            ("defendant", "n.", "被告", "The defendant pleaded not guilty.", "被告辯稱無罪。"),
            ("dispute", "n./v.", "爭議", "Resolve the dispute quickly.", "迅速解決爭議。"),
            ("enforce", "v.", "執行", "Enforce the new regulation.", "執行新規定。"),
            ("file", "v.", "提出（訴訟）", "File a lawsuit.", "提起訴訟。"),
            ("jurisdiction", "n.", "管轄權", "This is under federal jurisdiction.", "這屬於聯邦管轄。"),
            ("lawsuit", "n.", "訴訟", "A lawsuit was filed.", "訴訟已提起。"),
            ("legislation", "n.", "法律；立法", "New legislation was passed.", "新法律通過了。"),
            ("liability", "n.", "責任", "The company denied liability.", "公司否認責任。"),
            ("mediate", "v.", "調解", "A lawyer mediated the dispute.", "律師調解了爭議。"),
            ("patent", "n.", "專利", "Apply for a patent.", "申請專利。"),
            ("plaintiff", "n.", "原告", "The plaintiff won the case.", "原告勝訴了。"),
            ("verdict", "n.", "判決", "The verdict was unanimous.", "判決是一致的。"),
        ],
        [
            ("acreage", "n.", "英畝數", "The property has 10 acres.", "這房產有10英畝。"),
            ("amenity", "n.", "便利設施", "The apartment has many amenities.", "公寓有很多便利設施。"),
            ("assessment", "n.", "評估", "A tax assessment was conducted.", "進行了稅務評估。"),
            ("condominium", "n.", "公寓大廈", "She bought a condominium.", "她買了一間公寓。"),
            ("demolish", "v.", "拆除", "The old building was demolished.", "舊建築被拆除了。"),
            ("equity", "n.", "淨值", "Build equity in your home.", "增加你的房屋淨值。"),
            ("foreclosure", "n.", "法拍", "The house went into foreclosure.", "房子進入法拍程序。"),
            ("inhabit", "v.", "居住", "200 people inhabit the building.", "200人居住在這棟大樓。"),
            ("occupant", "n.", "住戶", "All occupants must evacuate.", "所有住戶必須撤離。"),
            ("permit", "n.", "許可證", "Obtain a building permit.", "取得建築許可證。"),
            ("residential", "adj.", "住宅的", "This is a residential area.", "這是住宅區。"),
            ("subdivision", "n.", "分區", "A new housing subdivision.", "新的住宅分區。"),
            ("utilities", "n.", "水電", "Utilities are included in the rent.", "房租含水電。"),
            ("zoning", "n.", "分區規劃", "Check the zoning regulations.", "檢查分區規劃法規。"),
            ("vacancy", "n.", "空屋", "The vacancy rate is low.", "空屋率很低。"),
        ],
        [
            ("arbitration", "n.", "仲裁", "Settle through arbitration.", "通過仲裁解決。"),
            ("breach", "n./v.", "違反", "A breach of contract occurred.", "發生了違約。"),
            ("compliance", "n.", "合規", "Ensure regulatory compliance.", "確保法規合規。"),
            ("confidentiality", "n.", "保密性", "Maintain confidentiality.", "維持保密性。"),
            ("copyright", "n.", "著作權", "Protect your copyright.", "保護你的著作權。"),
            ("deposition", "n.", "證詞", "Give a deposition.", "進行作證。"),
            ("indemnity", "n.", "賠償", "An indemnity clause is included.", "包含了賠償條款。"),
            ("injunction", "n.", "禁令", "The court issued an injunction.", "法院發出禁令。"),
            ("negligence", "n.", "過失", "Sued for negligence.", "因過失被起訴。"),
            ("notarize", "v.", "公證", "Notarize the document.", "公證文件。"),
            ("ordinance", "n.", "法令", "A new city ordinance.", "新的市政法令。"),
            ("precedent", "n.", "先例", "This case sets a precedent.", "此案開了先例。"),
            ("statute", "n.", "法規", "According to the statute.", "根據法規。"),
            ("testimony", "n.", "證詞", "The witness gave testimony.", "證人提供了證詞。"),
            ("waiver", "n.", "棄權書", "Sign a liability waiver.", "簽署免責棄權書。"),
        ],
        [
            ("acquisition", "n.", "收購；取得", "Property acquisition takes time.", "房產取得需要時間。"),
            ("adjacent", "adj.", "鄰近的", "The park is adjacent to the building.", "公園在大樓旁邊。"),
            ("blueprint", "n.", "藍圖", "Review the blueprint carefully.", "仔細審查藍圖。"),
            ("contractor", "n.", "承包商", "Hire a licensed contractor.", "聘請有執照的承包商。"),
            ("depreciation", "n.", "折舊", "Calculate property depreciation.", "計算房產折舊。"),
            ("easement", "n.", "地役權", "An easement grants access.", "地役權允許通行。"),
            ("escrow", "n.", "第三方保管", "Funds are held in escrow.", "資金由第三方保管。"),
            ("lien", "n.", "留置權", "A lien was placed on the property.", "房產被設置了留置權。"),
            ("probate", "n.", "遺囑認證", "The estate went through probate.", "遺產經過了遺囑認證。"),
            ("quitclaim", "n.", "放棄權利", "Sign a quitclaim deed.", "簽署放棄權利契約。"),
            ("sublease", "v./n.", "轉租", "Can I sublease the apartment?", "我可以轉租公寓嗎？"),
            ("title", "n.", "所有權", "Transfer the property title.", "轉移房產所有權。"),
            ("variance", "n.", "變異；特別許可", "Apply for a zoning variance.", "申請分區特別許可。"),
            ("stipulate", "v.", "規定", "The contract stipulates the terms.", "合約規定了條款。"),
            ("amend", "v.", "修訂", "Amend the contract.", "修訂合約。"),
        ],
    ]

    grammar = """## 條件句 (Conditionals) — TOEIC 重要文法

條件句用 if 引導條件子句，表示假設的情況。

## 一、零條件句 (Zero Conditional)
結構：If + 現在式, 現在式
用法：表示永遠為真的事實或規律

EX: If you heat water to 100 degrees, it boils.
EX: 如果你把水加熱到100度，水就會沸騰。

EX: If employees work overtime, they receive extra pay.
EX: 如果員工加班，他們會收到加班費。

## 二、第一條件句 (First Conditional)
結構：If + 現在式, will + 原形動詞
用法：表示未來可能發生的事情

EX: If the weather is nice, we will hold the event outdoors.
EX: 如果天氣好，我們將在戶外舉辦活動。

EX: If the company meets its target, employees will receive a bonus.
EX: 如果公司達到目標，員工將獲得獎金。

注意：if 子句用現在式（不用 will），主要子句用 will。

## 三、第二條件句 (Second Conditional)
結構：If + 過去式, would + 原形動詞
用法：表示現在不太可能發生的假設

EX: If I had more time, I would study abroad.
EX: 如果我有更多時間，我會出國留學。（但我沒有）

EX: If the company were larger, it would open overseas offices.
EX: 如果公司更大，就會開設海外辦公室。（但公司不夠大）

## 四、unless = if ... not（除非）
EX: Unless you submit the application by Friday, you will not be considered.
EX: = If you do not submit the application by Friday, you will not be considered.
EX: 除非你在星期五前提交申請，否則不會被考慮。

## 五、provided that / as long as / on condition that = if（只要...就）
EX: You may leave early provided that you finish your work.
EX: 只要你完成工作，你可以提早離開。

EX: The warranty is valid as long as you keep the receipt.
EX: 只要你保留收據，保固就有效。

## 六、TOEIC 常考重點
1. if 子句和主要子句的時態搭配
2. unless 的用法（= if not）
3. provided that / as long as 的用法
4. 注意 should 在條件句中的正式用法：
   Should you have any questions, please contact us.
   = If you have any questions, please contact us.
   如果您有任何問題，請與我們聯繫。"""

    part5 = [
        ("If the contract _______ signed by Friday, the deal will be finalized.", "is", "was", "will be", "would be"),
        ("_______ you need further assistance, please call our office.", "Unless", "Although", "Should", "Despite"),
        ("The warranty will remain valid as long as the product _______ properly maintained.", "is", "was", "will be", "would be"),
        ("_______ the tenant fails to pay rent, the landlord may begin eviction proceedings.", "Unless", "If", "Although", "Despite"),
        ("If we _______ a larger budget, we could renovate the entire building.", "have", "had", "will have", "having"),
        ("The lease will be renewed _______ both parties agree to the terms.", "unless", "despite", "provided that", "although"),
        ("Unless the property passes inspection, the sale _______ proceed.", "will", "will not", "would", "would not"),
        ("If the building _______ the safety standards, it will receive a permit.", "meet", "meets", "met", "meeting"),
        ("_______ the court rules in our favor, we will proceed with the project.", "Unless", "If", "Despite", "Although"),
        ("The agreement is binding on condition that all parties _______ the document.", "sign", "signed", "will sign", "signing"),
        ("If the interest rates _______ lower, more people would buy homes.", "are", "were", "will be", "have been"),
        ("The company will not be held liable _______ negligence can be proven.", "if", "unless", "as long as", "provided that"),
        ("_______ you submit the forms on time, your application will be processed.", "Unless", "Although", "Provided that", "Despite"),
        ("If the tenant _______ the lease, legal action may be taken.", "violate", "violates", "violated", "will violate"),
        ("We would settle the case _______ the other party agreed to mediation.", "if", "unless", "although", "despite"),
        ("The deal will go through _______ there are no legal objections.", "unless", "as long as", "although", "despite"),
        ("_______ the property were available, we would make an offer immediately.", "If", "Unless", "Although", "When"),
        ("Employees will be reimbursed _______ they submit valid receipts.", "unless", "although", "despite", "provided that"),
        ("If the regulation _______ changed, many businesses will be affected.", "is", "was", "will be", "would be"),
        ("The contract is void _______ both parties have agreed to the amendments.", "if", "unless", "although", "despite"),
    ]

    reading_title = "Notice: Apartment Lease Agreement Update"
    reading_pass = """SUNSHINE APARTMENTS
Lease Agreement Update Notice

Dear Residents,

We are writing to inform you of updates to the lease agreement for all units at Sunshine Apartments, effective July 1, 2026.

KEY CHANGES:

1. Rent Adjustment
Monthly rent for all units will increase by 3%. This adjustment reflects rising maintenance costs and property tax increases. Tenants who renew their lease for a two-year term will receive a 1% discount on the new rate.

2. Pet Policy
Starting July 1, pets will be allowed in designated units on floors 1-3 only. A pet deposit of $300 is required, and a monthly pet fee of $25 will be added to your rent. All pets must be registered with the management office.

3. Parking
Each unit is entitled to one free parking space. Additional parking spaces may be rented for $75 per month, subject to availability. All vehicles must display a valid parking permit.

4. Common Area Usage
The rooftop garden will now be open from 6:00 a.m. to 10:00 p.m. daily. Residents wishing to reserve the community room for private events must submit a request at least two weeks in advance.

Current tenants who wish to renew their lease under the new terms should contact the management office by June 15. If you have any questions, please call (02) 2345-6789 or email info@sunshineapts.com.

Thank you for being a valued resident.

Best regards,
Management Office
Sunshine Apartments"""

    reading_qs = [
        ("By how much will the monthly rent increase?", "1%", "2%", "3%", "5%"),
        ("How can tenants receive a discount on the new rent rate?", "By paying in advance", "By renewing for two years", "By referring a new tenant", "By signing up for auto-pay"),
        ("On which floors are pets allowed?", "All floors", "Floors 1-3", "Floors 4-10", "Only the ground floor"),
        ("How much does an additional parking space cost per month?", "$25", "$50", "$75", "$100"),
        ("By when should current tenants contact the management office to renew?", "May 1", "June 1", "June 15", "July 1"),
    ]

    p5_answers = [
        ("A", "If 條件句，主要子句用 will，if 子句用現在式 is。"),
        ("C", "Should you need = If you need，是正式的條件句倒裝。"),
        ("A", "as long as 子句用現在式 is。"),
        ("B", "如果房客沒付房租，房東可以開始驅逐程序。用 If。"),
        ("B", "第二條件句（假設），If + 過去式 had，主句用 could。"),
        ("C", "只要雙方同意，租約就會續約。provided that = if。"),
        ("B", "Unless = if not，除非通過檢查，否則不會進行，用 will not。"),
        ("B", "If 子句用現在式，building 是第三人稱，用 meets。"),
        ("B", "如果法院判我們勝訴，我們將進行專案。用 If。"),
        ("A", "on condition that 子句用現在式 sign。"),
        ("B", "第二條件句，If + 過去式 were（假設利率較低）。"),
        ("B", "除非能證明過失，否則公司不負責。unless = if not。"),
        ("C", "只要你按時提交，申請就會被處理。Provided that = If。"),
        ("B", "If 子句用現在式，tenant 是第三人稱，用 violates。"),
        ("A", "第二條件句，If + 過去式 agreed，主句用 would settle。"),
        ("B", "只要沒有法律異議，交易就會成交。as long as = if。"),
        ("A", "第二條件句的假設，If the property were available。"),
        ("D", "只要他們提交有效收據，就會報銷。provided that = if。"),
        ("A", "If 子句用現在式 is（第一條件句，未來可能發生）。"),
        ("B", "除非雙方同意修改，否則合約無效。unless = if not。"),
    ]

    rd_answers = [
        ("C", "文中提到 Monthly rent for all units will increase by 3%。"),
        ("B", "文中提到 Tenants who renew their lease for a two-year term will receive a 1% discount。"),
        ("B", "文中提到 pets will be allowed in designated units on floors 1-3 only。"),
        ("C", "文中提到 Additional parking spaces may be rented for $75 per month。"),
        ("C", "文中提到 should contact the management office by June 15。"),
    ]

    build_week(10, title, vocab_days, grammar, part5, reading_title, reading_pass, reading_qs, p5_answers, rd_answers)


def week11():
    title = "Part 5+6 Intensive Drill (Mixed Grammar)"

    pdf = ToeicPDF(11, title)
    pdf.cover_page()

    # Part 5 - 40 questions
    pdf.add_page()
    pdf.section_title("Part 5: Incomplete Sentences (40 Questions)")
    pdf.body("Choose the best answer to complete each sentence. This drill covers ALL grammar topics from Weeks 1-10.")

    part5 = [
        ("The _______ of the new building was completed ahead of schedule.", "construct", "constructive", "construction", "constructively"),
        ("Ms. Wang has _______ the sales team since January.", "manage", "managed", "managing", "management"),
        ("All documents must be _______ by the department head before distribution.", "approve", "approving", "approved", "approval"),
        ("The company is looking for candidates _______ have experience in marketing.", "whom", "whose", "which", "who"),
        ("_______ the heavy rain, the outdoor event was held as planned.", "Although", "Because of", "Despite", "Therefore"),
        ("The quarterly report will be submitted _______ the end of this month.", "in", "on", "at", "by"),
        ("If the budget _______ approved, the project will begin next month.", "is", "was", "will be", "would be"),
        ("The new employee training program has been very _______.", "effect", "effective", "effectively", "effectiveness"),
        ("Sales have increased _______ since the new advertising campaign launched.", "significance", "significant", "significantly", "signify"),
        ("The meeting room _______ we usually use is being renovated.", "who", "whom", "whose", "that"),
        ("_______ in 2005, the company has grown to over 500 employees.", "Establish", "Established", "Establishing", "Establishment"),
        ("Employees are required to _______ with the new dress code policy.", "comply", "compliance", "compliant", "compliantly"),
        ("The hotel offers a _______ breakfast to all guests.", "compliment", "complimentary", "complimenting", "complimentarily"),
        ("_______ the training session ends, please complete the evaluation form.", "If", "Unless", "When", "Despite"),
        ("The manager _______ the team for their outstanding performance.", "commend", "commended", "commending", "commendation"),
        ("The proposal was rejected; _______, the team submitted a revised version.", "moreover", "however", "therefore", "furthermore"),
        ("She has been responsible _______ managing the company's finances.", "to", "in", "for", "with"),
        ("The _______ results of the experiment were published in a journal.", "surprise", "surprising", "surprised", "surprisingly"),
        ("Customers _______ purchase items over $100 will receive free shipping.", "who", "whom", "whose", "which"),
        ("The company plans to _______ its operations to Southeast Asia.", "expand", "expansion", "expansive", "expanded"),
        ("_______ you have any questions, do not hesitate to contact us.", "Although", "Should", "Despite", "Moreover"),
        ("The annual conference _______ place at the Grand Hotel every year.", "take", "takes", "took", "taking"),
        ("The new software is _______ with all major operating systems.", "compatible", "compatibility", "compatibly", "comparison"),
        ("_______ heavy investment in marketing, the product failed to sell.", "Although", "Because", "Despite", "However"),
        ("The contract must be signed _______ both parties before it takes effect.", "from", "to", "by", "for"),
        ("She felt _______ after the long journey.", "exhaust", "exhausting", "exhausted", "exhaustion"),
        ("The company has not yet decided _______ to launch the new product.", "what", "which", "when", "who"),
        ("The report, _______ was prepared by the research team, contains vital data.", "that", "which", "who", "whom"),
        ("Profits declined last year; _______, the company reduced its workforce.", "however", "moreover", "consequently", "nevertheless"),
        ("The landlord requires tenants to pay rent _______ the first of each month.", "in", "on", "at", "by"),
        ("The new regulations will go into effect _______ January 1.", "in", "on", "at", "by"),
        ("Applicants must have a minimum of five years of _______ in the field.", "experience", "experienced", "experiencing", "experiential"),
        ("The project was completed _______ than expected.", "early", "earlier", "earliest", "earliness"),
        ("All employees are _______ to attend the safety seminar.", "require", "required", "requiring", "requirement"),
        ("The company offered generous _______ to attract top talent.", "compensate", "compensated", "compensation", "compensatory"),
        ("_______ completing the training, new employees receive their ID badges.", "With", "Upon", "During", "While"),
        ("The product is designed for consumers who are _______ about quality.", "concern", "concerned", "concerning", "concerns"),
        ("We need to hire someone _______ skills include data analysis.", "who", "whom", "whose", "which"),
        ("The shipment will arrive _______ the end of the week.", "in", "on", "at", "by"),
        ("The board of directors _______ unanimously to approve the merger.", "vote", "voted", "voting", "votes"),
    ]

    pdf.part5_questions(part5)

    # Part 6 - Text Completion (2 passages with blanks)
    pdf.add_page()
    pdf.section_title("Part 6: Text Completion")
    pdf.body("Read the following texts and choose the best answer for each blank.")

    pdf.sub_title("Passage 1: Company Announcement")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    passage1 = """Dear Employees,

We are pleased to announce that GlobalTech has been __(41)__ as the Best Workplace of the Year by Business Weekly magazine. This achievement reflects the hard work and __(42)__ of every team member.

To celebrate this honor, the company will host a special dinner on December 15 at the Regent Hotel. All employees and their families are invited to attend. __(43)__, we will be giving each employee a $200 gift card as a token of appreciation.

Please RSVP by December 8 by emailing events@globaltech.com. We look forward to __(44)__ this achievement together.

Best regards,
Management"""
    pdf.multi_cell(170, 6, passage1, border=1, fill=True)
    pdf.ln(3)

    p6_q1 = [
        ("(41)", "recognize", "recognized", "recognizing", "recognition"),
        ("(42)", "dedicate", "dedicating", "dedicated", "dedication"),
        ("(43)", "However", "Therefore", "Additionally", "Nevertheless"),
        ("(44)", "celebrate", "celebrating", "celebrated", "celebration"),
    ]
    pdf.part5_questions(p6_q1)

    pdf.sub_title("Passage 2: Store Policy")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    passage2 = """RETURN POLICY

Thank you for shopping at BrightMart. We want you to be completely __(45)__ with your purchase. If you are not happy with an item, you may return it within 30 days.

To process a return, the item must be in its original packaging and __(46)__ by the receipt. Refunds will be issued to the original payment method within 5-7 business days.

Please note that certain items, __(47)__ electronics and personal care products, cannot be returned once opened. __(48)__ you have questions about our return policy, please contact customer service at 1-800-555-0199.

BrightMart Management"""
    pdf.multi_cell(170, 6, passage2, border=1, fill=True)
    pdf.ln(3)

    p6_q2 = [
        ("(45)", "satisfy", "satisfying", "satisfied", "satisfaction"),
        ("(46)", "accompany", "accompanying", "accompanied", "accompaniment"),
        ("(47)", "include", "included", "includes", "including"),
        ("(48)", "Although", "Despite", "Should", "Moreover"),
    ]
    pdf.part5_questions(p6_q2)

    # Answer Key
    pdf.add_page()
    pdf.section_title("Answer Key 解答與詳解")

    pdf.sub_title("Part 5 Answers:")
    p5_answers = [
        ("C", "冠詞 The 後面需要名詞，construction。"),
        ("B", "has + p.p. 現在完成式，managed。"),
        ("C", "must be + p.p. 被動語態，approved。"),
        ("D", "先行詞是 candidates（人），缺主詞，用 who。"),
        ("C", "空格後是名詞片語 the heavy rain，用 Despite。"),
        ("D", "by the end of = 在...結束之前。"),
        ("A", "if 條件句用現在式，is。"),
        ("B", "has been very + 形容詞，effective。"),
        ("C", "修飾動詞 increased 用副詞，significantly。"),
        ("D", "先行詞是 The meeting room（物），用 that。"),
        ("B", "company 被成立，用過去分詞 Established。"),
        ("A", "are required to + 原形動詞，comply。"),
        ("B", "需要形容詞修飾 breakfast，complimentary（免費的）。"),
        ("C", "當...結束時，用 When。"),
        ("B", "過去式動詞，commended。"),
        ("B", "提案被拒但提交了修改版，語意轉折用 however。"),
        ("C", "responsible for 固定搭配。"),
        ("B", "results 是物，令人驚訝用 surprising。"),
        ("A", "先行詞是 Customers（人），缺主詞，用 who。"),
        ("A", "plans to + 原形動詞，expand。"),
        ("B", "Should you = If you，正式條件句倒裝。"),
        ("B", "every year 現在式，第三人稱用 takes。"),
        ("A", "is + 形容詞，compatible。"),
        ("C", "空格後是名詞片語 heavy investment，用 Despite。"),
        ("C", "signed by = 由...簽署。"),
        ("C", "She 是人，感到疲憊用 exhausted。"),
        ("C", "尚未決定「何時」推出，用 when。"),
        ("B", "有逗號的非限定子句，先行詞是 report（物），用 which。"),
        ("C", "利潤下降，結果裁員。因果關係用 consequently。"),
        ("D", "by the first = 在第一天之前。"),
        ("B", "January 1 是特定日期，用 on。"),
        ("A", "five years of + 名詞，experience。"),
        ("B", "比較級，用 earlier。"),
        ("B", "are required = 被要求，被動語態。"),
        ("C", "形容詞 generous + 名詞，compensation。"),
        ("B", "Upon completing = 一旦完成，Upon + V-ing。"),
        ("B", "consumers 是人，感到關心用 concerned。"),
        ("C", "空格後有名詞 skills（所有格），用 whose。"),
        ("D", "by the end of = 在...之前。"),
        ("B", "過去式動詞，voted。"),
    ]

    pdf.set_font("chi", "", 9)
    for i, (ans, expl) in enumerate(p5_answers, 1):
        if pdf.get_y() > 268:
            pdf.add_page()
        pdf.set_font("chi", "B", 9)
        pdf.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("chi", "", 9)
        pdf.multi_cell(0, 5, f"   {expl}")
        pdf.ln(1)

    pdf.ln(3)
    pdf.sub_title("Part 6 Answers:")
    p6_answers = [
        ("B", "(41) has been + p.p. 被動語態，recognized。"),
        ("D", "(42) the + 名詞，dedication（奉獻）。"),
        ("C", "(43) 補充說明額外福利，用 Additionally（此外）。"),
        ("B", "(44) look forward to + V-ing，celebrating。"),
        ("C", "(45) 人感到滿意用 satisfied。"),
        ("C", "(46) be + p.p. 被動語態，accompanied（附有）。"),
        ("D", "(47) including = 包括，後接名詞列表。"),
        ("C", "(48) Should you = If you，正式條件句。"),
    ]

    pdf.set_font("chi", "", 9)
    for i, (ans, expl) in enumerate(p6_answers, 41):
        if pdf.get_y() > 268:
            pdf.add_page()
        pdf.set_font("chi", "B", 9)
        pdf.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("chi", "", 9)
        pdf.multi_cell(0, 5, f"   {expl}")
        pdf.ln(1)

    path = os.path.join(OUTPUT_DIR, "week11.pdf")
    pdf.output(path)
    print(f"  [OK] {path}")


def week12():
    title = "Part 7 Reading Intensive (4 Passages)"

    pdf = ToeicPDF(12, title)
    pdf.cover_page()

    # Reading tips
    pdf.add_page()
    pdf.section_title("Part 7 閱讀技巧")
    pdf.grammar_block("""## TOEIC Part 7 答題策略

## 1. 先看題目再看文章
先快速掃過題目，知道要找什麼資訊，再帶著問題去讀文章。

## 2. 常見文章類型
email (電子郵件), letter (信件), notice (公告), advertisement (廣告),
article (文章), report (報告), form (表格), text message (簡訊)

## 3. 常見題目類型
主旨題：What is the purpose of this email?
細節題：When will the event take place?
推論題：What can be inferred about Mr. Kim?
同義詞題：The word "address" in line 5 is closest in meaning to...
NOT/TRUE 題：What is NOT mentioned in the notice?

## 4. 時間分配
單篇閱讀：每篇約3-4分鐘
雙篇閱讀：每組約5-6分鐘
三篇閱讀：每組約6-7分鐘

## 5. 關鍵技巧
找關鍵字定位答案位置
注意同義替換（paraphrase）
答案通常按照文章順序出現""")

    # Passage 1 - Email
    pdf.add_page()
    pdf.section_title("Passage 1: Email Exchange")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    p1 = """From: sarah.martinez@techsolutions.com
To: james.wilson@techsolutions.com
Date: February 10
Subject: Client Meeting Rescheduled

Hi James,

I wanted to let you know that our meeting with Pinnacle Corp has been rescheduled from Thursday, February 13, to Monday, February 17, at 2:00 p.m. The client requested the change because their CFO, Ms. Rebecca Torres, will be traveling on Thursday and wants to be present for the presentation.

I've already reserved Conference Room B for the meeting. Could you please update the presentation slides to include the Q3 financial projections? Also, please print 10 copies of the proposal document for distribution.

I'd like us to do a practice run of the presentation on Friday afternoon. Are you available at 3:00 p.m.?

Thanks,
Sarah"""
    pdf.multi_cell(170, 6, p1, border=1, fill=True)
    pdf.ln(2)

    pdf.set_fill_color(250, 250, 245)
    p1b = """From: james.wilson@techsolutions.com
To: sarah.martinez@techsolutions.com
Date: February 10
Subject: RE: Client Meeting Rescheduled

Hi Sarah,

Thanks for the update. I'll revise the slides to include the Q3 data by Thursday evening. However, I won't be available for the practice run on Friday at 3:00 p.m. because I have a dentist appointment. Could we do it at 10:00 a.m. instead?

Also, I noticed that we don't have the latest revenue figures from the finance department. Should I contact them directly, or would you prefer to handle that?

Best,
James"""
    pdf.multi_cell(170, 6, p1b, border=1, fill=True)
    pdf.ln(3)

    q1 = [
        ("Why was the meeting rescheduled?", "The conference room was unavailable", "The CFO will be traveling on the original date", "James was not available", "The presentation was not ready"),
        ("What does Sarah ask James to do?", "Reserve a conference room", "Contact Ms. Torres", "Update the slides with Q3 projections", "Cancel the original meeting"),
        ("Why can't James do the practice run at 3:00 p.m. on Friday?", "He has another meeting", "He has a dentist appointment", "He will be on vacation", "He needs to finish the slides"),
        ("What information is James missing?", "The meeting location", "The client's contact information", "The latest revenue figures", "The presentation schedule"),
        ("When will the presentation slides be ready?", "February 10", "By Thursday evening", "Friday morning", "February 17"),
    ]
    pdf.sub_title("Questions 1-5:")
    pdf.part5_questions(q1)

    # Passage 2 - Notice
    pdf.add_page()
    pdf.section_title("Passage 2: Company Notice")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    p2 = """ANNUAL EMPLOYEE HEALTH SCREENING

The Human Resources Department is pleased to announce that the annual employee health screening will be held in the first-floor conference hall from March 3 to March 7.

SCHEDULE:
Monday, March 3: Departments A-C (Last names starting with A through C)
Tuesday, March 4: Departments D-G
Wednesday, March 5: Departments H-L
Thursday, March 6: Departments M-R
Friday, March 7: Departments S-Z

TIME: 8:00 a.m. to 4:00 p.m. each day
Appointments are available in 15-minute intervals. Please sign up through the employee portal by February 25.

WHAT TO EXPECT:
- Basic physical examination
- Blood pressure and cholesterol check
- Vision and hearing test
- Optional flu vaccination (free of charge)

PREPARATION:
- Please fast for at least 8 hours before your appointment for accurate blood test results.
- Bring your employee ID card.
- Wear comfortable clothing.

Employees who complete the health screening will receive a $50 wellness credit on their next paycheck. For questions, contact HR at extension 4500.

Human Resources Department"""
    pdf.multi_cell(170, 6, p2, border=1, fill=True)
    pdf.ln(3)

    q2 = [
        ("When should employees sign up for the screening?", "By February 25", "By March 1", "By March 3", "By March 7"),
        ("Which day should an employee with the last name 'Park' attend?", "Monday", "Tuesday", "Wednesday", "Thursday"),
        ("What should employees do before the health screening?", "Exercise for 30 minutes", "Fast for at least 8 hours", "Bring a doctor's note", "Complete an online form"),
        ("What incentive do employees receive for completing the screening?", "A day off", "A $50 wellness credit", "Free gym membership", "A gift card"),
        ("What is optional during the health screening?", "Blood pressure check", "Vision test", "Flu vaccination", "Cholesterol check"),
    ]
    pdf.sub_title("Questions 6-10:")
    pdf.part5_questions(q2)

    # Passage 3 - Article
    pdf.add_page()
    pdf.section_title("Passage 3: News Article")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    p3 = """LOCAL COFFEE CHAIN ANNOUNCES EXPANSION PLANS

Metro Coffee, a popular local coffee chain founded in Taipei in 2015, announced plans to open 15 new locations across Taiwan over the next two years. The announcement was made at a press conference on Wednesday by CEO Angela Liu.

"Since our founding, we have focused on providing high-quality coffee at reasonable prices," said Liu. "Our customers have shown tremendous loyalty, and we believe it's time to bring Metro Coffee to more communities."

The expansion will begin with five new stores in Taichung and Kaohsiung in the first half of next year. An additional ten stores will open in smaller cities, including Hsinchu, Tainan, and Chiayi, by the end of the following year.

Metro Coffee currently operates 25 locations, all in the greater Taipei area. The company reported annual revenue of $15 million last year, a 25% increase from the previous year.

To support the expansion, Metro Coffee plans to hire approximately 200 new employees, including store managers, baristas, and administrative staff. Job postings will be available on the company's website starting next month.

Industry analyst Kevin Huang commented, "Metro Coffee has found a sweet spot in the market between premium coffee shops and convenience store coffee. Their expansion into other cities is a natural next step."

The company also announced a new loyalty app that will launch simultaneously with the first new stores. The app will offer rewards, mobile ordering, and exclusive promotions to registered users."""
    pdf.multi_cell(170, 6, p3, border=1, fill=True)
    pdf.ln(3)

    q3 = [
        ("How many new locations does Metro Coffee plan to open?", "5", "10", "15", "25"),
        ("Where does Metro Coffee currently have stores?", "Throughout Taiwan", "In the greater Taipei area only", "In Taipei and Kaohsiung", "In six major cities"),
        ("What was Metro Coffee's revenue increase last year?", "15%", "20%", "25%", "30%"),
        ("How many new employees will be hired?", "About 100", "About 150", "About 200", "About 250"),
        ("What will the new loyalty app offer?", "Free coffee every month", "Rewards and mobile ordering", "Delivery service", "Music streaming"),
    ]
    pdf.sub_title("Questions 11-15:")
    pdf.part5_questions(q3)

    # Passage 4 - Double passage (linked information)
    pdf.add_page()
    pdf.section_title("Passage 4: Job Posting + Application Email")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    p4a = """POSITION: Marketing Coordinator
COMPANY: Horizon Media Group
LOCATION: Taipei, Taiwan
SALARY: NT$45,000 - NT$55,000 per month (depending on experience)

Horizon Media Group is seeking a motivated Marketing Coordinator to join our growing team. The ideal candidate will have:

Requirements:
- Bachelor's degree in marketing, communications, or a related field
- Minimum 2 years of experience in digital marketing
- Proficiency in social media management tools
- Strong written and verbal communication skills in both English and Mandarin
- Experience with Google Analytics and SEO optimization

Responsibilities:
- Develop and execute social media marketing campaigns
- Analyze campaign performance and prepare monthly reports
- Coordinate with external agencies and vendors
- Manage the company's content calendar
- Assist in organizing promotional events

Benefits: Health insurance, annual bonus, 15 days paid leave, professional development budget

To apply, send your resume and cover letter to careers@horizonmedia.com by March 20. Please include "Marketing Coordinator Application" in the subject line."""
    pdf.multi_cell(170, 6, p4a, border=1, fill=True)
    pdf.ln(2)

    pdf.set_fill_color(250, 250, 245)
    p4b = """From: lisa.chen@email.com
To: careers@horizonmedia.com
Date: March 15
Subject: Marketing Coordinator Application

Dear Hiring Manager,

I am writing to apply for the Marketing Coordinator position advertised on your website. I believe my qualifications and experience make me an excellent candidate for this role.

I graduated from National Taiwan University with a degree in Business Administration, with a minor in communications. For the past three years, I have worked as a Digital Marketing Specialist at Skyline Advertising, where I managed social media campaigns for over 20 clients.

In my current role, I have increased social media engagement by an average of 35% across all client accounts. I am proficient in Hootsuite, Google Analytics, and various SEO tools. I am also fluent in both English and Mandarin.

I am particularly interested in Horizon Media Group because of its reputation for innovative marketing strategies. I am excited about the opportunity to contribute to your team's success.

I have attached my resume and portfolio for your review. I am available for an interview at your convenience.

Thank you for your consideration.

Sincerely,
Lisa Chen"""
    pdf.multi_cell(170, 6, p4b, border=1, fill=True)
    pdf.ln(3)

    q4 = [
        ("What is the minimum experience required for the position?", "1 year", "2 years", "3 years", "5 years"),
        ("What is NOT listed as a job responsibility?", "Managing social media campaigns", "Preparing monthly reports", "Training new employees", "Organizing promotional events"),
        ("What degree does Lisa Chen hold?", "Marketing", "Communications", "Business Administration", "Computer Science"),
        ("How long has Lisa Chen worked in her current position?", "One year", "Two years", "Three years", "Five years"),
        ("What did Lisa Chen achieve in her current role?", "Increased sales by 35%", "Managed 50 clients", "Increased social media engagement by 35%", "Reduced marketing costs by 20%"),
    ]
    pdf.sub_title("Questions 16-20:")
    pdf.part5_questions(q4)

    # Answer Key
    pdf.add_page()
    pdf.section_title("Answer Key 解答與詳解")

    all_answers = [
        ("B", "Sarah 提到 their CFO will be traveling on Thursday。"),
        ("C", "Sarah 要求 James update the presentation slides to include the Q3 financial projections。"),
        ("B", "James 說 I have a dentist appointment。"),
        ("C", "James 說 we don't have the latest revenue figures。"),
        ("B", "James 說 I'll revise the slides by Thursday evening。"),
        ("A", "文中提到 Please sign up through the employee portal by February 25。"),
        ("D", "Park 姓氏 P 開頭，屬於 M-R，Thursday, March 6。"),
        ("B", "文中提到 Please fast for at least 8 hours before your appointment。"),
        ("B", "文中提到 employees will receive a $50 wellness credit。"),
        ("C", "文中提到 Optional flu vaccination (free of charge)。"),
        ("C", "文中提到 plans to open 15 new locations。"),
        ("B", "文中提到 currently operates 25 locations, all in the greater Taipei area。"),
        ("C", "文中提到 a 25% increase from the previous year。"),
        ("C", "文中提到 plans to hire approximately 200 new employees。"),
        ("B", "文中提到 app will offer rewards, mobile ordering, and exclusive promotions。"),
        ("B", "文中提到 Minimum 2 years of experience。"),
        ("C", "Training new employees 未列在職責中。"),
        ("C", "Lisa 提到 graduated from National Taiwan University with a degree in Business Administration。"),
        ("C", "Lisa 提到 For the past three years。"),
        ("C", "Lisa 提到 increased social media engagement by an average of 35%。"),
    ]

    pdf.set_font("chi", "", 9)
    for i, (ans, expl) in enumerate(all_answers, 1):
        if pdf.get_y() > 268:
            pdf.add_page()
        pdf.set_font("chi", "B", 9)
        pdf.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("chi", "", 9)
        pdf.multi_cell(0, 5, f"   {expl}")
        pdf.ln(1)

    path = os.path.join(OUTPUT_DIR, "week12.pdf")
    pdf.output(path)
    print(f"  [OK] {path}")


def week13():
    title = "Full Mock Test Simulation + Final Review"

    pdf = ToeicPDF(13, title)
    pdf.cover_page()

    # Review tips
    pdf.add_page()
    pdf.section_title("Final Review: 13 週重點回顧")
    pdf.grammar_block("""## 考試策略總整理

## Part 5 (30題, 建議10分鐘)
1. 詞性題 (30-40%)：看空格位置，判斷需要名詞/動詞/形容詞/副詞
2. 文法題 (20-30%)：時態、被動語態、關係子句、條件句
3. 詞彙題 (20-30%)：考同義詞或搭配用法
4. 介係詞/連接詞題 (10-20%)：固定搭配和邏輯關係

## Part 6 (16題, 建議10分鐘)
1. 先快速瀏覽整篇文章
2. 大部分題目與 Part 5 類似（詞性、文法、詞彙）
3. 但有「插入句」題型：要看上下文邏輯

## Part 7 (54題, 建議55分鐘)
1. 先看題目再看文章
2. 找關鍵字定位
3. 注意同義替換
4. 時間不夠時優先做單篇閱讀

## 文法重點清單
Week 1: 詞性辨識 (名詞、動詞、形容詞、副詞字尾)
Week 2: 動詞時態 (現在/過去/未來式)
Week 3: 完成式 (現在完成/過去完成/未來完成)
Week 4: 被動語態 (be + p.p.)
Week 5: 關係子句 (who/which/that/whose/where/when)
Week 6: 連接詞 (because/although/if/unless + 對等連接詞)
Week 7: 介係詞 (in/on/at/by/for + 固定搭配)
Week 8: 副詞連接詞 (however/therefore/moreover/nevertheless)
Week 9: 分詞 (-ing 令人.../  -ed 感到...)
Week 10: 條件句 (if/unless/provided that)""")

    # Mock Test Part 5 (30 questions)
    pdf.add_page()
    pdf.section_title("Mock Test: Part 5 (30 Questions)")
    pdf.body("Time limit: 10 minutes. Choose the best answer.")

    mock_p5 = [
        ("The management team has _______ a new policy regarding remote work.", "implement", "implementing", "implemented", "implementation"),
        ("All _______ must be submitted to the finance department by March 15.", "invoice", "invoices", "invoicing", "invoiced"),
        ("The seminar was extremely _______ for all participants.", "benefit", "beneficial", "beneficially", "benefiting"),
        ("Ms. Rodriguez, _______ has led the team for five years, announced her retirement.", "that", "which", "who", "whom"),
        ("_______ the company faced financial difficulties, it managed to avoid layoffs.", "Despite", "Although", "However", "Because of"),
        ("The new software will be installed _______ all company computers next week.", "in", "on", "at", "by"),
        ("If the proposal _______ accepted, construction will begin in June.", "is", "was", "will be", "would be"),
        ("The report was _______ by the external auditors last Friday.", "review", "reviewing", "reviewed", "reviewer"),
        ("_______ in the city center, the office is easily accessible by public transportation.", "Locate", "Located", "Locating", "Location"),
        ("Customer satisfaction has increased _______ since the new service policy was introduced.", "notable", "notability", "notably", "noting"),
        ("The CEO _______ to all employees at the annual meeting yesterday.", "speak", "spoke", "spoken", "speaking"),
        ("We need to order _______ office supplies before the end of the month.", "addition", "additional", "additionally", "adding"),
        ("The conference room _______ we booked is on the tenth floor.", "who", "whom", "where", "that"),
        ("_______ completing the orientation program, new hires will be assigned to their departments.", "Upon", "During", "While", "Since"),
        ("The marketing department is responsible _______ creating the advertising campaign.", "to", "in", "for", "with"),
        ("Sales figures were _______ than expected during the holiday season.", "high", "higher", "highest", "highly"),
        ("The company offers competitive salaries _______ attract qualified candidates.", "for", "in order to", "so", "because"),
        ("The warranty will be void _______ the product is used improperly.", "unless", "if", "although", "despite"),
        ("_______ budget constraints, the research department continued its projects.", "Although", "Because of", "Despite", "Therefore"),
        ("Employees who wish to _______ for the management training program should apply by Friday.", "registration", "register", "registered", "registering"),
        ("The board of directors will _______ the final decision next Tuesday.", "make", "made", "making", "makes"),
        ("The new regulation requires all buildings to be _______ for fire safety.", "inspect", "inspected", "inspecting", "inspection"),
        ("Sales revenue grew _______ in the third quarter compared to the second.", "steady", "steadily", "steadiness", "steadier"),
        ("The company picnic, _______ is held annually, will take place on September 20.", "that", "which", "who", "whom"),
        ("Please ensure that all documents are _______ organized before the audit.", "proper", "properly", "properness", "property"),
        ("Mr. Tanaka has been _______ as the new branch manager.", "appoint", "appointed", "appointing", "appointment"),
        ("The product recall was _______ due to safety concerns.", "initiate", "initiating", "initiated", "initiative"),
        ("_______ you experience any technical issues, please contact the IT helpdesk.", "Unless", "Although", "Should", "Despite"),
        ("The meeting will be held in the conference hall _______ the second floor.", "in", "on", "at", "by"),
        ("The project deadline has been extended; _______, all team members should continue working diligently.", "moreover", "however", "therefore", "nevertheless"),
    ]
    pdf.part5_questions(mock_p5)

    # Mock Part 6
    pdf.add_page()
    pdf.section_title("Mock Test: Part 6 (8 Questions)")

    pdf.sub_title("Text 1")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    mock_p6a = """Dear Mr. Thompson,

Thank you for your interest in the Marketing Manager position at Vertex Communications. We were very __(31)__ with your qualifications and interview performance.

We are pleased to __(32)__ you that you have been selected for the position. Your starting salary will be $65,000 per year, with a comprehensive benefits package __(33)__ health insurance, dental coverage, and a retirement plan.

__(34)__. Please contact our HR department at hr@vertex.com to complete the necessary paperwork.

We look forward to having you on our team.

Sincerely,
Patricia Wells
Director of Human Resources"""
    pdf.multi_cell(170, 6, mock_p6a, border=1, fill=True)
    pdf.ln(3)

    mock_p6a_q = [
        ("(31)", "impress", "impressive", "impressed", "impressing"),
        ("(32)", "inform", "informed", "informing", "information"),
        ("(33)", "include", "included", "includes", "including"),
        ("(34) Choose the sentence that best completes the text.", "We regret to inform you that the position has been filled.", "Your first day of work will be Monday, April 7.", "Unfortunately, we cannot offer you the position at this time.", "We will review your application and get back to you soon."),
    ]
    pdf.part5_questions(mock_p6a_q)

    pdf.sub_title("Text 2")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    mock_p6b = """NOTICE TO ALL RESIDENTS

The management office would like to inform all residents that the annual building maintenance will be __(35)__ from April 14 to April 18.

During this period, the following work will be performed:
- Exterior painting of the building
- Elevator inspection and maintenance (one elevator will remain __(36)__ at all times)
- Rooftop waterproofing

Residents should be __(37)__ that there may be some noise during working hours (8:00 a.m. to 5:00 p.m.). We sincerely apologize for any inconvenience.

__(38)__. For questions, please contact the management office at extension 100.

Building Management"""
    pdf.multi_cell(170, 6, mock_p6b, border=1, fill=True)
    pdf.ln(3)

    mock_p6b_q = [
        ("(35)", "conduct", "conducting", "conducted", "conducts"),
        ("(36)", "operate", "operational", "operating", "operation"),
        ("(37)", "aware", "awareness", "awaring", "awared"),
        ("(38) Choose the sentence that best completes the text.", "The maintenance has been canceled due to budget cuts.", "Please make alternative arrangements for parking during this period.", "Thank you for your understanding and cooperation.", "We are currently accepting applications for new tenants."),
    ]
    pdf.part5_questions(mock_p6b_q)

    # Mock Part 7 (2 passages)
    pdf.add_page()
    pdf.section_title("Mock Test: Part 7 (16 Questions)")

    pdf.sub_title("Passage 1: Notice")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    mock_p7a = """CITYWIDE TRANSPORTATION UPDATE

Effective Monday, March 10, the Greenline subway route will undergo major renovations. The following changes will be in effect until June 30:

1. Stations between Central Park and Harbor View will be closed. A free shuttle bus service will operate between these stations every 10 minutes from 6:00 a.m. to midnight.

2. The Redline subway will increase its frequency during peak hours (7:00-9:00 a.m. and 5:00-7:00 p.m.) to accommodate additional passengers.

3. Temporary bus route G7 will be added, running from Central Park to the Business District via Main Street. This route will operate from 6:30 a.m. to 11:00 p.m.

4. Monthly pass holders for the Greenline will receive a 20% discount on all bus services during the renovation period. To claim this discount, present your monthly pass at any customer service center.

For real-time updates and route planning, download the City Transit app or visit www.citytransit.gov.

We appreciate your patience during this improvement project."""
    pdf.multi_cell(170, 6, mock_p7a, border=1, fill=True)
    pdf.ln(3)

    mock_q7a = [
        ("How long will the Greenline renovations last?", "About one month", "About two months", "About four months", "About six months"),
        ("How often do shuttle buses run between the closed stations?", "Every 5 minutes", "Every 10 minutes", "Every 15 minutes", "Every 30 minutes"),
        ("What benefit do Greenline monthly pass holders receive?", "Free bus rides", "A 20% bus discount", "A free monthly Redline pass", "Priority boarding"),
        ("What is the temporary bus route G7?", "A replacement for the Redline", "A route from Central Park to Business District", "A route to the airport", "An express route to Harbor View"),
    ]
    pdf.sub_title("Questions 1-4:")
    pdf.part5_questions(mock_q7a)

    pdf.add_page()
    pdf.sub_title("Passage 2: Email + Schedule")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    mock_p7b1 = """From: events@industryexpo.com
To: all-exhibitors@industryexpo.com
Date: April 2
Subject: Industry Expo 2026 - Exhibitor Information

Dear Exhibitors,

Thank you for registering for Industry Expo 2026. Here is essential information for the event:

DATES: April 21-23 (Monday to Wednesday)
VENUE: Taipei International Convention Center
SETUP: Sunday, April 20, from 8:00 a.m. to 8:00 p.m.
TEARDOWN: Wednesday, April 23, from 5:00 p.m. to 10:00 p.m., or Thursday, April 24, from 8:00 a.m. to 12:00 p.m.

Each exhibitor will receive:
- Two exhibitor badges (additional badges: $50 each)
- One 3m x 3m booth space with basic setup (table, chairs, power)
- Listing in the official event directory
- Access to the exhibitor lounge

Please submit your booth design for approval by April 10. All electrical equipment must meet safety standards.

For any questions, contact our exhibitor services team at exhibitors@industryexpo.com.

Best regards,
Event Management Team"""
    pdf.multi_cell(170, 6, mock_p7b1, border=1, fill=True)
    pdf.ln(2)

    pdf.set_fill_color(250, 250, 245)
    mock_p7b2 = """INDUSTRY EXPO 2026 - EVENT SCHEDULE

Monday, April 21:
9:00 a.m. - Opening ceremony (Main Hall)
10:00 a.m. - Exhibition opens to visitors
12:00 p.m. - Keynote: "The Future of AI in Manufacturing" by Dr. Sarah Kim
2:00 p.m. - Panel: Sustainable Business Practices

Tuesday, April 22:
10:00 a.m. - Exhibition opens
11:00 a.m. - Workshop: Digital Marketing for Small Businesses
1:00 p.m. - Networking lunch (Exhibitor Lounge)
3:00 p.m. - Product Innovation Awards ceremony

Wednesday, April 23:
10:00 a.m. - Exhibition opens
11:00 a.m. - Workshop: Supply Chain Optimization
2:00 p.m. - Closing remarks
3:00 p.m. - Exhibition closes to visitors
5:00 p.m. - Teardown begins"""
    pdf.multi_cell(170, 6, mock_p7b2, border=1, fill=True)
    pdf.ln(3)

    mock_q7b = [
        ("When can exhibitors set up their booths?", "April 20", "April 21", "April 22", "April 23"),
        ("How many exhibitor badges are included?", "One", "Two", "Three", "Five"),
        ("When is the deadline for booth design approval?", "April 2", "April 10", "April 20", "April 21"),
        ("What happens on Tuesday at 3:00 p.m.?", "A networking lunch", "The opening ceremony", "Product Innovation Awards ceremony", "A workshop"),
        ("When does the exhibition close to visitors on the last day?", "2:00 p.m.", "3:00 p.m.", "5:00 p.m.", "8:00 p.m."),
        ("What is NOT included with the booth space?", "Table and chairs", "Power supply", "A listing in the event directory", "Printed marketing materials"),
        ("Who is giving the keynote speech?", "The event manager", "Dr. Sarah Kim", "An industry panel", "Product award winners"),
        ("When is the latest possible time to complete teardown?", "Wednesday 10 p.m.", "Thursday 8 a.m.", "Thursday 12 p.m.", "Thursday 5 p.m."),
    ]
    pdf.sub_title("Questions 5-12:")
    pdf.part5_questions(mock_q7b)

    # Passage 3 - Article with questions
    pdf.add_page()
    pdf.sub_title("Passage 3: News Article")
    pdf.set_font("chi", "", 10)
    pdf.set_fill_color(250, 250, 245)
    mock_p7c = """GREEN ENERGY INITIATIVE GAINS MOMENTUM IN TAIWAN

Taiwan's government announced a major expansion of its green energy program on Monday, pledging to invest NT$50 billion over the next five years in renewable energy infrastructure.

The plan includes the construction of three new solar power plants in southern Taiwan, expansion of the existing offshore wind farm near Changhua, and development of a new battery storage facility in Taoyuan. When completed, these projects are expected to generate enough clean energy to power approximately 500,000 homes.

Energy Minister Chen Wei-lin stated at a press conference, "Taiwan has set an ambitious goal of generating 20% of its electricity from renewable sources by 2030. This investment brings us significantly closer to achieving that target."

The initiative is expected to create over 8,000 new jobs in construction, engineering, and maintenance. Several international companies, including WindPower Global from Denmark and SolarTech from Germany, have already expressed interest in participating in the projects.

Environmental groups have praised the announcement but urged the government to set even more ambitious targets. "While this is a positive step, we believe Taiwan should aim for 30% renewable energy by 2030," said Green Taiwan Foundation spokesperson Michael Wang."""
    pdf.multi_cell(170, 6, mock_p7c, border=1, fill=True)
    pdf.ln(3)

    mock_q7c = [
        ("How much will the government invest in renewable energy?", "NT$20 billion", "NT$30 billion", "NT$50 billion", "NT$80 billion"),
        ("How many homes could the new projects power?", "About 100,000", "About 300,000", "About 500,000", "About 800,000"),
        ("What is Taiwan's renewable energy target for 2030?", "10%", "15%", "20%", "30%"),
        ("What target does the Green Taiwan Foundation recommend?", "20%", "25%", "30%", "50%"),
    ]
    pdf.sub_title("Questions 13-16:")
    pdf.part5_questions(mock_q7c)

    # Answer Key
    pdf.add_page()
    pdf.section_title("Answer Key 解答與詳解")

    pdf.sub_title("Part 5 Answers:")
    mock_p5_ans = [
        ("C", "has + p.p.，implemented。"),
        ("B", "All + 複數名詞 invoices。"),
        ("B", "was + 形容詞 beneficial。"),
        ("C", "非限定子句，先行詞是人，用 who。"),
        ("B", "兩個子句用逗號連接，需要連接詞 Although。"),
        ("B", "installed on computers，on 表示在設備上。"),
        ("A", "If 條件句用現在式 is。"),
        ("C", "was + p.p. 被動語態 reviewed。"),
        ("B", "被動意義，用過去分詞 Located。"),
        ("C", "修飾動詞 increased 用副詞 notably。"),
        ("B", "yesterday 過去式 spoke。"),
        ("B", "修飾名詞 supplies 用形容詞 additional。"),
        ("D", "先行詞是物 conference room，用 that。"),
        ("A", "Upon + V-ing 表示「一旦...」。"),
        ("C", "responsible for 固定搭配。"),
        ("B", "than 表示比較級 higher。"),
        ("B", "in order to + 原形動詞，表目的。"),
        ("B", "如果不當使用保固會失效。if 表條件。"),
        ("C", "空格後是名詞片語 budget constraints，用 Despite。"),
        ("B", "wish to + 原形動詞 register。"),
        ("A", "will + 原形動詞 make。"),
        ("B", "to be + p.p. 被動 inspected。"),
        ("B", "修飾動詞 grew 用副詞 steadily。"),
        ("B", "有逗號的非限定子句，先行詞是物，用 which。"),
        ("B", "修飾過去分詞 organized 用副詞 properly。"),
        ("B", "has been + p.p. 被動 appointed。"),
        ("C", "was + p.p. 被動 initiated。"),
        ("C", "Should you = If you 正式條件句。"),
        ("B", "on the second floor，樓層用 on。"),
        ("D", "截止日延長了；儘管如此，團隊仍應努力。用 nevertheless。"),
    ]

    pdf.set_font("chi", "", 9)
    for i, (ans, expl) in enumerate(mock_p5_ans, 1):
        if pdf.get_y() > 268:
            pdf.add_page()
        pdf.set_font("chi", "B", 9)
        pdf.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("chi", "", 9)
        pdf.multi_cell(0, 5, f"   {expl}")
        pdf.ln(1)

    pdf.ln(3)
    pdf.sub_title("Part 6 Answers:")
    mock_p6_ans = [
        ("C", "(31) were + p.p./形容詞，impressed（印象深刻的）。"),
        ("A", "(32) pleased to + 原形動詞 inform。"),
        ("D", "(33) including 表示「包括」。"),
        ("B", "(34) 前面在談入職細節，後面要求聯繫HR，所以插入句應提到開始日期。"),
        ("C", "(35) will be + p.p. 被動 conducted。"),
        ("B", "(36) remain + 形容詞 operational（可使用的）。"),
        ("A", "(37) be aware that... 意識到。"),
        ("C", "(38) 文末感謝語最合適。"),
    ]

    for i, (ans, expl) in enumerate(mock_p6_ans, 31):
        if pdf.get_y() > 268:
            pdf.add_page()
        pdf.set_font("chi", "B", 9)
        pdf.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("chi", "", 9)
        pdf.multi_cell(0, 5, f"   {expl}")
        pdf.ln(1)

    pdf.ln(3)
    pdf.sub_title("Part 7 Answers:")
    mock_p7_ans = [
        ("C", "March 10 到 June 30 約四個月。"),
        ("B", "文中提到 every 10 minutes。"),
        ("B", "文中提到 receive a 20% discount on all bus services。"),
        ("B", "文中提到 running from Central Park to the Business District via Main Street。"),
        ("A", "文中提到 SETUP: Sunday, April 20。"),
        ("B", "文中提到 Two exhibitor badges。"),
        ("B", "文中提到 submit your booth design for approval by April 10。"),
        ("C", "Tuesday 3:00 p.m. 是 Product Innovation Awards ceremony。"),
        ("B", "文中提到 Wednesday 3:00 p.m. Exhibition closes to visitors。"),
        ("D", "Printed marketing materials 未列在包含項目中。"),
        ("B", "文中提到 Keynote by Dr. Sarah Kim。"),
        ("C", "Thursday, April 24, from 8:00 a.m. to 12:00 p.m.，最晚是週四中午。"),
        ("C", "文中提到 pledging to invest NT$50 billion。"),
        ("C", "文中提到 power approximately 500,000 homes。"),
        ("C", "文中提到 generating 20% of its electricity from renewable sources by 2030。"),
        ("C", "文中提到 Taiwan should aim for 30% renewable energy by 2030。"),
    ]

    for i, (ans, expl) in enumerate(mock_p7_ans, 1):
        if pdf.get_y() > 268:
            pdf.add_page()
        pdf.set_font("chi", "B", 9)
        pdf.cell(0, 6, f"{i}. ({ans})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("chi", "", 9)
        pdf.multi_cell(0, 5, f"   {expl}")
        pdf.ln(1)

    # Final encouragement
    pdf.add_page()
    pdf.section_title("Final Notes 考前叮嚀")
    pdf.grammar_block("""## 考試當天注意事項

## 1. 考前準備
帶好證件（身分證 + 准考證）
帶鉛筆和橡皮擦（2B鉛筆）
提前到達考場

## 2. 時間分配 (Reading Section: 75 分鐘)
Part 5: 30題 — 10分鐘（每題20秒）
Part 6: 16題 — 10分鐘（每題40秒）
Part 7: 54題 — 55分鐘

## 3. 答題技巧
不確定的題目先標記，回頭再做
不要在一題上花太多時間
全部都要作答（沒有倒扣）
先做有把握的題目

## 4. 你已經準備好了！
經過13週的訓練，你已經：
學習了975個核心單字
練習了超過300題 Part 5 題目
閱讀了超過20篇文章
掌握了10大文法主題

相信自己，你一定可以達到 550+ 的目標！加油！""")

    path = os.path.join(OUTPUT_DIR, "week13.pdf")
    pdf.output(path)
    print(f"  [OK] {path}")


WEEK_BUILDERS = [week01, week02, week03, week04, week05, week06, week07, week08, week09, week10, week11, week12, week13]

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating TOEIC Weekly Study PDFs...")
    for fn in WEEK_BUILDERS:
        fn()
    print(f"\nDone! Generated {len(WEEK_BUILDERS)} PDFs in {OUTPUT_DIR}")
