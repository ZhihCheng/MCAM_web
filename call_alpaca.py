import argparse
import os
from opencc import OpenCC
import torch
from transformers import AutoModelForCausalLM,  LlamaTokenizer
from transformers import GenerationConfig
from transformers import BitsAndBytesConfig
import sys



cc = OpenCC('s2t') 
DEFAULT_SYSTEM_PROMPT = """You are an assistant with knowledge about motors. 你是一位有馬達領域知識的助手。"""

DEFAULT_Negative_PROMPT = None
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

TEMPLATE = (
    "[INST] <<SYS>>\n"
    "{system_prompt}\n"
    "<</SYS>>\n\n"
    "{instruction} [/INST]"
)

guidance_scale = 3.0
load_in_8bit = False
load_in_4bit = True
use_flash_attention_2 = False


base_model_path = './Chinese-Alpaca-2-7B'
draft_base_model = './Chinese-Alpaca-2-1.3B'



if guidance_scale > 1:
    try:
        from transformers.generation import UnbatchedClassifierFreeGuidanceLogitsProcessor
    except ImportError:
        raise ImportError("Please install the latest transformers (commit equal or later than d533465) to enable CFG sampling.")

if load_in_8bit and load_in_4bit:
    raise ValueError("Only one quantization method can be chosen for inference. Please check your arguments")



parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

def generate_prompt(instruction, system_prompt=DEFAULT_SYSTEM_PROMPT):
    return TEMPLATE.format_map({'instruction': instruction,'system_prompt': system_prompt})


class call_alpaca():
    def __init__(self) -> None:
        ################################data_init#######################################
        load_type = torch.float16
        if torch.cuda.is_available():
            self.device = torch.device(0)
        else:
            self.device = torch.device('cpu')
        tokenizer_path = base_model_path

        self.tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path, legacy=True)
        
        self.generation_config = GenerationConfig(
            temperature=0.2,
            top_k=40,
            top_p=0.9,
            do_sample=True,
            num_beams=1,
            repetition_penalty=1.1,
            max_new_tokens=400
        )




        quantization_config = BitsAndBytesConfig(
            load_in_4bit=load_in_4bit,
            load_in_8bit=load_in_8bit,
            bnb_4bit_compute_dtype=load_type,
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=load_type,
            low_cpu_mem_usage=True,
            device_map='auto',
            load_in_4bit=load_in_4bit,
            load_in_8bit=load_in_8bit,
            quantization_config=quantization_config if (load_in_4bit or load_in_8bit) else None,
            trust_remote_code=True
        )


        model_vocab_size = base_model.get_input_embeddings().weight.size(0)
        tokenizer_vocab_size = len(self.tokenizer)
        if model_vocab_size!=tokenizer_vocab_size:
            base_model.resize_token_embeddings(tokenizer_vocab_size)
        
        self.model = base_model
    
        if self.device==torch.device('cpu'):
            self.model.float()
        self.model.eval()
    
        
        #####################################################################
    
    def alpaca_predict(self,raw_input_text):
        input_text = generate_prompt(instruction=raw_input_text, system_prompt=DEFAULT_SYSTEM_PROMPT)
        negative_text = None if DEFAULT_Negative_PROMPT is None \
            else generate_prompt(instruction=raw_input_text, system_prompt=DEFAULT_Negative_PROMPT)
        inputs = self.tokenizer(input_text,return_tensors="pt")  #add_special_tokens=False ?

        
        if negative_text is None:
            negative_prompt_ids = None
            negative_prompt_attention_mask = None
        else:
            negative_inputs = self.tokenizer(negative_text,return_tensors="pt")
            negative_prompt_ids = negative_inputs["input_ids"].to(self.device)
            negative_prompt_attention_mask = negative_inputs["attention_mask"].to(self.device)
        generation_output = self.model.generate(
            input_ids = inputs["input_ids"].to(self.device),
            attention_mask = inputs['attention_mask'].to(self.device),
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
            generation_config = self.generation_config,
            guidance_scale = guidance_scale,
            negative_prompt_ids = negative_prompt_ids,
            negative_prompt_attention_mask = negative_prompt_attention_mask
        )
        s = generation_output[0]
        output = self.tokenizer.decode(s,skip_special_tokens=True)
        response = output.split("[/INST]")[-1].strip()
        #real output
        # print("Response:",cc.convert(response))
        # print("\n")
        return cc.convert(response)

    
