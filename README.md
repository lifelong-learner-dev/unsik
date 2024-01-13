# FINAL PROJECT (2023.12.13 ~ )

## 주제 : 운동, 식단 관리 사이트 개발 

### 2024/01/12 유저 인증, 로그인 함수 관련 수정

주의! 아래 지침을 수행하기 전 DB에 저장된 파일들을 export 시키거나 백업해놓으시기 바랍니다.
====================================

> 로그인 회원가입 기능 구현 도중 제가 임의로 만든 users_app_user 테이블 때문에 Django에서 유저 값을 넘길 때 인증 문제가 발생하고 있었습니다. 그냥 users_app_user 테이블만 삭제하여 해결되는 문제가 아니기에 아래 방법을 통해 깨끗한 DB를 재구축하는 작업을 선행합니다.

1. exercise, meal, unsik 등 app에 포함된 models.py 내의 정보를 모두 삭제해주세요.
    - models.py에 정보가 남아있을 경우 오류를 일으킵니다.

2. MySQL의 unsik_db 스키마를 drop해주세요.

    - users_app_user 테이블이 현재 인증 문제를 일으키고 있습니다.
    Django에서 따로 명령어를 통해 users_app_user 테이블을 생성해야 인증 문제가 해결됩니다.

3. 동봉된 MySQL 쿼리문에서 아래 명령어까지만 수행해주세요.

    ```
    CREATE SCHEMA unsik_db;

    use unsik_db;
    ```

4. venv 환경에서 python manage.py makemigrations 실행해주세요.

    ```bash
    python manage.py makemigrations
    ```

    - 만약 오류가 날 경우 meal, exercise 각 앱의 migrations 폴더에서 0001_init.py 같은 거 삭제해주세요.
    - 문제 없이 넘어갔다면 다음 명령어 실행해주세요.

    ```bash
    python manage.py migrate
    ```
    - 터미널 출력창에서 Applying sessions.0001_initial... OK 확인 후 다음 단계로 넘어가주세요. 안 된다면 오류메세지 확인 후 문제 해결 후 다시 수행해주세요.

5. 남은 SQL문 실행해주세요.
    - 이때 users_app_user 항목은 모두 주석처리 되어 실행하지 않습니다. users_app_user 테이블이 migrate를 통해 이미 만들어졌기 때문입니다.
6. inspectdb를 통해 각 models.py에 필요한 DB 넣어주세요.
   ```bash
   python manage.py inspectdb
   ```
   - users_app
     - UsersAppUser
   - meal
     - CalorieDictionary
     - Meal
     - UsersAppUser
7. 삭제했던 DB정보를 import 시켜주세요.
    - calorie_dict_all_processed.csv
    - additional_food_info.csv
    - 그 외 사용할 DB정보 등
8. 회원가입, 로그인 기능 작동하는지 확인해주세요.

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