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


def solo_round_1(min_players, max_players, matches_to_play, syntax, s_bias, sbs, point_system, min_skill=0):
    # set globals
    global methods
    global all_players
    global player_pool
    global all_sorted_players
    global all_matches_tourney

    all_sorted_players = []

    player_amt = random.randint(min_players, max_players)
    print("There are", player_amt, "people playing in this tournament.")

    plasmic = Player(732, 884, 24, .54, "Plasmic.TA")
    all_players.append(plasmic)
    all_sorted_players.append(plasmic)

    nazariy = Player(754, 743, 8, .61, "TA Nazariy")
    all_players.append(nazariy)
    all_sorted_players.append(nazariy)

    for i in range(player_amt - len(all_players)):
        skill_bias = s_bias  # between .8 and 1.2 (lower = lower skill tourney, higher = higher skill tourney)

        p_skill = random.randint(min_skill*10, 100) + random.random()

        name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
        min_skill = min_skill
        max_skill = int(p_skill * 10)
        skill = random.randint(min_skill, max_skill) * skill_bias
        play_style = ((p_skill / 100) * 10 + random.random()) / 10
        drop_spot = -1
        rotation = random.randint(int(p_skill / 2 * 10), int(p_skill * 30))
        while rotation > 1000:
            rotation -= random.randint(10, 100)
        while drop_spot == -1:
            b1 = int((max_skill / 10 + random.randint(1, 5) - skill / 10) / 5)
            b2 = 1 - play_style
            drop_spot = int(b1 * b2)
            if drop_spot > 30:
                drop_spot /= 2
                drop_spot += random.randint(1, 3) - random.randint(1, 3)
            elif drop_spot < 1:
                drop_spot = 1
        all_players.append(Player(skill, rotation, drop_spot, play_style, name))
        player_pool.append(Player(skill, rotation, drop_spot, play_style, name))

    m = matches_to_play

    for matches in range(m + 1):
        if matches > 1:
            for i in range(len(all_sorted_players)):
                if i < 10:
                    print("\nThe #", i + 1, "player right now is", all_sorted_players[i].get_name(), "and has",
                          all_sorted_players[i].get_points(),
                          "points and", all_sorted_players[i].get_wins(), "win(s). Their last placement was",
                          all_sorted_players[i].get_placement_match())
                elif all_sorted_players[i].get_name() == "Plasmic.TA":
                    print("\nThe #", i + 1, "player right now is", all_sorted_players[i].get_name(), "and has",
                          all_sorted_players[i].get_points(),
                          "points and", all_sorted_players[i].get_wins(), "win(s). Their last placement was",
                          all_sorted_players[i].get_placement_match())
                elif all_sorted_players[i].get_name() == "TA Nazariy":
                    print("\nThe #", i + 1, "player right now is", all_sorted_players[i].get_name(), "and has",
                          all_sorted_players[i].get_points(),
                          "points and", all_sorted_players[i].get_wins(), "win(s). Their last placement was",
                          all_sorted_players[i].get_placement_match())
                prev_removed = 0
                if (all_sorted_players[int(player_amt / 100)].get_points() - all_sorted_players[i].get_points()) > 20:
                    if random.randint(0, all_sorted_players[i].get_points() * 4) == random.randint(0,
                                                                                                   all_sorted_players[
                                                                                                       i].get_points() * 4):
                        if player_pool.__contains__(all_sorted_players[i - prev_removed]):
                            player_pool.remove(all_sorted_players[i - prev_removed])
                            prev_removed += 1

            for i in range(random.randint(0, 50)):
                skill_bias = 1  # between .8 and 1.2 (lower = lower skill tourney, higher = higher skill tourney)

                p_skill = random.randint(0, 100) + random.random()

                name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
                min_skill = 0
                max_skill = int(p_skill * 10)
                skill = random.randint(min_skill, max_skill) * skill_bias
                play_style = ((p_skill / 100) * 10 + random.random()) / 10
                drop_spot = -1
                rotation = random.randint(int(p_skill / 2 * 10), int(p_skill * 30))
                while rotation > 1000:
                    rotation -= random.randint(10, 100)
                while drop_spot == -1:
                    b1 = int((max_skill / 10 + random.randint(1, 5) - skill / 10) / 5)
                    b2 = 1 - play_style
                    drop_spot = int(b1 * b2)
                    if drop_spot > 30:
                        drop_spot /= 2
                        drop_spot += random.randint(1, 3) - random.randint(1, 3)
                    elif drop_spot < 1:
                        drop_spot = 1
                all_players.append(Player(skill, rotation, drop_spot, play_style, name))
                player_pool.append(Player(skill, rotation, drop_spot, play_style, name))

        print("Group ", matches + 1, ":", sep="")
        time_playing_s = time.time()  # Start time

        if matches == 0:
            all_matches = methods.create_play_matches(player_pool, 0, True)
            all_matches_tourney += len(all_matches)
        else:
            all_matches = methods.create_play_matches(all_sorted_players, 1 - (matches / 10) - .3)
            all_matches_tourney += len(all_matches)

        time_playing = (time.time() - time_playing_s).__round__(3)

        # Create scoreboard
        time_sorting_s = time.time()  # Start time

        all_sorted_players = methods.create_scoreboard(2, all_players, point_system, True)

        time_sorting = (time.time() - time_sorting_s).__round__(3)

        # Print what is going on
        print("\nMatch group", matches + 1, "done and sorted. It took", time_playing,
              "seconds to play all matches. It took",
              time_sorting, "seconds to sort all players.")

    total_points = 0
    print("\nThe #1 player right now is", all_sorted_players[0].get_name(), "and has",
          all_sorted_players[0].get_points(),
          "points and", all_sorted_players[0].get_wins(), "win(s).")

    # FINAL SORT
    all_sorted_players = methods.create_scoreboard(2, all_players, point_system, False)

    # Showing scoreboard
    print("\nSCOREBOARD:")
    for sb in range(len(all_sorted_players)):
        if sb < 5000 and all_sorted_players[sb].get_matches() > 0:
            print(sb + 1, ". ", all_sorted_players[sb].get_name(), " - ", all_sorted_players[sb].get_points(),
                  " points; ",
                  all_sorted_players[sb].get_wins(), " wins; ", all_sorted_players[sb].get_total_kills(),
                  " kills; Avg placement: ", all_sorted_players[sb].get_avg_placement(), "; Matches:",
                  all_sorted_players[sb].get_matches(), "; Skill: ",
                  all_sorted_players[sb].get_skill(), "/1000, play style: ",
                  all_sorted_players[sb].get_play_style().__round__(4),
                  ", rotation ability: ", all_sorted_players[sb].get_rotation(), sep="")
        elif all_sorted_players[sb].get_name() == "Plasmic.TA":
            print("\nThe #", sb + 1, "player right now is", all_sorted_players[sb].get_name(), "and has",
                  all_sorted_players[sb].get_points(),
                  "points and", all_sorted_players[sb].get_wins(), "win(s). Their last placement was",
                  all_sorted_players[sb].get_placement_match())
        elif all_sorted_players[sb].get_name() == "TA Nazariy":
            print("\nThe #", sb + 1, "player right now is", all_sorted_players[sb].get_name(), "and has",
                  all_sorted_players[sb].get_points(),
                  "points and", all_sorted_players[sb].get_wins(), "win(s). Their last placement was",
                  all_sorted_players[sb].get_placement_match())
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
