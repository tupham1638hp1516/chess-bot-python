import chess
transposition_table = {}

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 305,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 500000
}

PAWN_TABLE = [
    70, 70, 70, 70, 70, 70, 70, 70,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 10, 10, 10, 10, 10, 10,
    5,   5,  5,  5,  5,  5,  5,  5,
    0,   0,  5, 20, 20,  5,  0,  0,
    0,  0, -10,  5,  5, -10,  0,  0,
    5, 10,  -5, -10, -10,  -5, 10, 5,
    0,  0,  0 ,   0,   0,   0,  0, 0
]

KNIGHT_TABLE = [
    -50, -40, -40, -40, -40, -40, -40, -50,
    -40,   5,   0,   0,   0,   0,   5, -40,
    -30,   0,  10,  10,  10,  10,   5, -30,
      0,   0,   5,   0,   0,   5,   0,   0,
    -30,   5,  10,   0,   0,  10,   5, -30,
    -30,   0,  10,   5,   5,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -20, -30, -30, -30, -30, -20, -50
]

BISHOP_TABLE = [
    -10, -40, -40, -40, -40, -40, -40, -10,
      5,   5,   0,   0,   0,   0,   5,   5,
    -5,   0,   0,   0,   0,  10,   5,   -5,
    -10,   5,   5,   0,   0,   5,   5, -10,
    -30,   5,  10,   0,   0,  10,   5, -30,
    -30,   0,  10,   5,   5,  10,   0, -30,
      0,  10,   0,   0,   0,   0,  10,   0,
      5, -50, -20, -50, -50, -20, -50,   5
]

QUEEN_MIDDLE_TABLE = [
    -50, -50, -50,   5,   5, -50, -50, -50,
      5,   0,   0,   0,   0,   0,   0,   5,
      5,   0,   0,   0,   0,   0,   5,   5,
      5,   0,   0,   0,   0,   0,   0,   5,
      5,  -10,  10, -10, -10,  10, -10,  5,
      0,   0,  10,   5,   5,  10,   0,   0,
      0,  10,   0,   0,   0,   0,  10,   0,
    -50, -50,   0,   5,   5,   0, -50, -50
]

KING_MIDDLE_TABLE = [
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
     20,  30,   0,   0,   0,   0,  30,  20
]

ROOK_TABLE = [
      0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,
     10,   -10,   0,   0,   0,   0,   -10,  10
]

PIECE_SQUARE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_MIDDLE_TABLE,
    chess.KING: KING_MIDDLE_TABLE
}

def evaluate_board(board):#Đánh giá điểm bàn cờ
    
    if board.is_checkmate():
        return -50000 if board.turn else 20000
    """Nếu bị chiếu hết ( trong đây là quân trắng ) thì bàn cờ có điểm là -50000, còn nếu quân trắng chiếu hết thì điểm bàn cờ là 50000"""
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    """Tương tự thì nếu hòa, hoặc không đủ quân để chiếu hết thì điểm bàn cờ là 0"""

    score = 0
    
    # Tính điểm các quân + vị trí
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_value = PIECE_VALUES[piece.piece_type]# Giá trị quân
            piece_table = PIECE_SQUARE_TABLES.get(piece.piece_type, [0]*64)# Bảng điểm vị trí
            
            if piece.color == chess.WHITE:# Xét quân trắng
                score += piece_value + piece_table[square]
            else: #Nếu là quân đen => mirror vị trí
                mirrored_square = chess.square_mirror(square)
                score -= piece_value + piece_table[mirrored_square]
    
    # Thêm mobility (số nước đi hợp lệ), tăng tính linh hoạt
    original_turn = board.turn
    board.turn = chess.WHITE # Ép lượt sang Trắng
    white_mobility = len(list(board.legal_moves))
    board.turn = chess.BLACK # Ép lượt sang Đen
    black_mobility = len(list(board.legal_moves))
    board.turn = original_turn
    score += (white_mobility - black_mobility) * 2
    
    return score if board.turn else -score #Đảo chiều điểm nếu đến lượt đen

"""Hàm sắp xếp nước đi: ưu tiên nước ăn quân, nước chiếu sớm => giảm số node cần duyệt (alpha-beta pruning hiệu quả hơn)"""
def order_moves(board):
    """Sắp xếp nước đi: ưu tiên captures, promotions, checks"""
    move = list(board.legal_moves)
    
    def move_score(move):
        score_mark = 0
        
        # Ưu tiên chiếu
        board.push(move)
        if board.is_check():
             score_mark += 50000
        board.pop()

        # Ưu tiên promotion
        if move.promotion:
            score_mark += 10000

        # Ưu tiên captures (ăn quân)
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                score_mark += PIECE_VALUES[captured_piece.piece_type]
        
        
        return score_mark
    
    return sorted(moves, key=move_score, reverse=True)

def quiescence_search(board, alpha, beta):
    """Tìm kiếm quiescence để tránh đánh giá sai trong các tình huống biến động cao (như ăn quân)"""
    stand_pat = evaluate_board(board)
    
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    
    # Chỉ xét các nước ăn quân
    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence_search(board, -beta, -alpha)# Đảo chiều điểm
            board.pop()
            
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    
    return alpha

def minimax(board, depth, alpha, beta, maximizing):
    global transposition_table
    
    # Kiểm tra transposition table: Lưu trữ các kết quả trùng lặp để tránh tính toán lại=> Tối ưu thời gian
    #Ví dụ: Ở lần thứ 2 gặp một trạng thái, lấy từ cache thay vì tính lại
    fen = board.fen()
    if fen in transposition_table:#kiếm tra trạng thái đã được lưu
        cached_depth, cached_score, cached_move = transposition_table[fen]#lấy dữ liệu đã lưu
        if cached_depth >= depth:
            return cached_score, cached_move# Đây là kết quả đáng tin cậy
    
    # Điều kiện dừng
    if board.is_game_over():
        score = evaluate_board(board)
        return score, None
    
    if depth == 0:
        # Dùng quiescence search thay vì evaluate ngay
        score = quiescence_search(board, alpha, beta)
        return score, None
    
    # Sắp xếp nước đi
    moves = order_moves(board)
    best_move = None
    
    if maximizing:
        max_eval = float('-inf')#Điểm tốt nhất bằng âm vô cực để nước đầu tiên được cập nhật
        for move in moves:
            board.push(move)
            eval_score, _ = minimax(board, depth-1, alpha, beta, False)#Gọi đệ quy
            board.pop()
            
            if eval_score > max_eval:
                max_eval = eval_score#Câp nhật điểm tốt nhất
                best_move = move#Ghi nhớ
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:#Cắt tỉa alpha-beta
                break#Cắt nhánh ngay
        
        # Lưu vào transposition table
        transposition_table[fen] = (depth, max_eval, best_move)
        return max_eval, best_move#Điểm tốt nhất và nước đi tương ứng
    
    else:
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval_score, _ = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        
        # Lưu vào transposition table
        transposition_table[fen] = (depth, min_eval, best_move)
        return min_eval, best_move

"""Gọi minimax với chiều sâu tăng dần (iterative deepening) để hạn chế tính quá lâu, tối ưu nước đi trong thời gian cho phép."""
def get_bot_move(board, max_depth=3, time_limit=5):
    """Tìm nước đi với iterative deepening"""
    import time
    
    global transposition_table
    """Mỗi lần bot đi nước mới, bàn cờ thay đổi => cache cũ không còn giá trị"""
    transposition_table = {}  # Reset cache mỗi nước
    
    best_move = None#Khởi tạo, chưa tìm được nước tốt
    start_time = time.time()
    
    for depth in range(1, max_depth + 1):#Nếu hết thời gian, bot có kết quả tốt nhất từ độ sâu cấp trước
        try:
            _, move = minimax(board, depth, float('-inf'), float('inf'), board.turn)
            if move:
                best_move = move
            
            # Dừng sớm nếu vượt quá thời gian
            elapsed = time.time() - start_time
            if elapsed > time_limit:#Thời gian giới hạn
                break
                
        except Exception as e:
            print(f"Error at depth {depth}: {e}")
            break
    
    return best_move if best_move else list(board.legal_moves)[0]