#!/usr/bin/env python3
"""Test chatbot API functionality"""
import os
import warnings
from dotenv import load_dotenv

# Suppress warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

def test_google_genai():
    """Test direct Google Generative AI"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("✗ No API key found")
            return False
            
        genai.configure(api_key=api_key)
        
        # Try different model names
        model_names = ['gemini-pro', 'gemini-1.5-flash']
        
        for model_name in model_names:
            try:
                print(f"Trying {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("What is recycling? Answer in one sentence.")
                print(f"✓ {model_name} works: {response.text}")
                return model_name
            except Exception as e:
                print(f"✗ {model_name} failed: {e}")
                continue
        
        return False
        
    except Exception as e:
        print(f"✗ Google GenAI error: {e}")
        return False

def test_langchain():
    """Test LangChain wrapper"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        api_key = os.getenv('GOOGLE_API_KEY')
        model_names = ['gemini-pro', 'gemini-1.5-flash']
        
        for model_name in model_names:
            try:
                print(f"Testing LangChain with {model_name}...")
                model = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key
                )
                response = model.invoke("What is recycling?")
                print(f"✓ LangChain {model_name} works: {response.content[:100]}...")
                return model_name
            except Exception as e:
                print(f"✗ LangChain {model_name} failed: {e}")
                continue
        
        return False
        
    except Exception as e:
        print(f"✗ LangChain error: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Direct Google GenAI ===")
    direct_model = test_google_genai()
    
    print("\n=== Testing LangChain Wrapper ===")
    langchain_model = test_langchain()
    
    print("\n=== Results ===")
    if direct_model:
        print(f"Direct Google GenAI works with: {direct_model}")
    if langchain_model:
        print(f"LangChain works with: {langchain_model}")
    
    if direct_model or langchain_model:
        print("✓ At least one method works!")
    else:
        print("✗ Both methods failed")
