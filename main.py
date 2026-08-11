def orderedMove(self, player):
    size = self.game.board.SIZE
    considerCells = []
    neighborOffsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    for row in range(size):
        for col in range(size):
            if self.hypotheticalBoard[row][col] != "":
                continue

            nearStone = False
            for dx, dy in neighborOffsets:
                r, c = row + dx, col + dy
                if 0 <= r < size and 0 <= c < size and self.hypotheticalBoard[r][c] != "":
                    nearStone = True
                    break

            if not nearStone:
                continue

            length = 0
            for pos in self.vector:
                x, y = pos

                if row + x >= size or row + x < 0 or col + y >= size or col + y < 0:
                    continue

                if self.hypotheticalBoard[row + x][col + y] == player:
                    for i in range(3):
                        if x == 0: pass
                        elif x > 0: x += 1
                        elif x < 0: x -= 1
                        if y == 0: pass
                        elif y > 0: y += 1
                        elif y < 0: y -= 1

                        if row + x >= size or row + x < 0:
                            break
                        if col + y >= size or col + y < 0:
                            break

                        if self.hypotheticalBoard[row+x][col+y] == player:
                            length = i + 1
                        else:
                            length = i
                            break
                    break

            if length == 4:
                considerCells.insert(0, [row, col])
            else:
                considerCells.append([row, col])

    return considerCells
