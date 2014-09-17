#HewHolland Brewery WebServices

This isn't a real project but rather is the starting point for a way to locate NewHolland beers that I crave which are nearby me. Maybe one day it will turn into something that can actually be used within a iphone app or something. I'm not really focusing on best programming practices but using this more as a playground for some simple things that peek my interest and hopefully can be useful for others.

##Installation
For simple installtion on a raspberry pi (which is what I am using to play around with this). 

```sudo pip install virtualenv```
```pip install virtualenvwrapper```
```echo 'export WORKON_HOME=~/Envs' >> ~/.profile```
```source ~/.profile```
```source /usr/local/bin/virtualenvwrapper.sh```
```mkvirtualenv newholland```
```cd && mkdir newholland```
```git clone https://github.com/jdye64/NewHollandBrewery-web.git ./newholland```
```cd ./newholland && pip install -r requirements.txt```
```python BeerFinder.py```
