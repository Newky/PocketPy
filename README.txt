Pocket Library for Python
-------------------------

This came from my wanting to have something to do the following:

- Auto-magically tag articles which are above a certain length with the tag long. This would mean that when I have some time to read a lengthy article, I can simply call up that tag and read from those articles.
- I also want to (and can but haven't been bothered yet) to be able to auto tag articles based on words in the title. For example "Ubuntu 2013" would be auto-tagged with the tags "Linux" and "nerd".

In order to use the pocket API, you have to register a new pocket app. Do this by following the relevant links in the [developer docs](http://getpocket.com/developer/docs/overview).

Using this consumer key you will get an access token for the user by running the following:

python auth.py --key=\<consumer-key\>

Follow the instructions and the program will finish.
Check your .creds file in the root directory of the project to make sure that it exists and has a consumer key and access token.

There are three files in the repository as follows:

- auth.py -> this handles Oauth to get access token for the user. In order to make any API calls you need to have both a consumer key and an access token.
- pocket.py -> This contains any logic to do with making the actual requests, it has both a retrieve and modify function. (there is also an add API call which I will add when I need it). It also contains helper functions for adding tags etc to a list item.
- operators.py -> Not a very generic part, a place where I put some functions for doing all the steps. My functions which deal with the auto tagging long articles is what is run when this file is executed. When I get some more time, I will clean this up. However, really any new application should really just import auth and pocket python files and run with that.

I run this on a remote machine as a cron job, which runs every two hours and auto tags some of my list for me. in example/ there is an example bash script for how you might run it.
