document.getElementById('learnMore').addEventListener('click', function() {
    const infoBox = document.querySelector('.info-box p');
    infoBox.innerHTML = 'This Flask application is set up with Nginx as a reverse proxy and Gunicorn as the WSGI server. It includes SSL configuration and basic security features. Check out the Linode documentation to learn more about customizing your application!';
    this.style.display = 'none';
});
