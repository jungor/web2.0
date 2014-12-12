'use strict';
window.onload = function (){
    var startBtn = document.getElementById('start');
    var stopBtn = document.getElementById('stop');
    var displayArea = document.getElementById('displayarea');
    var sizeField = document.getElementById('size');
    var sizes = document.getElementsByName('size');
    var speedBox = document.getElementsByName('speed')[0];
    var aniSlt = document.getElementsByName('animation')[0];
    var counter = 0;
    var speed = 200;
    var timer;

    stopBtn.disabled = true;

    var stopAni = function(text) {
        return function(){
            clearTimeout(timer);
            displayArea.value = text;
            startBtn.disabled = false;
            aniSlt.disabled = false;
        };
    };

    var startAni = function(){
        var oldText = displayArea.value;
        var animation = ANIMATIONS[document.getElementsByName('animation')[0].value].split('=====\n');
        var printAni = function(){
            displayArea.value = animation[counter];
            counter = (counter+1)%animation.length;
            timer = setTimeout(printAni, speed);
        };
        printAni();
        stopBtn.disabled = false;
        startBtn.disabled = true;
        aniSlt.disabled = true;
        stopBtn.addEventListener('click', stopAni(oldText));
    };

    var changeSize = function(){
        for(var i=0; i < sizes.length; i++){
            if(sizes[i].checked){
                displayArea.classList.remove('samll', 'medium', 'large');
                displayArea.classList.add(sizes[i].value);
                break;
            }
        }
    };

    var changeSpeed = function(){
        if (speedBox.checked) {
            speed = 50;
        } else {
            speed = 200;
        }
    };

    startBtn.addEventListener('click', startAni);
    sizeField.addEventListener('change', changeSize);
    speedBox.addEventListener('change', changeSpeed);
};


