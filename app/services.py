from app.models import PattiGame
from app.tasks import start_new_patti_game,my_task

def check_and_start_game():
    game = PattiGame.objects.filter(status='OPEN').exists()
    print("GAME FOUND :: STARING")
    my_task.apply_async(args=[], countdown=1)
    if not game:
        print("HERE IS COMING")
        PattiGame.objects.create(status='OPEN')
        start_new_patti_game.apply_async(args=[],countdown=3)
     
def stop_game():
    games = PattiGame.objects.filter(status='OPEN')
    print(f"###### CLOED ##### {games=}")
    if games:
        for game in games:
            game.status = 'closed'
            game.save()