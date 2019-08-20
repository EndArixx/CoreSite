const twelve = 12

var theGrid = new Array(twelve);

for (var i = 0; i < theGrid.length; i++) {
  theGrid[i] = new Array(twelve);
}

var h = 1; 

for (var i = 0; i < twelve; i++) { 
    for (var j = 0; j < twelve; j++) { 
        theGrid[i][j] = h++; 
    } 
} 

const palette = document.getElementById('palette'), nameSpan = document.getElementById('name'), hexSpan=document.getElementById('hex');

for (var i = 0; i < twelve; i++) { 
    for (var j = 0; j < twelve; j++) { 
        //document.write(theGrid[i][j] + " "); 
		const li = document.createElement('li');
		li.title = "grid" +theGrid[i][j];
		li.style.backgroundColor = '#F5F5F5';
		palette.appendChild(li);
    } 
}  

palette.onclick = e => {
  const li = e.target;
  if (palette.active) palette.active.className = palette.active.className.replace(' active', '');
  palette.active=li;
  li.className+=' active';
  li.style.backgroundColor = '#008080';
};