#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ddsutil
import dds

def demo_over_the_wire_topics():
    print('Connecting to DDS domain...')
    dp = dds.DomainParticipant()

    print('Finding HelloWorldTopic...')
    found_topic = dp.find_topic('HelloWorldData_Msg')

    print('Registering HelloWorldData_Msg locally')
    local_topic = ddsutil.register_found_topic_as_local(found_topic)

    print('Getting Python classes for the found topic...')
    gen_info = ddsutil.get_dds_classes_for_found_topic(found_topic)
    OsplTestTopic = gen_info.get_class(found_topic.type_name)

    print('Creating sample data to write...')
    data = OsplTestTopic(userID=1, message='Hello World')

    print('Creating writers...')
    pub = dp.create_publisher()
    wr = pub.create_datawriter(local_topic, found_topic.qos)
    # data = gen_info.topic_data_class(userID=1, message='Hello World')

    print('Writing sample data...')
    wr.write(data)
    print('Wrote: %s' % (str(data)))
    print('All Done!!!')


if __name__ == '__main__':
    demo_over_the_wire_topics()