<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <title>PPP | Login</title>
</head>
<body>
    <section>
        <div class="imgBox">
            <img src="{{ url_for('static', filename='images/login.jpg') }}" alt="">
        </div>
        <div class="contentBox">
            <div class="formBox">
                <h2>Login</h2>
                <form action="/submit" method="POST">
                    <div class="inputBox">
                        <i class="fa fa-key"></i>
                        <span>Admin Key</span>
                        <input type="text" name="adminKey">
                    </div>
    
                    <div class="inputBox">
                        <i class="fa fa-lock"></i>
                        <span>Password</span>
                        <input type="password" name="password">
                    </div>
    
                    <div class="inputBox">
                        <input type="submit" value="Log In">
                    </div>
                </form>
            </div>
        </div>
    </section>
</body>
</html>