import openai
import config
import private

openai.api_key = private.API_KEY


def ask(que: str, ai: str = "curie"):
    try:
        response = openai.Completion.create(
            model=config.MODEL_DICT[ai][0],
            prompt=que,
            temperature=0.8,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        text = response["choices"][0]["text"]
        text = str(text).strip()
        return text, ai
    except:
        return "false", ai
