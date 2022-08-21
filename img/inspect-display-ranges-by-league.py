"""Examine the display ranges by league, as well as each league's plot.

@author: Ross Drucker
"""
import sportypy.surfaces.baseball as baseball
import sportypy.surfaces.basketball as basketball
import sportypy.surfaces.curling as curling
import sportypy.surfaces.football as football
import sportypy.surfaces.hockey as hockey
import sportypy.surfaces.soccer as soccer
import sportypy.surfaces.tennis as tennis

# Baseball --------------------------------------------------------------------
little_league = baseball.LittleLeagueField()
little_league.draw()
little_league.draw(display_range = "infield")

milb = baseball.MiLBField()
milb.draw()
milb.draw(display_range = "infield")

mlb = baseball.MLBField()
mlb.draw()
mlb.draw(display_range = "infield")

ncaa = baseball.NCAAField()
ncaa.draw()
ncaa.draw(display_range = "infield")

nfhs = baseball.NFHSField()
nfhs.draw()
nfhs.draw(display_range = "infield")

pony = baseball.PonyField()
pony.draw()
pony.draw(display_range = "infield")

# Basketball ------------------------------------------------------------------
fiba = basketball.FIBACourt()
fiba.draw()
fiba.draw(display_range = "offense")
fiba.draw(display_range = "defense")
fiba.draw(display_range = "offensive key")
fiba.draw(display_range = "defensive key")
fiba.draw(display_range = "offensive lane")
fiba.draw(display_range = "defensive lane")

nba = basketball.NBACourt()
nba.draw()
nba.draw(display_range = "offense")
nba.draw(display_range = "defense")
nba.draw(display_range = "offensive key")
nba.draw(display_range = "defensive key")
nba.draw(display_range = "offensive lane")
nba.draw(display_range = "defensive lane")

gleague = basketball.NBAGLeagueCourt()
gleague.draw()
gleague.draw(display_range = "offense")
gleague.draw(display_range = "defense")
gleague.draw(display_range = "offensive key")
gleague.draw(display_range = "defensive key")
gleague.draw(display_range = "offensive lane")
gleague.draw(display_range = "defensive lane")

ncaa = basketball.NCAACourt()
ncaa.draw()
ncaa.draw(display_range = "offense")
ncaa.draw(display_range = "defense")
ncaa.draw(display_range = "offensive key")
ncaa.draw(display_range = "defensive key")
ncaa.draw(display_range = "offensive lane")
ncaa.draw(display_range = "defensive lane")

nfhs = basketball.NFHSCourt()
nfhs.draw()
nfhs.draw(display_range = "offense")
nfhs.draw(display_range = "defense")
nfhs.draw(display_range = "offensive key")
nfhs.draw(display_range = "defensive key")
nfhs.draw(display_range = "offensive lane")
nfhs.draw(display_range = "defensive lane")

wnba = basketball.WNBACourt()
wnba.draw()
wnba.draw(display_range = "offense")
wnba.draw(display_range = "defense")
wnba.draw(display_range = "offensive key")
wnba.draw(display_range = "defensive key")
wnba.draw(display_range = "offensive lane")
wnba.draw(display_range = "defensive lane")

# Curling ---------------------------------------------------------------------
wcf = curling.WCFSheet()
wcf.draw()
wcf.draw(display_range = "house")

# Football --------------------------------------------------------------------
cfl = football.CFLField()
cfl.draw()
cfl.draw(display_range = "offense")
cfl.draw(display_range = "defense")
cfl.draw(display_range = "red zone")
cfl.draw(display_range = "dredzone")

ncaa = football.NCAAField()
ncaa.draw()
ncaa.draw(display_range = "offense")
ncaa.draw(display_range = "defense")
ncaa.draw(display_range = "red zone")
ncaa.draw(display_range = "dredzone")

nfhs11 = football.NFHSField(n_players = 11)
nfhs11.draw()
nfhs11.draw(display_range = "offense")
nfhs11.draw(display_range = "defense")
nfhs11.draw(display_range = "red zone")
nfhs11.draw(display_range = "dredzone")

nfhs9 = football.NFHSField(n_players = 9)
nfhs9.draw()
nfhs9.draw(display_range = "offense")
nfhs9.draw(display_range = "defense")
nfhs9.draw(display_range = "red zone")
nfhs9.draw(display_range = "dredzone")

nfhs8 = football.NFHSField(n_players = 8)
nfhs8.draw()
nfhs8.draw(display_range = "offense")
nfhs8.draw(display_range = "defense")
nfhs8.draw(display_range = "red zone")
nfhs8.draw(display_range = "dredzone")

nfhs6 = football.NFHSField(n_players = 6)
nfhs6.draw()
nfhs6.draw(display_range = "offense")
nfhs6.draw(display_range = "defense")
nfhs6.draw(display_range = "red zone")
nfhs6.draw(display_range = "dredzone")

nfl = football.NFLField()
nfl.draw()
nfl.draw(display_range = "offense")
nfl.draw(display_range = "defense")
nfl.draw(display_range = "red zone")
nfl.draw(display_range = "dredzone")

# Hockey ----------------------------------------------------------------------
ahl = hockey.AHLRink()
ahl.draw()
ahl.draw(display_range = "offense")
ahl.draw(display_range = "defense")
ahl.draw(display_range = "nzone")
ahl.draw(display_range = "ozone")
ahl.draw(display_range = "dzone")

echl = hockey.ECHLRink()
echl.draw()
echl.draw(display_range = "offense")
echl.draw(display_range = "defense")
echl.draw(display_range = "nzone")
echl.draw(display_range = "ozone")
echl.draw(display_range = "dzone")

iihf = hockey.IIHFRink()
iihf.draw()
iihf.draw(display_range = "offense")
iihf.draw(display_range = "defense")
iihf.draw(display_range = "nzone")
iihf.draw(display_range = "ozone")
iihf.draw(display_range = "dzone")

phf = hockey.PHFRink()
phf.draw()
phf.draw(display_range = "offense")
phf.draw(display_range = "defense")
phf.draw(display_range = "nzone")
phf.draw(display_range = "ozone")
phf.draw(display_range = "dzone")

ncaa = hockey.NCAARink()
ncaa.draw()
ncaa.draw(display_range = "offense")
ncaa.draw(display_range = "defense")
ncaa.draw(display_range = "nzone")
ncaa.draw(display_range = "ozone")
ncaa.draw(display_range = "dzone")

nhl = hockey.NHLRink()
nhl.draw()
nhl.draw(display_range = "offense")
nhl.draw(display_range = "defense")
nhl.draw(display_range = "nzone")
nhl.draw(display_range = "ozone")
nhl.draw(display_range = "dzone")

ohl = hockey.OHLRink()
ohl.draw()
ohl.draw(display_range = "offense")
ohl.draw(display_range = "defense")
ohl.draw(display_range = "nzone")
ohl.draw(display_range = "ozone")
ohl.draw(display_range = "dzone")

qmjhl = hockey.QMJHLRink()
qmjhl.draw()
qmjhl.draw(display_range = "offense")
qmjhl.draw(display_range = "defense")
qmjhl.draw(display_range = "nzone")
qmjhl.draw(display_range = "ozone")
qmjhl.draw(display_range = "dzone")

nwhl = hockey.NWHLRink()
nwhl.draw()
nwhl.draw(display_range = "offense")
nwhl.draw(display_range = "defense")
nwhl.draw(display_range = "nzone")
nwhl.draw(display_range = "ozone")
nwhl.draw(display_range = "dzone")

ushl = hockey.USHLRink()
ushl.draw()
ushl.draw(display_range = "offense")
ushl.draw(display_range = "defense")
ushl.draw(display_range = "nzone")
ushl.draw(display_range = "ozone")
ushl.draw(display_range = "dzone")

# Soccer ----------------------------------------------------------------------
epl = soccer.EPLPitch()
epl.draw()
epl.draw(display_range = "offense")
epl.draw(display_range = "defense")

fifa = soccer.FIFAPitch()
fifa.draw()
fifa.draw(display_range = "offense")
fifa.draw(display_range = "defense")

mls = soccer.MLSPitch()
mls.draw()
mls.draw(display_range = "offense")
mls.draw(display_range = "defense")

ncaa = soccer.NCAAPitch()
ncaa.draw()
ncaa.draw(display_range = "offense")
ncaa.draw(display_range = "defense")

nwsl = soccer.NWSLPitch()
nwsl.draw()
nwsl.draw(display_range = "offense")
nwsl.draw(display_range = "defense")

# Tennis ----------------------------------------------------------------------
atp = tennis.ATPCourt()
atp.draw()
atp.draw(display_range = "serve")
atp.draw(display_range = "receive")

ita = tennis.ITACourt()
ita.draw()
ita.draw(display_range = "serve")
ita.draw(display_range = "receive")

itf = tennis.ITFCourt()
itf.draw()
itf.draw(display_range = "serve")
itf.draw(display_range = "receive")

ncaa = tennis.NCAACourt()
ncaa.draw()
ncaa.draw(display_range = "serve")
ncaa.draw(display_range = "receive")

usta = tennis.USTACourt()
usta.draw()
usta.draw(display_range = "serve")
usta.draw(display_range = "receive")

wta = tennis.WTACourt()
wta.draw()
wta.draw(display_range = "serve")
wta.draw(display_range = "receive")
