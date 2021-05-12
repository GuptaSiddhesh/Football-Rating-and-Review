import requests
class PlayerBase(object):
    def __init__(self, player_json, offense=[], defense=[], kicker=[], flags=[]):
        self.player_id = player_json['player']
        self.fname = player_json['fname']
        self.lname = player_json['lname']
        self.pname = player_json['pname']
        self.fullname = self.fname + " " + self.lname
        self.pos1 = player_json['pos1']
        self.pos2 = player_json['pos2']
        self.height = player_json['height']
        self.weight = player_json['weight']
        self.dob = player_json['dob']
        self.dpos = player_json['dpos']
        self.col = player_json['col']
        self.dv = player_json['dv']
        self.start = player_json['start']
        self.cteam = player_json['cteam']
        self.posd = player_json['posd']
        self.jnum = player_json['jnum']
        self.dcp = player_json['dcp']
        self.offense = offense
        self.defense = defense
        self.kicker = kicker
        self.flags = flags

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

    def __repr__(self):
        return self.gid


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


class KickerGame(object):
    def __init__(self, play_style):
        self.player_id = play_style['player']
        self.gid = play_style['gid']
        self.pat = play_style['pat']
        self.fgs = play_style['fgs']
        self.fgm = play_style['fgm']
        self.fgl = play_style['fgl']
        self.fp = play_style['fp']
        self.game = play_style['game']
        self.seas = play_style['seas']
        self.year = play_style['year']
        self.team = play_style['team']

    def __repr__(self):
        return self.gid


class PlayerClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = f'https://api.armchairanalysis.com/v1.1/test'

    def all_players(self):
        search_url = f'/players?status=active'
        resp = self.sess.get(self.base_url + search_url)

        if resp.status_code != 200:
            return ValueError('URL error')

        data = resp.json()

        all_players_json = data['data']

        result = []

        for item_json in all_players_json:
            result.append(PlayerBase(item_json))

        return result

    def get_players_by_team(self, tname):
        player_url = self.base_url + f'/players/{tname}'

        resp = self.sess.get(player_url)

        if resp.status_code != 200:
            raise ValueError('Search request failed, make sure proper team name given')

        data = resp.json()

        all_players_json = data['data']

        result = []

        for item_json in all_players_json:
            result.append(PlayerBase(item_json))

        return result

    def retrieve_player_by_id(self, player_id):
        player_url = self.base_url + f'/player/{player_id}'

        resp = self.sess.get(player_url)

        if resp.status_code != 200:
            raise ValueError('Search request failed, make sure proper Player_Id given')
        data = resp.json()
        basic = data['data']

        flag = []
        offense = []
        defense = []
        kicker = []

        offense_url = player_url + f'/offense'
        resp = self.sess.get(offense_url)
        if resp.status_code == 200:
            flag.append(1)
            games_json = resp.json()['data']
            for game_json in games_json:
                offense.append(OffenseGame(game_json))

        defense_url = player_url + f'/defense'
        resp = self.sess.get(defense_url)
        if resp.status_code == 200:
            flag.append(2)
            games_json = resp.json()['data']
            for game_json in games_json:
                defense.append(DefenseGame(game_json))

        kicker_url = player_url + f'/kickers'
        resp = self.sess.get(kicker_url)
        if resp.status_code == 200:
            flag.append(3)
            games_json = resp.json()['data']
            for game_json in games_json:
                kicker.append(KickerGame(game_json))

        player = PlayerBase(basic, offense=offense, defense=defense, kicker=kicker, flags=flag)
        return player

    def retrieve_player_by_name(self, player_fname, player_lname):
        player_url = self.base_url + f'/player/:{player_fname}_{player_lname}'
        print(player_fname + player_lname)
        resp = self.sess.get(player_url)

        if resp.status_code != 200:
            # raise ValueError('Search request failed, make sure proper Player Name given')
            return resp.json()
        data = resp.json()
        basic = data['data'][0]
        return basic['player']


