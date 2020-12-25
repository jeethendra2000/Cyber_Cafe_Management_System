$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.dropdown-trigger').dropdown({
        'coverTrigger' : false,
        'constrainWidth' : false,
    });
    $('select').formSelect();
    $('.modal').modal();
});