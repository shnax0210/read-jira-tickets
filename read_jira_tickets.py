import json
import os
import pathlib

import requests

from map_ticket_fields import map_ticket_fields


class JiraTicketsReader:
    def __init__(self, login, password, jira_base_url, batch_size=50):
        self.login = login
        self.password = password
        self.jira_base_url = jira_base_url
        self.batch_size = batch_size

    def read_tickets(self, jql, mappings, base_path):
        with self.__create_session() as session:
            found_tickets_number, errors = 0, []
            for ticket in self.__read_tickets(session, jql):
                found_tickets_number = found_tickets_number + 1
                try:
                    self.__save_to_file(map_ticket_fields(ticket, mappings), base_path, ticket['key'])
                except Exception as ex:
                    errors.append("Error reading/saving ticket {}:{}".format(ticket['key'], ex))
            return {
                "numberOfFoundTickets": found_tickets_number,
                "numberOfSuccessfullySavedTickets": found_tickets_number - len(errors),
                "errors": errors
            }

    @staticmethod
    def __save_to_file(data, base_path, file_name):
        pathlib.Path(base_path).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(base_path, file_name + ".json"), 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def __create_session(self):
        session = requests.Session()
        session.auth = (self.login, self.password)
        return session

    def __add_url_prefix(self, relative_path):
        return self.jira_base_url + relative_path

    @staticmethod
    def __check_if_there_are_more_tickets_to_read(search_result):
        next_start_at = search_result['startAt'] + search_result['maxResults']
        return next_start_at < search_result['total'], next_start_at

    def __read_tickets(self, session, query):
        are_there_more_tickets_to_read = True
        start_at = 0

        while are_there_more_tickets_to_read:
            search_result = session.get(self.__add_url_prefix('/rest/api/latest/search'),
                                        params={'jql': query, "startAt": start_at, "maxResults": self.batch_size}).json()

            for ticket in search_result['issues']:
                yield ticket

            are_there_more_tickets_to_read, start_at = self.__check_if_there_are_more_tickets_to_read(search_result)
