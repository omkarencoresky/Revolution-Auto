document.getElementById('sidenav-dropdown-Car-Management').addEventListener('click', function(event) {
    event.preventDefault();
    
    var element = document.getElementById('sidenav-dropdown-menus-Car-Management');
    
    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');  
    }
});


document.getElementById('sidenav-dropdown-Services-Management').addEventListener('click', function(event) {
    event.preventDefault();
    
    var element = document.getElementById('sidenav-dropdown-menu-Services-Management');
    console.log('here')
    
    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');  
    }
});


document.getElementById('sidenav-dropdown-User-Management').addEventListener('click', function(event) {
    event.preventDefault();
    var element = document.getElementById('sidenav-dropdown-menu-User-Management');
    
    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');  
    }
});