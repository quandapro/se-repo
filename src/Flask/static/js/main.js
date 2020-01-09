$(document).ready(function () {
    function preprocessing(){
        let options = []
        let sliders = {}
        $('.autosubmit').each(function(){
            if ($(this).prop("checked")){
                options.push($(this).attr("name"))
            }
        })

        $('.slider').each(function(){
            key = $(this).attr("name")
            value = $(this).attr("value")
            sliders[key] = value
        })
        original_image = $("#myimage_1").attr('src').split('/')[3]
        $.ajax({
            type: "POST",
            url: "/image",
            data: {image: original_image, 
                data: JSON.stringify(options),
                sliders: JSON.stringify(sliders)},
            dataType: 'json',
            success: function(data, status, xhr) {
                $("#myimage_2").attr('src', data)
                imageZoom("myimage_1", "myresult_1");
                imageZoom("myimage_2", "myresult_2");
            }
        })
    }
    $('.autosubmit').click(function(){
        preprocessing();
    })

    $('.slider').change(function(){
        preprocessing();
    })
});

function imageZoom(imgID, resultID) {
    var img, lens, result, cx, cy;
    img = document.getElementById(imgID);
    result = document.getElementById(resultID);
    if ($(".img-zoom-lens").length == 2){
        $(".img-zoom-lens").remove()
    }
    /* Create lens: */
    lens = document.createElement("DIV");
    lens.setAttribute("class", "img-zoom-lens");
    /* Insert lens: */
    img.parentElement.insertBefore(lens, img);
    /* Calculate the ratio between result DIV and lens: */
    cx = result.offsetWidth / lens.offsetWidth;
    cy = result.offsetHeight / lens.offsetHeight;
    /* Set background properties for the result DIV */
    result.style.backgroundImage = "url('" + img.src + "')";
    result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
    /* Execute a function when someone moves the cursor over the image, or the lens: */
    lens.addEventListener("mousemove", moveLens);
    img.addEventListener("mousemove", moveLens);
    /* And also for touch screens: */
    lens.addEventListener("touchmove", moveLens);
    img.addEventListener("touchmove", moveLens);
    function moveLens(e) {
        var pos, x, y;
        /* Prevent any other actions that may occur when moving over the image */
        e.preventDefault();
        /* Get the cursor's x and y positions: */
        pos = getCursorPos(e);
        /* Calculate the position of the lens: */
        x = pos.x - (lens.offsetWidth / 2);
        y = pos.y - (lens.offsetHeight / 2);
        /* Prevent the lens from being positioned outside the image: */
        if (x > img.width - lens.offsetWidth) { x = img.width - lens.offsetWidth; }
        if (x < 0) { x = 0; }
        if (y > img.height - lens.offsetHeight) { y = img.height - lens.offsetHeight; }
        if (y < 0) { y = 0; }
        /* Set the position of the lens: */
        lens.style.left = x + "px";
        lens.style.top = y + "px";
        /* Display what the lens "sees": */
        result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
    }
    function getCursorPos(e) {
        var a, x = 0, y = 0;
        e = e || window.event;
        /* Get the x and y positions of the image: */
        a = img.getBoundingClientRect();
        /* Calculate the cursor's x and y coordinates, relative to the image: */
        x = e.pageX - a.left;
        y = e.pageY - a.top;
        /* Consider any page scrolling: */
        x = x - window.pageXOffset;
        y = y - window.pageYOffset;
        return { x: x, y: y };
    }
}   
