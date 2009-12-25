import lha

tpg = lha.TwoPlayerGame(2,2)

tpg.matrix[0][0].payoffA = -2
tpg.matrix[0][0].payoffB = -2

tpg.matrix[0][1].payoffA = 0
tpg.matrix[0][1].payoffB = -3

tpg.matrix[1][0].payoffA = -3
tpg.matrix[1][0].payoffB = 0

tpg.matrix[1][1].payoffA = -1
tpg.matrix[1][1].payoffB = -1

tpg.printGame()
tpg.preprocess()
tpg.printGame()
