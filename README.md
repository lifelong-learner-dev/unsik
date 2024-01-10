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

### 2024.01.03 식단 분석 페이지 추가
    - 식단 분석 페이지 작업중 
    - 시간대별 코멘트
    - 이미지 업로드 

### 2024/01/10 csh 변경점
    > requirements.txt가 수정되었습니다.
    - torch==2.1.2
    - ultralytics==8.0.229

    > settings.py에 MEDIA_ROOT, MEDIA_URL 관련 코드가 생성되었습니다.
    - 이미지를 이곳에 임시 저장한 후 디텍션하기 위한 용도입니다.

    > unsik/urls.py에 DEBUG용 코드가 생성되었습니다. MEDIA_ROOT 경로를 제대로 못 잡을 때 이렇게 쓰면 된다고 합니다.

    > meal_analyze_result가 생성되었습니다. 결과를 보여주는 화면입니다.

    > modules/meal_anal.py 코드가 작성 되었습니다. YOLO v8 모델을 위한 코드로 원할한 작동을 위해서는 requirements.txt의 필수 패키지들을 설치해야 합니다.

    <footer>
    % marquee는 실험용입니다.