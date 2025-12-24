const body=document.body;
const button=document.getElementById("button");
const text_box=document.getElementById("text_box");
const left_text=[
    "Deer Aici",
    "On this special day, I would like to wish you: ",
    "Merry Christmas & Happy New Year!",
    "",
    "又一年聖誕節到了！感謝你這些日子的陪伴和分享！",
    "作為你的朋友，我感到十分幸運，",
    "我們的友誼是我生活中最具有價值的寶藏。",
    "過完聖誕節，新年也要來了，",
    "在這裏，我希望在新的一年，",
    "我們都可以過得開心，學業進步。",
    "願我們友誼長存！最後再說一句：",
    "聖誕快樂！新年快樂！",
]
const right_text=[
    "your friend",
    "Jeffy",
    "2025.12.24",
]

function sleep(t){
    return new Promise(resolve=>setTimeout(resolve,t));
}

async function print_text(){
    await sleep(1000);
    for(let i=0;i<left_text.length;i++){
        let s=left_text[i];
        const p=document.createElement("p");
        p.classList.add("pleft");
        p.textContent="";
        text_box.appendChild(p);
        for(let j=0;j<s.length;j++){
            await sleep(100);
            p.textContent+=s[j];
        }
    }
    for(let i=0;i<right_text.length;i++){
        let s=right_text[i];
        const p=document.createElement("p");
        p.classList.add("pright");
        p.textContent="";
        text_box.appendChild(p);
        for(let j=0;j<s.length;j++){
            await sleep(100);
            p.textContent+=s[j];
        }
    }
}

bgcs=["bgc0","bgc1","bgc2"];
now_ci=0;
function change_bgc(){
    body.classList.remove(bgcs[now_ci++]);
    if(now_ci>=bgcs.length) now_ci-=bgcs.length;
    body.classList.add(bgcs[now_ci]);
}

button.addEventListener("click",change_bgc);
body.classList.add("bgc0");
print_text();