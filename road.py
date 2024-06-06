
DATA_LR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 2, 4, 2, 4, 2, 0, 0, 0,-2,-2,-4,-4,-2,-1, 0, 0, 0, 0, 0, 0, 0]
DATA_UD = [0, 0, 1, 2, 3, 2, 1, 0,-2,-4,-2, 0, 0, 0, 0, 0,-1,-2,-3,-4,-3,-2,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-3, 3, 0,-6, 6, 0]
CLEN = len(DATA_LR)


BOARD = 120
CMAX = BOARD*CLEN
curve = [0]*CMAX
updown = [0]*CMAX
object_left = [0]*CMAX
object_right = [0]*CMAX


def make_road():
    for i in range(CLEN):
        lr1 = DATA_LR[i]
        lr2 = DATA_LR[(i+1)%CLEN]
        ud1 = DATA_UD[i]
        ud2 = DATA_UD[(i+1)%CLEN]
        for j in range(BOARD):
            pos = j+BOARD*i
            curve[pos] = lr1*(BOARD-j)/BOARD + lr2*j/BOARD
            updown[pos] = ud1*(BOARD-j)/BOARD + ud2*j/BOARD
            
            

