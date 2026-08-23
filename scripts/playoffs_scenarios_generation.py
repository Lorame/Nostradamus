""" 
This code will help generate all of the 128 possible scenarios of the playoffs.
It will for sure contain the ultimate set of the last qualified teams for the 
league phase. When all the matches are over, the only thing left to do will be to 
identify among the 128 scenarios, the one that became true. 

"""
import json
from pathlib import Path
import pandas as pd

playoffs_matches = pd.read_csv('data/reference/ucl_2026_2027_playoff_matches.csv')

dic_playoffs = {}

for index in playoffs_matches['playoff_id']:
    key = index
    temp_match = playoffs_matches[playoffs_matches['playoff_id'] == index]
    dic_playoffs[key] = temp_match[['club_id_team_1','club_id_team_2']].iloc[0].tolist()

print(f"There are {len(dic_playoffs)} matches left in the third round of the playoffs.")

scenarios_list = [format(number,"07b") for number in range(128)]
print(f"Number of possible scenarios : {len(scenarios_list)}. First scenario : {scenarios_list[0]} & last scenarios : {scenarios_list[-1]}.")

potential_qualified_scenarios = {}

for scenario in scenarios_list:
    part_scenario = []
    for i in range(1,len(dic_playoffs)+1):
        if int(scenario[i-1]) == 0:
            part_scenario.append(dic_playoffs[i][0])
        elif int(scenario[i-1]) == 1:
            part_scenario.append(dic_playoffs[i][1])
    potential_qualified_scenarios[scenario] = part_scenario
    

print(f"Number of generated scenarios : {len(potential_qualified_scenarios)}")

""" This following piece of code is there to make sure the logic of the previous code respects 
what should be obtained if we handpicked the winners directly in the playoff dictionnary.


print("Scenario 0000000:")
print(potential_qualified_scenarios["0000000"])

print("Scenario 1111111:")
print(potential_qualified_scenarios["1111111"])

# Check scenario 0000000
expected_0000000 = []

for match_id in dic_playoffs:
    expected_0000000.append(dic_playoffs[match_id][0])

print("0000000 generated:", potential_qualified_scenarios["0000000"])
print("0000000 expected :", expected_0000000)
print("Match:", potential_qualified_scenarios["0000000"] == expected_0000000)


# Check scenario 1111111
expected_1111111 = []

for match_id in dic_playoffs:
    expected_1111111.append(dic_playoffs[match_id][1])

print("1111111 generated:", potential_qualified_scenarios["1111111"])
print("1111111 expected :", expected_1111111)
print("Match:", potential_qualified_scenarios["1111111"] == expected_1111111)
"""

OUTPUT_PATH = Path("data/processed/ucl_2026_2027_playoff_scenarios.json")
OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

scenarios_json = {}

for scenario_id, (binary_result, qualified_clubs) in enumerate(
    potential_qualified_scenarios.items(),
    start=1
):
    scenarios_json[scenario_id] = {
        "binary_result": binary_result,
        "qualified_clubs": qualified_clubs
    }

with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
    json.dump(
        scenarios_json,
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"JSON file created : {OUTPUT_PATH}")