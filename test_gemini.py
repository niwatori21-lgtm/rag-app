from google import genai

# ここに AI Studio の API キーを直接書く
client = genai.Client(api_key="AIzaSyByualT2Sc4QuuF6ffPrjCCsrq7k5dNs80")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="こんにちは"
)

print(response.text)
