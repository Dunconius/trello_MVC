# this file is defining some default settings for flask when we use the regular run command.

# this one tells flask to read the file called 'main' instead of 'app'
# if this command is getting an error try 'main:create_app' which defines the name of the function
FLASK_APP=main

# this one tells flask to launch in debug mode so I don't have to type that in all the time
FLASK_DEBUG=1

# this one sets the port for it to run in.
FLASK_RUN_PORT=8080
