import argparse
import json
from vllm import LLM, SamplingParams
import os
from tqdm import tqdm
from srcs.utils import extract_questions
from srcs.prompt import atomic_question_ver3 


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Process input arguments for the script.")
    
    # 각 변수에 대한 argument 추가
    parser.add_argument("--results_path", type=str, default="results", help="Path to store the VLM direct results.")
    parser.add_argument("--vlm_model", type=str, default="llava-ov_0.5b", help="VLM model to use.")
    parser.add_argument("--llm_model", type=str, default="Phi-3.5-mini-instruct", help="LLM model to use.")
    
    parser.add_argument("--task", type=str, default="gen_total_question", help="task:Vans_D(Video+answer to Desc), V_D(Video to Desc), V_MD(Video to Multi-view Desc)")
    parser.add_argument("--prompt_ver", type=str, default="ver3", help="Prompt version.")
    parser.add_argument("--gpu_num", type=str, default="0", help="Prompt version.")
    
    # vlm arguments
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for sampling.")
    parser.add_argument("--top_k", type=int, default=1, help="Top-k sampling.")
    parser.add_argument("--max_tokens", type=int, default=256, help="Maximum number of tokens.")
    parser.add_argument("--frequency_penalty", type=float, default=1.0, help="Frequency penalty.")
    parser.add_argument("--presence_penalty", type=float, default=0.5, help="Presence penalty.")
    
    args = parser.parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"]= args.gpu_num

    # 모델 load
    if args.vlm_model == 'llava-ov_7b':
        MODEL="llava-hf/llava-onevision-qwen2-7b-ov-hf"
        vlm_answer_path = 'output/Llava-ov_7b_samples_nextqa_mc_test.jsonl'
    elif args.vlm_model == 'llava-ov_0.5b':
        MODEL="llava-hf/llava-onevision-qwen2-0.5b-ov-hf"
        vlm_answer_path = 'output/Llava-ov_0.5b_samples_nextqa_mc_test.jsonl'
    
    use_model_path = f"vlm_{args.vlm_model}_llm_{args.llm_model}"
    result_output_path = f"{args.task}_{args.prompt_ver}"
    save_folder = os.path.join(args.results_path, use_model_path, result_output_path)
    
    pre_task_load_path = os.path.join(args.results_path, use_model_path)
    
    # 디렉토리가 없으면 생성
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"Directory created: {save_folder}")
    else:
        print(f"Directory already exists: {save_folder}")

    NoBeam_SamplingParams = SamplingParams(temperature = 0.0, top_k=1, max_tokens = 256, frequency_penalty = 1.0, presence_penalty = 0.5, stop= "\n\n")
    llm = LLM(model="microsoft/Phi-3.5-mini-instruct", download_dir = "../model_dir", tensor_parallel_size=1, max_model_len=4096)
    
    # 첫 번재 answer output data load    
    with open(vlm_answer_path, 'r', encoding='utf-8') as f:
        Llava_outputs = [json.loads(line) for line in f]  
    video_set = {Lo['doc']['video'] for Lo in Llava_outputs}
    
    # generation
    ansOrder=["A","B","C","D","E"]
    task_key = args.task.split("_")[0]
    for vid in tqdm(list(video_set)[500:]):
        file_path = os.path.join(save_folder, f"{vid}.json")
        if os.path.exists(file_path):
            print(f"Skipping file {vid}.json as it already exists")
            continue
                
        generated_text=[]
        for res in filter(lambda q: q['doc']['video'] == vid, Llava_outputs):
            results_dict={}
            results_dict['doc_id']=res['doc_id']
            results_dict['question']=res['doc']['question']
            results_dict['target_answer']=res['doc']['answer']
            results_dict['llava_output']=res["filtered_resps"][0]
            
            for n in range(5):
                output_dict={}
                quest_prompt = res['doc']['question']
                quest_prompt+="?\nAnswer:" + res['doc']["a"+str(n)]

                o = llm.generate(
                    [atomic_question_ver3 % (quest_prompt)],
                    NoBeam_SamplingParams,
                    use_tqdm=False
                )
                output_dict['qa'] = quest_prompt
                output_dict['gen_question'] = [line.lstrip('-').strip() for line in o[0].outputs[0].text.splitlines()]
                results_dict["a"+str(n)] = output_dict

            generated_text.append(results_dict)
        # question_option_description
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(generated_text, json_file, ensure_ascii=False, indent=4)