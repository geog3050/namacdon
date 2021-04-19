from itertools import combinations_with_replacement

numbers = list(range(1,21))
dubs = [2 * n for n in numbers]
trips = [3 * n for n in numbers]
bulls = [25,50]
instance_points = numbers + dubs + trips + bulls
possible_points = list(set(instance_points))
record_keeper = []
two_dart_combos = combinations_with_replacement(instance_points,2)
three_dart_combos = combinations_with_replacement(instance_points,3)

def dart_score():
    try:
        game_score = int(input('What is the game score?'))
    except:
         print('Score must be a valid number')
    if game_score == 0:
        return 'Then why are you asking for a score???'        
    elif isinstance(game_score, int):
        return point_scorer(game_score, 0)

    
def point_scorer(entry_score, n):
    record_keeper.append(entry_score)
    current_score = entry_score
    if current_score == 0:
        return 'You win!!!'        
    elif current_score < 0:
        return f'Bust!! Score goes back to {record_keeper[0]}'       
    elif n >= 3:
        return f'Out of throws! Current score is {current_score}'        
    elif current_score >= 60:
        print('Go for triple-twenty!')
    elif current_score == 50:
        print('Nail that double bullseye to win!')
    elif current_score <= 20:
        print(f'Hit the {current_score} to win!')
    elif current_score in trips:
        trip_val = current_score // 3
        print(f'Get {current_score} to win by hitting the Triple {trip_val}')
    elif current_score in dubs:
        dub_val = current_score // 2
        print(f'Get {current_score} to win by hitting the Double {dub_val}')        
    elif current_score > 20:
        print('This throw: go for triple-twenty')
    return executor(current_score, n)
    
def executor(current_score, n):
    try:
        dart_throw = int(input('What value did you hit?'))
    except:
        print('Score must be a valid number')
    if isinstance(dart_throw, int):
        exit_score = current_score - dart_throw
        n = n + 1
    return point_scorer(exit_score, n)

def show_me_combos():
    try:
        game_score = int(input('What is the game score?'))
    except:
         print('Score must be a valid number')
    if game_score == 0:
        return 'Then why are you asking for a score???'        
    elif game_score > 60:
        return 'Just go for triple-twenty three times'
    elif isinstance(game_score, int):
        for i in list(three_dart_combos):
            if sum(i) == game_score:
                print(i)
        for i in list(two_dart_combos):
             if sum(i) == game_score:
                print(i)
