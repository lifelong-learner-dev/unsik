# FINAL PROJECT (2023.12.13 ~ )

## 주제 : 운동, 식단 관리 사이트 개발 

### 2024/01/02 

#### 프로젝트 기본 세팅
    > 모든 세팅이 완료되시면 
      주소 : http://127.0.0.1:8000/exercise/
      로 이동하시면 기본 페이지 확인 가능 (추후 수정 가능)

    > venv 설치목록 (window 기준)
      2024/01/02
      > pip install django
      > pip install mysqlclient
      > pip install django djangorestframework

    > requirements.txt에 있는 목록 전체설치
      > pip install -r requirements.txt

    > .gitignore 생성

    > DB 접속 정보 (./db_settings.py)
      > mysql사용
      > 계정 자기것으로 수정 필요 (비밀번호 포함)
      > database명 unsik_db

    > template 아래 base.html, nvbar.html 생성
      > nvbar에 운동, 식단 메뉴목록 써놓기만 한 상태 
      > templates 폴더
        > base.html 생성
        > nvbar.html 생성
          > exercise와 meal url 링크 추가

    > static 폴더 생성
      > css 폴더 생성
        > css 폴더 내에 basic.css 파일
      > js 폴더 생성
        > jquery는 사용해본 버전인 3.7.1 (필요시 변경 가능)

    > unsik 폴더 내 settings.py
      > DATABASE와 SECRET_KEY db_settings.py로 이동
      > INSTALLED_APPS "rest_framework", "exercise", "meal" 추가
      > TEMPLATES의 DIRS에 BASE_DIR 추가
      > STATICFILES_DIR 추가
      
    > unsik 폴더 내 urls.py
      > exercise.urls 와 meals.urls 추가

    > meal 폴더
      > templates\meal 폴더
        > meal_index.html 생성
      > views.py 
        > meal_index 추가
      > urls.py
        > meal_index url 추가

    > exercise 폴더
      > templates\exercise 폴더
        > exercise_index.html 생성
      > views.py 
        > exercise_index 추가
      > urls.py
        > exercise_index url 추가



### 2024/01/04 csh 변경점

  > 운식 로고가 생성되었습니다.

  > templates에 header, footer, main.html이 추가 되었습니다.

  > nvbar.html이 일부 수정되었습니다.

  > reset.css 가 추가되었습니다. 스타일 초기화하는 코드가 담겨 있습니다. 초기화된 스타일에 맞춰 다른 페이지도 작성해주시면 감사하겠습니다.

  > 메인페이지는 아직 작성 중입니다.
    > 메뉴 css는 변경될 예정입니다.
    > 메뉴 a 태그에 링크는 자유롭게 걸어주시기 바랍니다.