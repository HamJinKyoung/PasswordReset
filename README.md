# django auth를 이용한 비밀번호 초기화 기능 구현하기

## settings.py

```
EMAIL_HOST = 'smtp.gmail.com'
# 메일을 호스트하는 서버
EMAIL_PORT = '587'
# gmail과의 통신하는 포트
EMAIL_HOST_USER = '발신할 이메일'
# 발신할 이메일
EMAIL_HOST_PASSWORD = '발신할 메일의 비밀번호'
# 발신할 메일의 비밀번호
EMAIL_USE_TLS = True
# TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# 사이트와 관련한 자동응답을 받을 이메일 주소

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
# 보낸 이메일 파일(.txt)들을 담아 둘 경로
```

## urls.py

django.contrib.auth에 있는 password_reset기능을 사용하기 위해 필요한 urlpatterns를 추가해준다.

```python
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="app/password_reset.html"), name='password_reset'),
    path('app/password_reset/done',auth_views.PasswordResetView.as_view(template_name="app/password_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html"), name='password_reset_confirm'),
    path('app/reset/done',auth_views.PasswordResetView.as_view(template_name="app/password_reset_complete.html"), name='password_reset_complete'),
]
```

이때 template_name 속성을 이용하면 직접 만든 html파일의 경로를 적어주면, 장고 admin site와 같은 페이지가 아닌 직접 만든 html이 뜨게할 수 있다.

## password_reset.html

사용자가 비밀번호를 잊어버렸을 때, 비밀번호찾기 버튼
`<a href="{% url 'password_reset' %}">비밀번호찾기</a>`을 누르면 가장 먼저 뜨는 페이지.
form을 이용해 비밀번호를 재설정하기 위한 이메일을 받을 이메일주소를 받는다.

```html
<h1>Forgot your password?</h1>
<span class="subheading">Enter your email address below, and we'll email instructions for setting a new one.</span>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Send me instructions!" />
</form>
```

보낸 이메일은 settings.py에서 설정한 sent_emails폴더에 백업되며, 이메일 형식은 다음과 같다.

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
Subject: Password reset on 127.0.0.1:8000
From: [settings.py에서 설정한 발신할 이메일 주소]
To: [password_reset.html에서 form으로 받은 사용자 이메일 주소]
Date: Sun, 13 Sep 2020 04:34:54 -0000
Message-ID: <159997169499.26820.8129248342526793521@DESKTOP-L5AS6MM>


You're receiving this email because you requested a password reset for your user account at 127.0.0.1:8000.

Please go to the following page and choose a new password:

http://127.0.0.1:8000/reset/Mg/5jv-fea03114792907766937/

Your username, in case you’ve forgotten: [회원가입시 입력했던 사용자이름]

Thanks for using our site!

The 127.0.0.1:8000 team



-------------------------------------------------------------------------------
```

## password_done.html

password_reset.html에서 받은 이메일 주소로 이메일을 보낸 후, 사용자에게 이메일을 확인해보라는 메시지를 담은 페이지.

```html
<h1>Check your inbox.</h1>
<span>We've emailed you instructions for setting your password. You should receive the email shortly!</span>
```

## password_reset_confirm.html

보낸 이메일에 있는 url주소를 통해 들어갔을 때 보여지는 페이지.
새로운 비밀번호를 입력받고, 비밀번호를 변경해준다.

```html
<h1>Set a new password!</h1>
{% if validlink %}
<form method="POST">
    {% csrf_token %} {{ form.as_p }}
    <input type="submit" value="Change my password" />
</form>
{% else %}
<p>The password reset link was invalid, possibly because it has already been used. Please request a new password reset.</p>
{% endif %}
```

## password_reset_complete.html

비밀번호 초기화가 완료되었을 때 나오는 페이지.
로그인 페이지로 갈 수 있도록 a태그를 이용해 링크를 걸어주었다.

```html
<h1>Password reset complete</h1>
<p>Your new password has been set. You can log in now on the <a href="{% url 'signin' %}">log in page</a>.</p>
```
