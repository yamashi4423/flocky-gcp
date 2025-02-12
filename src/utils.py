import openai
from consts.prompts import SYSTEM_PROMPT


def response_text_from_llm(user_message: str, client: openai.OpenAI, model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_message}]
    )
    reply_text = response.choices[0].message.content.strip()
    return reply_text