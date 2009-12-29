#!/usr/bin/python

from optparse import OptionParser

DEBUG = False
ALGO  = True

def debug(message):
  global DEBUG
  if DEBUG:
    print "DEBUG: " + message

def algo(message):
  global ALGO
  print "ALGORITMUS: " + message

class PureStrategy:
  """Reprezentuje jednu ryzi strategii, coz je de facto jen jednoducha dvojice"""
  """Ale buhvi co bude potreba aby umela"""

  def __init__(self, payoffA, payoffB):
    debug("Vytvareni strategie [%s,%s]" % (payoffA, payoffB))
    self.payoffA = payoffA
    self.payoffB = payoffB

  def getNegative(self):
    """Vraci nejnizsi payoff, pokud je negativni"""
    """Je to potreba pro preprocessing"""
    if self.payoffA < 0 or self.payoffB < 0:
      return abs(min(self.payoffA, self.payoffB))
    else:
      return 0

class TwoPlayerGame:
  """Reprezentuje jednu dvouhracovou hru"""

  def __init__(self, stratsA, stratsB, name="Game"):
    """Jen inicializuje pocty strategii a jmeno"""

    if stratsA < 2 or stratsB < 2:
      raise ValueError, "Not really a game: each player should have at least 2 strategies"
    else:
      self.stratsA = stratsA
      self.stratsB = stratsB
      self.name = name
      self.slack = 0

      debug("Vytvorena hra %s: %s/%s strategii" % (name, stratsA, stratsB))

  def loadMatrices(self, first, second):
    """Z dodanych matic vytvori jednu, jejiz cleny jsou PureStrategy"""
    """Ocekava spravnou velikost matic, jinak haze ValueError"""

    # pokud nemame spravny pocet radku
    if len(first) != self.stratsA or len(second) != self.stratsA:
      raise ValueError, "Matrices do not have proper number of lines"

    # rovnou vytvorit matici timhle osklivym list comprehension
    # pokud dostanem IndexError, nemame spravny pocer radku
    try:
      self.matrix   = [ [PureStrategy(first[y][x],second[y][x]) for x in range(self.stratsB)] for y in range(self.stratsA) ]

    except IndexError:
      raise ValueError, "Matrice do not have proper number of columns"

    debug("Do hry %s byly nahrany matice" % self.name)

  def printGame(self):
    """Vypise hru primo pomoci print"""

    print "Game name: %s" % self.name
    print "Strategies: A=%s, B=%s" % (self.stratsA, self.stratsB)
    for i in range(self.stratsA):
      for j in range(self.stratsB):
        strat = self.matrix[i][j]
        print "[%s:%s] " % (strat.payoffA, strat.payoffB),
      print "\n",

  def positivize(self):
    """Vytvori strategicky ekvivalentni hru, pokud mame nejake negativni payoff"""
    """Lemke-Howson neumi negativni payoff, takze musime pricist takove A, aby"""
    """vsechny payoff byly >= 0"""

    slack = 0

    # najdeme nejnizsi negativni hodnotu
    for i in range(self.stratsA):
      for j in range(self.stratsB):
        slack = max(slack, self.matrix[i][j].getNegative())

    # pokud jsme nejakou nasli, tak jeji abs proste pricteme ke vsem payoff
    if slack > 0:
      self.slack = slack
      algo("Nejnizsi negativni uzitek je -%s: pricteme ho k cele hre" % slack)
      for i in range(self.stratsA):
        for j in range(self.stratsB):
          self.matrix[i][j].payoffA += slack
          self.matrix[i][j].payoffB += slack

  def unslack(self):
    """Vrati hru do puvodniho stavu pred prictenim konstanty pro odnegativizaci"""
    for i in range(self.stratsA):
      for j in range(self.stratsB):
        self.matrix[i][j].payoffA -= self.slack
        self.matrix[i][j].payoffB -= self.slack

  def _payoffs(self, player, strategy):
    """Vraci vektor payoffu pro hrace a urcitou strategii"""
    """Je potreba pri eliminaci dominovanych strategii"""

    if player == "A":
      ret = [ self.matrix[strategy][x].payoffA for x in range(self.stratsB) ]
    else:
      ret = [ self.matrix[x][strategy].payoffB for x in range(self.stratsA) ]

    return ret

  def AStrategyDominates(self, first, second):
    """Vraci True, pokud strategie s indexem first ostre dominuje tu s indexem second"""
    """Pro strategie prvniho hrace"""

    fir = self._payoffs("A", first)
    sec = self._payoffs("A", second)

    for i in range(self.stratsB):
      # pokud je druhy payoff vyssi nebo stejny, nemuze dominovat, koncime
      if sec[i] >= fir[i]:
        return False

    return True

  def BStrategyDominates(self, first, second):
    """Vraci True, pokud strategie s indexem first ostre dominuje tu s indexem second"""
    """Pro strategie druheho hrace"""

    fir = self._payoffs("B", first)
    sec = self._payoffs("B", second)

    for i in range(self.stratsA):
      # pokud je druhy payoff vyssi nebo stejny, nemuze dominovat, koncime
      if sec[i] >= fir[i]:
        return False

    return True

  def eliminate(self):
    """Eliminace dominovanych strategii"""
    """Mely by se eliminovat i strategie dominovane smisenymi strategiemi"""
    """Ale netusim, jak to v rozumnem case provest, takze jen pro ryzi"""
    """Vraci True, pokud zustala jen jedina strategie = ekvilibrium"""

    removed = True
    # pokud jsme v minulem prubehu odstranili strategii, zkusime to znova
    while removed:
      removed = False
      kick = None

      # vyzkousime vsechny pary. O(x^2) :(
      # TODO: zajimalo by me, jestli to jde lip
      # NOTE: teoreticky O(x * log x), ale zase bych musel porovnavat 2x v kazdem kroku
      for i in range(self.stratsA):
        for j in range(self.stratsA):
          if self.AStrategyDominates(i, j):
            algo("Hrac 1: strategie %s je dominovana strategii %s" % (j, i))
            # kick je dominovana strategie
            kick = j
            break # z prvniho foru

        if kick is not None:
          break # z druheho foru

      # dominovanou vyhodime
      if kick is not None:
        self.matrix.pop(kick)
        self.stratsA -= 1
        removed = True

    # totez pro strategie druheho hrace
      kick = None

      for i in range(self.stratsB):
        for j in range(self.stratsB):
          if self.BStrategyDominates(i, j):
            algo("Hrac 2: strategie %s je dominovana strategii %s" % (j, i))
            kick = j
            break

        if kick is not None:
          break

      if kick is not None:
        for i in range(self.stratsA):
          self.matrix[i].pop(kick)
        self.stratsB -= 1
        removed = True

    return self.stratsB == 1 == self.stratsA

  def preprocess(self):
    """Udela preprocessing cele hry"""
    """Odstrani negativni payoff"""
    """Eliminuje dominovane strategie"""
    """Vraci True, pokud zustalo jen ekviibrium"""

    algo("=== Odstraneni negativnich uzitku ===")
    self.positivize()

    algo("=== Eliminace dominovanych strategii ===")
    equi = self.eliminate()

    return equi

class GameFactory:
  """Trida pro nacitani a ukladani her do souboru"""
  """resp. odkudkoliv, co umi readline a writeline"""

  def loadGameFrom(self, input):
    """Nahraje hru z input"""
    """Haze input error pokud je ve zdroji neco spatne"""

    # nacist jmeno
    name = input.readline()

    # nacist pocty strategii
    first, second = [ int(x) for x in input.readline().split(",") ]

    # nacist strategie prvniho hrace
    firstm = []
    for i in range(first):
      line = input.readline()
      line = line.replace(" ", "")
      line = line.split(",")
      if len(line) != second:
        raise InputError, "Input line does not have proper number of columns"
      else:
        line = [ int(x) for x in line ]
        firstm.append(line)

    #nacist strategie druheho hrace
    secondm = []
    for i in range(first):
      line = input.readline()
      line = line.replace(" ", "")
      line = line.split(",")
      if len(line) != second:
        raise InputError, "Input line does not have proper number of columns"
      else:
        line = [ int(x) for x in line ]
        secondm.append(line)

    # konecne vyrobit hru a nacist do ni matice vyplat
    game = TwoPlayerGame(first, second, name.strip())
    game.loadMatrices(firstm, secondm)

    return game

parser = OptionParser()
parser.add_option("-a", "--algorithm", dest="algo", action="store_true",
                  help="Vypis postupu algoritmu", default=False)
parser.add_option("-d", "--debug", dest="debug", action="store_true",
                  help="Vypis ladicich informace", default=False)
parser.add_option("-g", "--game", dest="game", metavar="GAMEFILE",
                  help="Soubor s definici hry",)

(options, args) = parser.parse_args()

DEBUG = options.debug
ALGO  = options.algo

gf = GameFactory()
debug("Otevirani souboru %s" % options.game)

fp = open(options.game, "r")\

debug("Nahravani hry ze souboru")
game = gf.loadGameFrom(fp)
fp.close()
game.printGame()
print "========================================\n"

if game.preprocess():
  print "Po predzpracovani zbyl jen jeden profil => ekvilibrium v ryzich strategiich:"
  game.unslack()
  game.printGame()
else:
  game.printGame()
