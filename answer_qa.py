import json
from vllm import LLM, SamplingParams
import os
from tqdm import tqdm
from srcs.utils import video_load
from srcs.qa_prompt import get_prompt
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Process input arguments for the script.")
    
    # 각 변수에 대한 argument 추가
    parser.add_argument("--results_path", type=str, default="results", help="Path to store the VLM direct results.")
    parser.add_argument("--video_path", type=str, default="../FBL_VQA/data/nextqa", help="Path to the video data.")
    parser.add_argument("--vlm_model", type=str, default="llava-ov_0.5b", help="VLM model to use.")
    parser.add_argument("--llm_model", type=str, default="Phi-3.5-mini-instruct", help="LLM model to use.")
    
    parser.add_argument("--pre_task", type=str, default="gen_answer_question_ver3_wo_llava_output", help="")
    parser.add_argument("--task", type=str, default="answer_qa_wo", help="")
    parser.add_argument("--prompt_ver", type=str, default="ver1", help="Prompt version.")
    parser.add_argument("--gpu_num", type=str, default="1", help="Prompt version.")
    # vlm arguments
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for sampling.")
    parser.add_argument("--top_k", type=int, default=1, help="Top-k sampling.")
    parser.add_argument("--max_tokens", type=int, default=256, help="Maximum number of tokens.")
    parser.add_argument("--frequency_penalty", type=float, default=1.0, help="Frequency penalty.")
    parser.add_argument("--presence_penalty", type=float, default=0.5, help="Presence penalty.")

    args = parser.parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"]= args.gpu_num
    
    use_model_path = f"vlm_{args.vlm_model}_llm_{args.llm_model}"
    result_output_path = f"{args.task}_prompt-{args.prompt_ver}"
    
    save_folder = os.path.join(args.results_path, use_model_path, result_output_path)
    pre_task_load_path = os.path.join(args.results_path, use_model_path, args.pre_task)
    # 디렉토리가 없으면 생성
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"Directory created: {save_folder}")
    else:
        print(f"Directory already exists: {save_folder}")
    
    # 모델 load
    if args.vlm_model == 'llava-ov_7b':
        MODEL="llava-hf/llava-onevision-qwen2-7b-ov-hf"
        vlm_answer_path = 'output/Llava-ov_7b_samples_nextqa_mc_test.jsonl'
    elif args.vlm_model == 'llava-ov_0.5b':
        MODEL="llava-hf/llava-onevision-qwen2-0.5b-ov-hf"
        vlm_answer_path = 'output/Llava-ov_0.5b_samples_nextqa_mc_test.jsonl'

    # 모델 load
    llm = LLM(model=MODEL, tensor_parallel_size=1)
    sampling_params = SamplingParams(temperature = args.temperature, top_k=args.top_k, max_tokens = args.max_tokens, frequency_penalty = args.frequency_penalty, presence_penalty = args.presence_penalty)
    
    # 첫 번재 answer output data load    
    with open(vlm_answer_path, 'r', encoding='utf-8') as f:
        Llava_outputs = [json.loads(line) for line in f]  
    video_set = {Lo['doc']['video'] for Lo in Llava_outputs}
        
    # generation
    for vid in tqdm(list(video_set)[500:]):
        file_path = os.path.join(save_folder, f"{vid}.json")
        if os.path.exists(file_path):
            print(f"Skipping file {vid}.json as it already exists")
            continue
        else:
            pre_resFile_path = os.path.join(pre_task_load_path, f"{vid}.json")
        with open(pre_resFile_path, 'r', encoding='utf-8') as json_file:
            pre_resFile = json.load(json_file)

        video = video_load(args.video_path, vid)
        
        generated_text=[]
        for res in pre_resFile:
            qa_prompt_list=[]
            qa_list=[]
            
            for q in res['gen_question']:
                text_prompt = get_prompt(args.prompt_ver, q)            
                outputs = llm.generate({"prompt": text_prompt,"multi_modal_data": {"video": video}}, sampling_params=sampling_params, use_tqdm =False)
                
                #qa_prompt_list.append(q)
                qa_list.append(outputs[0].outputs[0].text)    
            #res['vlm_prompt'] = qa_prompt_list
            res['vlm_qa'] = qa_list
            generated_text.append(res)
        
        # Save the dictionary as a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(generated_text, json_file)