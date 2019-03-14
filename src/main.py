"""
Test GUIDs performance

"""
import pprint
import time

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

import models
import factories

USERS_TO_CREATE = 1_000
ITERATIONS_FOR_TIMING = 1_000


if __name__ == '__main__':
    engine = create_engine('mysql+mysqldb://myuser:mypass@127.0.0.1:3306/mydb')
    Session = sessionmaker()

    connection_made = False
    connection = None
    while not connection_made:
        connection = engine.connect()  # grab a new connection
        connection_made = connection.execute('select "OK"')  # and retry

    transaction = connection.begin()
    models.Base.metadata.create_all(engine)
    session = Session(bind=connection, autoflush=False)
    factories.UserFactory._meta.sqlalchemy_session = session

    records = connection.execute('SHOW VARIABLES LIKE "version";')
    _, version = records.next()
    print(f'MySQL Version: {version}')

    inspector = inspect(engine)
    print('\n\nInspecting table columns:')
    pprint.pprint(inspector.get_columns('guid_user'))
    print('\n\nInspecting table indexes:')
    pprint.pprint(inspector.get_indexes('guid_user'))

    user = factories.UserFactory.create()

    start = time.time()
    factories.UserFactory.create_batch(USERS_TO_CREATE)
    print(f'\n\nGenerated {USERS_TO_CREATE} users in: {time.time()-start:0.4f}s')

    start = time.time()
    for _ in range(ITERATIONS_FOR_TIMING):
        session.query(models.UserModel).filter(models.UserModel.id == user.id)
    print(f'Selected {ITERATIONS_FOR_TIMING} users by id: {time.time()-start:0.6f}s')

    start = time.time()
    for _ in range(ITERATIONS_FOR_TIMING):
        session.query(models.UserModel).filter(models.UserModel.guid == user.guid)
    print(f'Selected {ITERATIONS_FOR_TIMING} users by guid: {time.time()-start:0.6f}s')

    user = factories.UserFactory.create()
    print(f'\n\nCreated user: {user}')
    print(f'{user.address}')
    print(f'Finding all users in the state of: {user.address["state"]}\n\n')

    # Flush to write the created users to db before trying to query
    session.flush()

    all_users_in_state = session.query(models.UserModel).filter(models.UserModel.address['state'] == user.address['state'])
    print(f'{all_users_in_state}\n\n')

    for user_in_state in all_users_in_state.all():
        print(f'{user_in_state.name:20s} [{user_in_state.guid}] {user_in_state.address["state"]}')

    session.close()
    transaction.rollback()
    connection.close()

    print(f'\n\nDone.')
