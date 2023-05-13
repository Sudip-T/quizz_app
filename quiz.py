import random
import json


total_score = 0
correct_score = 0
incorrect_score = 0

correct_answer_list = []
incorrect_answer_list = []
quiz_type = ['Random Questions', 'Category Specific Questions']
dashboard_action = ['Show Score', 'Show Correctly Answered', 'Show Incorrectly Answered','Exit']


with open('question_bank.json', 'r') as file:
    question_data = json.load(file)


def showAnswer(ciAnswer_list):
    '''it displays correct or incorrect answer list'''
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
    elif messageType == 'ch':
        return 'Choose one of the following to proceed.'
    

def displayBoard(data):
    print('---------------------------------------')
    print(messages('ch'))
    for index, option in enumerate(data):
        print(index+1,option)
    print('---------------------------------------')


def determineUserChoice(dashboard_type, msg_type):
    '''it first displays board. then it prompts for user input. if user input is numeric and within the range of data length, it converts into int and returns
       user input. or if user input is in dashboard_type, it returns the index of user input. if not, it display what's to be done and recalls function
    '''
    displayBoard(dashboard_type)
    user_choice = input(messages(msg_type))
    if user_choice.isnumeric():
        if int(user_choice) > 0 and int(user_choice) <= len(dashboard_type):
            user_choice = int(user_choice)-1
            return user_choice
        else:
            print(messages('ecn'))
            return determineUserChoice(dashboard_type, msg_type)
    elif user_choice.title() in dashboard_type:
        user_choice = dashboard_type.index(user_choice.title())
        return user_choice
    else:
        if user_choice != '':
            print(messages('cafl'))
        else:
            print(messages('ae'))
        return determineUserChoice(dashboard_type, msg_type)


def print_option(options):
    "it receives question in play's options and simply prints"
    for option in options:
        print(option)


def user_input(random_question):
    '''it first print the question located at index 0. Then display options, receives and returns user choice as A, B or C'''
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
    ansList.append((question[0], question[1][2:], user_answer))


def quizzBody(default_category='none'):
    '''it first randomly chooses question either from random category and specific category. then it receives user input that manipulated by user_input().
       if user correctly answers, score is adjusted accordingly and answer is added to correct_answer_list through qaAppending(). else score is adjusted 
       accordingly and incorrect_answer_list appended. lastly, it deletes question being asked from list so not to have repetition
    '''
    global total_score, correct_score, incorrect_score, correct_answer_list, incorrect_answer_list, total_question
    for i in range(5):
        if default_category == 'none':
            random_category = random.choice(list(question_data))
            random_question = random.choice(question_data[random_category])
        else:
             random_question = random.choice(question_data[default_category])
        print('--------------------------------------')
        user_inpRt = user_input(random_question)
        if user_inpRt == random_question[1][0]:
            total_score +=1
            correct_score +=1
            qaAppending(correct_answer_list, random_question, user_inpRt)
        else:
            total_score -=1
            incorrect_score +=1
            qaAppending(incorrect_answer_list, random_question, user_inpRt)
            
            
        if default_category == 'none':
            del_question = question_data[random_category].index(random_question)
            del question_data[random_category][del_question]
        else:
            del_question = question_data[default_category].index(random_question)
            del question_data[default_category][del_question]


def initilizeAction(user_choice):
    '''this function runs quizbody() based on user selection, either random questions or category specific question. 
       if user choose category specific question, available categorie/s is/are displayed and quizbody() is invoked passing selected category. 
    '''
    if user_choice == quiz_type.index('Random Questions'):
        print(f'Great! Here are 5 random questions from categories {[key for key in question_data.keys()]}...')
        quizzBody()
    
    elif user_choice == quiz_type.index('Category Specific Questions'):
        print('-----------------------------------')
        for i,c in enumerate([key for key in question_data.keys()]):
            print(i+1,c)
        category_selection = int(input(messages('pc')))-1
        quizzBody(list(question_data)[category_selection])


def dashBoardAction(dash_action):
    '''it performs dashboard action invoking different function. it also calls itself after certain function is performed'''
    if dash_action == 0:
        print('------------------------------------')
        print(f'Your total score is {total_score}.')
        dashBoardAction(determineUserChoice(dashboard_action, 'fainp'))
    elif dash_action == 1:
        print('-----------------')
        if len((correct_answer_list)) <= 0:
            print(messages('0qnr'))
        else:
            print(f'You got {len(correct_answer_list)} question/s right.')
            showAnswer(correct_answer_list)
        dashBoardAction(determineUserChoice(dashboard_action, 'fainp'))
    elif dash_action == 2:
        print('-----------------')
        if len((incorrect_answer_list)) <= 0:
            print(messages('alltrue'))
        else:
            print(f'You got {len(incorrect_answer_list)} question/s incorrect.')
            showAnswer(incorrect_answer_list)
        dashBoardAction(determineUserChoice(dashboard_action, 'fainp'))
    else:
        print('-' * len(messages('farewell')) ) 
        print(messages('farewell'))


def performUserAction():
    '''this function invokes two functions. first function invokes another function that further calls many other functions. it basically runs quizbody()
       that does quiz and save scores accordingly and append correct and incorrect answer. second function also invokes another function that performs action
       as such showing score, correct or incorrect answer list, exit
    '''
    initilizeAction(determineUserChoice(quiz_type, 'qsinp'))
    dashBoardAction(determineUserChoice(dashboard_action, 'fainp'))
    
    
performUserAction()