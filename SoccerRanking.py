import csv
from collections import Counter
from operator import itemgetter
from colorama import Fore, Style


# Pep8 checked (long lines splited)*

filename_0 = 'Premier_League_1920.csv'
filename_1 = 'Seria_A_1718.csv'
filename_2 = 'Bundesliga_1_1819.csv'

# 'Protection' against incorrect user input in most of the code
# works as a repeating ask of input, also some cases corrected (marked as ##)
# Italian Seria A file has xx/xx/xx date format


def full_ranking_PL(filename):
    ls_winners = []
    ls_draws = []
    ls_home_teams = []
    ls_away_teams = []
    ls_home_team_goals = []
    ls_away_team_goals = []
    # csv file opening and key getting
    with open(filename, newline='') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            dict_match = (row['Date'], row['HomeTeam'], row['FTHG'],
                          row['FTAG'], row['AwayTeam'])
            HomeTeam_key = list(dict_match)[1]
            FTHG_key = list(dict_match)[2]
            FTAG_key = list(dict_match)[3]
            AwayTeam_key = list(dict_match)[4]
            ls_home_teams.append(HomeTeam_key)
            ls_away_teams.append(AwayTeam_key)
            ls_home_team_goals.append(FTHG_key)
            ls_away_team_goals.append(FTAG_key)
            if int(FTHG_key) > int(FTAG_key):
                ls_winners.append(HomeTeam_key)
            if int(FTAG_key) > int(FTHG_key):
                ls_winners.append(AwayTeam_key)
            if int(FTHG_key) == int(FTAG_key):
                ls_draws.append(HomeTeam_key)
                ls_draws.append(AwayTeam_key)
        win_counter = []
        draw_counter = []
        # game counting and sorting
        count_home_games = dict(Counter(ls_home_teams))
        count_away_games = dict(Counter(ls_away_teams))
        team_games_played = dict(Counter(count_home_games) +
                                 Counter(count_away_games))
        team_games_played = sorted(team_games_played.items(),
                                   key=lambda games: games[1])
        for team in ls_winners:
            win_counter.append(ls_winners.count(team))
        ls_win_counter = list(map(list, set(zip(ls_winners, win_counter))))
        for team in ls_draws:
            draw_counter.append(ls_draws.count(team))
        ls_draw_counter = list(map(list, set(zip(ls_draws, draw_counter))))
        for team in ls_win_counter:
            team[1] *= 3
        dct_win_counter = dict(ls_win_counter)
        dct_draw_counter = dict(ls_draw_counter)
        # counting won and draw games (by collections module) and sorting them
        ranking = dict(Counter(dct_win_counter) + Counter(dct_draw_counter))
        ranking = sorted(ranking.items(), key=lambda points: points[1])
        list.reverse(ranking)
        ranking = list(map(list, ranking))
        n_0 = 0
        while n_0 < len(ranking):
            goal_sum_home = 0
            goal_sum_away = 0
            goal_sum_home_missed = 0
            goal_sum_away_missed = 0
            head = ranking[n_0]
            # getting match indexes
            indexPosList_team1_home = [team for team in
                                       range(len(ls_home_teams))
                                       if ls_home_teams[team] == head[0]]
            indexPosList_team1_away = [team for team in
                                       range(len(ls_away_teams))
                                       if ls_away_teams[team] == head[0]]
            # counting goals and goal difference
            for match in indexPosList_team1_home:
                for home_goals in ls_home_team_goals[match]:
                    home_goals = int(home_goals)
                    goal_sum_home += home_goals
                for away_goals in ls_away_team_goals[match]:
                    away_goals = int(away_goals)
                    goal_sum_home_missed += away_goals
            for match in indexPosList_team1_away:
                for away_goals in ls_away_team_goals[match]:
                    away_goals = int(away_goals)
                    goal_sum_away += away_goals
                for home_goals in ls_home_team_goals[match]:
                    home_goals = int(home_goals)
                    goal_sum_away_missed += home_goals
            goal_sum_team = goal_sum_home + goal_sum_away
            goal_sum_missed = goal_sum_home_missed + goal_sum_away_missed
            goal_diff = goal_sum_team - goal_sum_missed
            ranking[n_0].append(goal_diff)
            ranking[n_0].append(goal_sum_team)
            n_0 += 1
        ranking = list(map(tuple, ranking))
        # Priority sorting using operator module
        ranking = sorted(ranking, key=itemgetter(1, 2, 3), reverse=True)
        ranking = list(map(list, ranking))
        # Game counting
        for games in team_games_played:
            for team in ranking:
                if team[0] == games[0]:
                    team.append(games[1])
        # win counter
        for wins in ls_win_counter:
            for team in ranking:
                if team[0] == wins[0]:
                    team.append(int(wins[1] / 3))
        # draw counter
        for draws in ls_draw_counter:
            for team in ranking:
                if team[0] == draws[0]:
                    team.append(draws[1])
        # loss counter
        n_0 = 0
        while n_0 < len(ranking):
            Games_played = ranking[n_0][4]
            Wins = ranking[n_0][5]
            Draws = ranking[n_0][6]
            losses = Games_played - Wins - Draws
            ranking[n_0].append(losses)
            n_0 += 1
        # output ranking table + Same place requirement
        print('{:>17}{:>16}{:>24}{:>15}{:>20}{:>17}{:>10}{:>10}'
              .format('Teams:', 'Points:', 'Goal difference:', 'Goals:',
                      'Games played: ', 'Wins: ', 'Draws: ', 'Losses: '))
        n_0 = 0
        n_1 = 1
        in_1 = 0
        for ts_1, ts_2, ts_3, ts_4, ts_5, ts_6, ts_7, ts_8 in ranking:
            if n_0 < len(ranking):
                print('Place ' + str(n_1) + ':  ' +
                      '{:<21}{:<23}{:<15}{:<19}{:<19}{:<10}{:<10}{:<10}'
                      .format(ts_1, ts_2, ts_3, ts_4, ts_5, ts_6, ts_7, ts_8))
                if in_1 < len(ranking) - 1:
                    head = ranking[in_1]
                    next_head = ranking[in_1 + 1]
                    if head[1] == next_head[1]:
                        if head[2] == next_head[2]:
                            if head[3] == next_head[3]:
                                n_1 -= 1
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    break
            n_0 += 1
            n_1 += 1
            in_1 += 1
        input_file.close()
    print('\n')


def team_matches(filename):
    team_name = input('Enter: ')
    with open(filename, newline='') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            dict_match = (row['Date'], row['HomeTeam'], row['FTHG'],
                          row['FTAG'], row['AwayTeam'])
            ##
            if team_name.isdigit():
                break
            if team_name in dict_match:
                print(dict_match)
        input_file.close()
        print('\n')


def match_on_date(filename):
    match_date = input(str('Enter: '))
    print('\n')
    ##
    if len(match_date) in range(8, 11):
        ##
        for character in match_date:
            ##
            if character.isdigit():
                with open(filename, newline='') as input_file:
                    reader = csv.DictReader(input_file)
                    for row in reader:
                        dict_match = (row['Date'], row['HomeTeam'],
                                      row['FTHG'], row['FTAG'],
                                      row['AwayTeam'])
                        if match_date in dict_match:
                            print(dict_match)
                    print('\n')
                    break


# menu: ## calculated only by EN Premier League rules
keys = True
while keys:
    print(f'{Fore.GREEN}Greetings, Traveler! {Style.RESET_ALL}', '\n')
    print('Choose a tournament: ', '\n',
          f'{Fore.GREEN}1. {Style.RESET_ALL}' +
          'English Premier League 2019/2020', '\n',
          f'{Fore.GREEN}2. {Style.RESET_ALL}' +
          'Italian Seria A 2017/2018', '\n',
          f'{Fore.GREEN}3. {Style.RESET_ALL}' +
          'German Bundesliga 1 2018/2019', '\n',
          f'{Fore.GREEN}4. {Style.RESET_ALL}' +
          'To quit', '\n',)
    keys_1 = input('Enter: ')
    print('\n')
    while keys_1:
        if keys_1 == '1':
            filename = filename_0
            print('English Premier League 2019/2020')
            print('Choose from: ', '\n',
                  f'{Fore.GREEN}1. {Style.RESET_ALL}' +
                  'Ranking + Statistics', '\n',
                  f'{Fore.GREEN}2. {Style.RESET_ALL}' +
                  'Team matches', '\n',
                  f'{Fore.GREEN}3. {Style.RESET_ALL}' +
                  'Matches on a given date', '\n',
                  f'{Fore.GREEN}4. {Style.RESET_ALL}' +
                  'Back', '\n')
            print('double ' + f'{Fore.GREEN}ENTER {Style.RESET_ALL}' +
                  'to quit')
            print('*enter 1,2,3,4', '\n')
            keys_2 = input('Enter: ')
            # ranking table
            if keys_2 == '1':
                full_ranking_PL(filename)
            # finding team matches
            if keys_2 == '2':
                print('Enter a team: ')
                print('*first letter is an upper letter, no space in the end')
                print('\n')
                team_matches(filename)
            # finding matches on a given date
            if keys_2 == '3':
                print('Enter a date: ')
                print('*like this: 01/01/2001')
                match_on_date(filename)
            if keys_2 == '4':
                keys_1 = False
                print('\n')
            else:
                continue
        if keys_1 == '2':
            filename = filename_1
            print('Italian Seria A 2017/2018')
            print('Choose from: ', '\n',
                  f'{Fore.GREEN}1. {Style.RESET_ALL}' +
                  'Ranking + Statistics', '\n',
                  f'{Fore.GREEN}2. {Style.RESET_ALL}' +
                  'Team matches', '\n',
                  f'{Fore.GREEN}3. {Style.RESET_ALL}' +
                  'Matches on a given date', '\n',
                  f'{Fore.GREEN}4. {Style.RESET_ALL}' +
                  'Back', '\n')
            print('double ' + f'{Fore.GREEN}ENTER {Style.RESET_ALL}' +
                  'to quit')
            print('*enter 1,2,3,4', '\n')
            keys_2 = input('Enter: ')
            # ranking table
            if keys_2 == '1':
                full_ranking_PL(filename)
            # finding team matches
            if keys_2 == '2':
                print('Enter a team: ')
                print('*first letter is an upper letter, no space in the end')
                print('\n')
                team_matches(filename)
            # finding matches on a given date
            if keys_2 == '3':
                print('Enter a date: ')
                print('*like this: 01/01/01')
                print('\n')
                match_on_date(filename)
            if keys_2 == '4':
                keys_1 = False
                print('\n')
            else:
                continue
        if keys_1 == '3':
            filename = filename_2
            print('German Bundesliga 1 2018/2019')
            print('Choose from: ', '\n',
                  f'{Fore.GREEN}1. {Style.RESET_ALL}' +
                  'Ranking + Statistics', '\n',
                  f'{Fore.GREEN}2. {Style.RESET_ALL}' +
                  'Team matches', '\n',
                  f'{Fore.GREEN}3. {Style.RESET_ALL}' +
                  'Matches on a given date', '\n',
                  f'{Fore.GREEN}4. {Style.RESET_ALL}' +
                  'Back', '\n')
            print('double ' + f'{Fore.GREEN}ENTER {Style.RESET_ALL}' +
                  'to quit')
            print('*enter 1,2,3,4', '\n')
            keys_2 = input('Enter: ')
            # ranking table
            if keys_2 == '1':
                full_ranking_PL(filename)
            # finding team matches
            if keys_2 == '2':
                print('Enter a team: ')
                print('*first letter is an upper letter, no space in the end')
                print('\n')
                team_matches(filename)
            # finding matches on a given date
            if keys_2 == '3':
                print('Enter a date: ')
                print('*like this: 01/01/2001')
                print('\n')
                match_on_date(filename)
            if keys_2 == '4':
                keys_1 = False
                print('\n')
            else:
                continue
        # quit option
        if keys_1 == '4':
            print(10 * ('\n'))
            print(f'{Fore.GREEN}quited. {Style.RESET_ALL}')
            quit()
        else:
            keys_1 = False
