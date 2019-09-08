class Point:
	def __init__(this, x = 0, y = 0):
		this.x = x
		this.y = y

n = 10
TheGrid = [[0] * n for i in range(n)]		
	
def Painter(A, B, grid,color):
	start = Point()
	end = Point()
	
	if(A.x < B.x):
		#print(str(B.x) +' is bigger than '+str(A.x))
		start.x = A.x
		end.x = B.x
	else: #B.x =< A.x
		#print(str(B.x) +' is less than or equal to '+str(A.x))
		start.x = B.x
		end.x = A.x
	if(A.y < B.y):
		#print(str(B.y) +' is bigger than '+str(A.y))
		start.y = A.y
		end.y = B.y
	else: #B.y >= A.y
		#print(str(B.y) +' is less than or equal to '+str(A.y))
		start.y = B.y
		end.y = A.y
	
	print('Start ('+ str(start.x)+','+ str(start.y)+') End ('+str(end.x)+','+str(end.y)+')')
	
	for i in range(start.x, end.x+1):
		for j in range(start.y, end.y+1):
			#print('('+str(i)+','+str(j)+') '+color)
			grid[i-1][j-1] = color

Painter(Point(3,5),Point(1,7),TheGrid,"X")	
Painter(Point(4,7),Point(4,2),TheGrid,"@")	
Painter(Point(7,7),Point(7,7),TheGrid,"J")	

for row in TheGrid:
	for elem in row:
		print(elem,end ="")
	print()