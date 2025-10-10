from pathlib import Path
import time
import regex
import os
from typing import Dict, List, Tuple, Union
import mmap
import re
import random
class BPE():
    def __init__(self):
        self.PAT = r"""'(?:[sdmt][ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\n{L}\p{N}]+|\s+(?|\S)|\s+"""

    def load_sample_doc(self, input_path: str, sample_size: int, special_token: str):
        try:
            with open(input_path, "r+", encoding="utf-8", errors="ignore") as f:
                with mmap.mmap(f.fileno, 0, access=mmap.ACCESS_READ) as mm:
                    documents = []
                    start = 0
                    while start < len(mm):
                        end = mm.find(special_token.encode('utf-8'), start)
                        if end == -1:
                            doc = mm[start:].decode("utf-8", errors="replace").strip()
                            if doc:
                                documents.append(doc)

                            break
                        doc = mm[start:end].decode("utf-8", errors="replace").strip()
                        start = end + len(special_token)
                        if doc:
                            documents.append(doc)
                    if len(documents) > sample_size:
                        documents = random.sample(documents, sample_size)
                    return special_token.join(documents)
                
        except Exception as e:
            raise IOError(f"加载数据集失败：{e}")
                    
    
    def pretokenizer(self, documents: List[str], num_prosesser: int, bytes_to_unicode_map: Dict[int, str]):
        self.load_sample_doc()
        pass

    def run_train_bpe(self, input_path: Union[str, os.PathLike], vocab_size: int, special_tokens: List[str], num_prosesser: int, sample_size: int, **kwargs)-> Tuple[Dict[int, bytes], List[Tuple[bytes, bytes]]]:
        base_vocab_size = 256+len(special_tokens)

        byte_to_unicode_map = self.byte_to_unicode()
        unicode_to_byte_map = {b: bytes([a]) for a, b in byte_to_unicode_map}

        #词汇表
        vocab = {i: bytes([i]) for i in range(256)}
        next_token_id = 256
        existing_bytes = set(vocab.values)

        for st in special_tokens:
            sx = st.encode('utf-8')
            if sx not in existing_bytes and len(vocab) < vocab_size:
                vocab[next_token_id] = sx
                existing_bytes.add(sx)
                next_token_id += 1

        text = self.load_sample_doc(input_path, sample_size=sample_size, special_token=special_tokens[0])

        special_tokens_ = [re.escape(st) for st in special_tokens]
        special_token = "|".join(special_tokens_)
        documents = [part for part in re.split(special_token, text) if part]

        self.pretokenizer(documents=documents, num_prosesser=num_prosesser, bytes_to_unicode_map=byte_to_unicode_map)

    def byte_to_unicode() -> Dict[int, str]:
        """字节到Unicode映射（与训练时一致）"""
        bs = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256)) 
        cs = bs[:]
        n = 0
        for b in range(256):
            if b not in bs:
                bs.append(b)
                cs.append(256 + n)
                n += 1
        return {b: chr(c) for b, c in zip(bs, cs)}


if __name__ == '__main__':
    config = {
        "vocab": 10000,
        "special_tokens": ["<|endoftext|>"],
        "num_processer": 5,
        "sample_size": 30000
    }

    train_path = ""
    valid_path = ""
    # 检查文件是否存在
    if not Path(train_path).exists():
        raise FileNotFoundError(f"训练集文件 {train_path} 不存在")
    if not Path(valid_path).exists():
        raise FileNotFoundError(f"验证集文件 {valid_path} 不存在")
    
    print("start train......")
    start_time = time.time()

    tokenizer = BPE()

    tokenizer.run_train_bpe(train_path, **config)

