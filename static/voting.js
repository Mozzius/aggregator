// adds event listeners for voting and sends them off to the server

function addPost(id,image) {
    console.log('Adding '+id)
    var votingBox = document.getElementById(id)
    var upvote = votingBox.childNodes[0]
    var score = votingBox.childNodes[1]
    var downvote = votingBox.childNodes[2]

    if (image !== '') {
        document.getElementById('img-'+id).style.backgroundImage="url('"+image+"')"
    }

    upvote.addEventListener('click',function () {
        console.log('Upvote :)')
        if (upvote.classList.contains('upvoted')) {
            score.textContent = parseInt(score.textContent) + 1
            // send upvote to server
        } else {
            score.textContent = parseInt(score.textContent) - 1
            // send unupvote to server
        }
        upvote.classList.toggle('upvoted')
    })

    downvote.addEventListener('click',function () {
        console.log('Downvote :(')
        if (downvote.classList.contains('downvoted')) {
            score.textContent = parseInt(score.textContent) + 1
            // send downvote to server
        } else {
            score.textContent = parseInt(score.textContent) - 1
            // send undownvote to server
        }
        upvote.classList.toggle('downvoted')
    })
}