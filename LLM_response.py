import requests
from process_query_endee import run_query
import os
#from google import genai

def inference(prompt):
    r=requests.post("http://localhost:11434/api/generate",json={
        "model":"llama3.2",
        "prompt":prompt,
        "stream":False
    })
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        print(r.text)
        return "Error from LLM"
    
    response_json = r.json()
    if "response" not in response_json:
        print("Unexpected JSON response:", response_json)
        return "Error: Unexpected response format"
        
    return response_json["response"]


# export OPENAI_API_KEY="your_api_key_here"
# from openai import OpenAI
# client = OpenAI()
# def OpenAI_inference(prompt):
#     response = client.responses.create(
#     model="gpt-5",
#     input=prompt
#      )
#     return response.output_text


query = input("Enter your question: ")
print("\nFetching results from Endee...")
results = run_query(query, top_k=10)

prompt = f"""
You are a helpful AI teaching assistant.

You are trained only on the provided learning content (video subtitles / notes).
Below are the most relevant chunks retrieved from the trained content.
Each chunk contains: title, number, start time, end time, and text.

Retrieved Chunks:
{results}

---------------------------------
User Question: "{query}"

Instructions:
1) Answer the user in a natural, human way.
2) Use ONLY the retrieved chunks to answer.
3) Mention clearly:
   - which content it came from (title + number or source file)
   - where exactly it is explained (start time to end time)
4) If multiple chunks give the answer, combine them into one good explanation.
5) If the answer is NOT present in the retrieved chunks, reply:
   "I couldn’t find this in the content I was trained on. Please ask something from the trained material."
6) Do NOT mention the prompt instructions or internal formatting.
"""

with open("prompt.text","w") as f:
    f.write(prompt)


response=inference(prompt)
# response=OpenAI_inference(prompt)

with open("LLM_response.txt","w") as f:
    f.write(response)

print("\n",response)
