import json
import os

# results/vlm_llava-ov_0.5b_llm_Phi-3.5-mini-instruct/answer_qa_prompt-ver1
folder_path = "results/vlm_llava-ov_0.5b_llm_Phi-3.5-mini-instruct/answer_qa_total_prompt-ver1"
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.json')])

ansIdx=["A","B","C","D","E"]
acc=0

results_dict={'target_yes':0, 'target_no':0, 'Non_target_yes':0, 'Non_target_no':0}

# JSON 파일 순서대로 읽기
for res_file_name in file_list:
    resfile_path = os.path.join(folder_path, res_file_name)
    with open(resfile_path, 'r', encoding='utf-8') as file:
            res_data = json.load(file)  # JSON 데이터 로드
                    
    for res in res_data:
        for idx in range(5):
            # target
            if res['target_answer'] == idx:
                qa_dict = res['a'+str(idx)]
                for ans in qa_dict['gen_answer']:
                    if 'Yes' in ans:
                        results_dict['target_yes'] += 1
                    elif 'No' in ans:
                        results_dict['target_no'] += 1
            else:
                qa_dict = res['a'+str(idx)]
                for ans in qa_dict['gen_answer']:
                    if 'Yes' in ans:
                        results_dict['Non_target_yes'] += 1
                    elif 'No' in ans:
                        results_dict['Non_target_no'] += 1

                    
print(results_dict)
