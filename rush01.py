from sys import argv

class SkyscraperSolver:
    
    """
    constraints = [
        [col1u, col2u, col3u, col4u], (up)
        [col1d, col2d, col3d, col4d], (down)
        [row1l, row2l, row3l, row4l], (left)
        [row1r, row2r, row3r, row4r], (right)
    """
    def __init__(self, constraints):
        self.traversed = 0
        self.constraints = constraints
        self.solution = [
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1]
                        ]
        
    def validateSolution(self):
        for i in range(4):
            if self.isValidRow(i) == False or self.isValidCol(i) == False:
                return False
        return True

    def printSolution(self):
        for row in self.solution:
            print(row[0], row[1], row[2], row[3])
            
    def prettyPrint(self):
        print(f" X | {self.constraints[0][0]} | {self.constraints[0][1]} | {self.constraints[0][2]} | {self.constraints[0][3]} | X ")
        print("-----------------------")
        print(f" {self.constraints[2][0]} | {self.solution[0][0]} | {self.solution[0][1]} | {self.solution[0][2]} | {self.solution[0][3]} | {self.constraints[3][0]} ")
        print(f" {self.constraints[2][1]} | {self.solution[1][0]} | {self.solution[1][1]} | {self.solution[1][2]} | {self.solution[1][3]} | {self.constraints[3][1]} ")
        print(f" {self.constraints[2][2]} | {self.solution[2][0]} | {self.solution[2][1]} | {self.solution[2][2]} | {self.solution[2][3]} | {self.constraints[3][2]} ")
        print(f" {self.constraints[2][3]} | {self.solution[3][0]} | {self.solution[3][1]} | {self.solution[3][2]} | {self.solution[3][3]} | {self.constraints[3][3]} ")
        print("-----------------------")
        print(f" X | {self.constraints[1][0]} | {self.constraints[1][1]} | {self.constraints[1][2]} | {self.constraints[1][3]} | X ")

    def getCol(self, x_pos):
        col = []
        for i in range(4):
            col.append(self.solution[i][x_pos])
        return col

    # constraints[0][x_pos] up
    # constraints[1][x_pos] down
    # constraints[2][y_pos] left
    # constraints[3][y_pos] right
    def isValidCol(self, x_pos):

        col = self.getCol(x_pos) # up [ ... ] down
        
        if sorted(col) != [1, 2, 3, 4]:
            return False
        
        hehe = [col, col[::-1]]
        cs = [self.constraints[0][x_pos], self.constraints[1][x_pos]]
        for n, item in enumerate(hehe):
            tallest = item[0]
            visible = 1
            for i in range(1, 4):
                if tallest < item[i]:
                    visible += 1
                    tallest = item[i]
            if visible != cs[n]:
                return False
        return True

    def isValidRow(self, y_pos):
        
        row = self.solution[y_pos]
        
        if sorted(row) != [1, 2, 3, 4]:
            return False
        
        hehe = [row, row[::-1]]
        cs = [self.constraints[2][y_pos], self.constraints[3][y_pos]]
        for n, item in enumerate(hehe):
            tallest = item[0]
            visible = 1
            for i in range(1, 4):
                if tallest < item[i]:
                    visible += 1
                    tallest = item[i]
            if visible != cs[n]:
                return False
        return True
    
    # O(4 ^ n)
    def solve(self, x_pos, y_pos, value_test):
        
        if value_test > 4: # value larger than 4 -> all values tested -> flag as wrong to backtrack
            self.solution[y_pos][x_pos] = 0
            return 0
        
        self.solution[y_pos][x_pos] = value_test # set value to test inside solution
        self.traversed += 1
        bt = 0
        
        if y_pos == 3 and not self.isValidCol(x_pos): # if rows all valid and current column not valid, try diff value
            return self.solve(x_pos, y_pos, value_test + 1)
        
        if x_pos < 3: # if curr column valid check next column
            bt = self.solve(x_pos + 1, y_pos, 1)
        else: # if all columns valid, start checking rows
            if self.isValidRow(y_pos) == True:
                if y_pos == 3: # if all rows valid, we found a solution
                    return 1
                bt = self.solve(0, y_pos + 1, 1) # if curr row valid check next row
                
        
        if bt: # pull result (either 1 - solution found or 0 - fail) up
            return bt
        
        return self.solve(x_pos, y_pos, value_test + 1) # if row not valid, try diff value
        

def handleArgv(argv):
    if len(argv) != 2:
        return None
    data = [int(x) for x in argv[1] if x.isdigit()] # convert argv to list
    if len(data) != 16:
        return None
    constraints = [data[x:x + 4] for x in range(0, 16, 4)]
    return constraints

def main():
    constraints = handleArgv(argv)
    if not constraints:
        print("Error")
        return

    solver = SkyscraperSolver(constraints)
    
    if (solver.solve(0, 0, 1) == 1 and solver.validateSolution() == True):
        solver.printSolution()
        print(f"States explored: {solver.traversed}")
    else:
        print("Error")
        print(f"States explored: {solver.traversed}")

if __name__ == "__main__":
    main()