import random
import time
import method_storage
import rounds
from method_storage import Player

# DEFINITIONS

# Name system
syntax = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_$#%.*!"

# Starting point system
points_system = "100:0,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:0,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                "80:0,79:0,78:0,77:0,76:0,75:1,74:0,73:0,72:0,71:0,70:0,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                "60:0,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:1,49:0,48:0,47:0,46:0,45:0,44:0,43:0,42:0,41:0," \
                "40:1,39:0,38:0,37:0,36:0,35:0,34:0,33:0,32:0,31:0,30:1,29:0,28:0,27:0,26:0,25:1,24:0,23:0,22:0,21:0," \
                "20:1,19:0,18:0,17:0,16:0,15:1,14:0,13:0,12:0,11:0,10:1,9:0,8:0,7:0,6:0,5:1,4:0,3:1,2:1,1:3/e-1,pk"

# All methods used
methods = method_storage
rounds = rounds

# Records of tourney
total_elims_of_W = 0
avg_elims_per_W = 0
avg_length_of_match = 0

# Players
player_pool = []
all_players = []
all_sorted_players = []
qualified_players = []
# Matches
all_matches_tourney = 0

# MATCH CODE

tourney_type = int(input("What kind of tournament would you like to be played?"))
# TYPES:

# Presets: TODO (in progress)
# Solos: TODO (in progress)
# 0 - Solo cash cup  -> Works
# 1 - Solo cash r1 + Solo cash r2  -> TODO (in progress)
# 2 - Dreamhack stage 1 + Dreamhack stage 2 + Dreamhack finals  -> TODO (next)
# 3 - FNCS stage 1 + FNCS stage 2 + FNCS heats + FNCS finals  -> TODO (in progress)
# 4 - World Cup weekly opens + World Cup weekly finals + World Cup finals  -> TODO (in progress)
# 4 - 1v1 (creative)  -> TODO
# 5 - 1v1 (kill race)  -> TODO
# Duos: TODO
# 0 - Duo cash cup  -> TODO
# Custom  -> TODO (Last)

# Different tournament styles  TODO (make stuff into methods)

if tourney_type == 0:  # One-round cash cups
    all_sorted_players = rounds.solo_round_1(70000, 80000, 10, syntax, .35, True, 30, points_system)

    report = input(
        "Would you like to get the match report of a player? (If yes, respond with # id, if no respond with 'n')")
    if not report == 'n':
        for all_p in range(len(all_sorted_players)):
            if all_sorted_players[all_p].get_name() == report:
                all_sorted_players[all_p].get_match_report()

elif tourney_type == 1:  # Two-round cash cups
    all_sorted_players = rounds.solo_round_1(55000, 80000, 6, syntax, .4, True, 30, points_system)

    qualifiers = []

    for sb in range(100):
        player = methods.Player(all_sorted_players[sb].get_skill(), all_sorted_players[sb].get_rotation(),
                                all_sorted_players[sb].get_drop_spot(),
                                all_sorted_players[sb].get_play_style(), all_sorted_players[sb].get_name())
        qualifiers.append(player)

    # SECOND ROUND

    all_sorted_players = rounds.solo_custom(qualifiers, 6, -.2)

elif tourney_type == 2:  # TODO (daily for now, should be DH)
    all_sorted_players = rounds.solo_round_1(9000, 12000, 10, syntax, .6, True, 0, points_system)

    report = input(
        "Would you like to get the match report of a player? (If yes, respond with # id, if no respond with 'n')")
    if not report == 'n':
        for all_p in range(len(all_sorted_players)):
            if all_sorted_players[all_p].get_name() == report:
                all_sorted_players[all_p].get_match_report()

elif tourney_type == 3:  # FNCS (Solos)
    all_sorted_players = rounds.solo_round_1(11000, 15000, 7, syntax, -.2, False, 220, points_system)

    heat_qualifiers = []
    grands_qualifiers = []

elif tourney_type == 4:  # World Cup Style
    solo_final_quals = []
    duo_final_quals = []

    solo_finals = []
    duo_finals = []

    for week in range(10):
        for region in range(6):
            if week + 1 % 2 == 1:  # Solos
                min = 0
                if region == 0 or 1 or 4:  # OCE, ASIA, BRAZIL
                    min = 260
                    if region == 0:
                        print("OCE week", week + 1)
                    if region == 1:
                        print("ASIA week", week + 1)
                    if region == 4:
                        print("BRAZIL week", week + 1)
                elif region == 2 or 3:  # EU, NAE
                    min = 240
                    if region == 2:
                        print("EU week", week + 1)
                    if region == 0:
                        print("NAE week", week + 1)
                elif region == 6:  # NAW
                    min = 245
                    if region == 0:
                        print("NAW week", week + 1)
                all_sorted_player = rounds.solo_round_1(100000 / 10, 125000 / 10, 10, syntax, .1, False, min,
                                                        points_system)

                weekly_qualifiers = []
                sunday_qualifiers = []

                for sb in range(3000):
                    player = methods.Player(all_sorted_player[sb].get_skill(), all_sorted_player[sb].get_rotation(),
                                            all_sorted_player[sb].get_drop_spot(),
                                            all_sorted_player[sb].get_play_style(),
                                            all_sorted_player[sb].get_name())
                    sunday_qualifiers.append(player)

                # SECOND ROUND

                all_sorted_players = rounds.solo_round_2(sunday_qualifiers, 10, -.3)

                if region == 0:  # OCE
                    solo_final_quals.append(all_sorted_player[0])
                elif region == 1 or 4:  # ASIA, BRAZIL
                    if week + 1 == 1 or 5 or 9:
                        solo_final_quals.append(all_sorted_player[0])
                    elif week + 1 == 3 or 7:
                        solo_final_quals.append(all_sorted_player[0])
                        solo_final_quals.append(all_sorted_player[1])
                elif region == 6:  # NAW
                    solo_final_quals.append(all_sorted_player[0])
                    solo_final_quals.append(all_sorted_player[1])
                elif region == 3:  # NAE
                    solo_final_quals.append(all_sorted_player[0])
                    solo_final_quals.append(all_sorted_player[1])
                    solo_final_quals.append(all_sorted_player[2])
                    solo_final_quals.append(all_sorted_player[3])
                    solo_final_quals.append(all_sorted_player[4])
                    solo_final_quals.append(all_sorted_player[5])
                elif region == 2:  # EU
                    solo_final_quals.append(all_sorted_player[0])
                    solo_final_quals.append(all_sorted_player[1])
                    solo_final_quals.append(all_sorted_player[2])
                    solo_final_quals.append(all_sorted_player[3])
                    solo_final_quals.append(all_sorted_player[4])
                    solo_final_quals.append(all_sorted_player[5])
                    solo_final_quals.append(all_sorted_player[6])
                    solo_final_quals.append(all_sorted_player[7])

elif tourney_type == 10:  # Manual
    all_sorted_players = []

    player_amt = random.randint(100, 100)
    print("There are", player_amt, "people playing in this tournament.")

    for i in range(player_amt - 22):
        skill_bias = 1  # between .8 and 1.2 (lower = lower skill tourney, higher = higher skill tourney)

        name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
        skill = random.randint(850, 975)
        play_style = random.randint(130, int(skill/3))/1000  # (((skill / 1000) * 100 + random.random()) / 100)
        all_players.append(
            Player(skill, random.randint(850, 1000), 1,
                   play_style, name))
        player_pool.append(Player(skill, 1001 - skill, 1, play_style, name))

    voil = Player(984, 932, 1, .21, "v0il")
    all_players.append(voil)
    player_pool.append(voil)
    npen = Player(988, 947, 1, .18, "OA npen")
    all_players.append(npen)
    player_pool.append(npen)
    arkive = Player(972, 894, 1, .25, "arkive8")
    all_players.append(arkive)
    player_pool.append(arkive)
    nanolite = Player(859, 984, 1, .13, "nanolite")
    all_players.append(nanolite)
    player_pool.append(nanolite)
    crimz = Player(964, 926, 1, .20, "OA Crimz")
    all_players.append(crimz)
    player_pool.append(crimz)
    mack = Player(952, 944, 1, .19, "TSM MackWood1x")
    all_players.append(mack)
    player_pool.append(mack)
    riversan = Player(977, 988, 1, .12, "Liquid Riversan")
    all_players.append(riversan)
    player_pool.append(riversan)
    scoped = Player(991, 920, 1, 26, "Scoped")
    all_players.append(scoped)
    player_pool.append(scoped)
    cole = Player(976, 954, 1, .22, "Co1azo")
    all_players.append(cole)
    player_pool.append(cole)
    unknown = Player(1000, 894, 1, .28, "NRG Lil Unknown")
    all_players.append(unknown)
    player_pool.append(unknown)
    klass = Player(934, 955, 1, .19, "KIass")
    all_players.append(klass)
    player_pool.append(klass)
    grazca = Player(958, 924, 1, .25, "E11 Grazca")
    all_players.append(grazca)
    player_pool.append(grazca)
    kwah = Player(975, 908, 1, .22, "kwah")
    all_players.append(kwah)
    player_pool.append(kwah)
    jamper = Player(968, 957, 1, .17, "LG Jamper")
    all_players.append(jamper)
    player_pool.append(jamper)
    roat = Player(894, 919, 1, .27, "roatdw")
    all_players.append(roat)
    player_pool.append(roat)
    zyfa = Player(964, 926, 1, .20, "SEN Zyfa")
    all_players.append(crimz)
    player_pool.append(crimz)
    ajerss = Player(977, 954, 1, .17, "Ajerss")
    all_players.append(ajerss)
    player_pool.append(ajerss)
    prien = Player(946, 924, 1, .16, "Outcast Prien")
    all_players.append(prien)
    player_pool.append(prien)
    cloud = Player(956, 941, 1, .18, "CloudThaGreat")
    all_players.append(cloud)
    player_pool.append(cloud)
    deyy = Player(978, 941, 1, .22, "Pure Deyy")
    all_players.append(deyy)
    player_pool.append(deyy)
    glace = Player(935, 927, 1, .17, "Vanish Glace")
    all_players.append(glace)
    player_pool.append(glace)
    acorn = Player(963, 988, 1, .15, "Acorn")
    all_players.append(acorn)
    player_pool.append(acorn)

    for matches in range(6):
        if matches > 0:
            print("\nThe #1 player right now is", all_sorted_players[0].get_name(), "and has",
                  all_sorted_players[0].get_points(),
                  "points and", all_sorted_players[0].get_wins(), "win(s).")

        print("Group ", matches + 1, ":", sep="")
        time_playing_s = time.time()  # Start time

        if matches == 0:
            all_matches = methods.create_play_matches(player_pool, True, 0)
            all_matches_tourney += len(all_matches)
        else:
            all_matches = methods.create_play_matches(all_sorted_players, False, 0)
            all_matches_tourney += len(all_matches)

        time_playing = (time.time() - time_playing_s).__round__(3)

        # Create scoreboard
        time_sorting_s = time.time()  # Start time

        all_sorted_players = methods.create_scoreboard(2, all_players, points_system, True)

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
    all_sorted_players = methods.create_scoreboard(2, all_players, points_system, False)

    # Showing scoreboard
    print("\nSCOREBOARD:")
    for sb in range(len(all_sorted_players)):
        if sb < 10000:
            print(sb + 1, ". ", all_sorted_players[sb].get_name(), " - ", all_sorted_players[sb].get_points(),
                  " points; ",
                  all_sorted_players[sb].get_wins(), " wins; ", all_sorted_players[sb].get_total_kills(),
                  " kills. Skill: ",
                  all_sorted_players[sb].get_skill(), "/1000, play style: ",
                  all_sorted_players[sb].get_play_style().__round__(4),
                  ", rotation ability: ", all_sorted_players[sb].get_rotation(), sep="")
        total_points += all_sorted_players[sb].get_points()

    avg_points = int(total_points / len(all_sorted_players))

    print("The average player had ", avg_points, " points.", sep="")

    print("")

    report = input(
        "Would you like to get the match report of a player? (If yes, respond with # id, if no respond with 'n')")
    if not report == 'n':
        for all_p in range(len(all_sorted_players)):
            if all_sorted_players[all_p].get_name() == report:
                all_sorted_players[all_p].get_match_report()
