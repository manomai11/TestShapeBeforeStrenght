import random

BALANCED_SHAPES = {
    "4333","3433","3343","3334",
    "4432","4423","4342","4243",
    "4324","4234","3442","2443",
    "3424","2434","3244","2344",
    "5332","5323","5233",
    "3532","3523","2533",
    "3352","3253","2353",
    "3325","3235","2335"
}

SPECIAL_D4C5 = {
    "4045", "0445", "3145", "1345", "2245"
}

# ฟังก์ชันสุ่มแจกไพ่ 1 มือ (จำลอง HCP และ Shape 4 ตัวรวมกันได้ 13)
def generate_random_hand():
    # สุ่ม Shape ให้ผลรวมความยาวไพ่เท่ากับ 13
    while True:
        s = random.randint(0, 7)
        h = random.randint(0, 7 - s)
        d = random.randint(0, 13 - s - h)
        c = 13 - s - h - d
        if max(s, h, d, c) <= 9: # ป้องกันแจกไพ่กองเดียวเกินจริง
            shape = f"{s}{h}{d}{c}"
            break
            
    # สุ่ม HCP ตั้งแต่ 0 ถึง 25
    hcp = random.randint(0, 25)
    return hcp, shape

# สร้างโจทย์ 20 ข้อที่ไม่ซ้ำกันสำหรับแต่ละโหมด
def generate_practice_questions(mode, total=20):
    questions = []
    seen = set()
    
    while len(questions) < total:
        hcp, shape = generate_random_hand()
        is_bal = shape in BALANCED_SHAPES
        
        # หาคำตอบที่ถูกต้องตาม Mode ที่เลือก
        if mode == "resp_1c":
            ans = response_1c(hcp, shape, balanced=is_bal)
        elif mode == "resp_1d":
            ans = response_1d(hcp, shape, balanced=is_bal)
        elif mode == "opening":
            # ตัวอย่างเปิด (สามารถปรับเรียกฟังก์ชัน Opening ของคุณได้)
            ans = "1C" if hcp >= 12 else "PASS"
        else:
            ans = "1N"
            
        # กรองเอาเฉพาะมือที่มีคำตอบสมเหตุสมผล หรือสุ่มได้หลากหลาย
        key = f"{hcp}_{shape}"
        if key not in seen:
            seen.add(key)
            questions.append({
                "hcp": hcp,
                "shape": shape,
                "balanced": is_bal,
                "correct_answer": ans
            })
            
    return questions

# (ฟังก์ชัน response_1c และ response_1d ที่มีอยู่เดิมของคุณ ใส่ไว้ที่นี่เช่นเดิม)
