"""
Base Provider Interface.

Har provider (Gemini, AgentRouter, aur future mein koi bhi naya) is
interface ko follow karega — matlab har provider mein ek `call()`
function hoga jo (text, input_tokens, output_tokens) return karega.

Isse naya provider add karna bahut easy ho jata hai: bas ek naya
class banao jo BaseProvider ko implement kare, aur registry mein
ek entry add karo. Kahin aur code change nahi karna padega.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def call(self, model_id: str, prompt: str, max_tokens: int = 512) -> dict:
        """
        Returns a dict with keys: text, input_tokens, output_tokens
        """
        raise NotImplementedError
