from ollama import chat

response=chat(

    model="qwen3",

    messages=[

        {
            "role":"user",
            "content":"aws jump box terraform"
        }

    ]

)

print(response)