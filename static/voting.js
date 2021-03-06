// adds event listeners for voting and sends them off to the server
console.log('voting loaded')
function addPost(id,url) {
    document.addEventListener('DOMContentLoaded', function() {
        var post = document.getElementById('post-'+id)
        var upvote = document.getElementById('up-'+id)
        var score = document.getElementById('score-'+id)
        var downvote = document.getElementById('down-'+id)

        console.log(post.classList)

        if (url.match(/\.(jpeg|jpg|gif|png)$/) != null) {
            document.getElementById('img-'+id).style.backgroundImage="url('"+url+"')"
        } else {
            document.getElementById('img-'+id).style.backgroundImage="url(static/link.png)"
        }

        upvote.addEventListener('click',function (e) {
            e.preventDefault()
            console.log('Upvote :)')
            if (upvote.classList.contains('upvoted')) {
                score.textContent = parseInt(score.textContent) + 1
                // send upvote to server
            } else {
                score.textContent = parseInt(score.textContent) - 1
                // send unupvote to server
            }
            upvote.classList.toggle('upvoted')
            post.classList.toggle('upvoted')
        })

        downvote.addEventListener('click',function (e) {
            e.preventDefault()
            console.log('Downvote :(')
            if (downvote.classList.contains('downvoted')) {
                score.textContent = parseInt(score.textContent) + 1
                // send downvote to server
            } else {
                score.textContent = parseInt(score.textContent) - 1
                // send undownvote to server
            }
            upvote.classList.toggle('downvoted')
            post.classList.toggle('downvoted')
        })
    })
}