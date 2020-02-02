'''
-- PORN HANG
Hangman Game that works by scraping random comment from pornhub
'''
import requests, logging
from bs4 import BeautifulSoup
from random import choices
from datetime import datetime
import os
from math import ceil
#from IPython.display import clear_output #otebook
import time

from ascci_text import man, banner

logging.basicConfig(level=logging.INFO)

class HangMan:    
    '''
    Main class that contains all the methods for the game
    '''
    def comment(self):
        '''
        Get the comment from pornhub
        '''
        comment = ''
        while comment == '' or comment == '[[commentMessage]]':
            logging.info("Sending Request..")
            source = requests.get('https://www.pornhub.com/random')
            logging.info(source.status_code)
            soup = BeautifulSoup(source.text, 'lxml')
            logging.info("Parsing information\nRetrieving Comment")
            commentBlock = soup.find('div', class_='commentBlock')

            if commentBlock is None:
                self.comment()

            comment = commentBlock.find('div', class_='commentMessage').span.text
            
            if comment == '' or comment =='[[commentMessage]]':
                logging.info("No comments found. Retrying")
                
        return comment.lower()
        logging.info("Success!!")
            
    
    def display(self, answer, error):
        '''
        Display the output to the user for every input
        '''
        #clear_output() #inpython
        os.system('cls') #windows
        #os.system('clear') #linux
        
        print(banner) 
        
        print(man[error]) 
        
        for ans in answer:
            print(ans, end=' ')

        print('\n')

        
    def user_info(self):
        '''
        Get the user's name from user
        and save it records.txt file
        '''
        name = input("Enter your name: ")
        print()
        now = datetime.now()
        now = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('records.txt', 'a') as f:
            f.write('Name: ' + name)
            f.write('Time: ' + now)
            f.write('\n------------------------\n')

            
    def win(self, temp_comment):  
        '''
        If the user wins the game 
        '''      
        #clear_output() #ipython
        os.system('cls') #windows
        #os.system('clear') #linux
        
        print(f'''Yahoo!!! You correctly guessed the comment. The comment was\n------------------- \n"{temp_comment}"\n----------------\n
        Congratulations. Press 'R' to replay? \nPress  'Q' to quit. ''')

        action = input()
        if action.lower() == 'r':
            self.play()
        else:
            #clear_output()
            os.system('cls') #windows
            #os.system('clear') #linux
            

    def lose(self, temp_comment):
        '''
        if the user loses the game
        '''
        #clear_output()
        os.system('cls') #windows
        #os.system('clear') #linux
        print(f'Sorry! You Failed. The comment was\n------------------ \n"{temp_comment}"\n---------------------\n')

        print("Press 'R' to retry.")
        print("or Press any key to quit.")

        action = input()

        if action.lower() == 'r':
            self.play()
        else:
            #os.system('cls') #windows
            #os.system('clear') #linux
            clear_output()
    
    def play(self):
        '''
        Main method that calls other method and plays the game
        '''
        error = 0
        temp_comment = self.comment() #call comment method
        comment = list(temp_comment.lower())
        answer = ['_']*len(comment)
        self.user_info() #call user_info method
        
        while True:
            self.display(answer, error) #call display method
            guess = input()
            print()
            guess = guess.lower() 
            
            if guess not in comment:
                error += 1 #increase error
                
            if len(guess) == 1 and guess in comment: 
                occurence = comment.count(guess)
                for i in range(occurence):
                    index = comment.index(guess)
                    answer[index] = guess
                    comment[index] = ''
                
            elif len(guess) != 1:
                print('You must enter only a word')
                time.sleep(1)
            
            
            # Win
            if ''.join(comment) == '':
                self.win(temp_comment) #call win method
                break
            
            #lose
            if error > 6:
                self.lose(temp_comment) #call lose method
                break

if __name__ == '__main__':
    #Create object and call the play method
    hang = HangMan().play()
    