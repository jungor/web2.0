;
$(function() {
    var puzzleSize = 4;
    var areaWidth = 400;
    var puzzleImg = 'url("sao.jpg")';
    var currentsteps = 0;
    var starttime = null;
    var stoptime = null;
    var $area = $('#puzzlearea');
    var $pieces = $area.children();
    var $shuffleBtn = $('#shufflebutton');
    var $imgSlt = $('<select name="image" id="imageselect"><option value="sao" selected="selected">sao</option><option value="alo">alo</option><option value="ggo">ggo</option><option value="uw">uw</option></select>');
    var $blank = $('<div></div>');
    var set = function(event) {
        steps = 0;
        puzzleImg = 'url(' + $imgSlt.val() + '.jpg)';
        $blank.css({
            'top': '300px',
            'left': '300px'
        });
        $pieces.each(function(index, el) {
            $(el).off('click', move).removeClass('movablepiece').addClass('puzzlepiece').css({
                'top': Math.floor(index / puzzleSize) * (areaWidth / puzzleSize) + 'px',
                'left': index % puzzleSize * (areaWidth / puzzleSize) + 'px',
                'background-size': '400px 400px',
                'background-image': puzzleImg,
                'background-position': -index % puzzleSize * (areaWidth / puzzleSize) + 'px ' + -Math.floor(index / puzzleSize) * (areaWidth / puzzleSize) + 'px',
                'user-select': 'none'
            });
        });
    }
    var isMovable = function(piece) {
        return ($blank.css('top') === piece.css('top') && Math.abs(parseInt($blank.css('left')) - parseInt(piece.css('left'))) === (areaWidth / puzzleSize)) || ($blank.css('left') === piece.css('left') && Math.abs(parseInt($blank.css('top')) - parseInt(piece.css('top'))) === (areaWidth / puzzleSize));
    }
    var isFinish = function() {
        var result = true;
        $pieces.each(function(index, el) {
            if ($(el).css('top') !== Math.floor(index / puzzleSize) * (areaWidth / puzzleSize) + 'px' ||
                $(el).css('left') !== index % puzzleSize * (areaWidth / puzzleSize) + 'px') {
                result = false;
            };
        });
        return result;
    }
    var lightMovable = function() {
        $pieces.each(function(index, el) {
            $(el).off('click', move).removeClass('movablepiece');
            if (isMovable($(el))) {
                $(el).on('click', move).addClass('movablepiece');
            }
        });
    }
    var congratulate = function() {
        $pieces.css('display', 'none');
        $area.css('background-image', 'url(congratulation.jpg)');
        alert('Your steps: ' + steps + '\nYour time: ' + (stoptime - starttime || stoptime) / 1000 + 's');
        setTimeout(function() {
            steps = 0;
            $area.css('background-image', '');
            $pieces.css('display', 'block').off('click', move).removeClass('movablepiece');
        }, 1000)
    }
    var move = function(event) {
        var $piece = $(event.target);
        var tmpcss = {
            'top': $blank.css('top'),
            'left': $blank.css('left')
        };
        $blank.css({
            'top': $piece.css('top'),
            'left': $piece.css('left')
        });
        if (event.clientX) {
            steps++;
            $piece.animate(tmpcss, 100, function() {
                lightMovable();
                if (isFinish()) {
                    stoptime = new Date();
                    congratulate();
                }
            });
        } else {
            $piece.css(tmpcss);
            lightMovable();
        };
    }
    var shuffle = function(event) {
        lightMovable();
        starttime = new Date();
        var count = 201; // count must be odd io prevent finishing
        while (count--) {
            $('.movablepiece').get(Math.round(Math.random() * ($('.movablepiece').length - 1))).click();
        }
    }
    $shuffleBtn.on('click', shuffle);
    $imgSlt.on('change', set).appendTo('#controls');
    set();
});
