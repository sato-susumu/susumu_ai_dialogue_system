import random


# noinspection PyMethodMayBeStatic
class MessageFilter:
    def __init__(self):
        pass

    def exclude_empty_message(self, message_list):
        return [item for item in message_list if item.message != ""]

    def choose_random_items(self, message_list, num_items):
        # 順番を維持しつつ、ランダムに選ぶ
        random_indexes = random.sample(range(len(message_list)), num_items)
        return [message_list[index] for index in sorted(random_indexes)]
