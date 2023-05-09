var quill;

function createEditor() {
    if (quill) return;
    
    var textarea = document.getElementById("id_content")
    const editor = document.createElement("div")

    editor.id = "html-editor"
    editor.innerHTML = textarea.value
    textarea.parentElement.parentElement.insertBefore(editor, textarea.parentElement)

    quill = new Quill('#html-editor', {
        modules: {
            toolbar: [
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
                ['blockquote', 'code-block'],

                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                [{ 'script': 'sub' }, { 'script': 'super' }],      // superscript/subscript
                [{ 'indent': '-1' }, { 'indent': '+1' }],          // outdent/indent
                [{ 'direction': 'rtl' }],                         // text direction

                [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown

                [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
                [{ 'font': [] }],
                [{ 'align': [] }],

                // ['clean'],
                ['link'/* , 'image' */]
            ]/* ,
            image: {
                
            } */
        }, theme: 'snow'
    });

    const qleditor = document.querySelector('#html-editor .ql-editor')
    quill.on('text-change', () => {
        textarea.value = qleditor.innerHTML
    })
    setTimeout(() => {
        qleditor.style.width = "100% !important"
    }, 2000);
}

// contentMainButtons.push({ text: "Editor", do: createEditor, at: /add|change/g })
initFuncs.push(createEditor)
