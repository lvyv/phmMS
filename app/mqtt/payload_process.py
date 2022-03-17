class PayloadProcess:

    @staticmethod
    def process(msg):
        # TODO 解析数据，并将数据写入数据库
        print(msg)

    @staticmethod
    def getEquipCode(topic):
        topics = topic.split("/")
        if len(topics) == 3:
            return topics[1]
        return None

    @staticmethod
    def topicIsEqual(topic1, topic2):
        if topic1 == topic2:
            return True
        equipCode = PayloadProcess.getEquipCode(topic1)
        if equipCode is None:
            return False
        generalTopic = topic1.replace(equipCode, "+")
        if generalTopic == topic2:
            return True
        return False
