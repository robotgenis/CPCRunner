$(document).ready(function($) {
    $(".clickable").click(function() {
        window.location = $(this).data("href");
    });

    $(".myCode").click(function(e){
        let newClip = e.currentTarget.innerText;
        navigator.clipboard.writeText(newClip);
        $("#copy-toast").toast('show');
    });
});
