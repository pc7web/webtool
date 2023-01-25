contentMainButtons.push({
    text: "draft", do: () => {
        let values = {}
        let inputs = document.getElementsByTagName('input')
        let textareas = document.getElementsByTagName('textarea')
        for (let i = 0; i < inputs.length; i++) {
            const el = inputs[i];
            if (!el.name.startsWith('_'))
                values[el.name] = el.value
        }
        for (let i = 0; i < textareas.length; i++) {
            const el = textareas[i];
            values[el.name] = el.value
        }
        delete values["csrfmiddlewaretoken"]
        sessionStorage.setItem(document.location.pathname, JSON.stringify(values));
    }, at: /add|change/g
})
contentMainButtons.push({
    text: "load", do: () => {
        let values = JSON.parse(sessionStorage.getItem(document.location.pathname) ?? '{}');
        let inputs = document.getElementsByTagName('input')
        let textareas = document.getElementsByTagName('textarea')
        for (let i = 0; i < inputs.length; i++) {
            const el = inputs[i];
            if (values[el.name]) {
                el.value = values[el.name]
            }
        }
        for (let i = 0; i < textareas.length; i++) {
            const el = textareas[i];
            if (values[el.name]) {
                el.value = values[el.name]
            }
        }
        delete values["csrfmiddlewaretoken"]
    }, at: /add|change/g
})
