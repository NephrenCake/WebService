import base64
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from captcha.views import CaptchaStore, captcha_image
from rest_framework_simplejwt.views import TokenObtainPairView
from login.serializer import DmallTokenObtainPairSerializer

from django.views import View


class CaptchaAPIView(View):

    def get(self, request):
        hash_key = CaptchaStore.generate_key()
        try:
            # 获取图片id
            id_ = CaptchaStore.objects.filter(hashkey=hash_key).first().id
            image = captcha_image(request, hash_key)
            # 将图片转换为base64
            image_base = 'data:image/png;base64,%s' % base64.b64encode(image.content).decode('utf-8')
            json_data = json.dumps({"id": id_, "image_base": image_base})
            # 批量删除过期验证码
            CaptchaStore.remove_expired()
        except:
            json_data = None
        return HttpResponse(json_data, content_type="application/json")


class DmallTokenObtainPairView(TokenObtainPairView):
    # 登录成功返回token
    serializer_class = DmallTokenObtainPairSerializer


# 使用 token 之后，应当继承 APIView 类
class test(APIView):
    def get(self, request):
        return JsonResponse({"msg": "ok"}, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        return JsonResponse({"msg": "ok"}, json_dumps_params={"ensure_ascii": False})


class test_no_login(View):
    def get(self, request):
        return JsonResponse({"msg": "ok"}, json_dumps_params={"ensure_ascii": False})
