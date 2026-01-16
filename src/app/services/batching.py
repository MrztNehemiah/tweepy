import tiktoken
from typing import List, Dict


# GPT-2
# enc = tiktoken.get_encoding("gpt2")
# print(enc.encode("hello world!!!"))

# GPT-4
# enc = tiktoken.get_encoding("cl100k_base")
# print(enc.encode("hello world!!!"))

enc = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    return len(enc.encode(text))


class BatchToken:
    def __init__(self, items, max_tokens: int) -> None:
        self.items = items
        self.max_tokens = max_tokens
        self._batches: List[Dict] = []
        self._oversized: List[Dict] = []
        self._processed: bool = False

    def _process(self):
        """Process items once, separate into batches and oversized"""
        if self._processed:
            return

        batches = []
        oversized = []
        current_batch = []
        current_tokens = 0
        batch_id = 0

        for item in self.items:
            tokens = count_tokens(item)

            if tokens > self.max_tokens:
                oversized.append({"item": item, "token_count": tokens})
                continue

            if current_tokens + tokens <= self.max_tokens:
                current_batch.append(item)
                current_tokens += tokens
            else:
                batches.append(
                    {
                        "batch_id": batch_id,
                        "texts": current_batch,
                        "token_count": current_tokens,
                    }
                )
                batch_id += 1
                current_batch = [item]
                current_tokens = tokens

        if current_batch:
            batches.append(
                {
                    "batch_id": batch_id,
                    "texts": current_batch,
                    "token_count": current_tokens,
                }
            )

        self._batches = batches
        self._oversized = oversized
        self._processed = True

    def batch(self):
        self._process()
        return self._batches

    def oversize(self):
        self._process()
        return {"oversized": self._oversized}
