# Sqlite

The following sqlite files where created using  `~/scratch/manoelribeiro/helpers/text_dict.sqlite` the main database that has the form:
```
Tablename: text
  {id_c: {"likes": likes,
          "text": text,
          "is_reply": isreply, 
          "timestamp": timestamp, 
          "channel_id": chanel_id, 
          "category": category}
```
Where category represents the community name;

## Description
##### ** The tablename of all following sqlite files have a different name, it's called "value" **

Folders created to facilitate the process of get IDs and iterate over the database:
- `./split_texts/` contains the original database splited at each 10 Milion comments
- `./community_texts/`contains the original database splited by community

The folders created to store the values from empath and perspective have the form:
```
# ./empath_sqlite/
Tablename: value
  {id_c: {"size": size,
          "sadness": empath_value,
          empath_category_2: empath_value,
          empath_category_3: empath_value, 
          .
          .
          .
          empath_category_21: empath_value}}
```

```
# ./perspective_sqlite/
Tablename: value
  {id_c: {'TOXICITY': perspective_value,
          'SEVERE_TOXICITY': perspective_value,
          'IDENTITY_ATTACK': perspective_value,
          'INSULT': perspective_value,
          'PROFANITY': perspective_value,
          'THREAT': perspective_value,
          'SEXUALLY_EXPLICIT': perspective_value,
          'FLIRTATION': perspective_value}}
```
