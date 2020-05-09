Array.prototype.last = function() {
    if(this.length === 0) return undefined;
    return this[this.length - 1];
};

function hTree(el) {
    var tree = [];
    var nodes = [];
    var prev = null;

    for(var i = 0; i < el.children.length; i++) {
        var child = el.children[i];
        if(!/^(H|h)(\d+)$/.test(child.tagName)) {
            continue;
        }

        var n = parseInt(child.tagName.substr(1));
        var node = {n: n, name: child.innerText, el: child, children: []};
        
        if(prev === null) {
            tree.push(node);
        } else if(n > prev.n) {
            prev.children.push(node);
            nodes.push(prev);
        } else if(n == prev.n) {
            nodes.last().children.push(node);
        } else {
            while(nodes.last().n >= n) {
                nodes.pop();
            }
            
            nodes.last().children.push(node);
            nodes.push(node);
        }
        
        prev = node;
    }

    return tree;
}

function contentIndex(el, tree, pNo = '', depth = 0)
{
    if(depth + 1 > maxIndexDepth) return;
    
    for(var i = 0; i < tree.length; i++) {
        var node = tree[i];
        
        var no = (pNo === '' ? ('' + (i+1)) : (pNo + '.' + (i+1)));
        var anchorName = no + '-' + node.name;
        
        var link = document.createElement("A");
        link.href = '#' + anchorName;
        link.innerHTML = '<span class="index-no">' + no + '</span>' + ' ' + node.name;
        
        var div = document.createElement("DIV");
        div.className = 'index-' + depth;
        div.appendChild(link);
        el.appendChild(div);
        
        node.el.innerHTML = '<a name="' + anchorName + '">' + node.el.innerHTML + '</a>';

        contentIndex(el, node.children, no, depth + 1);
    }
}

window.onload = function() {
    var tree = hTree(document.querySelector('#content'));
    var el = document.createElement("DIV");
    contentIndex(el, tree);
    el.className = 'index';
    document.body.appendChild(el);
};

window.onbeforeprint = function() {
    document.querySelector('.index').style.display = 'none';
};

window.onafterprint = function() {
    document.querySelector('.index').style.display = 'block';
};