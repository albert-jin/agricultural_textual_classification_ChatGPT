import json


"""
"""
def trans_txt(inp1_file, inp2_file, ratio=10):
    # positive, negative => 1, 0
    # './pos.json', './neg.json'
    # './train.json', './test.json'
    stats = {'negative': 0, "positive": 0,'neg_train':0,'pos_train':0,'neg_test':0,'pos_test':0}
    with open(inp1_file, mode='rt', encoding='utf-8') as inp_pos, open(inp2_file, mode='rt', encoding='utf-8') as inp_neg:
        lines_pos = inp_pos.readlines()
        lines_neg = inp_neg.readlines()
        def filter_(str_):
            return len(str_.split(' ')) > 5
        lines_pos = list(filter(filter_, lines_pos))
        lines_neg = list(filter(filter_, lines_neg))
    with open('./pos.json', mode='wt', encoding='utf-8') as oup_pos, open('./neg.json', mode='wt', encoding='utf-8') as oup_neg:
        for line_pos in lines_pos:
            json_row = {"text": line_pos.replace('\n', ',').replace('\r', ','), "label": 1}
            oup_pos.write(json.dumps(json_row, ensure_ascii=False) + '\n')
            stats['positive'] += 1
        for line_neg in lines_neg:
            json_row = {"text": line_neg.replace('\n', ',').replace('\r', ','), "label": 0}
            oup_neg.write(json.dumps(json_row, ensure_ascii=False) + '\n')
            stats['negative'] += 1
    with open('./train.json', mode='wt', encoding='utf-8') as oup_train, open('./test.json', mode='wt', encoding='utf-8') as oup_test:
        over_count = 0
        for line_pos in lines_pos:
            json_row = {"text": line_pos.replace('\n', ',').replace('\r', ','), "label": 1}
            if over_count < int(stats['positive']*(ratio-1)/ratio):
                oup_train.write(json.dumps(json_row, ensure_ascii=False) + '\n')
                stats['pos_train'] += 1
            else:
                oup_test.write(json.dumps(json_row, ensure_ascii=False) + '\n')
                stats['pos_test'] += 1
            over_count += 1
        over_count = 0
        for line_neg in lines_neg:
            json_row = {"text": line_neg.replace('\n', ',').replace('\r', ','), "label": 0}
            if over_count < int(stats['negative']*(ratio-1)/ratio):
                oup_train.write(json.dumps(json_row, ensure_ascii=False) + '\n')
                stats['neg_train'] += 1
            else:
                oup_test.write(json.dumps(json_row, ensure_ascii=False) + '\n')
                stats['neg_test'] += 1
            over_count +=1
    print(f'数据集类别占比统计{stats}')

if __name__ == '__main__':
    trans_txt('./pos.txt', './neg.txt')
