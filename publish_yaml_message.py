from google.cloud import pubsub_v1
import time
import yaml
import argparse


def publish_yaml_message(yaml_filepath):
    project_id = 'ccblender'
    topic_name = 'video-blend-requests'

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    futures = dict()

    with open(yaml_filepath) as f:
        yaml_dict = yaml.full_load(f)


    def get_callback(f, data):
        def callback(f):
            try:
                print(f.result())
                futures.pop(data)
            except:  # noqa
                print('Please handle {} for {}.'.format(f.exception(), data))
        return callback


    data = str(yaml_dict)
    futures.update({data: None})
    # When you publish a message, the client returns a future.
    future = publisher.publish(
        topic_path, data=data.encode('utf-8')  # data must be a bytestring.
    )
    futures[data] = future
    # Publish failures shall be handled in the callback function.
    future.add_done_callback(get_callback(future, data))

    # Wait for all the publish futures to resolve before exiting.
    while futures:
        time.sleep(5)

    print('YAML published to ' + topic_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml')
    args = parser.parse_args()

    publish_yaml_message(args.yaml)
