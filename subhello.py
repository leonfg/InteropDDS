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

    # 载入QoS配置
    qp = QosProvider('file://DDS_DefaultQoS_All.xml', 'DDS DefaultQosProfile')

    # 创建域参与者
    dp = DomainParticipant(qos = qp.get_participant_qos())

    # 创建Subscriber
    sub = dp.create_subscriber(qos = qp.get_subscriber_qos())

    # 读取IDL文件生成消息数据类e
    gen_info = ddsutil.get_dds_classes_from_idl('HelloWorldData.idl', 'HelloWorldData::Msg')

    # 生成topic
    topic = gen_info.register_topic(dp, 'HelloWorldData_Msg', qp.get_topic_qos())

    # 创建reader
    readerQos = qp.get_reader_qos()
    # 1.创建轮询reader
    reader = sub.create_datareader(topic, readerQos)
    # 2.创建触发回调reader
    # reader2 = sub.create_datareader(topic, readerQos, DataAvailableListener())

    # 创建waitset
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







