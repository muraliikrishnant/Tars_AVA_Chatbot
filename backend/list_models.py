import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables.")
else:
    print(f"Checking models with API Key ending in ...{api_key[-4:]}")
    try:
        client = genai.Client(api_key=api_key)
        # The v2 SDK manner to list models might differ, but let's try the standard client method if available
        # or fallback to the models resource.
        # Based on main.py, 'client.models' is used.
        
        print("\n--- Available Models ---")
        # Note: Pagination might be needed but for debugging we just want to see if we can connect 
        # and what the top models are.
        pager = client.models.list() 
        found_flash_2 = False
        
        for model in pager:
            print(f"Model: {model.name}")
            print(f"  - Display Name: {model.display_name}")
            # print(f"  - Metadata: {model}") # Verbose
            if "gemini-2.0-flash" in model.name:
                found_flash_2 = True
                
        print("\n------------------------")
        if found_flash_2:
            print("SUCCESS: `gemini-2.0-flash` was found in the list of available models.")
        else:
            print("WARNING: `gemini-2.0-flash` was NOT found. You might need to use `gemini-1.5-flash` or similar.")
            
    except Exception as e:
        print(f"Error listing models: {e}")

