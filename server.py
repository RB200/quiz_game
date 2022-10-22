import socket
from threading import Thread
import random

questions = [
    'Which country gifted the Statue of Liberty to the US?\nA.) France\nB.) Germany\nC.) Canada\nD.) China\n',
    'How many bones are there in the human body?\nA.) 200\nB.) 203\nC.) 206\nD.) 209\n',
    'Which U.S. state is known for peaches?\nA.) North Carolina\nB.) Nebraska\nC.) Maine\nD.) Georgia\n',
    'Steve Harvey is a game show host. What’s that show called?\nA.) Jeopardy!\nB.) Family Feud\nC.) Wheel of Fortune\nD.) Chain Reaction\n',
    'Who is the author of the Harry Potter series?\nA.) Dan Brown\nB.) J.R.R Tolkien\nC.) Charles Dickens\nD.) JK Rowling\n',
    'What is the name of the character that Johnny Depp plays in Pirates of the Caribbean?\nA.) John Wick\nB.) Superman\nC.) Jack Sparrow\nD.) Spiderman\n',
    'What has a gravitational pull so strong that light cannot even escape it?\nA.) Black Hole\nB.) White Dwarf Star\nC.) Supernova\nD.) Planet\n',
    'Which U.S. State is the largest?\nA.) Texas\nB.) California\nC.) Alaska\nD.) New York\n',
    'How many days are in a leap year?\nA.) 365\nB.) 366\nC.) 367\nD.) 368\n',
    'Who founded Microsoft?\nA.) Tom Cruise\nB.) Elon Musk\nC.) Steve Jobs\nD.) Bill Gates\n',
    'What are the 3 primary colors?\nA.) Red, Yellow, Blue\nB.) Green, Red, Orange\nC.) White, Black, Red\nD.) Blue, White, Red\n',
    'What is the name of the author who wrote The Great Gatsby?\nA.) J.R.R Tolkien\nB.) JK Rowling\nC.) F. Scott Fitzgerald\nD.) Dan Brown\n'
]

answers = ['a','c','d','b','d','c','a','c','b','d','a','c']

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


ip = '127.0.0.1'
port = 8000

server.bind((ip,port))
server.listen()

clients = []

def get_random_question_answer(con):
    r = random.randint(0,(len(questions)-1))
    q = questions[r]
    a = answers[r]
    con.send(q.encode('utf-8'))
    return r, q, a

def remove_question(idx):
    questions.pop(idx)
    answers.pop(idx)

def clientthread(con,add):
    score = 0
    con.send('Welcome to the game!\n'.encode('utf-8'))
    con.send('You will receive a question, the answer is either A, B, C, or D.\n'.encode('utf-8'))
    con.send('Good Luck!\n'.encode('utf-8'))
    idx, question, answer = get_random_question_answer(con)
    while True:
        try:
            message = con.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer: 
                    score += 1
                    con.send(f'Bravo! Your score is {score}\n'.encode('utf-8'))
                else:
                    con.send('Incorrect answer! Better luck next time.\n'.encode('utf-8'))
                remove_question(idx)
                idx, question, answer = get_random_question_answer(con)
                print(message)
            else:
                remove(con)
            
        except: 
            continue

while True:
    con,add = server.accept()
    thread = Thread(target=clientthread,args=(con,add))
    clients.append(con)
    thread.start()
    
