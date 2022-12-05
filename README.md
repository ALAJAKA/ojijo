# ojijo

프로젝트 CRUD 게시판 및 로그인 기능 Flask

기한 : 2022년 12/2 ~ 12/8일까지

팀명 : 오지죠<br>

팀장 : 정성욱<br>
&nbsp&nbsp&nbsp&nbspㄴ담당 페이지 : 마이페이지<br>
팀원 : 김민수<br>
      ㄴ담당 페이지 : 게시글 상세보기 페이지<br>
팀원 : 박종수<br>
      ㄴ담당 페이지 : 게시글 작성 및 수정 페이지<br>
팀원 : 이재관<br>
      ㄴ담당 페이지 : 개인 정보 수정 페이지<br>
팀원 : 표정훈<br>
      ㄴ담당 페이지 : 메인 페이지<br>

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
  
-데이터 테이블(users,board)
  
create table users(
    id int primary key auto_increment,
    user_id varchar(20) unique,
    user_pw varchar(20) not null ,
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

