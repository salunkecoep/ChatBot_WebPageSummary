# imports
import requests
from bs4 import BeautifulSoup
import ollama
import gradio as gr

# Constants
LLM_MODEL = "llama3.2"

# A class to represent a Webpage
class Website:
    
    url: str
    title: str
    text: str

    def __init__(self, url):
        
        # Create this Website object from the given url using the BeautifulSoup library
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

# Print the title and content of a website.
# ed = Website("https://edwarddonner.com")
# print(ed.title)
# print(ed.text)

# Define our system prompt
system_prompt = "You are an assistant that analyzes the contents of a website \
    and provides a short summary, ignoring text that might be navigation related. \
    Respond in markdown."

# A function that writes a User Prompt that asks for summaries of websites.
def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "The contents of this website is as follows; \
        please provide a short summary of this website in markdown. \
        If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


# The API from Ollama expects the same message format as OpenAI:
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# Show summary of a given website.
def summarize(url):
    try:
        website = Website(url)
        messages = messages_for(website)
        response = ollama.chat(model=LLM_MODEL, messages=messages)
        # print(response['message']['content'])
        return response['message']['content']
    except Exception as e:
        return f"An error occurred: {e}"

# Show summary of a particular website.
# summarize("https://wisdomfromsrisriravishankar.blogspot.com/2025/06/to-be-enthusiastic-or-difficult-is-your.html")

# Gradio UI
summarizeUI = gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(label="Enter Website URL"),
    outputs=gr.Markdown(label="Website Summary"),
    title="Website Summarizer",
    description="Enter a URL to get a summarized version of the webpage content.",
    allow_flagging="never" 
)

# Launch the Gradio UI
summarizeUI.launch()
















