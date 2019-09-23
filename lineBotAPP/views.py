from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from linebot import LineBotApi, WebhookParser
from django.views.decorators.csrf import csrf_exempt
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent,TextSendMessage
from modules import AssistantTranlator
from modules import Invoice

# Create your views here.

LINE_BOT_API = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
MissionStauts="None"

@csrf_exempt
def callback(request):
    
#    MissionStauts=""
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
                global MissionStauts
                
                if mtext =="使用說明":
                    LINE_BOT_API.reply_message(event.reply_token, TextSendMessage("目前功能模組有\"-翻譯\"與\"-兌獎\"\n" + 
                                                                                  "翻譯支援語言有\"@英文\", \"@中文\", \"@日文\", \"@韓文\" \n" +
                                                                                  "翻譯使用方式:  @英文 你好 \n" +
                                                                                  "兌獎為當期統一發票對獎: 功能分別有 開獎、與輸入發票號碼對獎 \n" + 
                                                                                  "使用方式: 開獎或123(輸入發票號碼)"))
                
                if MissionStauts == "None":
                    if mtext[0] == "-":
                        MissionStauts = mtext[1:3]
                        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage("目前模組: " + MissionStauts + "  ，輸入\"-\"可以離開此模組"))
                    else:
                        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage("目前沒有任務模組，請輸入\"說明\"來了解如何使用"))
                        
                elif MissionStauts == "翻譯":
                    if mtext[0] != "-":
                        Responese = AssistantTranlator.assistantTranslator()
                        Responese.setLang(mtext[:3])
                        Responese.setText(mtext[4:])
                        
                        LINE_BOT_API.reply_message(event.reply_token, Responese.startTranslate())
                    else:
                        MissionStauts = "None"
                        
                elif MissionStauts == "兌獎":
                    if mtext[0] != "-":
                        Responese = Invoice.invoice()
                        if mtext == "開獎":
                            LINE_BOT_API.reply_message(event.reply_token, Responese.show())
                        elif mtext.isdigit():
                            Responese.setNumber(int(mtext))
                            Responese.run()
#                            LINE_BOT_API.reply_message(event.reply_token, Responese.setNumber(int(mtext)))
                    else:
                        MissionStauts = "None"

                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()