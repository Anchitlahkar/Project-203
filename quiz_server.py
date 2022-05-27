import socket
import random
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

print("server started")

list_of_clients = []
nicknames = []

questions = [
    "Hitler party which came into power in 1933 is known as\nA. Labour Party\nB. Nazi Party\nC. Ku-Klux-Klan\nD. Democratic Party\n\n",
    "For which of the following disciplines is Nobel Prize awarded?\nA.Physics and Chemistry\nB. Physiology or Medicine\nC. Literature, Peace and Economice\nD. All of the above\n\n",
    "Garampani sanctuary is located at?\nA. Junagarh, Gujarat\nB. Diphu, Assam\nC. Kohima, Nagaland\nD. Gangtok, Sikkim\n\n",
    "Eritrea, which became the 182nd member of the UN in 1993, is in the continent of\nA. Asia\nB. Africa\nC. Europe\nD. Australia\n\n",
    "Entomology is the science that studies\nA. Behavior of human being\nB. Insect\nC. The origin and history of technical and scientific term\nD. The formation of rocks\n\n",
    "Grand Central Terminal, Park Avenue, New York is the world's\nA. largest railway station\nB. highest railway station\nC. longest railway station\nD. None of the above\n\n",
    "How many Lok Sabha seats belong to Rajasthan?\nA. 4\nB. 2\nC. 3\nD. 17\n\n",
    "India has largest deposits of ____ in the world.\nA. gol\nB. coppe\nC. mic\nD. None of the above",
    "ICAO stands for?\nA. International Civil Aviation Organizatio\nB. Indian Corporation of Agriculture Organizatio\nC. Institute of Company of Accounts Organizatio\nD. None of the above\n\n"
    "In which year of First World War Germany declared war on Russia and France?\nA. 1914\nB. 1915\nC. 1916\nD. 1917\n\n"
]

answer = ["a", "b", "b", "b", "d", "b", "b", "c", "a", "a"]

no_ques = len(questions)+1

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def get_random_question(conn):
    rand_index = random.randint(0, len(questions)-1)
    rand_question = questions[rand_index]
    ques_ans = answer[rand_index]

    conn.send(rand_question.encode("utf-8"))
    return rand_index, rand_question, ques_ans


def remove_ques(idx):
    questions.pop(idx)
    answer.pop(idx)


def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


def clientthread(conn, nick_name):
    score = 0
    conn.send("Welcome to this quiz room !!!!".encode('utf-8'))
    conn.send("Answer Questions Correctly\n".encode('utf-8'))
    conn.send("Good Luck\n\n".encode('utf-8'))

    idx, ques, ans = get_random_question(conn)

    while True:
        if len(questions)-1 != 0:
            try:
                message = conn.recv(2048).decode('utf-8')
                if message:
                    msg=message.split(":")[1].lower()
                    msg.replace(" ", "")


                    if msg == ans:
                        score += 1
                        conn.send(
                            f"\nCorrect Answer, Good Job!!!\n\n".encode("utf-8"))

                    else:
                        conn.send(
                            f"\nIncorrect Answer. Try Again!!!\n\n".encode("utf-8"))

                    remove_ques(idx)

                    idx, ques, ans = get_random_question(conn)

                else:
                    remove(conn)
                    remove_nickname(nick_name)

            except:
                continue

        else:
            conn.send(f"\n\n\nScore: {score}/{no_ques}".encode("utf-8"))
            print(f"{nick_name} Scored: {score}/{no_ques}")
            break


while True:
    conn, addr = server.accept()

    conn.send('NICKNAME'.encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    print(f"{nickname} joined")

    list_of_clients.append(conn)

    new_thread = Thread(target=clientthread, args=(conn, nickname))
    new_thread.start()
