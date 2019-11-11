import time
import yaml
from end_to_end import download
from google.cloud import pubsub_v1, storage

project_id = 'ccblender'
subscription_name = 'video-blend-requests-subscription'

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(project_id, subscription_name)


def upload_blob(bucket_name, data_string, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data_string)
    print(f'File uploaded to {destination_blob_name}')


def callback(message):
    print('Received message: {}'.format(message))

    yaml_dict = yaml.full_load(message.data)

    message.ack()
    upload_blob(
        'video-blend-requests-bucket',
        message.data,
        message.attributes.get('filename')
    )
    download(message.data)


subscriber.subscribe(subscription_path, callback=callback)


# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(10)
