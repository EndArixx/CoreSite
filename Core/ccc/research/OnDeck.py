GMhands=[23,18,15]
playerhands={
    "Suit":[
        [10,9,8],
        [7,6,0],
        [5,4,0],
        [3,2,0],
        ]
    ,"Color":[
        [10,9,8,5,4,0],
        [7,6,3,2,0,0],
        ] * 2
    ,"Number":[
        [0,*range(2,11)]
        ] * 4
    }

def Play(G,D):
    O = ''
    for n,v in D.items():
        P = 0
        F = 0
        o=''
        for g in G:
            R(v,g)
            p = Pass
            f = Total- Pass
            o+='\t['+str(g)+'] p:'+str(p)+' - f:'+str(f)+' ('+'{:.1%}'.format(p/(f+p))+') t:'+str(f+p)+'\n'
            P+=p
            F+=f
        O+=n+': '+'P:'+str(P)+' - F:'+str(F)+' ('+'{:.1%}'.format(P/(F+P))+') T:'+str(F+P)+'\n'+o
    return O

def R(cards, target):
    global Total
    Total = 0
    global Pass
    Pass = 0
    def r(hand, target, score):
        if(len(hand) <= 0): 
            global Total
            Total += 1
            if( score >= target):
                global Pass 
                Pass += 1
        else:
            for card in hand[0]:
                r(hand[1:],target,score+card)
    r(cards, target ,0)

print(Play(GMhands,playerhands))