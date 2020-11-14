# This is manual right now

# Vars that change:
    skill_bias = 1.3  # between .6 and 1.4 (distribution: 1.35 is WC level | .6 is all bots | 1 is DH)

    player_amt = 100  # random.randint(7, 10) * 100
    print("There are", player_amt, "people playing in this tournament.")

    m = 10
    tourneys = 100

    points_system = "100:1,99:0,98:0,97:0,96:0,95:0,94:0,93:0,92:0,91:0,90:0,89:0,88:0,87:0,86:0,85:0,84:0,83:0,82:0,81:0," \
                    "80:0,79:0,78:0,77:0,76:0,75:1,74:0,73:0,72:0,71:0,70:0,69:0,68:0,67:0,66:0,65:0,64:0,63:0,62:0,61:0," \
                    "60:0,59:0,58:0,57:0,56:0,55:0,54:0,53:0,52:0,51:0,50:1,49:0,48:0,47:0,46:0,45:0,44:0,43:0,42:0,41:0," \
                    "40:1,39:0,38:0,37:0,36:0,35:0,34:0,33:0,32:0,31:0,30:1,29:0,28:0,27:0,26:0,25:1,24:0,23:0,22:0,21:0," \
                    "20:1,19:0,18:0,17:0,16:0,15:1,14:0,13:0,12:0,11:0,10:1,9:0,8:0,7:0,6:0,5:1,4:0,3:1,2:1,1:3/e-1,pk"

    print(points_system)

    all_sorted_players = []

    perfect = Player(500, 500, 15, .5, "Perfect Player")
    all_players.append(perfect)
    all_sorted_players.append(perfect)

    plasmic = Player(767, 874, 24, .02, "Plasmic.TA")
    all_players.append(plasmic)
    all_sorted_players.append(plasmic)

    # nazariy = Player(754, 743, 8, .12, "TA Nazariy")
    # all_players.append(nazariy)
    # all_sorted_players.append(nazariy)

    key = methods.create_player(skill_bias, syntax, 1000, 400, .8, 2, "HARD KEY++++")
    # s_key = methods.create_player(skill_bias, syntax, 940, 550, .4, 7, "SEMI KEY++++")
    mid = methods.create_player(skill_bias, syntax, 900, 750, .2, 14, "MEDIUM++++")
    # s_passive = methods.create_player(skill_bias, syntax, 840, 860, .12, 19, "SEMI PASSIVE++++")
    passive = methods.create_player(skill_bias, syntax, 750, 920, .01, 30, "HARD PASSIVE++++")
    all_players.append(key)
    all_sorted_players.append(key)
    # all_players.append(s_key)
    # all_sorted_players.append(s_key)
    all_players.append(mid)
    all_sorted_players.append(mid)
    # all_players.append(s_passive)
    # all_sorted_players.append(s_passive)
    all_players.append(passive)
    all_sorted_players.append(passive)

    for i in range(player_amt - len(all_players)):
        p_skill = random.randint(int((skill_bias / 1.4) * 100), 100) + random.random()

        name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
        min_skill = int(p_skill * 10) - int(p_skill / 4)
        max_skill = int(p_skill * 10) + int(p_skill / 4)
        skill = int(p_skill * 10) + random.randint(0, int(p_skill / 4)) - random.randint(0, int(p_skill / 4))
        while skill <= 0:
            skill += random.randint(0, int(p_skill))
        play_style = (((p_skill / 100) * 10 + random.random()) / 10) - (skill_bias / 1.4)
        drop_spot = random.randint(1, int(p_skill / 3))
        while drop_spot > 30 or drop_spot < 1:
            drop_spot -= random.randint(0, int(p_skill / 10))
        rotation = int(p_skill * 10) + random.randint(0, int(p_skill / 4)) - random.randint(0, int(p_skill / 4))
        while rotation <= 0:
            rotation += random.randint(0, int(p_skill))
        all_players.append(Player(skill, rotation, drop_spot, play_style, name))
        player_pool.append(Player(skill, rotation, drop_spot, play_style, name))

    last_p_place = 0
    last_adjust = None  # Used for adjusting large amounts
    best = None
    best_adjust = 101
    perfected = ""
    for extra in range(tourneys):
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
                    if player_pool[p].get_points() + 2 < player_pool[
                        p].get_matches() and random.random() > random.random():
                        del (player_pool[p - removed])
                        removed += 1
                    new_drop = player_pool[p].get_drop_spot()
                    pt_diff = player_pool[int(player_amt * .03)].get_points() - player_pool[p].get_points()
                    if pt_diff > 0:
                        player_pool[p].set_drop_spot(
                            player_pool[p].get_drop_spot() + random.randint(0, int(pt_diff / 5)))
                    while new_drop > 30:
                        new_drop -= random.randint(0, 10)

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
        perfectC = None
        p_place = 0
        print("\nSCOREBOARD:")
        for sb in range(len(all_sorted_players)):
            if sb < 10 and all_sorted_players[sb].get_matches() > 0:
                print(sb + 1, ". ", all_sorted_players[sb].get_name(), " - ", all_sorted_players[sb].get_points(),
                      " points; Skill: ",
                      all_sorted_players[sb].get_skill(), "/1000, play style: ",
                      all_sorted_players[sb].get_play_style().__round__(4),
                      ", rotation ability: ", all_sorted_players[sb].get_rotation(), "; Average finish: ",
                      round(all_sorted_players[sb].get_avg_finish(), 1), sep="")
            if all_sorted_players[sb].get_matches() > 0:
                total_points += all_sorted_players[sb].get_points()
                all_sorted_players[sb].set_finish(sb + 1)
                all_sorted_players[sb].reset_points()
            if all_sorted_players[sb].get_name() == perfect.get_name():
                p_place = sb
                perfectC = all_sorted_players[sb]

        if perfectC is not None:
            all_sorted_players.remove(perfectC)
            all_players.remove(perfectC)
            player_pool.remove(perfectC)
            print("Perfect player: finished ", p_place, " with skill ", perfectC.get_skill(), ", rotation of ",
                  perfectC.get_rotation(),
                  ", a play style of ", perfectC.get_play_style(), ", and a drop spot of ", perfectC.get_drop_spot(),
                  sep="")
            # Goes through each aspect of the player, up and down as well, until it finds what increases the placement the most, and it adjusts that until it doesn't move
            if last_p_place < best_adjust and not extra == 0 and extra < 9:
                best_adjust = last_p_place
                if (extra - 1) == 0:
                    best = "sU"
                if (extra - 1) == 2:
                    best = "rU"
                if (extra - 1) == 4:
                    best = "psU"
                if (extra - 1) == 6:
                    best = "dsD"
                if (extra - 1) == 1:
                    best = "sD"
                if (extra - 1) == 3:
                    best = "rD"
                if (extra - 1) == 5:
                    best = "psD"
                if (extra - 1) == 7:
                    best = "dsU"
                if best == "sU":
                    perfectC.set_skill(perfectC.get_skill() + random.randint(0, 100))
                if best == "sD":
                    perfectC.set_skill(perfectC.get_skill() - random.randint(0, 100))
                if best == "rU":
                    perfectC.set_rotation(perfectC.get_rotation() + random.randint(0, 100))
                if best == "rD":
                    perfectC.set_rotation(perfectC.get_rotation() - random.randint(0, 100))
                if best == "psU":
                    perfectC.set_play_style(perfectC.get_play_style() + random.randint(0, .1))
                if best == "psD":
                    perfectC.set_play_style(perfectC.get_play_style() - random.randint(0, .1))
                if best == "dsU":
                    perfectC.set_drop_spot(perfectC.get_drop_spot() + random.randint(0, 3))
                if best == "dsD":
                    perfectC.set_drop_spot(perfectC.get_drop_spot() - random.randint(0, 3))
            if extra < 8:
                perfectC = perfect
                if extra == 0:
                    perfectC.set_skill(600)
                elif extra == 1:
                    perfectC.set_skill(400)
                if extra == 2:
                    perfectC.set_rotation(600)
                elif extra == 3:
                    perfectC.set_rotation(400)
                if extra == 4:
                    perfectC.set_play_style(.6)
                elif extra == 5:
                    perfectC.set_play_style(.4)
                if extra == 6:
                    perfectC.set_drop_spot(10)
                elif extra == 7:
                    perfectC.set_drop_spot(20)
            elif extra > 9:
                # TODO
                a = 1

            player_pool.append(perfectC)
            all_players.append(perfectC)
            all_sorted_players.append(perfectC)

        avg_points = int(total_points / len(all_sorted_players))

        print("The average player had ", avg_points, " points.", sep="")

    total_points = 0

    # FINAL SORT
    s_players = methods.create_scoreboard(3, all_players, points_system, False)

    # Showing scoreboard
    print("\nSCOREBOARD: (with", len(s_players), "players)")
    for sb in range(len(s_players)):
        if sb < 5000:
            print(sb + 1, ". ", s_players[sb].get_name(), " - Avg points: ", s_players[sb].get_avg_points(), " | "
                                                                                                             "Avg kills: ",
                  s_players[sb].get_avg_kills(), " | Avg placement: ", s_players[sb].get_avg_place(),
                  " | Skill: ", s_players[sb].get_skill(), " | Rotation: ", s_players[sb].get_rotation(), " | "
                                                                                                          "Style: ",
                  s_players[sb].get_play_style(), " | Drop: ", s_players[sb].get_drop_spot(), " | "
                                                                                              "Avg finish: ",
                  s_players[sb].get_avg_finish(), " | Wins: ", s_players[sb].get_t_wins(), sep="")
        total_points += s_players[sb].get_points()

    avg_points = int(total_points / len(s_players))

    print("The average player had ", avg_points, " points.", sep="")

    print("")

    report = input(
        "Would you like to get the match report of a player? (If yes, respond with # id, if no respond with 'n')")
    if not report == 'n':
        for all_p in range(len(s_players)):
            if s_players[all_p].get_name() == report:
                s_players[all_p].get_match_report()

    # write_to_file(m, tourneys, skill_bias, all_sorted_players)