import sys

SuitOrder = [
        [10,9,8],
        [7,6,0],
        [5,4,0],
        [3,2,0],
        ]
SuitSpread = [
        [10,8,0],
        [9,7,0],
        [6,4,0],
        [5,3,2],
        ]
SuitMix = [
        [10,6,2],
        [9,3,0],
        [8,4,0],
        [7,5,0],
        ]
        
Suit = SuitSpread
ColorSame = Suit[0] + Suit[2]
ColorOff =  Suit[1] + Suit[3]

ColorBoth = [
        ColorSame,
        ColorOff,
        ]
        
#[[0,*range(2,11)]]
Number = [list(dict.fromkeys(Suit[0] + Suit[1] + Suit[2] + Suit[3]))]

Hands = {
    8:{
        "Suit":[Suit * 2,10],
        "Color":[ColorBoth * 4,0],
        "Number":[Number * 8,0]
    },
    4:{
        "Suit":[Suit,8],
        "Color":[ColorBoth * 2,0],
        "Number":[Number * 4,2],
    },
    3:{
        "Suit-M-0,2,3":[Suit[:1]+ Suit[2:],2],
        "Suit-M-0,1,3":[Suit[:2]+ Suit[3:],2],
        "Suit-M-0,1,2":[Suit[:3]+ Suit[4:],2],
        "Number": [Number * 3,2],
    },
    2:{
        "Suit":[[Suit[0],Suit[1]],0],
        "Color":[ColorBoth,4],
        "Number": [Number * 2,2],
    },
    1:{
        "Suit":[[Suit[0]],0],
        "ColorSame":[[ColorSame],3],
        "ColorOff":[[ColorOff],3],
        "Number": [Number,0],
    },
}

def Play(GameHands,players, distancefromCenter = .1, distancefromEnds = 9, countOfChallenges = 3):
    TheoreticalChallenges=range( 10*players,players,-1)
    error = False
    DFC =  distancefromCenter / 100
    DFE = distancefromEnds / 100
    if not 0 < distancefromCenter < 50:
        print('Error distancefromCenter expected between 0 and 50 but found: ' + str(distancefromCenter))
        error = True
    
    if not 0 < distancefromEnds < 50:
        print('Error distancefromEnds expected between 0 and 50 but found: ' + str(distancefromEnds))
        error = True
    for i,j in GameHands.items():
        if len(j) != 2:
            print('Error: '+str(i) +' 2 fields expected found: '+ str(len(j)))
            error = True
        if len(j[0]) != players:
            print('Error there must be a hand per player('+str(players)+')\n\tError hand: '+str(i)+ ' count:'+str(len(j[0]))+'\n\t' +str(j[0]))
            error = True
    if error:
        return
    print ('-'*50 + '\n|'+' '*21+
        '~['+str(players)+']~'+
        ' '*22+'|\n'+'-'*50 + '\n')
    def play(G,Hand,mode):       
        all = []
        Grid = []
        O = ('Challenges: ' + str(G) +'\n')
        for name,card in Hand.items():
            dict = {}
            P = 0
            F = 0
            o = ''
            if card[1] > 0:
                for g in G:
                    R(card[0],g)
                    p = Pass
                    f = Total - Pass
                    if mode:
                        o+=('\t\t['+str(g)+'] p:'+str(p)+
                            ' - f:'+str(f)+' ('+'{:.1%}'.format(p/(f+p))+
                            ') t:'+str(f+p)+'\n')
                    P+=p
                    F+=f
                    t = ['{:.1%}'.format(Pass/Total),p,f]
                    dict[g] = t
                if mode:
                    O+=('\t'+name+': '+'P:'+str(P)+
                        ' - F:'+str(F)+' ('+'{:.1%}'.format(P/(F+P))+
                        ') T:'+str(F+P)+' W:'+str(card[1])+' \n'+o)
                all += [P/(F+P)]*card[1]
                Grid += [[dict,card[1]]]
        if mode:
            print( O + 'Odds: {:.2%}\n'.format(sum(all)/len(all)))
        else:
            Balance(Grid,G)
    
    def Balance(rounds,possibleValues):
        global valid
        valid = []
        dict = {}
        comb = {}
        for v in possibleValues:
            x = []
            p = True
            for r in rounds:
                z = r[0][v]
                x = x + [[z,r[1]]]
                if not (1-DFE > z[1]/(z[2]+z[1]) > DFE):
                    p = False
            if p:
                dict[v] = x
        for x,y in dict.items():
            sum = 0
            sumWght = 0
            for z in y:
                num = z[0]
                wght = z[1]
                sumWght += wght
                sum += (num[1]/(num[1]+num[2]))*wght
            comb[x] = sum/sumWght
        keys = list(comb.keys())
        def balance(dict,keys, depth,sum,c):
            global valid
            if depth >= countOfChallenges:
                if .5+DFC > sum/countOfChallenges > .5-DFC:
                    valid += [c]
            else:
                for x in keys:
                    balance(dict,keys[keys.index(x)+1:], depth+1,sum + dict[x],c + [x])
                    
        balance(comb,keys,0,0,[])
        for game in valid:
            play(game,GameHands,True)
        

    def R(cards, target):
        global Total
        global Pass
        Total = 0
        Pass = 0
        def r(hand, target, score):
            if(len(hand) <= 0): 
                global Total
                global Pass 
                Total += 1
                if( score >= target):
                    Pass += 1
            else:
                for card in hand[0]:
                    r(hand[1:],target,score+card)
        r(cards, target ,0)
    play(TheoreticalChallenges,GameHands,False)
    
if __name__== "__main__":
    args = sys.argv
    argLen = len(args)
    try:
        if argLen > 5:
            print('Error, Maximum 4 Arguments: players, distancefromCenter = .1, distancefromEnds = 9, countOfChallenges = 3')
        elif argLen > 4:
            Play(Hands[int(args[1])], int(args[1]),float(args[2]),float(args[3]),int(args[4]))
        elif argLen > 3:
            Play(Hands[int(args[1])], int(args[1]),float(args[2]),float(args[3]))
        elif argLen > 2:
            Play(Hands[int(args[1])], int(args[1]),float(args[2]))
        elif argLen > 1:
            Play(Hands[int(args[1])], int(args[1]))
        else:
            for p, h in Hands.items():
                Play(h,p)
    except KeyError as e:
        print('I\'m Sorry, "%s" is not currenly a valid amount of players.' % str(e))
    except ValueError:
        print('I\'m Sorry, Ivalid arguments: %s\n\tproper format: [INT, FLOAT?, FLOAT?, INT?]' % str(args[1:]))