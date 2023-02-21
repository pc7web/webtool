var p = [],
    indentConfig = {
        tab: { char: '\t', size: 1 },
        space: { char: ' ', size: 4 }
    },
    configDefault = {
        type: 'tab'
    },
    push = function (m) { return '\\' + p.push(m) + '\\'; },
    pop = function (m, i) { return p[i - 1] },
    tabs = function (count, indentType) { return new Array(count + 1).join(indentType); };

function JSONFormat(json, indentType) {
    p = [];
    var out = "",
        indent = 0;

    // Extract backslashes and strings
    json = json
        .replace(/\\./g, push)
        .replace(/(".*?"|'.*?')/g, push)
        .replace(/\s+/, '');

    // Indent and insert newlines
    for (var i = 0; i < json.length; i++) {
        var c = json.charAt(i);

        switch (c) {
            case '{':
            case '[':
                out += c + "\n" + tabs(++indent, indentType);
                break;
            case '}':
            case ']':
                out += "\n" + tabs(--indent, indentType) + c;
                break;
            case ',':
                out += ",\n" + tabs(indent, indentType);
                break;
            case ':':
                out += ": ";
                break;
            default:
                out += c;
                break;
        }
    }

    // Strip whitespace from numeric arrays and put backslashes 
    // and strings back in
    out = out
        .replace(/\[[\d,\s]+?\]/g, function (m) { return m.replace(/\s/g, ''); })
        .replace(/\\(\d+)\\/g, pop) // strings
        .replace(/\\(\d+)\\/g, pop); // backslashes in strings

    return out;
};

function json_formatter(json, config) {
    config = config || configDefault;
    var indent = indentConfig[config.type];

    if (indent == null) {
        throw new Error('Unrecognized indent type: "' + config.type + '"');
    }
    var indentType = new Array((config.size || indent.size) + 1).join(indent.char);
    return JSONFormat(JSON.stringify(json), indentType);
}


// let toJson = true
// var jsonData = {
//     get() {
//         return sessionStorage.getItem(document.location.pathname)
//     },
//     set(value) {
//         sessionStorage.setItem(document.location.pathname, value)
//     }
// }

var timeOutObj;
function format_data() {
    clearTimeout(timeOutObj)
    timeOutObj = setTimeout(() => {
        let el = document.getElementById('id_data')
        if (!el) {
            let query = prompt('Enter element id: ')
            el = document.getElementById(query)
            if (!el)
                return;
        }

        // if (!jsonData.get())
        //     jsonData.set(el.value)

        try {
            // if (toJson) {
            //     jsonData.set(el.value)
            el.value = json_formatter(JSON.parse(el.value))
            //     toJson = !toJson
            // } else {
            //     const res = confirm('Undo format?')
            //     if (res) {
            //         el.value = jsonData.get()
            //         toJson = !toJson
            //     }
            // }
        } catch (er) {
            alert(er)
        }
    },
        500);
}

function createEditor() {
    // //cdn.quilljs.com/1.3.6/quill.snow.css
    var textarea = document.getElementById("id_data")
    const editor = document.createElement("div")
    editor.id = "json-editor"
    // editor.innerHTML = "sfsdfsdf"
    textarea.parentElement.appendChild(editor)
    var quill = new Quill('#json-editor', {
        // modules: {
        //     toolbar: '#toolbar'
        // },
        theme: 'snow'
    });
    // textarea.parentElement.insertBefore(editor, textarea)
    // console.log(
    //     );
}

contentMainButtons.push({ text: "Format json", do: format_data, at: /add|change/g })
contentMainButtons.push({ text: "Editor", do: createEditor, at: /add|change/g })

// setTimeout(() => {
//     createEditor()
// }, 500);
