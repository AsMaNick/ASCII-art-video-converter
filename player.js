var slider = document.getElementById("slider");
var current_frame, start_pos, pause, timeout_id, content, len, slider_down;
var speeds = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2], current_speed = 3;
var FPS = 30;
var delay = 1000 / FPS;

function loadFile(event) {
    var input = event.target;
    if ('files' in input && input.files.length > 0) {
        readFileContent(input.files[0]).then(file_content => {
            content = file_content;
            showVideo();
        });
    }
}

function get_time(t) {
    var m = parseInt(t / 60);
    var s = t % 60;
    m = m.toString();
    s = s.toString();
    if (m.length < 2) {
        m = "0" + m;
    }
    if (s.length < 2) {
        s = "0" + s;
    }
    return m + ":" + s;
}

function get_time_label(frame_id, total_frames) {
    var t_total = parseInt(total_frames / FPS);
    var t_cur = parseInt((frame_id + 1) / total_frames * t_total);
    return get_time(t_cur) + ' / ' + get_time(t_total);
}

function showFrame(target, is_first_frame) {
    if (pause && !is_first_frame) {
        return;
    }
    var pos = start_pos + current_frame * len;
    var frame_id = current_frame;
    var total_frames = parseInt(content.length / len);
    document.getElementById("time").innerHTML = get_time_label(frame_id, total_frames);
    if (!slider_clicked) {
        slider.value = frame_id;
    }
    target.innerHTML = content.substr(pos, len).split('\n').join('<br>').split(' ').join('&nbsp');
    current_frame += 1;
    if (current_frame < total_frames) {
        timeout_id = setTimeout(function() { showFrame(target, false) }, delay / speeds[current_speed]);
    }
}

function isDigit(character) {
    return '0' <= character && character <= '9';
}

function parseMetaInformation(content) {
    var pos = 0, h = '', w = '';
    while (pos < content.length && isDigit(content[pos])) {
        h += content[pos];
        ++pos;
    }
    ++pos;
    while (pos < content.length && isDigit(content[pos])) {
        w += content[pos];
        ++pos;
    }
    pos += 2;
    h = parseInt(h);
    w = parseInt(w);
    var meta = {
        'h': h,
        'w': w,
        'start_pos': pos
    }
    return meta;
}

function showVideo() {
    content = content.split('\r\n').join('\n')
    var target = document.getElementById('screen');
    var meta = parseMetaInformation(content);
    var h = meta.h, w = meta.w;
    len = h * (w + 1) + 1;
    var total_frames = parseInt(content.length / len);
    slider.min = 0;
    slider.max = total_frames - 1;
    slider.value = 0;
    start_pos = meta.start_pos;
    current_frame = 0;
    pause = false;
    slider_clicked = false;
    showFrame(target, true);
}

function readFileContent(file) {
    var reader = new FileReader();
    return new Promise((resolve, reject) => {
        reader.onload = event => resolve(event.target.result)
        reader.onerror = error => reject(error)
        reader.readAsText(file)
    })
}

function pauseClick() {
    var pause_img = document.getElementById("pause_img");
    if (pause_img.src.indexOf("pause.png") != -1) {
        clearTimeout(timeout_id);
        pause = true;
        pause_img.src = pause_img.src.replace("pause.png", "play.png");
    } else {
        pause_img.src = pause_img.src.replace("play.png", "pause.png");
        pause = false;
        showFrame(document.getElementById('screen'), true);
    }
}

function sliderMouseDown() {
    slider_clicked = true;
}

function sliderMouseUp() {
    slider_clicked = false;
    clearInterval(timeout_id);
    current_frame = parseInt(slider.value);
    showFrame(document.getElementById('screen'), true);
}

function speedDownClick() {
    if (current_speed > 0) {
        current_speed -= 1;
    }
    document.getElementById('speed').innerHTML = 'x' + speeds[current_speed].toFixed(2);
}

function speedUpClick() {
    if (current_speed + 1 < speeds.length) {
        current_speed += 1;
    }
    document.getElementById('speed').innerHTML = 'x' + speeds[current_speed].toFixed(2);
}

function loadFromURL() {
    var url = document.getElementById("url").value;
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.send(null);
    request.onreadystatechange = function () {
        console.log(request);
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                content = request.responseText;
                showVideo();
            }
        }
    }
}