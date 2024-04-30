document.addEventListener('DOMContentLoaded', function() {
    // https://stackoverflow.com/questions/26107125/cannot-read-property-addeventlistener-of-null
    // network.js:4 Uncaught TypeError: Cannot read properties of null (reading 'addEventListener') at HTMLDocument.<anonymous> (network.js:4:40)
    const follow = document.querySelector('#follow');
    const unfollow = document.querySelector('#unfollow');

    if (follow) {
        follow.addEventListener('click', () => follow);
        // follow.innerHTML = 'Unfollow';
    } 
    
    if (unfollow) {
        unfollow.addEventListener('click', () => unfollow);
        // unfollow.innerHTML = 'Follow';
    }
});