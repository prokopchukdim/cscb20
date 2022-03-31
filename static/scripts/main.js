// document.onload() = function() {
//     let s_tog = document.getElementById("student-toggle");
//     if (!!s_tog){
//         s_tog.checked = true;
//     }
// }

function toggleCheck(type){

    let t_tog = document.getElementById("instructor-toggle");

    let s_tog = document.getElementById("student-toggle");
    
    if (t_tog.checked && s_tog.checked && type === 'i'){
        s_tog.checked = false;
    }

    else if (t_tog.checked && s_tog.checked && type === 's'){
        t_tog.checked = false;
    }
}