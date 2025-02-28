import json
import os

# results/vlm_llava-ov_0.5b_llm_Phi-3.5-mini-instruct/answer_qa_prompt-ver1
folder_path = "results/vlm_llava-ov_0.5b_llm_Phi-3.5-mini-instruct/answer_qa_wo_prompt-ver1"
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.json')])

ansIdx=["A","B","C","D","E"]
acc=0

results_dict={'acc_yes':0, 'acc_no':0, 'inacc_yes':0, 'inacc_no':0}

# JSON 파일 순서대로 읽기
for res_file_name in file_list:
    resfile_path = os.path.join(folder_path, res_file_name)
    with open(resfile_path, 'r', encoding='utf-8') as file:
            res_data = json.load(file)  # JSON 데이터 로드
                    
    for res in res_data:
        # LLaVA가 정답일 때
        if ansIdx[res['target_answer']] == res['llava_output'][0]:
            for qa in res['vlm_qa']:
                if "Yes" in qa:
                    results_dict['acc_yes'] += 1
                elif "No" in qa:
                    results_dict['acc_no'] += 1
        else:
            for qa in res['vlm_qa']:
                if "Yes" in qa:
                    results_dict['inacc_yes'] += 1
                elif "No" in qa:
                    results_dict['inacc_no'] += 1
                    

print(results_dict)
print((results_dict['acc_yes']+results_dict['inacc_yes'])/(results_dict['acc_no']+results_dict['inacc_no']))