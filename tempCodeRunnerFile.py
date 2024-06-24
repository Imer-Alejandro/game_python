def move_obstacle_until_free(obstacle_letter, new_pos, rows, cols):
    positions = elements[obstacle_letter]
    orientation = determine_orientation(positions)

    while not is_position_free(*new_pos, exclude_letter='A'):
        moved = False
        for x, y in positions:
            if orientation == 'vertical':
                possible_moves = [(x, y - 1), (x, y + 1)]
            elif orientation == 'horizontal':
                possible_moves = [(x - 1, y), (x + 1, y)]

            for move in possible_moves:
                if is_position_free(*move, exclude_letter=obstacle_letter):
                    elements[obstacle_letter].remove((x, y))
                    elements[obstacle_letter].append(move)
                    moved = True
                    break
            if moved:
                break

        if not moved:
            return False  # No se pudo mover el obstáculo

    return True  # Obstáculo movido exitosamente

def move_element(letter, key, rows, cols):
    if letter not in elements:
        return False

    positions = elements[letter]
    orientation = determine_orientation(positions)
    new_positions = []

    for x, y in positions:
        if orientation == 'vertical':
            if key == "UP":
                new_pos = (x, y - 1)
            elif key == "DOWN":
                new_pos = (x, y + 1)
            else:
                continue
        elif orientation == 'horizontal':
            if key == "LEFT":
                new_pos = (x - 1, y)
            elif key == "RIGHT":
                new_pos = (x + 1, y)
            else:
                continue

        if isinstance(new_pos, tuple):
            if new_pos[0] < 0 or new_pos[0] >= cols or new_pos[1] < 0 or new_pos[1] >= rows:
                return False  # Movimiento fuera de los límites del tablero

            if not is_position_free(*new_pos, exclude_letter=letter):
                if letter == 'A':
                    obstacle_letter = get_obstacle_at_position(new_pos)
                    if obstacle_letter:
                        if not move_obstacle_until_free(obstacle_letter, new_pos, rows, cols):
                            return False  # No se pudo mover el obstáculo

            new_positions.append(new_pos)

    if len(new_positions) == len(positions):
        elements[letter] = new_positions
        return True

    return False