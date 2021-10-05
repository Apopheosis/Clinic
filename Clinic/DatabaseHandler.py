import pymysql
from PyQt5.QtWidgets import *
from config import host, port, user, password, db_name

def Database_connect():
    try:
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print(connection)
    except Error as e:
        print(e)
    return connection

def insert_user(login, password, name, lastname, age, occupation):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        insert_user_query = "INSERT INTO users (login, password, name, lastname, age, occupation) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_user_query, (login, password, name, lastname, age, occupation))
    PrSt.commit()

def insert_patient(name, lastname, age, diagnosis):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        insert_user_query = "INSERT INTO patients (name, lastname, age, diagnosis) VALUES (%s, %s, %s, %s);"
        cursor.execute(insert_user_query, (name, lastname, age, diagnosis))
    PrSt.commit()

def insert_doctor(name, lastname, age):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        insert_user_query = "INSERT INTO doctors (name, lastname, age) VALUES (%s, %s, %s);"
        cursor.execute(insert_user_query, (name, lastname, age))
    PrSt.commit()

def insert_expert(name, lastname, age):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        insert_user_query = "INSERT INTO experts (name, lastname, age) VALUES (%s, %s, %s);"
        cursor.execute(insert_user_query, (name, lastname, age))
    PrSt.commit()

def fetch_user(login, password):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        select_users_query = "SELECT * FROM users WHERE login=%s AND password=%s;"
        cursor.execute(select_users_query, (login, password))
        result = cursor.fetchone()
    return result

def get_questions(table):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        select_questions_query = "SELECT * FROM " + table + ";"
        cursor.execute(select_questions_query)
        result = cursor.fetchall()
    return result

def send_questions(quest):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        send_questions_query = "INSERT INTO questions (qid, question, right_answer) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE question=%s, right_answer = %s"
        cursor.execute(send_questions_query, (quest[0], quest[1], quest[2], quest[1], quest[2]))
    PrSt.commit()

def send_answer(idquestion, answer, table):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        insert_answers_query = "UPDATE " + table + " SET answer = %s WHERE qid = %s;"
        cursor.execute(insert_answers_query, (answer, idquestion))
    PrSt.commit()

def delete_question(qobject):
    if qobject is not None:
        PrSt = Database_connect()
        with PrSt.cursor() as cursor:
            delete_question_query = "DELETE FROM questions WHERE qid = %s"
            cursor.execute(delete_question_query, (qobject.text()))
        PrSt.commit()

def create_question_list(idpat):
    idpat = str(idpat)
    table = "patient_" + idpat
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        create_table_query = """
    CREATE TABLE IF NOT EXISTS """ + table + """ (
            qid INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT,
            answer VARCHAR(45),
            right_answer VARCHAR(45)
        );
    """
        cursor.execute(create_table_query)
    PrSt.commit()
    

def fetch_doctors():
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        fetch_doctors_query = "SELECT * FROM doctors"
        cursor.execute(fetch_doctors_query)
        result = cursor.fetchall()
    return result

def fetch_experts():
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        fetch_experts_query = "SELECT * FROM experts"
        cursor.execute(fetch_experts_query)
        result = cursor.fetchall()
    return result

def fetch_patients():
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        fetch_patients_query = "SELECT * FROM patients"
        cursor.execute(fetch_patients_query)
        result = cursor.fetchall()
    return result

def get_patient_id(name,lastname,age):
    PrSt = Database_connect()
    with PrSt.cursor() as cursor:
        fetch_id_query = "SELECT idpatients FROM patients WHERE name=%s AND lastname=%s AND age=%s"
        cursor.execute(fetch_id_query, (name,lastname,age))
        result = cursor.fetchone()
    return result['idpatients']
    
