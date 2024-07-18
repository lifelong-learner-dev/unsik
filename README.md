# FINAL PROJECT (2023.12.13 ~ 2024.02.06)

## 주제 : 운동, 식단 관리 사이트 개발 

### 2024/02/05 임덕현 - 브랜치명 : ldh 
    > 1. 식단 추천 기능 google map 추가 & 멘트 추가
      > .env에 GOOGLE_MAP_API_KEY 추가 필요
      > 식단 목록에서 원하는 메뉴 클릭시 현재 지도에서 해당 메뉴 검색
    > 2. 식단 히스토리 페이지 현재달일 경우 다음달 버튼 숨김 & 크기 조절
    > 3. requirements.txt 내용 추가 (python-dotenv - API 키 서버에서 읽어와서 html로 보내는 부분에 사용)

### 2024/02/06 김근형 - 브랜치명 : ghk 수정 내용
    > payment.html : 결제 페이지 디자인 수정
    > 결제 관련 views.py : 결제 후 29일 남았다는 것을 보여주는 기능 추가

    > llm.html : 챗봇 페이지 디자인 수정
    > 챗봇 관련 views.py : 마이페이지에 있는 모든 정보를 
                          AI 챗봇에게 전달하여 해당 정보를 토대로 
                          답변가능하도록 기능 구현
                          * 추가로 챗봇에 전송 클릭 뿐아니라 엔터만 눌러도 메시지 전송 가능

    > users_app models.py : 회원가입시 운동목표가 생성되지 않고 null 값으로 되는 내용 수정 
                            user에 운동목표가 빠져있어 그것만 추가

    > 마이페이지 달력에 요일과 일에 밑줄 삭제 : 요청사항
    
    > 운동등급페이지들 : 디자인 수정

    
### 2024/02/05 김근형 - 브랜치명 : ghk 수정 내용
    > payment : AI 챗봇을 사용하기 위한 결제 페이지 추가
      > 아래 명령어 작동해주시면 됩니다.
        > use unsik_db;
          -- 기존 테이블에 AUTO_INCREMENT 설정 추가
          ALTER TABLE `point`
          MODIFY `point_idx` BIGINT AUTO_INCREMENT; 
          
      > 결제 완료되면 AI 챗봇 사용 가능
      > payment.html, payment.css 추가,
      > community/views.py에 기능 추가


### 2024/02/02 차성현 - 브랜치명 : csh 내용

    > 1. 메인페이지 슬라이드쇼 이미지가 추가되었습니다.
    > 2. 모든 페이지의 CSS가 소소하게 수정되었습니다.
    > 3. 식사 분석 페이지에서 아무 문제가 없을 경우 스마일 아이콘이 출력됩니다.
    > 4. sign_up.html 페이지 내에 ajax가 추가되었습니다. 본래 페이지 내에 스크립트를 바로 끼워넣는 것은 좋지 못하나 Django 문법을 사용하기 위해 넣었습니다.

### 2024/02/02 김근형 - 브랜치명 : ghk 수정 내용
    > 1. unsik 폴더에 
         .gitignore, db_settings.py, manage.py, README.md, requirements.txt 가 있는 곳에
        > .env 파일을 만들어주세요
          > .env 파일 안에 해당 문구를 추가하시고 
            제가 보내드리는 openai api key를 붙여넣으시면 됩니다.
            > OPENAI_API_KEY="여기안에 제가 보내드리는 api key를 넣으세요"

    > 2. pip install python-decouple==3.8
        >.env 파일 가져오기 위해 필요

    > 3. pip install openai==1.10.0
        > 운식 챗봇 사용하기 위해 필요

    > 4. 결제 기능 현재로서는 주석처리됨 
        > 사유 : 기능은 잘 작동하는데, 그 기능이 작동한 이후의 로직 미완성 (2월2일 오전 기준)

    > 5. 마이페이지 디자인 수정 (완료)
        > 세로에서 가로로 한번에 모든 내용을 볼 수 있도록 디자인 수정

    > 6. 나의 운동 등급 페이지 디자인 수정 (진행 중)
        > 추가 수정 필요 
          (등급 확인 버튼을 누르면, 입력 폼이 없어지고
           사용자 입력 값에 따라  
           각 운동마다 국민체력진흥공단 자료에서 몇 퍼센트에 속하는지 보여주기)

    > 7. 나의 운동 등급 페이지 관련된 모든 파일과 챗봇 관련된 모든 파일에 웹서버 url 추가 



### 2024/01/31 주요 페이지 CSS 변경, 서비스 플로우 재점검

    > 1. header 드롭다운 메뉴의 CSS가 변경되었습니다.
    > 2. footer CSS가 변경되었습니다.
    > 3. 식사 분석, 칼로리 사전 CSS가 변경되었습니다.

---

### 2024/01/30 AWS 서버에 프로젝트 올리기

로그인 창 클릭 시 화면 전체가 검게 덮이는 문제가 있어 급하게 수정하였습니다. 다른 모달에 영향을 미칠 지는 모르겠으나, 임시 조치만 취해놓은 상태입니다.

### 2024/01/31 주요 페이지 CSS 변경, 서비스 플로우 재점검

  > 1. header 드롭다운 메뉴의 CSS가 변경되었습니다.
  > 2. footer CSS가 변경되었습니다.
  > 3. 식사 분석, 칼로리 사전 CSS가 변경되었습니다.

---

### 2024/01/30 AWS 서버에 프로젝트 올리기

로그인 창 클릭 시 화면 전체가 검게 덮이는 문제가 있어 급하게 수정하였습니다. 다른 모달에 영향을 미칠 지는 모르겠으나, 임시 조치만 취해놓은 상태입니다.

### 2024/01/30 김근형 - 브랜치명 : ghk 수정 내용
1. AI 예측 모델 관련 모든 Ajax에서 url 경로 변경 (금일 AWS 서버에서 사용시 문제)
2. my_page관련 view 부분 수정: 추가 수정이 필요할 수 있을 것으로 보임
   - 운동, 식단은 그래프가 그려지기는 하나 바로 바로 적용이 되지는 않고 있음
     - 시간 또는 날짜 문제인 것 같음
   - 몸무게 daily 테이블에 있어 바로 적용이 됨
   

### 2024/01/29 DB 새로운 컬럼 생성 및 CSS 수정

오늘의 변경 사항

  > 1. users_app_user 테이블의 새로운 컬럼 추가.
  > 2. 상단메뉴, 메인페이지 CSS 변경
  > 3. 슬라이드 쇼 기능 구현

 - users_app_user 테이블에 새로운 컬럼이 추가되었습니다. 운동목표를 저장하기 위한 컬럼입니다. default 값은 NULL 입니다.

```sql
ALTER TABLE `unsik_db`.`users_app_user` 
ADD COLUMN `user_exercise_purpose` VARCHAR(45) NULL DEFAULT NULL AFTER `user_target_weight`;
```

users_app/forms.py에서 가입 시 이 테이블에 값을 넣으려고 합니다. 따라서 forms.py에도 변경된 항목이 있습니다.

마이그레이션 필요 시 수행해주세요.

 - 메인페이지의 전반적인 CSS가 변경 단계에 있습니다. 공통 색상은 아직 정해지지 않았지만 대부분 초록 / 파란색 계열로 갈피가 잡힌 듯 합니다.

 - ## merge 작업 시 CSS를 주의해주세요.

---

### 2024/01/26 식사 분석 알고리즘 및 CSS 배치 수정

    > 식사 분석 페이지의 전반적인 CSS를 손 보고 있습니다. 아직 만져야 할 부분들이 많습니다.

    > 알고리즘은 제대로 들어가는 느낌입니다. 다만 추가로 고려되어야 할 사항들이 있어 알고리즘이 완성된 단계는 아닙니다.

    > views.py meal_post 함수의 meal 테이블 기록 기능이 임시로 비활성화 되어 있습니다. DB 기록이 안 될 경우 이 부분을 확인해주시기 바랍니다.

#### 변경 내역

1. foodDict.py 함수 추가
2. views.py 함수 수정
3. meal_analyze.css 수정

---

### 2024/01/25 CSS 스타일 레이아웃 수정

meal 테이블 nutrient_info 행에 추가되는 정보가 추가되었습니다.

기존 : [총 탄수화물, 총 단백질, 총 지방, 총 당류, 총 나트륨(mg), 총 포화지방]  
추가 : [총 탄수화물, 총 단백질, 총 지방, 총 당류, 총 나트륨(mg), 총 포화지방, 총 트랜스지방, 총 식이섬유]  

테스트를 위해 Meal DB로 기록하는 기능이 임시로 비활성화 되어 있습니다.

식단 분석 페이지 CSS 계속 작업 중입니다. 식사 알고리즘은 아직 구축 단계에 있습니다.

### 2024/01/24 시간 저장 오차 수정

시간이 계속 UTC로 변경되어 들어가는 문제는 Django의 settings.py 내부에 정의된 설정 때문인 것으로 잠정 결론 지었습니다.

1. settings.py에서 아래 옵션을 False로 바꿉니다.

```python
USE_TZ = False
```

2. 또한 meal 테이블에 들어가는 Date 값을 자동 입력하기 위해 models.py 에서 아래처럼 바꿔줍니다.

```python
meal_date = models.DateTimeField(auto_now_add=True)
```

3. auto_now_add=True 의 의미는 자동 기입을 허용한다는 말입니다. 그 말은 views.py에서 시간을 받아와 기입할 필요가 없다는 것입니다.  
meal/views.py 370번 줄을 확인해주세요.

```python
Meal.objects.create(
    user = user_instance,
    # meal_date = current_time.strftime("%Y-%m-%d %H:%M:%S"),
    # meal_date = iso_formatted_time,
    # meal_date = current_time,
    meal_photo = meal_data_list[-1],
    meal_info = json.dumps(filtered_list),
    meal_type = meal_type,
    meal_calories = meal_calories,
    nutrient_info = json.dumps(nutrient_info)
)
```

날짜 기입란이 모두 비활성화 되었습니다. migration은 따로 필요 없습니다. 작동 테스트 후 문제가 있다면 알려주세요.

---
### 2024/01/25 ghk브랜치 (김근형)
    > 마이페이지 완료
      > 달력에 식단, 운동 관련 표시 완료
      > 몸무게 그래프 출력 완료
      > 식단으로 인한 섭취 칼로리와
        운동으로 인한 소비 칼로리 그래프에 표시 완료

    > 마이페이지 수정 페이지 완료


### 2024/01/23 
### 임덕현님 수정하신 내용 merge + 마이페이지, 유저 정보(키, 몸무게) 수정페이지 백엔드+프론트엔드 1차 완료
    > 추가 작업 필요한 내용
      > 그래프 추가될 예정
      > 달력에 식단, 운동 테이블에 기록된 내용이 있으면 달력에 표시될 수 있도록 시도할 예정

    > 작업한 내용
      > 마이페이지 백엔드
        > forms.py 
          > MypageUserForm 클래스 추가
        > views.py
          > 키, 몸무게 정보 수정을 위한 my_page_update 기능 생성
        > urls.py
          > 수정을 위한 url 추가
        
      > 마이페이지 프론트엔드
        > my_page.html
          > 수정버튼에 수정 페이지 url 추가
        > my_page_update.html
          > 키, 몸무게 수정 페이지 생성
        > my_page1.css
          > my_page.html과 my_page_update.html css 작성
        > mypage_calendar.css
          > full calendar 라이브러리 관련 css 추가


### 2024/01/22 DB 저장 시간 오차 수정

    > DB에 저장되는 meal_date가 현재 시각보다 -9시 늦는 것을 확인했습니다. views.py 이외 따로 건드린 것은 없습니다.

    > 메인 페이지 css가 현재 디자인 변경 중에 있습니다.

    > views.py와 foodDict.py에 새로 작성 중인 함수가 몇 있습니다. 아직 구현이 완벽히 되지 않았습니다.

    > meal_analyze_result.html 아래에 ajax 기능이 동작하고 있습니다. 테스트겸 작성한 코드들이 즐비합니다.

---

### 2024/01/19 식사 분석 결과 DB 저장 기능 구현
#### (01/12자 유저 인증, 로그인 함수 수정 내역은 아래에 있습니다.)

> 식단 분석 페이지에서 유저가 고르거나 바꾼 음식이 식단 DB에 저장되도록 하는 기능이 어느정도 구현되었습니다.

+ 선행되어야 하는 작업이 존재하므로 아래 지침을 따라주시기 바랍니다.

1. MySQL의 meal DB만 Drop 후 재생성 해주세요.  
  postNum 키의 자동증가 (AUTO_INCREMENT) 미지정을 이유로 값이 들어갈 때 오류가 발생합니다. postNum 요소만 바꿔 meal 테이블만 새로 만들어주시면 됩니다.  
  아래 명령어를 실행해주세요.

  ```sql
  DROP TABLE meal;

  CREATE TABLE `meal` (
    `postNum` BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT NOT NULL,
    `meal_date` DATETIME,
    `meal_photo` VARCHAR(255),
    `meal_info` TEXT,
    `meal_type` VARCHAR(20),
    `meal_calories` FLOAT,
    `nutrient_info` TEXT
  );

  ALTER TABLE `meal` ADD FOREIGN KEY (`user_id`) REFERENCES `users_app_user` (`id`);
  ```

2. Django에서 필요한 모델들을 다시 가져와주세요.  
  마이그레이션이 진행된 상태라 다시 할 필요는 없습니다. 다만 변경된 DB 정보는 업데이트 해 주어야 합니다.  
  아래 명령어를 따라주세요.

  ```cmd
  python manage.py inspectdb
  ```
3. 받아온 db 정보 중 meal 항목을 찾아 meal/models.py에 붙여넣어주세요.

  ```python
  class Meal(models.Model):
    postnum = models.BigAutoField(db_column='postNum', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING)
    meal_date = models.DateTimeField(blank=True, null=True)
    meal_photo = models.CharField(max_length=255, blank=True, null=True)
    meal_info = models.TextField(blank=True, null=True)
    meal_type = models.CharField(max_length=20, blank=True, null=True)
    meal_calories = models.FloatField(blank=True, null=True)
    nutrient_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meal'
  ```
  postnum 항목에 **BigAutoField** 지정 여부와 user에 **ForeignKey** 지정을 확인해주세요.

4. 테스트  
  정보가 제대로 들어가는 지 테스트 합니다. 식단 분석 페이지에 사진을 올리고 CRUD 기능 테스트 해주세요.

5. DB 입력 정보  
  nutrient_info에 기입되는 리스트 순서입니다. 나트륨을 제외한 모든 무게 단위는 (g) 입니다.  
  [총 탄수화물, 총 단백질, 총 지방, 총 당류, 총 나트륨(mg), 총 포화지방]

---

### 2024/01/22 DB 저장 시간 오차 수정

    > DB에 저장되는 meal_date가 현재 시각보다 -9시 늦는 것을 확인했습니다. views.py 이외 따로 건드린 것은 없습니다.

    > 메인 페이지 css가 현재 디자인 변경 중에 있습니다.

    > views.py와 foodDict.py에 새로 작성 중인 함수가 몇 있습니다. 아직 구현이 완벽히 되지 않았습니다.

    > meal_analyze_result.html 아래에 ajax 기능이 동작하고 있습니다. 테스트겸 작성한 코드들이 즐비합니다.

---

### 2024/01/19 식사 분석 결과 DB 저장 기능 구현
#### (01/12자 유저 인증, 로그인 함수 수정 내역은 아래에 있습니다.)

> 식단 분석 페이지에서 유저가 고르거나 바꾼 음식이 식단 DB에 저장되도록 하는 기능이 어느정도 구현되었습니다.

+ 선행되어야 하는 작업이 존재하므로 아래 지침을 따라주시기 바랍니다.

1. MySQL의 meal DB만 Drop 후 재생성 해주세요.  
  postNum 키의 자동증가 (AUTO_INCREMENT) 미지정을 이유로 값이 들어갈 때 오류가 발생합니다. postNum 요소만 바꿔 meal 테이블만 새로 만들어주시면 됩니다.  
  아래 명령어를 실행해주세요.

  ```sql
  DROP TABLE meal;

  CREATE TABLE `meal` (
    `postNum` BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT NOT NULL,
    `meal_date` DATETIME,
    `meal_photo` VARCHAR(255),
    `meal_info` TEXT,
    `meal_type` VARCHAR(20),
    `meal_calories` FLOAT,
    `nutrient_info` TEXT
  );

  ALTER TABLE `meal` ADD FOREIGN KEY (`user_id`) REFERENCES `users_app_user` (`id`);
  ```

2. Django에서 필요한 모델들을 다시 가져와주세요.  
  마이그레이션이 진행된 상태라 다시 할 필요는 없습니다. 다만 변경된 DB 정보는 업데이트 해 주어야 합니다.  
  아래 명령어를 따라주세요.

  ```cmd
  python manage.py inspectdb
  ```
3. 받아온 db 정보 중 meal 항목을 찾아 meal/models.py에 붙여넣어주세요.

  ```python
  class Meal(models.Model):
    postnum = models.BigAutoField(db_column='postNum', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING)
    meal_date = models.DateTimeField(blank=True, null=True)
    meal_photo = models.CharField(max_length=255, blank=True, null=True)
    meal_info = models.TextField(blank=True, null=True)
    meal_type = models.CharField(max_length=20, blank=True, null=True)
    meal_calories = models.FloatField(blank=True, null=True)
    nutrient_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meal'
  ```
  postnum 항목에 **BigAutoField** 지정 여부와 user에 **ForeignKey** 지정을 확인해주세요.

4. 테스트  
  정보가 제대로 들어가는 지 테스트 합니다. 식단 분석 페이지에 사진을 올리고 CRUD 기능 테스트 해주세요.

5. DB 입력 정보  
  nutrient_info에 기입되는 리스트 순서입니다. 나트륨을 제외한 모든 무게 단위는 (g) 입니다.  
  [총 탄수화물, 총 단백질, 총 지방, 총 당류, 총 나트륨(mg), 총 포화지방]

---

### ghk 브랜치 : 2024/01/22 회원가입시 

    >! 회원가입시 자동으로 daily 테이블에 레코드(기록) 생성
    
        > 1. users_app의 forms.py에 
            > daily 테이블에 레코드 생성 코드 작성
        
        > 2. users_app의 models.py에
            > daily 테이블 DB포함
            > daily 테이블의 user 부분 
              > 'UsersAppUser' => User로 변경
        
        > 3. sign_up.html에 목표몸무게 추가 

    > ! 마이페이지 초안 작성 (!!! 추가 작업 진행 필요 초안만 작성됨 !!!)
        > 1. my_page.html 생성 (users_app/templates/users_app)
        > 2. views.py에 my_page function 생성 (users_app)
        > 3. urls.py에 my_page url 추가 (users_app)
        > 4. nvbar에 마이페이지 url 추가
        > 5. my_page1.css 생성 (static/css)

### 2024/01/12 유저 인증, 로그인 함수 관련 수정

주의! 아래 지침을 수행하기 전 DB에 저장된 파일들을 export 시키거나 백업해놓으시기 바랍니다.
====================================

> 로그인 회원가입 기능 구현 도중 제가 임의로 만든 users_app_user 테이블 때문에 Django에서 유저 값을 넘길 때 인증 문제가 발생하고 있었습니다. 그냥 users_app_user 테이블만 삭제하여 해결되는 문제가 아니기에 아래 방법을 통해 깨끗한 DB를 재구축하는 작업을 선행합니다.
>  > 필요한 파일 목록
>  >  > (modified)Unsik_query.sql  
>  >  > calorie_dict_all_processed.csv  
>  >  > additional_food_info.csv (농축산물 일부 생것 포함된 csv)

1. 마이그레이션 안전을 위해 주석처리된 구문들이 있습니다. 지금 당장은 손 대지 않도록 합시다.

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
   주석처리된 항목들을 이때 풀어주시면 됩니다. 항목은 아래와 같습니다.  가급적 순서에 맞춰 주석을 풀어주시기 바랍니다.

    * users_app
      - models.py
        + 14번 줄부터 끝까지
      - forms.py
        + 3번 줄 'from 구문'
        + 14번 줄 'model = User'
      - views.py
        + 2번 줄 'from 구문'
    * meal
      - models.py
        + 4번 줄부터 끝까지
      - views.py
        + 5번 줄 'from 구문'
    
7. 삭제했던 DB정보를 import 시켜주세요.
    - calorie_dict_all_processed.csv
    - additional_food_info.csv
    - 그 외 사용할 DB정보 등
8. 회원가입, 로그인 기능 작동하는지 확인해주세요.

## 종료

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

### exercise 테이블 수정 sql
```sql
-- exercise_date를 datetime 타입으로 변경
ALTER TABLE exercise MODIFY COLUMN exercise_date datetime;

-- exercise_type을 ENUM 타입으로 변경
ALTER TABLE exercise MODIFY COLUMN exercise_type ENUM('유산소', '웨이트');

-- weight (무게)와 reps (횟수), sets(세트수) 컬럼 추가
ALTER TABLE exercise ADD COLUMN weight int DEFAULT NULL;
ALTER TABLE exercise ADD COLUMN reps int DEFAULT NULL;
ALTER TABLE exercise ADD COLUMN sets int DEFAULT NULL;

-- 외래키 설정 01/23 추가
ALTER TABLE exercise ADD FOREIGN KEY (`user_id`) REFERENCES `users_app_user` (`id`);
-- postNum 자동 증가로 변경
ALTER TABLE exercise DROP PRIMARY KEY;
ALTER TABLE exercise MODIFY COLUMN postNum BIGINT AUTO_INCREMENT PRIMARY KEY;
```
### venv 설치 패키지 - 방성준 (2024-02-01)
    > pip install pandas==2.0.0
      pip install scikit-learn==1.3.0

### 브랜치명 (lim) - 임덕현 (2024-01-22 16:50)
    > 나의 식단 히스토리 페이지 추가(meal_history)
      * 일단은 데이터가 몇개 없어서 전체 기간으로 그래프 그렸고 협의후 옵션 지정 예정

    > 식단 상세 페이지 추가(meal_detail)
      * 섭취한 총 칼로리, 영양소 정보 추가로 부족한 영양소 계산해서 넣을 예정

### 브랜치명 (lim) - 임덕현 (2024-01-23)
     > 유저 정보에서 유저 활동 수준 구분을 5개로 수정 (("5", "매 활발한 활동"),("4","활발한 활동"),("3","보통 활동"),("2","약간의 활동"), ("1","거의 활동이 없음")))

     > 기존 데이터의 경우 오류가 날수 있기때문에 업데이트 필요
     > UPDATE users_app_user
        SET user_activity = CASE 
          WHEN user_activity = 'active' THEN '4'
          WHEN user_activity = 'deactive' THEN '2'
          ELSE '3'
        END;

     > Users_app_user 테이블 컬럼명 변경 : [user_age -> user_birth] 컬럼값에 생년월일이 들어가기 때문에 혼선을 줄 수 있어 컬럼명 변경. Alter문 실행 필요
        - Alter table users_app_user change user_age user_birth date 
        - 컬럼명이 바뀌었으므로 migration 필요

### 브랜치명 (lim) - 임덕현 (2024-01-26)
      > 식단 추천을 위한 Menu table Create
          create table menu(
            menu_id int not null auto_increment primary key,
              menu_type varchar(20), # 메뉴구분
              menu_classification varchar(20), # 식단 구분 
            menu_dtl varchar(100),
              calories float
          );
      
      > python manage.py inspectdb 명령어를 사용하여 models.py에 menu테이블 추가 필요

      > meal_hitory 페이지 그래프 기간 한달로변경 & 텍스트는 한달중 데이터가 있는 날짜 카운트
      
      > 따로 올린 기준을 바탕으로 메뉴 3개정도 select 해 추천해줄 예정 

### 브랜치명 (lim) - 임덕현 (2024-01-29)
      > 메인페이지의 회원가입1, 회원가입2중 현재 사용하는 회원가입2 -> 회원가입 변경, 회원가입1 주석처리
      
      > 로그인 안한 사용자에게 마이페이지 숨김 처리

      > meal_history페이지 식단 추천 추가 (7일간 먹은 칼로리 기준으로 일단 구현 조건 추가 예정)

      > meal_hitory, meal_detail페이지 css수정
      
