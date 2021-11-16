# Simple utility to read jira tickets to json files with fields remapping

## Base info
The utility search tickets by jql query, remap ticket fields and save each ticket to separate file in provided folder.

Please check read_jira_tickets_cmd_adapter.py to get more info regarding present parameters.

Cmd example below has next mappings: `-m "fields/summary,fields/description->string:text" "fields/components[]/name->single_string:label"`
It means that jira ticket fields `fields/summary` and `fields/description` will be concatenated to single string and written to field with name `text`.
And jira ticket field `fields/components[]/name` (`fields/components` is array) will be written to field with name `label` but only in case if there is only one element in `fields/components` array. In other case ticket will be not saved to result file.


## Run python directly
1) install python 3.9
2) install dependencies: `pip3 install -r requirements.txt`
3) Run `python3 read_jira_tickets_cmd_adapter.py -jql "some jql query" -u "user" -p "password" -url "https://jira-api.example.com" -path "./results" -m "fields/summary,fields/description->string:text" "fields/components[]/name->single_string:label"`
Note: please update parameters values in the command above!

## Run from docker
1) Install docker
2) Build image: `docker build -t add-jira-label .`
3) Run: `docker run --rm add-jira-label python add_jira_label_cmd_adapter.py -jql "some jql query" -u "user" -p "password" -url "https://jira-api.example.com" -path "./results" -m "fields/summary,fields/description->string:text" "fields/components[]/name->single_string:label"`
Note: please update parameters values in the command above!
