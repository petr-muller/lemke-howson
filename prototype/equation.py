#!/usr/bin/python

class EquationModel:
  def __init__(self):
    self.equations = []

  def addEquation(self, eq):
    if eq.left == 0:
      raise ValueError, "Cannot add equation to model: it has to have some left side"
    else:
      self.equations.append(eq)

  def __str__(self):
    return "\n".join(["%s" % x for x in self.equations])

  def pivotBy(self, variable):
    index = -1
    cur = None
    i = 0
    for eq in self.equations:
      if variable in eq.right:
        if cur is None or eq.body[variable] < cur:
          cur = eq.body[variable]
          index = i
      i += 1

    self.equations[index].solveFor(variable)
    for eq in self.equations:
      eq.substitute(self.equations[index])

    self.nextpivot = index + 1

  def getNextPivot(self):
    return self.nextpivot

  def solutionsForNonbasic0(self):
    solution = {}
    for eq in self.equations:
      for r in eq.right:
        solution[r] = 0
      solution[eq.left] = eq.constant
    
    return solution

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

# game of chicken, preprocessed to nonnegative...

eq1 = Equation()
eq2 = Equation()
eq3 = Equation()
eq4 = Equation()

index = 1
for i in (eq1, eq2, eq3, eq4):
  i.addConstant(1)
  i.addToEquation(-1, "v%s" % index)
  i.solveFor("v%s" % index)
  index += 1

eq1.addToEquation(-1, "x3")
eq1.addToEquation(-3, "x4")

eq2.addToEquation(-2, "x4")

eq3.addToEquation(-1, "x1")
eq3.addToEquation(-3, "x2")

eq4.addToEquation(-2, "x2")

eqm = EquationModel()
for i in (eq1, eq2, eq3, eq4):
  eqm.addEquation(i)

print eqm

startpivot = 4
print "Next pivot: %s" % startpivot
eqm.pivotBy("x%s" % startpivot )
print eqm

nextpivot = eqm.getNextPivot()
print "Next pivot: %s" % nextpivot
eqm.pivotBy("x%s" % nextpivot )
print eqm

nextpivot = eqm.getNextPivot()
print "Next pivot: %s" % nextpivot
eqm.pivotBy("x%s" % nextpivot )
print eqm

nextpivot = eqm.getNextPivot()
print "Next pivot: %s" % nextpivot
#eqm.pivotBy("x%s" % nextpivot )

#nextpivot = eqm.getNextPivot()
#print "Next pivot: %s" % nextpivot


sol = eqm.solutionsForNonbasic0()
print sol

print "Prop1: %s" % (sol["x1"] / (sol["x1"] + sol["x2"]))
print "Prop2: %s" % (sol["x2"] / (sol["x1"] + sol["x2"]))
print "Prop3: %s" %  (sol["x3"] / (sol["x3"] + sol["x4"]))
print "Prop4: %s" % (sol["x4"] / (sol["x3"] + sol["x4"]))
