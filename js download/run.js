console.log("page started")

var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = "//code.jquery.com/jquery-2.2.1.min.js";

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script.onreadystatechange = handler;
    script.onload = handler;

    // Fire the loading
    head.appendChild(script);

    function handler(){
       console.log('jquery added :)');
    }

    var script2 = document.createElement('script');
    script2.type = 'text/javascript';
    script2.src = chrome.runtime.getURL("convert.js");

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script2.onreadystatechange = handler;
    script2.onload = handler;

    // Fire the loading
    head.appendChild(script2);

    function handler(){
       console.log('convert added)');
    }


