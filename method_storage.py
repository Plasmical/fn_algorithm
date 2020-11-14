import random
from typing import List
import sys

progress_x = 0


class Player:
    points = 0
    points_match = 0
    kills = 0
    t_kills = 0
    matches = 0
    placement_match = 0
    avg_placement = 0
    total_placement = 0
    wins = 0
    match_report = []
    tourneys = 0
    t_var = 0  # between -20 and 20, is random every tournament, determines feeling of the day

    # Stats
    total_matches = 0
    total_finish = 0
    total_place = 0
    total_kills = 0
    total_pts = 0
    avg_finish = 0
    avg_place = 0
    avg_kills = 0
    avg_pts = 0
    t_wins = 0

    def __init__(self, mech, rotation, drop_spot, play_style, name):
        self._skill = mech
        self._rotate = rotation
        self._drop_spot = drop_spot
        self._play_style = play_style
        self._name = name
        self._match_report = self.match_report

    def add_match_report(self, points, kills, placement):
        self.points_match -= self.points
        m_report = self._name + " - Match " + str(len(self.match_report)) + ": kills-" + str(kills) + ", placement-" + str(placement) + ", points-" + str(points)
        self._match_report.append(m_report)
        self.matches += 1

    def get_match_report(self):  # TODO (broken)
        for reports in range(len(self._match_report)):
            if self._match_report.__contains__(self._name):
                print(self._match_report[reports])

    def set_t_var(self, t_var):
        self.t_var = t_var

    def get_t_var(self):
        return self.t_var

    def get_name(self):
        return self._name

    def get_wins(self):
        return self.wins

    def add_win(self):
        self.wins += 1

    def get_skill(self):
        return self._skill

    def set_skill(self, skill):
        self._skill = skill

    def get_points(self):
        return self.points

    def add_points(self, amt):
        self.points += amt

    def get_drop_spot(self):
        return self._drop_spot

    def set_drop_spot(self, new):
        self._drop_spot = new

    def get_play_style(self):
        return self._play_style

    def set_play_style(self, p_style):
        self._play_style = p_style

    def get_total_kills(self):
        return self.t_kills

    def add_total_kills(self):
        self.t_kills += self.kills

    def get_kills(self):
        return self.kills

    def add_kills(self, amt):
        self.kills += amt

    def reset_kills(self):
        self.kills = 0

    def get_matches(self):
        return self.matches

    def add_match(self):
        self.matches += 1

    def get_placement_match(self):
        return self.placement_match

    def set_placement_match(self, rank):
        self.placement_match = rank

    def get_avg_placement(self):
        return self.avg_placement

    def add_placement(self, place):
        self.total_placement += place

    def set_points_match(self):
        self.points_match = self.points

    def get_rotation(self):
        return self._rotate

    def set_rotation(self, rotate):
        self._rotate = rotate

    def set_finish(self, finish):
        self.total_finish += finish
        self.total_place += self.total_placement
        self.total_kills += self.t_kills
        self.total_pts += self.points
        if finish == 1:
            self.t_wins += 1

    def get_avg_finish(self):
        return self.avg_finish

    def get_avg_points(self):
        return self.avg_pts

    def get_avg_kills(self):
        return self.avg_kills

    def get_avg_place(self):
        return self.avg_place

    def get_t_wins(self):
        return self.t_wins

    def reset_points(self):
        self.tourneys += 1
        self.total_matches += self.matches
        self.avg_finish = self.total_finish / self.tourneys
        self.avg_place = self.total_place / self.total_matches
        self.avg_kills = self.total_kills / self.total_matches
        self.avg_pts = self.total_pts / self.tourneys
        self.points = 0
        self.matches = 0
        self.kills = 0
        self.t_kills = 0
        self.avg_placement = 0
        self.total_placement = 0
        self.wins = 0


class Match:
    players_alive = 0
    m_player_pool = []

    def __init__(self, m_player):
        self.m_player_pool = m_player
        self.players_alive = len(m_player)

    def simulation(self, s_bias):
        play_match(self.m_player_pool, s_bias)


# METHOD DECLARATION


def create_player(skill_bias, syntax, skill=None, rotation=None, play_style=None, drop=None, name=None):
    sk = skill
    ro = rotation
    ps = play_style
    dr = drop
    na = name

    p_skill = random.randint(int((skill_bias / 1.4) * 100), 100) + random.random()

    if na is None:
        name = ''.join((random.choice(syntax) for x in range(random.randint(3, 20))))
        na = name
    if sk is None:
        skill = int(p_skill * 10) + random.randint(0, int(p_skill / 4)) - random.randint(0, int(p_skill / 4))
        while skill <= 0:
            skill += random.randint(0, int(p_skill))
        sk = skill
    if ps is None:
        play_style = (((p_skill / 100) * 10 + random.random()) / 10) - (skill_bias / 1.4)
        ps = play_style
    if ro is None:
        rotation = random.randint(int(p_skill / 2 * 10), int(p_skill * 30))
        while rotation > 1000:
            rotation -= random.randint(10, 100)
        ro = rotation
    if dr is None:
        drop_spot = -1
        max_skill = int(p_skill * 10) + int(p_skill / 4)
        while drop_spot == -1:
            b1 = int((max_skill / 10 + random.randint(1, 5) - skill / 10) / 5)
            b2 = 1 - play_style
            drop_spot = int(b1 * b2)
            if drop_spot > 30:
                drop_spot /= 2
                drop_spot += random.randint(1, 3) - random.randint(1, 3)
            elif drop_spot < 1:
                drop_spot = 1
        dr = drop_spot
    p = Player(sk, ro, dr, ps, na)
    return p


def play_match(players_in_match, style_bias):
    players_alive = len(players_in_match)

    pool = players_in_match

    random.shuffle(pool)

    cycles = 0

    while players_alive > 1:
        avg_style = 0
        avg_drop = 0
        avg_skill = 0
        random.shuffle(pool)
        # Simulate the match
        if not len(pool) == 2:
            for pl in range(len(pool)):
                if pl >= len(pool):
                    break
                if random.randint(0, cycles) > random.randint(0, 50):
                    del (pool[pl])
                    continue
                nums = []
                for all_p in range(len(pool)):
                    avg_style += pool[all_p].get_play_style()
                    avg_drop += pool[all_p].get_drop_spot()
                    avg_skill += pool[all_p].get_skill()
                    if not all_p == pl:
                        if pool[all_p].get_rotation()/1000 < random.random()/1.02:
                            nums.append(all_p)
                avg_style /= len(pool)
                avg_drop /= len(pool)
                avg_skill /= len(pool)
                if cycles > 4:
                    if pool[pl].get_play_style() + style_bias > random.random():
                        p2 = -1
                        if len(nums) > 0:
                            nump = random.randint(0, len(nums) - 1)
                            p2 = nums[nump]
                        if p2 != -1:
                            p1skill = pool[pl].get_skill() + random.random() * cycles + random.randint(10, 110) + pool[pl].get_t_var()
                            p2skill = pool[p2].get_skill() + random.random() * cycles + random.randint(5, 100) + pool[p2].get_t_var()
                            if p1skill >= p2skill:
                                pool[pl].add_kills(1)
                                pool[p2].set_placement_match(players_alive)
                                del (pool[p2])
                                players_alive -= 1
                            else:
                                pool[p2].add_kills(1)
                                pool[pl].set_placement_match(players_alive)
                                del (pool[pl])
                                players_alive -= 1
                else:
                    if pool[pl].get_play_style() + style_bias > random.random():
                        p2 = -1
                        for pn in range(len(pool)):
                            if not pn == pl:
                                if pool[pl].get_drop_spot() == pool[pn].get_drop_spot():
                                    p2 = pn
                        if not p2 == -1:
                            p1skill = pool[pl].get_skill() + random.random() * 50 + random.randint(10, 150) + pool[
                                pl].get_t_var()
                            p2skill = pool[p2].get_skill() + random.random() * 50 + random.randint(10, 150) + pool[
                                p2].get_t_var()
                            if p1skill >= p2skill:
                                pool[pl].add_kills(1)
                                pool[p2].set_placement_match(players_alive)
                                del (pool[p2])
                                players_alive -= 1
                            else:
                                pool[p2].add_kills(1)
                                pool[pl].set_placement_match(players_alive)
                                del (pool[pl])
                                players_alive -= 1
            cycles += 1

            # self debug
            if cycles >= 50:
                while players_alive > 2:
                    pl = random.randint(0, len(pool)-1)
                    p2 = -1
                    while p2 == -1 or p2 == pl:
                        p2 = random.randint(0, len(pool)-1)
                    if p2 != -1:
                        p1skill = pool[pl].get_skill() + random.random() * cycles + random.randint(15, 25)
                        p2skill = pool[p2].get_skill() + random.random() * cycles + random.randint(0, 15)
                        if p1skill >= p2skill:
                            pool[pl].add_kills(1)
                            pool[p2].set_placement_match(players_alive)
                            del (pool[p2])
                            players_alive -= 1
                        else:
                            pool[p2].add_kills(1)
                            pool[pl].set_placement_match(players_alive)
                            del (pool[pl])
                            players_alive -= 1
        elif len(pool) == 2:
            if (pool[0].get_skill() + random.random() * 20 + 20) >= (
                    pool[1].get_skill() + random.random() * 20):
                pool[0].add_kills(1)
                pool[1].set_placement_match(2)
                del (pool[1])
                players_alive -= 1
            else:
                pool[1].add_kills(1)
                pool[0].set_placement_match(2)
                del (pool[0])
                players_alive -= 1
        if players_alive == 1:
            pool[0].set_placement_match(1)
        players_alive = len(pool)


def give_points(to_give, points_system):
    if to_give.get_placement_match() == 0:
        return

    p_points = 0

    split_system = points_system.split("/")  # splits placement and elims

    placement_pts = split_system[0].split(",")  # splits between different placements
    placements = []
    points_give = []
    for i in range(len(placement_pts)):
        temp = placement_pts[i].split(":")
        placements.append(int(temp[0]))
        points_give.append(int(temp[1]))

    e_split2 = split_system[1].split("-")  # splits off bloatware
    elim_pts = int(e_split2[1].split(",")[0])  # gets elim points

    to_give.add_points(to_give.get_kills() * elim_pts)
    p_points += to_give.get_kills() * elim_pts

    if to_give.get_placement_match() == 1:
        to_give.add_points(points_give[0])
        to_give.add_win()

    for p in range(len(placement_pts)):
        if p + 1 == len(placement_pts):
            continue
        if to_give.get_placement_match() <= placements[p]:
            to_give.add_points(points_give[p])
            p_points += points_give[p]
        else:
            break
    to_give.add_match()
    to_give.set_points_match()
    to_give.add_placement(to_give.get_placement_match())
    to_give.add_total_kills()
    to_give.reset_kills()


def sort_players(to_sort_t, points_system, give_pts):
    all_sorted_players_d: List[Player] = []

    to_sort = to_sort_t

    if give_pts:
        for pl_to_add in range(len(to_sort)):  # Loop over all players to be added
            give_points(to_sort[pl_to_add], points_system)

    for pl_to_add in range(len(to_sort)):  # Loop over all players to be added
        if pl_to_add == 0:  # Check if list is empty
            all_sorted_players_d.append(to_sort[pl_to_add])
            continue
        if to_sort[pl_to_add].get_matches() == 0:
            all_sorted_players_d.append(to_sort[pl_to_add])
            continue
        for al_added in range(len(all_sorted_players_d)):  # Loop over players in scoreboard
            if to_sort[pl_to_add].get_points() > all_sorted_players_d[al_added].get_points():
                # Has more points than this player so add him
                all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
                break  # Prevent adding multiple times
            elif to_sort[pl_to_add].get_points() == all_sorted_players_d[al_added].get_points():  # Tiebreaker
                if to_sort[pl_to_add].get_wins() > to_sort[al_added].get_wins():
                    # Has more wins than this player so add him
                    all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
                    break  # Prevent adding multiple times
                elif to_sort[pl_to_add].get_wins() == all_sorted_players_d[al_added].get_wins():  # Tiebreaker
                    if to_sort[pl_to_add].get_total_kills() > all_sorted_players_d[al_added].get_total_kills():
                        # Has more kills than this player
                        all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
                        break  # Prevent adding multiple times
                    elif to_sort[pl_to_add].get_total_kills() == all_sorted_players_d[al_added].get_total_kills():
                        if to_sort[pl_to_add].get_avg_placement() < all_sorted_players_d[al_added].get_avg_placement():
                            # Has better placement than this player
                            all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
                            break  # Prevent adding multiple times
                        elif to_sort[pl_to_add].get_avg_placement() == all_sorted_players_d[al_added].get_avg_placement():
                            # Has equal placement than this player
                            all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
                            break  # Prevent adding multiple times
            if al_added + 1 >= len(all_sorted_players_d):
                all_sorted_players_d.append(to_sort[pl_to_add])
        progress_bar(pl_to_add, len(to_sort), "Sorting players:")

    return all_sorted_players_d


def sort_players_finish(to_sort_t):
    all_sorted_players_d: List[Player] = []

    to_sort = to_sort_t

    for pl_to_add in range(len(to_sort)):  # Loop over all players to be added
        if pl_to_add == 0:  # Check if list is empty
            all_sorted_players_d.append(to_sort[pl_to_add])
            continue
        for al_added in range(len(all_sorted_players_d)):  # Loop over players in scoreboard
            if to_sort[pl_to_add].get_avg_finish() < all_sorted_players_d[al_added].get_avg_finish():
                # Has better finish than this player so add him
                all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
                break  # Prevent adding multiple times
            if al_added + 1 >= len(all_sorted_players_d):
                all_sorted_players_d.append(to_sort[pl_to_add])
        progress_bar(pl_to_add, len(to_sort), "Sorting players:")

    return all_sorted_players_d


def sort_players_skip(to_sort, skip_at):
    all_sorted_players_d = []

    for pl_to_add in range(len(to_sort)):  # Loop over players to add
        if to_sort[pl_to_add].get_points() <= skip_at:  # Skip if player has less or equal points to req.
            continue
        if pl_to_add == 0:  # Check if list is empty
            all_sorted_players_d.append(to_sort[pl_to_add])
            continue
        for al_added in range(len(all_sorted_players_d)):  # Loop over players in scoreboard
            if to_sort[pl_to_add].get_points() > all_sorted_players_d[al_added].get_points():
                # Has more points than this player so add him
                all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
            elif to_sort[pl_to_add].get_points() == all_sorted_players_d[al_added].get_points():  # Tiebreaker
                if to_sort[pl_to_add].get_total_kills() > all_sorted_players_d[al_added].get_total_kills():
                    # Has more kills than this player
                    all_sorted_players_d.insert(al_added, to_sort[pl_to_add])
                # TODO

    return all_sorted_players_d


def create_scoreboard(type_scoreboard, to_sort, point_system, give_pts):
    # SORTING
    all_sorted_players_d = []
    if type_scoreboard == 0:  # Type 0 -> in-game type (top 10k)
        all_sorted_players_d = sort_players(to_sort, point_system, give_pts)

    elif type_scoreboard == 1:  # Type 1 -> Shortened version (must have >0 points)
        all_sorted_players_d = sort_players_skip(to_sort, 0)

    elif type_scoreboard == 2:  # Type 2 -> Lengthened version (all)
        all_sorted_players_d = sort_players(to_sort, point_system, give_pts)

    elif type_scoreboard == 3:  # Type 3 -> based on average finish
        all_sorted_players_d = sort_players_finish(to_sort)

    return all_sorted_players_d


def create_play_matches(pool, s_bias, shuffle=False):
    all_matches = []

    player_pool = pool

    if shuffle:
        random.shuffle(player_pool)

    matches_to_create = int(len(player_pool) / 100)

    for i in range(matches_to_create):
        players = []

        for p in range(100):
            players.append(player_pool[0])
            player_pool.remove(player_pool[0])

        progress_bar(i, matches_to_create, "Creating matches:")
        match = Match(players)
        all_matches.append(match)

    avg_style_total = 0
    for play in range(len(all_matches)):
        avg_style = 0
        for i in range(len(all_matches[play].m_player_pool)):
            avg_style += all_matches[play].m_player_pool[i].get_play_style()
        avg_style /= len(all_matches[play].m_player_pool)
        s_bias += 1-avg_style
        progress_bar(play, len(all_matches), "Playing matches:", avg_style)
        play_match(all_matches[play].m_player_pool, s_bias-(play/10))

    return all_matches


def progress_bar(current, total, name, avg_style=None, bar_length=100):
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    if avg_style is None:
        sys.stdout.write("\r{0: <{1}} [{2}]{3}%".format(name, 20, arrow + spaces, (percent * 100).__round__(3)))
    else:
        sys.stdout.write("\r{0: <{1}} [{2}]{3} [{4}]%".format(name, 20, arrow + spaces, (percent * 100).__round__(3), str(avg_style)))
    sys.stdout.flush()
    if current == total:
        sys.stdout.write('\n\n')
