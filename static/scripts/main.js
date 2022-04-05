window.onload = function() {

    //Code for marks page. Changes the values of hidden input fields on page-load
    //for Flask to be able to read all necessary info on a POST request.
    let component_cells = document.getElementsByClassName("remark-cell-1");
    let mark_cells = document.getElementsByClassName("remark-cell-2");
    for (let cell of component_cells){
        let parent = cell.parentElement;
        parent.getElementsByClassName("remark-input-1")[0].setAttribute("value",cell.innerText);

    }
    for (let cell of mark_cells){
        let parent = cell.parentElement;
        parent.getElementsByClassName("remark-input-2")[0].setAttribute("value",cell.innerText);

    }
        
}

//Allows toggling between student and instructor to work
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