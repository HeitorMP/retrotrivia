# Simple Quiz Game Engine in PyGame
# for Batocera Retrotrivia
# lbrpdx - 2020/2021
# https://github.com/lbrpdx/retrotrivia
# License: LGPL 3.0
import xml.etree.ElementTree as ET
import random
import os

BASEPATH  = '/userdata/roms/'
XML       = '/gamelist.xml'
MIN_GAMES = 10   # Don't index if fewer than this
MAX_GAMES = 5000 # Don't index full sets
SYSTEMS   = [  '3do', '3ds', 'amiga1200', 'amiga500', 'amigacd32', 'amigacdtv', 'amstradcpc', 'apple2', 'atari2600', 'atari5200', 'atari7800', 'atari800', 'atarist', 'atomiswave', 'c128', 'c20', 'c64', 'channelf', 'colecovision', 'daphne', 'dos', 'dreamcast', 'easyrpg', 'fbneo', 'fds', 'flash', 'fmtowns', 'fpinball', 'gameandwatch', 'gamecube', 'gamegear', 'gb', 'gba', 'gbc', 'gx4000', 'intellivision', 'jaguar', 'lutro', 'lynx', 'mame', 'mastersystem', 'megadrive', 'model3', 'msx', 'msx1', 'msx2', 'msx2+', 'msxturbor', 'mugen', 'n64', 'naomi', 'nds', 'neogeo', 'neogeocd', 'nes', 'ngp', 'ngpc', 'o2em', 'openbor', 'pc88', 'pc98', 'pcengine', 'pcenginecd', 'pcfx', 'pico8', 'pokemini', 'ports', 'prboom', 'ps2', 'ps3', 'psp', 'psx', 'satellaview', 'saturn', 'scummvm', 'sega32x', 'segacd', 'sg1000', 'snes', 'solarus', 'sufami', 'supervision', 'supergrafx', 'thomson', 'tic80', 'vectrex', 'virtualboy', 'wii', 'wiiu', 'windows', 'wswan', 'wswanc', 'x1', 'xbox', 'x68000', 'zx81', 'zxspectrum' ]

class gamelist:
    def __init__(self):
        self.Q = []
        self.systems = SYSTEMS

    def load(self, system):
        q = []
        if not os.path.isfile(BASEPATH+system+XML):
            return q
        try:
            self.tree = ET.parse(BASEPATH+system+XML)
        except Exception as e:
            print("Warning: unable to load {}/gamelist.xml".format(system))
            return q
        root = self.tree.getroot()
        setgames = set()
        for item in root.findall('game/name'):
            short=item.text.split('(')[0] # Remove (USA, Europe...)
            setgames.add(short.rstrip(' '))
        allgames = [n for n in setgames]
        if len(allgames) < MIN_GAMES:
            return q
        indexed_games = 0
        for item in root.findall('game'):
            vid = item.find('video')
            file_vid = False
            if vid is not None:
                v = vid.text
                try:
                    if os.path.isfile(BASEPATH+system+'/'+v):
                        file_vid = True
                    else:
                        pass
                except:
                    pass
                if file_vid:
                    name = item.find('name')
                    n = name.text.split('(')[0].rstrip(' ')
                    it = list(range(4))
                    it = [i+1 for i in it]
                    random.shuffle(it)
                    possval = random.sample(allgames, 5)
                    if n in possval:
                        possval.remove(n)
                    res = n, possval[0], possval[1], possval[2]
                    line = [ BASEPATH+system+'/'+v, it[0], '', '', '', '']
                    for i in list (range(4)):
                        line[1+it[i]]=res[i]
                    out = tuple(line)
                    q.append(out)
                    indexed_games += 1
                    if indexed_games >= MAX_GAMES:
                        return q
        return q

    def load_all(self):
        for sys in self.systems:
            self.Q.append(self.load(sys))
        return self.Q

    def show(self):
        for item in self.Q:
            print (item)

if __name__ == '__main__':
    gl = gamelist()
    gl.load_all()
    gl.show()
