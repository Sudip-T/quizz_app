import random
import json


total_score = 0
correct_score = 0
incorrect_score = 0
# total_question = len(question_bank)

correct_answer_list = []
incorrect_answer_list = []
quiz_type = ['Random Questions', 'Category Specific Questions']
dashboard_action = ['Show Score', 'Show Correctly Answered', 'Show Incorrectly Answered','Exit']



with open('question_bank.json', 'r') as file:
    question_data = json.load(file)



def showAnswer(ciAnswer_list):
    print()
    for indx,indi_data in enumerate(ciAnswer_list):
        print(indx +1,f'Question - {indi_data[0]} || Correct Answer - {indi_data[1]} || Your Answer - {indi_data[2]}')



def messages(messageType, opt='none'):
    if messageType == 'pc':
        return 'Enter your preferred quizz category..._____'
    if messageType == 'ae':
        return 'Action cannot be empty.'
    elif messageType == 'cafl':
        return 'Choose one of the action from list.'
    elif messageType == 'farewell':
        return 'Thank you for using this app...'
    elif messageType == '0qnr':
        return 'You got none of questions right. Better luck next time!'
    elif messageType == 'alltrue':
        return 'You got all questions right. Great Job!'
    elif messageType == 'fainp':
        return 'Choose one of the following action to proceed : '
    elif messageType == 'qsinp':
        return 'Enter your preferred action: '
    elif messageType == 'ecn':
        return 'Enter number between displayed range.'
    

def quizType_selection(data):
    print('---------------------------------------')
    print('Choose one of the following to proceed.')
    for index, option in enumerate(data):
        print(index+1,option)
    print('---------------------------------------')


def determineUserChoice(quiz_type, msg_type):
    quizType_selection(quiz_type)
    user_choice = input(messages(msg_type))
    if user_choice.isnumeric():
        if int(user_choice) > 0 and int(user_choice) <= len(quiz_type):
            user_choice = int(user_choice)-1
            return user_choice
        else:
            print(messages('ecn'))
            return determineUserChoice(quiz_type, msg_type)
    elif user_choice.title() in quiz_type:
        user_choice = quiz_type.index(user_choice.title())
        return user_choice
    else:
        if user_choice != '':
            print(messages('cafl'))
        else:
            print(messages('ae'))
        return determineUserChoice(quiz_type, msg_type)



# it prints options for question being asked
def print_option(options):
    for option in options:
        print(option)



def user_input(random_question):
    print(random_question[0])
    print_option(random_question[2])
    user_answer = input('Enter (A, B, C): ').upper()
    if user_answer in ['A', 'B', 'C']:
        return user_answer
    else:
        print('-----------------------------')
        print('Enter option as A or B or C')
        print('-----------------------------')
        user_input(random_question)


# this function appends displayed questions and user inputted answer
def qaAppending(ansList, question, user_answer):
    '''
    this function takes correct or incorrect answer list and appends questions and answers accordingly.
    '''
    # user_ans_index = question[2].index(question[2].startswith)
    for i in question[2]:
        print(i)
    ansList.append((question[0], question[1][2:], user_answer))



def quizzBody(default_category='none'):
    global total_score, correct_score, incorrect_score, correct_answer_list, incorrect_answer_list
    for i in range(5):
        if default_category == 'none':
            random_category = random.choice(list(question_data))
            random_question = random.choice(question_data[random_category])
        else:
             random_question = random.choice(question_data[default_category])
        print('--------------------------------------')
        user_inpRt = user_input(random_question)
        if user_inpRt == random_question[1][0]:
            print('user input is',user_inpRt[0])
            total_score +=1
            correct_score +=1
            qaAppending(correct_answer_list, random_question, user_inpRt)
        else:
            total_score -=1
            incorrect_score +=1
            qaAppending(incorrect_answer_list, random_question, user_inpRt)
            
            
        if default_category == 'none':
            de = question_data[random_category].index(random_question)
            del question_data[random_category][de]
        else:
            de = question_data[default_category].index(random_question)
            del question_data[default_category][de]



def initilizeAction(user_choice):
    if user_choice == quiz_type.index('Random Questions'):
        print(f'Great! Here are 5 random questions from categories {[key for key in question_data.keys()]}...')
        quizzBody()
    
    elif user_choice == quiz_type.index('Category Specific Questions'):
        print('-----------------------------------')
        for i,c in enumerate([key for key in question_data.keys()]):
            print(i+1,c)
        category_selection = int(input(messages('pc')))-1
        quizzBody(list(question_data)[category_selection])
    elif user_choice == quiz_type.index('Exit'):
        print(messages('farewell'))



def performUserAction():
    initilizeAction(determineUserChoice(quiz_type, 'qsinp'))
    dashaction_user = determineUserChoice(dashboard_action, 'fainp')
    print(dashaction_user)
    
    
performUserAction()
