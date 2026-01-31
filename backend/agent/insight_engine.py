import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from backend.config import config
from backend.rag.retriever import retrieve_context
from backend.rag.prompts import INSIGHT_PROMPT
import google.generativeai as genai

class InsightEngine:
    _model = None
    _tokenizer = None

    def _load_model(self):
        if self.use_hf and InsightEngine._model is None:
            print(f"Loading Hugging Face model: {config.HF_MODEL_ID}...")
            try:
                # Load model
                InsightEngine._model = AutoModelForCausalLM.from_pretrained(
                    config.HF_MODEL_ID, 
                    trust_remote_code=True, 
                    device_map="auto",
                    token=config.HF_TOKEN
                )
                # Load tokenizer
                InsightEngine._tokenizer = AutoTokenizer.from_pretrained(
                    config.HF_MODEL_ID, 
                    trust_remote_code=True,
                    token=config.HF_TOKEN
                )
                print("HF model loaded successfully.")
            except Exception as e:
                print(f"Error loading HF model: {e}")
                self.use_hf = False

    def __init__(self):
        self.use_hf = config.HF_TOKEN is not None
        # Lazy load is preferred for faster startup
        # self._load_model()
        
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(config.MODEL_NAME)
        else:
            self.gemini_model = None

    def generate_insight(self, query: str) -> str:
        """
        Generates business insights based on retrieved context.
        Uses Hugging Face model if configured, otherwise falls back to Gemini.
        """
        context = retrieve_context(query)
        if not context:
            return "No verified drug launch found in ingested data."
            
        prompt = INSIGHT_PROMPT.format(context=context, query=query)
        
        if self.use_hf:
            if InsightEngine._model is None:
                self._load_model()
            
            if InsightEngine._model:
                # Hugging Face Inference
                inputs = InsightEngine._tokenizer(prompt, return_tensors="pt").to(InsightEngine._model.device)
            with torch.no_grad():
                outputs = InsightEngine._model.generate(**inputs, max_new_tokens=200)
            
            # Decode only the new tokens
            input_len = inputs["input_ids"].shape[1]
            response_text = InsightEngine._tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
            return response_text
        
        elif self.gemini_model:
            # Gemini Fallback
            response = self.gemini_model.generate_content(prompt)
            return response.text
        else:
            return "No LLM configuration found. Mock Insight: Market trends indicate steady growth in biopharma."

insight_engine = InsightEngine()
