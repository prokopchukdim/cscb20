
function toggleCheck(type){

    let t_tog = document.getElementById("teacher-toggle");
    let t_lbl = document.getElementById("teacher-label");

    let s_tog = document.getElementById("student-toggle");
    let s_lbl = document.getElementById("student-label");

    
    if (t_tog.checked && s_tog.checked && type === 't'){
        s_tog.checked = false;
    }

    else if (t_tog.checked && s_tog.checked && type === 's'){
        t_tog.checked = false;
    }
}