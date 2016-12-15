# Generates all arrangements of M bits into N possible positions

# for pretty printing of the 'final' dictionary
from pprint import pprint
import sys

M = 2 # number chosen i.e. 3
N = 4 # number total i.e. 32

# global variable for pre-computing powers of two up through N
powersOfTwo = []

# global variable for the final collection of bitvectors
final = {}

# global variable for combinations of indices
ncombos = N ** M
combos = [None] * ncombos
cnt = 0

# a function to generate a n-bit bitvector - and corresponding decimal
# value - for m bit positions, but only save it to 'final' if the
# combination of m positions hadn't been visited yet
def genBitVector(n, indices):
    global final, powersOfTwo
    result = 0
    
    # Map unique set of indices to their corresponding powers of 2.
    # This prevents double-counting when two or more indices are equal.
    uniquePowers = {}
    for idx in indices:
        if idx not in uniquePowers:
            uniquePowers[idx] = powersOfTwo[idx]
            
    # String representation of the bit vector, for easier visualization
    bitVec = ['0'] * n

    # Generate the integer value by adding 2^idx to result for each idx
    for idx in uniquePowers:
        result += uniquePowers[idx]
        bitVec[n-idx-1] = '1'

    # Only save this result if it hadn't been saved before. Since
    # we're finding duplicates, does this imply we could optimize by
    # saving some calculations that have been done before?
    if result not in final:
        #print bitVec, "(", res, ")"
        final[result] = ''.join(bitVec)

# Generates all combinations of positions of m bits in a bitvector of
# length n (the recursion part of combosGenRecurse())
def combosRecurse(m, n, runningBitList, level, ival):
    global combos, cnt

    # Add my ival to lst, skipping top level "root"
    #print "appending ival", ival, "at level", level
    if level != m:
        runningBitList.append(ival)

    # test for stopping condition
    if level == 0:
        # at a leaf node; add this (partial) bit list to combos & return
        combos[cnt] = runningBitList
        cnt += 1
        return

    # Recurse through "children"
    for i in range(0, n):
        # Pass the running list to next level, which will add to it
        new_list = list(runningBitList)
        combosRecurse(m, n, new_list, level-1, i)

# Generates all combinations of positions of m bits in a bitvector of
# length n
def combosGenRecurse(m, n):
    global cnt
    cnt = 0
    combosRecurse(m, n, [], m, 0)

# Simplified version of combosGenRecurse() that hardcodes M = 3 (i,j,k)
def combosGenIter(n):
    global cnt
    global combos
    cnt = 0
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                indices = [i, j, k]
                #print "i,j,k:", i, j, k
                combos[cnt] = list([i, j, k])
                cnt += 1
                
# Generates all arrangements of m bits into n positions
def generate(m, n):
    global powersOfTwo, final, combos
    print "Distributing 1 ..", m, "objects among", n, "positions..."
    final = {}
    powersOfTwo = [2**x for x in range(0,n)]
    combosGenRecurse(m, n)
    #combosGenIter(n)
    #print combos
    #sys.exit()
    for indices in combos:
        #print "generating bit vector for:", "indices:", indices
        genBitVector(n, indices)
    pprint(final)
    print "(", len(final), "combinations of", m, "into", n, ")"

# generate all arrangements of M bits into N possible positions
generate(M, N)

