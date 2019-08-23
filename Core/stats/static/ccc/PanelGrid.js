//---------------------------------------------------------------------
//Constants------------------------------------------------------------
//---------------------------------------------------------------------
const twelve = 12
const panelgrid = document.getElementById('panelgrid'), nameSpan = document.getElementById('name'), hexSpan=document.getElementById('hex');

//---------------------------------------------------------------------
//Variables------------------------------------------------------------
//---------------------------------------------------------------------
var theGrid = new Array(twelve);
var checked = false
var showgrid = true
var firstX
var firstY
var sel = document.getElementById('colorchooser');
var tog = document.getElementById('gridtoggle');

//---------------------------------------------------------------------
//Init-----------------------------------------------------------------
//---------------------------------------------------------------------
sel.style.backgroundColor = sel.options[sel.selectedIndex].value

for (var i = 0; i < theGrid.length; i++) {
  theGrid[i] = new Array(twelve);
}
for (var i = 0; i < sel.length; i++) { 
	sel.options[i].style.backgroundColor = sel.options[i].value
}
for (var i = 0; i < twelve; i++) { 
    for (var j = 0; j < twelve; j++) { 
		const li = document.createElement('li');
		//li.name = "grid" [i]+"-"+[j];
		li.title = "("+i+","+j+")"
		li.style.backgroundColor = '#F5F5F5';
		li.dataset.x = j
		li.dataset.y = i
		theGrid[i][j] = li; 
		panelgrid.appendChild(li);
    } 
}  


//---------------------------------------------------------------------
//Events---------------------------------------------------------------
//---------------------------------------------------------------------
sel.onclick = e => {
	sel.style.backgroundColor = sel.options[sel.selectedIndex].value
}

tog.onclick = e => {
	if(showgrid){showgrid = false}
	else{showgrid = true}
	for (var i = 0; i < twelve; i++) { 
		for (var j = 0; j < twelve; j++) { 
			if(showgrid)theGrid[i][j].style.borderColor = "#000000" 
			else theGrid[i][j].style.borderColor = theGrid[i][j].style.backgroundColor
		}
	}
}


panelgrid.onclick = e => {
	const li = e.target;
	if (panelgrid.active) panelgrid.active.className = panelgrid.active.className.replace(' active', '');
	panelgrid.active=li;
	li.className+=' active';
	
	if(checked) {	
		Painter(firstX,firstY,Number(li.dataset.x),Number(li.dataset.y),sel.options[sel.selectedIndex].value)
		checked = false;
	}
	else
	{	
		//use black for current because it will not be allowed as an option
		li.style.backgroundColor = "#000000";
		firstX = li.dataset.x
		firstY = li.dataset.y
		checked = true;
	}
};

//---------------------------------------------------------------------
//Functions------------------------------------------------------------
//---------------------------------------------------------------------
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
			if(!showgrid){
				theGrid[i][j].style.borderColor = color;
			}
		}	
	}
}