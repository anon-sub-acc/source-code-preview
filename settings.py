valid_chars = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11,
               'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21,
               'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26, '0': 27, '1': 28, '2': 29, '3': 30, '4': 31,
               '5': 32, '6': 33, '7': 34, '8': 35, '9': 36, '-': 37, '_': 38, '.': 39}

group_map = {0: 'benign', 1: 'bamital', 2: 'banjori', 3: 'bazarloader', 4: 'bedep', 5: 'beebone', 6: 'blackhole',
             7: 'bobax', 8: 'ccleaner', 9: 'chaes', 10: 'chinad', 11: 'chir', 12: 'conficker', 13: 'corebot',
             14: 'cryptolocker', 15: 'darkshell', 16: 'darkwatchman', 17: 'diamondfox', 18: 'dircrypt', 19: 'dmsniff',
             20: 'dnsbenchmark', 21: 'dnschanger', 22: 'downloader', 23: 'dyre', 24: 'ebury', 25: 'ekforward',
             26: 'emotet', 27: 'enviserv', 28: 'feodo', 29: 'flubot', 30: 'fobber', 31: 'g01', 32: 'gameover',
             33: 'gameover_p2p', 34: 'gozi', 35: 'goznym', 36: 'gspy', 37: 'hesperbot', 38: 'infy', 39: 'kingminer',
             40: 'locky', 41: 'm0yv', 42: 'm0yvtdd', 43: 'madmax', 44: 'makloader', 45: 'matsnu', 46: 'mirai',
             47: 'modpack', 48: 'monerominer', 49: 'murofet', 50: 'murofetweekly', 51: 'mydoom', 52: 'necro',
             53: 'necurs', 54: 'nymaim', 55: 'nymaim2', 56: 'oderoor', 57: 'omexo', 58: 'padcrypt', 59: 'pandabanker',
             60: 'phorpiex', 61: 'pitou', 62: 'proslikefan', 63: 'pushdo', 64: 'pushdotid', 65: 'pykspa', 66: 'pykspa2',
             67: 'pykspa2s', 68: 'qadars', 69: 'qakbot', 70: 'qhost', 71: 'qsnatch', 72: 'ramdo', 73: 'ramnit',
             74: 'ranbyus', 75: 'randomloader', 76: 'redyms', 77: 'rovnix', 78: 'sharkbot', 79: 'shifu', 80: 'simda',
             81: 'sisron', 82: 'sphinx', 83: 'suppobox', 84: 'sutra', 85: 'symmi', 86: 'szribi', 87: 'tempedreve',
             88: 'tempedrevetdd', 89: 'tinba', 90: 'tinynuke', 91: 'tofsee', 92: 'torpig', 93: 'tsifiri', 94: 'ud2',
             95: 'ud3', 96: 'ud4', 97: 'urlzone', 98: 'vawtrak', 99: 'vidro', 100: 'vidrotid', 101: 'virut',
             102: 'volatilecedar', 103: 'wd', 104: 'xshellghost', 105: 'xxhex', 106: 'zloader'}

tlds = {'': 0, '3utilities.com': 1, 'ac': 2, 'ad': 3, 'ae': 4, 'af': 5, 'ag': 6, 'ai': 7, 'al': 8, 'am': 9, 'aq': 10,
        'at': 11, 'ax': 12, 'az': 13, 'bar': 14, 'be': 15, 'bg': 16, 'bid': 17, 'biz': 18, 'blackfriday': 19, 'bm': 20,
        'bounceme.net': 21, 'br': 22, 'bs': 23, 'bt': 24, 'by': 25, 'bz': 26, 'ca': 27, 'cc': 28, 'cd': 29, 'cf': 30,
        'ch': 31, 'click': 32, 'club': 33, 'cm': 34, 'cn': 35, 'co': 36, 'co.ck': 37, 'co.fk': 38, 'co.id': 39,
        'co.il': 40, 'co.in': 41, 'co.ls': 42, 'co.rs': 43, 'co.th': 44, 'co.uk': 45, 'co.za': 46, 'co.zm': 47,
        'co.zw': 48, 'com': 49, 'com.ar': 50, 'com.br': 51, 'com.cy': 52, 'com.do': 53, 'com.eg': 54, 'com.fj': 55,
        'com.ge': 56, 'com.gu': 57, 'com.kh': 58, 'com.km': 59, 'com.lb': 60, 'com.lr': 61, 'com.my': 62, 'com.pf': 63,
        'com.ps': 64, 'com.py': 65, 'com.sv': 66, 'com.tr': 67, 'com.ua': 68, 'com.uy': 69, 'com.ve': 70, 'cw': 71,
        'cx': 72, 'cyou': 73, 'cz': 74, 'date': 75, 'ddns.net': 76, 'ddnsking.com': 77, 'de': 78, 'dk': 79,
        'dnsalias.com': 80, 'doesntexist.com': 81, 'dynalias.com': 82, 'dyndns.org': 83, 'dynu.net': 84, 'dz': 85,
        'ec': 86, 'ee': 87, 'email': 88, 'es': 89, 'eu': 90, 'feedback': 91, 'fi': 92, 'fm': 93, 'fr': 94, 'ga': 95,
        'gd': 96, 'gdn': 97, 'gen.in': 98, 'gg': 99, 'github.io': 100, 'gl': 101, 'gotdns.ch': 102, 'gq': 103,
        'gr': 104, 'gs': 105, 'gy': 106, 'hk': 107, 'hk.org': 108, 'hm': 109, 'hn': 110, 'hopto.org': 111, 'host': 112,
        'hosting': 113, 'ht': 114, 'icu': 115, 'id': 116, 'im': 117, 'in': 118, 'info': 119, 'io': 120, 'ir': 121,
        'it': 122, 'je': 123, 'jp': 124, 'ke': 125, 'kg': 126, 'ki': 127, 'kim': 128, 'kn': 129, 'kr': 130, 'kz': 131,
        'la': 132, 'lc': 133, 'li': 134, 'live': 135, 'lk': 136, 'lv': 137, 'ly': 138, 'md': 139, 'me': 140,
        'me.uk': 141, 'men': 142, 'ml': 143, 'mn': 144, 'mo': 145, 'mobi': 146, 'monster': 147, 'ms': 148, 'mu': 149,
        'mv': 150, 'mx': 151, 'myftp.biz': 152, 'myftp.org': 153, 'myvnc.com': 154, 'name': 155, 'net': 156,
        'news': 157, 'nf': 158, 'ng': 159, 'nl': 160, 'nr': 161, 'nu': 162, 'onion': 163, 'online': 164,
        'onthewifi.com': 165, 'org': 166, 'pa': 167, 'pe': 168, 'ph': 169, 'pk': 170, 'pl': 171, 'pm': 172, 'pro': 173,
        'ps': 174, 'pw': 175, 'qa': 176, 're': 177, 'redirectme.net': 178, 'rent': 179, 'ro': 180, 'rocks': 181,
        'rs': 182, 'ru': 183, 'ru.net': 184, 'sc': 185, 'se': 186, 'servebeer.com': 187, 'serveblog.net': 188,
        'servecounterstrike.com': 189, 'serveftp.com': 190, 'servegame.com': 191, 'servehalflife.com': 192,
        'servehttp.com': 193, 'serveirc.com': 194, 'serveminecraft.net': 195, 'servemp3.com': 196, 'servepics.com': 197,
        'servequake.com': 198, 'sg': 199, 'sh': 200, 'shop': 201, 'site': 202, 'so': 203, 'space': 204, 'st': 205,
        'store': 206, 'su': 207, 'support': 208, 'sx': 209, 'sytes.net': 210, 'tc': 211, 'tech': 212, 'tel': 213,
        'tf': 214, 'tickets': 215, 'tj': 216, 'tk': 217, 'tl': 218, 'tm': 219, 'to': 220, 'today': 221, 'top': 222,
        'tt': 223, 'tv': 224, 'tw': 225, 'ua': 226, 'ug': 227, 'uk': 228, 'us': 229, 'uy.com': 230, 'uz': 231,
        'vg': 232, 'vn': 233, 'vu': 234, 'webhop.me': 235, 'website': 236, 'wf': 237, 'win': 238, 'work': 239,
        'ws': 240, 'wtf': 241, 'xxx': 242, 'xyz': 243, 'yt': 244, 'zapto.org': 245}

DS_MODELS_PATH = "./datasets/mod.pkl"
DS_EXPLAINABILITY_PATH = "./datasets/ex.pkl"

maxlen = 253
max_features = len(valid_chars) + 1
nb_classes = len(group_map)
class_weighting_power = 0.2
