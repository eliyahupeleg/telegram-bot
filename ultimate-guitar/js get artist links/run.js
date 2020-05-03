// if the last page of this letter, go to next letter.
if (document.getElementsByClassName('pZcWD').length == 0){
    window.location.href.slice(0,38) + String.fromCharCode(window.location.href.slice(38,39).charCodeAt(0)+1) + ".htm"
}

//if not, download the links and go to next page.
else {

    //all the artist bars.
    artists = document.getElementsByClassName('wSTi6');

    //string to save the links.
    var links = "";

    //extract the link from the html.
    for ( var a of artists){
        links += a.children[0].href + "\n"
    }
    
    //save the links to file.
    download(links, window.location.href.slice(38,-4), String)
    
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

    if(window.location.href.slice(39,-4) != "") {window.location.href = window.location.href.slice(0,39) + String(parseInt(parseInt(window.location.href.slice(39,-4)) + 1)) + ".htm"}
    else{window.location.href = window.location.href.slice(0,39) + window.location.href.slice(39,-4) + 1 + ".htm"}

}
