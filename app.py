import random
import ipywidgets as widgets
from IPython.display import display, clear_output

USER_DATABASE = {}

HCP_MAP = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
RANK_ORDER = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

def evaluate_hand(hand):
    counts = {'S': 0, 'H': 0, 'D': 0, 'C': 0}
    hcp = 0
    suit_cards = {'S': [], 'H': [], 'D': [], 'C': []}
    
    for card in hand:
        rank = card[0]
        suit = card[1]
        counts[suit] += 1
        suit_cards[suit].append(rank)
        if rank in HCP_MAP:
            hcp += HCP_MAP[rank]
            
    for suit in suit_cards:
        suit_cards[suit].sort(key=lambda r: RANK_ORDER[r], reverse=True)
            
    shape = [counts['S'], counts['H'], counts['D'], counts['C']]
    return hcp, shape, counts, suit_cards

def is_balanced(shape):
    s = sorted(shape, reverse=True)
    return s in [[4, 3, 3, 3], [4, 4, 3, 2], [5, 3, 3, 2]]

def has_honor(cards):
    return any(r in ['A', 'K', 'Q'] for r in cards)

def match_shape_new(shape, pattern_str):
    s, h, d, c = shape
    parts = pattern_str.strip().split()
    if parts[0] == "any":
        target_counts = sorted([int(x) for x in parts[1]])
        actual_counts = sorted(shape)
        return target_counts == actual_counts
    else:
        target_tuple = tuple(int(x) for x in pattern_str.strip())
        return tuple(shape) == target_tuple

def has_second_suit_greater_than_4(shape, primary_suit_idx):
    for idx, length in enumerate(shape):
        if idx != primary_suit_idx and length > 4:
            return True
    return False

def has_second_suit_5plus(shape, primary_suit_idx):
    for idx, length in enumerate(shape):
        if idx != primary_suit_idx and length >= 5:
            return True
    return False

# --- ฟังก์ชันกฎ Opening ที่แก้ไขการ return ให้ถูกต้องครบถ้วน ---
def logic_opening(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    
    def is_solid(suit_name, suit_idx):
        cards = suit_cards[suit_name]
        if len(cards) >= 7:
            honors = [card for card in cards if card in ['A', 'K', 'Q', 'J', 'T']]
            if len(honors) >= min(len(cards)-1, 5):
                if not has_second_suit_5plus(shape, suit_idx):
                    return True
        return False

    if 5 <= hcp <= 10:
        if c >= 8 and not has_second_suit_5plus(shape, 3): return "4C", "5-10 HCP, C=8"
        if d >= 8 and not has_second_suit_5plus(shape, 2): return "4D", "5-10 HCP, D=8"
        if h >= 8 and not has_second_suit_5plus(shape, 1): return "4H", "5-10 HCP, H=8"
        if s >= 8 and not has_second_suit_5plus(shape, 0): return "4S", "5-10 HCP, S=8"

    if is_solid('H', 1): return "3N", "Solid H7+"
    if is_solid('S', 0): return "3N", "Solid S7+"

    if 5 <= hcp <= 10:
        if c == 7 and not has_second_suit_greater_than_4(shape, 3): return "3C", "C=7"
        if d == 7 and not has_second_suit_greater_than_4(shape, 2): return "3D", "D=7"
        if h == 7 and not has_second_suit_5plus(shape, 1): return "3H", "H=7"
        if s == 7 and not has_second_suit_5plus(shape, 0): return "3S", "S=7"

    if 11 <= hcp <= 13:
        if h == 6 and not has_second_suit_5plus(shape, 1): return "2H", "H=6"
        if s == 6 and not has_second_suit_5plus(shape, 0): return "2S", "S=6"

    if 11 <= hcp <= 20:
        if (s, h, d, c) == (4, 4, 1, 4): return "1C", "Shape 4414"
        elif (4 in shape) and shape.count(4) == 3 and shape.count(1) == 1:
            return "1D", "Shape 4-4-4-1"

    if 11 <= hcp <= 20 and (match_shape_new(shape, "4144") or match_shape_new(shape, "1444")):
        return "1D", "4144 or 1444"
    if 11 <= hcp <= 15 and d == 4 and c == 5:
        return "1D", "D=4, C=5"

    if hcp < 11: return "Pass", "<11 HCP"
    
    if hcp >= 21:
        if 20 <= hcp <= 22 and is_balanced(shape): return "2N", "20-22 Balanced"
        return "2C", "21+ HCP"
    if 20 <= hcp <= 22 and is_balanced(shape): return "2N", "20-22 Balanced"
    
    if 11 <= hcp <= 20:
        if s == 5 and h == 5: return "1S", "5-5 Major, S > H"
        if s == 5 and d == 5: return "1S", "5-5 S and D, S > D"
        if s == 5 and c == 5: return "1S", "5-5 S and C, S > C"
        if h == 5 and d == 5: return "1H", "5-5 H and D, H > D"
        if h == 5 and c == 5: return "1H", "5-5 H and C, H > C"
        if d == 5 and c == 5: return "1D", "5-5 Minor, D > C"
        
        suits_len = [('S', s), ('H', h), ('D', d), ('C', c)]
        long_suits = [item for item in suits_len if item[1] >= 5]
        if len(long_suits) >= 2:
            order = {'S': 4, 'H': 3, 'D': 2, 'C': 1}
            long_suits.sort(key=lambda x: (x[1], order[x[0]]), reverse=True)
            best_suit = long_suits[0][0]
            mapping = {'S': '1S', 'H': '1H', 'D': '1D', 'C': '1C'}
            return mapping[best_suit], f"Two suits, longer suit {best_suit}"

    if 17 <= hcp <= 20 and s >= 5 and h >= 5: return "2D", "M55+"
    if 11 <= hcp <= 13 and is_balanced(shape): return "1C", "Balanced"
    if 14 <= hcp <= 16 and is_balanced(shape): return "1N", "Balanced"
    if 17 <= hcp <= 19 and is_balanced(shape) and s < 5 and h < 5: return "1C", "Balanced"
    
    if 11 <= hcp <= 20 and c >= 5 and c >= s and c >= h: return "1C", "C5+"
    if 11 <= hcp <= 20 and d >= 5: return "1D", "D5+"
    if 11 <= hcp <= 16 and s >= 5: return "1S", "S5+"
    if 17 <= hcp <= 20 and s >= 5: return "1S", "S5+"
    if 11 <= hcp <= 16 and h >= 5: return "1H", "H5+"
    if 17 <= hcp <= 20 and h >= 5: return "1H", "H5+"
    
    return "Pass", "Pass"

# --- ฟังก์ชันกฎ Resp_1N, 1C, 1D, 1H, 1S ---
def logic_resp_1n(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    has_M5 = (s >= 5 or h >= 5)
    has_m6 = (d >= 6 or c >= 6)
    has_m55 = (d >= 5 and c >= 5)
    has_M55 = (s >= 5 and h >= 5)
    if hcp >= 11 and (s == 3 and h == 1 and ((d == 5 and c == 4) or (d == 4 and c == 5))): return "3H", "3154/3145"
    if hcp >= 11 and (s == 1 and h == 3 and ((d == 5 and c == 4) or (d == 4 and c == 5))): return "3S", "1354/1345"
    if hcp <= 8 and s < 5 and h < 5 and d < 6 and c < 6 and not has_m55: return "Pass", "Pass"
    if 7 <= hcp <= 8 and (has_M55 or (has_M5 and (d >= 5 or c >= 5))): return "2C", "M55 or M5m5"
    if hcp == 9 and d < 6 and c < 6 and not has_m55: return "2C", "9 HCP"
    if hcp == 10 and s < 5 and h < 5 and d < 6 and c < 6 and not has_m55: return "2C", "10 HCP"
    if hcp >= 16 and s < 5 and h < 5 and d < 6 and c < 6 and not has_m55: return "2C", "16+ HCP"
    if 11 <= hcp <= 15 and ((2 < s < 5) or (2 < h < 5)): return "3C", "3-card Major support"
    return "Pass", "Default Pass"

def logic_resp_1c(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    has_M4 = (s >= 4 or h >= 4)
    has_m6 = (d >= 6 or c >= 6)
    has_m55 = (d >= 5 and c >= 5)
    def check_bal_dbl():
        if is_balanced(shape):
            for st, cards in suit_cards.items():
                if len(cards) == 2 and not has_honor(cards): return False
            return True
        return False
    if hcp <= 5 and c >= 4 and c > s and c > h and c > d: return "Pass", "Pass"
    if h >= 4 and s >= 4: return "1D", "H4S4"
    if h >= 4 and h > s: return "1D", "H4+ H>S"
    if s >= 4 and s >= h and not (s == 4 and h == 4): return "1H", "S4+, S>=H"
    if 5 <= hcp <= 10 and has_m55: return "2S", "m55"
    if 5 <= hcp <= 10 and c >= 6: return "3C", "C6+"
    if 0 <= hcp <= 10 and d >= 6 and not has_M4: return "2C", "D6 no M4"
    if 11 <= hcp <= 12 and d >= 5 and not has_M4: return "2C", "D5 no M4"
    if 11 <= hcp <= 12 and c >= 5 and s < 4 and h < 4: return "2D", "C5+ M<4"
    if 11 <= hcp <= 12 and is_balanced(shape) and s < 4 and h < 4 and d < 5 and c < 5: return "2H", "Balanced"
    if 5 <= hcp <= 10 and s < 4 and h < 4 and not has_m6 and not has_m55: return "1S", "M<4"
    if hcp >= 13 and s < 4 and h < 4: return "1N", "13+ M<4"
    if hcp >= 13 and (s == 4 or h == 4) and check_bal_dbl(): return "1N", "13+ 4M Balanced"
    return "Pass", "Pass"

def logic_resp_1d(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    def check_bal_dbl():
        if is_balanced(shape):
            for st, cards in suit_cards.items():
                if len(cards) == 2 and not has_honor(cards): return False
            return True
        return False
    if hcp <= 5: return "Pass", "Pass"
    if hcp >= 5 and h >= 4 and h > s and not (h == 4 and s == 4): return "1H", "H4+ H>S"
    if hcp >= 5 and s >= 4 and s >= h and not (h == 4 and s == 4): return "1S", "S4+ S>=H"
    if hcp >= 13 and s < 4 and h < 4: return "1N", "13+ M<4"
    if hcp >= 13 and (h == 4 or s == 4) and check_bal_dbl(): return "1N", "13+ 4M Balanced"
    if 5 <= hcp <= 10 and c == 5 and s < 4 and h < 4 and d < 3: return "2C", "C=5"
    if 5 <= hcp <= 10 and c >= 6 and s < 4 and h < 4 and d < 4: return "2C", "C6+"
    if 5 <= hcp <= 10 and 3 <= d <= 4 and s < 4 and h < 4: return "2D", "D 3-4"
    if 11 <= hcp <= 12 and is_balanced(shape) and s < 4 and h < 4: return "2H", "Balanced"
    if 11 <= hcp <= 12 and c >= 5 and not is_balanced(shape) and s < 4 and h < 4: return "2S", "C5+ Unbalanced"
    if 11 <= hcp <= 12 and d >= 4 and not is_balanced(shape) and s < 4 and h < 4: return "3C", "D4+ Unbalanced"
    if 5 <= hcp <= 10 and d == 5 and s < 4 and h < 4: return "3D", "D=5"
    return "Pass", "Pass"

def logic_resp_1h(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    def is_3433(shp): return sorted(shp, reverse=True) == [4, 3, 3, 3] and shp[1] == 4
    def has_shg(shp, mx=0): return any(l <= mx for l in shp)
    if hcp >= 13 and h >= 4 and s < 2: return "3S", "H4+ S<2"
    if hcp >= 13 and h >= 4 and c < 2: return "3N", "H4+ C<2"
    if hcp >= 13 and h >= 4 and d < 2: return "4C", "H4+ D<2"
    if hcp >= 13 and h >= 4 and has_shg(shape, 0): return "3D", "Void"
    if hcp >= 13 and h == 3 and has_shg(shape, 1): return "2D", "H=3 Shortage"
    if hcp >= 13: return "2C", "13+ Any"
    has_ace = any(r == 'A' for r in suit_cards['H'])
    if 4 <= hcp <= 5 and h == 4 and has_ace and not is_3433(shape): return "3H", "H=4 Ace"
    if hcp <= 5 and h == 4 and not is_3433(shape): return "3D", "H=4"
    if 11 <= hcp <= 12 and s >= 5 and h < 4: return "1N", "S5+"
    if 10 <= hcp <= 12 and h == 3: return "2D", "H=3"
    if hcp <= 5 and h < 4: return "Pass", "Pass"
    if 5 <= hcp <= 12 and s < 5 and h < 3: return "1S", "S<5 H<3"
    if 5 <= hcp <= 10 and s == 5 and h < 3: return "1N", "S=5"
    if 5 <= hcp <= 10 and s >= 6 and h < 2: return "2S", "S>=6"
    if 5 <= hcp <= 10 and s >= 7 and h < 3: return "1N", "S>=7"
    if 5 <= hcp <= 9 and (h == 3 or is_3433(shape)): return "2H", "H=3 or 3433"
    if 10 <= hcp <= 12 and h >= 4 and has_shg(shape, 1): return "2N", "H4+ Shortage"
    if 8 <= hcp <= 12 and h >= 4 and not has_shg(shape, 1): return "3C", "H4+"
    if 6 <= hcp <= 7 and h == 4 and not is_3433(shape): return "3H", "H=4"
    if 5 <= hcp <= 10 and h == 4 and has_shg(shape, 1): return "4H", "H=4 Shortage"
    if 5 <= hcp <= 10 and h >= 5: return "4H", "H5+"
    return "Pass", "Pass"

def logic_resp_1s(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    def is_4333(shp): return sorted(shp, reverse=True) == [4, 3, 3, 3] and shp[0] == 4
    def has_shg(shp, mx=0): return any(l <= mx for l in shp)
    if hcp >= 13 and s >= 4 and s == 1: return "3H", "S4+ S=1"
    if hcp >= 13 and s >= 4 and c == 1: return "3N", "S4+ C=1"
    if hcp >= 13 and s >= 4 and d == 1: return "4C", "S4+ D=1"
    if hcp >= 13 and s >= 4 and has_shg(shape, 0): return "3D", "Void"
    if hcp >= 13 and s == 3 and has_shg(shape, 1): return "2H", "S=3 Shortage"
    if hcp >= 13: return "2C", "13+ Any"
    has_ace = any(r == 'A' for r in suit_cards['S'])
    if 4 <= hcp <= 5 and s == 4 and has_ace and not is_4333(shape): return "3S", "S=4 Ace"
    if hcp <= 5 and s == 4 and not is_4333(shape): return "3D", "S=4"
    if 11 <= hcp <= 12 and s < 3 and h < 5: return "1N", "S<3 H<5"
    if 10 <= hcp <= 12 and s == 3: return "2H", "S=3"
    if hcp <= 5 and s < 4: return "Pass", "Pass"
    if 5 <= hcp <= 10 and s < 3 and h < 6: return "1N", "S<3 H<6"
    if 6 <= hcp <= 10 and h >= 6 and s < 3: return "2D", "H6+"
    if 11 <= hcp <= 12 and h >= 5 and s < 4: return "2D", "H5+"
    if 5 <= hcp <= 9 and (s == 3 or is_4333(shape)): return "2S", "S=3"
    if 10 <= hcp <= 12 and s >= 4 and has_shg(shape, 1): return "2N", "S4+ Shortage"
    if 8 <= hcp <= 12 and s >= 4 and not has_shg(shape, 1): return "3C", "S4+"
    if 6 <= hcp <= 7 and s == 4 and not is_4333(shape): return "3S", "S=4"
    if 5 <= hcp <= 9 and s == 4 and has_shg(shape, 1): return "4S", "S=4 Shortage"
    if hcp <= 9 and s >= 5: return "4S", "S5+"
    return "Pass", "Pass"

# --- แอปพลิเคชันหลัก ---
class MasterBridgeQuizApp:
    def __init__(self):
        self.current_user = None
        self.current_score = 0
        self.current_question = 1
        
        self.username_input = widgets.Text(description='ชื่อผู้ใช้:', placeholder='กรอกชื่อของคุณ')
        self.login_btn = widgets.Button(description='เข้าสู่ระบบ', button_style='primary')
        self.login_btn.on_click(self.handle_login)
        self.login_output = widgets.Output()
        
        self.login_page = widgets.VBox([
            widgets.HTML("<h2>🃏 ระบบฝึกทักษะบริดจ์ (Bridge Master Training)</h2>"),
            widgets.HBox([self.username_input, self.login_btn]),
            self.login_output
        ])
        
        self.btn_opening = widgets.Button(description='ฝึกเปิด (Opening)', button_style='info', layout=widgets.Layout(width='250px', height='40px'))
        self.btn_resp_1c = widgets.Button(description='ฝึกตอบ 1C opening', button_style='info', layout=widgets.Layout(width='250px', height='40px'))
        self.btn_resp_1d = widgets.Button(description='ฝึกตอบ 1D opening', button_style='info', layout=widgets.Layout(width='250px', height='40px'))
        self.btn_resp_1h = widgets.Button(description='ฝึกตอบ 1H opening', button_style='info', layout=widgets.Layout(width='250px', height='40px'))
        self.btn_resp_1s = widgets.Button(description='ฝึกตอบ 1S opening', button_style='info', layout=widgets.Layout(width='250px', height='40px'))
        self.btn_resp_1n = widgets.Button(description='ฝึกตอบ 1N opening', button_style='info', layout=widgets.Layout(width='250px', height='40px'))
        
        self.btn_opening.on_click(lambda b: self.start_quiz('opening', 'ฝึกเปิด (Opening)'))
        self.btn_resp_1c.on_click(lambda b: self.start_quiz('resp_1c', 'ฝึกตอบ 1C opening'))
        self.btn_resp_1d.on_click(lambda b: self.start_quiz('resp_1d', 'ฝึกตอบ 1D opening'))
        self.btn_resp_1h.on_click(lambda b: self.start_quiz('resp_1h', 'ฝึกตอบ 1H opening'))
        self.btn_resp_1s.on_click(lambda b: self.start_quiz('resp_1s', 'ฝึกตอบ 1S opening'))
        self.btn_resp_1n.on_click(lambda b: self.start_quiz('resp_1n', 'ฝึกตอบ 1N opening'))
        
        self.menu_page = widgets.VBox([
            widgets.HTML("<h3>📂 กรุณาเลือกหัวข้อแบบฝึกหัด (เซ็ตละ 20 ข้อ)</h3>"),
            self.btn_opening, self.btn_resp_1c, self.btn_resp_1d, 
            self.btn_resp_1h, self.btn_resp_1s, self.btn_resp_1n
        ])
        
        self.stats_label = widgets.HTML("<b>ผู้เล่น: - | โหมด: -</b>")
        self.back_to_menu_btn = widgets.Button(description='⬅️ กลับหน้าเมนู', button_style='warning')
        self.back_to_menu_btn.on_click(self.go_to_menu)
        
        self.output_area = widgets.Output()
        
        self.next_btn = widgets.Button(
            description='ข้อต่อไป (Next) ➡️', 
            button_style='success',
            layout=widgets.Layout(width='200px', height='60px')
        )
        self.next_btn.on_click(self.load_new_hand)
        
        self.score_summary_label = widgets.HTML("<b>คะแนน: 0 / 0</b>")
        self.feedback_area = widgets.Output()
        
        right_panel = widgets.VBox([
            self.score_summary_label,
            widgets.HTML("<br>"),
            self.next_btn,
            widgets.HTML("<br><b>ผลการตรวจคำตอบ:</b>"),
            self.feedback_area
        ], layout=widgets.Layout(padding='0px 0px 0px 20px'))
        
        self.keypad_box = self.create_keypad()
        
        self.quiz_page = widgets.VBox([
            widgets.HBox([self.stats_label, widgets.HTML("&nbsp;&nbsp;|&nbsp;&nbsp;"), self.back_to_menu_btn]),
            widgets.HTML("<hr>"),
            widgets.HBox([
                widgets.VBox([
                    self.output_area,
                    widgets.HTML("<b>เลือกคำตอบ Bidding:</b>"),
                    self.keypad_box
                ]),
                right_panel
            ])
        ])
        
        self.container = widgets.VBox([self.login_page])

    def create_keypad(self):
        levels = ['1', '2', '3', '4', '5', '6', '7']
        suits_list = ['C', 'D', 'H', 'S', 'N']
        rows = []
        for lvl in levels:
            row_btns = []
            for s in suits_list:
                bid_str = lvl + s
                btn = widgets.Button(description=bid_str, layout=widgets.Layout(width='45px', height='32px'))
                btn.on_click(lambda b, val=bid_str: self.check_answer(val))
                row_btns.append(btn)
            rows.append(widgets.HBox(row_btns))
            
        pass_btn = widgets.Button(description='Pass', layout=widgets.Layout(width='75px', height='32px'), button_style='info')
        pass_btn.on_click(lambda b: self.check_answer('Pass'))
        rows.append(widgets.HBox([pass_btn]))
        return widgets.VBox(rows)

    def handle_login(self, b):
        uname = self.username_input.value.strip()
        if not uname:
            with self.login_output:
                clear_output()
                print("⚠️ กรุณากรอกชื่อผู้ใช้ก่อนเข้าสู่ระบบ")
            return
        self.current_user = uname
        self.container.children = [self.menu_page]

    def go_to_menu(self, b):
        self.container.children = [self.menu_page]

    def start_quiz(self, mode_key, mode_name):
        self.current_mode = mode_key
        self.current_mode_name = mode_name
        self.current_score = 0
        self.current_question = 1
        
        self.stats_label.value = f"<b>ผู้เล่น: {self.current_user} | หมวด: {self.current_mode_name}</b>"
        self.container.children = [self.quiz_page]
        self.load_new_hand(None)

    def load_new_hand(self, b):
        if self.current_question > 20:
            with self.output_area:
                clear_output(wait=False)
                print("==================================================")
                print(f"🎉 จบเซ็ตแบบฝึกหัด 20 ข้อแล้วครับ!")
                print(f"🏆 คะแนนรวมที่คุณทำได้: {self.current_score} / 20 คะแนน")
                print("==================================================")
            with self.feedback_area:
                clear_output(wait=False)
            self.score_summary_label.value = f"<b>คะแนนรวม: {self.current_score} / 20</b>"
            self.next_btn.description = 'จบเซ็ตแล้ว (เลือกเมนู)'
            self.next_btn.on_click(self.go_to_menu)
            return

        self.next_btn.description = 'ข้อต่อไป (Next) ➡️'
        self.next_btn.on_click(self.load_new_hand)

        with self.feedback_area:
            clear_output(wait=False)
            
        mode = self.current_mode
        suits = ['S', 'H', 'D', 'C']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        deck = [r + s for s in suits for r in ranks]
        
        while True:
            hand = random.sample(deck, 13)
            hcp, shape, counts, suit_cards = evaluate_hand(hand)
            
            if mode == 'opening':
                bid, reason = logic_opening(hcp, shape, counts, suit_cards)
                if bid == 'Pass': continue
            elif mode == 'resp_1c':
                bid, reason = logic_resp_1c(hcp, shape, counts, suit_cards)
            elif mode == 'resp_1d':
                bid, reason = logic_resp_1d(hcp, shape, counts, suit_cards)
            elif mode == 'resp_1h':
                bid, reason = logic_resp_1h(hcp, shape, counts, suit_cards)
            elif mode == 'resp_1s':
                bid, reason = logic_resp_1s(hcp, shape, counts, suit_cards)
            elif mode == 'resp_1n':
                bid, reason = logic_resp_1n(hcp, shape, counts, suit_cards)
            break
            
        self.correct_bid = bid
        self.reason = reason
        
        self.score_summary_label.value = f"<b>คะแนน: {self.current_score} / {self.current_question - 1}</b>"
        
        with self.output_area:
            clear_output(wait=False)
            print("==================================================")
            print(f"  ข้อที่ {self.current_question} จาก 20 ข้อ")
            print("==================================================")
            print(f"♠ S:  {'  '.join(suit_cards['S'])}")
            print(f"♥ H:  {'  '.join(suit_cards['H'])}")
            print(f"♦ D:  {'  '.join(suit_cards['D'])}")
            print(f"♣ C:  {'  '.join(suit_cards['C'])}")
            print("--------------------------------------------------")
            print(f"📊 HCP: {hcp}   |   ทรงไพ่ (Shape): {shape[0]}{shape[1]}{shape[2]}{shape[3]}")
            print("==================================================")

    def check_answer(self, user_bid):
        if self.current_question > 20: return
        
        is_correct = (user_bid == self.correct_bid)
        if is_correct:
            self.current_score += 1
            
        with self.feedback_area:
            clear_output(wait=False)
            if is_correct:
                print(f"✅ ถูกต้อง! คุณเลือกตอบ {user_bid}")
            else:
                print(f"❌ ผิด! คุณเลือกตอบ {user_bid} แต่คำตอบที่ถูกต้องคือ {self.correct_bid}")
            print(f"💡 เหตุผล: {self.reason}")

        self.score_summary_label.value = f"<b>คะแนน: {self.current_score} / {self.current_question}</b>"
        self.current_question += 1

app = MasterBridgeQuizApp()
display(app.container)
