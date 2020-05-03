//if not, download the links and go to next page.


//all the artist bars.
artists = document.getElementsByClassName('_2hJom');

//string to save the links.
var links = "";

//extract the link from the html.
for ( var a of artists){
    links += a.children[0].children[0].children[0].href + "\n"
}


function save(){
    if(document.getElementsByClassName('_2Yr6L _1_yTk')[0] != null){
        download(links, document.getElementsByClassName('_2Yr6L _1_yTk')[0].textContent.replace(" Chords & Tabs", ""), String)
        if(document.getElementsByClassName('_2kTPR _1nJLO _3sEsO _2KJtL _1ofov kWOod')[0] != null){document.getElementsByClassName('_2kTPR _1nJLO _3sEsO _2KJtL _1ofov kWOod')[0].click()}
    }
}
setTimeout(save, 1000);

//save the links to file.


// Function to download data to a file
function download(data, filename, type) {
    const file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);  
        }, 0); 
    }
}

