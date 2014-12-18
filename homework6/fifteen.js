'use strict';
window.onload = function(){
    var area = document.getElementById('puzzlearea');
    var pieces = puzzlearea.children;
    var size = 4;
    var shuffleBtn = document.getElementById('shufflebutton');
    var blank = document.createElement('div');
    var congratulation = document.createElement('div');
    var addBlank = function(){
        blank.classList.add('puzzlepiece');
        blank.style.backgroundImage = 'url()';
        // blank.style.top = Math.floor(pieces.length/size)*100+'px';
        // blank.style.left = pieces.length%size*100+'px';
        blank.style.visibility = 'hidden';
        area.appendChild(blank);
    }
    var resetPosition = function(){
        for (var index = 0; index < pieces.length; index++) {
            pieces[index].classList.add('puzzlepiece');
            pieces[index].style.top = Math.floor(index/size)*100+'px';
            pieces[index].style.left = index%size*100+'px';
        };
    }
    var changeBackground = function(){
        for (var index = 0; index < pieces.length; index++) {
            pieces[index].style.backgroundSize = '400px, 400px';
            pieces[index].style.backgroundPositionX = -index%size*100+'px';
            pieces[index].style.backgroundPositionY = -Math.floor(index/size)*100+'px';
        };
    }
    var isMovable = function(piece){
        return (blank.style.top == piece.style.top
            && Math.abs(parseInt(blank.style.left)-parseInt(piece.style.left)) == 100)
            || (blank.style.left == piece.style.left
            && Math.abs(parseInt(blank.style.top)-parseInt(piece.style.top)) == 100);
    }
    var lightMovable = function(){
        for (var index = 0; index < pieces.length; index++) {
            pieces[index].removeEventListener('click', move);
            if (isMovable(pieces[index])) {
                pieces[index].classList.add('movablepiece');
                pieces[index].addEventListener('click',move);
            } else {
                pieces[index].classList.remove('movablepiece');
            }
        };
    }
    var shuffle = function(event){
        var random;
        var count = 500;
        var movableIndxs = [];
        while (count) {
            for (var index = 0; index < pieces.length; index++) {
                if (isMovable(pieces[index])) {
                    movableIndxs.push(index);
                }  
            }
            random = movableIndxs[Math.round(Math.random(new Date()))*(movableIndxs.length-1)];
            pieces[random].click();
            movableIndxs = []
            count--;
        }
    }
    var isFinish = function(){
        var result = true;
        for (var index = 0; index < pieces.length; index++) {
            if (pieces[index].style.top !== Math.floor(index/size)*100+'px' ||
            pieces[index].style.left !== index%size*100+'px') {
                result = false;
                break;
            }
        }
        return result;
    }
    var congratulate = function(){
        congratulation.classList.add('puzzlepiece');
        congratulation.style.zIndex = '999';
        congratulation.style.top = '0px';
        congratulation.style.left = '0px';
        congratulation.style.width = '400px';
        congratulation.style.height = '400px';
        congratulation.style.backgroundPosition = '0px, 0px';
        congratulation.style.backgroundImage = 'url("congratulation.jpg")';
        area.appendChild(congratulation);
        setTimeout(function(){
            area.removeChild(congratulation);
        }, 1000)
    }
    var move = function(event){
        var piece = event.target;
        var tmptop = blank.style.top;
        blank.style.top = piece.style.top;
        piece.style.top= tmptop;        
        var tmpleft = blank.style.left;
        blank.style.left = piece.style.left;
        piece.style.left= tmpleft;
        lightMovable();
        if (event.x && isFinish()) {
            congratulate();
        };
    }
    shuffleBtn.addEventListener('click', shuffle);
    addBlank();
    resetPosition();
    changeBackground();
    lightMovable();
    // shufflebutton.click();
}