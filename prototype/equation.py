#!/usr/bin/python

class Equation:
  def __init__(self):
    self.left       = 0
    self.right      = []
    self.body       = {}
    self.constant   = 0

  def __str__(self):
    format = "%s = %s"
    right  = []
    for key in self.body.keys():
      right.append("%+.2f%s" % (self.body[key], key))

    right.append("%+.2f" % self.constant)
    return format % (self.left, " ".join([ str(x) for x in right]))

  def addToEquation(self, coef, label):
    if label == self.left:
      raise ValueError, "Adding to equation's left size is not possible"
    
    if label in self.right:
      self.body[label] += coef
    else:
      self.body[label] =  coef
      self.right.append(label)
  
  def addConstant(self, coef):
    self.constant += coef

  def substitute(self, other):
    if other.left in self.right:
      my = self.body[other.left]
      self.right.remove(other.left)
      self.body.pop(other.left)

      self.addConstant(other.constant * my)
      for key in other.right:
        self.addToEquation( my*other.body[key], key)

  def solveFor0(self):
    if self.left != 0:
      tmp = self.left
      self.left = 0
      self.addToEquation(-1, tmp)

  def solveFor(self, label):
    self.solveFor0()

    if label not in self.right:
      raise ValueError, "Cannot solve an equation which is not in it"

    my = -1.0 * self.body[label]
    self.right.remove(label)
    self.body.pop(label)

    self.left = label

    self.constant /= float(my)
    for key in self.right:
      self.body[key] = float(self.body[key]) / float(my)

  def substituteValue(self, label, value):
    if label not in self.right:
      raise ValueError, "Error substituting to var %s: no such variable" % label

    coef = float(self.body[label])
    self.addConstant(coef * value)
    self.right.remove(label)
    self.body.pop(label)

eq1 = Equation()
eq1.addToEquation(2, "x")
eq1.addToEquation(-3, "y")

eq2 = Equation()
eq2.addToEquation(1, "x")
eq2.addToEquation(1, "y")
eq2.addConstant(-5)

print eq1
print eq2

eq2.substituteValue("y", 4)
print eq2
