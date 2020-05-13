# reading_list

[![codefactor](https://www.codefactor.io/repository/github/bfeldman89/reading_list/badge?style=plastic)](https://www.codefactor.io/repository/github/bfeldman89/reading_list)
![GitHub](https://img.shields.io/github/license/bfeldman89/reading_list?style=plastic)

![Twitter Follow](https://img.shields.io/twitter/follow/botfeldman89?style=social)

![Twitter Follow](https://img.shields.io/twitter/follow/bfeldman89?style=social)

## tools

### currently used
repo|description|website
---|---|---
[newspaper](https://github.com/atlanhq/camelot)|News, full-text, and article metadata extraction in Python 3.|[:link:](https://newspaper.readthedocs.io/en/latest/)
[gensim](https://github.com/frictionlessdata/goodtables-py)|Validate tabular data in Python|[:link:](https://frictionlessdata.io/)

### of interest

repo|description|website
---|---|---
[permacc api](https://github.com/harvard-lil/perma)|Use POST to [create a new archive](https://perma.cc/docs/developer#create-an-archive). Include the URL as JSON-encoded data. You can request the creation of multiple archives at once by [creating a batch](https://perma.cc/docs/developer#batches). Use HTTP POST, and include a list of URLs and a target folder ID (mandatory) as JSON-encoded data.|[:link:](https://perma.cc/settings/profile)

___
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)


###TK

```python
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='84ea3c42ac1f456491fe62dce605f770')
ms_articles = newsapi.get_everything(q='Mississippi and prison and coronavirus', from_param='2020-05-09', language='en')
all_articles = newsapi.get_everything(q='prison and coronavirus', from_param='2020-05-09', language='en')
```
