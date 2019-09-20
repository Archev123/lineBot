from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from linebot import LineBotApi, WebhookParser
from django.views.decorators.csrf import csrf_exempt
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent
from modules import AssistantTranlator

# Create your views here.

LINE_BOT_API = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == "POST": 
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                
                mtext = event.message.text
                Responese = AssistantTranlator.assistantTranslator()
                Responese.setLang(mtext[:3])
                Responese.setText(mtext[4:])
                
                LINE_BOT_API.reply_message(event.reply_token, Responese.startTranslate())
        return HttpResponse()
    else:
        return HttpResponseBadRequest()