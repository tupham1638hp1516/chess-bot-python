import chess
transposition_table = {}#Lưu trữ trạng thái đã đánh giá

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

import chess

""" Bảng điểm cho các quân cờ tùy vào vị trí nó đang có trên bàn cờ. Bảng viết theo góc
nhìn quân trắng (a8 -> h1). Để tính điểm cho quân đen, ta sẽ mirror vị trí """
# Bảng điểm cho Tốt (Pawn)
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,   # Hàng 8
    50, 50, 50, 50, 50, 50, 50, 50,  # Hàng 7 
    10, 10, 20, 30, 30, 20, 10, 10,  # Hàng 6
    5,  5, 10, 20, 20, 10,  5,  5,   # Hàng 5 
    0,  0,  0, 15, 15,  0,  0,  0,   # Hàng 4 
    5, -5,-10,  0,  0,-10, -5,  5,   # Hàng 3
    5, 10, 10,-10,-10, 10, 10,  5,   # Hàng 2 
    0,  0,  0,  0,  0,  0,  0,  0    # Hàng 1
]

# Bảng điểm cho Mã (Knight)
KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,  # Hàng 8 
    -40,-20,  0,  5,  5,  0,-20,-40,  # Hàng 7
    -30,  0, 10, 15, 15, 10,  0,-30,  # Hàng 6 
    -30,  5, 15, 20, 20, 15,  5,-30,  # Hàng 5
    -30,  0, 15, 20, 20, 15,  0,-30,  # Hàng 4
    -30,  5, 20, 15, 15, 20,  5,-30,  # Hàng 3 
    -40,-20,  0,  5,  5,  0,-20,-40,  # Hàng 2
    -50,-40,-30,-30,-30,-30,-40,-50   # Hàng 1 
]

# Bảng điểm cho Tượng (Bishop)
BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

# Bảng điểm cho Xe (Rook)
ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,   # Hàng 8
    5, 10, 10, 10, 10, 10, 10,  5,  # Hàng 7 
  -10, -5,  0,  0,  0,  0, -5,-10,  # Hàng 6 
  -10, -5,  0,  0,  0,  0, -5,-10,  # Hàng 5
  -10, -5,  0,  0,  0,  0, -5,-10,  # Hàng 4
  -10, -5,  0,  0,  0,  0, -5,-10,  # Hàng 3
  -10, -5,  0,  0,  0,  0, -5,-10,  # Hàng 2
    0,  0,  0,  5,  5,  0,  0,  0   # Hàng 1 
]

# Bảng điểm cho Hậu (Queen)
QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,  # Hàng 8 
    -10,  0,  0,  0,  0,  0,  0,-10,  # Hàng 7
    -10,  0,  0,  5,  5,  0,  0,-10,  # Hàng 6
     -5,  0,  0,  5,  5,  0,  0, -5,  # Hàng 5
    -10,  0,  0,  5,  5,  0,  0,-10,  # Hàng 4
    -10,  0,  0,  5,  5,  0,  0,-10,  # Hàng 3
    -10,  0,  0,  0,  0,  0,  0,-10,  # Hàng 2
    -20,-10,-10, -5, -5,-10,-10,-20   # Hàng 1 
]

# Bảng điểm cho VUA (King) - Giai đoạn giữa cuộc
KING_MIDDLE_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]

# Bảng điểm cho VUA (King) - Giai đoạn tàn cuộc
KING_END_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

PIECE_SQUARE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_MIDDLE_TABLE  # Sẽ đổi sang KING_END_TABLE ở endgame
}

def evaluate_board(board):
    """Trả về điểm số của bàn cờ theo tiêu chí: giá trị quân + vị trí + mobility"""
    if board.is_checkmate():
        return -20000 if board.turn else 20000 #ưu tiên chiếu/ các nước có khả năng chiếu
    if board.is_stalemate() or board.is_insufficient_material():# Hòa
        return 0
    
    score = 0
    
    # Tính điểm các quân + vị trí
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_value = PIECE_VALUES[piece.piece_type]# Giá trị quân
            piece_table = PIECE_SQUARE_TABLES.get(piece.piece_type, [0]*64)# Bảng điểm vị trí
            
            if piece.color == chess.WHITE:# Xét quân trắng
                position_value = piece_table[square]
                score += piece_value + position_value
            else: #Nếu là quân đen => mirror vị trí
                mirrored_square = chess.square_mirror(square)
                position_value = piece_table[mirrored_square]
                score -= piece_value + position_value
    
    # Thêm mobility (số nước đi hợp lệ), tăng tính linh hoạt
    mobility = len(list(board.legal_moves))
    if board.turn:  # Trắng
        score += mobility * 2
    else:  # Đen
        score -= mobility * 2
    
    return score if board.turn else -score #Đảo chiều điểm nếu đến lượt đen

"""Hàm sắp xếp nước đi: ưu tiên nước ăn quân, nước chiếu sớm => giảm số node cần duyệt (alpha-beta pruning hiệu quả hơn)"""
def order_moves(board):
    """Sắp xếp nước đi: ưu tiên captures, promotions, checks"""
    moves = list(board.legal_moves)
    
    def move_score(move):
        score = 0
        
        # Ưu tiên captures (ăn quân)
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                attacker = board.piece_at(move.from_square)
                score += PIECE_VALUES[captured_piece.piece_type] * 10
                score -= PIECE_VALUES[attacker.piece_type]
        
        # Ưu tiên promotion
        if move.promotion:
            score += PIECE_VALUES.get(move.promotion, 0)
        
        # Ưu tiên chiếu/ nước ghim vv
        board.push(move)
        if board.is_check():
             score += 50
        board.pop()
        
        return score
    
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