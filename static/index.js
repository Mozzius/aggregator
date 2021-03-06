// generic functions for most pages

window.onresize = autoToggle

function autoToggle() {
    var left = document.getElementsByClassName('left')[0]
    if (window.innerWidth < 1200 && !left.classList.contains('mini') || window.innerWidth > 1200 && left.classList.contains('mini')) {
        toggleLeft()
    }
}

function toggleLeft() {
    document.getElementsByClassName('left')[0].classList.toggle('mini')
    document.getElementsByClassName('main')[0].classList.toggle('wide')
    document.getElementById('toggleleft').classList.toggle('fa-caret-left')
    document.getElementById('toggleleft').classList.toggle('fa-caret-right')
}

autoToggle()