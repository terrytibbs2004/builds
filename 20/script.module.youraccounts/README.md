To add *Your Accounts* as a deppendecy
add the following to your addon's addon.xml file between the `<requires></requires>` tag.

`<import addon="script.module.youraccounts" version="1.0.0" />`
Addon developers can access *Your Accounts* as simply as

# How to call *Your Accounts* settings 

You can use `import youraccounts` once the dependecy is added to your addon.  The following lists the functions that can be called that will respond with a dictionary and the supplied key and value.

### youraccount.getAll()
This function call will provide all available accounts as a dictionary for each account handled.  If we called `accounts = youraccounts.getAll()` The returned data will be as follows.
`accounts ={'premiumize': {'enabled': '', username': '', 'token': ''}, 'alldebrid': {'enabled': '', 'username': '', 'token': ''}, 'tmdb': {'username': '', 'password': '', 'api_key': '', 'session_id': ''},
	'realdebrid': {'enabled': '', 'username': '', 'token': '', 'secret': '', 'refresh': '', 'client_id': ''}, 'ororo': {'password': '', 'email': ''}, 'tvdb': {'api_key': ''}, 'filepursuit': {'api_key': ''},
	'trakt': {'username': '', 'token': '', 'expires': '', 'refresh': ''}, 'imdb': {'user': ''}, 'easyNews': {'username': '', 'password': ''}, 'furk': {'username': '', 'api_key': '', 'password': ''},
	'fanart_tv': {'api_key': ''}}`

### youraccount.getTrakt()
Returns trakt only account info
```trakt': {'username': '', 'token': '', 'expires': '', 'refresh': ''}```

### youraccount.getAllDebrid()
Returns all debrid account information supported (currently All-Debrid, Premiumize.me, Real-Debrid)
There is an addional key for each dictionary `'enabled'`.  This key could be used by the adon developer that the debrid service is temporarily disabled by the user.
`{premiumize': {'enabled': '', 'username': '', 'token': ''}, 'alldebrid': {'enabled': '', 'username': '', 'token': ''}, 'realdebrid': {'enabled': '', 'username': '', 'token': '', 'secret': '', 'refresh': '', 'client_id': ''}}`

### youraccount.getAD()
`alldebrid': {'enabled': '', 'username': '', 'token': ''}`
 
### youraccount.getPM()
`premiumize': {'enabled': '', 'username': '', 'token': ''}`
  
### youraccount.getRD()
`realdebrid': {'enabled': '', 'username': '', 'token': '', 'secret': '', 'refresh': '', 'client_id': ''}`

### youraccount.getAllMeta()
`{'tmdb': {'username': '', 'password': '', 'api_key': '', 'session_id': ''}, 'tvdb': {'api_key': ''}, 'imdb': {'user': ''}, 'fanart_tv': {'api_key': ''}}`

### youraccount.getFanart_tv()
`fanart_tv': {'api_key': ''}`

### youraccount.getTMDb()
`tmdb': {'username': '', 'password': '', 'api_key': '', 'session_id': ''}`

### youraccount.getTVDb()
`tvdb': {'api_key': ''}`

### youraccount.getIMDb()
`imdb': {'user': ''}`

### getAllScraper()
`{'ororo': {'password': '', 'email': ''}, 'filepursuit': {'api_key': ''}, 'easyNews': {'username': '', 'password': ''}, 'furk': {'username': '', 'api_key': '', 'password': ''}}`

### getFilepursuit()
`filepursuit: {'api_key': ''}`

### youraccount.getFurk()
`furk: {'username': '', 'api_key': '', 'password': ''}`

### youraccount.getEasyNews()
`easyNews: {'username': '', 'password': ''}`

### youraccount.getOrro()
`ororo: {'password': '', 'email': ''}`
