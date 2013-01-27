Pocket Library for Python
-------------------------

This came from my wanting to have something to do the following:

- Auto-magically tag articles which are above a certain length with the tag long. This would mean that when I have some time to read a lengthy article, I can simply call up that tag and read from those articles.
- I also want to (and can but haven't been bothered yet) to be able to auto tag articles based on words in the title. For example "Ubuntu 2013" would be auto-tagged with the tags "Linux" and "nerd".
- The end goal is to make an automatically tagging system with some form of intelligence perhaps using something like bayesian filtering. Right now, I am doing a lot of data grabbing from this and will work on the more intelligent side when I get a proper opportunity.

In order to use the pocket API, you have to register a new pocket app. Do this by following the relevant links in the [developer docs](http://getpocket.com/developer/docs/overview).

Using this consumer key you will get an access token for the user by running the following:

python auth.py --key=\<consumer-key\>

Follow the instructions and the program will finish.
Check your .creds file in the root directory of the project to make sure that it exists and has a consumer key and access token.

There are three seperate files that are exposed in pocketpy

- auth.py -> this handles Oauth to get access token for the user. In order to make any API calls you need to have both a consumer key and an access token.
- pocket.py -> This contains any logic to do with making the actual requests, it has the retrieve, modify and add functions. 
- tags.py -> This is a seperate logic file which handles the higher level case of using the modify function to add tags to items.

In the bin/ directory of this project, there is a number of scripts to do things like automatically grabbing the items in a users pocket and saving them. It also handles the article tagging.

I run this on a remote machine as a cron job, which runs every two hours and auto tags some of my list for me. in example/ there is an example bash script for how you might run it.
