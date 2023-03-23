import csv
import json
import os


"""
Tornado-数据集类别占比统计{'Others': 1056, 'Tornado': 2517} / 3572
Sandy-数据集类别占比统计{'Others': 697, 'Sandy': 1494} / 2190
Floods-数据集类别占比统计{'Others': 886, 'Floods': 2712} / 3597
Blizzard-数据集类别占比统计{'Others': 308, 'Blizzard': 3342} / 3649
Matthew-数据集类别占比统计{'Others': 1641, 'Matthew': 3564} / 5204
Hurricane-数据集类别占比统计{'Others': 3179, 'Hurricane': 4645} / 7823
Michael-数据集类别占比统计{'Others': 888, 'Michael': 3340} / 4227
Wildfires-数据集类别占比统计{'Others': 333, 'Wildfires': 4264} / 4596
Dorian-数据集类别占比统计{'Others': 1465, 'Dorian': 5676} / 7140

Process finished with exit code 0
"""
def trans_csv(inp_file, category):
    # non_category, category => 0, 1
    """
    将 2011Tornado_Summary.csv 转换成 Tornado.json
    :param inp_file: 2011Tornado_Summary.csv
    :param category: Tornado
    :return: Tornado.json
    """
    stats = {"Others":0, category:1}
    counts = 0
    with open(inp_file, mode='rt', encoding='utf-8') as inp, open(f'{category}.json', mode='wt', encoding='utf-8') as oup:
        reader = csv.reader(inp)
        first_flag = True
        for row in reader:
            if first_flag:
                first_flag = False
                continue
            sentence, tag = row[1], row[3]
            label = int(eval(tag))
            if label == 1:
                stats[category] += 1
            else:
                stats['Others'] += 1
            counts += 1
            json_row = {"text": sentence.replace('\n', ','), "label": label}
            oup.write(json.dumps(json_row, ensure_ascii=False) + '\n')
        print(f'{category}-数据集类别占比统计{stats} / {counts}')


def trans_train_test(inp_configs):
    """
    将 inp_files 中的所有类别的记录整理成 可训练的格式.
    :param inp_configs: ["./Blizzard.json",...]
    :return: ["./train.json","./test.json"]
    configs: 一共5个类别，设置training数据集每个类别占比均匀，每个类1000例，testing数据集每个类别占比均匀，每个类200例
    """
    # note that Dorian and Matthew and Michael and Sandy + Hurricane belong to Hurricane (飓风)
    # tornado（龙卷风） floods (洪水) blizzard（暴风雪）wildfires (野火)
    label = 0
    with open('./train.json', mode='wt', encoding='utf-8') as oup1, open(f'./test.json', mode='wt', encoding='utf-8') as oup2:
        for category_name in inp_configs:
            train_samples_num = 1000 // len(file_configs[category_name])
            test_samples_num = 200 // len(file_configs[category_name])
            for file in file_configs[category_name]:
                count = 0
                with open(file, mode='rt', encoding='utf-8') as inp:
                    record = eval(inp.readline().strip())
                    while record:
                        if record['label'] == 1:
                            record = {'text': record['text'], 'category': category_name, 'label': label}
                            if count < train_samples_num:
                                oup1.write(json.dumps(record, ensure_ascii=False) + '\n')
                            if train_samples_num < count:
                                oup2.write(json.dumps(record, ensure_ascii=False) + '\n')
                            count +=1
                        if count > train_samples_num+test_samples_num:
                            break
                        record = eval(inp.readline().strip())
            print('category:',category_name,', label:',label)
            label += 1


if __name__ == '__main__':
    # for filename in os.listdir('.'):
    #     if filename.endswith('csv'):
    #         filepath = os.path.join('.', filename)
    #         category = filename.split('_')[0][4:]
    #         trans_csv(filepath, category)
    file_configs = {'Hurricane':['./Hurricane.json','./Sandy.json','./Michael.json','./Matthew.json','./Dorian.json'],
                    'Wildfires':['./Wildfires.json'], 'Blizzard':['./Blizzard.json'], 'Floods':['./Floods.json'], 'Tornado':['./Tornado.json']}
    trans_train_test(file_configs)
    """
    category: Hurricane , label: 0
    category: Wildfires , label: 1
    category: Blizzard , label: 2
    category: Floods , label: 3
    category: Tornado , label: 4
    
    Process finished with exit code 0
    """