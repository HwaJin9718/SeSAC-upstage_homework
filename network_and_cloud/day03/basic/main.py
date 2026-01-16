import os
from logging import INFO

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
import mysql.connector
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

# ---------------------------
# [TASK 1] 로그 저장 폴더 생성
# ---------------------------
# TODO: "logs"라는 이름의 폴더를 생성해주세요!
# Hint: os.makedirs()를 활용하면 됩니다. 이미 폴더가 있어도 에러가 나지 않도록 exist_ok=True 옵션 사용
# 이 부분을 채워주세요!
os.makedirs("logs", exist_ok=True)

# ---------------------------
# [TASK 2] 로그 포맷 및 핸들러 설정
# ---------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"

# TODO: LOG_FORMAT을 사용하여 formatter를 생성하세요
# Hint: logging.Formatter()를 사용하여 LOG_FORMAT을 전달
formatter = logging.Formatter(LOG_FORMAT)  # 이 부분을 채워주세요!

file_handler = RotatingFileHandler(
    # TODO: 로그 파일 경로를 지정하세요 (logs 폴더 안에 app.log 파일)
    # Hint: "logs/파일명.확장자" 형식으로 작성
    filename="logs/app.log",  # 이 부분을 채워주세요!

    # TODO: 로그 파일의 최대 크기를 바이트 단위로 지정하세요
    # Hint: 1MB = 1024 * 1024 바이트
    maxBytes=1024*1024,  # 이 부분을 채워주세요!

    # TODO: 보관할 백업 파일 개수를 지정하세요
    # Hint: 5개의 백업 파일을 유지하려면?
    backupCount=5,  # 이 부분을 채워주세요!

    encoding="utf-8"
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# ---------------------------
# [TASK 3] 루트 로거 통합 설정
# ---------------------------
root_logger = logging.getLogger()

# TODO: 로그 레벨을 INFO로 설정하세요
# Hint: logging 모듈의 INFO 상수를 사용하세요
root_logger.setLevel(INFO)  # 이 부분을 채워주세요!

# TODO: 파일 핸들러를 루트 로거에 추가하세요
# Hint: addHandler() 메서드를 사용하여 file_handler를 추가
root_logger.addHandler(file_handler)  # 이 부분을 채워주세요!

# TODO: 콘솔 핸들러를 루트 로거에 추가하세요
# Hint: addHandler() 메서드를 사용하여 console_handler를 추가
root_logger.addHandler(console_handler)  # 이 부분을 채워주세요!

logging.getLogger("uvicorn").handlers = root_logger.handlers
logging.getLogger("uvicorn.access").handlers = root_logger.handlers


### FastAPI 애플리케이션 객체 생성 (API 서버의 시작점)
app = FastAPI()

### DB 연결을 생성하는 함수 (요청마다 MySQL과 연결)
def get_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


# ---------------------------
# CREATE
# ---------------------------
@app.post("/todos")
async def create_todo(request: Request):
   ### 요청 body(JSON) 파싱
   body = await request.json()
   content = body.get("content")

   ### 필수 값 검증 (content 없으면 에러 반환)
   if not content:
       # TODO: ERROR 레벨로 로그를 기록하세요
       # Hint: logging.error()를 사용하여 "제목이 없는 할 일 생성 시도: content missing" 메시지 기록
       logging.error("content missing") # 이 부분을 채워주세요!
       raise HTTPException(status_code=400, detail="content is required")

   ### DB 연결 및 SQL 실행 준비
   conn = get_db()
   cursor = conn.cursor()

   # INSERT
   # insert into ~ values ~ 절을 활용하여 todoList row를 삽입합니다.
   # insert into todo : todo 테이블에 새로운 데이터를 삽입하겠다는 의미
   # (content) values (%s) content 컬럼에 values 다음에 올 값을 넣겠다는 의미
   # , (content,) content string값을 %s 자리에 대입한다는 의미
   cursor.execute(
       "INSERT INTO todo (content) VALUES (%s)",
       (content,)
   )

   ### INSERT 결과를 DB에 실제 반영
   conn.commit()

   ### 방금 생성된 row의 PK(id) 값 가져오기
   todo_id = cursor.lastrowid

   # TODO: INFO 레벨로 로그를 기록하세요
   # Hint: logging.info()를 사용하여 "새로운 할 일 생성 완료: ID {todo_id}" 메시지 기록 (f-string 사용)
   logging.info(f"Todo 생성 완료 / todo 번호 : {todo_id}")  # 이 부분을 채워주세요!

   # SELECT (방금 생성한 todo 조회)
   # select ~ from ~ where 절을 이용하여 방금 삽입한 todo 를 불러옵니다.
   # SELECT id, content, created_at : id,content,create_at값을 불러오겠다는 의미
   # FROM todo : todo 테이블에서 값을 불러오겠다는 의미
   # WHERE id = %s : id가 %s인값을 불러오겠다는 의미
   # , (todo_id,) : %s에 todo_id값을 대입하겠다는 의미
   cursor.execute(
       "SELECT id, content, created_at FROM todo WHERE id = %s",
       (todo_id,)
   )
   row = cursor.fetchone()

   ### DB 연결 종료
   cursor.close()
   conn.close()

   ### 생성된 todo 데이터를 JSON 형태로 반환
   return {
       "id": row[0],
       "content": row[1],
       "created_at": str(row[2])
   }

# ---------------------------
# READ
# ---------------------------
@app.get("/todos")
def get_todos():
   ### DB 연결
   conn = get_db()
   cursor = conn.cursor()

  # 전체 조회
  # select ~ from ~ order by ~ 를 활용하여 전체 todo list를 만든 최근에 만든 순으로 조회합니다.
  # SELECT id, content, created_at : id,content,create_at값을 불러오겠다는 의미
  # FROM todo : todo 테이블에서 값을 불러오겠다는 의미
  # ORDER BY id DESC  id값 기준 내림차순으로 정렬하겠다는 의미
   cursor.execute(
       "SELECT id, content, created_at FROM todo ORDER BY id DESC"
   )
   rows = cursor.fetchall()

   ### DB 연결 종료
   cursor.close()
   conn.close()

   if len(rows) == 0:
       logging.info("전체 조회 목록 없음")
   else:
       logging.info(f"전체 조회 목록 {len(rows)}건")

   ### 여러 개의 row를 JSON 리스트 형태로 변환하여 반환
   return [
       {
           "id": r[0],
           "content": r[1],
           "created_at": str(r[2])
       }
       for r in rows
   ]

# ---------------------------
# DELETE
# ---------------------------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
   ### URL 경로 변수(todo_id)로 삭제 대상 지정
   conn = get_db()
   cursor = conn.cursor()

   # DELETE
   # delete from ~ where ~ 절을 활용하여 todo list를 삭제합니다.
   # delete from todo : todo 테이블에서 값을 삭제하겠다는 의미
   # WHERE id = %s : id가 %s인값을 삭제하겠다는 의미
   # , (todo_id,) : %s에 todo_id값을 대입하겠다는 의미
   cursor.execute(
       "DELETE FROM todo WHERE id = %s",
       (todo_id,)
   )

   ### 삭제 결과 DB 반영
   conn.commit()

   ### 실제로 삭제된 행의 개수
   affected = cursor.rowcount

   ### DB 연결 종료
   cursor.close()
   conn.close()

   ### 삭제 대상이 없었을 경우 404 반환
   if affected == 0:
       logging.error(f"삭제 실패 / todo 번호 : {todo_id}")
       raise HTTPException(status_code=404, detail="Todo not found")

   logging.info(f"{todo_id}번 todo 삭제 완료")
   ### 삭제 성공 메시지 반환
   return {"message": "Todo deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
