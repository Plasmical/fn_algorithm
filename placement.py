import method_storage
import rounds

# DEFINITIONS

# Name system
syntax = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_$#%.*!"

# Starting point system
points_system = "p-25:3,15:2,5:2,1:3/e-1,pk"
placement_points = ""
elim_points = 0

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

split_system = points_system.split("/")  # splits placement and elims

p_split2 = split_system[0].split("-")  # splits off bloatware
placement_pts = p_split2[1].split(",")  # splits between different placements

e_split2 = split_system[1].split("-")  # splits off bloatware
elim_pts = int(e_split2[1].split(",")[0])  # gets elim points

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
    all_sorted_players = rounds.solo_round_1(70000/10, 80000/10, 10, syntax, .35, 3, True)

    report = input(
        "Would you like to get the match report of a player? (If yes, respond with # id, if no respond with 'n')")
    if not report == 'n':
        for all_p in range(len(all_sorted_players)):
            if all_sorted_players[all_p].get_name() == report:
                all_sorted_players[all_p].get_match_report()

elif tourney_type == 1:  # Two-round cash cups
    all_sorted_players = rounds.solo_round_1(55000, 80000, 6, syntax, .4, 3, True)

    qualifiers = []

    for sb in range(100):
        player = methods.Player(all_sorted_players[sb].get_skill(), all_sorted_players[sb].get_drop_spot(),
                                all_sorted_players[sb].get_play_style(), all_sorted_players[sb].get_name())
        qualifiers.append(player)

    # SECOND ROUND

    all_sorted_players = rounds.solo_custom(qualifiers, 6, -.2)

elif tourney_type == 3:  # FNCS (Solos)
    all_sorted_players = rounds.solo_round_1(11000, 15000, 7, syntax, -.2, 1, False)

    heat_qualifiers = []
    grands_qualifiers = []

elif tourney_type == 4:  # World Cup Style
    solo_final_quals = []
    duo_final_quals = []

    solo_finals = []
    duo_finals = []

    for week in range(10):
        for region in range(6):
            if week+1 % 2 == 1:  # Solos
                spread = 0
                if region == 0 or 1 or 4:  # OCE, ASIA, BRAZIL
                    spread = 4
                    if region == 0:
                        print("OCE week", week+1)
                    if region == 1:
                        print("ASIA week", week+1)
                    if region == 4:
                        print("BRAZIL week", week+1)
                elif region == 2 or 3:  # EU, NAE
                    spread = 3
                    if region == 2:
                        print("EU week", week+1)
                    if region == 0:
                        print("NAE week", week+1)
                elif region == 6:  # NAW
                    spread = 2
                    if region == 0:
                        print("NAW week", week+1)
                all_sorted_player = rounds.solo_round_1(100000/10, 125000/10, 10, syntax, .1, spread, False)

                weekly_qualifiers = []
                sunday_qualifiers = []

                for sb in range(3000):
                    player = methods.Player(all_sorted_player[sb].get_skill(), all_sorted_player[sb].get_drop_spot(),
                                            all_sorted_player[sb].get_play_style(), all_sorted_player[sb].get_name())
                    sunday_qualifiers.append(player)

                # SECOND ROUND

                all_sorted_players = rounds.solo_round_2(sunday_qualifiers, 10, -.3)

                if region == 0:  # OCE
                    solo_final_quals.append(all_sorted_player[0])
                elif region == 1 or 4:  # ASIA, BRAZIL
                    if week+1 == 1 or 5 or 9:
                        solo_final_quals.append(all_sorted_player[0])
                    elif week+1 == 3 or 7:
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

    # Solo finals
    solo_finals = rounds.solo_custom(solo_final_quals, 6, -.5)

    for s_finals in range(len(solo_finals)):
        print("#", s_finals+1, " ", solo_finals[s_finals].get_name(), " - ", solo_finals[s_finals].get_points(),
              " points with ", solo_finals[s_finals].get_wins(), " wins", sep="")
