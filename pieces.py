"""Defines all pieces (Pawn, Rook, Bishop, Knight, Queen, King)."""

class Pawn: 
    def __init__(self, color, position=None): 
        self.color = color.lower()
        self.shorthand = "P" if self.color == "white" else "p"
        self.position = position
        self.move_counter = 0
    
    def __repr__(self): 
        return self.shorthand

class Rook: 
    def __init__(self, color, position=None): 
        self.color = color.lower()
        self.shorthand = "R" if self.color == "white" else "r"
        self.position = position
        self.move_counter = 0

    def __repr__(self): 
        return self.shorthand

class Knight: 
    def __init__(self, color, position=None): 
        self.color = color.lower()
        self.shorthand = "N" if self.color == "white" else "n"
        self.position = position
        self.move_counter = 0

    def __repr__(self): 
        return self.shorthand

class Bishop: 
    def __init__(self, color, position=None): 
        self.color = color.lower()
        self.shorthand = "B" if self.color == "white" else "b"
        self.position = position
        self.move_counter = 0

    def __repr__(self): 
        return self.shorthand

class King: 
    def __init__(self, color, position=None): 
        self.color = color.lower()
        self.shorthand = "K" if self.color == "white" else "k"
        self.position = position
        self.move_counter = 0

    def __repr__(self): 
        return self.shorthand

class Queen: 
    def __init__(self, color, position=None): 
        self.color = color.lower()
        self.shorthand = "Q" if self.color == "white" else "q"
        self.position = position
        self.move_counter = 0

    def __repr__(self): 
        return self.shorthand

class Empty: 
    def __init__(self): 
        self.shorthand = " "

    def __repr__(self): 
        return " "