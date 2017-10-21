'''
Alex Schlumpf
11/16/16
I pledge my honor that I have abided by the Stevens Honor System.
'''
DATA = {}

def read_prefs(filename):
    '''Assume filename is path to an existing file in the format above.
       Print each user name and a list of the user's prefs.'''
    input_file = open(filename, 'r')   # Open the file for reading.
    for line in input_file:# Get one line at a time.
        if line != '\n':
            user, artists = line.split(':')
            artists = artists.split(',')
            for i in range(len(artists)):
                artists[i] = artists[i].strip()
            user = user.strip()
            DATA[user]=artists
    input_file.close() # Important - do not forget to close the file

def write_prefs(filename):
    '''Open existing or new file named filename.
       Write SAMPLE_FILE_CONTENT to it.'''
    output_file = open(filename, 'w')
    line = []
    for user in DATA:
        s = user+':'
        for artist in DATA[user]:
            s = s + artist+','
        line+=[s[:-1]]
    for l in line:
        output_file.write(l + '\n')
    output_file.close()

def allMatches(L1, L2):
    ''' Calculates all matching strings in that two lists share. '''
    L1.sort()
    L2.sort()    
    count = 0
    i = 0
    j = 0
    while i < len(L1) and j < len(L2):
        if L1[i] == L2[j]:
                i += 1
                j += 1
                count += 1
        elif L1[i] > L2[j]:
                j += 1
        else:
                i += 1
    return count

def matchNum(L1, L2):
    ''' Calculates the number of matches two lists share. '''
    L1.sort()
    L2.sort()    
    count = 0
    i = 0
    j = 0
    while i < len(L1) and j < len(L2):
        if L1[i] == L2[j]:
                i += 1
                j += 1
                count += 1
        elif L1[i] > L2[j]:
                j += 1
        else:
                i += 1
    return count    

def dropMatches(L1, L2):
    ''' Returns a list of elements from L1 who don't match between L1 and L2. If L1 and L2 share no matches, the empty list is returned.''' 
    if matchNum(L1, L2) == 0:
        return []
    else:
        new_list=[]
        L1.sort()
        L2.sort()
        i=0
        j=0
        while i < len(L1) and j < len(L2):
            if L1[i] == L2[j]:
                i+=1
                j+=1
            elif L1[i]<L2[j]:
                new_list.append(L1[i])
                i+=1
            else:
                j+=1
        while i < len(L1):
            new_list.append(L1[i])
            i+=1
        while j < len(L2):
            j+=1
        return new_list


def dictToL():
    ''' Converts the dictionary DATA to a list of form [[User, [artists]] '''
    L = []
    for user in  DATA:
        L.append([user, DATA[user]])
    return L

def compare(user):
    ''' Compares the artist likes the entered user has to the artists every other user in DATA likes, and returns a list of the other users along with how many artist likes they share, as well
    as the amount they don't share. '''
    user_artists = DATA[user]
    L = dictToL()
    output = []
    for i in range(len(L)):
        if user == L[i][0]:
            continue
        matches = matchNum(user_artists, L[i][1])
        output.append([L[i][0], matches, len(L[i][1]) - matches])
    return output

def maxValUserRec(users):
    ''' MaxValUser specifically for getRec(), as it takes into account a third parameter which is the amount of remaining users after those which match between two users are dropped. 
    Users with no remaining artists are eliminated. In the case where multiple users share the max matches, the user who has the most remaining artists is returned.''' 
    max_val = users[0]
    for x in users:
        if x[2] == 0:
            continue
        elif x[1] > max_val[1]:
            max_val = x
        elif x[1] == max_val[1] and x[2] > max_val[2]:
            max_val = x
    return max_val


def maxValUser(users):
    ''' Calculates the user/artist with the maximum value at index 1. The value this represents varies depending on the function. ''' 
    max_val = users[0]
    for x in users:
        if x[1] > max_val[1]:
            max_val = x
    return max_val


def getArtists():
    ''' Returns a list of all artists in DATA. ''' 
    L = dictToL()
    output = []
    for i in range(len(L)):
        for x in L[i][1]:
            if x in output:
                continue
            else:
                output.append(x)
    return output

def countArtists():
    ''' Returns a list the most popular artist, and how many likes they have. '''
    L = dictToL()
    artists = getArtists()
    output = []
    for artist in artists:
        count = 0
        for i in range(len(L)):
            if artist in L[i][1]:
                count += 1
        output.append([artist, count])
    return maxValUser(output)
def likeList():
    ''' Returns the user with the most liked artists, excluding those whose usernames end in '$'. '''
    L = dictToL()
    count = 0
    output = []
    for i in range(len(L)):
        if L[i][0][-1] == '$':
            continue
        elif L[i][1] == ['']:
            output.append([L[i][0], 0])
        else:
            count = 0
            for _ in L[i][1]:
                count += 1
            output.append([L[i][0], count])
    return output

def displayMenu():
    ''' Displays the menu the user is prompted when running the main function, and after issuing a command. '''
    print('Enter a letter to display an option:')
    print('   e - enter preferences')
    print('   r - get recommendations')
    print('   p - show most popular artist')
    print('   h - how popular is the most popular artist')
    print('   m - which user has the most likes')
    print('   q - save and quit')

def enterPrefs():
    ''' Enter the liked artists for the entered user. Duplicates are denied.'''
    Name = input('Enter your username: ').strip().title()
    artists = []
    while(1):
        A = input('Enter the artist, to stop enter \'S\': ').strip().title()
        if A == 'S':
            break
        if A in artists:
            print('You already entered', A + '! Try again with a different artist.')
        else:
            artists.append(A)
            DATA[Name] = artists

def getRec():
    ''' Get recommendations for the entered user based on what other users in DATA like. If the user has no likes, no recommendation is made. If the user shares a number of artists with multiple users,
    the user who has the most recommendations to offer is printed. '''
    Name = input('Enter your username: ').strip().title()
    best_match = maxValUserRec(compare(Name))
    matches = dropMatches(DATA[best_match[0]], DATA[Name])
    output = ''
    for x in matches:
        output = output + x + ', '
    if matches == []:
        print('I don\'t have any recommendations for you.')
    else:
        print('Here are some artists I recommend for you:', output[:-2])

def showPop():
    ''' Shows the most popular artist. '''
    pop = countArtists()
    print('The most popular artist is', pop[0], '. Press h to see how many likes they have!')

def howPop():
    ''' Shows how popular the most popular artist is. '''
    pop = countArtists()
    print('The most popular artist has', pop[1], 'likes. Press p to see who it is!')

def mostLike():
    ''' Prints the user with the most liked artists, how many artists they like, and which artists they like.'''
    user = maxValUser(likeList())
    prefs = ''
    for x in DATA[user[0]]:
        prefs = prefs + x + ', '
    print('The user with the most likes is', user[0], 'at a total of', str(user[1]) + '. Their likes include ' + prefs[:-2] + '.')

def main():
    
    letters = ['q', 'e', 'r', 'p', 'h', 'm']
    read_prefs('musicrecplus.txt')
    while(1):
        displayMenu()
        user_input = input('Enter a command: ')
        if user_input not in letters:
            print('Enter proper value: ')
        elif user_input == 'q':
            print('Your work has been saved. Goodbye!')
            break
        elif user_input == 'e':
            enterPrefs()
        elif user_input == 'r':
            getRec()
        elif user_input == 'p':
            showPop()
        elif user_input == 'h':
            howPop()
        else:
            mostLike()
    write_prefs('musicrecplus.txt')

if __name__ == "__main__": main()
