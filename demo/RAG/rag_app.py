import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()

# Azure AI Search credentials
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Azure Foundry Credentials
FOUNDRY_ENDPOINT = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
FOUNDRY_API_KEY = os.getenv("AZURE_AI_FOUNDRY_API_KEY")
MODEL_NAME = os.getenv("AZURE_AI_FOUNDRY_MODEL")

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

# Initialize Search Client
search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_ADMIN_KEY)
)

def search_knowledge_base(query: str):
    """Searches the Azure AI Search index for relevant context."""
    results = search_client.search(search_text=query, top=3)
    
    context = []
    chunk_ids = []
    for doc in results:
        # Based on Exercise 7, the index has title, locations, persons, keyPhrases
        title = doc.get("title", "Unknown")
        key_phrases = doc.get("keyPhrases", [])
        locations = doc.get("locations", [])
        
        chunk_id = doc.get("id", title) # Use title as chunk ID if id isn't explicitly available
        chunk_ids.append(chunk_id)
        
        doc_info = f"Chunk ID/Title: {chunk_id}\nLocations: {', '.join(locations) if locations else 'None'}\nKey Phrases: {', '.join(key_phrases) if key_phrases else 'None'}"
        context.append(doc_info)
        
    return "\n\n".join(context), chunk_ids

import sys
import urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

# Extract subdomain to construct standard cognitiveservices endpoint
parsed_url = urllib.parse.urlparse(FOUNDRY_ENDPOINT)
hostname = parsed_url.hostname
if "services.ai.azure.com" in hostname:
    subdomain = hostname.split(".")[0]
    openai_endpoint = f"https://{subdomain}.cognitiveservices.azure.com/"
else:
    openai_endpoint = FOUNDRY_ENDPOINT

def main():
    # Get standard openai.AzureOpenAI client
    openai_client = AzureOpenAI(
        azure_endpoint=openai_endpoint,
        api_key=FOUNDRY_API_KEY,
        api_version="2024-12-01-preview"
    )
    
    print("\n=============================================")
    print("Welcome to the Margie's Travel RAG Assistant!")
    print("Type 'exit' to quit.")
    print("=============================================\n")

    while True:
        try:
            user_query = input("You: ").strip()
            if user_query.lower() in ["quit", "exit"]:
                break
                
            if not user_query:
                continue

            print("\n[System] Searching knowledge base...")
            context, chunk_ids = search_knowledge_base(user_query)
            
            system_prompt = f"""
You are a helpful travel assistant.
Please answer the user's question using ONLY the following context.
If the answer cannot be found in the context, say "I don't know based on the provided information."

--- Context ---
{context}
----------------
"""
            
            print("[System] Generating answer...")
            response = openai_client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            
            print(f"\nAssistant: {response.choices[0].message.content}")
            print(f"\n[Sources used - Chunk IDs]: {', '.join(chunk_ids)}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
