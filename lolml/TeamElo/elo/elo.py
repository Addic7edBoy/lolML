from team import Team

class EloRatingSystem(object):
    """Elo Rating System for a single league"""
    def __init__(self, league, teamfile, K=20):
        self.league_name = league
        self.K = K
        self.teams = {}
        with open(teamfile, 'r') as teams:
            for team in teams:
                team_info = list(map(str.strip, team.split(',')))
                self.teams[team_info[0]] = Team(*team_info)
        self.alignment = [0]
        self.season_boundary = []
        self.brier_scores = []

    def __repr__(self):
        team_table = []
        for _, team in self.teams.items():
            team_table.append((team.rating, "    {:>3}  {}\n".format(team.abbrev, int(team.rating))))
        team_table.sort(key=lambda tup: tup[0], reverse=True)
        table_str = "{} Elo Ratings\n".format(self.league_name)
        for row in team_table:
            table_str += row[1]
        return table_str

    def getTeam(self, team_name):
        return self.teams[team_name]

    def getWinProb(self, team1, team2):
        """
        Get the probability that team1 will beat team2.
        @return win probability between 0 and 1.
        """
        rating_diff = team1.rating - team2.rating
        win_prob = 1 / (10**(-rating_diff/400) + 1)
        return win_prob

    def adjustRating(self, winning_team, losing_team):
        """
        Adjust the model's understanding of two teams based on the outcome of a
        match between the two teams.
        """
        forecast_delta = 1 - self.getWinProb(winning_team, losing_team)
        correction = self.K * forecast_delta
        winning_team.updateRating(correction)
        losing_team.updateRating(-correction)
        brier = forecast_delta**2
        self.brier_scores.append(brier)

    def loadGamesFile(self, gamefile):
        with open(gamefile, 'r') as games:
            for game in games:
                game = game.strip()
                if not game:
                    continue
                if game == "#Align#":
                    self.align()
                    continue
                t1, t1s, t2s, t2 = game.split()
                w_team = self.getTeam(t1 if int(t1s) else t2)
                l_team = self.getTeam(t2 if int(t1s) else t1)
                self.adjustRating(w_team, l_team)

    def align(self):
        max_games = 0
        for _, team in self.teams.items():
            max_games = max(max_games, len(team.rating_history[-1]))
            team.rating_history.append([team.rating])
        alignment = max_games + self.alignment[-1] - 1
        self.alignment.append(alignment)
        return alignment

    def newSeasonReset(self):
        for _, team in self.teams.items():
            new_start = team.rating - (team.rating - 1500)/4
            team.rating = new_start
        season_bound = self.align()
        self.season_boundary.append(season_bound)

    def predict(self, team1, team2):
        win_prob = self.getWinProb(self.getTeam(team1), self.getTeam(team2))
        if win_prob < 0.5:
            team1, team2 = team2, team1
            win_prob = 1 - win_prob
        print("{} {}% over {}".format(team1, int(win_prob*100), team2))

    def printBrier(self):
        print("Brier Score: {:.4f}".format(sum(self.brier_scores)/len(self.brier_scores)))

    def stats(self):
        self.printBrier()
        print(self)


lcs = EloRatingSystem("LCS", "teams.csv", K=30)
print(lcs.teams)
lcs.loadGamesFile('playoffs.games')
lcs.predict('TL', 'C9')
print(lcs.stats)
lcs.printBrier()