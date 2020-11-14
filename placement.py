###
# Coded by Plasmic
# Can be used by anyone
# Open API
# Do not distribute
###


# Imports:

import random
import time
import method_storage
import rounds
from method_storage import Player
from xlwt import Workbook

# DEFINITIONS:

# Name system
syntax = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_$#%.*!"

# Default point system ("fair")
points_system = "100:11,99:1,98:1,97:1,96:1,95:1,94:1,93:1,92:1,91:1,90:1,89:1,88:1,87:1,86:1,85:1,84:1,83:1,82:1,81:1," \
                "80:1,79:1,78:1,77:1,76:1,75:1,74:1,73:1,72:1,71:1,70:1,69:1,68:1,67:1,66:1,65:1,64:1,63:1,62:1,61:1," \
                "60:1,59:1,58:1,57:1,56:1,55:1,54:1,53:1,52:1,51:1,50:2,49:2,48:2,47:2,46:2,45:2,44:2,43:2,42:2,41:2," \
                "40:2,39:2,38:2,37:2,36:2,35:2,34:2,33:2,32:2,31:2,30:1,29:2,28:2,27:2,26:2,25:3,24:3,23:3,22:3,21:3," \
                "20:3,19:3,18:3,17:3,16:3,15:1,14:3,13:3,12:3,11:3,10:4,9:4,8:4,7:4,6:4,5:1,4:4,3:5,2:6,1:8/e-15,pk"

# Other files (methods)
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

wb = Workbook()


def write_to_file(m2, tourneys2, skill_bias2, all_sorted_players_copy, sheet_name):
    # Spreadsheet
    sheet1 = wb.add_sheet(sheet_name)

    # Write to spreadsheet
    # Manual stuff
    sheet1.write(1, 0, "MATCHES: " + str(m2))
    sheet1.write(2, 0, "TOURNAMENTS: " + str(tourneys2))
    sheet1.write(3, 0, "SKILL BIAS: " + str(skill_bias2))
    sheet1.write(5, 0, "Place:")
    sheet1.write(5, 1, "Name (random):")
    sheet1.write(5, 3, "Average points:")
    sheet1.write(5, 4, "Average kills:")
    sheet1.write(5, 5, "Average Place:")
    sheet1.write(5, 6, "Skill:")
    sheet1.write(5, 7, "Rotation:")
    sheet1.write(5, 8, "Play style:")
    sheet1.write(5, 9, "Drop:")
    sheet1.write(5, 10, "Average finish:")
    sheet1.write(5, 11, "Tourney wins:")

    all_sorted_players_copy = methods.create_scoreboard(3, all_players, points_system, False)
    for i in range(len(all_sorted_players_copy)):
        sheet1.write(i + 6, 0, str(i + 1) + "")
        sheet1.write(i + 6, 1, all_sorted_players_copy[i].get_name())
        sheet1.write(i + 6, 3, str(round(all_sorted_players_copy[i].get_avg_points(), 3)) + "")
        sheet1.write(i + 6, 4, str(round(all_sorted_players_copy[i].get_avg_kills(), 3)) + "")
        sheet1.write(i + 6, 5, str(round(all_sorted_players_copy[i].get_avg_place(), 3)) + "")
        sheet1.write(i + 6, 6, str(all_sorted_players_copy[i].get_skill()) + "")
        sheet1.write(i + 6, 7, str(all_sorted_players_copy[i].get_rotation()) + "")
        sheet1.write(i + 6, 8, str(round(all_sorted_players_copy[i].get_play_style(), 3)) + "")
        sheet1.write(i + 6, 9, str(all_sorted_players_copy[i].get_drop_spot()) + "")
        sheet1.write(i + 6, 10, str(round(all_sorted_players_copy[i].get_avg_finish(), 3)) + "")
        sheet1.write(i + 6, 11, str(all_sorted_players_copy[i].get_t_wins()) + "")
        wb.save(sheet_name + ".xls")


# MATCH CODE:

# Input
tourney_type = input(
    "What kind of tournament would you like to be played (must be typed in format, type 'help' if needed):\n")

# RESPONSE -> <mode>:<type>:<round#>  OR  'help'
# <mode> - gamemode ((1, s, solo(s)), (2, d, duo(s)), (3, t, trio(s)), (4, sq, squad(s)))
# <type> - Tourney type (cc, fncs, dh, custom)
# <round#> - Amount of rounds
# 'help' - <mode>:<type>:<round#>


# TOURNEYS:

# Tourney type:
t_mode = ""  # Gamemode (creating str variable before assigning it a value later)
t_type = ""  # Tournament type (creating str variable before assigning it a value later)
t_round = ""  # Rounds to be played (creating str variable before assigning it a value later)

if len(tourney_type.split(";")) == 3:
    t_mode = tourney_type.split(";")[0]
    print("Mode: " + t_mode)
    t_type = tourney_type.split(";")[1]
    print("Type: " + t_type)
    t_round = tourney_type.split(";")[2]
    print("Rounds: " + t_round)

elif tourney_type == "help":
    # new tourney type:
    cont = str  # Declaring as string

    # Showing help and asking if user needs more
    cont = input(
        "Typing format: '<mode>;<type>;<round#>.' \nIf you need more help, please specify 'mode,type,roundHelp', "
        "otherwise continue.\n")

    # If this is never fulfilled
    while not len(cont.split(":")) == 3:
        if cont == "help":
            cont = input("Typing format: '<mode>;<type>;<round#>.' Typing 'End' also ends the program."
                         " \nIf you need more help, please specify 'mode,type,roundHelp', otherwise continue.\n")
        elif cont == "modeHelp":
            cont = input("This is the gamemode. Please type: ((1, s, solo(s)), (2, d, duo(s)), (3, t, trio(s)), "
                         "(4, sq, squad(s))), specifying which mode to use. Any abbreviation shown works "
                         "\nIf you need more help, please specify 'mode,type,roundHelp', otherwise continue.\n")
        elif cont == "typeHelp":
            cont = input("This is the Tourney type. Please type: (cc, fncs, dh, custom). Any abbreviation shown works "
                         "\nIf you need more help, please specify 'mode,type,roundHelp', otherwise continue.\n")
        elif cont == "roundHelp":
            cont = input("This is the amount of rounds. Please type a number between 1 and 2 (only works for cc), "
                         "\nIf you need more help, please specify 'mode,type,roundHelp', otherwise continue.\n")
        elif cont == "End":
            break
        else:
            cont = input(
                "What you just typed is not supported. Please try again, remember, help/modeHelp/typeHelp/roundHelp.\n")

    t_mode = cont.split(";")[0]
    t_type = cont.split(";")[1]
    t_round = cont.split(";")[2]

# TOURNEYS

if t_mode == "1" or "s" or "solo" or "solos":  # Solos
    print("SOLOS!")

    if t_type == "cc" or "cash cup" or "Cash Cup":  # Cash Cup
        points_system = "100:0,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:0,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                        "80:0,79:0,78:0,77:0,76:0,75:1,74:0,73:0,72:0,71:0,70:0,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                        "60:0,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:1,49:0,48:0,47:0,46:0,45:0,44:0,43:0,42:0,41:0," \
                        "40:1,39:0,38:0,37:0,36:0,35:0,34:0,33:0,32:0,31:0,30:1,29:0,28:0,27:0,26:0,25:1,24:0,23:0,22:0,21:0," \
                        "20:1,19:0,18:0,17:0,16:0,15:1,14:0,13:0,12:0,11:0,10:1,9:0,8:0,7:0,6:0,5:1,4:0,3:1,2:1,1:3/e-1,pk"
        if t_round == "1":  # 1-round cash cup
            all_sorted_players = rounds.solo_round_1(70000, 80000, 50, syntax, .35, True, points_system,
                                                     190)  # TODO adjust back

            report = input(
                "Would you like to get the match report of a player? (If yes, respond with # id, if no respond with 'n')")
            if not report == 'n':
                for all_p in range(len(all_sorted_players)):
                    if all_sorted_players[all_p].get_name() == report:
                        all_sorted_players[all_p].get_match_report()

        elif t_round == "2":  # 2-round cash cup
            all_sorted_players = rounds.solo_round_1(55000, 80000, 6, syntax, .4, True, points_system, 210)

            qualifiers = []

            for sb in range(100):
                player = methods.Player(all_sorted_players[sb].get_skill(), all_sorted_players[sb].get_rotation(),
                                        all_sorted_players[sb].get_drop_spot(),
                                        all_sorted_players[sb].get_play_style(), all_sorted_players[sb].get_name())
                qualifiers.append(player)

            # SECOND ROUND

            all_sorted_players = rounds.solo_custom(qualifiers, 6, -.2)

    elif t_type == "dh" or "DH" or "Dreamhack":  # TODO
        points_system = "100:0,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:0,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                        "80:0,79:0,78:0,77:0,76:0,75:0,74:0,73:0,72:0,71:0,70:0,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                        "60:0,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:1,49:1,48:1,47:1,46:1,45:1,44:1,43:1,41:2,41:1," \
                        "40:1,39:1,38:1,37:1,36:1,35:1,34:1,33:1,32:1,31:1,30:1,29:1,28:1,27:1,26:1,25:1,24:1,23:1,22:1,21:1," \
                        "20:1,19:1,18:1,17:1,16:1,15:1,14:1,13:1,12:1,11:1,10:1,9:1,8:1,7:1,6:1,5:1,4:1,3:2,2:4,1:7/e-5,pk"

        all_sorted_players = rounds.solo_round_1(75000, 100000, 10, syntax, -.1, True, points_system, 220)

        report = input(
            "Would you like to get the match report of a player? (If yes, respond with # id, if no respond with 'n')")
        if not report == 'n':
            for all_p in range(len(all_sorted_players)):
                if all_sorted_players[all_p].get_name() == report:
                    all_sorted_players[all_p].get_match_report()
    
    elif t_type == "fncs" or "FNCS":  # TODO
        points_system = "100:0,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:0,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                        "80:0,79:0,78:0,77:0,76:0,75:1,74:0,73:0,72:0,71:0,70:0,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                        "60:0,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:1,49:0,48:0,47:0,46:0,45:0,44:0,43:0,42:0,41:0," \
                        "40:1,39:0,38:0,37:0,36:0,35:0,34:0,33:0,32:0,31:0,30:1,29:0,28:0,27:0,26:0,25:1,24:0,23:0,22:0,21:0," \
                        "20:1,19:0,18:0,17:0,16:0,15:1,14:0,13:0,12:0,11:0,10:1,9:0,8:0,7:0,6:0,5:1,4:0,3:1,2:1,1:3/e-1,pk"

        all_sorted_players = rounds.solo_round_1(11000, 20000, 7, syntax, -.2, False, points_system, 480)

        heat_qualifiers = []
        grands_qualifiers = []

    elif t_type == "wc" or "WC" or "world cup" or "World Cup":
        points_system = "100:0,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:0,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                        "80:0,79:0,78:0,77:0,76:0,75:0,74:0,73:0,72:0,71:0,70:0,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                        "60:0,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:0,49:0,48:0,47:0,46:0,45:0,44:0,43:0,42:0,41:0," \
                        "40:0,39:0,38:0,37:0,36:0,35:0,34:0,33:0,32:0,31:0,30:0,29:0,28:0,27:0,26:0,25:3,24:0,23:0,22:0,21:0," \
                        "20:0,19:0,18:0,17:0,16:0,15:2,14:0,13:0,12:0,11:0,10:0,9:0,8:0,7:0,6:0,5:2,4:0,3:0,2:0,1:3/e-1,pk"

        solo_final_quals = []
        duo_final_quals = []

        solo_finals = []
        duo_finals = []

        for week in range(10):
            for region in range(6):
                if week + 1 % 2 == 1:  # Solos
                    min = 0
                    if region == 0 or 1 or 4:  # OCE, ASIA, BRAZIL
                        min = 500
                        if region == 0:
                            print("OCE week", week + 1)
                        if region == 1:
                            print("ASIA week", week + 1)
                        if region == 4:
                            print("BRAZIL week", week + 1)
                    elif region == 2 or 3:  # EU, NAE
                        min = 460
                        if region == 2:
                            print("EU week", week + 1)
                        if region == 0:
                            print("NAE week", week + 1)
                    elif region == 6:  # NAW
                        min = 470
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

elif t_mode == "2" or "d" or "duo" or "duos":  # Duos
    a = 0  # Placeholder
    # EMPTY

elif t_mode == "3" or "t" or "trio" or "trios":  # Trios
    a = 0  # Placeholder
    # EMPTY

elif t_mode == "4" or "sq" or "squad" or "squads":  # Squads
    a = 0  # Placeholder
    # EMPTY

if tourney_type == "man":  # Manual (using for debugging right now)
    player_amt = 100  # random.randint(7, 10) * 100
    print("There are", player_amt, "people playing in this tournament.")

    m = 6
    tourneys = 100
    p_var = 5  # Player variation, determines how many times players are shuffled and recreated

    points_system = "100:1,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:1,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                    "80:1,79:0,78:0,77:0,76:0,75:0,74:0,73:0,72:0,71:0,70:1,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                    "60:1,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:1,49:0,48:0,47:0,46:0,45:0,44:0,43:0,42:0,41:0," \
                    "40:1,39:0,38:0,37:0,36:0,35:0,34:0,33:0,32:0,31:0,30:1,29:0,28:0,27:0,26:0,25:1,24:0,23:0,22:0,21:0," \
                    "20:1,19:0,18:0,17:0,16:0,15:1,14:0,13:0,12:0,11:0,10:1,9:1,8:1,7:1,6:1,5:1,4:1,3:1,2:2,1:4/e-1,pk"

    print(points_system)

    all_sorted_players = []

    for rng in range(p_var):
        for i in range(player_amt - len(all_players)):
            name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
            skill = 500
            play_style = .5
            drop_spot = random.randint(0, 30)
            rotation = 500
            player = Player(skill, rotation, drop_spot, play_style, name)
            player.set_t_var(random.randint(0, 20) - random.randint(0, 20))
            all_players.append(player)
            player_pool.append(player)

        for extra in range(int(tourneys / p_var)):
            for var in range(len(player_pool)):
                player_pool[var].set_t_var(random.randint(0, 20) - random.randint(0, 20))
            print("")
            print("")
            print("")
            print("")
            print("Tournament", extra, "starting!")
            for matches in range(m + 1):
                if matches > 1:
                    for i in range(len(all_sorted_players)):
                        prev_removed = 0
                        if (all_sorted_players[int(player_amt / 100)].get_points() - all_sorted_players[
                            i].get_points()) > 80:
                            if random.randint(0, all_sorted_players[i].get_points() * 4) == random.randint(0,
                                                                                                           all_sorted_players[
                                                                                                               i].get_points() * 4):
                                if player_pool.__contains__(all_sorted_players[i - prev_removed]):
                                    player_pool.remove(all_sorted_players[i - prev_removed])
                                    prev_removed += 1

                    removed = 0
                    for p in range(len(player_pool)):
                        pt_diff = player_pool[int(player_amt * .03)].get_points() - player_pool[p].get_points()
                        if pt_diff > 0:
                            player_pool[p].set_drop_spot(
                                player_pool[p].get_drop_spot() + random.randint(0, int(pt_diff / 5)))

                time_playing_s = time.time()  # Start time

                if matches == 0:
                    all_matches = methods.create_play_matches(player_pool, 0, True)
                    all_matches_tourney += len(all_matches)
                else:
                    all_matches = methods.create_play_matches(all_sorted_players, 1 - (matches / 10) - .3, True)
                    all_matches_tourney += len(all_matches)

                time_playing = (time.time() - time_playing_s).__round__(3)

                # Create scoreboard
                time_sorting_s = time.time()  # Start time

                all_sorted_players = methods.create_scoreboard(2, all_players, points_system, True)

                time_sorting = (time.time() - time_sorting_s).__round__(3)

            total_points = 0

            all_sorted_players = methods.create_scoreboard(2, all_players, points_system, False)

            # Showing scoreboard
            print("\nSCOREBOARD:")
            for sb in range(len(all_sorted_players)):
                if sb < 10 and all_sorted_players[sb].get_matches() > 0:
                    print(sb + 1, ". ", all_sorted_players[sb].get_name(), " - Points: ",
                          round(all_sorted_players[sb].get_points(), 2), " | "
                                                                         "Avg kills: ",
                          round(all_sorted_players[sb].get_total_kills() / m, 2), " | Avg placement: ",
                          round(all_sorted_players[sb].get_avg_placement(), 2),
                          " | Skill: ", all_sorted_players[sb].get_skill(), " | Rotation: ",
                          all_sorted_players[sb].get_rotation(), " | "
                                                                 "Style: ",
                          round(all_sorted_players[sb].get_play_style(), 2), " | Drop: ",
                          all_sorted_players[sb].get_drop_spot(), " | "
                                                                  "Avg finish: ",
                          round(all_sorted_players[sb].get_avg_finish(), 2), " | Wins: ",
                          all_sorted_players[sb].get_t_wins(), sep="")
                if all_sorted_players[sb].get_matches() > 0:
                    total_points += all_sorted_players[sb].get_points()
                    all_sorted_players[sb].set_finish(sb + 1)
                    all_sorted_players[sb].reset_points()

            avg_points = int(total_points / len(all_sorted_players))

            print("The average player had ", avg_points, " points.", sep="")

        total_points = 0

        # FINAL SORT
        s_players = methods.create_scoreboard(3, all_players, points_system, False)

        # Showing scoreboard
        print("\nSCOREBOARD: (with", len(s_players), "players)")
        for sb in range(len(s_players)):
            if sb < 5000:
                print(sb + 1, ". ", s_players[sb].get_name(), " - Avg points: ",
                      round(s_players[sb].get_avg_points(), 2), " | "
                                                                "Avg kills: ",
                      round(s_players[sb].get_avg_kills(), 2), " | Avg placement: ",
                      round(s_players[sb].get_avg_place(), 2),
                      " | Skill: ", s_players[sb].get_skill(), " | Rotation: ",
                      s_players[sb].get_rotation(), " | "
                                                    "Style: ",
                      round(s_players[sb].get_play_style(), 2), " | Drop: ",
                      s_players[sb].get_drop_spot(), " | "
                                                     "Avg finish: ",
                      round(s_players[sb].get_avg_finish(), 2), " | Wins: ",
                      s_players[sb].get_t_wins(), sep="")
            total_points += s_players[sb].get_points()

        avg_points = int(total_points / len(s_players))

        print("The average player had ", avg_points, " points.", sep="")

if tourney_type == "gosu":  # Manual (using for debugging right now)
    # Vars that change:
    skill_bias = .3  # between 0 and 1 (distribution: .95 is WC level | .1 is all bots | .6 is DH)

    player_amt = 100  # random.randint(7, 10) * 100
    print("There are", player_amt, "people playing in this tournament.")

    m = 6
    tourneys = 1000
    p_var = 20  # Player variation, determines how many times players are shuffled and recreated

    points_system = "100:1,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:1,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                    "80:1,79:0,78:0,77:0,76:0,75:0,74:0,73:0,72:0,71:0,70:1,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                    "60:1,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:1,49:0,48:0,47:0,46:0,45:0,44:0,43:0,42:0,41:0," \
                    "40:1,39:0,38:0,37:0,36:0,35:0,34:0,33:0,32:0,31:0,30:1,29:0,28:0,27:0,26:0,25:1,24:0,23:0,22:0,21:0," \
                    "20:1,19:0,18:0,17:0,16:0,15:1,14:0,13:0,12:0,11:0,10:1,9:1,8:1,7:1,6:1,5:1,4:1,3:1,2:2,1:4/e-1,pk"

    print(points_system)

    all_sorted_players = []

    plasmic = Player(767, 874, 23, .51, "Plasmic.TA")
    all_players.append(plasmic)
    all_sorted_players.append(plasmic)

    gingy = Player(748, 772, 5, .54, "FaZe Gingy")
    all_players.append(gingy)
    all_sorted_players.append(gingy)

    vanish = Player(711, 540, 4, .48, "BH Vanish")
    all_players.append(vanish)
    all_sorted_players.append(vanish)

    cazm = Player(724, 638, 7, .39, "TyB Cazm")
    all_players.append(cazm)
    all_sorted_players.append(cazm)

    dizzle = Player(648, 620, 12, .4, "YT DizzleFN")
    all_players.append(dizzle)
    all_sorted_players.append(dizzle)

    cxleb = Player(734, 684, 6, .61, "vCxlebFN")
    all_players.append(cxleb)
    all_sorted_players.append(cxleb)

    parinoia = Player(691, 632, 14, .38, "Parinoia FC")
    all_players.append(parinoia)
    all_sorted_players.append(parinoia)

    ashton = Player(724, 712, 11, .41, "OG Ashton.")
    all_players.append(ashton)
    all_sorted_players.append(ashton)

    scoped = Player(641, 589, 22, .24, "The ScopedTV")
    all_players.append(scoped)
    all_sorted_players.append(scoped)

    wavvy = Player(768, 640, 2, .49, "Wavvy Boi")
    all_players.append(wavvy)
    all_sorted_players.append(wavvy)

    keru = Player(791, 784, 16, .43, "Keru")
    all_players.append(keru)
    all_sorted_players.append(keru)

    nick = Player(634, 548, 5, .51, "?Nick")
    all_players.append(nick)
    all_sorted_players.append(nick)

    b1tch = Player(679, 581, 9, .39, "FLYJuan1tho")
    all_players.append(b1tch)
    all_sorted_players.append(b1tch)

    sundown = Player(684, 612, 7, .51, "SxD0wn")
    all_players.append(sundown)
    all_sorted_players.append(sundown)

    perfect = Player(750, 700, 8, .5, "PERFECT")
    all_players.append(perfect)
    all_sorted_players.append(perfect)

    naz = Player(734, 791, 9, .58, "TA Nazariy")
    all_players.append(naz)
    all_sorted_players.append(naz)

    for rng in range(p_var):
        for i in range(player_amt - len(all_players)):
            p_skill = random.randint(30, 65) + random.random() - random.random()

            name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
            min_skill = int(p_skill * 10) - int(p_skill / 4)
            max_skill = int(p_skill * 10) + int(p_skill / 4)
            skill = int(p_skill * 10) + random.randint(0, int(p_skill / 4)) - random.randint(0, int(p_skill / 4))
            while skill <= 0:
                skill += random.randint(0, int(p_skill))
            play_style = (((p_skill / 100) * 10 + random.random()) / 10) - skill_bias
            drop_spot = random.randint(1, 30)
            rotation = int(p_skill * 10) + random.randint(0, int(p_skill / 4)) - random.randint(0, int(p_skill / 4))
            while rotation <= 0:
                rotation += random.randint(0, int(p_skill))
            player = Player(skill, rotation, drop_spot, play_style, name)
            player.set_t_var(random.randint(0, 20) - random.randint(0, 20))
            all_players.append(player)
            player_pool.append(player)

        for extra in range(int(tourneys / p_var)):
            for var in range(len(player_pool)):
                player_pool[var].set_t_var(random.randint(0, 20) - random.randint(0, 20))
            print("")
            print("")
            print("")
            print("")
            print("Tournament", extra+1, "starting!")
            for matches in range(m + 1):
                if matches > 1:
                    for i in range(len(all_sorted_players)):
                        prev_removed = 0
                        if (all_sorted_players[int(player_amt / 100)].get_points() - all_sorted_players[
                            i].get_points()) > 80:
                            if random.randint(0, all_sorted_players[i].get_points() * 4) == random.randint(0,
                                                                                                           all_sorted_players[
                                                                                                               i].get_points() * 4):
                                if player_pool.__contains__(all_sorted_players[i - prev_removed]):
                                    player_pool.remove(all_sorted_players[i - prev_removed])
                                    prev_removed += 1

                time_playing_s = time.time()  # Start time

                if matches == 0:
                    all_matches = methods.create_play_matches(player_pool, 0, True)
                    all_matches_tourney += len(all_matches)
                else:
                    all_matches = methods.create_play_matches(all_sorted_players, 1 - (matches / 10) - .3, True)
                    all_matches_tourney += len(all_matches)

                time_playing = (time.time() - time_playing_s).__round__(3)

                # Create scoreboard
                time_sorting_s = time.time()  # Start time

                all_sorted_players = methods.create_scoreboard(2, all_players, points_system, True)

                time_sorting = (time.time() - time_sorting_s).__round__(3)

            total_points = 0

            all_sorted_players = methods.create_scoreboard(2, all_players, points_system, False)

            # Showing scoreboard
            print("\nSCOREBOARD:")
            for sb in range(len(all_sorted_players)):
                if sb < 10 and all_sorted_players[sb].get_matches() > 0:
                    print(sb + 1, ". ", all_sorted_players[sb].get_name(), " - Points: ",
                          round(all_sorted_players[sb].get_points(), 2), " | "
                                                                         "Avg kills: ",
                          round(all_sorted_players[sb].get_total_kills() / m, 2), " | Avg placement: ",
                          round(all_sorted_players[sb].get_avg_placement(), 2),
                          " | Skill: ", all_sorted_players[sb].get_skill(), " | Rotation: ",
                          all_sorted_players[sb].get_rotation(), " | "
                                                                 "Style: ",
                          round(all_sorted_players[sb].get_play_style(), 2), " | Drop: ",
                          all_sorted_players[sb].get_drop_spot(), " | "
                                                                  "Avg finish: ",
                          round(all_sorted_players[sb].get_avg_finish(), 2), " | Wins: ",
                          all_sorted_players[sb].get_t_wins(), sep="")
                if all_sorted_players[sb].get_matches() > 0:
                    total_points += all_sorted_players[sb].get_points()
                    all_sorted_players[sb].set_finish(sb + 1)
                    all_sorted_players[sb].reset_points()

            avg_points = int(total_points / len(all_sorted_players))

            print("The average player had ", avg_points, " points.", sep="")

        total_points = 0

        # FINAL SORT
        s_players = methods.create_scoreboard(3, all_players, points_system, False)

        # Showing scoreboard
        print("\nSCOREBOARD: (with", len(s_players), "players)")
        for sb in range(len(s_players)):
            if sb < 5000:
                print(sb + 1, ". ", s_players[sb].get_name(), " - Avg points: ",
                      round(s_players[sb].get_avg_points(), 2), " | "
                                                                "Avg kills: ",
                      round(s_players[sb].get_avg_kills(), 2), " | Avg placement: ",
                      round(s_players[sb].get_avg_place(), 2),
                      " | Skill: ", s_players[sb].get_skill(), " | Rotation: ",
                      s_players[sb].get_rotation(), " | "
                                                    "Style: ",
                      round(s_players[sb].get_play_style(), 2), " | Drop: ",
                      s_players[sb].get_drop_spot(), " | "
                                                     "Avg finish: ",
                      round(s_players[sb].get_avg_finish(), 2), " | Wins: ",
                      s_players[sb].get_t_wins(), sep="")
            total_points += s_players[sb].get_points()

        avg_points = int(total_points / len(s_players))

        print("The average player had ", avg_points, " points.", sep="")

elif tourney_type == "man-1p":
    # Point Calculator
    done = False
    while not done:
        response = input(
            "Please type the placement and eliminations of the player below: (type help if you need help or end if you want to end)")
        if response == "end":
            print("Ended.")
            done = True
        elif response == "help":
            print("The format for typing is: p:##-e:##-<name>")
        elif response == "calc":
            points = int(input("Please input a number you wish for a player to obtain."))
            if not points == 0:
                for p in range(1, 100):
                    player = Player(0, 0, 0, 0, "test")
                    player.set_placement_match(p)
                    methods.give_points(player, points_system)
                    if player.get_points() == points:
                        print(p, "place is", points)
                        done = False
                        i = 0
                        while not done:
                            i += 1
                            player.set_placement_match(p - i)
                            player.add_kills(1)
                            methods.give_points(player, points_system)
                            if player.get_points() == points:
                                print(p, "place is", points)
                            if i > 50:
                                done = True
                            player.add_points(-player.get_points())
                        player.reset_kills()
        else:
            placement = response.split("-")[0]
            elims = response.split("-")[1]
            name = response.split("-")[2]
            player = Player(0, 0, 0, 0, name)
            player.set_placement_match(int(placement.split(":")[1]))
            player.add_kills(int(elims.split(":")[1]))
            methods.give_points(player, points_system)
            print(player.get_name() + " got", player.get_points(), "points from this match.")
