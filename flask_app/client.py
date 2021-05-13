import requests

class mainClient(object):
    def __init__(self):
        self.session = requests.Session()
        self.base_url = f'https://api.armchairanalysis.com/v1.1/test'

#This function works to return all the players in the database
    def getAll(self):
        search_url = f'/players?status=active'
        response = self.session.get(self.base_url + search_url)

        if response.status_code != 200:
            return ValueError('Wrong URL has been provided')
        else:
            data = response.json()
        d = data['data']

        allPlayers = []
        for each in d:
            allPlayers.append(mainPlayer(each))

        return allPlayers

#This function returns player specific to the selected team
    def get_players_by_team(self, tname):
        player_url = self.base_url + f'/players/{tname}'

        resp = self.session.get(player_url)
        d = resp.json()

        all_players_json = d['data']

        allPlayers = []
        for item_json in all_players_json:
            allPlayers.append(mainPlayer(item_json))

        return allPlayers

    def getPlayerByID(self, player_id):
        url = self.base_url + f'/player/{player_id}'

        resp = self.session.get(url)

        if resp.status_code != 200:
            raise ValueError('Player ID was incorrect')


        info = resp.json()['data']
        flag = []
        style = []
        if self.session.get(url + f'/offense').status_code == 200:
           
            records = self.session.get(url + f'/offense').json()['data']
            for rec in records:
                style.append(oStyle(rec))
            player = mainPlayer(info, oStyle=style, dStyle=[],type=1)
            return player

        elif self.session.get(url + f'/defense').status_code == 200:
            records = self.session.get(url + f'/defense').json()['data']
            for rec in records:
                style.append(dStyle(rec))

            
            player = mainPlayer(info, oStyle=[], dStyle=style, type=2)
            return player
        
        elif self.session.get(url).status_code == 200:
            records = self.session.get(url).json()['data']

            
            player = mainPlayer(info, oStyle=[], dStyle=[], type=3)
            return player


class mainPlayer(object):
    def __init__(self, info, oStyle=[], dStyle=[], type=0):
        self.player_id = info['player']
        self.fname = info['fname']
        self.lname = info['lname']
        self.pname = info['pname']
        self.dpos = info['dpos']
        self.col = info['col']
        
        self.height = info['height']
        self.fullname = self.fname + " " + self.lname
      
        self.dcp = info['dcp']
        self.dob = info['dob']
        self.dStyle = dStyle
        self.oStyle = oStyle
        self.pos1 = info['pos1']
        self.pos2 = info['pos2']
        self.jnum = info['jnum']
        self.weight = info['weight']
        self.dv = info['dv']
        self.start = info['start']
        self.cteam = info['cteam']
        self.posd = info['posd']
        self.type = type

    def __repr__(self):
        return self.fullname


class dStyle(object):
    def __init__(self, play_style):
        self.player_id = play_style['player']
        self.gid = play_style['gid']
        self.solo = play_style['solo']
        self.comb = play_style['comb']
        self.sck = play_style['sck']
        self.saf = play_style['saf']
        self.blk = play_style['blk']
        self.rety = play_style['rety']
        self.fp2 = play_style['fp2']
        self.tdret = play_style['tdret']
        
        self.snp = play_style['snp']
        self.fp = play_style['fp']
        self.game = play_style['game']
        self.ints = play_style['ints']
        self.pdef = play_style['pdef']
        self.frcv = play_style['frcv']
        self.forc = play_style['forc']
        self.tdd = play_style['tdd']
        self.peny = play_style['peny']
        self.year = play_style['year']
        self.team = play_style['team']
        
        
        self.seas = play_style['seas']

class oStyle(object):
    def __init__(self, play_style):
        self.player_id = play_style['player']
        self.gid = play_style['gid']
        self.fp2 = play_style['fp2']
        self.seas = play_style['seas']
        self.tdret = play_style['tdret']
        self.fuml = play_style['fuml']
        self.fp3 = play_style['fp3']
        self.pa = play_style['pa']
        self.pc = play_style['pc']
        self.py = play_style['py']
        self.ints = play_style['ints']
        self.tdp = play_style['tdp']
        self.ra = play_style['ra']
        self.ret = play_style['ret']
        self.rety = play_style['rety']
        self.year = play_style['year']
        self.team = play_style['team']
        self.trg = play_style['trg']
        self.rec = play_style['rec']
        self.recy = play_style['recy']
        self.tdrec = play_style['tdrec']
        self.sra = play_style['sra']
        self.ry = play_style['ry']
        self.tdr = play_style['tdr']
        self.game = play_style['game']
        self.peny = play_style['peny']
        self.snp = play_style['snp']
        self.fp = play_style['fp']



        





        



