import google.generativeai as genai


genai.configure(api_key="API KEY")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

safe = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction='Give a direct answer to the question without additional text or formatting',
    safety_settings=safe,
)

session = model.start_chat(history=[])

def add_category(links, categories):
    cat = ", ".join(categories)
    links = "\n".join(links)
    ft = f'Categorize the following headlines with 1 of the following categories: {cat}\nALSO rate the news relevancy from 1-10\nReturn your responses in this format <title> ;; <category> ;; <relevancy> and DO NOT ADD BOLD OR ADDITIONAL FORMATTING\nHere are the headlines:\n{links}'
    res = session.send_message(ft).text.strip().split('\n')
    return res
