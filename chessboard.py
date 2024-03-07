import pygame
import sys
from Engine import State
from Engine import move
import requests
import json
import time
import threading

#board
board = []

# frames
FPS = 15

# Define colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# accessing images
IMAGES = {}

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_SIZE = (550, 550)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess Board")

# Set the size of each square
SQUARE_SIZE = WINDOW_SIZE[0] // 8

# number law
law = 0


# Function to draw the chessboard
def draw_board():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = GREY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"),
                                               (SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def check_law(clicks_prev, board):
    global law
    check1 = clicks_prev[0]
    check2 = clicks_prev[1]
    if board[check1[0]][check1[1]] == "--":
        law = -1

    if clicks_prev[0] == clicks_prev[1]:
        law = -1

    char1 = board[check1[0]][check1[1]]
    char2 = board[check2[0]][check2[1]]

    if char1[0] == char2[0]:
        law = -1

    if char1 == "wp":
        if check1[0] == 6:
            print(char1)
            value = check1[0] - check2[0]
            print(value)
            if value > 2:
                law = -1

        if check1[0] != 6:
            if check1[0] - check2[0] != 1:
                law = -1

        if char2[0] == "b":
            if check1[1] == check2[1]:
                law = -1

        if check1[1] <= 6:
            if board[check1[0] - 1][check1[1] + 1] == "--":
                if check2[0] == (check1[0] - 1) and check2[1] == (check1[1] + 1):
                    law = -1

        if board[check1[0] - 1][check1[1] - 1] == "--":
            if check2[0] == (check1[0] - 1) and check2[1] == (check1[1] - 1):
                law = -1

        if check2[0] - check1[0] >= 1:
            law = -1

        if check2[0] == check1[0]:
            law = -1

    if char1 == "bp":
        if check1[0] == 1:
            print(char1)
            value = check2[0] - check1[0]
            print(value)
            if value > 2:
                law = -1

        if check1[0] != 1:
            if check2[0] - check1[0] != 1:
                law = -1

        if char2[0] == "w":
            if check1[1] == check2[1]:
                law = -1

        if check1[1] <= 6:
            if board[check1[0] + 1][check1[1] + 1] == "--":
                if check2[0] == check1[0] + 1 and check2[1] == check1[1] + 1:
                    law = -1

        if board[check1[0] + 1][check1[1] - 1] == "--":
            if check2[0] == (check1[0] + 1) and check2[1] == (check1[1] - 1):
                law = -1

        if check2[0] - check1[0] <= -1:
            law = -1

    if char1 == "wR":
        if check1[0] - check2[0] != 0 and check1[1] - check2[1] != 0:
            law = -1

        if check2[0] - check1[0] < 0:
            rang = check1[0] - check2[0]
            print(rang)
            count = 0
            cek = check1[0] - 1
            while count < rang - 1:
                word = board[cek - count][check1[1]]
                if word[0] == "w":
                    law = -1
                count = count + 1

        if check2[1] - check1[1] > 0:
            rang = check2[1] - check1[1]
            print(rang)
            count = 0
            cek = check1[1] + 1
            while count < rang - 1:
                word = board[check2[0]][cek + count]
                if word[0] == "w":
                    law = -1
                count = count + 1

        if check2[1] - check1[1] < 0:
            rang = check1[1] - check2[1]
            print(rang)
            count = 0
            cek = check1[1] - 1
            while count < rang - 1:
                word = board[check2[0]][cek - count]
                if word[0] == "w":
                    law = -1
                count = count + 1

        if check2[0] - check1[0] > 0:
            rang = check2[0] - check1[0]
            print(rang)
            count = 0
            cek = check1[0] + 1
            while count < rang - 1:
                word = board[cek+count][check2[1]]
                if word[0] == "w":
                    law = -1
                count = count + 1


    if char1 == "bR":
        if check1[0] - check2[0] != 0 and check1[1] - check2[1] != 0:
            law = -1

        if check2[0] - check1[0] < 0:
            rang = check1[0] - check2[0]
            print(rang)
            count = 0
            cek = check1[0] - 1
            while count < rang - 1:
                word = board[cek - count][check1[1]]
                if word[0] == "b":
                    law = -1
                count = count + 1

        if check2[1] - check1[1] > 0:
            rang = check2[1] - check1[1]
            print(rang)
            count = 0
            cek = check1[1] + 1
            while count < rang - 1:
                word = board[check2[0]][cek + count]
                if word[0] == "b":
                    law = -1
                count = count + 1

        if check2[1] - check1[1] < 0:
            rang = check1[1] - check2[1]
            print(rang)
            count = 0
            cek = check1[1] - 1
            while count < rang - 1:
                word = board[check2[0]][cek - count]
                if word[0] == "b":
                    law = -1
                count = count + 1

        if check2[0] - check1[0] > 0:
            rang = check2[0] - check1[0]
            print(rang)
            count = 0
            cek = check1[0] + 1
            while count < rang - 1:
                word = board[cek+count][check2[1]]
                if word[0] == "b":
                    law = -1
                count = count + 1

    if char1 == "wN":
        if abs(check1[0] - check2[0]) == 2 or abs(check1[1] - check2[1]) == 2:
            if abs(check1[0] - check2[0]) == 2:
                if abs(check1[1] - check2[1]) != 1:
                    law = -1

            if abs(check1[1] - check2[1]) == 2:
                if abs(check1[0] - check2[0]) != 1:
                    law = -1

        if abs(check2[0] - check1[0]) == 1 and abs(check2[1] - check1[1]) == 1:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] == 1:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] == -1:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] <= 3:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] >= 1:
            law = -1

        if check1[1] == check2[1]:
            law = -1

    if char1 == "bN":
        if abs(check1[0] - check2[0]) == 2 or abs(check1[1] - check2[1]) == 2:
            if abs(check1[0] - check2[0]) == 2:
                if abs(check1[1] - check2[1]) != 1:
                    law = -1

            if abs(check1[1] - check2[1]) == 2:
                if abs(check1[0] - check2[0]) != 1:
                    law = -1

        if abs(check2[0] - check1[0]) == 1 and abs(check2[1] - check1[1]) == 1:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] == 1:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] == -1:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] <= 3:
            law = -1

        if check1[0] == check2[0] and check2[1] - check1[1] >= 1:
            law = -1

        if check1[1] == check2[1]:
            law = -1

    if char1 == "wB":
        if check1[0] == check2[0]:
            law = -1

        if check1[1] == check2[1]:
            law = -1

        #up and right direction
        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] + 1
            while count < rang-1:
                let = board[y-count][x+count]
                if let != "--":
                    law = -1
                count += 1

        #down and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] + 1
            x = check1[1] - 1
            while count < rang-1:
                let = board[y+count][x-count]
                if let != "--":
                    law = -1
                count += 1

        #up and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] - 1
            while count < rang-1:
                let = board[y-count][x-count]
                if let != "--":
                    law = -1
                count += 1
        #down and right
        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0]+1
            x = check1[1]+1
            while count < rang-1:
                let = board[y+count][x+count]
                if let != "--":
                    law = -1
                count += 1





    if char1 == "bB":
        if check1[0] == check2[0]:
            law = -1

        if check1[1] == check2[1]:
            law = -1

        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] + 1
            while count < rang-1:
                let = board[y-count][x+count]
                if let != "--":
                    law = -1
                count += 1

        #down and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] + 1
            x = check1[1] - 1
            while count < rang-1:
                let = board[y+count][x-count]
                if let != "--":
                    law = -1
                count += 1

        #up and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] - 1
            while count < rang-1:
                let = board[y-count][x-count]
                if let != "--":
                    law = -1
                count += 1
        #down and right
        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0]+1
            x = check1[1]+1
            while count < rang-1:
                let = board[y+count][x+count]
                if let != "--":
                    law = -1
                count += 1

    if char1 == "wK":
        if abs(check1[0] - check2[0]) > 1:
            law = -1

        if abs(check1[1] - check2[1]) > 1:
            law = -1

    if char1 == "bK":
        if abs(check1[0] - check2[0]) > 1:
            law = -1

        if abs(check1[1] - check2[1]) > 1:
            law = -1

    if char1 == "wQ":
        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] + 1
            while count < rang - 1:
                let = board[y - count][x + count]
                if let != "--":
                    law = -1
                count += 1

            # down and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] + 1
            x = check1[1] - 1
            while count < rang - 1:
                let = board[y + count][x - count]
                if let != "--":
                    law = -1
                count += 1

            # up and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] - 1
            while count < rang - 1:
                let = board[y - count][x - count]
                if let != "--":
                    law = -1
                count += 1
            # down and right
        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0] + 1
            x = check1[1] + 1
            while count < rang - 1:
                let = board[y + count][x + count]
                if let != "--":
                    law = -1
                count += 1

        if check2[1]-check1[1] < 0 and check1[0] == check2[0]:
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            x = check1[1] - 1
            while count < rang - 1:
                let = board[check2[0]][x-count]
                if let != "--":
                    law = -1
                count += 1

        if check2[1]-check1[1] > 0 and check1[0] == check2[0]:
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            x = check1[1] + 1
            while count < rang - 1:
                let = board[check2[0]][x+count]
                if let != "--":
                    law = -1
                count += 1

        if check2[0]-check1[0] >0 and check1[1] == check2[1]:
            count = 0
            rang = check2[0]-check1[0]
            y = check1[0] + 1
            while count < rang - 1:
                let = board[y+count][check1[1]]
                if let != "--":
                    law = -1
                count += 1


        if check2[0]-check1[0] <0 and check1[1] == check2[1]:
            count = 0
            rang = check1[0]-check2[0]
            y = check1[0] - 1
            while count < rang - 1:
                let = board[y-count][check1[1]]
                if let != "--":
                    law = -1
                count += 1

    if char1 == "bQ":
        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] + 1
            while count < rang - 1:
                let = board[y - count][x + count]
                if let != "--":
                    law = -1
                count += 1

            # down and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] + 1
            x = check1[1] - 1
            while count < rang - 1:
                let = board[y + count][x - count]
                if let != "--":
                    law = -1
                count += 1

            # up and left direction
        if (check2[1] - check1[1] < 0) and (check2[0] - check1[0] < 0):
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            y = check1[0] - 1
            x = check1[1] - 1
            while count < rang - 1:
                let = board[y - count][x - count]
                if let != "--":
                    law = -1
                count += 1
            # down and right
        if (check2[1] - check1[1] > 0) and (check2[0] - check1[0] > 0):
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            y = check1[0] + 1
            x = check1[1] + 1
            while count < rang - 1:
                let = board[y + count][x + count]
                if let != "--":
                    law = -1
                count += 1

        if check2[1]-check1[1] < 0 and check1[0] == check2[0]:
            count = 0
            rang = check1[1] - check2[1]
            print(rang)
            x = check1[1] - 1
            while count < rang - 1:
                let = board[check2[0]][x-count]
                if let != "--":
                    law = -1
                count += 1

        if check2[1]-check1[1] > 0 and check1[0] == check2[0]:
            count = 0
            rang = check2[1] - check1[1]
            print(rang)
            x = check1[1] + 1
            while count < rang - 1:
                let = board[check2[0]][x+count]
                if let != "--":
                    law = -1
                count += 1

        if check2[0]-check1[0] >0 and check1[1] == check2[1]:
            count = 0
            rang = check2[0]-check1[0]
            y = check1[0] + 1
            while count < rang - 1:
                let = board[y+count][check1[1]]
                if let != "--":
                    law = -1
                count += 1


        if check2[0]-check1[0] <0 and check1[1] == check2[1]:
            count = 0
            rang = check1[0]-check2[0]
            y = check1[0] - 1
            while count < rang - 1:
                let = board[y-count][check1[1]]
                if let != "--":
                    law = -1
                count += 1

def send_board(board):
    global law
    player_id = "player1"
    data = {'array': board, 'player_id': player_id}

    data_json = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post('http://100.25.179.191:5001/upload', data=data_json, headers=headers)

        if response.status_code == 200:
            print("Array sent successfully.")

        else:
            print(f"Error sending array: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending array: {e}")

def get_array(stop_event):
    global board
    print("Thread for board update")
    while not stop_event.is_set():
        try:
            response = requests.get('http://100.25.179.191:5001/')
            if response.status_code == 200:
                    print(response.json())
                    data = response.json()
                    board = data['array']

            else:

                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        time.sleep(2)
    print("Threading stopped")

def reset_board():
    
    board = [
                 ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  # Black back rank
                 ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # Black pawns
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # White pawns
                 ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]   # White back rank
        ]

    send_board(board)
    print("Board reset")


def main():
    global law
    global board

    load_images()
    game = State()
    running = True
    clock = pygame.time.Clock()
    selected = ()
    clicks_prev = []
    count = 0
    stop_event = threading.Event()

    board = game.board


    # Create and start the thread
    thread = threading.Thread(target=get_array, args=(stop_event,))
    thread.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reset_board()
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                col = mouse[0] // SQUARE_SIZE
                row = mouse[1] // SQUARE_SIZE

                selected = (row, col)
                clicks_prev.append(selected)

                if len(clicks_prev) == 2:
                    check_law(clicks_prev, board)
                    if law == 0:
                        move(clicks_prev[0], clicks_prev[1], board)
                        send_board(board)
                        clicks_prev = []

        # Draw the chessboard
        #draw_board()



        # write a function that waits for the server response

        draw_board()


        #allow next movement
        law = 0

        #hold for 0.7 seconds
        #time.sleep(1)

        # draw pieces
        draw_pieces(screen, board)

        # Update the display
        pygame.display.flip()

        # frames
        clock.tick(FPS)
    stop_event.set()  # Signal the thread to stop

    # Wait for the thread to finish
    thread.join()

if __name__ == "__main__":
    main()

