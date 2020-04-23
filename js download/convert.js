const chrds = ["A#6add9", "Ab6add9", "A#add9", "A#dim7", "A#m7b5", "A#maj7", "A#maj9", "A#sus2", "A#sus4", "A6add9", "Abadd9", "Abdim7", "Abm7b5", "Abmaj7", "Abmaj9", "Absus2", "Absus4", "A#7#5", "A#7b5", "A#7b9", "A#aug", "A#dim", "A#m11", "Aadd9", "Ab7#5", "Ab7b5", "Ab7b9", "Abaug", "Abdim", "Abm11", "Adim7", "Am7b5", "Amaj7", "Amaj9", "Asus2", "Asus4", "A#11", "A#13", "A#m6", "A#m7", "A#m9", "A7#5", "A7b5", "A7b9", "Aaug", "Ab11", "Ab13", "Abm6", "Abm7", "Abm9", "Adim", "Am11", "A#6", "A#7", "A#9", "A#m", "A11", "A13", "Ab6", "Ab7", "Ab9", "Abm", "Am6", "Am7", "Am9", "A#", "A6", "A7", "A9", "Ab", "Am", "A", "Bb6add9", "B6add9", "Bbadd9", "Bbdim7", "Bbm7b5", "Bbmaj7", "Bbmaj9", "Bbsus2", "Bbsus4", "Badd9", "Bb7#5", "Bb7b5", "Bb7b9", "Bbaug", "Bbdim", "Bbm11", "Bdim7", "Bm7b5", "Bmaj7", "Bmaj9", "Bsus2", "Bsus4", "B7#5", "B7b5", "B7b9", "Baug", "Bb11", "Bb13", "Bbm6", "Bbm7", "Bbm9", "Bdim", "Bm11", "B11", "B13", "Bb6", "Bb7", "Bb9", "Bbm", "Bm6", "Bm7", "Bm9", "B6", "B7", "B9", "Bb", "Bm", "B", "C#6add9", "C#add9", "C#dim7", "C#m7b5", "C#maj7", "C#maj9", "C#sus2", "C#sus4", "C6add9", "C#7#5", "C#7b5", "C#7b9", "C#aug", "C#dim", "C#m11", "Cadd9", "Cdim7", "Cm7b5", "Cmaj7", "Cmaj9", "Csus2", "Csus4", "C#11", "C#13", "C#m6", "C#m7", "C#m9", "C7#5", "C7b5", "C7b9", "Caug", "Cdim", "Cm11", "C#6", "C#7", "C#9", "C#m", "C11", "C13", "Cm6", "Cm7", "Cm9", "C#", "C6", "C7", "C9", "Cm", "C", "C", "D#6add9", "Db6add9", "D#add9", "D#dim7", "D#m7b5", "D#maj7", "D#maj9", "D#sus2", "D#sus4", "D6add9", "Dbadd9", "Dbdim7", "Dbm7b5", "Dbmaj7", "Dbmaj9", "Dbsus2", "Dbsus4", "D#7#5", "D#7b5", "D#7b9", "D#aug", "D#dim", "D#m11", "Dadd9", "Db7#5", "Db7b5", "Db7b9", "Dbaug", "Dbdim", "Dbm11", "Ddim7", "Dm7b5", "Dmaj7", "Dmaj9", "Dsus2", "Dsus4", "D#11", "D#13", "D#m6", "D#m7", "D#m9", "D7#5", "D7b5", "D7b9", "Daug", "Db11", "Db13", "Dbm6", "Dbm7", "Dbm9", "Ddim", "Dm11", "D#6", "D#7", "D#9", "D#m", "D11", "D13", "Db6", "Db7", "Db9", "Dbm", "Dm6", "Dm7", "Dm9", "D#", "D6", "D7", "D9", "Db", "Dm", "D", "Eb6add9", "E6add9", "Ebadd9", "Ebdim7", "Ebm7b5", "Ebmaj7", "Ebmaj9", "Ebsus2", "Ebsus4", "Eadd9", "Eb7#5", "Eb7b5", "Eb7b9", "Ebaug", "Ebdim", "Ebm11", "Edim7", "Em7b5", "Emaj7", "Emaj9", "Esus2", "Esus4", "E7#5", "E7b5", "E7b9", "Eaug", "Eb11", "Eb13", "Ebm6", "Ebm7", "Ebm9", "Edim", "Em11", "E11", "E13", "Eb6", "Eb7", "Eb9", "Ebm", "Em6", "Em7", "Em9", "E6", "E7", "E9", "Eb", "Em", "E", "F#6add9", "F#add9", "F#dim7", "F#m7b5", "F#maj7", "F#maj9", "F#sus2", "F#sus4", "F6add9", "F#7#5", "F#7b5", "F#7b9", "F#aug", "F#dim", "F#m11", "Fadd9", "Fdim7", "Fm7b5", "Fmaj7", "Fmaj9", "Fsus2", "Fsus4", "F#11", "F#13", "F#m6", "F#m7", "F#m9", "F7#5", "F7b5", "F7b9", "Faug", "Fdim", "Fm11", "F#6", "F#7", "F#9", "F#m", "F11", "F13", "Fm6", "Fm7", "Fm9", "F#", "F6", "F7", "F9", "Fm", "F", "G#6add9", "Gb6add9", "G#add9", "G#dim7", "G#m7b5", "G#maj7", "G#maj9", "G#sus2", "G#sus4", "G6add9", "Gbadd9", "Gbdim7", "Gbm7b5", "Gbmaj7", "Gbmaj9", "Gbsus2", "Gbsus4", "G#7#5", "G#7b5", "G#7b9", "G#aug", "G#dim", "G#m11", "Gadd9", "Gb7#5", "Gb7b5", "Gb7b9", "Gbaug", "Gbdim", "Gbm11", "Gdim7", "Gm7b5", "Gmaj7", "Gmaj9", "Gsus2", "Gsus4", "G#11", "G#13", "G#m6", "G#m7", "G#m9", "G7#5", "G7b5", "G7b9", "Gaug", "Gb11", "Gb13", "Gbm6", "Gbm7", "Gbm9", "Gdim", "Gm11", "G#6", "G#7", "G#9", "G#m", "G11", "G13", "Gb6", "Gb7", "Gb9", "Gbm", "Gm6", "Gm7", "Gm9", "G#", "G6", "G7", "G9", "Gb", "Gm", "G"];

if(document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.bArae4 > a")){
hrf = document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.bArae4 > a").href;}
else hrf = window.location.href;

if(hrf.length >= 51 && ! document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.bArae4 > span")){
	try{
		window.open(document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.bArae4 > a").href)
	} catch (error) {
		console.log(error)
	}
}else{

capo = "";

if(document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.song_block_content > div > p")) capo = String.fromCharCode(160) + jQuery('<center>').html(document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.song_block_content > div > p")).text();


aligh = document.querySelector("#songContentTPL").align;
language = "HE"
if(aligh == "left") language = "EN";
if(aligh == "right") language = "HE";
//שומר את כל הפסקאות של המוזיקה.
var html = jQuery('<div>').html(document.getElementById("songContentTPL")).text();

//חלק מהאקורדים מאפשרים תצוגות נוספות, והטקסט  מופיע בתוך השיר. מוחק אותו.
html = html.replace(/לחץ לתצוגה נוספת/g,"");
html = html.replace(/Click for other display/g,"");

counter = 0;
pos = [];
posNn = [];
//מכין רשימה של מיקומי "שורת אקורדים" 

//I מחלק למערך של שורות
lst = html.split('\n');
//I עותק אחד לבדיקות
newl = lst;

//I בודק איזה שורות במערך הן אקורדים
for (let i of newl){
	//I שורות שהיו רק "אנטר" הופכות במערך לתא ריק
	if(i == "") {posNn.push(counter); counter ++; continue;}

	//I אם יש סימן פלוס אחרי שם האקורד, הסיפריה לא מזהה אותו
	i = i.replace(new RegExp("[+]", "g"), "");

	//I מוחק מהשורה את כל האקורדים למיניהם
	for(let chrd of chrds){
		i = i.replace(new RegExp(chrd, "g"), "");
	}

	//I מוחק מהשורה את שאר הסימנים שאולי יהיו חוץ מאקורדים
	i = i.replace(new RegExp("[x1234567890\r\n/]", 'g'), "").replace(new RegExp(String.fromCharCode(160), 'g'), "");

	//I אם לא ריק, לא מדובר בשורת אקורדים
	if (i == "") {pos.push(counter); 	console.log(lst[counter]);}
	counter++;
}

//רשימת מספרי השורות של האקורדים.
console.log(pos)


//I יחס של 2:1 בין מילים לאקורדים
//I מצמיד לימין אם עברית
aftrNChrd = "\n\n";
if(language == "HE") {bfrChrd = "\u200F"; aftrNChrd = "\n";}
else bfrChrd = "";
aftrChrd = "\n";
counter = 0;
spccntr = 1;
newData = "";
lstcntr = 0;
//I בונה את מערך הנתונים מחדש
for (let j of lst){
	if(posNn.includes(counter)) {console.log(counter, "posNn"); counter++; continue;}
	if(pos.includes(counter)){
		console.log(counter, "pos");
		
		if(language == "HE"){
			//I סופר כמה רווחים להוסיף אחרי האקורדים. מעביר את הרווחים מהסוף להתחלה כי הם עברו צד.
			for(var i = 0; i < j.length; i++){
				if(j.slice(j.length - spccntr, j.length).replace(new RegExp(String.fromCharCode(160), 'g'), "") == "")
					{spccntr++; continue;}
				else{j = j.slice(j.length - spccntr + 1, j.length) + j.slice(0, j.length - spccntr + 1);
					spccntr = 0;
				}
			}


		}
		j = bfrChrd + j + aftrChrd;
		if(language == "HE" && j[j.length-2] == String.fromCharCode(35)) j =  String.fromCharCode(35) + j.slice(0, j.length-2) + j.slice(j.length-1, j.length);
		//I אם יש 2 שורות אקורדים רצוף, צריך רווח ביניהם. קורה אחרי פתיחה או מעבר
		if(pos.includes(lstcntr)) j = '\n' + j;
		newData += j;	
	}else{
		console.log(counter, "not pos");
		newData += j + aftrNChrd;
	}
	lstcntr = counter;
	counter++;
}

//I השם הוא "שם הזמר-שם השיר"
	const name = jQuery('<div>').html(document.querySelector("#page_content > div.row > div > div.song_block_top > div.ArtistAndSongName")).text().slice(1, -1);


	editedBy = "המערכת";
if(document.getElementById("editByUser")) editedBy = "גולש";

singer = name.split("  - ")[0];
song = name.split(" - ")[1];
newData = song + '\n' + singer + '\n' + editedBy + '\n' + capo + '\n' + newData;
newData = newData.replace(new RegExp("[?!]", 'g'), "");
newData = newData.replace(new RegExp("מעבר:", 'g'), "\nמעבר:");
newData = newData.replace(new RegExp("פתיחה:", 'g'), "\nפתיחה:");
newData = newData.replace(new RegExp("סיום:", 'g'), "\nסיום:");
newData = newData.replace(new RegExp("Intro:", 'g'), "\nIntro:");
newData = newData.replace(new RegExp("Bridge:", 'g'), "\nBridge:");
newData = newData.replace(new RegExp("/", 'g'), "/ ");


//create file. name: "artist-song.txt". downloading the file.
//download(newData, name, String);

download(newData, "update", String);
//I למנוע עומס
window.close();

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
}
