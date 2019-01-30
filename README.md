# Django-Page
Django - Korean Style, Wordpress-like, Simplest, CMS (Content Management System)


한.국.형. ㅋ

**- 문서 정리 중 -**

## Features
- page code 기반 자동 url 매칭
- ckeditor 기반 admin 제공 
- 기타등등 

## 의존성
- Django (2.0+ 만 테스트)
- django-ckeditor
- easy-thumbnails

## 권장 설치
- django-revision
- django-revision-compare
- django-bootstrap4

## 설치
### 0. pip install
```python
pip install django-page
```
### 1. app setup
INSTALL_APPS에 'page'추가

``` python
INSTALLED_APPS = [
    ...
    'page',
    ...
```

### 2. URL setup
메인 urls.py 파일 제일 하단에 page.urls 추가
``` python
urlpatterns = [

    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    ...
 
    path('admin/', admin.site.urls),
    ...
    path('', include('page.urls')),
]

```

### 3. Custumize Template
templates/page/base.html 를 오버라이드해서 현 사이트 스타일과 일치하게 변경한다
필수적으로 필요한 블럭명은 css, leader, content, title, subtitle, bgimage 이다

아래는 base.html 템플릿 예시
``` html
<html lang="ko">
<head>
    <title>{{ site.name }}</title>

    {% block css %}
    {% endblock %}
</head>
<body class="st-container st-effect-3">

<div class="wrapper">

    {% block leader %}
        <h1>{% block title %}Title{% endblock %}</h1>
        <p>{% block subtitle %}Subtitle{% endblock %}</p>
    {% endblock %}

    {% block content %}
    {% endblock %}
</div>
</body>
</html>
```

## Page Code
영문으로 된 slug 타입 문자열로 바로 URL로 대응 된다.

예를 들어 페이지 코드가 'test'인 경우 '/test' url로 연결시 표출된다.
따라서 admin등 다른 앱과 충돌이 되는 코드는 사용 하지말것!

### Build-in page code
페이지 코드 'home'의 경우 루트 URL ('/')에 대해 예약 되어 있다.


## Shortcode
등록된 키워드를 django template tag로 변환, 해석 해준다

### 사용법
page 컨텐츠 상에 다음과 같이 추가
```python
[커맨드 매개변수1 매개변수2...]
```

### Build-in 명령어
- 페이지 넣기 
    - 매개변수 : 페이지 코드 또는 페이지 ID
    - 등록된 페이지 내용을 컨텐츠 중간에 삽입
- 반복 문구 넣기
    - 매개변수 : 반복문구 코드 또는 반목문구 ID
    - 등록된 반복 사용 문구를 컨텐츠 중간에 삽입
- 포함하기 = 가져오기
    - include
    
### 커스텀 명령어 추가

1. 커스텀 명령어 선언
settings.py 상에 다음과 같이 선언

```python

PAGE_SHORTCODES = {
    "연락처넣기": "contact",
    "다운로드항목": "download",
    "보기": "view",
}
```

2. 파라메터 니모닉 선언
편의를 위해서 첫번째 매개변수는 복잡한 내용으로 맵핑 가능
```python
PAGE_TARGET_MAP = {
    "공지사항": "widget/notice.html",
    "FAQ": "widget/faq.html",
}
```

ex>
[보기 공지사항] 의 경우 {% view "widget/notice.html" %} 으로 변환됨.

3. load 할 모듈 추가
커스텀 테그를 추가하기 위해서 사용 될 templatetags 모듈을 추가.
모든 shortcode 실행 시점 상단에서 load 됨
  
```python
PAGE_UNPACK_WITH = (
    'home',
    'contact_info',
)
```

다음과 같이 상단에 포함됨
```python
{% load home %}
{% load contact_info %}
```
