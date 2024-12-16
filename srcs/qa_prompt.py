def get_prompt(ver, quest):
    if ver == "ver1":
        prompt =  "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n"
        prompt += "<|im_start|>user\n<video>\n"
        prompt += f"{quest}"
        prompt += "<|im_end|>\n<|im_start|>assistant\n"  

    return prompt