# Substantive

Python script for German noun gender analysis.

## Installation

Download [dict.cc](http://www1.dict.cc/translation_file_request.php) and use the following script on it to extract the data containing gender for each word.

```bash
  grep -P ".*?noun" dict.cc.txt | \
  grep -P -o "[A-ZÄÜÖß][a-zA-ZÄÜÖäüöß-]+[a-zäüöß] \{(m|f|n)\}" | \
  sort | uniq > dict.cc_nouns_with_gender.txt
```


