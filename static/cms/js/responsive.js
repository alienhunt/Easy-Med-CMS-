
// functions to be called as the page loads
function main() {
    console.log("in main");
    startSession();
    // select();
    show_date();
    sessionActive();
}

// function reloads the page after 20 seconds if the user is inactive
function sessionActive() {
    setTimeout(() => {
        // reload the page 
        alert("Your Session Has Expired Please Login again!");
        console.log("expired")
        location.reload()
        // after 20000 ms -> 20
    }, (3 * 60 * 1000))
}

// to restrict the date input max attribute to today
function restrict_max() {
    var da = new Date().toISOString().split("T")[0];
    console.log(da);
    document.getElementById("dateid").max = da;
    console.log(document.getElementById("dateid").max);
}

// to restrict the date input min attribute to tomorrow
function restrict_min() {
    var da = new Date();
    console.log(da);
    da.setDate(da.getDate() + 1);
    da = da.toISOString().split("T")[0];
    console.log(da);
    document.getElementById("slotdate").min = da;
    console.log(document.getElementById("slotdate").min);
}

// to display current date
function show_date() {
    var date = new Date();
    var display = document.getElementById("date");
    if (display != null) {
        display.innerHTML = date.toISOString().split("T")[0];
    }
}
window.onscroll = function () { scroll_check() };

//to check if the screen is scrolled down
function scroll_check() {
    top_btn = document.getElementById("top-btn");
    if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
        $("#top-btn").fadeIn();
        //top_btn.style.display = "block"; 
    }
    else {
        $("#top-btn").fadeOut();
        //top_btn.style.display = "none";   
    }
}

// this fucntion will go on top
function page_top() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

//for table checkbox responsiveness
function select(all = false) {
    var rows = document.querySelectorAll('.select-bit');
    var count = 0;
    if (all == true) { 
        rows.forEach(row => {
            row.getElementsByClassName('checkbox')[0].checked = true;
        });
    }
    rows.forEach(row => {
        if (row.getElementsByClassName('checkbox')[0].checked == true) {
            row.classList.add('table-danger');
            count++;
        }
        else {
            row.classList.remove('table-danger');
        }
    });
    var text = document.getElementById('appointment-text');
    if (text != undefined) {
        if (count > 1) {
            console.log(text.innerText = "Are you sure that you want to cancel your appointments?");
        }
        else {
            console.log(text.innerText = "Are you sure that you want to cancel your appointment?");
        }
    }
}

function selectAll() {
    var selects = document.getElementById('selectall');
    if (selects.checked == true) {
        select(all=true);
    }
}

// to toggle the password visibility
function togglePassword() {
    var pass = document.getElementById("pass");
    var lock = document.getElementById("lock");
    if (lock.classList.contains("fa-unlock") == true) {
        lock.classList.remove("fa-unlock");
        lock.classList.add("fa-lock");
        lock.setAttribute("title", "Show Password");
        console.log(lock.getAttribute("title"));
        pass.setAttribute("type", "password");
        pass.classList.toggle('side-content');
        pass.classList.toggle('side-header');
    }
    else {
        lock.classList.remove("fa-lock");
        lock.classList.add("fa-unlock");
        lock.setAttribute("title", "Hide Password");
        pass.setAttribute("type", "text");
        pass.classList.toggle('side-content');
        pass.classList.toggle('side-header');
    }
}

// validates password in signup form
function checkPass() {
    var pass = document.getElementById("pass");
    var conf = document.getElementById("conf");
    if (pass.value.length == 0 && conf.value.length == 0) {
        conf.classList.remove("red")
        conf.classList.remove("green")
        conf.classList.add("white")
    }
    else {
        if (pass.value == conf.value) {
            conf.setAttribute("style", "color:#8bd8bd");
        }
        else {
            conf.setAttribute("style", "color:#ff3d49");
        }
    }
}

// function to alert the user and start the session 
function startSession() {

    names = document.getElementsByClassName("index");
    console.log(names)
    if (names.length > 0) {
        alert("Alert!\n\nIf the user is inactive for three minutes, then the page will reload, and the server will automatically log the user out.");
    }
}

// function alerts the user if the input is not valid
function forgotValidate() {

    check = document.getElementById('forgot-validate');
    console.log(check);

    if (check != null) {

        email = document.getElementById('email');
        contact = document.getElementById('contact');

        console.log(email.value);

        if (email.value === "" && contact.value === "") {
            alert("Please give your email id or contact number!\nMust give atleast one of the two!");
        }
        else {
            document.getElementsByTagName('form')[0].submit();
        }
    }

}

// function to start logo animation when the cms logo is clicked
function logoAnimate() {

    var logo = document.getElementsByClassName("cms_logo")[0];
    var nba = 'navbar-brand-animate';
    // if(logo.classList.contains(nba)){
    //     logo.classList.remove(nba);
    // }
    logo.classList.add(nba);
    setTimeout(() => {
        logo.classList.remove(nba);
    }, 2000);
    console.log("animate", logo);
}