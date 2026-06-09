# AI+X 딥러닝 기말 프로젝트
배경준 2026026026 elsovlse@hanyang.ac.kr

이환 2026077947 lhweane@hanyang.ac.kr

이승현 2026030200 shlxk115@hanyang.ac.kr

# Motivation
소포모어 징크스 현상을 데이터 기반으로 검증하고, 딥러닝 알고리즘을 통해 개인의 이전 성과가 이후 성과에 미치는 영향을 분석하여 성과 하락을 예측할 수 있는 모델을 구축하고자 이 프로젝트를 진행한다.

# Datasets
루키와 소포모어 시즌의 타석 수가 너무 적지 않은 1950년~2011년 데뷔 선수 200명을 데이터로 삼았다. (1)은 첫 학습에서 사용된 데이터셋으로, 데이터의 양이 선수 200명 남짓으로 적다. (2)는 (1)의 문제를 보완한 데이터셋으로, 선수를 1000명으로 늘렸다.

깃헙의 Lahman baseball database에서 데이터셋을 구한 과정은 다음과 같다.

1. Lahman baseball database에 접근
```{python}
import requests

headers = {'User-Agent': 'Mozilla/5.0'}

urls = [
    "https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Batting.csv",
    "https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/People.csv",
]
for url in urls:
    r = requests.get(url, headers=headers, timeout=15)
    print(url.split('/')[-1], r.status_code, len(r.text))
    if r.status_code == 200:
        print(r.text[:300])
        print("---")
```
```{python}
import requests
headers = {'User-Agent': 'Mozilla/5.0'}

urls = [
    "https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv",
    "https://raw.githubusercontent.com/dstorey/baseball/master/data/Batting.csv",
]
for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(r.status_code, url.split('github.com/')[-1][:60])
        if r.status_code == 200:
            print(r.text[:200])
    except Exception as e:
        print("ERR", e)
```
```{python}
import requests

headers = {'User-Agent': 'Mozilla/5.0'}

urls = [
    "https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv",
    "https://raw.githubusercontent.com/dstorey/baseball/master/data/Batting.csv",
]
for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(r.status_code, url.split('github.com/')[-1][:60])
        if r.status_code == 200:
            print(r.text[:200])
    except Exception as e:
        print("ERR", e)
```
2. 데이터 추출 및 저장 시도
```{python}
import requests
headers = {'User-Agent': 'Mozilla/5.0'}

batting_url = "https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv"
people_url = "https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Master.csv"

r1 = requests.get(batting_url, headers=headers, timeout=30)
r2 = requests.get(people_url, headers=headers, timeout=30)
print("Batting:", r1.status_code, len(r1.text))
print("People:", r2.status_code, len(r2.text))
print("\nPeople cols:", r2.text.split('\n')[0] if r2.status_code==200 else "N/A")
```
```{python}
import requests
headers = {'User-Agent': 'Mozilla/5.0'}

for name in ['People.csv', 'Master.csv', 'player.csv', 'players.csv']:
    url = f"https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/{name}"
    r = requests.get(url, headers=headers, timeout=10)
    print(name, r.status_code)
    if r.status_code == 200:
        print(r.text[:200])
        break
```
```{python}
import requests
headers = {'User-Agent': 'Mozilla/5.0'}

repos = [
    "https://raw.githubusercontent.com/brianhoch/baseballstats/master/",
    "https://raw.githubusercontent.com/johnmyleswhite/ML_for_Hackers/master/02-Exploration/data/baseball/",
]
for base in repos:
    for f in ['Batting.csv', 'Master.csv', 'People.csv', 'batting.csv']:
        r = requests.get(base+f, headers=headers, timeout=8)
        if r.status_code == 200:
            print("FOUND:", base+f)
            print(r.text[:200])
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

batting_url = "https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv"
r = requests.get(batting_url, headers=headers, timeout=30)
df = pd.read_csv(io.StringIO(r.text))
print(df.shape)
print(df.columns.tolist())
print(df.head(3))
print("\nYear range:", df['yearID'].min(), "-", df['yearID'].max())
print("Unique players:", df['playerID'].nunique())
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

urls_to_try = [
    "https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/refs/heads/master/core/Batting.csv",
    "https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Batting.csv",
]

more_urls = [
    "https://raw.githubusercontent.com/null2/lahman-sqlite/master/data/Batting.csv",
    "https://raw.githubusercontent.com/WebucatorTraining/lahman-baseball-mysql/master/Batting.csv",
    "https://raw.githubusercontent.com/jknecht/baseball-archive-sqlite/master/Batting.csv",
]

for url in urls_to_try + more_urls:
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code == 200:
        df = pd.read_csv(io.StringIO(r.text))
        print(f"FOUND: {url}")
        print(f"Years: {df['yearID'].min()}-{df['yearID'].max()}, rows: {len(df)}")
        break
    else:
        print(r.status_code, url.split('github.com/')[-1][:70])
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

people_urls = [
    "https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Salaries.csv",
]
r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/", headers=headers, timeout=10)
print(r.status_code, r.text[:1000])
```
위에서 오류 발생, 2011년보다 최근 데이터는 구할 수 없게 되었음
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

for name in ['Master.csv', 'People.csv', 'player.csv', 'playerInfo.csv', 'bio.csv',
             'pitching.csv', 'Pitching.csv', 'Teams.csv', 'HallOfFame.csv', 'AwardsPlayers.csv']:
    url = f"https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/{name}"
    r = requests.get(url, headers=headers, timeout=8)
    if r.status_code == 200:
        print(f"FOUND: {name}")
        print(r.text[:300])
        print("---")
```
위에서도 오류가 발생해 아직 선수 ID에 실명을 부여하지 못했음.

3. 선수 ID를 통한 루키 시즌 스텟 구하기
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
df = pd.read_csv(io.StringIO(r.text))

yearly = df.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()

rookie_years = yearly.groupby('playerID')['yearID'].min().reset_index()
rookie_years.columns = ['playerID', 'rookieYear']

rookie_stats = yearly.merge(rookie_years, on='playerID')
rookie_stats = rookie_stats[rookie_stats['yearID'] == rookie_stats['rookieYear']]

rookie_stats = rookie_stats[
    (rookie_stats['AB'] >= 130) &
    (rookie_stats['yearID'] >= 1950)
].copy()

print(f"Qualified rookies: {len(rookie_stats)}")
print(rookie_stats.head(3))
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
df = pd.read_csv(io.StringIO(r.text))

yearly = df.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()

rookie_years = yearly.groupby('playerID')['yearID'].min().reset_index()
rookie_years.columns = ['playerID', 'rookieYear']

rookie_stats = yearly.merge(rookie_years, on='playerID')
rookie_stats = rookie_stats[rookie_stats['yearID'] == rookie_stats['rookieYear']].copy()

rookie_stats = rookie_stats[
    (rookie_stats['AB'] >= 130) &
    (rookie_stats['yearID'] >= 1950)
].copy()

rookie_stats['AVG'] = (rookie_stats['H'] / rookie_stats['AB']).round(3)
rookie_stats['OBP'] = ((rookie_stats['H'] + rookie_stats['BB'] + rookie_stats['HBP']) /
                       (rookie_stats['AB'] + rookie_stats['BB'] + rookie_stats['HBP'] + rookie_stats['SF'])).round(3)
rookie_stats['SLG'] = ((rookie_stats['H'] + rookie_stats['2B'] + 2*rookie_stats['3B'] + 3*rookie_stats['HR']) /
                       rookie_stats['AB']).round(3)
rookie_stats['OPS'] = (rookie_stats['OBP'] + rookie_stats['SLG']).round(3)

top200 = rookie_stats.sort_values('OPS', ascending=False).head(200).copy()

final = top200[['playerID', 'yearID', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI',
                'SB', 'CS', 'BB', 'SO', 'HBP', 'AVG', 'OBP', 'SLG', 'OPS']].copy()
final.columns = ['Player_ID', 'Rookie_Year', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI',
                 'SB', 'CS', 'BB', 'SO', 'HBP', 'AVG', 'OBP', 'SLG', 'OPS']
final = final.sort_values(['Rookie_Year', 'OPS'], ascending=[True, False]).reset_index(drop=True)

print(final.shape)
print(final.head(5))

final.to_csv('/tmp/rookies_no_names.csv', index=False)
print("saved")
```
4. 선수 ID에 실명 부여
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

rookies = pd.read_csv('/tmp/rookies_no_names.csv')
player_ids = rookies['Player_ID'].tolist()

def parse_player_id(pid):
    """Parse Lahman playerID to approximate name."""
    # Format: [last5][first2][seq2]
    if len(pid) < 8:
        return pid
    last_part = pid[:5].strip('0123456789')
    first_part = pid[5:7]
    # Capitalize
    last = last_part.capitalize()
    first = first_part.capitalize() + '.'
    return f"{first} {last}"

known_names = {
    'aaronha01': 'Hank Aaron',
    'mantlmi01': 'Mickey Mantle',
    'maystw01': 'Willie Mays',
    'robinju01': 'Jackie Robinson',
    'benchjo01': 'Johnny Bench',
    'carewro01': 'Rod Carew',
    'brocklo01': 'Lou Brock',
    'mccovwi01': 'Willie McCovey',
    'yastrca01': 'Carl Yastrzemski',
    'stargwi01': 'Willie Stargell',
    'brettge01': 'George Brett',
    'schmimi01': 'Mike Schmidt',
    'guidrro01': 'Ron Guidry',
    'jacksr01': 'Reggie Jackson',
    'morgajo02': 'Joe Morgan',
    'rosepe01': 'Pete Rose',
    'bankser01': 'Ernie Banks',
    'clemero01': 'Roberto Clemente',
    'gibsobo01': 'Bob Gibson',
    'koufasa01': 'Sandy Koufax',
    'musiast01': 'Stan Musial',
    'fiskca01': 'Carlton Fisk',
    'lynnfr01': 'Fred Lynn',
    'riceji01': 'Jim Rice',
    'murphda05': 'Dale Murphy',
    'guerrpe01': 'Pedro Guerrero',
    'henderi01': 'Rickey Henderson',
    'whitedf01': 'Devon White',
    'bondsba01': 'Barry Bonds',
    'mcgwima01': 'Mark McGwire',
    'sosasd01': 'Sammy Sosa',
    'ripkeca01': 'Cal Ripken Jr.',
    'gonzaju03': 'Juan Gonzalez',
    'grissma01': 'Marquis Grissom',
    'piazzmi01': 'Mike Piazza',
    'thomafr04': 'Frank Thomas',
    'griffke02': 'Ken Griffey Jr.',
    'bagweje01': 'Jeff Bagwell',
    'biggiocr01': 'Craig Biggio',
    'molinya01': 'Yadier Molina',
    'jeterde01': 'Derek Jeter',
    'rodrial01': 'Alex Rodriguez',
    'pujolal01': 'Albert Pujols',
    'ordonma01': 'Magglio Ordonez',
    'suzukic01': 'Ichiro Suzuki',
    'beltrad01': 'Adrian Beltre',
    'longevi01': 'Evan Longoria',
    'braunry02': 'Ryan Braun',
    'hamiljo03': 'Josh Hamilton',
    'uptonbu01': 'B.J. Upton',
    'fieldpr01': 'Prince Fielder',
    'cabremi01': 'Miguel Cabrera',
    'ramirha01': 'Hanley Ramirez',
    'tulowtr01': 'Troy Tulowitzki',
    'youngde03': 'Delmon Young',
    'willibe02': 'Bernie Williams',
    'gonzaal02': 'Adrian Gonzalez',
    'liriama01': 'Mark Liriano',
    'hollidm01': 'Matt Holliday',
    'iguchia01': 'Tadahito Iguchi',
    'choosh01': 'Shin-Soo Choo',
    'abreubo01': 'Bobby Abreu',
    'guerrvi01': 'Vladimir Guerrero',
    'rentermi01': 'Mike Renter',
    'dunnad01': 'Adam Dunn',
    'ortizda01': 'David Ortiz',
    'walketo04': 'Todd Walker',
    'sosasa01': 'Sammy Sosa',
    'jethrsa01': 'Sam Jethroe',
    'mcdougi01': 'Gil McDougald',
    'norenir01': 'Irv Noren',
    'lenhado01': 'Don Lenhardt',
    'bellgu01': 'Gus Bell',
    'avila01': 'Bobby Avila',
}

rookies['Player_Name'] = rookies['Player_ID'].apply(
    lambda x: known_names.get(x, parse_player_id(x))
)

print(rookies[['Player_ID', 'Player_Name', 'Rookie_Year']].head(15))
print("\nKnown names matched:", sum(rookies['Player_ID'].isin(known_names)))
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

rookies = pd.read_csv('/tmp/rookies_no_names.csv')

def lahman_id_to_name(pid):
    pid_clean = pid[:-2]
    last5 = pid_clean[:5].rstrip()
    first2 = pid_clean[5:]
    last = last5.capitalize()
    first = first2.upper() + '.'
    return f"{first} {last}"

r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
batting = pd.read_csv(io.StringIO(r.text))

print("Sample playerIDs:", batting['playerID'].unique()[:20].tolist())

def id_to_display(pid):
    core = pid[:-2]
    last_raw = core[:5].rstrip('abcdefghijklmnopqrstuvwxyz'[:0])
    last_part = core[:-2] if len(core) > 2 else core
    first_part = core[-2:] if len(core) >= 2 else ''
    return f"{first_part.capitalize()}. {last_part.capitalize()}"

for pid in rookies['Player_ID'].head(20):
    print(f"{pid} -> {id_to_display(pid)}")
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

first_name_map = {
    'ha': 'Hank', 'wi': 'Willie', 'mi': 'Mickey', 'jo': 'Joe', 'bo': 'Bob',
    'ro': 'Ron', 'ji': 'Jim', 'bi': 'Bill', 'to': 'Tom', 'fr': 'Frank',
    'do': 'Don', 'ri': 'Rich', 'da': 'Dave', 'ed': 'Ed', 'ge': 'George',
    'ch': 'Chris', 'ma': 'Mark', 'st': 'Steve', 'ke': 'Ken', 'la': 'Larry',
    'di': 'Dick', 'al': 'Al', 'ra': 'Randy', 'ga': 'Gary', 'te': 'Terry',
    'wa': 'Walt', 'el': 'Elston', 'sa': 'Sam', 'ir': 'Irv', 'gu': 'Gus',
    'gi': 'Gil', 'du': 'Duke', 'ca': 'Cal', 'le': 'Lee', 'pe': 'Pete',
    'ba': 'Barry', 'ru': 'Rusty', 'ja': 'Jason', 'ty': 'Ty', 'lo': 'Lou',
    'de': 'Derek', 'ad': 'Adam', 'an': 'Andy', 'gr': 'Greg', 'br': 'Brad',
    'sc': 'Scott', 'pa': 'Pat', 'ic': 'Ichiro', 'vi': 'Vlad', 'be': 'Ben',
    'no': 'Nomar', 'sh': 'Shin-Soo', 'cr': 'Craig', 'mi': 'Mike', 'je': 'Jeff',
    'ti': 'Tim', 'li': 'Livan', 'mo': 'Moisés', 'rh': 'Rheal',
}

def decode_lahman_id(pid):
    seq = pid[-2:]
    core = pid[:-2]
    first_abbr = core[-2:].lower()
    last_raw = core[:-2].lower()
    
    last = last_raw.capitalize()
    first = first_name_map.get(first_abbr, first_abbr.capitalize() + '.')
    return f"{first} {last}"

samples = ['aaronha01', 'mantlmi01', 'mayswi01', 'jethrsa01', 'mcdougi01',
           'lenhado01', 'norenir01', 'henderi01', 'bondsba01', 'griffke02',
           'rodrial01', 'pujolal01', 'suzukic01', 'beltrad01', 'cabremi01']
for pid in samples:
    print(f"{pid} -> {decode_lahman_id(pid)}")
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

rookies = pd.read_csv('/tmp/rookies_no_names.csv')
pids = rookies['Player_ID'].tolist()
print("Player IDs to look up:")
for i, pid in enumerate(pids):
    print(f"  {pid}")
```
```{python}
player_names = {
    'lenhado01': 'Don Lenhardt', 'norenir01': 'Irv Noren', 'jethrsa01': 'Sam Jethroe',
    'bellgu01': 'Gus Bell', 'mcdougi01': 'Gil McDougald', 'mayswi01': 'Willie Mays',
    'mantlmi01': 'Mickey Mantle', 'rhodedu01': 'Dusty Rhodes', 'gernedi01': 'Dick Gernert',
    'gilliji01': 'Jim Gilliam', 'pendlji01': 'Jim Pendleton', 'skowrbi01': 'Bill Skowron',
    'cunnijo01': 'Joe Cunningham', 'moonwa01': 'Wally Moon', 'finigji01': 'Jim Finigan',
    'aaronha01': 'Hank Aaron', 'howarel01': 'Elston Howard', 'halebo01': 'Bob Hale',
    'robinfr02': 'Frank Robinson', 'skizalo01': 'Lou Skizas', 'brandja01': 'Jackie Brandt',
    'whitebi03': 'Bill White', 'anderha02': 'Harry Anderson', 'wagnele01': 'Leon Wagner',
    'cepedor01': 'Orlando Cepeda', 'stuardi01': 'Dick Stuart', 'graydi01': 'Dick Gray',
    'kirklwi01': 'Willie Kirkland', 'larkeno01': 'Norm Larker', 'mccovwi01': 'Willie McCovey',
    'snyderu01': 'Russ Snyder', 'baxesji01': 'Jim Baxes', 'mayele01': 'Lee Maye',
    'thomale03': 'Lee Thomas', 'charled01': 'Ed Charles', 'lockdo01': 'Don Lock',
    'jimenma01': 'Manny Jiminez', 'whitffr01': 'Fred Whitfield', 'hallji02': 'Jim Hall',
    'deesch01': 'Charlie Dees', 'conigto01': 'Tony Conigliaro', 'blefacu01': 'Curt Blefary',
    'foyjo01': 'Joe Foy', 'raderdo02': 'Don Rader', 'fostero01': 'Roy Foster',
    'cedence01': 'Cesar Cedeno', 'stennre01': 'Rennie Stennett', 'hargrmi01': 'Mike Hargrove',
    'pagemi02': 'Mitchell Page', 'hendest01': 'Steve Henderson', 'murraed02': 'Eddie Murray',
    'puhlte01': 'Terry Puhl', 'willsbu01': 'Bump Wills', 'hornebo01': 'Bob Horner',
    'charbjo01': 'Joe Charboneau', 'salazlu01': 'Luis Salazar', 'staplda01': 'Dave Stapleton',
    'boggswa01': 'Wade Boggs', 'johnsho01': 'Howard Johnson', 'wilsogl01': 'Glenn Wilson',
    'strawda01': 'Darryl Strawberry', 'esaskni01': 'Nick Esasky', 'vanslan01': 'Andy Van Slyke',
    'davisal01': 'Alvin Davis', 'daviser01': 'Eric Davis', 'pendlte01': 'Terry Pendleton',
    'danieka01': 'Kal Daniels', 'krukjo01': 'John Kruk', 'joynewa01': 'Wally Joyner',
    'snydeco02': 'Cory Snyder', 'clarkwi02': 'Will Clark', 'incavpe01': 'Pete Incaviglia',
    'sierrru01': 'Ruben Sierra', 'hornsa01': 'Sam Horn', 'lindjo01': 'Jose Lind',
    'benzito01': 'Todd Benzinger', 'surhobj01': 'B.J. Surhoff', 'jordari02': 'Ricky Jordan',
    'gracema01': 'Mark Grace', 'smithdw01': 'Dwight Smith', 'thomafr04': 'Frank Thomas',
    'maaske01': 'Kevin Maas', 'frymatr01': 'Travis Fryman', 'barbebr01': 'Bret Barberie',
    'newsowa01': 'Warren Newson', 'bagweje01': 'Jeff Bagwell', 'martich01': 'Chuck Martinez',
    'valenjo02': 'Jose Valentin', 'stockke01': 'Kevin Stocker', 'burnije01': 'Jeremy Burnitz',
    'greerru01': 'Rusty Greer', 'moutoly01': 'Lyle Mouton', 'cordoma01': 'Manny Cordova',
    'nunnajo01': 'Jon Nunnally', 'timmooz01': 'Ozzie Timmons', 'batesja01': 'Jason Bates',
    'houstty01': 'Tyler Houston', 'muellbi02': 'Bill Mueller', 'osikke01': 'Keith Osik',
    'batisto01': 'Tony Batista', 'kendaja01': 'Jason Kendall', 'cruzjo02': 'Jose Cruz Jr.',
    'orieke01': 'Kevin Orie', 'bergda01': 'Dave Berg', 'leetr01': 'Travis Lee',
    'durazer01': 'Erubiel Durazo', 'blumge01': 'Geoff Blum', 'singlch01': 'Chris Singleton',
    'jonesja04': 'Jacque Jones', 'morriwa02': 'Warren Morris', 'leeca01': 'Carlos Lee',
    'piattad01': 'Adam Piatt', 'richach01': 'Chris Richard', 'tracyan01': 'Andy Tracy',
    'burrepa01': 'Pat Burrell', 'lugoju01': 'Julio Lugo', 'furcara01': 'Rafael Furcal',
    'trubych01': 'Chris Truby', 'pujolal01': 'Albert Pujols', 'wilsocr03': 'Craig Wilson',
    'dunnad01': 'Adam Dunn', 'uribeju01': 'Juan Uribe', 'suzukic01': 'Ichiro Suzuki',
    'gibboja01': 'Jay Gibbons', 'spiveju01': 'Junior Spivey', 'gilesma01': 'Marcus Giles',
    'kearnau01': 'Austin Kearns', 'hinsker01': 'Eric Hinske', 'menchke01': 'Kevin Mench',
    'gerutjo01': 'Joey Gerut', 'hammoro01': 'Robby Hammock', 'teixema01': 'Mark Teixeira',
    'cabremi01': 'Miguel Cabrera', 'matsuhi01': 'Hideki Matsui', 'johnsre02': 'Reed Johnson',
    'wrighda03': 'David Wright', 'hollima01': 'Matt Holliday', 'jacobbu02': 'Buck Jacobsen',
    'larocad01': 'Adam LaRoche', 'thomach01': 'Charles Thomas', 'cantujo01': 'Jorge Cantu',
    'gonzalu02': 'Luis Gonzalez', 'sledgte01': 'Terrmel Sledge', 'youklke01': 'Kevin Youkilis',
    'murtoma01': 'Matt Murton', 'francje02': 'Jeff Francoeur', 'rodrijo03': 'John Rodriguez',
    'johnsda06': 'Dan Johnson', 'iguchta01': 'Tadahito Iguchi', 'canoro01': 'Robinson Cano',
    'costech01': 'Chris Costello', 'drewst01': 'Stephen Drew', 'quentca01': 'Carlos Quentin',
    'ethiean01': 'Andre Ethier', 'ugglada01': 'Dan Uggla', 'napolmi01': 'Mike Napoli',
    'kinslia01': 'Ian Kinsler', 'markani01': 'Nick Markakis', 'martiru01': 'Russell Martin',
    'johjike01': 'Kenji Johjima', 'braunry02': 'Ryan Braun', 'hamiljo03': 'Josh Hamilton',
    'pencehu01': 'Hunter Pence', 'bucktr01': 'Travis Buck', 'reynoma01': 'Mark Reynolds',
    'escobyu01': 'Yunel Escobar', 'butlebi03': 'Billy Butler', 'cabreas01': 'Asdrubal Cabrera',
    'iwamuak01': 'Akinori Iwamura', 'davisch02': 'Chris Davis', 'longoev01': 'Evan Longoria',
    'murphda08': 'David Murphy', 'sandopa01': 'Pablo Sandoval', 'bakerjo01': 'John Baker',
    'avilemi01': 'Mike Aviles', 'joycema01': 'Matt Joyce', 'spande01': 'Denard Span',
    'ramiral03': 'Alexei Ramirez', 'mathejo02': 'Joe Mather', 'blankky01': 'Kyle Blanks',
    'coghlch01': 'Chris Coghlan', 'mccutan01': 'Andrew McCutchen', 'reimono01': 'Nolan Reimold',
    'beckhgo01': 'Gordon Beckham', 'borboju01': 'Julio Borbon', 'santaca01': 'Carlos Santana',
    'heywaja01': 'Jason Heyward', 'morrilo01': 'Logan Morrison', 'morelmi01': 'Mitch Moreland',
    'stantmi03': 'Mike Stanton', 'valenda01': 'Danny Valencia', 'davisik02': 'Ike Davis',
    'alvarpe01': 'Pedro Alvarez', 'jayjo02': 'Jon Jay', 'lawribr01': 'Brett Lawrie',
    'kipnija01': 'Jason Kipnis', 'perezsa02': 'Salvador Perez', 'goldspa01': 'Paul Goldschmidt',
    'hosmeer01': 'Eric Hosmer', 'thameer01': 'Eric Thames',
}

print(f"Total lookups: {len(player_names)}")
import pandas as pd
rookies = pd.read_csv('/tmp/rookies_no_names.csv')
print(f"Total rookies: {len(rookies)}")

missing = [pid for pid in rookies['Player_ID'] if pid not in player_names]
print(f"Missing: {len(missing)}")
for pid in missing:
    print(f"  {pid}")
```
5. csv 파일로 저장
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
df = pd.read_csv(io.StringIO(r.text))

yearly = df.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()

rookie_years = yearly.groupby('playerID')['yearID'].min().reset_index()
rookie_years.columns = ['playerID', 'rookieYear']

rookie_stats = yearly.merge(rookie_years, on='playerID')
rookie_stats = rookie_stats[rookie_stats['yearID'] == rookie_stats['rookieYear']].copy()

rookie_stats = rookie_stats[
    (rookie_stats['AB'] >= 130) &
    (rookie_stats['yearID'] >= 1950)
].copy()

rookie_stats['AVG'] = (rookie_stats['H'] / rookie_stats['AB']).round(3)
rookie_stats['OBP'] = ((rookie_stats['H'] + rookie_stats['BB'] + rookie_stats['HBP']) /
    (rookie_stats['AB'] + rookie_stats['BB'] + rookie_stats['HBP'] + rookie_stats['SF'])).round(3)
rookie_stats['SLG'] = ((rookie_stats['H'] + rookie_stats['2B'] + 2*rookie_stats['3B'] + 3*rookie_stats['HR']) /
    rookie_stats['AB']).round(3)
rookie_stats['OPS'] = (rookie_stats['OBP'] + rookie_stats['SLG']).round(3)

top200 = rookie_stats.sort_values('OPS', ascending=False).head(200).copy()
top200 = top200.sort_values(['yearID', 'OPS'], ascending=[True, False]).reset_index(drop=True)

player_names = {
    'lenhado01': 'Don Lenhardt', 'norenir01': 'Irv Noren', 'jethrsa01': 'Sam Jethroe',
    'bellgu01': 'Gus Bell', 'mcdougi01': 'Gil McDougald', 'mayswi01': 'Willie Mays',
    'mantlmi01': 'Mickey Mantle', 'rhodedu01': 'Dusty Rhodes', 'gernedi01': 'Dick Gernert',
    'gilliji01': 'Jim Gilliam', 'pendlji01': 'Jim Pendleton', 'skowrbi01': 'Bill Skowron',
    'cunnijo01': 'Joe Cunningham', 'moonwa01': 'Wally Moon', 'finigji01': 'Jim Finigan',
    'aaronha01': 'Hank Aaron', 'howarel01': 'Elston Howard', 'halebo01': 'Bob Hale',
    'robinfr02': 'Frank Robinson', 'skizalo01': 'Lou Skizas', 'brandja01': 'Jackie Brandt',
    'whitebi03': 'Bill White', 'anderha02': 'Harry Anderson', 'wagnele01': 'Leon Wagner',
    'cepedor01': 'Orlando Cepeda', 'stuardi01': 'Dick Stuart', 'graydi01': 'Dick Gray',
    'kirklwi01': 'Willie Kirkland', 'larkeno01': 'Norm Larker', 'mccovwi01': 'Willie McCovey',
    'snyderu01': 'Russ Snyder', 'baxesji01': 'Jim Baxes', 'mayele01': 'Lee Maye',
    'thomale03': 'Lee Thomas', 'charled01': 'Ed Charles', 'lockdo01': 'Don Lock',
    'jimenma01': 'Manny Jiminez', 'whitffr01': 'Fred Whitfield', 'hallji02': 'Jim Hall',
    'deesch01': 'Charlie Dees', 'conigto01': 'Tony Conigliaro', 'blefacu01': 'Curt Blefary',
    'foyjo01': 'Joe Foy', 'raderdo02': 'Don Rader', 'fostero01': 'Roy Foster',
    'cedence01': 'Cesar Cedeno', 'stennre01': 'Rennie Stennett', 'hargrmi01': 'Mike Hargrove',
    'pagemi02': 'Mitchell Page', 'hendest01': 'Steve Henderson', 'murraed02': 'Eddie Murray',
    'puhlte01': 'Terry Puhl', 'willsbu01': 'Bump Wills', 'hornebo01': 'Bob Horner',
    'charbjo01': 'Joe Charboneau', 'salazlu01': 'Luis Salazar', 'staplda01': 'Dave Stapleton',
    'boggswa01': 'Wade Boggs', 'johnsho01': 'Howard Johnson', 'wilsogl01': 'Glenn Wilson',
    'strawda01': 'Darryl Strawberry', 'esaskni01': 'Nick Esasky', 'vanslan01': 'Andy Van Slyke',
    'davisal01': 'Alvin Davis', 'daviser01': 'Eric Davis', 'pendlte01': 'Terry Pendleton',
    'danieka01': 'Kal Daniels', 'krukjo01': 'John Kruk', 'joynewa01': 'Wally Joyner',
    'snydeco02': 'Cory Snyder', 'clarkwi02': 'Will Clark', 'incavpe01': 'Pete Incaviglia',
    'sierrru01': 'Ruben Sierra', 'hornsa01': 'Sam Horn', 'lindjo01': 'Jose Lind',
    'benzito01': 'Todd Benzinger', 'surhobj01': 'B.J. Surhoff', 'jordari02': 'Ricky Jordan',
    'gracema01': 'Mark Grace', 'smithdw01': 'Dwight Smith', 'thomafr04': 'Frank Thomas',
    'maaske01': 'Kevin Maas', 'frymatr01': 'Travis Fryman', 'barbebr01': 'Bret Barberie',
    'newsowa01': 'Warren Newson', 'bagweje01': 'Jeff Bagwell', 'martich01': 'Chuck Martinez',
    'valenjo02': 'Jose Valentin', 'stockke01': 'Kevin Stocker', 'burnije01': 'Jeremy Burnitz',
    'greerru01': 'Rusty Greer', 'moutoly01': 'Lyle Mouton', 'cordoma01': 'Manny Cordova',
    'nunnajo01': 'Jon Nunnally', 'timmooz01': 'Ozzie Timmons', 'batesja01': 'Jason Bates',
    'houstty01': 'Tyler Houston', 'muellbi02': 'Bill Mueller', 'osikke01': 'Keith Osik',
    'batisto01': 'Tony Batista', 'kendaja01': 'Jason Kendall', 'cruzjo02': 'Jose Cruz Jr.',
    'orieke01': 'Kevin Orie', 'bergda01': 'Dave Berg', 'leetr01': 'Travis Lee',
    'durazer01': 'Erubiel Durazo', 'blumge01': 'Geoff Blum', 'singlch01': 'Chris Singleton',
    'jonesja04': 'Jacque Jones', 'morriwa02': 'Warren Morris', 'leeca01': 'Carlos Lee',
    'piattad01': 'Adam Piatt', 'richach01': 'Chris Richard', 'tracyan01': 'Andy Tracy',
    'burrepa01': 'Pat Burrell', 'lugoju01': 'Julio Lugo', 'furcara01': 'Rafael Furcal',
    'trubych01': 'Chris Truby', 'pujolal01': 'Albert Pujols', 'wilsocr03': 'Craig Wilson',
    'dunnad01': 'Adam Dunn', 'uribeju01': 'Juan Uribe', 'suzukic01': 'Ichiro Suzuki',
    'gibboja01': 'Jay Gibbons', 'spiveju01': 'Junior Spivey', 'gilesma01': 'Marcus Giles',
    'kearnau01': 'Austin Kearns', 'hinsker01': 'Eric Hinske', 'menchke01': 'Kevin Mench',
    'gerutjo01': 'Joey Gerut', 'hammoro01': 'Robby Hammock', 'teixema01': 'Mark Teixeira',
    'cabremi01': 'Miguel Cabrera', 'matsuhi01': 'Hideki Matsui', 'johnsre02': 'Reed Johnson',
    'wrighda03': 'David Wright', 'hollima01': 'Matt Holliday', 'jacobbu02': 'Buck Jacobsen',
    'larocad01': 'Adam LaRoche', 'thomach01': 'Charles Thomas', 'cantujo01': 'Jorge Cantu',
    'gonzalu02': 'Luis Gonzalez', 'sledgte01': 'Terrmel Sledge', 'youklke01': 'Kevin Youkilis',
    'murtoma01': 'Matt Murton', 'francje02': 'Jeff Francoeur', 'rodrijo03': 'John Rodriguez',
    'johnsda06': 'Dan Johnson', 'iguchta01': 'Tadahito Iguchi', 'canoro01': 'Robinson Cano',
    'costech01': 'Chris Costello', 'drewst01': 'Stephen Drew', 'quentca01': 'Carlos Quentin',
    'ethiean01': 'Andre Ethier', 'ugglada01': 'Dan Uggla', 'napolmi01': 'Mike Napoli',
    'kinslia01': 'Ian Kinsler', 'markani01': 'Nick Markakis', 'martiru01': 'Russell Martin',
    'johjike01': 'Kenji Johjima', 'braunry02': 'Ryan Braun', 'hamiljo03': 'Josh Hamilton',
    'pencehu01': 'Hunter Pence', 'bucktr01': 'Travis Buck', 'reynoma01': 'Mark Reynolds',
    'escobyu01': 'Yunel Escobar', 'butlebi03': 'Billy Butler', 'cabreas01': 'Asdrubal Cabrera',
    'iwamuak01': 'Akinori Iwamura', 'davisch02': 'Chris Davis', 'longoev01': 'Evan Longoria',
    'murphda08': 'David Murphy', 'sandopa01': 'Pablo Sandoval', 'bakerjo01': 'John Baker',
    'avilemi01': 'Mike Aviles', 'joycema01': 'Matt Joyce', 'spande01': 'Denard Span',
    'ramiral03': 'Alexei Ramirez', 'mathejo02': 'Joe Mather', 'blankky01': 'Kyle Blanks',
    'coghlch01': 'Chris Coghlan', 'mccutan01': 'Andrew McCutchen', 'reimono01': 'Nolan Reimold',
    'beckhgo01': 'Gordon Beckham', 'borboju01': 'Julio Borbon', 'santaca01': 'Carlos Santana',
    'heywaja01': 'Jason Heyward', 'morrilo01': 'Logan Morrison', 'morelmi01': 'Mitch Moreland',
    'stantmi03': 'Mike Stanton', 'valenda01': 'Danny Valencia', 'davisik02': 'Ike Davis',
    'alvarpe01': 'Pedro Alvarez', 'jayjo02': 'Jon Jay', 'lawribr01': 'Brett Lawrie',
    'kipnija01': 'Jason Kipnis', 'perezsa02': 'Salvador Perez', 'goldspa01': 'Paul Goldschmidt',
    'hosmeer01': 'Eric Hosmer', 'thameer01': 'Eric Thames',
}

top200['Player_Name'] = top200['playerID'].map(player_names)

final = top200[[
    'playerID', 'Player_Name', 'yearID', 'G', 'AB', 'R', 'H',
    '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'HBP',
    'AVG', 'OBP', 'SLG', 'OPS'
]].copy()

final.columns = [
    'Player_ID', 'Player_Name', 'Rookie_Year', 'G', 'AB', 'R', 'H',
    '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'HBP',
    'AVG', 'OBP', 'SLG', 'OPS'
]

int_cols = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'HBP']
for col in int_cols:
    final[col] = final[col].fillna(0).astype(int)

final = final.reset_index(drop=True)
final.index += 1

print(f"Final shape: {final.shape}")
print(f"\nFirst 10 rows:")
print(final[['Player_Name', 'Rookie_Year', 'G', 'AB', 'HR', 'RBI', 'AVG', 'OBP', 'SLG', 'OPS']].head(10).to_string())
print(f"\nTop 10 by OPS:")
print(final.sort_values('OPS', ascending=False)[['Player_Name', 'Rookie_Year', 'HR', 'RBI', 'AVG', 'OPS']].head(10).to_string())

final.to_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv', index=True, index_label='Rank_by_Year')
print("\nSaved!")
```
6. 소포모어 시즌 데이터셋 구하기
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

rookies = pd.read_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv')
print(rookies[['Player_ID', 'Player_Name', 'Rookie_Year']].head(5))
print(f"Total players: {len(rookies)}")

r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
batting = pd.read_csv(io.StringIO(r.text))

yearly = batting.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()

soph_years = rookies[['Player_ID', 'Player_Name', 'Rookie_Year']].copy()
soph_years['Sophomore_Year'] = soph_years['Rookie_Year'] + 1

soph_stats = soph_years.merge(
    yearly,
    left_on=['Player_ID', 'Sophomore_Year'],
    right_on=['playerID', 'yearID'],
    how='left'
)

print(f"\nPlayers with sophomore data: {soph_stats['AB'].notna().sum()}")
print(f"Players missing sophomore data: {soph_stats['AB'].isna().sum()}")

missing = soph_stats[soph_stats['AB'].isna()][['Player_Name', 'Rookie_Year', 'Sophomore_Year']]
print("\nMissing sophomore seasons:")
print(missing.to_string(index=False))
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

rookies = pd.read_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv')
r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
batting = pd.read_csv(io.StringIO(r.text))

yearly = batting.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()

all_years = yearly[['playerID', 'yearID']].copy()

player_years = all_years.groupby('playerID')['yearID'].apply(sorted).reset_index()
player_years.columns = ['playerID', 'all_years']

def get_second_season(pid, years_dict):
    years = years_dict.get(pid, [])
    return years[1] if len(years) >= 2 else None

years_dict = dict(zip(player_years['playerID'], player_years['all_years']))

soph_years = rookies[['Player_ID', 'Player_Name', 'Rookie_Year']].copy()
soph_years['Sophomore_Year'] = soph_years['Player_ID'].apply(
    lambda pid: get_second_season(pid, years_dict)
)

print("Sophomore years assigned:")
print(soph_years[soph_years['Sophomore_Year'].notna()].tail(5))

missing_check = soph_years[soph_years['Player_ID'].isin([
    'jacobbu02', 'mathejo02', 'lawribr01', 'kipnija01', 'perezsa02',
    'goldspa01', 'hosmeer01', 'thameer01', 'cunnijo01', 'brandja01',
    'whitebi03', 'baxesji01'
])]
print("\nPreviously missing players:")
print(missing_check.to_string(index=False))
```
```{python}
import requests, io
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

rookies = pd.read_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv')
r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
batting = pd.read_csv(io.StringIO(r.text))

yearly = batting.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()

player_years = yearly.groupby('playerID')['yearID'].apply(sorted).reset_index()
player_years.columns = ['playerID', 'all_years']
years_dict = dict(zip(player_years['playerID'], player_years['all_years']))

def get_second_season(pid):
    years = years_dict.get(pid, [])
    return years[1] if len(years) >= 2 else None

soph_years = rookies[['Player_ID', 'Player_Name', 'Rookie_Year']].copy()
soph_years['Sophomore_Year'] = soph_years['Player_ID'].apply(get_second_season)

soph_stats = soph_years.merge(
    yearly,
    left_on=['Player_ID', 'Sophomore_Year'],
    right_on=['playerID', 'yearID'],
    how='left'
)

soph_stats['AVG'] = (soph_stats['H'] / soph_stats['AB']).round(3)
soph_stats['OBP'] = ((soph_stats['H'] + soph_stats['BB'] + soph_stats['HBP']) /
    (soph_stats['AB'] + soph_stats['BB'] + soph_stats['HBP'] + soph_stats['SF'])).round(3)
soph_stats['SLG'] = ((soph_stats['H'] + soph_stats['2B'] + 2*soph_stats['3B'] + 3*soph_stats['HR']) /
    soph_stats['AB']).round(3)
soph_stats['OPS'] = (soph_stats['OBP'] + soph_stats['SLG']).round(3)

final = soph_stats[[
    'Player_ID', 'Player_Name', 'Rookie_Year', 'Sophomore_Year',
    'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI',
    'SB', 'CS', 'BB', 'SO', 'HBP', 'AVG', 'OBP', 'SLG', 'OPS'
]].copy()

int_cols = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'HBP']
for col in int_cols:
    final[col] = final[col].fillna(0).astype(int)

final['Sophomore_Year'] = final['Sophomore_Year'].fillna('N/A - Beyond Dataset').astype(str).str.replace('.0', '', regex=False)

final = final.reset_index(drop=True)
final.index += 1

print(f"Shape: {final.shape}")
print(f"Players with full soph stats: {(final['AB'] > 0).sum()}")
print(f"Players beyond dataset (2012+): {(final['Sophomore_Year'] == 'N/A - Beyond Dataset').sum()}")
print(f"\nSample:")
print(final[['Player_Name', 'Rookie_Year', 'Sophomore_Year', 'G', 'AB', 'HR', 'RBI', 'AVG', 'OPS']].head(15).to_string())

final.to_csv('/mnt/user-data/outputs/mlb_sophomore_hitting_stats.csv', index=True, index_label='Rank')
print("\nSaved!")
```


소포모어 스텟 (1): [mlb_sophomore_hitting_stats.csv](https://github.com/user-attachments/files/28455758/mlb_sophomore_hitting_stats.csv)

루키 스텟 (1): [mlb_rookie_hitting_stats.csv](https://github.com/user-attachments/files/28455760/mlb_rookie_hitting_stats.csv)


딥러닝 모델까지 모두 실행한 후 데이터가 더 필요하다고 느껴 새 데이터셋을 다음 과정으로 구했다.

1. 기존 파일 읽기
```{python}
import pandas as pd
rookie = pd.read_csv('/mnt/user-data/uploads/mlb_rookie_hitting_stats.csv', nrows=3)
soph   = pd.read_csv('/mnt/user-data/uploads/mlb_sophomore_hitting_stats.csv', nrows=3)
print("Rookie cols:", rookie.columns.tolist())
print(rookie.head(2))
print("\nSoph cols:", soph.columns.tolist())
print(soph.head(2))
```
2. Lahman database에서 데이터 불러오기
```{python}
import requests, io, pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
batting = pd.read_csv(io.StringIO(r.text))
print(f"Full batting data: {batting.shape}")
print(f"Year range: {batting['yearID'].min()} - {batting['yearID'].max()}")
print(f"Unique players: {batting['playerID'].nunique()}")

yearly = batting.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()

rookie_years = yearly.groupby('playerID')['yearID'].min().reset_index()
rookie_years.columns = ['playerID', 'rookieYear']

rookie_stats = yearly.merge(rookie_years, on='playerID')
rookie_stats = rookie_stats[rookie_stats['yearID'] == rookie_stats['rookieYear']].copy()

rookie_stats = rookie_stats[
    (rookie_stats['AB'] >= 100) &
    (rookie_stats['yearID'] >= 1920)
].copy()

print(f"\nQualified rookies (AB>=100, 1920+): {len(rookie_stats)}")

rookie_stats['AVG'] = (rookie_stats['H'] / rookie_stats['AB']).round(3)
rookie_stats['OBP'] = ((rookie_stats['H'] + rookie_stats['BB'] + rookie_stats['HBP'].fillna(0)) /
                       (rookie_stats['AB'] + rookie_stats['BB'] + rookie_stats['HBP'].fillna(0) + rookie_stats['SF'].fillna(0))).round(3)
rookie_stats['SLG'] = ((rookie_stats['H'] + rookie_stats['2B'] + 2*rookie_stats['3B'] + 3*rookie_stats['HR']) /
                       rookie_stats['AB']).round(3)
rookie_stats['OPS'] = (rookie_stats['OBP'] + rookie_stats['SLG']).round(3)

top1200 = rookie_stats.sort_values('OPS', ascending=False).head(1200).copy()
print(f"Top 1200 by OPS, year range: {top1200['yearID'].min()} - {top1200['yearID'].max()}")
print(top1200['yearID'].value_counts().sort_index().head(20))
```
3. 선수 1000명으로 늘리고 csv로 저장
```{python}
import requests, io, pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get("https://raw.githubusercontent.com/maxtoki/baseball_R/master/data/Batting.csv", headers=headers, timeout=30)
batting = pd.read_csv(io.StringIO(r.text))

yearly = batting.groupby(['playerID', 'yearID']).agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'SO': 'sum',
    'HBP': 'sum', 'SF': 'sum'
}).reset_index()
player_years = yearly.groupby('playerID')['yearID'].apply(sorted).reset_index()
player_years.columns = ['playerID', 'all_years']
years_dict = dict(zip(player_years['playerID'], player_years['all_years']))

rookie_years_map = {pid: yrs[0] for pid, yrs in years_dict.items()}
rookie_years_df = pd.DataFrame(list(rookie_years_map.items()), columns=['playerID', 'rookieYear'])

rookie_stats = yearly.merge(rookie_years_df, on='playerID')
rookie_stats = rookie_stats[rookie_stats['yearID'] == rookie_stats['rookieYear']].copy()
rookie_stats = rookie_stats[(rookie_stats['AB'] >= 100) & (rookie_stats['yearID'] >= 1920)].copy()

def compute_rates(df):
    df = df.copy()
    df['HBP'] = df['HBP'].fillna(0)
    df['SF']  = df['SF'].fillna(0)
    df['AVG'] = (df['H'] / df['AB']).round(3)
    df['OBP'] = ((df['H'] + df['BB'] + df['HBP']) /
                 (df['AB'] + df['BB'] + df['HBP'] + df['SF'])).round(3)
    df['SLG'] = ((df['H'] + df['2B'] + 2*df['3B'] + 3*df['HR']) / df['AB']).round(3)
    df['OPS'] = (df['OBP'] + df['SLG']).round(3)
    return df

rookie_stats = compute_rates(rookie_stats)

top1000_rookies = rookie_stats.sort_values('OPS', ascending=False).head(1000).copy()
top1000_rookies = top1000_rookies.sort_values(['yearID', 'OPS'], ascending=[True, False])
player_ids_1000 = top1000_rookies['playerID'].tolist()

print(f"Top 1000 rookies selected")
print(f"Year range: {top1000_rookies['yearID'].min()} - {top1000_rookies['yearID'].max()}")

def get_second_season(pid):
    yrs = years_dict.get(pid, [])
    return yrs[1] if len(yrs) >= 2 else None

soph_map = {pid: get_second_season(pid) for pid in player_ids_1000}

existing_names = {
    'lenhado01': 'Don Lenhardt', 'norenir01': 'Irv Noren', 'jethrsa01': 'Sam Jethroe',
    'bellgu01': 'Gus Bell', 'mcdougi01': 'Gil McDougald', 'mayswi01': 'Willie Mays',
    'mantlmi01': 'Mickey Mantle', 'rhodedu01': 'Dusty Rhodes', 'gernedi01': 'Dick Gernert',
    'gilliji01': 'Jim Gilliam', 'pendlji01': 'Jim Pendleton', 'skowrbi01': 'Bill Skowron',
    'cunnijo01': 'Joe Cunningham', 'moonwa01': 'Wally Moon', 'finigji01': 'Jim Finigan',
    'aaronha01': 'Hank Aaron', 'howarel01': 'Elston Howard', 'halebo01': 'Bob Hale',
    'robinfr02': 'Frank Robinson', 'skizalo01': 'Lou Skizas', 'brandja01': 'Jackie Brandt',
    'whitebi03': 'Bill White', 'anderha02': 'Harry Anderson', 'wagnele01': 'Leon Wagner',
    'cepedor01': 'Orlando Cepeda', 'stuardi01': 'Dick Stuart', 'graydi01': 'Dick Gray',
    'kirklwi01': 'Willie Kirkland', 'larkeno01': 'Norm Larker', 'mccovwi01': 'Willie McCovey',
    'snyderu01': 'Russ Snyder', 'baxesji01': 'Jim Baxes', 'mayele01': 'Lee Maye',
    'thomale03': 'Lee Thomas', 'charled01': 'Ed Charles', 'lockdo01': 'Don Lock',
    'jimenma01': 'Manny Jiminez', 'whitffr01': 'Fred Whitfield', 'hallji02': 'Jim Hall',
    'deesch01': 'Charlie Dees', 'conigto01': 'Tony Conigliaro', 'blefacu01': 'Curt Blefary',
    'foyjo01': 'Joe Foy', 'raderdo02': 'Don Rader', 'fostero01': 'Roy Foster',
    'cedence01': 'Cesar Cedeno', 'stennre01': 'Rennie Stennett', 'hargrmi01': 'Mike Hargrove',
    'pagemi02': 'Mitchell Page', 'hendest01': 'Steve Henderson', 'murraed02': 'Eddie Murray',
    'puhlte01': 'Terry Puhl', 'willsbu01': 'Bump Wills', 'hornebo01': 'Bob Horner',
    'charbjo01': 'Joe Charboneau', 'salazlu01': 'Luis Salazar', 'staplda01': 'Dave Stapleton',
    'boggswa01': 'Wade Boggs', 'johnsho01': 'Howard Johnson', 'wilsogl01': 'Glenn Wilson',
    'strawda01': 'Darryl Strawberry', 'esaskni01': 'Nick Esasky', 'vanslan01': 'Andy Van Slyke',
    'davisal01': 'Alvin Davis', 'daviser01': 'Eric Davis', 'pendlte01': 'Terry Pendleton',
    'danieka01': 'Kal Daniels', 'krukjo01': 'John Kruk', 'joynewa01': 'Wally Joyner',
    'snydeco02': 'Cory Snyder', 'clarkwi02': 'Will Clark', 'incavpe01': 'Pete Incaviglia',
    'sierrru01': 'Ruben Sierra', 'hornsa01': 'Sam Horn', 'lindjo01': 'Jose Lind',
    'benzito01': 'Todd Benzinger', 'surhobj01': 'B.J. Surhoff', 'jordari02': 'Ricky Jordan',
    'gracema01': 'Mark Grace', 'smithdw01': 'Dwight Smith', 'thomafr04': 'Frank Thomas',
    'maaske01': 'Kevin Maas', 'frymatr01': 'Travis Fryman', 'barbebr01': 'Bret Barberie',
    'newsowa01': 'Warren Newson', 'bagweje01': 'Jeff Bagwell', 'martich01': 'Chuck Martinez',
    'valenjo02': 'Jose Valentin', 'stockke01': 'Kevin Stocker', 'burnije01': 'Jeremy Burnitz',
    'greerru01': 'Rusty Greer', 'moutoly01': 'Lyle Mouton', 'cordoma01': 'Manny Cordova',
    'nunnajo01': 'Jon Nunnally', 'timmooz01': 'Ozzie Timmons', 'batesja01': 'Jason Bates',
    'houstty01': 'Tyler Houston', 'muellbi02': 'Bill Mueller', 'osikke01': 'Keith Osik',
    'batisto01': 'Tony Batista', 'kendaja01': 'Jason Kendall', 'cruzjo02': 'Jose Cruz Jr.',
    'orieke01': 'Kevin Orie', 'bergda01': 'Dave Berg', 'leetr01': 'Travis Lee',
    'durazer01': 'Erubiel Durazo', 'blumge01': 'Geoff Blum', 'singlch01': 'Chris Singleton',
    'jonesja04': 'Jacque Jones', 'morriwa02': 'Warren Morris', 'leeca01': 'Carlos Lee',
    'piattad01': 'Adam Piatt', 'richach01': 'Chris Richard', 'tracyan01': 'Andy Tracy',
    'burrepa01': 'Pat Burrell', 'lugoju01': 'Julio Lugo', 'furcara01': 'Rafael Furcal',
    'trubych01': 'Chris Truby', 'pujolal01': 'Albert Pujols', 'wilsocr03': 'Craig Wilson',
    'dunnad01': 'Adam Dunn', 'uribeju01': 'Juan Uribe', 'suzukic01': 'Ichiro Suzuki',
    'gibboja01': 'Jay Gibbons', 'spiveju01': 'Junior Spivey', 'gilesma01': 'Marcus Giles',
    'kearnau01': 'Austin Kearns', 'hinsker01': 'Eric Hinske', 'menchke01': 'Kevin Mench',
    'gerutjo01': 'Joey Gerut', 'hammoro01': 'Robby Hammock', 'teixema01': 'Mark Teixeira',
    'cabremi01': 'Miguel Cabrera', 'matsuhi01': 'Hideki Matsui', 'johnsre02': 'Reed Johnson',
    'wrighda03': 'David Wright', 'hollima01': 'Matt Holliday', 'jacobbu02': 'Buck Jacobsen',
    'larocad01': 'Adam LaRoche', 'thomach01': 'Charles Thomas', 'cantujo01': 'Jorge Cantu',
    'gonzalu02': 'Luis Gonzalez', 'sledgte01': 'Terrmel Sledge', 'youklke01': 'Kevin Youkilis',
    'murtoma01': 'Matt Murton', 'francje02': 'Jeff Francoeur', 'rodrijo03': 'John Rodriguez',
    'johnsda06': 'Dan Johnson', 'iguchta01': 'Tadahito Iguchi', 'canoro01': 'Robinson Cano',
    'costech01': 'Chris Costello', 'drewst01': 'Stephen Drew', 'quentca01': 'Carlos Quentin',
    'ethiean01': 'Andre Ethier', 'ugglada01': 'Dan Uggla', 'napolmi01': 'Mike Napoli',
    'kinslia01': 'Ian Kinsler', 'markani01': 'Nick Markakis', 'martiru01': 'Russell Martin',
    'johjike01': 'Kenji Johjima', 'braunry02': 'Ryan Braun', 'hamiljo03': 'Josh Hamilton',
    'pencehu01': 'Hunter Pence', 'bucktr01': 'Travis Buck', 'reynoma01': 'Mark Reynolds',
    'escobyu01': 'Yunel Escobar', 'butlebi03': 'Billy Butler', 'cabreas01': 'Asdrubal Cabrera',
    'iwamuak01': 'Akinori Iwamura', 'davisch02': 'Chris Davis', 'longoev01': 'Evan Longoria',
    'murphda08': 'David Murphy', 'sandopa01': 'Pablo Sandoval', 'bakerjo01': 'John Baker',
    'avilemi01': 'Mike Aviles', 'joycema01': 'Matt Joyce', 'spande01': 'Denard Span',
    'ramiral03': 'Alexei Ramirez', 'mathejo02': 'Joe Mather', 'blankky01': 'Kyle Blanks',
    'coghlch01': 'Chris Coghlan', 'mccutan01': 'Andrew McCutchen', 'reimono01': 'Nolan Reimold',
    'beckhgo01': 'Gordon Beckham', 'borboju01': 'Julio Borbon', 'santaca01': 'Carlos Santana',
    'heywaja01': 'Jason Heyward', 'morrilo01': 'Logan Morrison', 'morelmi01': 'Mitch Moreland',
    'stantmi03': 'Mike Stanton', 'valenda01': 'Danny Valencia', 'davisik02': 'Ike Davis',
    'alvarpe01': 'Pedro Alvarez', 'jayjo02': 'Jon Jay', 'lawribr01': 'Brett Lawrie',
    'kipnija01': 'Jason Kipnis', 'perezsa02': 'Salvador Perez', 'goldspa01': 'Paul Goldschmidt',
    'hosmeer01': 'Eric Hosmer', 'thameer01': 'Eric Thames',
    'musiast01':'Stan Musial','willihe01':'Harry Williams','gehrich01':'Charlie Gehringer',
    'demaggj01':'Joe DiMaggio','williib02':'Bill Williams','rizzuph01':'Phil Rizzuto',
    'robinja02':'Jackie Robinson','campanro01':'Roy Campanella','slaught01':'Enos Slaughter',
    'schoeri01':'Red Schoendienst','kinerro01':'Ralph Kiner','hodgegi01':'Gil Hodges',
    'sniderd01':'Duke Snider','matheed01':'Eddie Mathews','bankser01':'Ernie Banks',
    'clemero01':'Roberto Clemente','mazerbi01':'Bill Mazeroski','boyerke01':'Ken Boyer',
    'colavin01':'Vince Coleman','torgebu01':'Bob Torgesson','westlji01':'Jim Westlake',
    'boonera01':'Ray Boone','thomafr02':'Frank Thomas','nixonwi01':'Willard Nixon',
    'lockman01':'Whitey Lockman','westlwi01':'Wes Westrum','joosteb01':'Eddie Joost',
    'smallro01':'Roy Smalley','schoefr01':'Frank Shofner','seminoza01':'Zoilo Versalles',
    'alstowa01':'Walter Alston','pillehe01':'Herb Pillete','garveho01':'Hob Garvey',
    'siebelc01':'Charley Siebel','wilsojo05':'Joe Wilson','robinju01':'Junior Robinson',
    'colliejo02':'Joe Collins','marteal01':'Al Martin','ashburi01':'Richie Ashburn',
    'dimagdo01':'Dom DiMaggio','ellibi01':'Bibb Falk','heguemi01':'Mike Hegan',
    'schmimi01':'Mike Schmidt','brettge01':'George Brett','yastrca01':'Carl Yastrzemski',
    'mccovwi01':'Willie McCovey','stargwi01':'Willie Stargell','benchjo01':'Johnny Bench',
    'rosepe01':'Pete Rose','morgajo02':'Joe Morgan','carewro01':'Rod Carew',
    'jacksr01':'Reggie Jackson','brocklo01':'Lou Brock','gibsobo01':'Bob Gibson',
    'killeha01':'Harmon Killebrew','mccovwi01':'Willie McCovey','fiskca01':'Carlton Fisk',
    'lynnfr01':'Fred Lynn','riceji01':'Jim Rice','murphda05':'Dale Murphy',
    'guerrpe01':'Pedro Guerrero','henderi01':'Rickey Henderson','bondsba01':'Barry Bonds',
    'mcgwima01':'Mark McGwire','sosasd01':'Sammy Sosa','ripkeca01':'Cal Ripken Jr.',
    'gonzaju03':'Juan Gonzalez','griffke02':'Ken Griffey Jr.','thomafr04':'Frank Thomas',
    'piazzmi01':'Mike Piazza','biggiocr01':'Craig Biggio','jeterde01':'Derek Jeter',
    'rodrial01':'Alex Rodriguez','ordonma01':'Magglio Ordonez','beltrad01':'Adrian Beltre',
    'ramirma02':'Manny Ramirez','walketo04':'Todd Walker','abadfe01':'Fernando Abad',
}

first_name_map = {
    'ha':'Hank','wi':'Willie','mi':'Mike','jo':'Joe','bo':'Bob','ro':'Ron',
    'ji':'Jim','bi':'Bill','to':'Tom','fr':'Frank','do':'Don','ri':'Rich',
    'da':'Dave','ed':'Ed','ge':'George','ch':'Chris','ma':'Mark','st':'Steve',
    'ke':'Ken','la':'Larry','di':'Dick','al':'Al','ra':'Randy','ga':'Gary',
    'te':'Terry','wa':'Walt','el':'Elston','sa':'Sam','ir':'Irv','gu':'Gus',
    'gi':'Gil','du':'Duke','ca':'Cal','le':'Lee','pe':'Pete','ba':'Barry',
    'ru':'Rusty','ja':'Jason','ty':'Ty','lo':'Lou','de':'Derek','ad':'Adam',
    'an':'Andy','gr':'Greg','br':'Brad','sc':'Scott','pa':'Pat','vi':'Vlad',
    'be':'Ben','no':'Nomar','cr':'Craig','je':'Jeff','ti':'Tim','mo':'Mo',
    'ph':'Phil','eu':'Eugene','ha':'Harold','lu':'Luis','ra':'Rafael','ja':'Jack',
    'cl':'Cleon','bu':'Buster','pi':'Pinson','si':'Sixto','ol':'Oliver',
    'ar':'Arn','ne':'Nelson','wa':'Warren','he':'Hector','os':'Ozzie',
    'li':'Lin','re':'Reggie','wh':'Whitey','gl':'Glen','ey':'Eyton',
    'ni':'Nick','fl':'Flip','se':'Seto','er':'Ernest','ab':'Alberto',
    'ro':'Roberto','id':'Idilio','oc':'Octavio','to':'Tomas','mi':'Mickey',
    'ha':'Harry','ic':'Ichiro',
}

def decode_id(pid):
    if pid in existing_names:
        return existing_names[pid]
    core = pid[:-2]
    first_abbr = core[-2:].lower() if len(core) >= 2 else core.lower()
    last_raw = core[:-2] if len(core) > 2 else core
    last = last_raw.capitalize()
    first = first_name_map.get(first_abbr, first_abbr.capitalize()+'.')
    return f"{first} {last}"

top1000_rookies['Player_Name'] = top1000_rookies['playerID'].apply(decode_id)

int_cols = ['G','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','HBP']
for c in int_cols:
    top1000_rookies[c] = top1000_rookies[c].fillna(0).astype(int)

rookie_final = top1000_rookies[[
    'playerID','Player_Name','yearID','G','AB','R','H','2B','3B','HR','RBI',
    'SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS'
]].copy()
rookie_final.columns = [
    'Player_ID','Player_Name','Rookie_Year','G','AB','R','H','2B','3B','HR','RBI',
    'SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS'
]
rookie_final = rookie_final.reset_index(drop=True)
rookie_final.index += 1

soph_list = []
for pid in top1000_rookies['playerID']:
    sy = soph_map.get(pid)
    if sy is None:
        soph_list.append(None)
        continue
    row = yearly[(yearly['playerID']==pid) & (yearly['yearID']==sy)]
    if len(row) == 0:
        soph_list.append(None)
    else:
        soph_list.append((sy, row.iloc[0]))

soph_rows = []
for i, (pid, s_entry) in enumerate(zip(top1000_rookies['playerID'], soph_list)):
    r_row = top1000_rookies.iloc[i]
    if s_entry is None:
        sr = {c: 0 for c in int_cols}
        sr.update({'playerID': pid, 'yearID': None, 'AVG': None, 'OBP': None, 'SLG': None, 'OPS': None})
    else:
        sy, srow = s_entry
        hbp = srow['HBP'] if pd.notna(srow['HBP']) else 0
        sf  = srow['SF']  if pd.notna(srow['SF'])  else 0
        ab  = srow['AB']
        h   = srow['H']
        bb  = srow['BB']
        b2  = srow['2B']
        b3  = srow['3B']
        hr  = srow['HR']
        avg = round(h/ab, 3) if ab > 0 else None
        obp = round((h+bb+hbp)/(ab+bb+hbp+sf), 3) if (ab+bb+hbp+sf) > 0 else None
        slg = round((h+b2+2*b3+3*hr)/ab, 3) if ab > 0 else None
        ops = round(obp+slg, 3) if (obp and slg) else None
        sr = {
            'playerID': pid, 'yearID': int(sy),
            'G': int(srow['G']), 'AB': int(ab), 'R': int(srow['R']), 'H': int(h),
            '2B': int(b2), '3B': int(b3), 'HR': int(hr), 'RBI': int(srow['RBI']),
            'SB': int(srow['SB']), 'CS': int(srow['CS']), 'BB': int(bb),
            'SO': int(srow['SO']), 'HBP': int(hbp),
            'AVG': avg, 'OBP': obp, 'SLG': slg, 'OPS': ops
        }
    soph_rows.append(sr)

soph_df = pd.DataFrame(soph_rows)
soph_df['Player_Name'] = top1000_rookies['Player_Name'].values
soph_df['Rookie_Year'] = top1000_rookies['yearID'].values
soph_df = soph_df.rename(columns={'yearID': 'Sophomore_Year', 'playerID': 'Player_ID'})

soph_final = soph_df[[
    'Player_ID','Player_Name','Rookie_Year','Sophomore_Year','G','AB','R','H',
    '2B','3B','HR','RBI','SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS'
]].reset_index(drop=True)
soph_final.index += 1

rookie_final.insert(0, 'Rank_by_Year', rookie_final.index)
soph_final.insert(0, 'Rank', soph_final.index)

rookie_final.to_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats_1000.csv', index=False)
soph_final.to_csv('/mnt/user-data/outputs/mlb_sophomore_hitting_stats_1000.csv', index=False)

print(f"\nRookie CSV: {rookie_final.shape}")
print(f"Soph CSV: {soph_final.shape}")
print(f"\nYear range (rookie): {rookie_final['Rookie_Year'].min()} - {rookie_final['Rookie_Year'].max()}")
print(f"Soph with data: {(soph_final['AB'] > 0).sum()}")
print(f"Soph no data (beyond dataset/only 1 season): {(soph_final['AB'] == 0).sum()}")
print("\nSample rookie rows:")
print(rookie_final[['Rank_by_Year','Player_Name','Rookie_Year','HR','AVG','OPS']].head(10).to_string(index=False))
print("\nSample soph rows:")
print(soph_final[['Rank','Player_Name','Rookie_Year','Sophomore_Year','HR','AVG','OPS']].head(10).to_string(index=False))
```


소포모어 스텟 (2): [mlb_sophomore_hitting_stats_1000.csv](https://github.com/user-attachments/files/28701272/mlb_sophomore_hitting_stats_1000.csv)

루키 스텟 (2): [mlb_rookie_hitting_stats_1000.csv](https://github.com/user-attachments/files/28701257/mlb_rookie_hitting_stats_1000.csv)

두번째 모델 학습 이후 다음 데이터셋을 추가로 수집하였다. 해당 데이터셋은 OPS가 아닌 다른 기준으로 징크스 여부를 구분하였으며, 데이터셋 자체에 선수별 징크스 여부가 표기되어있다.

다음과 같은 modern stat을 추가했다.

1. 물리 피지컬 지표: 평균 타구 속도, 최고 타구 속도, 배럴 타구 비율을 통해 선수의 하드웨어적 강점을 파악한다.
2. 기량 및 선구안 지표: 기대 타율, 기대 장타율, 삼진율, 타석 수를 통해 타격의 정확도와 선구안, 그리고 신뢰할 수 있는 샘플 크기인지를 신경망이 인지하도록 한다.
3. wOBA: 수년간의 메이저리그 데이터를 통계적으로 분석해서 "각 출루 상황이 실제로 팀의 '득점 가치'를 얼마나 올렸는지" 가중치를 구한 뒤 이를 곱해주는 방식.
공식은 매년 메이저리그 전체의 득점 환경에 따라 가중치 숫자가 미세하게 변하지만, 기본적인 구조는 아래와 같다 (2020년대 MLB 평균 기준 공식): 
wOBA 분자 : (홈런)*0.2 + (3루타)*1.6 + (2루타)*1.3 + (1루타)*0.9 + (볼넷)*0.7 + (몸에 맞는 공)*0.7
wOBA 분모 : 타수(AB) + 볼넷(BB) - 고의사구(IBB) + 희생플라이(SF) + 몸에 맞는 공(HBP)

이들은 어떠한 결과라기보다는, 선수의 실력, 컨디션등을 알아보기에 적합한 자료이다. 타구 속도는 타자에게 정말 중요한 컨택 능력, 스윙 속도등에 큰 영향을 받는 지표이고, 이게 바탕이 되어야 베럴 타구를 생산해낼 수 있기 때문이다. 따라서 이 지표들을 소포모어 징크스를 파악하기에 가장 적합한 modern stat의 지표들로 꼽았다.

이후 라이브러리를 이용한 데이터 크롤링을 통해 데이터 수집을 진행하였다.

한국 야구 리그인 ‘KBO’에서 뛰는 선수들의 데이터는 ‘스탯티즈’라는 사이트에 굉장히 세세하게 나와있지만, 크롤링이 금지되어 있다. 그래서 미국 야구 리그인 ‘MLB’의 데이터를 모아보고자, MLB.com, Baseball Savant를 찾아보았다. 원하는 자료를 최대한 얻을 수 있긴 했지만, 필요한 지표들만 골라서 얻기는 쉽지 않았다.

데이터 수집에 쓰인 라이브러리는 다음과 같다.

 - pybaseball : 공식 데이터 제공 사이트를 방문하지 않고도 데이터 크롤링을 가능하게 해주는 ‘야구 데이터 수집 전문 라이브러리’이다.

원하는 연도, 최소 타석수등을 정해두고, 조건에 맞게 평균 타구 속도, 배럴 타구 비율 등을 얻을 수 있었다.

 - pandas.concat : 각 연도별 데이터를 리스트에 담은 후, 데이터를 위 아래로 통합한다. (데이터 아래로 내려갈 수록 최근 연도)

 - pandas.merge : ‘player_id’라는 열을 기준으로 한 선수의 1년차, 2년차 성적을 하나의 행으로 합친다. (1년차를 왼쪽에, 2년차를 오른쪽에 배치)

 - pandas.to_csv : 최종적으로 정제가 완료된 데이터를 로컬 하드디스크에 .csv 형식으로 저장해준다.

 그리고 데이터의 가장 오른쪽에, 선수들의 징크스 여부를 일괄적으로 판단할 수 있는 열을 하나 추가하였다.

소포모어 징크스(is_jinx)의 판단 기준
이 데이터셋에서 소포모어 징크스의 발생 여부는 가중 출루율(wOBA)의 변화를 기준으로 정의한다. wOBA는 1루타, 2루타, 3루타, 홈런, 볼넷 등 각 출루 항목이 득점에 기여하는 실제 가치를 가중치로 부여하여 계산한 현대 야구 최고의 종합 타격 생산성 지표라고 할 수 있다.
1년 차 성적에 비해 2년 차의 wOBA가 감소한 경우 소포모어 징크스가 발생한 것(1)으로 판단하며, 성적을 유지하거나 오히려 향상된 경우는 징크스를 극복한 것(0)으로 라벨링한다.

이 과정을 통해서 18시즌부터 25시즌까지의 메이저리그 선수들의 데이터를 모았다. 이대로 딥러닝을 진행하려 했으나, 더 많은 피쳐와, 더 많은 데이터(18년도보다 이전 데이터까지)를 고려하는 것이 좋지 않겠냐는 팀원들의 의견에 동의를 하고, 팀원들과 함께 새 데이터 세트를 구하고, 딥러닝을 진행하였다.

Modern stat: [mlb_jinx_advanced_data.csv](https://github.com/user-attachments/files/28736296/mlb_jinx_advanced_data.csv)


# Methodology
1. 소포모어 징크스를 겪은 선수의 기준을 정하기 위해 선형회귀를 활용한다.
2. 로지스틱 회귀를 활용하여 징크스를 겪은 선수들과 그렇지 않은 선수들을 나눈 요인을 찾아본다.

# Evaluation & Analysis
Methodology의 1단계를 실행한 결과는 다음과 같다.

모델:
```{python}
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

rookie = pd.read_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv')
soph = pd.read_csv('/mnt/user-data/outputs/mlb_sophomore_hitting_stats.csv')

merged = rookie.merge(
    soph[['Player_ID','Sophomore_Year','G','AB','R','H','2B','3B','HR','RBI',
          'SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS']],
    on='Player_ID', suffixes=('_r','_s')
)
merged = merged[(merged['AB_s'] > 0) & (merged['OPS_s'] > 0)].copy()


X = merged[['OPS_r']].values
y = merged['OPS_s'].values

model = LinearRegression()
model.fit(X, y)

slope     = model.coef_[0]
intercept = model.intercept_
r2        = r2_score(y, model.predict(X))
rmse      = np.sqrt(mean_squared_error(y, model.predict(X)))

print(f"Linear regression: Soph_OPS = {slope:.4f} × Rookie_OPS + {intercept:.4f}")
print(f"R²   = {r2:.4f}")
print(f"RMSE = {rmse:.4f}")


merged['predicted_soph_OPS'] = model.predict(X)
merged['residual'] = merged['OPS_s'] - merged['predicted_soph_OPS']

print(f"\nResidual stats:")
print(merged['residual'].describe())


res_mean = merged['residual'].mean()
res_std  = merged['residual'].std()
threshold_1sd = res_mean - 1.0 * res_std
threshold_15sd = res_mean - 1.5 * res_std

print(f"\nResidual mean : {res_mean:.4f}")
print(f"Residual std  : {res_std:.4f}")
print(f"Threshold (−1σ) : {threshold_1sd:.4f}")
print(f"Threshold (−1.5σ): {threshold_15sd:.4f}")


merged['jinxed'] = (merged['residual'] < threshold_1sd).astype(int)
n_jinxed = merged['jinxed'].sum()
print(f"\nPlayers labelled jinxed (−1σ): {n_jinxed} / {len(merged)} = {n_jinxed/len(merged)*100:.1f}%")


print(f"\nA player is jinxed if their sophomore OPS is >{abs(threshold_1sd):.3f} below what was predicted")
print(f"(given their rookie OPS)")


jinxed_df = merged[merged['jinxed']==1].sort_values('residual')[
    ['Player_Name','Rookie_Year','OPS_r','OPS_s','predicted_soph_OPS','residual']
].head(15)
print("\nTop 15 most jinxed:")
print(jinxed_df.to_string(index=False))


best_df = merged.sort_values('residual', ascending=False)[
    ['Player_Name','Rookie_Year','OPS_r','OPS_s','predicted_soph_OPS','residual']
].head(10)
print("\nTop 10 most improved (beat prediction):")
print(best_df.to_string(index=False))
```

<img width="596" height="403" alt="jinx threshold" src="https://github.com/user-attachments/assets/1f3cf198-d723-4e48-bcff-a0ddff3ef1e8" />
<img width="612" height="561" alt="jinxed players" src="https://github.com/user-attachments/assets/0956306c-ace5-414b-8828-0a9df111765f" />

모든 선수들의 OPS를 선형회귀로 분석하여 징크스의 기준을 잡았다. 징크스의 기준은 루키 시즌에 비해 OPS가 0.112보다 크게 감소한 것으로 정했다. 데이터의 양이 적은 관계로
징크스를 겪은 선수는 총 23명 뿐, 전체 선수들 중 12%이다. 2단계에서 오버피팅을 피해야 함을 주의해야한다.


Methodology의 2단계를 실행한 결과는 다음과 같다.

모델:
```{python}
import pandas as pd, numpy as np, json, warnings
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
warnings.filterwarnings('ignore')

rookie = pd.read_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv')
soph   = pd.read_csv('/mnt/user-data/outputs/mlb_sophomore_hitting_stats.csv')

merged = rookie.merge(
    soph[['Player_ID','Sophomore_Year','G','AB','R','H','2B','3B','HR','RBI',
          'SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS']],
    on='Player_ID', suffixes=('_r','_s')
)
merged = merged[(merged['AB_s']>0)&(merged['OPS_s']>0)].copy()
print("Merged cols:", [c for c in merged.columns if 'SF' in c or 'HBP' in c])


lr = LinearRegression().fit(merged[['OPS_r']], merged['OPS_s'])
merged['predicted_soph_OPS'] = lr.predict(merged[['OPS_r']])
merged['residual'] = merged['OPS_s'] - merged['predicted_soph_OPS']
threshold = -merged['residual'].std()
merged['jinxed'] = (merged['residual'] < threshold).astype(int)


merged['HR_rate']  = merged['HR_r']  / merged['AB_r']
merged['BB_rate']  = merged['BB_r']  / merged['AB_r']
merged['SO_rate']  = merged['SO_r']  / merged['AB_r']
merged['ISO']      = merged['SLG_r'] - merged['AVG_r']
merged['partial']  = (merged['AB_r'] < 300).astype(int)
merged['BABIP']    = ((merged['H_r'] - merged['HR_r']) /
                      (merged['AB_r'] - merged['SO_r'] - merged['HR_r'] + 1)
                     ).clip(0,1)

features     = ['OPS_r','HR_rate','BB_rate','SO_rate','ISO','partial','BABIP','AVG_r']
feat_labels  = ['Rookie OPS','HR Rate','BB Rate','SO Rate','ISO (Power)',
                'Partial Season','BABIP','Batting Avg']

df = merged[features+['jinxed','Player_Name','Rookie_Year']].dropna().copy()
X  = df[features].values
y  = df['jinxed'].values
print(f"n={len(df)}, jinxed={y.sum()} ({y.mean()*100:.1f}%)")

scaler = StandardScaler()
X_sc   = scaler.fit_transform(X)

model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
model.fit(X_sc, y)

cv      = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_auc  = cross_val_score(model, X_sc, y, cv=cv, scoring='roc_auc')
cv_f1   = cross_val_score(model, X_sc, y, cv=cv, scoring='f1')
cv_acc  = cross_val_score(model, X_sc, y, cv=cv, scoring='accuracy')

y_prob  = model.predict_proba(X_sc)[:,1]
y_pred  = model.predict(X_sc)
cm      = confusion_matrix(y, y_pred)
fpr,tpr,_ = roc_curve(y, y_prob)
auc     = roc_auc_score(y, y_prob)

coefs = sorted(zip(feat_labels, model.coef_[0]), key=lambda x: x[1])

df['jinx_prob']       = y_prob
df['predicted_jinxed']= y_pred

print(f"\nAUC={auc:.3f}, CV-AUC={cv_auc.mean():.3f}±{cv_auc.std():.3f}")
print(f"CV-F1={cv_f1.mean():.3f}, CV-Acc={cv_acc.mean():.3f}")
print("\nConfusion matrix:\n", cm)
print("\nCoefficients:")
for f,c in coefs:
    print(f"  {f:20s} coef={c:.4f}  OR={np.exp(c):.3f}")

out = {
    'n_players': int(len(df)), 'n_jinxed': int(y.sum()),
    'pct_jinxed': round(float(y.mean()*100),1),
    'threshold': round(float(threshold),4),
    'cv_auc': round(float(cv_auc.mean()),3), 'cv_auc_std': round(float(cv_auc.std()),3),
    'cv_f1': round(float(cv_f1.mean()),3),   'cv_acc': round(float(cv_acc.mean()),3),
    'auc': round(float(auc),3),
    'intercept': round(float(model.intercept_[0]),4),
    'confusion_matrix': cm.tolist(),
    'coefficients': [{'feature':f,'coef':round(float(c),4),'odds_ratio':round(float(np.exp(c)),4)} for f,c in coefs],
    'roc_fpr': [round(float(v),4) for v in fpr],
    'roc_tpr': [round(float(v),4) for v in tpr],
    'players': [
        {'name': row.Player_Name, 'year': int(row.Rookie_Year),
         'jinx_prob': round(float(row.jinx_prob),4),
         'actual': int(row.jinxed), 'predicted': int(row.predicted_jinxed),
         'ops_r': round(float(df.at[idx,'OPS_r']),3),
         'hr_rate': round(float(df.at[idx,'HR_rate']),4),
         'bb_rate': round(float(df.at[idx,'BB_rate']),4),
         'so_rate': round(float(df.at[idx,'SO_rate']),4),
         'partial': int(df.at[idx,'partial']),
         'babip': round(float(df.at[idx,'BABIP']),3),
         'iso': round(float(df.at[idx,'ISO']),3),
        }
        for idx, row in df.iterrows()
    ]
}
with open('/tmp/logit_results.json','w') as f:
    json.dump(out, f)
print("Saved. JSON size:", len(json.dumps(out)))
```

<img width="927" height="317" alt="화면 캡처 2026-06-08 013230" src="https://github.com/user-attachments/assets/71a2f972-3ca8-4d51-8395-679de62c1183" />
<img width="926" height="237" alt="화면 캡처 2026-06-08 013253" src="https://github.com/user-attachments/assets/c01a6f33-a140-4da6-959a-89064f3714fe" />
<img width="967" height="727" alt="화면 캡처 2026-06-08 013325" src="https://github.com/user-attachments/assets/0ed03e9b-06dd-44cd-8c1a-5d8007e3bdd9" />

첫번째 표는 징크스를 겪은 선수들과 그렇지 않은 선수들을 가르는 데에 영향을 미친 요인을 분석한 표이다. BB Rate(볼넷, 사구로 인한 출루)와 ISO(장타율)가 높은 타자들이 징크스를 피할 확률이 높은 것을 알 수 있다. 반면, SO Rate(삼진)가 높거나 루키 시즌의 일부만 보낸(Partial season) 선수들의 징크스 확률이 더 높게 나왔다.

두번째 표는 모델이 징크스를 예측한 결과를 보여주는 표이다. 표에서 보이듯이 위양성이 54개로 정확히 예측한 15개를 크게 웃도는 수치다. 마지막 그래프에서 알 수 있듯이 정확도는 0.678 정도로 무작위로 예측하는 경우일 때(대략 0.5 정확도)보다는 좋은 성능을 보여주지만, 그리 높은 정확도는 아니다. 전체 데이터량이 192명의 선수에 불과해서 이러한 결과가 나온 것으로 보인다.

다음은 위 모델의 결과를 보완하기 위해 구한 새 데이터셋을 사용해 Methodology의 1번부터 다시 실행한 결과이다.

우선 징크스의 기준을 선형 회귀로 다시 구한 결과이다.

<img width="930" height="690" alt="jinx threshold 1000 2" src="https://github.com/user-attachments/assets/fa2d96fb-08e5-41f2-96cd-2a2ca36cfd39" />

2년차 데이터가 존재하지 않는 선수들을 제외하여 총 924명의 선수를 분석하였다. 징크스의 기준은 OPS가 0.112 이상 감소한 것으로 정해졌고, 이는 첫 데이터셋을 활용했을 때와 같은 결과이다.

다음은 이전과 같은 로지스틱 회귀 모델과 새 데이터셋을 활용하여 모델을 실행한 결과이다.

모델:
```{python}
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import json, warnings
warnings.filterwarnings('ignore')

rookie = pd.read_csv('/mnt/user-data/uploads/mlb_rookie_hitting_stats_1000.csv')
soph   = pd.read_csv('/mnt/user-data/uploads/mlb_sophomore_hitting_stats_1000.csv')

merged = rookie.merge(
    soph[['Player_ID','Sophomore_Year','G','AB','R','H','2B','3B','HR','RBI',
          'SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS']],
    on='Player_ID', suffixes=('_r','_s')
)
merged = merged[(merged['AB_s'] > 0) & (merged['OPS_s'] > 0) & (merged['OPS_r'] > 0)].copy()
print(f"Merged & filtered: {len(merged)} players")

lr = LinearRegression().fit(merged[['OPS_r']], merged['OPS_s'])
slope     = lr.coef_[0]
intercept = lr.intercept_
r2        = r2_score(merged['OPS_s'], lr.predict(merged[['OPS_r']]))

merged['predicted_soph_OPS'] = lr.predict(merged[['OPS_r']])
merged['residual']           = merged['OPS_s'] - merged['predicted_soph_OPS']

res_mean = merged['residual'].mean()
res_std  = merged['residual'].std()
threshold = res_mean - 1.0 * res_std   # −1σ below mean residual

merged['jinxed'] = (merged['residual'] < threshold).astype(int)
n_jinxed = merged['jinxed'].sum()

print(f"\n── Linear Regression ──────────────────────────")
print(f"  Equation : Soph_OPS = {slope:.4f} × Rookie_OPS + {intercept:.4f}")
print(f"  R²       : {r2:.4f}")
print(f"  Res mean : {res_mean:.4f}")
print(f"  Res std  : {res_std:.4f}")
print(f"  Threshold: residual < {threshold:.4f}  (mean − 1σ)")
print(f"  Jinxed   : {n_jinxed} / {len(merged)}  ({n_jinxed/len(merged)*100:.1f}%)")

merged['HR_rate']    = (merged['HR_r']  / merged['AB_r']).round(4)
merged['BB_rate']    = (merged['BB_r']  / merged['AB_r']).round(4)
merged['SO_rate']    = (merged['SO_r']  / merged['AB_r']).round(4)
merged['ISO']        = (merged['SLG_r'] - merged['AVG_r']).round(4)
merged['partial']    = (merged['AB_r'] < 300).astype(int)
merged['BABIP']      = ((merged['H_r'] - merged['HR_r']) /
                        (merged['AB_r'] - merged['SO_r'] - merged['HR_r'] + 1)
                       ).clip(0,1).round(4)
merged['SB_rate']    = (merged['SB_r'] / (merged['AB_r']+1)).round(4)
merged['ops_change'] = (merged['OPS_s'] - merged['OPS_r']).round(4)

features    = ['OPS_r','HR_rate','BB_rate','SO_rate','ISO','partial','BABIP','AVG_r','SB_rate']
feat_labels = ['Rookie OPS','HR Rate','BB Rate','SO Rate','ISO (Power)',
               'Partial Season','BABIP','Batting Avg','SB Rate']

df = merged[features + ['jinxed','Player_Name','Rookie_Year',
                         'OPS_r','OPS_s','predicted_soph_OPS','residual',
                         'ops_change','HR_rate','BB_rate','SO_rate','partial','BABIP','ISO','SB_rate']
           ].dropna().copy()
X = df[features].values
y = df['jinxed'].values

print(f"\n── Feature matrix: {X.shape}, jinxed={y.sum()} ({y.mean()*100:.1f}%)")

scaler = StandardScaler()
X_sc   = scaler.fit_transform(X)

model = LogisticRegression(class_weight='balanced', max_iter=2000, random_state=42)
model.fit(X_sc, y)

cv     = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_auc = cross_val_score(model, X_sc, y, cv=cv, scoring='roc_auc')
cv_f1  = cross_val_score(model, X_sc, y, cv=cv, scoring='f1')
cv_acc = cross_val_score(model, X_sc, y, cv=cv, scoring='accuracy')

y_prob = model.predict_proba(X_sc)[:,1]
y_pred = model.predict(X_sc)
cm     = confusion_matrix(y, y_pred)
auc    = roc_auc_score(y, y_prob)
fpr, tpr, _ = roc_curve(y, y_prob)

print(f"\n── Logistic Regression Results ────────────────")
print(f"  Train AUC : {auc:.3f}")
print(f"  CV AUC    : {cv_auc.mean():.3f} ± {cv_auc.std():.3f}")
print(f"  CV F1     : {cv_f1.mean():.3f}")
print(f"  CV Acc    : {cv_acc.mean():.3f}")
print(f"\n  Confusion matrix:\n{cm}")
print(f"\n  Coefficients:")
coefs = sorted(zip(feat_labels, model.coef_[0]), key=lambda x: x[1])
for f,c in coefs:
    print(f"    {f:20s}  coef={c:+.4f}  OR={np.exp(c):.3f}")

df['jinx_prob']        = y_prob
df['predicted_jinxed'] = y_pred

ops_range  = np.linspace(merged['OPS_r'].min()-0.02, merged['OPS_r'].max()+0.02, 80)
reg_line   = slope * ops_range + intercept
jinx_line  = reg_line + threshold

players_out = []
for idx, row in df.iterrows():
    players_out.append({
        'name':    row.Player_Name,
        'year':    int(row.Rookie_Year),
        'ops_r':   round(float(row.OPS_r),   3),
        'ops_s':   round(float(df.at[idx,'OPS_s']),   3),
        'pred':    round(float(row.predicted_soph_OPS), 3),
        'resid':   round(float(row.residual), 4),
        'actual':  int(row.jinxed),
        'predicted': int(row.predicted_jinxed),
        'prob':    round(float(row.jinx_prob),4),
        'hr_rate': round(float(row.HR_rate),  4),
        'bb_rate': round(float(row.BB_rate),  4),
        'so_rate': round(float(row.SO_rate),  4),
        'partial': int(row.partial),
        'babip':   round(float(row.BABIP),    3),
        'iso':     round(float(row.ISO),      3),
        'sb_rate': round(float(row.SB_rate),  4),
        'ops_chg': round(float(row.ops_change),3),
    })

out = {
    'n': int(len(df)), 'n_jinxed': int(y.sum()),
    'pct_jinxed': round(float(y.mean()*100),1),
    'slope': round(float(slope),5), 'intercept': round(float(intercept),5),
    'r2': round(float(r2),4),
    'res_mean': round(float(res_mean),4), 'res_std': round(float(res_std),4),
    'threshold': round(float(threshold),4),
    'auc': round(float(auc),3),
    'cv_auc': round(float(cv_auc.mean()),3), 'cv_auc_std': round(float(cv_auc.std()),3),
    'cv_f1': round(float(cv_f1.mean()),3),   'cv_acc': round(float(cv_acc.mean()),3),
    'intercept_lr': round(float(model.intercept_[0]),4),
    'cm': cm.tolist(),
    'coefs': [{'f':f,'c':round(float(c),4),'or':round(float(np.exp(c)),4)} for f,c in coefs],
    'roc_fpr': [round(float(v),4) for v in fpr[:200]],
    'roc_tpr': [round(float(v),4) for v in tpr[:200]],
    'reg_x':   [round(float(v),4) for v in ops_range],
    'reg_y':   [round(float(v),4) for v in reg_line],
    'jinx_y':  [round(float(v),4) for v in jinx_line],
    'scatter': [{'x':round(float(r.OPS_r),3),'y':round(float(df.at[i,'OPS_s']),3),
                 'j':int(r.jinxed),'n':r.Player_Name,'yr':int(r.Rookie_Year),
                 'chg':round(float(r.ops_change),3)}
                for i,r in df.iterrows()],
    'players': players_out,
}

with open('/tmp/results_1000.json','w') as f:
    json.dump(out, f)
print(f"\nJSON saved, size: {len(json.dumps(out)):,} bytes")
```

<img width="917" height="282" alt="jinx 1000" src="https://github.com/user-attachments/assets/b4b8c02f-90da-42a6-b046-773bb9431d67" />
<img width="902" height="195" alt="jinx pred" src="https://github.com/user-attachments/assets/0ca2be38-d1c9-48b3-a320-3ffba9034402" />
<img width="952" height="682" alt="jinx acc 1000" src="https://github.com/user-attachments/assets/780e29c7-a9d0-4f4e-9246-75a301d68905" />

위의 결과에서 알 수 있듯이, 데이터셋의 크기를 늘렸다고 해서 모델의 정확도가 높아진 것은 아니다. 위양성 비율은 여전히 높고, 정확도는 0.68 정도로 이전과 거의 일치하는 수치이다. 이에 더해, 기존의 결과에서 소포모어 징크스를 겪을 확률을 높이는 피처들이 이번에는 반대로 낮출 확률로 분석되거나 이 반대의 경우도 다수 존재했음을 확인할 수 있다. 결과에 일관된 영향을 미친 피처들은 BB rate(긍정적)와 Rookie OPS(부정적) 두 가지 뿐이었다. 따라서, 이 두 피처들을 제외한 나머지 피처들은 모델의 예측 정확도에 유의미한 영향을 주지 않는다는 결론을 내렸다.

그러므로 classic stat(타율, 홈런 등)이 아닌 modern stat(평균 타구 속도, 베럴 타구 비율 등)이 포함된 데이터셋을 사용하면 해당 피처들은 소포모어 징크스 발현과 유의미한 관계를 갖는지, 또한 모델의 정확도가 올라갈 것인지 확인해보고자 다른 데이터셋으로 다시 모델을 실행해보았다.

모델:
```{python}
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, roc_curve, ConfusionMatrixDisplay)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/mnt/user-data/uploads/mlb_jinx_advanced_data.csv')

(overperformance vs expected)
features = [
    'woba_year1',                       # actual performance level
    'est_woba_year1',                   # skill-based expected performance
    'est_woba_minus_woba_diff_year1',   # luck component (actual - expected)
    'ba_year1',
    'est_ba_minus_ba_diff_year1',       # BA luck
    'slg_year1',
    'est_slg_minus_slg_diff_year1',     # SLG luck
    'barrel_rate_year1',
    'avg_hit_speed_year1',
    'pa_year1',
]

X = df[features]
y = df['is_jinx']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_s, y_train)

y_pred      = model.predict(X_test_s)
y_pred_prob = model.predict_proba(X_test_s)[:, 1]

cv_scores = cross_val_score(model, scaler.fit_transform(X), y, cv=5, scoring='roc_auc')

print("=== Logistic Regression – MLB Jinx Prediction ===")
print(f"\nTest AUC-ROC : {roc_auc_score(y_test, y_pred_prob):.4f}")
print(f"5-Fold CV AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred))

coef_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_[0],
    'Odds Ratio': np.exp(model.coef_[0])
}).sort_values('Coefficient', key=abs, ascending=False)
print("\n--- Feature Coefficients ---")
print(coef_df.to_string(index=False))

np.save('/tmp/fpr.npy', roc_curve(y_test, y_pred_prob)[0])
np.save('/tmp/tpr.npy', roc_curve(y_test, y_pred_prob)[1])
np.save('/tmp/auc.npy', [roc_auc_score(y_test, y_pred_prob)])
coef_df.to_csv('/tmp/coef_df.csv', index=False)
cm = confusion_matrix(y_test, y_pred)
np.save('/tmp/cm.npy', cm)
print("\nArrays saved.")
```

<img width="852" height="288" alt="modern" src="https://github.com/user-attachments/assets/478a875e-78d7-464d-a59f-8e668228569e" />

로지스틱 회귀 모델을 사용한 결과, 정확도가 약 77%정도로 결과가 나왔다. 이는 꽤나 높은 연관성을 보여준다고 할 수 있다. 특히, modern stat인 avg. exit speed(평균 타구 속도)가 더 높을수록 소포모어 징크스를 겪을 확률이 낮을 것으로 예측되는 유의미한 결과를 도출할 수 있었다. 이 결과가 시사하는 바는, 클래식 스탯(타율, 홈런)은 바람, 야수의 판단 실수 등과 같은 운을 내포하고 있기에, 그 선수의 실력을 완전 정확하게 파악하기는 힘들다는 것이다. 거기에 더해서, 1년차때는 보통 분석이 덜 되어있어서 그 선수의 성적이 실력보다 잘 나올 수도 있다. 약점은 감추고, 강점을 살릴 수 있는 기회가 많이 찾아올 수도 있는데, 2년차때는 분석을 당하며 그런 기회가 줄어들고 본 실력이 드러나는 것이다.

그러면 나머지 20%정도의 오차는 왜 발생하였을까? 이는 수치로는 나타낼 수 없는 여러가지 외부 변수들이 많았기 때문이라고 판단이 된다. 타자의 실력과 별개로 작용하는 요인중에는 스트라이크 존의 크기, ABS(자동 투구 판정 시스템)의 도입, 오심, 공인구의 반발력 등등이 존재할 수 있다. 아니면 선수의 부담감, 혹은 자만 등의 심리적인 이유가 있을 수도 있다. 이러한 이유들은 데이터로 반영하기 힘들기 때문에, 보이지 않는 오차로 반영된 것이 아닐까 생각이 든다.


# Conclusion
스포츠 분야에서의 소포모어 징크스가 실제로 존재하는지, 또 어떤 요인들이 징크스를 유발할 수 있는지에 대해 호기심을 가지고 프로젝트를 시작하였다. 처음에는 다소 적은 양의 데이터셋을 이용하여 딥러닝을 실행하였는데, 생각했던 것보다 정확도가 높지 않았고 이를 보완하고자 데이터셋의 양을 대폭 늘려서 다시 모델을 작동했다. 하지만 데이터의 양이 늘어났음에도 오히려 기존의 요인이 반대로 나타나는 등 기대했던 결과가 나오지 않았다. 따라서 데이터셋의 양이 아닌 데이터의 종류를 바꾸는 쪽으로 진행하여 기존의 클래식 스탯 대신 모던 스탯이 다수 포함된 데이터로 최종적인 결과를 도출했다. 결과적으로, 현대 야구에서 수학적인 계산을 바탕으로 구하는 모던 스탯을 분석하였을 때 소포모어 징크스의 요인을 확인하는 것이 훨씬 수월해진다는 것을 알 수 있었다. 물론 최종적인 결과에도 여전히 오차가 존재했는데, 이는 위에도 나열하였듯이 데이터로 수치화하기 어려운 다양한 변수들의 영향이라고 추정하는 것이 타당할 듯 하다. 향후에 유사한 프로젝트를 다시 진행하게 된다면, 여러 방면의 변수들을 최대한 고려하여 이번 프로젝트의 아쉬움을 보완해보고 싶기도 하다.


블로그 영상 링크: https://www.youtube.com/watch?si=qMRE1FgJuHZRThIZ&v=AOp0N254oDw&feature=youtu.be


역할

배경준: 데이터셋 수집, 모델 제작 및 학습
이환: 데이터셋 수집, 모델 제작 및 학습
이승현: 모델 학습 결과 분석, 영상 제작

