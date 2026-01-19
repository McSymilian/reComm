from datetime import datetime
from time import sleep
from src.utils.api_client import APIClient
from src.utils.data_store import DataStore

if __name__ == "__main__":
    # Example usage of the APIClient
    client2 = APIClient(host="192.168.100.44", port=8080)
    
    # Authenticate a user
    client2.authenticate(username="test1", password="pass")
    print(client2.get_friends())
    datastore2 = DataStore(client2)
    datastore2.initialize()
    print(datastore2)
    

    message_response = client2.send_private_message(
        receiver_username="test",
        content="Hello from test_api_client!" + datetime.now().isoformat()
    )
    sleep(1)

    # group_creation_response = client.create_group(
    #     group_name="Test Group",
    # )
    # print(f"Group creation response: {group_creation_response}")
    client = APIClient(host="192.168.100.44", port=8080)
    client.authenticate(username="test", password="pass")
    datastore = DataStore(client)
    datastore.initialize()
    print(datastore)
    client.send_private_message(
        receiver_username="test1",
        content="Hello from test_api_client to test1!" + datetime.now().isoformat()
    )
    print(datastore2)
    print(datastore)

    print(client.get_notification(1))
    # client.create_group(
    #     group_name="Test Group from test_api_client"
    # )
    groups = client.get_user_groups()
    group_id = groups.groups[0].groupId
    client.add_member_to_group(
        group_id=group_id,
        username="test1"
    )
    client.get_group_messages(
        group_id=group_id,
        since=0,
        limit=10
    )
    client.send_group_message(
        group_id=group_id,
        content="Hello group from test_api_client!" + datetime.now().isoformat()
    )


    print(f"Message send response: {message_response}")

    # add friend
    # send_friend_request_response = client.send_friend_request(addressee_username="test")
    # if send_friend_request_response.code != 200:
    #     print(f"Add friend failed: {send_friend_request_response.message}")
    # else:
    #     print("Friend request sent successfully.")

    