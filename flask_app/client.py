import requests
class PlayerBase(object):
    def __init__(self, player_json, offense=[], defense=[], kicker=[], type=0):
        self.player_id = player_json['player']
        self.fname = player_json['fname']
        self.lname = player_json['lname']
        self.pname = player_json['pname']
        self.dpos = player_json['dpos']
        self.col = player_json['col']
        self.fullname = self.fname + " " + self.lname
        self.pos1 = player_json['pos1']
        self.pos2 = player_json['pos2']
        self.height = player_json['height']
        self.jnum = player_json['jnum']
        self.weight = player_json['weight']
        self.dcp = player_json['dcp']
        self.dob = player_json['dob']
        self.defense = defense
        self.kicker = kicker
        self.offense = offense
        self.dv = player_json['dv']
        self.start = player_json['start']
        self.cteam = player_json['cteam']
        self.posd = player_json['posd']
        
        
        
        
        
        self.type = type

    def __repr__(self):
        return self.fullname


class OffenseGame(object):
    def __init__(self, play_style):
        self.player_id = play_style['player']
        self.gid = play_style['gid']
        self.pa = play_style['pa']
        self.pc = play_style['pc']
        self.py = play_style['py']
        self.ints = play_style['ints']
        self.tdp = play_style['tdp']
        self.ra = play_style['ra']
        self.sra = play_style['sra']
        self.ry = play_style['ry']
        self.tdr = play_style['tdr']
        self.trg = play_style['trg']
        self.rec = play_style['rec']
        self.recy = play_style['recy']
        self.tdrec = play_style['tdrec']
        self.ret = play_style['ret']
        self.rety = play_style['rety']
        self.tdret = play_style['tdret']
        self.fuml = play_style['fuml']
        self.peny = play_style['peny']
        self.snp = play_style['snp']
        self.fp = play_style['fp']
        self.fp2 = play_style['fp2']
        self.fp3 = play_style['fp3']
        self.game = play_style['game']
        self.seas = play_style['seas']
        self.year = play_style['year']
        self.team = play_style['team']

    # def __repr__(self):
    #     return self.gid


class DefenseGame(object):
    def __init__(self, play_style):
        self.player_id = play_style['player']
        self.gid = play_style['gid']
        self.solo = play_style['solo']
        self.comb = play_style['comb']
        self.sck = play_style['sck']
        self.saf = play_style['saf']
        self.blk = play_style['blk']
        self.ints = play_style['ints']
        self.pdef = play_style['pdef']
        self.frcv = play_style['frcv']
        self.forc = play_style['forc']
        self.tdd = play_style['tdd']
        self.rety = play_style['rety']
        self.tdret = play_style['tdret']
        self.peny = play_style['peny']
        self.snp = play_style['snp']
        self.fp = play_style['fp']
        self.fp2 = play_style['fp2']
        self.game = play_style['game']
        self.seas = play_style['seas']
        self.year = play_style['year']
        self.team = play_style['team']

    def __repr__(self):
        return self.gid



class PlayerClient(object):
    def __init__(self):
        self.session = requests.Session()
        self.base_url = f'https://api.armchairanalysis.com/v1.1/test'

#This function works to return all the players in the database
    def getAll(self):
        search_url = f'/players?status=active'
        response = self.session.get(self.base_url + search_url)

        if response.status_code != 200:
            return ValueError('URL error')
        else:
            data = response.json()
        d = data['data']

        allPlayers = []
        for each in d:
            allPlayers.append(PlayerBase(each))

        return allPlayers

#This function returns player specific to the selected team
    def get_players_by_team(self, tname):
        player_url = self.base_url + f'/players/{tname}'

        resp = self.session.get(player_url)

        if resp.status_code != 200:
            raise ValueError('Search request failed, make sure proper team name given')
        else:
            d = resp.json()

        all_players_json = d['data']

        allPlayers = []
        for item_json in all_players_json:
            allPlayers.append(PlayerBase(item_json))

        return allPlayers

    def getPlayerByID(self, player_id):
        url = self.base_url + f'/player/{player_id}'

        resp = self.session.get(url)

        if resp.status_code != 200:
            raise ValueError('Search request failed, make sure proper Player_Id given')


        basic = resp.json()['data']
        flag = []
        style = []
        if self.session.get(url + f'/offense').status_code == 200:
           
            records = self.session.get(url + f'/offense').json()['data']
            for rec in records:
                style.append(OffenseGame(rec))
            player = PlayerBase(basic, offense=style, defense=[], kicker=[], type=1)
            return player

        elif self.session.get(url + f'/defense').status_code == 200:
            records = self.session.get(url + f'/defense').json()['data']
            for rec in records:
                style.append(DefenseGame(rec))

            
            player = PlayerBase(basic, offense=[], defense=style, kicker=[], type=2)
            return player
        
        elif self.session.get(url).status_code == 200:
            records = self.session.get(url).json()['data']

            
            player = PlayerBase(basic, offense=[], defense=[], kicker=style, type=3)
            return player

        



