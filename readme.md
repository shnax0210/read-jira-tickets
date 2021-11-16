# Simple utility to read jira tickets to json files with fields remapping

## Base info
The utility searches tickets by jql query, remaps ticket fields and saves each ticket to separate file in provided folder.

Please check read_jira_tickets_cmd_adapter.py to get more info regarding present parameters.

For example next mapping: `-m "fields/summary,fields/description->string:text" "fields/components[]/name->single_string:label"`
means that jira ticket fields `fields/summary` and `fields/description` will be concatenated to single string and written to field with name `text`.
And jira ticket field `fields/components[]/name` (`fields/components` is array) will be written to field with name `label` but only in case if there is only one element in `fields/components` array. In other case ticket will be not saved to result file.

[dpath](https://pypi.org/project/dpath/) is used for retrieving of jira ticket fields.

So the utility can be used for preparing data for Machine Learning or some other tasks.

## Run python directly
1) install python 3.9
2) install dependencies: `pip3 install -r requirements.txt`
3) Run `python3 read_jira_tickets_cmd_adapter.py -jql "some jql query" -u "user" -p "password" -url "https://jira-api.example.com" -path "./results" -m "fields/summary,fields/description->string:text" "fields/components[]/name->single_string:label"`

## Run from docker
1) Install docker
2) Build image: `docker build -t read-jira-tickets .`
3) Run: `docker run --rm -v $PWD/results:/results read-jira-tickets python read_jira_tickets_cmd_adapter.py -jql "some jql query" -u "user" -p "password" -url "https://jira-api.example.com" -path "/results" -m "fields/summary,fields/description->string:text" "fields/components[]/name->single_string:label"`

Please update at least next parameters values in the command above:
- jql - jira query to get tickets
- u - jira user login
- p - jira user password
- url - jira base url
 
Also there is `$PWD` usage that is applicable only on unix systems (please change it to absolute path on windows). 
