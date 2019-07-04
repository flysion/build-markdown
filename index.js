window.onload = function() {
    var indexEl = document.createElement("DIV");
    indexEl.className = 'index';
    
    var content = document.querySelector('#content');
    for(var i = 0; i < content.children.length; i++) {
        var child = content.children[i];
        if(!/^(H|h)(\d+)$/.test(child.tagName)) {
            continue;
        }

        var n = parseInt(child.tagName.substr(1));
        if(n > indexMaxDepth) {
            continue;
        }
        
        var anchor = 't-' + i;
    
        var link = document.createElement("A");
        link.href = '#' + anchor;
        link.innerText = child.innerText;
        
        var div = document.createElement("DIV");
        div.className = 'index-' + n;
        div.appendChild(link);

        child.innerHTML = '<a name="'+anchor+'">'+child.innerHTML+'</a>';

        indexEl.appendChild(div);
    }
    
    document.body.appendChild(indexEl);
};