document.addEventListener('DOMContentLoaded', function() {

    // Hide edit post textarea.
    const edit_post_div = document.querySelectorAll('.edit-post-div');
    edit_post_div.forEach((div) => {
        div.style.display = 'none';
    });


    // Follow and Unfollow a User
    // https://stackoverflow.com/questions/26107125/cannot-read-property-addeventlistener-of-null
    // network.js:4 Uncaught TypeError: Cannot read properties of null (reading 'addEventListener') at HTMLDocument.<anonymous> (network.js:4:40)
    const follow = document.querySelector('#follow');
    const unfollow = document.querySelector('#unfollow');

    if (follow) { // Check for the button.
        follow.addEventListener('click', (e) => {
            e.preventDefault();
            user_to_follow = follow.dataset.user;
            console.log('User to follow id:', user_to_follow)

            // Fetch error in python - Forbidden (CSRF token missing.): /edit/post_id
            // To fetch from JS you must include the CSRF token.
            // https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
            // https://docs.djangoproject.com/en/5.0/howto/csrf/

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            // Send a POST request to the /follow/user route with the values of user_following and following_user.
            fetch(`/follow/${user_to_follow}`, {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                body: JSON.stringify({
                    user_follows: user_to_follow //following 
                    // following_user: current_user //follower
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log('Result:', result)
            })

            // Update view without refreshing
            // Update the innerHTML of the Follow button
            follow.innerHTML = 'Unfollow';

            // Update Number of Followers: {{ all_followers }}
            num_following = document.getElementById('num-following');
            console.log('Num Following', parseInt(num_following.innerHTML), typeof(num_following.innerHTML)) // String must be converted to a number to increase by 1.

            num_following.innerHTML = parseInt(num_following.innerHTML) + 1; 
            
        });
    }
        
        
    if (unfollow) { // Check for the button.   
        unfollow.addEventListener('click', (e) => {
            e.preventDefault(); 
            user_to_unfollow = unfollow.dataset.user; 
            console.log('User to unfollow id:', user_to_unfollow) 

            // Fetch error in python - Forbidden (CSRF token missing.): /edit/post_id
            // To fetch from JS you must include the CSRF token.
            // https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
            // https://docs.djangoproject.com/en/5.0/howto/csrf/

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            // Send a POST request to the /unfollow/user route with the values of user_following and following_user.
            fetch(`/unfollow/${user_to_unfollow}`, {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                body: JSON.stringify({
                    user_follows: user_to_unfollow, //following
                    // following_user: current_user //follower
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log('Result:', result)
            })

            // Update view without refreshing
            // Update the innerHTML of the Follow button
            unfollow.innerHTML = 'Follow';

            // Update Number Following: {{ all_following }}
            num_following = document.getElementById('num-following');
            console.log('Num Following', parseInt(num_following.innerHTML), typeof(num_following.innerHTML)) // String must be converted to a number to increase by 1.

            num_following.innerHTML = parseInt(num_following.innerHTML) - 1;             

        });
    }


    // Edit Post


    // When user clicks on the edit button, 
    const edit = document.querySelectorAll('.edit');
    
    edit.forEach((btn) => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();

            // Get post id from the button data-post attribute.
            // const post_id = btn.dataset.edit            
            // console.log('Button Data:', post_id); // Returns post_id as a string. edit function is looking for an integer.
            // console.log('Type of Button Data:', typeof(post_id)) // Returns string
            const post_id = parseInt(btn.dataset.edit);
            console.log('Button Data:', post_id);
            // console.log('Type of Button Data:', typeof(post_id))
            
            // Identify the one post to edit.
            // https://developer.mozilla.org/en-US/docs/Web/API/Element/querySelector - querySelector(selectors)
            // selectors - https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors
            // https://stackoverflow.com/questions/37081721/use-variables-in-document-queryselector
            // https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape_static
            const post = document.querySelector('[data-post='+ CSS.escape(post_id) +']')
            console.log('post:', post);

            // Remove the edit button
            // btn.remove();

            // Hide the edit button
            const edit_button = document.querySelectorAll('.edit');
            edit_button.forEach((btn) => {
                // If the post id === the edit button data-edit, hide edit button for that post only.
                // console.log('Edit data id', parseInt(btn.dataset.edit))
                const edit_button_data = parseInt(btn.dataset.edit);
                if (post_id === edit_button_data) {
                    btn.style.display = 'none';
                }
            });

            // Show the div stored in the const variable edit_post_div.
            edit_post_div.forEach((div) => {
                // If the post id === the edit div data-post, show textarea for that post only.
                // console.log('Div data-post', div.dataset.post)
                const post_to_edit_data = parseInt(div.dataset.post)
                if (post_id === post_to_edit_data) { 
                    div.style.display = 'block';
                }           
                
            });


            const save_button = document.querySelectorAll('[data-save]');
            save_button.forEach((btn) => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    // console.log('This save button was clicked:', btn); // Returns the button that was just clicked.
                    
                    console.log('Post id:', post_id, typeof(post_id));

                    // Value of the edited post.
                    // const post_revisions = document.querySelector(data-text="{{ post.id }}).value;
                    const post_revisions = document.querySelector('[data-text='+ CSS.escape(post_id) +']').value;
                    console.log('Post Revisions:', post_revisions);

                    // Fetch error in python - Forbidden (CSRF token missing.): /edit/post_id
                    // To fetch from JS you must include the CSRF token.
                    // https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
                    // https://docs.djangoproject.com/en/5.0/howto/csrf/

                    function getCookie(name) {
                        let cookieValue = null;
                        if (document.cookie && document.cookie !== '') {
                            const cookies = document.cookie.split(';');
                            for (let i = 0; i < cookies.length; i++) {
                                const cookie = cookies[i].trim();
                                // Does this cookie string begin with the name we want?
                                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                    break;
                                }
                            }
                        }
                        return cookieValue;
                    }

                    // Send a POST request to the /edit/post_id route with the value of post_revisions.
                    fetch(`/edit/${post_id}`, {
                        method: 'POST',
                        headers: {'X-CSRFToken': getCookie('csrftoken')},
                        body: JSON.stringify({ 
                            post: post_revisions
                        })
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log('Result:', result)
                    })


                    // Hide the div stored in the const variable edit_post_div.
                    edit_post_div.forEach((div) => {
                        // If the post id === the edit div id, hide textarea for that post only.
                        // console.log('Div id', div.dataset.post)
                        const post_to_edit_data = parseInt(div.dataset.post)
                        if (post_id === post_to_edit_data) { 
                            div.style.display = 'none';                                
                        }        

                        
                        // Clear the textarea
                        // https://stackoverflow.com/questions/15968911/how-to-clear-text-area-with-a-button-in-html-using-javascript
                        const textarea = document.querySelectorAll('.edited-post') // 
                        textarea.forEach((txt) => {
                            const text_data = parseInt(txt.dataset.text)
                            // console.log('Text data-text', text_data);
                            if (post_id === text_data) {
                                txt.value = '';
                            }
                        });                                              

                        // Show edit button
                        const edit_button = document.querySelectorAll('.edit');
                        edit_button.forEach((btn) => {
                            // If the post id === the edit button data-edit, hide edit button for that post only.
                            // console.log('Edit data id', parseInt(btn.dataset.edit))
                            const edit_button_data = parseInt(btn.dataset.edit);
                            if (post_id === edit_button_data) {
                                btn.style.display = 'inline-block';
                            }  
                        });  

                        
                        // Replace post.innerHTML with the author's revisions.
                        const post_body = document.querySelectorAll('[data-body]');
                        
                        post_body.forEach((p) => {
                            // console.log('Post Body:', p)
                            const p_data = parseInt(p.dataset.body);
                            if (post_id === p_data) {
                                p.innerHTML = post_revisions;
                            }
                        });
                        

                    });
            
                });
        
            });

            
            /*
            // Create this form here dynamically and send to the edit function.
            const form = document.createElement('form');
            // https://forum.djangoproject.com/t/generate-dynamic-url-js-to-template/10138
            // https://stackoverflow.com/questions/17364632/java-generating-strings-with-placeholders

            // !!!!!! Unable to set url. Error - Page not found (404) - The current path, {% url 'edit' post_id %}, didn’t match any of those within the view.  !!!!!!
            // ********** https://stackoverflow.com/questions/59752034/django-url-tag-not-working-when-dynamically-loading-the-page **********
            // form.setAttribute('action', `{% url 'edit' post_id %}`)
            form.setAttribute('action', `{% url 'edit' ${post_id} %}`)
            form.setAttribute('method', 'post')

            // https://stackoverflow.com/questions/42733761/how-to-properly-append-django-csrf-token-to-form-in-inline-javascript
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrfmiddlewaretoken';
            input.value = '{% csrf_token %}';
            form.append(input);

            const text = document.createElement('textarea');
            text.classList.add('form-control');
            text.setAttribute('id', 'exampleFormControlTextarea1');
            text.setAttribute('rows', '3');                        

            const button = document.createElement('button'); 
            button.setAttribute('type', 'submit');
            button.classList.add('btn');
            button.classList.add('btn-primary');
            button.innerHTML = 'Save';

            form.append(text);
            form.append(button);

            post.append(form);
            */
            

            
            
            
        });      

    });



    // “Like” and “Unlike”: Users may click a button on any post to toggle whether or not they “like” that post.
    // Using JavaScript, you should asynchronously let the server know to update the like count (as via a call to fetch) and 
    // then update the post’s like count displayed on the page, without requiring a reload of the entire page.

    // Store the like buttons in the varible called like.
    const like = document.querySelectorAll('.like');

    like.forEach((btn) => {
        // If user clicks the like button...
        btn.addEventListener('click', () => {

            // Identify the button that was clicked.
            const like_button = btn.dataset.like;
            console.log('Btn was clicked', like_button); // Post id

            // If the innerHTML is like
            if (btn.innerHTML === 'Like') {

                // Fetch error in python - Forbidden (CSRF token missing.): /edit/post_id
                // To fetch from JS you must include the CSRF token.
                // https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
                // https://docs.djangoproject.com/en/5.0/howto/csrf/

                function getCookie(name) {
                    let cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        const cookies = document.cookie.split(';');
                        for (let i = 0; i < cookies.length; i++) {
                            const cookie = cookies[i].trim();
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }


                // The likes for that post increase by one.
                // Send a PUT request to /like/post_id to increase the like score by 1.
                // fetch()
                
                // The innerHTML for that Like button becomes Unlike.
                // btn.innerHTML = 'Unlike'
            // } else {
                // The likes for that post decrease by one.
    
                // The innerHTML for that Unlike button becomes Like.
            }        
    
        });
    });



});