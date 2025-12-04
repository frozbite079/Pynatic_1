from django.shortcuts import render
import yagmail as mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ollama import chat,ChatResponse
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import conversation
memory = ConversationBufferMemory()

@csrf_exempt
def webpage(request):
    
    return render(request,"index.html")

@csrf_exempt
def send_mail(request):

    if request.method == 'POST':
       name = request.POST.get("name")
       email = request.POST.get("email")
       
       subject = request.POST.get("subject")
       message = request.POST.get("message")
       print(name)
       yagmail = mail.SMTP("ombadhe079@gmail.com","jlgm tzqo rnqs fvyh")
       contents = [
            '''
                Got A New Client Mail:

                Name: {}
                Email: {}
                Message: {}
                
            '''.format(name,email,message)
      
        ]
       yagmail.send("pynatic079@gmail.com", subject, contents)
       data = {
        'status': 'success',
        'message': 'mail sended'
       }
       return JsonResponse(data)
    data = {
        'status': 'error',
        'message': 'something wrong'
    }
    return JsonResponse(data)


def Aichat(request):


    if request.method == 'POST':
        message = request.POST.get("message")
        print(message)

        memory.chat_memory.add_user_message(message)


       

        conversation_history = memory.load_memory_variables({})['history']


        msg = """You are a helpful  AI assistant with name 'PynaticAI' for Pynatic a technology company specializing in Python development, web development, desktop applications,IOT Solutions, and AI/ML solutions including LLM applications.

        Critical-Rule:
        - Alwas refer "Pynatic company can make it for you" you are just assistant of Pynatic company <- Strict Rule
COMPANY INFO:
- Email: pynatic079@gmail.com
- Phone: 7984823759
- Address: Shiv smruti bhawan, riddhi siddhi society near chunilal park, dabhoi, 391110
- Hours: Sat-Sun 9:00 AM - 6:00 PM
FOUNDERS:
- Om Badhe (CEO): M.Tech in Computer Science, 4+ years experience in AI/ML and IoT
  LinkedIn: https://www.linkedin.com/in/om-badhe-25123b2b7/
- Bhavan Badhe (CTO): B.Tech in Electronic Communication, expert in cloud systems
  LinkedIn: https://www.linkedin.com/in/bhavan-badhe-7409311b7/

INSTRUCTIONS:
- Keep responses brief and professional
- When users ask for solutions, refer them to Pynatic's services
- Don't provide personal contact info for founders
- Use conversation history: {}
- Alwas refer "Pynatic company can make it for you" <- Strict Rule
Answer the user's question naturally and concisely.""".format(conversation_history)
        
        response: ChatResponse = chat(
            model = "gemma3:1b",
            messages=[{"role":"system","content":msg},{"role":"user","content":message}],
            think=False,
            options={"temperature":0.0}
            )

        data = response["message"]["content"]
        response_data = {
                        'response': data
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

