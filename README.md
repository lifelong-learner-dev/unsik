# FINAL PROJECT (2023.12.13 ~ )

## 주제 : 운동, 식단 관리 사이트 개발 

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

### 브랜치명 (lim) - 임덕현 (2024-01-22 16:50)
    > 나의 식단 히스토리 페이지 추가(meal_history)
      * 일단은 데이터가 몇개 없어서 전체 기간으로 그래프 그렸고 협의후 옵션 지정 예정

    > 식단 상세 페이지 추가(meal_detail)
      * 섭취한 총 칼로리, 영양소 정보 추가로 부족한 영양소 계산해서 넣을 예정
