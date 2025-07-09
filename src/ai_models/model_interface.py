
"""
AI model interface for generating research paper summaries.
"""
import os
import requests
import json
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class BaseAIModel(ABC):
    """Base class for AI model interfaces."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_key = os.getenv("ABACUSAI_API_KEY")
        if not self.api_key:
            raise ValueError("ABACUSAI_API_KEY environment variable not found")
    
    @abstractmethod
    def generate_summary(self, text: str, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Generate summary using the AI model."""
        pass

class OpenAIModel(BaseAIModel):
    """OpenAI GPT model interface."""
    
    def __init__(self, model_name: str = "gpt-4.1-mini"):
        super().__init__(model_name)
        self.base_url = "https://apps.abacus.ai/v1/chat/completions"
    
    def generate_summary(self, text: str, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Generate summary using OpenAI GPT model."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            full_prompt = f"{prompt}\n\nText to summarize:\n{text}"
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": temperature,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            st.error(f"Error generating summary with {self.model_name}: {str(e)}")
            return None

class ClaudeModel(BaseAIModel):
    """Anthropic Claude model interface."""
    
    def __init__(self, model_name: str = "claude-3-sonnet-20240229"):
        super().__init__(model_name)
        self.base_url = "https://apps.abacus.ai/v1/chat/completions"
    
    def generate_summary(self, text: str, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Generate summary using Claude model."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            full_prompt = f"{prompt}\n\nText to summarize:\n{text}"
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": temperature,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            st.error(f"Error generating summary with {self.model_name}: {str(e)}")
            return None

class DeepseekModel(BaseAIModel):
    """Deepseek model interface."""
    
    def __init__(self, model_name: str = "deepseek-chat"):
        super().__init__(model_name)
        self.base_url = "https://apps.abacus.ai/v1/chat/completions"
    
    def generate_summary(self, text: str, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Generate summary using Deepseek model."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            full_prompt = f"{prompt}\n\nText to summarize:\n{text}"
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": temperature,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            st.error(f"Error generating summary with {self.model_name}: {str(e)}")
            return None

class ModelManager:
    """Manager class for all AI models."""
    
    def __init__(self):
        self.models = {
            "GPT-4": OpenAIModel("gpt-4"),
            "GPT-4-Mini": OpenAIModel("gpt-4.1-mini"),
            "Claude-3-Sonnet": ClaudeModel("claude-3-sonnet-20240229"),
            "Claude-3-Haiku": ClaudeModel("claude-3-haiku-20240307"),
            "Deepseek-Chat": DeepseekModel("deepseek-chat"),
            "Llama-3-8B": OpenAIModel("meta-llama/Llama-3-8b-chat-hf"),
            "Mistral-7B": OpenAIModel("mistralai/Mistral-7B-Instruct-v0.1")
        }
    
    def get_model(self, model_name: str) -> Optional[BaseAIModel]:
        """Get AI model by name."""
        return self.models.get(model_name)
    
    def get_available_models(self) -> list:
        """Get list of available model names."""
        return list(self.models.keys())
    
    def generate_summary(self, model_name: str, text: str, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Generate summary using specified model."""
        model = self.get_model(model_name)
        if not model:
            st.error(f"Model '{model_name}' not found")
            return None
        
        return model.generate_summary(text, prompt, temperature)
