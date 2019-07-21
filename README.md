# wiki_named_entity_extractor

Named entity extractor based wikipedia's page link.

Procedure 
1. Download wikipedia's ...page-arcles.xml.bz2 from [here](https://dumps.wikimedia.org/jawiki/latest/) 
2. By using [wikiextractor](https://github.com/attardi/wikiextractor), extract contents
```
 python WikiExtractor.py -o result ../jawiki-XXXX-pages-articles.xml.bz2
```
3. Use link_analysis.py to create synonym list of json
```
python link_analysis.py <WikiExtractor's output dir> <output file name>
```
4. run the extractor
python extractor.py <output file name> "text to extract entities"
