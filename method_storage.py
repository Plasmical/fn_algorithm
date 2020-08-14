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

    def get_match_report(self):  # TODO (broken)
        for reports in range(len(self._match_report)):
            if self._match_report.__contains__(self._name):
                print(self._match_report[reports])

    def get_name(self):
        return self._name

    def get_wins(self):
        return self.wins

    def add_win(self):
        self.wins += 1

    def get_skill(self):
        return self._skill

    def get_points(self):
        return self.points

    def add_points(self, amt):
        self.points += amt

    def get_drop_spot(self):
        return self._drop_spot

    def get_play_style(self):
        return self._play_style

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
        self.avg_placement = self.total_placement / self.matches

    def set_points_match(self):
        self.points_match = self.points

    def get_rotation(self):
        return self._rotate


class Match:
    players_alive = 0
    m_player_pool = []

    def __init__(self, m_player):
        self.m_player_pool = m_player
        self.players_alive = len(m_player)

    def simulation(self, s_bias):
        play_match(self.m_player_pool, s_bias)


# METHOD DECLARATION


def play_match(players_in_match, style_bias):
    players_alive = len(players_in_match)

    pool = players_in_match

    while players_alive > 1:
        # Simulate the match
        if not len(pool) == 2:
            for pl in range(len(pool)):
                if pl >= len(pool):
                    break
                nums = []
                for all_p in range(len(pool)):
                    if not all_p == pl:
                        if pool[all_p].get_rotation()/1000 < random.random()/1.02:
                            nums.append(all_p)
                if pool[pl].get_play_style() + style_bias > random.random():
                    p2 = -1
                    if len(nums) > 0:
                        nump = random.randint(0, len(nums) - 1)
                        p2 = nums[nump]
                    if p2 != -1:
                        if (pool[pl].get_skill() + random.random() * 20 + 20) >= (
                                pool[p2].get_skill() + random.random() * 20):
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
    to_give.add_match_report(p_points, to_give.get_kills(), to_give.get_placement_match())
    to_give.set_points_match()
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
                # TODO
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

    return all_sorted_players_d


def create_play_matches(pool, shuffle, s_bias):
    all_matches = []

    player_pool = pool

    matches_to_create = int(len(player_pool) / 100)

    if shuffle:
        random.shuffle(player_pool)

    for i in range(matches_to_create):
        players = []

        for p in range(100):
            players.append(player_pool[0])
            player_pool.remove(player_pool[0])

        progress_bar(i, matches_to_create, "Creating matches:")
        match = Match(players)
        all_matches.append(match)

    for play in range(len(all_matches)):
        progress_bar(play, len(all_matches), "Playing matches:")
        play_match(all_matches[play].m_player_pool, s_bias)

    return all_matches


def progress_bar(current, total, name, bar_length=100):
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r{0: <{1}} [{2}]{3}%".format(name, 20, arrow + spaces, (percent * 100).__round__(3)))
    sys.stdout.flush()
    if current == total:
        sys.stdout.write('\n\n')
