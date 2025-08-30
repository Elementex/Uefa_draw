import random
from collections import defaultdict

class UCLTeamDrawSimulator:
    def __init__(self):
        # Pots (9 teams each, Swiss format)
        self.pots = {
            1: [
                ("Manchester City", "ENG"), ("Bayern Munich", "GER"), ("Real Madrid", "ESP"),
                ("PSG", "FRA"), ("Liverpool", "ENG"), ("Inter Milan", "ITA"),
                ("Borussia Dortmund", "GER"), ("RB Leipzig", "GER"), ("Barcelona", "ESP")
            ],
            2: [
                ("Bayer Leverkusen", "GER"), ("Atletico Madrid", "ESP"), ("Atalanta", "ITA"),
                ("Juventus", "ITA"), ("Benfica", "POR"), ("Arsenal", "ENG"),
                ("Club Brugge", "BEL"), ("Shakhtar Donetsk", "UKR"), ("AC Milan", "ITA")
            ],
            3: [
                ("Feyenoord", "NED"), ("Sporting CP", "POR"), ("PSV Eindhoven", "NED"),
                ("Dinamo Zagreb", "CRO"), ("RB Salzburg", "AUT"), ("Lille", "FRA"),
                ("Red Star Belgrade", "SRB"), ("Young Boys", "SUI"), ("Celtic", "SCO")
            ],
            4: [
                ("Slovan Bratislava", "SVK"), ("Monaco", "FRA"), ("Sparta Prague", "CZE"),
                ("Aston Villa", "ENG"), ("Bologna", "ITA"), ("Girona", "ESP"),
                ("VfB Stuttgart", "GER"), ("Sturm Graz", "AUT"), ("Brest", "FRA")
            ]
        }

        # Lookups
        self.all_teams = {}
        for pot_num, teams in self.pots.items():
            for team_name, country in teams:
                self.all_teams[team_name.lower()] = (team_name, country, pot_num)

        # Global fixtures database
        # team_name -> list of (opponent_name, country, pot, home/away)
        self.fixtures = defaultdict(list)

    # ---------- Constraints ----------
    def can_play_against(self, my_team, opponent_team):
        my_name, my_country, my_pot = my_team
        opp_name, opp_country, opp_pot = opponent_team

        # Can't play themselves
        if my_name == opp_name:
            return False
        # No same-country
        if my_country == opp_country:
            return False
        # Already opponents
        if any(opp_name == opp for opp, _, _, _ in self.fixtures[my_name]):
            return False

        return True

    def draw_team_fixtures(self, team_name):
        team_key = team_name.lower().strip()
        if team_key not in self.all_teams:
            print(f"Team '{team_name}' not found.")
            return None

        team_info = self.all_teams[team_key]
        my_name, my_country, my_pot = team_info

        # If already fully drawn
        if len(self.fixtures[my_name]) == 8:
            print(f"\n{my_name} already has all fixtures assigned.")
            return self.fixtures[my_name]

        print(f"\nDrawing fixtures for {my_name} ({my_country}) [Pot {my_pot}]")
        print("=" * 60)

        # Go pot by pot and fill in missing opponents
        for pot in [1, 2, 3, 4]:
            already_from_pot = sum(1 for _, _, p, _ in self.fixtures[my_name] if p == pot)
            needed_from_pot = 2 - already_from_pot
            if needed_from_pot <= 0:
                continue

            # Eligible opponents
            candidates = [
                (opp_name, opp_country, pot)
                for opp_name, opp_country in self.pots[pot]
                if self.can_play_against(team_info, (opp_name, opp_country, pot))
            ]

            if len(candidates) < needed_from_pot:
                print(f"Not enough valid opponents in Pot {pot}. Draw failed.")
                return None

            chosen = random.sample(candidates, needed_from_pot)

            # Assign matches (reciprocal storage)
            for opp_name, opp_country, opp_pot in chosen:
                # Decide home/away (try to balance 4H/4A)
                if sum(1 for _, _, _, h in self.fixtures[my_name] if h == "H") < 4:
                    home = "H"
                else:
                    home = "A"

                # Add to both teams
                self.fixtures[my_name].append((opp_name, opp_country, opp_pot, home))
                self.fixtures[opp_name].append((my_name, my_country, my_pot, "H" if home == "A" else "A"))

        # Print fixtures for this team
        print("\nFixtures:")
        for opp, c, p, h in self.fixtures[my_name]:
            side = "vs" if h == "H" else "@"
            print(f"  {side} {opp} ({c}) [Pot {p}]")

        return self.fixtures[my_name]

    # ---------- UI ----------
    def list_all_teams(self):
        print("\nAVAILABLE TEAMS:")
        print("=" * 50)
        for pot_num in [1, 2, 3, 4]:
            print(f"\nPOT {pot_num}:")
            for team_name, country in self.pots[pot_num]:
                print(f"  - {team_name} ({country})")

    def show_team_fixtures(self, team_name):
        team_key = team_name.lower().strip()
        if team_key not in self.all_teams:
            print(f"Team '{team_name}' not found.")
            return

        my_name, my_country, my_pot = self.all_teams[team_key]

        if not self.fixtures[my_name]:
            print(f"\n{my_name} has no fixtures yet. Run a draw first.")
            return

        print(f"\nFixtures for {my_name} ({my_country}) [Pot {my_pot}]")
        print("=" * 60)
        for opp, c, p, h in self.fixtures[my_name]:
            side = "vs" if h == "H" else "@"
            print(f"  {side} {opp} ({c}) [Pot {p}]")

# ---------- Main Program ----------
def main():
    simulator = UCLTeamDrawSimulator()
    print("UEFA Champions League Team Draw Simulator")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Draw fixtures for a team")
        print("2. List all teams")
        print("3. Show a team’s fixtures")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            team_name = input("\nEnter team name: ").strip()
            if not team_name:
                print("Please enter a team name.")
                continue
            result = simulator.draw_team_fixtures(team_name)
            if result is None:
                print("\nDraw failed or team not found.")
        elif choice == "2":
            simulator.list_all_teams()
        elif choice == "3":
            team_name = input("\nEnter team name: ").strip()
            simulator.show_team_fixtures(team_name)
        elif choice == "4":
            print("\nThanks for using the UCL Draw Simulator!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
