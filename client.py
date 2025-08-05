from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

comppletion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
)

print(comppletion.choices[0].message.content)
