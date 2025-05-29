import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False
selected_row = 0
selected_col = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            # R: restart the game
            if event.key == pygame.K_r:
                user = None
                board = ttt.initial_state()
                ai_turn = False
                selected_row = 0
                selected_col = 0
            elif user is None:
                # X: Choose x
                if event.key == pygame.K_x:
                    user = ttt.X
                # O: Choose O
                elif event.key == pygame.K_o:
                    user = ttt.O
            else:
                # Move within the chart with arrow keys
                if event.key == pygame.K_UP and selected_row > 0:
                    selected_row -= 1
                if event.key == pygame.K_DOWN and selected_row < 2:
                    selected_row += 1
                if event.key == pygame.K_LEFT and selected_col > 0:
                    selected_col -= 1
                if event.key == pygame.K_RIGHT and selected_col < 2:
                    selected_col += 1
                # Space: To mark the highlighted cell
                if event.key == pygame.K_SPACE and user == ttt.player(board) and not ttt.terminal(board):
                    if board[selected_row][selected_col] == ttt.EMPTY:
                        board = ttt.result(board, (selected_row, selected_col))

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        game_over = ttt.terminal(board)
        player = ttt.player(board)
        for i in range(3):
            row = []
            for j in range(3):
                # Define each tile rectangle
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                # Draw title border
                pygame.draw.rect(screen, white, rect, 3)

                # Draw x or o if cell is not empty
                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                # highlight the cell only if it's users turn and game is not over yet.
                if i == selected_row and j == selected_col and user == player and not game_over:
                    pygame.draw.rect(screen, (255, 255, 0), rect, 3)  # yellow highlight
                row.append(rect)
            tiles.append(row)



        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
