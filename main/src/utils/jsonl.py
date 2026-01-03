import json
from typing import Iterable
from pydantic import BaseModel

def load_act(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]



def store_jsonl(path: str, records: Iterable):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            if isinstance(r, BaseModel):
                f.write(json.dumps(r.model_dump(), ensure_ascii=False) + "\n")
            else:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
