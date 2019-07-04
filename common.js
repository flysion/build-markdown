$( document ).ready(function() {
    let body = $('body > div'), html = [];
    for(let i = 0; i < body.children().length; i++) {
        let child = body.children()[i];
        if(!/^H(\d+)$/.test(child.tagName)) {
            continue;
        }
        
        let n = parseInt(child.tagName.substr(1));
        if(n >= 4) continue;
        
        let text = $(child).text();
        
        html.push(str_repeat('&nbsp;&nbsp;&nbsp;', n - 1) + '<a href="#' + text + '">' + text + '</a>');

        $(child).prepend('<a name="' + text + '"></a>');
    }

    function str_repeat(str, len) {
        let s = '';
        for(let i = 0; i < len; i++) {
            s += str;
        }
        return s;
    }

    $('body').prepend('<div style="position:fixed;border:1px solid #737272;background-color:#e4e4e4;padding:5px;top:10px;left:' + (body.outerWidth() + 10 + body.offset().left) + 'px;">' + html.join('<br/>') + '</div>');
});