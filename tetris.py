import curses
import random
import time

BOARD_W, BOARD_H = 10, 20

TETROMINOES = {
    'I': [[(0,1),(1,1),(2,1),(3,1)], [(2,0),(2,1),(2,2),(2,3)]],
    'O': [[(1,0),(2,0),(1,1),(2,1)]],
    'T': [[(0,1),(1,1),(2,1),(1,0)], [(1,0),(1,1),(1,2),(2,1)], [(0,1),(1,1),(2,1),(1,2)], [(1,0),(1,1),(1,2),(0,1)]],
    'S': [[(1,0),(2,0),(0,1),(1,1)], [(1,0),(1,1),(2,1),(2,2)]],
    'Z': [[(0,0),(1,0),(1,1),(2,1)], [(2,0),(1,1),(2,1),(1,2)]],
    'J': [[(0,0),(0,1),(1,1),(2,1)], [(1,0),(2,0),(1,1),(1,2)], [(0,1),(1,1),(2,1),(2,2)], [(1,0),(1,1),(0,2),(1,2)]],
    'L': [[(2,0),(0,1),(1,1),(2,1)], [(1,0),(1,1),(1,2),(2,2)], [(0,1),(1,1),(2,1),(0,2)], [(0,0),(1,0),(1,1),(1,2)]],
}

COLORS = {'I': 1, 'O': 2, 'T': 3, 'S': 4, 'Z': 5, 'J': 6, 'L': 7}

def new_piece():
    shape = random.choice(list(TETROMINOES.keys()))
    return {'shape': shape, 'rot': 0, 'x': 3, 'y': 0}

def cells(piece):
    rotations = TETROMINOES[piece['shape']]
    rot = piece['rot'] % len(rotations)
    return [(piece['x'] + dx, piece['y'] + dy) for dx, dy in rotations[rot]]

def valid(board, piece):
    for x, y in cells(piece):
        if x < 0 or x >= BOARD_W or y >= BOARD_H:
            return False
        if y >= 0 and board[y][x]:
            return False
    return True

def place(board, piece):
    color = COLORS[piece['shape']]
    for x, y in cells(piece):
        if y >= 0:
            board[y][x] = color

def clear_lines(board):
    cleared = [row for row in board if any(c == 0 for c in row)]
    n = BOARD_H - len(cleared)
    return [[0] * BOARD_W for _ in range(n)] + cleared, n

def draw(stdscr, board, piece, score, level, next_piece):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    ox, oy = (w - BOARD_W * 2 - 2) // 2, (h - BOARD_H - 2) // 2

    # 테두리
    for y in range(BOARD_H + 2):
        stdscr.addstr(oy + y, ox, '|')
        stdscr.addstr(oy + y, ox + BOARD_W * 2 + 1, '|')
    stdscr.addstr(oy + BOARD_H + 1, ox, '+' + '-' * (BOARD_W * 2) + '+')
    stdscr.addstr(oy, ox, '+' + '-' * (BOARD_W * 2) + '+')

    # 보드
    for y, row in enumerate(board):
        for x, c in enumerate(row):
            if c:
                try:
                    stdscr.addstr(oy + 1 + y, ox + 1 + x * 2, '[]', curses.color_pair(c))
                except curses.error:
                    pass

    # 현재 블록
    for x, y in cells(piece):
        if y >= 0:
            try:
                stdscr.addstr(oy + 1 + y, ox + 1 + x * 2, '[]', curses.color_pair(COLORS[piece['shape']]))
            except curses.error:
                pass

    # 사이드 패널
    px = ox + BOARD_W * 2 + 4
    stdscr.addstr(oy + 1,  px, f'점수: {score}')
    stdscr.addstr(oy + 2,  px, f'레벨: {level}')
    stdscr.addstr(oy + 4,  px, 'NEXT:')
    for dx, dy in TETROMINOES[next_piece['shape']][0]:
        try:
            stdscr.addstr(oy + 6 + dy, px + dx * 2, '[]', curses.color_pair(COLORS[next_piece['shape']]))
        except curses.error:
            pass
    stdscr.addstr(oy + 10, px, '←→ : 이동')
    stdscr.addstr(oy + 11, px, '↑  : 회전')
    stdscr.addstr(oy + 12, px, '↓  : 내리기')
    stdscr.addstr(oy + 13, px, 'q  : 종료')

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN,    curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN,   curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED,     curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE,    curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE,   curses.COLOR_BLACK)

    board = [[0] * BOARD_W for _ in range(BOARD_H)]
    piece = new_piece()
    next_piece = new_piece()
    score, level, lines_total = 0, 1, 0
    last_fall = time.time()
    score_table = [0, 100, 300, 500, 800]

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT:
            moved = {**piece, 'x': piece['x'] - 1}
            if valid(board, moved):
                piece = moved
        elif key == curses.KEY_RIGHT:
            moved = {**piece, 'x': piece['x'] + 1}
            if valid(board, moved):
                piece = moved
        elif key == curses.KEY_UP:
            rotated = {**piece, 'rot': piece['rot'] + 1}
            if valid(board, rotated):
                piece = rotated
        elif key == curses.KEY_DOWN:
            dropped = {**piece, 'y': piece['y'] + 1}
            if valid(board, dropped):
                piece = dropped

        interval = max(0.1, 0.8 - (level - 1) * 0.07)
        if time.time() - last_fall > interval:
            dropped = {**piece, 'y': piece['y'] + 1}
            if valid(board, dropped):
                piece = dropped
            else:
                place(board, piece)
                board, n = clear_lines(board)
                lines_total += n
                score += score_table[min(n, 4)]
                level = lines_total // 10 + 1
                piece = next_piece
                next_piece = new_piece()
                if not valid(board, piece):
                    break
            last_fall = time.time()

        draw(stdscr, board, piece, score, level, next_piece)

    stdscr.nodelay(False)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    msg = f'게임 오버! 최종 점수: {score}'
    stdscr.addstr(h // 2, (w - len(msg)) // 2, msg)
    stdscr.addstr(h // 2 + 1, (w - 16) // 2, '아무 키나 누르세요')
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
