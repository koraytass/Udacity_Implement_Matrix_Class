import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

    
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        if self.h == 1:
            unit_matrix=abs(self[0][0])
            return unit_matrix
        elif self.h==2:
            a = self[0][0]
            b = self[0][1]
            c = self[1][0]
            d = self[1][1]
            
            determinant = abs((a * d - b * c))
            return determinant
        # TODO - your code here

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        summation=0
        for i in range(self.h):
            for k in range(self.w):
                if i == k:
                    summation += self[i][k]
        
        return summation

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        inverse_of_unit_matrix=[]
        
        if self.h == 1:
            inverse_of_unit_matrix.append([1 / self[0][0]])
            return Matrix(inverse_of_unit_matrix)
        elif self.h == 2:
            a = self[0][0]
            b = self[0][1]
            c = self[1][0]
            d = self[1][1]
            factor = 1 / (a * d - b * c)
            inverse = [[d, -b],[-c, a]]
            for i in range(len(inverse)):
                for j in range(len(inverse[0])):
                    inverse[i][j] = factor * inverse[i][j]
            return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = []
        for c in range(self.w):
            new_row = []
            for r in range(self.h):
                new_row.append(self[r][c])
            matrix_transpose.append(new_row)
        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.
        Example:
        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]
        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        summation = []
        for i in range(self.h):
            array = [] # reset the list
            for j in range(self.w):
                array.append(self[i][j] + other[i][j]) # add the matrices
            summation.append(array)

        return Matrix(summation)
    
    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)
        Example:
        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        multiplication = []
        factor = -1
        for i in range(self.h):
            row=[]
            for j in range(self.w):
                row.append(factor*self[i][j])
            multiplication.append(row)
        
        return Matrix(multiplication)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        subs=[]
        for i in range(self.h):
            elem=[]
            for k in range(self.w):
                elem.append(self.g[i][k]-other.g[i][k])
            subs.append(elem)
        return Matrix(subs)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        vect = zeroes(self.h, other.w)
        for x in range(self.h):
            for y in range(other.w):
                for z in range(other.h):
                    vect[x][y] += self[x][z] * other[z][y]
        return vect

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.
        Example:
        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            multp = zeroes(self.h, self.w)
            for i in range(self.h):
                for j in range(self.w):
                    multp[i][j] = self[i][j] * other
            return multp
            