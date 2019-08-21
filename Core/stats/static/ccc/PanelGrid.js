const twelve = 12
var hexColor = '#DDA0DD'
var theGrid = new Array(twelve);
var checked = false
var firstX
var firstY

for (var i = 0; i < theGrid.length; i++) {
  theGrid[i] = new Array(twelve);
}

//var h = 1; 

// for (var i = 0; i < twelve; i++) { 
    // for (var j = 0; j < twelve; j++) { 
        // theGrid[i][j] = h++; 
    // } 
// } 

const palette = document.getElementById('palette'), nameSpan = document.getElementById('name'), hexSpan=document.getElementById('hex');

for (var i = 0; i < twelve; i++) { 
    for (var j = 0; j < twelve; j++) { 
		const li = document.createElement('li');
		//li.name = "grid" [i]+"-"+[j];
		li.title = "("+i+","+j+")"
		li.style.backgroundColor = '#F5F5F5';
		li.dataset.x = j
		li.dataset.y = i
		theGrid[i][j] = li; 
		palette.appendChild(li);
    } 
}  

palette.onclick = e => {
	const li = e.target;
	if (palette.active) palette.active.className = palette.active.className.replace(' active', '');
	palette.active=li;
	li.className+=' active';
	
	if(checked) {	
		Painter(firstX,firstY,Number(li.dataset.x),Number(li.dataset.y),hexColor)
		checked = false;
	}
	else
	{
		//li.style.backgroundColor = '#32CD32';
		firstX = li.dataset.x
		firstY = li.dataset.y
		checked = true;
	}
};

function Painter(Ax, Ay, Bx, By, color){
	var startx
	var starty
	var endx
	var endy
	
	if(Ax < Bx){
		startx = Ax
		endx = Bx
	}
	else{
		startx = Bx
		endx = Ax
	}
	if(Ay < By){
		starty = Ay
		endy = By
	}
	else{
		starty = By
		endy = Ay
	}
	for (var i = starty; i <= endy; i++) { 
		for (var j = startx; j <= endx; j++) { 
			theGrid[i][j].style.backgroundColor = color;
		}	
	}
}