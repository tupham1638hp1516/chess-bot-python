from flask import Flask, render_template, request, jsonify
import chess
from Test import get_bot_move

app = Flask(__name__)
board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json 
    move_uci = data.get('move')
    corrections = {'e1h1': 'e1g1', 'e1a1': 'e1c1', 'e8h8': 'e8g8', 'e8a8': 'e8c8'}
    move_uci = corrections.get(move_uci, move_uci)
    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)
            if not board.is_game_over() and not board.turn:
                bot_move = get_bot_move(board)
                if bot_move:
                    board.push(bot_move)
            return jsonify({'success': True, 'fen': board.fen()})
        else:
            return jsonify({'success': False, 'error': 'Illegal move'})
    except Exception as e:  
        return jsonify({'success': False, 'error': str(e)}) 

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = chess.Board()
    if not board.turn:
        bot_move = get_bot_move(board)
        if bot_move:
            board.push(bot_move)
    return jsonify({'success': True, 'fen': board.fen()})

if __name__ == '__main__':
    app.run(debug=True)  