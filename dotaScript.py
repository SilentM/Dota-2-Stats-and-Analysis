import requests
import json
from jsonmerge import Merger

# sources
# https://github.com/joshuaduffy/dota2api/blob/master/dota2api/ref/heroes.json

def runScriptFn():
    r = requests.get("https://api.opendota.com/api/players/107828036/matches")

    with open('sample/output.json', 'w') as out:
        json.dump(r.json(), out, sort_keys=True, indent='\t')

    jsonFile = r.json()

    mapOfHeroKills = {}

    for match in jsonFile:
        hero_id = match["hero_id"]
        hero_kill = match["kills"]
        arrayHeroKill = []
        nameOfHero = ""

        if hero_id in mapOfHeroKills:
            mapOfHeroKills[hero_id] += hero_kill
        else:
            mapOfHeroKills[hero_id] = hero_kill

    with open('heroNameID.json', 'r') as f:
        heroNameID = json.load(f)

    listOfHero = list(heroNameID.values())

    for idValue, kill in mapOfHeroKills.items():
        for heroList in listOfHero:
            for hero in heroList:
                if hero["id"] == idValue:
                    nameOfHero = hero["localized_name"]

                    x = {
                        "id": idValue,
                        "kills": kill,
                        "name": nameOfHero
                    }

                    arrayHeroKill.append(x)

    arrayHeroKill.sort(key=lambda x: x["id"], reverse=False)


    with open('heroes.json', 'r') as f:
        heroImages = json.load(f)

    #
    listOfHeroImages = heroImages["heroes"]

    for arrayHero in arrayHeroKill:
        for heroImage in listOfHeroImages:
            if arrayHero["id"] == heroImage["id"]:
                arrayHero["image"] = heroImage["url_small_portrait"]

    with open('static/data/heroKills.json', 'w') as json_file:

        json.dump(arrayHeroKill, json_file)





runScriptFn()

# constants = requests.get("https://api.opendota.com/api/constants/heroes")
# with open('constants.json', 'w') as out:
#     json.dump(constants.json(), out, sort_keys=True, indent='\t')
#
