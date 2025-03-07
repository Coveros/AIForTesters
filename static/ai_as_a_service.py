from google import genai

api_key = input("enter your API key: ")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how to create a good test case",
)

print(response.text)