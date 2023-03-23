import csv
import json


"""
数据集类别占比统计 {'Bioagressor': 80, 'Disease': 93, 'Others': 152}
数据集类别占比统计 {'Bioagressor': 19, 'Disease': 19, 'Others': 45}

Process finished with exit code 0
"""
def trans_csv(inp_file, oup_file):
    # Bioagressor, Disease, Others => 0, 1, 2
    stats = {'Bioagressor':0, "Disease":1, "Others":2}
    counts = 0
    with open(inp_file, mode='rt', encoding='utf-8') as inp, open(oup_file, mode='wt', encoding='utf-8') as oup:
        reader = csv.reader(inp)
        first_flag = True
        for row in reader:
            if first_flag:
                first_flag = False
                continue
            sentence, bioagressor, disease = row[1], row[3], row[4]
            if int(eval(bioagressor)) == 1:
                label = 0
                stats['Bioagressor'] +=1
            elif int(eval(disease)) == 1:
                label = 1
                stats['Disease'] += 1
            else:  # Bioagressor, Disease 两列数值都不是1,"1"
                label = 2
                stats['Others'] += 1
            counts += 1
            json_row = {"text": sentence.replace('\n', ','), "label": label}
            oup.write(json.dumps(json_row, ensure_ascii=False) + '\n')
        print(f'数据集类别占比统计{stats} / {counts}')


if __name__ == '__main__':
    trans_csv('./train_set.csv', './train.json')
    trans_csv('./val_set.csv', './test.json')


