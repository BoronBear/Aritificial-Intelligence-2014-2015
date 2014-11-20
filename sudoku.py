"""
#========================================================================================#
||											||
||		Name: Kevin Lin								||
||		Date: 10/13/2014							||
||		Period: 2								||
||		Description: Recursively Solves a 9x9 Sudoku                    	||
||		                                                                        ||
||                                                                                      ||
#========================================================================================#
"""
#===========================<GLOBAL CONSTANTS AND IMPORTS>===============================#
import copy
MAX = 9
CELL_LENGTH = 3
#========================================================================================#
class Cell(object):
    matrix = None
    def __init__(self, val, r, c, matrix):
        if val != 0:
            self.value = {val}
        else:
            self.value = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.row = r
        self.col = c
        self.block = self.blockNumber(r, c)
        Cell.matrix = matrix
    def blockNumber(self, r, c):
        return ((r//3)+3*(c//3))
#----------------------------------------------------------------------------------------#
def createtheSudokuBoard():
    M = [[4,8,1,5,0,9,6,7,0],
    [3,0,0,8,1,6,0,0,2],
    [5,0,0,7,0,3,0,0,8],
    [2,0,0,0,0,0,0,0,9],
    [9,0,0,0,0,0,0,0,1],
    [8,0,0,0,0,0,0,0,4],
    [0,3,9,2,7,5,4,8,0],
    [6,0,0,0,0,0,9,2,7],
    [7,0,0,0,0,0,3,1,0]]
    matrix = []
    for r in range(MAX):
        row = []
        for c in range(MAX):
            row.append(Cell(M[r][c], r, c, matrix))
        matrix.append(row)
    for r in range(MAX):
        for c in range(MAX):
           matrix[r][c].value = generatePossibleValuesForCell(matrix, r, c)
    displaytheSudokuBoard(matrix)
    return matrix

#----------------------------------------------------------------------------------------#
def isBad(matrix):
	for r in range(MAX):
		for c in range(MAX):
			if matrix[r][c].value == set():
                            return True
	return False
#----------------------------------------------------------------------------------------#
def isCorrect(matrix):
    rows = []
    cols = []
    blocs = []
    for a in range(MAX):
        rows.append([])
        cols.append([])
        blocs.append([])
    for r in range(MAX):
        for c in range(MAX):
            rows[r].append(matrix[r][c].value)
            cols[c].append(matrix[r][c].value)
            blocs[(r // CELL_LENGTH) + CELL_LENGTH * (c // CELL_LENGTH)].append(matrix[r][c].value)
    for r in rows:
        for n in range(1, MAX+1):
            if{n} not in r:
                return False
    for c in cols:
        for n in range(1, MAX+1):
            if{n} not in c:
                return False
    for b in blocs:
        for n in range(1, MAX+1):
            if{n} not in b:
                return False
    return True
#----------------------------------------------------------------------------------------#
def recursivelySolvetheSudoku(matrix):
    matrix = employBasicTechniques(matrix)
    if(isBad(matrix) or isCorrect(matrix)):
        return matrix
    oldMatrix = deepcopy(matrix)
    r, c = smallestValueSet(matrix)
    for guess in matrix[r][c].value:
        matrix = recursivelySolvetheSudoku(matrix)
        if(isCorrect(matrix)):
            return matrix
        matrix = restoreOldVals(matrix, oldMatrix)
    return matrix
#----------------------------------------------------------------------------------------#
def employBasicTechniques(matrix):
    changeMade = True
    while(changeMade):
        changeMade = False
        trickByEliminatePossibilitiesForRowColBloc(matrix, changeMade)
#        trickByEliminatePossibilitiesForCell(matrix, changeMade)
    return matrix
#----------------------------------------------------------------------------------------#
#def trickByEliminatePossibilitiesForCell(matrix, changeMade):
#	for a in range(9):
#		for b in range(9):
#			if(len(matrix[a][b].value) == 1):
#				cell
#----------------------------------------------------------------------------------------#
#def trickBySingleCell(matrix, xind, yind):
#	possiblenumbers = generatePossibleValuesForCell(matrix, xind, yind)
#	if(len(possiblenumbers] == 1):
#		matrix[xind][yind] = possiblenumbers[0]
#		return true
#	return false
#----------------------------------------------------------------------------------------#
def updateCell(matrix, xval, yval):
	xround = (xval//3)*3
	yround = (yval//3)*3
	for a in range(9):
		matrix[xval][a].value = generatePossibleValuesForCell(matrix, xval, yval)
		matrix[a][yval].value = generatePossibleValuesForCell(matrix, xval, yval)
		matrix[xround + (a // 3)][yround + (a % 3)].value = generatePossibleValuesForCell(matrix, xround + (a//3), yround + (a%3))
#----------------------------------------------------------------------------------------#
def trickByEliminatePossibilitiesForRowColBloc(matrix, changeMade):
	for i in range(9):
		if trickByRow(matrix, i) :
			changeMade = True
		if trickByCol(matrix, i) :
			changeMade = True
		if trickByBloc(matrix, (i//3)*3, i%3):
			changeMade = True
#----------------------------------------------------------------------------------------#
def generatePossibleValuesForCell(matrix, xind, yind):
    possiblenumbers = copy.deepcopy(matrix[xind][yind].value)
    for i in range(9):
        if len(matrix[xind][yind].value) == 1:
            if matrix[xind][yind].value[0] in possiblenumbers:
                possiblenumbers.remove(n)
        for n in matrix[xind][yind].value:
            if n in possiblenumbers:
                possiblenumbers.remove(n)

        topleftxind = (xind // 3) * 3
        topleftyind = (yind // 3) * 3

        for a in range(3):
            for b in range(3):
                for n in matrix[topleftxind + a][topleftyind + b].value:
                    if n in possiblenumbers:
                        possiblenumbers.remove(n)
        return possiblenumbers
#----------------------------------------------------------------------------------------#
def trickByRow(matrix, index):
    change = False
    arrayofarraysofpossiblenumbers = []
    for i in range(9):
        arrayofarraysofpossiblenumbers.append(generatePossibleValuesForCell(matrix, i, index))
    count = 0
    indof = -1
    for a in range(1, 10):
        for b in range(9):
            for c in arrayofarraysofpossiblenumbers[b]:
                if(c == a):
                    count+=1
                    indof = b
        if(count == 1):
            matrix[b][index].value = {a}
            change = True
            updateCell(matrix, b, index)
            break
        count = 0
        indof = -1
    return change            
#----------------------------------------------------------------------------------------#
def trickByCol(matrix, index):
    change = False
    arrayofarraysofpossiblenumbers = []
    for i in range(9):
        arrayofarraysofpossiblenumbers.append(generatePossibleValuesForCell(matrix, index, i))
    count = 0
    indof = -1
    for a in range(1, 10):
        for b in range(9):
            for c in arrayofarraysofpossiblenumbers[b]:
                if(c == a):
                    count+=1
                    indof = b
        if(count == 1):
            matrix[index][b].value = {a}
            change = True
            updateCell(matrix, index, b)
            break
        count = 0
        indof = -1
    return change
#----------------------------------------------------------------------------------------#
def trickByBloc(matrix, xind, yind):
    change = False
    x = (xind // 3)*3
    y = (yind // 3)*3
    arrayofarraysofpossiblenumbers = []
    for i in range(9):
        arrayofarraysofpossiblenumbers.append(generatePossibleValuesForCell(matrix, x+(i//3), y+(i%3)))
    count = 0
    indof = -1
    for a in range(1, 10):
        for b in range(9):
            for c in arrayofarraysofpossiblenumbers[b]:
                if(c == a):
                    count += 1
                    indof = b
        if(count == 1):
            matrix[x+b//3][y+(b%3)].value = {a}
            change = True
            updateCell(matrix, index, b)
            break
        count = 0
        indof = -1
    return change
#----------------------------------------------------------------------------------------#
def restoreOldVals(matrix, oldMatrix):
    for r in range(MAX):
        for c in range(MAX):
            matrix[r][c].value = oldMatrix[r][c].value
    return matrix
#----------------------------------------------------------------------------------------#
def displaytheSudokuBoard(matrix):
	for r in range(MAX):
		for c in range(MAX):
			print(matrix[r][c].value, " ")
		print("\n \n")
#----------------------------------------------------------------------------------------#
def printVerification(matrix):
	return
#----------------------------------------------------------------------------------------#
def main():
    matrix = createtheSudokuBoard()
    matrix = recursivelySolvetheSudoku(matrix)
    displaytheSudokuBoard(matrix)
    printVerification(matrix)
#----------------------------------------------------------------------------------------#
main()
