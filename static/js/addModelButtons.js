var contentMainButtons = []
var initFuncs = []
// contentMainButtons.push({ text: "Format json", do: format_data, at: '/change' | '/[model_name]' })

function addBtns() {
    var contentMain = document.querySelector("#content-main > ul")
    if (!contentMain) {
        const el = document.createElement('ul')
        document.getElementById('content-main').appendChild(el)
        contentMain = document.querySelector("#content-main > ul")
    }
    contentMainButtons.forEach((btn) => {
        if (btn.at) {
            if (document.location.pathname.search(btn.at) < 0)
                return;
        }
        const li = document.createElement("li")
        const a = document.createElement("a")
        a.href = "javascript:;"
        a.onclick = btn.do
        a.text = btn.text
        li.appendChild(a)
        contentMain.appendChild(li);
    })
}
initFuncs.push(addBtns)

function windowInit() {
    initFuncs.forEach(func => {
        func()
    })
}

window.addEventListener("load", windowInit)
