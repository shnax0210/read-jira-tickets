FROM python:3.9.7-alpine3.14

ADD map_ticket_fields.py /jira/
ADD read_jira_tickets.py /jira/
ADD read_jira_tickets_cmd_adapter.py /jira/
ADD requirements.txt /jira/
WORKDIR /jira
RUN pip install -r requirements.txt
