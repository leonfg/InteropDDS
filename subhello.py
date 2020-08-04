#! /usr/bin/env python
# -*- coding: utf-8 -*-

from dds import *
import time
import ddsutil


# Listener类
class DataAvailableListener(Listener):
    def __init__(self):
        Listener.__init__(self)

    def on_data_available(self, entity):
        print('on_data_available called')
        l = entity.take(1)
        for (sd, si) in l:
            sd.print_vars()


if __name__ == "__main__":

    qp = QosProvider('file://DDS_DefaultQoS_All.xml', 'DDS DefaultQosProfile')

    dp = DomainParticipant(qos = qp.get_participant_qos())

    sub = dp.create_subscriber(qos = qp.get_subscriber_qos())

    gen_info = ddsutil.get_dds_classes_from_idl('HelloWorldData.idl', 'HelloWorldData::Msg')

    topic = gen_info.register_topic(dp, 'HelloWorldData_Msg', qp.get_topic_qos())

    readerQos = qp.get_reader_qos()

    reader = sub.create_datareader(topic, readerQos)

    # reader2 = sub.create_datareader(topic, readerQos, DataAvailableListener())

    waitset = WaitSet()
    rc = ReadCondition(reader, DDSMaskUtil.all_samples())
    waitset.attach(rc)
    print('Waiting for data:')
    # Print data
    while True:
        conditions = waitset.wait()
        l = reader.take(1)
        for sd, si in l:
            sd.print_vars()







