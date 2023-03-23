import argparse
import os.path
from tqdm import tqdm
from utils import classify_text_turbo, classify_text_davinci, get_answer_turbo, get_answer_davinci
# import openai
import json

# Att: Amazon_food_comments 没有neutral, 后期答案映射到label的时候，合并negative和neutral
data_meta = {'Amazon_food_comments': ['negative', 'positive', 'neutral'],
             'Natural_Hazards_Twitter': ['Hurricane', 'Wildfires', 'Blizzard', 'Floods', 'Tornado'],
             'PestObserver_France': ['Bioagressor', 'Disease', 'Others'],
             'Chinese_Agri_News': ['农业经济', '农业工程', '水产渔业', '养殖技术', '林业', '园艺', '农作物']}


def main(args):
    source_file_ChatGPT = f'./data/{args.dataset}/test.json'
    answers_file_ChatGPT = f'./data/{args.dataset}/answers_{args.model_type}.json'
    if os.path.exists(answers_file_ChatGPT):
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
            if query_text not in collected_sents:
                if 'davinci' in args.model_type:
                    # classify_text_davinci(query_text, data_meta[args.dataset], args.prompt_template)
                    answers = get_answer_davinci(query_text, data_meta[args.dataset], args.prompt_template)
                else:
                    # classify_text_turbo(query_text, data_meta[args.dataset], args.prompt_template)
                    answers = get_answer_turbo(query_text, data_meta[args.dataset], args.prompt_template)
                if len(answers) != 0:
                    print('Sentence: ', query_text, ', ChatGPT: ', answers)
                    json_row = {"text": query_text, "prompt": args.prompt_template, 'answers': answers}
                    oup.write(json.dumps(json_row, ensure_ascii=False) + '\n')
                    success_count += 1
                    stats['succ'] += 1
                else:
                    stats['fail'] +=1
        print(stats)


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
