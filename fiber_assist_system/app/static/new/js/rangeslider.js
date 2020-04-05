(function(factory) {
    window.rangeSlider = factory();
}(function() {
    'use strict';
    
    function init(target, min, max, cb) {
        var range = document.createElement('div');
        var start = document.createElement('input');
        var end = document.createElement('input');
        var left = document.createElement('span');
        var right = document.createElement('span');
        var btn = document.createElement('button');      
        var Slider = noUiSlider || {};
        var inputs = [start, end];
        var msgs = [left, right];
        var min = min || 0;
        var max = max || 0;
        var values = [min, max];
        var lock = false;
        
        values = [min, max];
        target.className = target.className + ' range-wrapper';
        range.className = 'range';
        start.className = 'range-linput';
        end.className = 'range-rinput';
        left.className = 'range-lmsg';
        right.className = 'range-rmsg';
        btn.className = 'range-btn';
        btn.innerText = '设为分析变量';
        target.appendChild(left);
        target.appendChild(right);
        target.appendChild(range);
        target.appendChild(start);
        target.appendChild(end);
        target.appendChild(btn);

        Slider.create(range, {
            start: [ min, max ],
            connect: true,
            range: {
                'min': min,
                'max': max,
            }
        });
        range.noUiSlider.on('update', function(newValues, index) {
            inputs[index].value = newValues[index];
            msgs[index].innerText = newValues[index];
            values[index] = newValues[index];
        });
        inputs.forEach(function(input, index) {
            input.addEventListener('change', function() {
                var r = [null, null];
                r[index] = this.value;
                range.noUiSlider.set(r);
            }, false);
        });
        btn.addEventListener('click', function() {
            if (lock) {
                lock = false;
                start.removeAttribute('disabled');
                end.removeAttribute('disabled');
                range.removeAttribute('disabled');
                range.querySelectorAll('.noUi-handle')[0].removeAttribute('disabled');
                range.querySelectorAll('.noUi-handle')[1].removeAttribute('disabled');
                range.querySelector('.noUi-connect').removeAttribute('disabled');
                cb(this,lock);
            } else {
                lock = true;
                var old_selected = $('.range-wrapper .selected');
                old_selected.click();
                start.setAttribute('disabled', true);
                end.setAttribute('disabled', true);
                range.setAttribute('disabled', true);
                range.querySelectorAll('.noUi-handle')[0].setAttribute('disabled', true);
                range.querySelectorAll('.noUi-handle')[1].setAttribute('disabled', true);
                range.querySelector('.noUi-connect').setAttribute('disabled', true);
                cb(this,lock);
            }
        });

        return {
            get: function() {
                return lock ? [] : values;
            }
        }
    }

    return {
        init: init,
    };
}));