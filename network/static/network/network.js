document.addEventListener('DOMContentLoaded', function() {

    // Hide edit post textarea.
    const edit_post_div = document.querySelectorAll('.edit-post-div');
    edit_post_div.forEach((div) => {
        div.style.display = 'none';
    });


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
                        console.log(btn); // Returns the button that was just clicked.
                        
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
                                    btn.style.display = 'block';
                                }
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

    });

});