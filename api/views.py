from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

class Chat(APIView):
    def post(self, request):
        #serializer = YourModelSerializer(data=request.data)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        usermessage = request.data.get('message', None)

        messages=[
            {"role": "system", "content": "You are a friend that gives good advice. concern if I have problem. limit reply 200 characters"},
        ]

        for obj in usermessage:
            sender = "user";
            if obj['sender'] == "AI":
                sender = "system";
            messages.append({"role": sender, "content": obj['text']})

        if usermessage is not None:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            return Response(completion.choices[0].message.content)
        else:
            return Response({'error': 'Message not found in request payload'}, status=400)
