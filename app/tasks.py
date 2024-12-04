from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import time
from app.models import PattiGame

card_list = {
        "1": "https://img.freepik.com/free-vector/ace-spades-playing-card-isolated_1308-78891.jpg?size=626&ext=jpg&ga=GA1.1.1141335507.1719273600&semt=sph",
        "2": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-88776.jpg?t=st=1719641559~exp=1719645159~hmac=06a9cc25b13885bff9cffcab964a43cf0ee859b5daadcfe6e3597f3ac0fec9a5&w=900",
        "3": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-79074.jpg?t=st=1719641619~exp=1719645219~hmac=5dc2cd692d2e0e77c333f2d936370b1f569e77ad4eb69897f79379a71ee83902&w=900",
        "4": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-82069.jpg?t=st=1719641698~exp=1719645298~hmac=d5ee15ef2c7afd9a67659aaf2af156b27502e79dac2b576232b29d6426996718&w=900",
        "5": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-78990.jpg?t=st=1719641716~exp=1719645316~hmac=1524688cf6b22246629e29b32d07ef89c244391116afe2f49b9b2d5762ccc527&w=900",
        "6": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-90597.jpg?t=st=1719641765~exp=1719645365~hmac=9cb7efbbb85ccf3a75c6f97da29d17266d32be5517628a7a47cf3b395c07253d&w=900",
        "8": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-78766.jpg?t=st=1719641794~exp=1719645394~hmac=6303771f11eb1afdd13a466ba2bdae966e314df40ab36f4018a2ee95bf294840&w=900",
        "10":"https://img.freepik.com/free-vector/ten-spades-playing-card-isolated_1308-79368.jpg?t=st=1719641660~exp=1719645260~hmac=c0113c2018010906bfee33f04dda2ffa105936b653077c6c564d448b6b074d8c&w=900",
        "1": "https://img.freepik.com/free-vector/ace-spades-playing-card-isolated_1308-78891.jpg?size=626&ext=jpg&ga=GA1.1.1141335507.1719273600&semt=sph",
        "2": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-88776.jpg?t=st=1719641559~exp=1719645159~hmac=06a9cc25b13885bff9cffcab964a43cf0ee859b5daadcfe6e3597f3ac0fec9a5&w=900",
        "3": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-79074.jpg?t=st=1719641619~exp=1719645219~hmac=5dc2cd692d2e0e77c333f2d936370b1f569e77ad4eb69897f79379a71ee83902&w=900",
        "4": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-82069.jpg?t=st=1719641698~exp=1719645298~hmac=d5ee15ef2c7afd9a67659aaf2af156b27502e79dac2b576232b29d6426996718&w=900",
        "5": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-78990.jpg?t=st=1719641716~exp=1719645316~hmac=1524688cf6b22246629e29b32d07ef89c244391116afe2f49b9b2d5762ccc527&w=900",
        "6": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-90597.jpg?t=st=1719641765~exp=1719645365~hmac=9cb7efbbb85ccf3a75c6f97da29d17266d32be5517628a7a47cf3b395c07253d&w=900",
        "8": "https://img.freepik.com/free-vector/ace-diamonds-playing-card-isolated_1308-78766.jpg?t=st=1719641794~exp=1719645394~hmac=6303771f11eb1afdd13a466ba2bdae966e314df40ab36f4018a2ee95bf294840&w=900",
        "10":"https://img.freepik.com/free-vector/ten-spades-playing-card-isolated_1308-79368.jpg?t=st=1719641660~exp=1719645260~hmac=c0113c2018010906bfee33f04dda2ffa105936b653077c6c564d448b6b074d8c&w=900",
    }

@shared_task
def start_new_patti_game():
    print(f"############### here task.. ############")
    game = PattiGame.objects.filter(status='OPEN').exists()
    print(f"########## GANE {game=}")
    if not game:
        return
    random_card = random.choice(["1", "2", "3", "4", "5", "6", "8", "10"])
    async_to_sync(get_channel_layer().group_send)(
            "patti",
            {"type": "start_game", "data": {"event_name":"start_game","card_link": card_list[random_card]}},
        )
    start_to_send_card_left_right.apply_async(args=[random_card],countdown=10)


@shared_task
def start_to_send_card_left_right(win_card):
    

    card_side = 0
    random_card = random.choice(list(card_list.keys()))  # Convert keys to list
    game = PattiGame.objects.filter(status='OPEN').exists()
    while int(random_card) != int(win_card) and game:
        async_to_sync(get_channel_layer().group_send)(
            "patti",
            {"type": "send_card_side_event", "data": {"event_name":"left_right","card_link": card_list[random_card], "side": card_side, "is_win": False,"random_card":random_card,"win_card":win_card}},
        )
        card_side = 1 if card_side == 0 else 0
        random_card = random.choice(list(card_list.keys()))  # Update random_card inside the loop
        print(f"loop running. {int(random_card) != int(win_card)} {int(win_card)=} {random_card}")
        time.sleep(1.5)
        
    async_to_sync(get_channel_layer().group_send)(
            "patti",
            {"type": "send_card_side_event", "data": {"event_name":"left_right","card_link": card_list[random_card], "side": card_side, "is_win": False,"random_card":random_card,"win_card":win_card}},
        )
    time.sleep(2)
    async_to_sync(get_channel_layer().group_send)(
        "patti",
        {"type": "send_winner", "data": {"event_name":"send_winner", "side": card_side, "is_win": False}},
    )
    
    restart_game.apply_async(args=[], countdown=1)

@shared_task
def restart_game():
    start_new_patti_game.apply_async(args=[], countdown=1)



@shared_task
def my_task():
    # Your task implementation here
    print(f'Task executed with arguments: ')