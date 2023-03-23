import argparse
import os.path
from tqdm import tqdm
from utils import classify_text_turbo, classify_text_davinci, get_answer_turbo, get_answer_davinci
# import openai
import json
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score, confusion_matrix, classification_report

# Att: Amazon_food_comments 没有neutral, 后期答案映射到label的时候，合并negative和neutral
data_meta = {'Amazon_food_comments': ['negative', 'positive', 'neutral'],
             'Natural_Hazards_Twitter': ['Hurricane', 'Wildfires', 'Blizzard', 'Floods', 'Tornado'],
             'PestObserver_France': ['Bioagressor', 'Disease', 'Others'],
             'Chinese_Agri_News': ['农业经济', '农业工程', '水产渔业', '养殖技术', '林业', '园艺', '农作物']}


def main(args):
    categories = data_meta[args.dataset]
    source_file_ChatGPT = f'./data/{args.dataset}/test.json'
    answers_file_ChatGPT = f'./data/{args.dataset}/answers_{args.model_type}.json'
    if not os.path.exists(answers_file_ChatGPT):
        open(answers_file_ChatGPT, 'wt', encoding='utf-8').close()
    collected_sents = []
    with open(answers_file_ChatGPT,'rt',encoding='utf-8') as inp:
        line = inp.readline()
        while line:
            collected_sents.append(eval(line.strip())['text'])
            line = inp.readline()
    with open(source_file_ChatGPT,'rt',encoding='utf-8') as inp, open(answers_file_ChatGPT, 'at', encoding='utf-8') as oup:
        lines = inp.readlines()
        success_count = len(collected_sents)
        stats = {'succ':0, 'fail':0}
        for line in tqdm(lines):
            if success_count > 1000:
                # print('预测量已足够多.')
                break
            query_text = line['text']
            real_tag = line['label']
            if query_text not in collected_sents:
                if 'davinci' in args.model_type:
                    # classify_text_davinci(query_text, categories, args.prompt_template)
                    answers = get_answer_davinci(query_text, categories, args.prompt_template)
                else:
                    # classify_text_turbo(query_text, categories, args.prompt_template)
                    answers = get_answer_turbo(query_text, categories, args.prompt_template)
                if len(answers) != 0:
                    print('Sentence: ', query_text, ', ChatGPT: ', answers)
                    json_row = {"text": query_text, "prompt": args.prompt_template, 'answers': answers, 'real_tag': real_tag}
                    oup.write(json.dumps(json_row, ensure_ascii=False) + '\n')
                    success_count += 1
                    stats['succ'] += 1
                else:
                    stats['fail'] +=1
        print(stats)

    # calculate the prediction's performance using acc/ f1-micro/ f1-macro/ recall / precision
    print('Calculating its metrics...')
    pred_list, real_list = [], []
    with open(answers_file_ChatGPT, 'rt', encoding='utf-8') as inp:
        lines = inp.readlines()
        for line in lines:
            answers, real_tag = eval(line.strip())['answers'], eval(line.strip())['real_tag']
            assert isinstance(real_tag, int)
            pred_tag = categories.index(answers[0])
            pred_list.append(pred_tag)
            real_list.append(real_tag)
            print('pred_list: ', pred_list)
            print('real_list: ', real_list)
            print('-----------------------------------------')
            print(confusion_matrix(real_list, pred_list))
            micro_f1_score = f1_score(real_list, pred_list, average='micro')
            macro_f1_score = f1_score(real_list, pred_list, average='macro')
            weighted_f1_score = f1_score(real_list, pred_list, average='weighted')
            recall_weighted = recall_score(real_list, pred_list, average='weighted')
            precision_weighted = precision_score(real_list, pred_list, average='weighted')
            print(classification_report(real_list, pred_list, target_names=categories))
            """
            average：字符串类型，取值为 [None, ‘binary’ (default), ‘micro’, ‘macro’, ‘samples’, ‘weighted’]。多分类必须的参数，如果为None，则返回每一类的recall，否则，根据其参数返回整体的召回率。
            'macro'：用于多分类，只有两个属性可以选择 ‘macro’ 和 ‘weighted’ 。' macro '：计算每个标签的指标，并计算它们的未加权平均值。不考虑样本类别是否平衡。' weighted '：计算每个标签的指标，并找到它们的平均值，对(每个标签的真实实例的数量)进行加权。
            'micro': 整体计算TP、FN、FP，然后根据公式计算得分。
            'macro': 计算每个标签的指标，并计算它们的未加权平均值。不考虑样本类别是否平衡。
            'weighted': 计算每个标签的指标，并找到它们的平均值，对(每个标签的真实实例的数量)进行加权。This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.
            """
            print(f"'\nmicro_f1_score: ', {micro_f1_score}, '\nmacro_f1_score: ', {macro_f1_score}, '\nweighted_f1_score: ' {weighted_f1_score}, '\nrecall_weighted: ', {recall_weighted}, '\nprecision_weighted: ', {precision_weighted}")


    """
    >>> from sklearn.metrics import f1_score
    >>> y_true = [0, 1, 2, 0, 1, 2]
    >>> y_pred = [0, 2, 1, 0, 0, 1]
    >>> f1_score(y_true, y_pred, average='macro')
    0.26...
    >>> f1_score(y_true, y_pred, average='micro')
    0.33...
    >>> f1_score(y_true, y_pred, average='weighted')
    0.26...
    >>> f1_score(y_true, y_pred, average=None)
    array([0.8, 0. , 0. ])
    >>> y_true = [0, 0, 0, 0, 0, 0]
    >>> y_pred = [0, 0, 0, 0, 0, 0]
    >>> f1_score(y_true, y_pred, zero_division=1)
    1.0...
    """


if __name__ == '__main__':
    # 考虑因素: 模型版本, 回答choices数量, 不同QA模板.
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default='Amazon_food_comments',
                        choices=['Amazon_food_comments', 'Natural_Hazards_Twitter', 'PestObserver_France',
                                 'Chinese_Agri_News'],
                        help='specify using which dataset, please refer to /data/.../test.json')
    parser.add_argument("--model_type", type=str, default='gpt-3.5-turbo',
                        choices=['text-davinci-001', 'text-davinci-002', "text-davinci-003", "gpt-3.5-turbo"],
                        help='specify using which model')
    parser.add_argument("--prompt_template", type=str, help='specify using the QA template', default=
                        "Classify the following sentence into one of the given categories: {}\n\nSentence: {}\nCategory: ")
    _args = parser.parse_args()
    main(_args)
