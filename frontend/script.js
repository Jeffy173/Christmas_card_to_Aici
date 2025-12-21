const input_name=document.getElementById("input_name");
const input_password=document.getElementById("input_password");

const result_box=document.getElementById("response_box");
let result_pre=document.createElement("pre");
result_box.appendChild(result_pre);

function update_result(d,data){
    if(result_pre!==null) result_box.removeChild(result_pre);
    result_pre=document.createElement("pre");
    result_pre.appendChild(document.createTextNode(d.is_200?
        data.message:
        // "Error:status="+d.status.toString()+",detail:"+JSON.stringify(data.detail,null,4)
        data.detail
    ));
    result_box.appendChild(result_pre);
}

function error_result(error){
    if(result_pre!==null) result_box.removeChild(result_pre);
    result_pre=document.createElement("pre");
    result_pre.appendChild(document.createTextNode(error));
    result_box.appendChild(result_pre);
}

function get_talking(){
    let d={
        is_200:true,
        status:0
    }
    fetch("/api/get_talking/",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            name:input_name.value,
            password:input_password.value
        }),
    })
    .then(response=>{
        if(!response.ok){
            d.is_200=false;
            d.status=response.status;
        }
        return response.json();
    })
    .then(data=>{
        console.log(data);
        update_result(d,data);
        localStorage.setItem("id",data.id);
    })
    .catch(error=>{
        console.error("Error:", error);
        error_result(error);
    });
}

function get_card(){
    let d={
        is_200:true,
        status:0
    }
    fetch("/api/get_card/",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            id:localStorage.getItem("id")
        }),
    })
    .then(response=>{
        if(!response.ok){
            d.is_200=false;
            d.status=response.status;
        }
        return response.json();
    })
    .then(data=>{
        console.log(data);
        const newWindow=window.open("card.html","_blank");
        newWindow.onload=()=>newWindow.document.documentElement.innerHTML=data.data.body;
        update_result(d,data);
    })
    .catch(error=>{
        console.error("Error:", error);
        error_result(error);
    });
}

function update_result_local(data){
    if(result_pre!==null) result_box.removeChild(result_pre);
    result_pre=document.createElement("pre");
    result_pre.appendChild(document.createTextNode(data));
    result_box.appendChild(result_pre);
}

const get_card_button=document.getElementById("get_card_button");
get_card_button.addEventListener("click",()=>{
    if(localStorage.getItem("id")===null){
        update_result_local("please log in first!");
        return ;
    }
    get_card();
});
const get_talking_button=document.getElementById("get_talking_button");
get_talking_button.addEventListener("click",()=>{
    if(input_name.value===""){
        update_result_local("please enter your name!");
        return ;
    }
    if(input_password.value===""){
        update_result_local("please enter your password!");
        return ;
    }
    get_talking();
});