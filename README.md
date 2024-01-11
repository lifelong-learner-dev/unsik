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

### 2024/01/11 csh 변경점
    > requirements.txt가 수정되었습니다.
    - torch==2.1.2
    - ultralytics==8.0.229

    > 부트스트랩 적용 후 CSS가 의도된 모습과 다르게 출력되는 부분을 수정하였습니다.

    > 식단 올리기 페이지에서 사진 업로드 없이 '분석' 버튼을 누르면
     오류 페이지가 출력되는 현상을 수정하였습니다.

    > 칼로리 사전 페이지 CSS가 소소하게 수정되었습니다. 크게 눈에 띄지는 않습니다.