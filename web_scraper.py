# Leif Ekstrom
# ENGN2045
# Final Project
# Due: 4/20/2021

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

DEBUG_MODE = False # Enable if you want to save the website's source HTML locally

query = 'dog' # An example query for testing and debugging purposes


def get_translation(q):
    soup = get_HTML(q)
    
    # SEARCH VALIDATION SECTION-------------------------------------------------------
    # Check to see if the "Sorry, couldn't find anything matching ___" div is there
    # If it is, it means that either the query isn't a real word or there no Japanese translation exists
    errorTag = soup.find_all(id= 'no-matches')
    if errorTag:
        print("Sorry, couldn't find anything matching {}.".format(q))
        print("Either the query isn't a real word or there no Japanese translation exists!")
        return
    
    # FURIGANA SECTION----------------------------------------------------------------
    # This is the location where any furigana would be located   
    # This is a list of all of all the search results on the first page
    targetTag = soup.find_all(class_= 'concept_light clearfix') 
    # Navigate to the tag where the furigana is located for the first search result
    furigana = str(targetTag[0].find(class_='furigana'))
    # Number of characters when written with kanji
    charCount = furigana.count('<span')-1
    
    startFound = False
    furiganaList = []
    for i in range(len(furigana)-7):
        if furigana[i] == '<' and not startFound:
            if furigana[i+1] == 's' and furigana[i+2] == 'p' and furigana[i+3] == 'a' and furigana[i+4] == 'n':
                startFound = True
                startLoc = i
        elif furigana[i] == '<' and startFound:
            if furigana[i+1] == '/' and furigana[i+2] == 's' and furigana[i+3] == 'p' and furigana[i+4] == 'a' and furigana[i+5] == 'n':
                endLoc = i
                furiganaList.append(furigana[startLoc:endLoc])
                startFound = False
    
    # Create a list with the the furigana for each character
    # If there are no furigana for that location add '' instead
    for i in range(len(furiganaList)):
        # Regex the furigana into a non-HTML format
        furiganaList[i] = re.sub('<[^>]*>', '', furiganaList[i]).strip()

    # FULL TRANSLATION SECTION--------------------------------------------------------
    # Navigate to the tag where the translation is located for the first search result
    utcStr = str(targetTag[0].find(class_='text'))
    # Set of substrings to remove from utcStr
    replaceSet = {'<span>','</span>','<span class="text">','\n'}
        # This will remove all of the HTML tags and formatting, leaving only UTC-8 character bytes
    for item in replaceSet:
        utcStr = utcStr.replace(item,'')
    utcStr = utcStr.strip()

    # KANA SECTION--------------------------------------------------------------------
    # If there are any kanji in the translation, make a string using their respective furigana instead
    utcList = list(utcStr)
    kanaStr = ''
    for i in range(len(utcList)):
        if furiganaList[i] == '':
            kanaStr = kanaStr + utcList[i]
        else:
            kanaStr = kanaStr + furiganaList[i]
    
    # NUMBER OF SEARCH RESULTS SECTION------------------------------------------------
    #numberTag = str(soup.find_all(class_='result_count'))
    numberTag = soup.find_all(class_='result_count')
    numRes = str(numberTag[0])
    #print(numRes.dtype)
    numRes = re.sub('<[^>]*>', '', numRes).strip().split()[1]
    print(numRes)
    
    # RESULT SECTION------------------------------------------------------------------
    # Write the result to a text file
    with open("translation_result.txt", "w", encoding='utf-8') as file:
        file.write('Searched Word: {}\n'.format(format_query(q)))
        file.write('Japanese Translation: {}\n'.format(utcStr))
        file.write('Kana: {}\n'.format(kanaStr))
        file.write('Number of Translation Results Found: {}'.format(numRes))

    # Print results to the console
    print_results()
    
      
def print_results():
    # Open the text file and print the results to the console
    print('Please check the text file translation_result.txt to see the translation!')
    
    # CURRENTLY THIS IS UNSTABLE AND SOMETIMES CAUSES CRASHING! DO NOT UNCOMMENT UNTIL THIS IS RESOLVED!
    # Cause of crashes: 
    #   UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 53: character maps to <undefined>
    # For whatever reason, Windows is 'special' and decides to throw a hissy fit when asked to display some non-standard non-aplhanum chars.
    # I believe that this is because Microsoft never added non-ASCII char support for the command line, and kanji are UTF-8 with no ASCII equivalent.
    # As of now, the translation results can be seen in the translation_result.txt file.
   
    # f = open('translation_result.txt', 'r')
    # fContents = f.read()
    # print(fContents)
    # f.close()

      
def get_HTML(q):
    # Obtain the source HTML of the relevant search page
    url = get_URL(q)
    page = urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html,'html.parser')
    
    # THIS IS FOR TESTING AND DEBUGGING PURPOSES!!!
    # Save the source HTML code to a local file for easy reading and debugging
    if DEBUG_MODE:
        with open("output1.html", "w", encoding='utf-8') as file:
            file.write(str(soup))
    
    return soup    

    
def get_URL(q):
    # Obtain the URL of the relevant search page
    url = 'https://jisho.org/search/' + format_query(q)
    return url


def format_query(q):
    # Convert the text to a format that can be searched via the website URL
    # The query must be fully lowercase with quotation marks surrounding it
    return '"' + q.lower() + '"'


def main():
    get_translation(query)
    

if __name__=="__main__": 
    main()