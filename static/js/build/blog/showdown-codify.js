//
//  Codify Extension for google-code-prettify
//  ```c printf("Hello!")``` -> <pre class="prettyprint lang-c>printf("Hello!")</pre>
//

(function () {
    var codify = function (converter) {
        return [{
            type: 'output',
            filter: function (text) {
                return text.replace(/(<pre>)?<code\s?(class="(\w+)")?>/gi, function(match, pre, cls, lang) {
                    if (pre) {
                        if (lang) {
                            return '<pre class="prettyprint linenums lang-' + lang + '" tabIndex="0"><code data-inner="1">';
                        } else {
                            return '<pre class="prettyprint linenums" tabIndex="0"><code data-inner="1">';
                        }
                    } else {
                        if (lang) {
                            return '<code class="prettyprint lang-' + lang + '">';
                        } else {
                            return '<code class="prettyprint">';
                        }
                    }
                });
            }
        }];
    };
    // Client-side export
    if (typeof window !== 'undefined' && window.Showdown && window.Showdown.extensions) {
        window.Showdown.extensions.codify = codify;
    }
    // Server-side export
    if (typeof module !== 'undefined') module.exports = codify;
}());
