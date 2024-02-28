from django.shortcuts import redirect, render
from pathlib import Path
from django.urls import reverse
from dotenv import load_dotenv
from openai import OpenAI

from shared.shared_functions import checkLogin

load_dotenv()

client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input="Teaching a four-year-old autistic child to speak requires patience, consistency, and a tailored approach to their unique needs. Here's a step-by-step checklist that you can use daily for the next three months. Keep in mind that progress may vary, and it's essential to adapt these steps based on the child's individual progress and preferences."
)

# OPENAI Test
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )
# print(completion.choices[0].message)

# Create your views here.
def dashboard(request):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  #response.stream_to_file(speech_file_path)
  return render(request, 'dashboard/dashboard.html')