#!/usr/bin/python

class PureStrategy:
  def __init__(self, payoffA, payoffB):
    self.payoffA = payoffA
    self.payoffB = payoffB

  def getNegative(self):
    if self.payoffA < 0 or self.payoffB < 0:
      return abs(min(self.payoffA, self.payoffB))
    else:
      return 0

class TwoPlayerGame:
  def __init__(self, stratsA, stratsB):
    if stratsA < 2 or stratsB < 2:
      raise ValueError, "Not really a game: each player should have at least 2 strategies"
    else:
      self.stratsA = stratsA
      self.stratsB = stratsB

      self.matrix   = [ [PureStrategy(3,2) for x in range(self.stratsB)] for y in range(self.stratsA) ]
      self.stratADigits = 1
      self.stratBDigits = 1

  def printGame(self):
    for i in range(self.stratsA):
      for j in range(self.stratsB):
        strat = self.matrix[i][j]
        print "[%s] " % ("%s:%s".center(self.stratADigits + self.stratBDigits + 1) % (strat.payoffA, strat.payoffB)),
      print "\n",
  
  def positivize(self):
    slack = 0

    for i in range(self.stratsA):
      for j in range(self.stratsB):
        slack = max(slack, self.matrix[i][j].getNegative())

    if slack > 0:
      for i in range(self.stratsA):
        for j in range(self.stratsB):
          self.matrix[i][j].payoffA += slack
          self.matrix[i][j].payoffB += slack

  def _payoffs(self, player, strategy):
    if player == "A":
      ret = [ self.matrix[strategy][x].payoffA for x in range(self.stratsB) ]
    else:
      ret = [ self.matrix[x][strategy].payoffB for x in range(self.stratsA) ]
    
    return ret

  def AStrategyDominates(self, first, second):
    fir = self._payoffs("A", first)
    sec = self._payoffs("A", second)

    for i in range(self.stratsA):
      if sec[i] >= fir[i]:
        return False

    return True

  def BStrategyDominates(self, first, second):
    fir = self._payoffs("B", first)
    sec = self._payoffs("B", second)

    for i in range(self.stratsA):
      if sec[i] >= fir[i]:
        return False

    return True

  def eliminate(self):
    removed = True
    while removed:
      removed = False
      kick = None

      for i in range(self.stratsA):
        for j in range(self.stratsA):
          if self.AStrategyDominates(i, j):
            kick = j
            break
        
        if kick is not None:
          break

      if kick is not None:
        self.matrix.pop(kick)
        self.stratsA -= 1
        removed = True

    removed = True
    while removed:
      removed = False
      kick = None

      for i in range(self.stratsB):
        for j in range(self.stratsB):
          if self.BStrategyDominates(i, j):
            kick = j
            break
        
        if kick is not None:
          break

      if kick is not None:
        for i in range(self.stratsA):
          self.matrix[i].pop(kick)
        self.stratsB -= 1
        removed = True

  def preprocess(self):
    self.positivize()
    self.eliminate()
