#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

from dds import *
import time
import ddsutil
from multiprocessing import Process, Queue


class PubProc(Process):
    def __init__(self, sn):
        super().__init__()
        self.sn = sn

    def run(self):
        qp = QosProvider('file://DDS_DefaultQoS_All.xml', 'DDS DefaultQosProfile')
        dp = DomainParticipant(qos=qp.get_participant_qos())

        pub = dp.create_publisher(qos=qp.get_publisher_qos())

        gen_info = ddsutil.get_dds_classes_from_idl('example1.idl', 'Sample::DataTypesList::DataTypes')

        topic = gen_info.register_topic(dp, "Example", qp.get_topic_qos())

        writer = pub.create_datawriter(topic, qp.get_writer_qos())

        Inner = gen_info.get_class("Sample::DataTypesList::Inner")
        Color = gen_info.get_class("Sample::DataTypesList::Color")

        inner1 = Inner(short1=self.sn, double1=222)
        inner2 = Inner(short1=777, double1=333)
        time.sleep(0.5)
        data = gen_info.topic_data_class(longValue=self.sn, booleanValue=True, charValue='a', stringValue='Fire!',
                                         seq1=[inner1, inner2], color1=Color.Red)
        writer.write(data)
        print(data)


if __name__ == "__main__":

    for i in range(10):
        proc = PubProc(i)
        proc.start()






