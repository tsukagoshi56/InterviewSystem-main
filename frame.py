from const import const
from da_concept_extractor import DA_Concept


class FrameController:
    def __init__(self):
        # 対話行為タイプとコンセプトの推定器
        self.da_concept = DA_Concept()
        # フレーム
        self.frame = {
            'body': "",
            'body_parts': "",
            'symptoms': "",
            'detailed': False,
            'fever': "",
            'parrot_query': "",
        }
        # self.test_frame = {
        #     'body': "",
        #     'body_parts': "",
        #     'symptoms': [
        #         {
        #             'type': "",
        #             'slot1': "",
        #             'slot2': ""
        #         },
        #         {
        #             'type': "",
        #             'slot1': "",
        #             'slot2': ""
        #         },
        #     ],
        #     'detailed': False,
        #     'fever': "",
        #     'parrot_query': "",
        # }

    # 発話から得られた情報をもとにフレームを更新
    def update(self, user_utt):
        da, conceptdic = self.da_concept.process(user_utt)

        # 値の整合性を確認し，整合しないものは空文字にする
        conceptdic = self.__consistency_check(conceptdic)

        # da と concept の整合性を確認
        if not self.__sufficiency_check(da, conceptdic):
            return self.frame, False

        tmp = ""
        if da == "body-symptoms-verb":
            self.frame['body'] = conceptdic['body']
            self.frame['symptoms'] = conceptdic['verb']
        elif da == "body-symptoms-noun":
            self.frame['body'] = conceptdic['body']
            self.frame['symptoms'] = conceptdic['noun']
        elif da == "body-symptoms-detail-verb":
            self.frame['detailed'] = True
            self.frame['body'] = conceptdic['body']
            self.frame['symptoms'] = conceptdic['verb']
            if 'parts' in conceptdic.keys():
                self.frame['body_parts'] = conceptdic['parts']
        elif da == "body-symptoms-detail-noun":
            self.frame['detailed'] = True
            self.frame['body'] = conceptdic['body']
            self.frame['symptoms'] = conceptdic['noun']
            if 'parts' in conceptdic.keys():
                self.frame['body_parts'] = conceptdic['parts']
        elif da == 'add-detail' and self.frame['body'] != "":
            self.frame['detailed'] = True
            self.frame['body_parts'] = conceptdic['parts']
            self.frame['parrot_query'] = self.frame['body'] + \
                self.frame['body_parts'] + self.frame['symptoms']
        elif da == 'temperture':
            self.frame['fever'] = user_utt
        elif da == 'other-symptoms':
            if 'body' in conceptdic.keys():
                self.frame['body'] = conceptdic['body']
            self.frame['symptoms'] = user_utt
            self.frame['parrot_query'] = user_utt

        if da in ["body-symptoms-verb", "body-symptoms-noun", "body-symptoms-detail-verb", "body-symptoms-detail-noun"]:
            for v in conceptdic.values():
                tmp += v
            self.frame['parrot_query'] = tmp

        # elif da == "initialize":
        #     frame = {"place": "", "date": "", "type": ""}
        # elif da == "correct-info":
        #     for k,v in conceptdic.items():
        #         if frame[k] == v:
        #             frame[k] = ""

        return self.frame, True

    # 値の整合性を確認し，整合しないものは空文字にする
    def __consistency_check(self, conceptdic):
        for k, v in conceptdic.items():
            if k == 'body' and v not in const.body + ["腹痛"]:
                conceptdic['body'] = ""
            elif k == 'body_detail' and v not in const.body_detail:
                conceptdic['body_detail'] = ""
            elif k == 'parts' and v not in const.parts:
                conceptdic['parts'] = ""
            elif k == 'verb' and v not in const.verb:
                conceptdic['verb'] = ""
            elif k == 'noun' and v not in const.noun:
                conceptdic['noun'] = ""
        return conceptdic

    # da と concept の整合性を確認
    def __sufficiency_check(self, da, c):
        if da == "body-symptoms-verb" and ('body' not in c or 'verb' not in c):
            return False
        elif da == "body-symptoms-noun" and ('body' not in c or 'noun' not in c):
            return False
        elif da == "body-symptoms-detail-verb" and (('body' not in c or 'parts' not in c) and 'body_detail' not in c and 'verb' not in c):
            return False
        elif da == "body-symptoms-detail-noun" and (('body' not in c or 'parts' not in c) and 'body_detail' not in c and 'noun' not in c):
            return False
        elif da == 'add-detail' and 'parts' not in c:
            return False
        return True
