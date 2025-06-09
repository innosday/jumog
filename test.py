import pygame
from threading import Event, Thread
import time
import random

class GameObject:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

def log_monitor(stop_event:Event):
    """
    데몬 스레드: 로그 모니터링
    """
    while not stop_event.is_set():
        log_level = random.choice(['INFO', 'WARNING', 'ERROR'])
        print(f"[로그 모니터] {log_level} 메시지 감지")
        time.sleep(2)

def spawn_objects(stop_event:Event, objects:list):
    """
    데몬 스레드: 랜덤 물체 소환
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # 빨강, 초록, 파랑, 노랑
    while not stop_event.is_set():
        # 랜덤 위치에 물체 생성
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        color = random.choice(colors)
        size = random.randint(20, 40)
        
        objects.append(GameObject(x, y, color, size))
        print(f"[물체 소환] 새로운 물체 생성: 위치({x}, {y}), 크기: {size}")
        time.sleep(3)  # 3초마다 새로운 물체 생성

def main():
    # 스레드 종료를 위한 이벤트 객체 생성
    stop_event = Event()
    
    # 게임 객체 리스트
    game_objects = []
    
    # 데몬 스레드들 시작
    log_thread = Thread(
        target=log_monitor,
        args=(stop_event,),
        daemon=True
    )
    
    spawn_thread = Thread(
        target=spawn_objects,
        args=(stop_event, game_objects),
        daemon=True
    )
    
    log_thread.start()
    spawn_thread.start()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("랜덤 물체 소환 예제")

    # 플레이어 물체 설정
    player = GameObject(400, 300, (255, 0, 0), 50)
    speed = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 키보드 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed
        if keys[pygame.K_UP]:
            player.y -= speed
        if keys[pygame.K_DOWN]:
            player.y += speed

        # 플레이어 경계 체크
        player.x = max(player.size//2, min(player.x, 800 - player.size//2))
        player.y = max(player.size//2, min(player.y, 600 - player.size//2))
        
        # 화면 그리기
        screen.fill((255, 255, 255))
        
        # 모든 게임 객체 그리기
        for obj in game_objects:
            pygame.draw.circle(screen, obj.color, (obj.x, obj.y), obj.size//2)
        
        # 플레이어 그리기
        pygame.draw.circle(screen, player.color, (player.x, player.y), player.size//2)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # 프로그램 종료
    print("\n프로그램 종료 중...")
    stop_event.set()
    pygame.quit()
    print("프로그램 종료 완료")

if __name__ == "__main__":
    main()