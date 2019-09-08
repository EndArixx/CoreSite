showmtotals = True
showctotals = True
showTtotals = True

challenge = {
	"Asured":5,
	"Easy":10,
	"Normal":15,
	"Hard":20,
	"Impossible":25,
	}
mod = [
	0,
	5,
	10
	]
reward = {
	15:1,
	20:2,
	25:5,
		}
risk = {
	20:2,
	25:3,
		}

twotens = []
for i in range(1,11):
	for j in range(1,11):
		twotens.append(i+j)
dieOptions = {}
#dieOptions['Two D10s'] = twotens
dieOptions['One D20'] = range(1,20+1)
for name,rank in challenge.items():
	if rank not in reward:
		reward[rank] = 0
	if rank not in risk:
		risk[rank] = 1

def Printinfo(name, Total, Success, Failed,Rewards,Damage,lead=""):
	out = ("""%s:
	Pass: %s Fail: %s Attempts: %s
	Success odds: %d%%
	Reward: %d (per roll: %s)
	Punish: %d (per roll: %s)""" %
		(name,Success,Failed,Total, Success/Total*100,
		Rewards,round(Rewards/Total, 3),
		Damage,round(Damage/Total, 3)))
	out = out.split("\n")	
	for line in out:
		print(str(lead) + line)

for name,diepool in dieOptions.items():
	TSuc = 0
	TFal = 0
	TRew = 0
	TDam = 0
	print("\n---------------------\n%s (%d to %d)\n---------------------\n"
		%(name,diepool[0],diepool[len(diepool)-1]))
	for cname,c in challenge.items():
		if showctotals or showmtotals:
			print("%s(%d)" % (cname,c))
		cSuc = 0
		cFal = 0 
		cRew = 0
		cDam = 0
		for m in mod:
			mSuc = 0 
			mFal = 0 
			mRew = 0
			mDam = 0
			for roll in diepool:
				if roll == diepool[len(diepool)-1]:
					mSuc += 1
					mRew += 1
					mRew += reward[c]
				elif roll == diepool[0]:
					mFal += 1
					mRew += 1
					mDam += risk[c]
				elif roll + m > c:
					mSuc += 1
					mRew += reward[c]
				else:
					mFal += 1
					mDam += risk[c]
			cSuc += mSuc
			cFal += mFal
			cRew += mRew
			cDam += mDam
			mTot = mSuc+mFal
			if showmtotals:
				Printinfo("Mod "+str(m),mTot,mSuc,mFal,mRew,mDam,"\t\t")
		TSuc += cSuc
		TFal += cFal
		TRew += cRew
		TDam += mDam
		cTot = cSuc + cFal
		if showctotals:
			Printinfo("Challenge "+str(c),cTot,cSuc,cFal,cRew,cDam,"\t")
	TTot = TSuc + TFal
	if showTtotals:
		Printinfo("Absolute totals for "+name,TTot,TSuc,TFal,TRew,TDam)