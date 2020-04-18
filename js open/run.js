//https://www.tab4u.com/resultsSimple?tab=songs&q=&type=&cat=&content=&max_chords=0&n=30&sort=&s=0





for(var j = 2; j < 34; j++){

	
	try{		
	song = document.querySelector("#page_content > div:nth-child(2) > table> tbody > tr:nth-child(" + j.toString() + ") > td.songTd1 > a").getAttribute("href").toString();

	urlSaver += song + '\n' ;
	console.log(j);
	window.open(song);
	browser.tabs.move(0)
	}catch{}
}



if(isNaN(url[len - 2])){ console.log("1"); window.location.href = url.slice(0, len-1) + "30";}
else{
if(isNaN(url[len - 3])) {console.log("2"); window.location.href = url.slice(0, len-2)+ (parseInt(url.slice(len -2, len)) + 30);}
else{
if(isNaN(url[len - 4])) {console.log("3"); window.location.href = url.slice(0, len-3)+ (parseInt(url.slice(len -3, len)) + 30);}
else{
if(isNaN(url[len - 5])) {console.log("4"); window.location.href = url.slice(0, len-4)+ (parseInt(url.slice(len -4, len)) + 30);}
}
}
}



// Function to download data to a file
function download(data, filename, type) {
    var file = new Blob([data], {type: type});
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
