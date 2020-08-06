#! /usr/bin/env python
# -*- coding: utf-8 -*-

from dds import *
import time
import ddsutil


if __name__ == "__main__":

    qp = QosProvider('file://TestQoS.xml', 'DDS TestQosProfile')

    dp = DomainParticipant(qos = qp.get_participant_qos())

    pub = dp.create_publisher(qos = qp.get_publisher_qos())

    gen_info = ddsutil.get_dds_classes_from_idl('example1.idl', 'Sample::DataTypesList::DataTypes')

    topic = gen_info.register_topic(dp, "Example", qp.get_topic_qos())

    writer = pub.create_datawriter(topic, qp.get_writer_qos())
    Inner = gen_info.get_class("Sample::DataTypesList::Inner")
    Color = gen_info.get_class("Sample::DataTypesList::Color")

    inner1 = Inner(short1=999, double1=222)
    inner2 = Inner(short1=777, double1=333)
    time.sleep(0.5)

    for i in range(10):
        data = gen_info.topic_data_class(longValue=i, booleanValue = True, charValue = 'a', stringValue = 'Fire!',
                                      seq1 = [inner1, inner2], color1 = Color.Red)
        writer.write(data)
        print(data)
        time.sleep(0.5)

    writer.dispose_instance(data)






