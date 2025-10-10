from modelscope import pipeline
import torch

class OpenAi():
    def __init__(self):
        self.model_id = "openai-mirror/gpt-oss-120b"
        self.pipe = pipeline(
            "text-generation",
            model=self.model_id,
            torch_dtype="auto",
            device_map="auto",
        )
    
    def _output(self, prompt):
        messages = [
            {"role": "user", "content": prompt},
        ]

        outputs = self.pipe(
            messages,
            max_new_tokens=256,
        )
        print(outputs[0]["generated_text"][-1])