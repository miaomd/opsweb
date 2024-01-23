import{c as M}from"./3024-night.4988d41a.js";(function(x,_){(function(s){s(M.exports)})(function(s){var d="CodeMirror-lint-markers",h="CodeMirror-lint-line-";function c(t,e,o){var n=document.createElement("div");n.className="CodeMirror-lint-tooltip cm-s-"+t.options.theme,n.appendChild(o.cloneNode(!0)),t.state.lint.options.selfContain?t.getWrapperElement().appendChild(n):document.body.appendChild(n);function i(r){if(!n.parentNode)return s.off(document,"mousemove",i);n.style.top=Math.max(0,r.clientY-n.offsetHeight-5)+"px",n.style.left=r.clientX+5+"px"}return s.on(document,"mousemove",i),i(e),n.style.opacity!=null&&(n.style.opacity=1),n}function v(t){t.parentNode&&t.parentNode.removeChild(t)}function w(t){!t.parentNode||(t.style.opacity==null&&v(t),t.style.opacity=0,setTimeout(function(){v(t)},600))}function p(t,e,o,n){var i=c(t,e,o);function r(){s.off(n,"mouseout",r),i&&(w(i),i=null)}var a=setInterval(function(){if(i)for(var l=n;;l=l.parentNode){if(l&&l.nodeType==11&&(l=l.host),l==document.body)return;if(!l){r();break}}if(!i)return clearInterval(a)},400);s.on(n,"mouseout",r)}function A(t,e,o){this.marked=[],e instanceof Function&&(e={getAnnotations:e}),(!e||e===!0)&&(e={}),this.options={},this.linterOptions=e.options||{};for(var n in y)this.options[n]=y[n];for(var n in e)y.hasOwnProperty(n)?e[n]!=null&&(this.options[n]=e[n]):e.options||(this.linterOptions[n]=e[n]);this.timeout=null,this.hasGutter=o,this.onMouseOver=function(i){D(t,i)},this.waitingFor=0}var y={highlightLines:!1,tooltips:!0,delay:500,lintOnChange:!0,getAnnotations:null,async:!1,selfContain:null,formatAnnotation:null,onUpdateLinting:null};function T(t){var e=t.state.lint;e.hasGutter&&t.clearGutter(d),e.options.highlightLines&&b(t);for(var o=0;o<e.marked.length;++o)e.marked[o].clear();e.marked.length=0}function b(t){t.eachLine(function(e){var o=e.wrapClass&&/\bCodeMirror-lint-line-\w+\b/.exec(e.wrapClass);o&&t.removeLineClass(e,"wrap",o[0])})}function F(t,e,o,n,i){var r=document.createElement("div"),a=r;return r.className="CodeMirror-lint-marker CodeMirror-lint-marker-"+o,n&&(a=r.appendChild(document.createElement("div")),a.className="CodeMirror-lint-marker CodeMirror-lint-marker-multiple"),i!=!1&&s.on(a,"mouseover",function(l){p(t,l,e,a)}),r}function G(t,e){return t=="error"?t:e}function I(t){for(var e=[],o=0;o<t.length;++o){var n=t[o],i=n.from.line;(e[i]||(e[i]=[])).push(n)}return e}function O(t){var e=t.severity;e||(e="error");var o=document.createElement("div");return o.className="CodeMirror-lint-message CodeMirror-lint-message-"+e,typeof t.messageHTML!="undefined"?o.innerHTML=t.messageHTML:o.appendChild(document.createTextNode(t.message)),o}function j(t,e){var o=t.state.lint,n=++o.waitingFor;function i(){n=-1,t.off("change",i)}t.on("change",i),e(t.getValue(),function(r,a){t.off("change",i),o.waitingFor==n&&(a&&r instanceof s&&(r=a),t.operation(function(){C(t,r)}))},o.linterOptions,t)}function k(t){var e=t.state.lint;if(!!e){var o=e.options,n=o.getAnnotations||t.getHelper(s.Pos(0,0),"lint");if(!!n)if(o.async||n.async)j(t,n);else{var i=n(t.getValue(),e.linterOptions,t);if(!i)return;i.then?i.then(function(r){t.operation(function(){C(t,r)})}):t.operation(function(){C(t,i)})}}}function C(t,e){var o=t.state.lint;if(!!o){var n=o.options;T(t);for(var i=I(e),r=0;r<i.length;++r){var a=i[r];if(!!a){var l=[];a=a.filter(function(N){return l.indexOf(N.message)>-1?!1:l.push(N.message)});for(var f=null,g=o.hasGutter&&document.createDocumentFragment(),L=0;L<a.length;++L){var u=a[L],m=u.severity;m||(m="error"),f=G(f,m),n.formatAnnotation&&(u=n.formatAnnotation(u)),o.hasGutter&&g.appendChild(O(u)),u.to&&o.marked.push(t.markText(u.from,u.to,{className:"CodeMirror-lint-mark CodeMirror-lint-mark-"+m,__annotation:u}))}o.hasGutter&&t.setGutterMarker(r,d,F(t,g,f,i[r].length>1,n.tooltips)),n.highlightLines&&t.addLineClass(r,"wrap",h+f)}}n.onUpdateLinting&&n.onUpdateLinting(e,i,t)}}function E(t){var e=t.state.lint;!e||(clearTimeout(e.timeout),e.timeout=setTimeout(function(){k(t)},e.options.delay))}function H(t,e,o){for(var n=o.target||o.srcElement,i=document.createDocumentFragment(),r=0;r<e.length;r++){var a=e[r];i.appendChild(O(a))}p(t,o,i,n)}function D(t,e){var o=e.target||e.srcElement;if(!!/\bCodeMirror-lint-mark-/.test(o.className)){for(var n=o.getBoundingClientRect(),i=(n.left+n.right)/2,r=(n.top+n.bottom)/2,a=t.findMarksAt(t.coordsChar({left:i,top:r},"client")),l=[],f=0;f<a.length;++f){var g=a[f].__annotation;g&&l.push(g)}l.length&&H(t,l,e)}}s.defineOption("lint",!1,function(t,e,o){if(o&&o!=s.Init&&(T(t),t.state.lint.options.lintOnChange!==!1&&t.off("change",E),s.off(t.getWrapperElement(),"mouseover",t.state.lint.onMouseOver),clearTimeout(t.state.lint.timeout),delete t.state.lint),e){for(var n=t.getOption("gutters"),i=!1,r=0;r<n.length;++r)n[r]==d&&(i=!0);var a=t.state.lint=new A(t,e,i);a.options.lintOnChange&&t.on("change",E),a.options.tooltips!=!1&&a.options.tooltips!="gutter"&&s.on(t.getWrapperElement(),"mouseover",a.onMouseOver),k(t)}}),s.defineExtension("performLint",function(){k(this)})})})();(function(x,_){(function(s){s(M.exports)})(function(s){s.registerHelper("lint","json",function(d){var h=[];if(!window.jsonlint)return window.console&&window.console.error("Error: window.jsonlint not defined, CodeMirror JSON linting cannot run."),h;var c=window.jsonlint.parser||window.jsonlint;c.parseError=function(v,w){var p=w.loc;h.push({from:s.Pos(p.first_line-1,p.first_column),to:s.Pos(p.last_line-1,p.last_column),message:v})};try{c.parse(d)}catch{}return h})})})();
