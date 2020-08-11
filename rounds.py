import random
import time
import method_storage
from method_storage import Player

# imports
methods = method_storage
def_player = Player

# definitions
all_players = []
player_pool = []
all_sorted_players = []

all_matches_tourney = 0


def solo_round_1(min_players, max_players, matches_to_play, syntax, s_bias, spread, scoreboard):
    # set globals
    global methods
    global all_players
    global player_pool
    global all_sorted_players
    global all_matches_tourney

    all_sorted_players = []

    player_amt = random.randint(min_players, max_players)
    print("There are", player_amt, "people playing in this tournament.")

    for i in range(player_amt):
        name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
        skill = random.randint(0, player_amt * spread)
        play_style = (((skill / player_amt) * 100 + random.random()) / 100) < 1
        all_players.append(Player(skill, 1, play_style, name))
        player_pool.append(Player(skill, 1, play_style, name))

    plasmic = Player(player_amt*.76, 1, .63, "ASC Plasmic")
    all_players.append(plasmic)
    player_pool.append(plasmic)

    for matches in range(matches_to_play):
        print("Group ", matches+1, ":", sep="")
        time_playing_s = time.time()  # Start time

        if matches == 0:
            all_matches = methods.create_play_matches(player_pool, True, s_bias)
            all_matches_tourney += len(all_matches)
        else:
            all_matches = methods.create_play_matches(all_sorted_players, False, s_bias)
            all_matches_tourney += len(all_matches)

        time_playing = (time.time() - time_playing_s).__round__(3)

        # Create scoreboard
        time_sorting_s = time.time()  # Start time

        all_sorted_players = methods.create_scoreboard(2, all_players)

        time_sorting = (time.time() - time_sorting_s).__round__(3)

        # Print what is going on
        print("\nThere are", len(all_sorted_players), "players on the scoreboard.")

        print("Match group", matches + 1, "done and sorted. It took", time_playing,
              "seconds to play all matches. It took",
              time_sorting, "seconds to sort all players.")

        print("The #1 player right now is", all_sorted_players[0].get_name(), "and has",
              all_sorted_players[0].get_points(),
              "points and", all_sorted_players[0].get_wins(), "win(s).")

        # New player pool
        player_pool = all_sorted_players

        for new_players in range(random.randint(10, 100)):
            name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
            skill = random.randint(0, player_amt * spread)
            play_style = (((skill / player_amt) * 100 + random.random()) / 100) < 1
            player_amt += 1
            all_players.append(Player(skill, 1, play_style, name))
            player_pool.append(Player(skill, 1, play_style, name))
            player_pool.remove(player_pool[random.randint(0, len(player_pool) - 1)])

        time.sleep(4)

    total_points = 0

    # FINAL SORT
    all_sorted_players = methods.create_scoreboard(2, all_players)
    scoreboard = methods.create_scoreboard(0, all_players)

    # Showing scoreboard
    print("\nSCOREBOARD:")
    for sb in range(len(all_sorted_players)):
        if sb < 10000 and scoreboard:
            print(sb + 1, ". ", scoreboard[sb].get_name(), " - ", scoreboard[sb].get_points(), " points; ",
                  scoreboard[sb].get_wins(), " wins; ", scoreboard[sb].get_total_kills(), " kills.", sep="")
        total_points += all_sorted_players[sb].get_points()

    avg_points = int(total_points / len(all_sorted_players))

    print("The average player had ", avg_points, " points.", sep="")

    print("")

    return all_sorted_players


def solo_round_2(qualifiers, matches_played, s_bias):
    # set globals
    global methods
    global all_players
    global player_pool
    global all_sorted_players
    global all_matches_tourney

    time_playing_s = time.time()  # Start time

    for matches in range(matches_played):
        methods.create_play_matches(qualifiers, False, s_bias)

        # Print what is going on
        print("There are", len(qualifiers), "players queuing.")

    time_playing = (time.time() - time_playing_s).__round__(3)

    print("All matches done. It took", time_playing, "seconds to play all matches.")

    time.sleep(4)

    total_points = 0

    # FINAL SORT
    all_sorted_players = methods.create_scoreboard(0, qualifiers)

    # Showing scoreboard
    print("SCOREBOARD:")
    for sb in range(len(all_sorted_players)):
        total_points += all_sorted_players[sb].get_points()

    avg_points = int(total_points / len(all_sorted_players))

    # AVERAGES
    print("The average player had ", avg_points, " points.", sep="")

    print("")

    return all_sorted_players


def solo_custom(qualifiers, matches_played, s_bias):
    # set globals
    global methods
    global all_players
    global player_pool
    global all_sorted_players
    global all_matches_tourney

    time_playing_s = time.time()  # Start time

    for matches in range(matches_played):
        methods.play_match(qualifiers, s_bias)

        # Print what is going on
        print("There are", len(qualifiers), "players queuing.")

    time_playing = (time.time() - time_playing_s).__round__(3)

    print("All matches done. It took", time_playing, "seconds to play all matches.")

    time.sleep(4)

    total_points = 0

    # FINAL SORT
    all_sorted_players = methods.create_scoreboard(0, qualifiers)

    # Showing scoreboard
    print("SCOREBOARD:")
    for sb in range(len(all_sorted_players)):
        print(sb + 1, ". ", all_sorted_players[sb].get_name(), " - ", all_sorted_players[sb].get_points(),
              " points; ",
              all_sorted_players[sb].get_wins(), " wins; ", all_sorted_players[sb].get_total_kills(), " kills.",
              sep="")
        total_points += all_sorted_players[sb].get_points()

    avg_points = int(total_points / len(all_sorted_players))

    # AVERAGES
    print("The average player had ", avg_points, " points.", sep="")

    print("")

    return all_sorted_players