# ojijo

프로젝트 CRUD 게시판 및 로그인 기능 Flask

기한 : 2022년 12/2 ~ 12/8일까지


팀명 : 오지죠


팀장 : 정성욱<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ㄴ담당 페이지 : 마이페이지      

팀원 : 김민수<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ㄴ담당 페이지 : 게시글 상세보기 페이지
      
팀원 : 박종수<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ㄴ담당 페이지 : 게시글 작성 및 수정 페이지
      
팀원 : 이재관<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ㄴ담당 페이지 : 개인 정보 수정 페이지
      
팀원 : 표정훈<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ㄴ담당 페이지 : 메인 페이지

### 구현 요구 사항

- 기술 스택
    - HTML
    - CSS
    - JavaScript
    - MySQL
    - flask

- 기능 요구 사항
    - 로그인
    - 회원 가입
    - 게시판
    - 마이 페이지
    - 프로필 수정
    - 데이터 또는 게시판 Pagination


- 목표 가눙
  Login 기능 구현
  게시판 CRUD 기능 구현
  개인정보 수정 및 삭제 기능 구현
  
- 추가 목표
  미정
  
일정

2022.12.02 ~ 2022.12.05 각자 layout 만들기

2022.12.05 ~ 2022.12.06 layout 합 및 DB테이블 구현 git 연동

2022.12.06 ~ 2022.12.07 login기능 구현하기

2022.12.07 ~ 2022.12.08 CRUD기능 구현하기

2022.12.08 ~ 2022.12.09 에러사항 및 추가 수정사항변경하기

v1.0.0 - 레이아웃 만들기 합치기

v1.0.1 -로그인 기능 구현

v1.0.2 -CRUD구현 완료

v1.0.3 -남는시간 추가기능 하고 싶은 것 정해서 구현하기

-데이터 테이블(users,board)

  ```
create database ojijo;

use ojijo;

create table users(
    id int primary key auto_increment,
    user_id varchar(20) unique,
    user_pw varchar(100) not null ,
    user_name varchar(20) not null ,
    user_site varchar(50),
    user_email varchar(50),
    user_nk varchar(10) unique not null ,
    user_fp varchar(50),
    user_img varchar(200),
    user_del int
);

create table board(
    id int primary key auto_increment,
    bd_title varchar(50) not null ,
    bd_content varchar(8000) not null,
    bd_writeDate datetime,
    bd_updateDate datetime,
    user_nk varchar(20)
);

alter table board add constraint foreign key(user_nk)references users(user_nk);
```


- **회원 기능**
    - [✅]  회원 가입, 로그인 구현
    - [✅]  마이 페이지 프로필 수정 구현
    - [✅]  비밀번호 DB에 암호화 -보류

- **DB**
    - [✅]  MySQL 정규화 작업
    - [✅]  MySQL Join 쿼리문을 활용 하여 데이터 전달

- **CRUD**
    - [✅]  게시글 쓰기 기능 구현
    - [✅]  게시글 글 보여주기 구현
    - [✅]  게시글 글 수정 구현
    - [✅]  게시글 글 삭제 구현

- **GIT** 2022-12-06 설정 완료
    - [✅]  git add / commit / push 활용
    - [✅]  git pull / merge 활용

