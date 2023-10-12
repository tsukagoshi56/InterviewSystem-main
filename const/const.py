# 影響範囲: dialogue_act_estimation, concept_extraction, frame

body_head = ["頭", "あたま", "頭部", "後頭部", "頭頂部", "前頭部", "側頭部", "こめかみ"]
body_stomach = ["おなか", "お腹", "腹", "はら"]
body_chest = ["胸", "胸部", "心臓"]
body_limbs = ["手", "右手", "左手", "両手", "足", "右足",
              "左足", "両足", "手足", "腕", "右腕", "左腕", "両腕"]
body_back = ["背中", "後ろ"]

body_detail_head = []
body_detail_stomach = ["下腹部", "上腹部", "みぞおち", "脇腹"]
body_detail_chest = []
body_detail_limbs = []

parts = ["全体", "右", "左", "上", "下"]

verb = ["痛い", "痛み", "痛む", "ズキズキする", "ジンジンする",
        "痺れる", "痺れ", "動かない",
        "腫れて",
        "締め付けられる"]

noun = ["痛み",
        "痺れ",
        "腫れ",
        "締め付け",
        "違和感"]

headache = ["頭痛がする"]
stomachache = ["腹痛がする"]
breath = [
    "呼吸ができない", "呼吸がしづらい", "息が苦しい",
    "息ができない", "息がしづらい", "息が苦しい",
    "息切れがする", "ゼーゼーする"
]
cough = [
    "咳が出る", "咳が止まらない",
    "痰が出る", "ゴホゴホする", "コンコンする",
]
heartburn = ["胸焼けがする", "胃がムカムカする"]


body = body_head + body_chest + body_stomach + body_limbs + body_back
body_detail = body_detail_head + body_detail_chest + body_detail_stomach

ex_head = body_head + body_detail_head
ex_chest = body_chest + body_detail_chest
ex_stomach = body_stomach + body_detail_stomach
ex_limbs = body_limbs
ex_back = body_back


# Aです
ex_symptoms = ['頭痛', '腹痛', '胸焼け', '息切れ', '呼吸困難', '耳鳴り', '動悸']


# 息、咳など
substance = ['咳', '呼吸', '息', '鼻水', '便', '下痢', 'ウンチ']
s_verb = ['止まらない', '辛い']

# どんな時に
# when = '立ち上がった時', '力を入れるとき']
# いつから
# fromwhen = ['今日', '昨日', '先週', '一日前']
