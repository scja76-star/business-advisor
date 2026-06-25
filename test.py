from groq import Groq

client = Groq(api_key="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")

message = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "A small business owner says their sales dropped 40%. What is the first question you would ask them?"}
    ]
)

print(message.choices[0].message.content)




