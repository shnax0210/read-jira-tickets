import argparse

from read_jira_tickets import JiraTicketsReader

ap = argparse.ArgumentParser()

ap.add_argument("-u", "--user", required=True, help="jira user login")
ap.add_argument("-p", "--password", required=True, help="jira user password")
ap.add_argument("-url", "--url", required=True, help="jira base url")
ap.add_argument("-jql", "--jql", required=True, help="jql query to get tickets for label adding")
ap.add_argument("-path", "--path", required=True, help="path to directory where to save results")
ap.add_argument("-m", "--mappings", required=True, help="mappings of jira ticket fields to result json field", nargs='+')
args = vars(ap.parse_args())

jira_tickets_reader = JiraTicketsReader(args['user'], args['password'], args['url'])

print('----------Start----------')
print(jira_tickets_reader.read_tickets(args['jql'], args['mappings'], args['path']))
print('----------Finish----------')
