import json


def trans_txt2json(inp_file):
    # ['农业经济', '农业工程', '水产渔业', '养殖技术', '林业', '园艺', '农作物'] => 0, 1, 2, 3, 4, 5, 6.
    # './train.json', './test.json'
    stats = {'农业经济': 0, "农业工程": 0,'水产渔业':0,'养殖技术':0,'林业':0,'园艺':0,'农作物':0}
    list_stats = list(stats)
    with open(inp_file, mode='rt', encoding='utf-8') as inp, open(f'./{inp_file.split(".")[1][1:]}.json', mode='wt', encoding='utf-8') as oup:
        lines = inp.readlines()
        for line in lines:
            splitter_data = line.strip().split('\t')
            if len(splitter_data) != 2:
                continue
            sent, category = splitter_data[0].strip(), splitter_data[1].strip()
            if category not in stats:
                continue
            json_row = {"text": sent, "category": category, "label": list_stats.index(category)}
            oup.write(json.dumps(json_row, ensure_ascii=False) + '\n')
            stats[category] += 1
        print('数据集统计: ', stats)


if __name__ == '__main__':
    trans_txt2json('./train.txt')
    trans_txt2json('./test.txt')
