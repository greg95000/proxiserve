import requests
import conf.config as config
from datetime import date, timedelta
from models.db_manager import dbManager

def connect():
    """Connect to the easy conso login page

    Returns:
        [requests.Session]: The session containing the connection cookies information
    """
    session = requests.Session()
    url = config.CONNECT_URL
    data = {
        "login": config.LOGIN,
        "password": config.PASSWORD
    }
    session.post(url, data=data)
    return session


def extract_condominium(session, start_date, end_date):
    """Extract the condominium data

    Args:
        session (requests.Session): The session used to get the data
        start_date (date): The start date for the query
        end_date (date): The end date for the query
    Returns:
        [int]: the condominium id or -1 if the condominium was not found
    """
    condominium_id = -1
    url = config.ALL_CONDOMINIUM_TEMPLATE.format(
        root=config.ROOT_URL,
        start_date=start_date,
        end_date=end_date
    )
    response = session.get(url)
    json_formated_data = response.json()
    for group in json_formated_data.get('df') or []:
        if (
            group.get('group_name') and config.CONDIMINIUM_NAME in group.get('group_name')
        ):
            condominium_id = int(group.get('group_id'))
    return condominium_id


def get_co_owner_data(session, condominium_id, start_date, end_date):
    """ Get the co-owners data from easy conso website

    Args:
        session (Session): The connection session used for easy conso
        condominium_id (int): The id of the condominium
        start_date (date): The starting date to fetch the data
        end_date (date): The ending date to fetch the data

    Returns:
        [dict]: The response in json format
    """
    url = config.CONDOMINIUM_DATA_TEMPLATE.format(
        root=config.ROOT_URL,
        start_date=start_date,
        end_date=end_date,
        condominium=condominium_id
    )
    response = session.get(url)
    if response.status_code != 200:
        raise Exception("Response of the url {url} answered status {status}".format(url=url,status=response.status_code))
    return response.json()


def rollback_on_date_and_data(session, start_date, end_date, last_date):
    condominium_id = extract_condominium(
        session,
        start_date.isoformat(),
        end_date.isoformat()
    )
    all_data = []
    while(True):
        received_data = get_co_owner_data(
            session,
            condominium_id,
            start_date.isoformat(),
            end_date.isoformat()
        )
        insert_data_in_database(received_data, start_date, end_date)
        if last_date.isoformat() == start_date.isoformat():
            return all_data
        start_date = start_date - timedelta(days=1)
        end_date = end_date - timedelta(days=1)


def insert_data_in_database(data, start_date, end_date):
    conso_list = data.get('df', [{}]) or [{}]
    aggregate_users = []
    for data_profil in conso_list:
        if data_profil.get('tenant_name') not in aggregate_users:
            #create user
            pass
        if data_profil.get('conso', False):
            # insert the consumption
            pass

def get_proxiserve_userid(data_profil):
    pass


if __name__ == "__main__":
    session = connect()
    # We need to get the last valid date when we got the data
    # start_date = yesterday
    # end_date = today
    # loop if we don't have the data until the day we have it
    today_date = date.today()
    start_date = today_date - timedelta(days=1)
    end_date = today_date
    last_date = date(2020, 11, 25)
    db_manager = dbManager()
    db_manager.create_database()
    #data = rollback_on_date_and_data(session, start_date, end_date, last_date)
