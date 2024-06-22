class DFSSolver:
    def __init__(self, initial_state, rows, cols):
        self.initial_state = initial_state
        self.rows = rows
        self.cols = cols
        self.visited = set()

    def solve(self):
        start = self.initial_state['A']
        goal = self.initial_state['goal'][0]

        # Determine the orientation of 'A'
        orientation = self.determine_orientation(start)

        # Get direction of movement based on goal position
        direction = self.get_direction(start, goal, orientation)

        # Perform the search
        path, obstacles = self.dfs(start[0], direction)
        filtered_path = self.filter_path(path, goal)
        return filtered_path, obstacles

    def dfs(self, current_position, direction):
        path = []
        obstacles = []

        x, y = current_position

        while (x, y) != tuple(self.initial_state['goal'][0]):
            path.append((x, y))
            next_position = self.get_next_position((x, y), direction)

            if not next_position:
                break

            x, y = next_position
            if not self.is_within_bounds(x, y):
                break

            if not self.is_position_free(x, y):
                # Identify obstacle and its letter
                for letter, positions in self.initial_state['obstacles'].items():
                    if (x, y) in positions:
                        obstacles.append((x, y, letter))
                        break

        path.append((x, y))
        return path, obstacles

    def determine_orientation(self, positions):
        if len(set(x for x, y in positions)) == 1:
            return 'vertical'
        return 'horizontal'

    def get_direction(self, start, goal, orientation):
        if orientation == 'vertical':
            return "DOWN" if goal[1] > start[0][1] else "UP"
        return "RIGHT" if goal[0] > start[0][0] else "LEFT"

    def get_next_position(self, position, direction):
        x, y = position
        if direction == "UP":
            return (x, y - 1)
        if direction == "DOWN":
            return (x, y + 1)
        if direction == "LEFT":
            return (x - 1, y)
        if direction == "RIGHT":
            return (x + 1, y)
        return None

    def is_within_bounds(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def is_position_free(self, x, y):
        for positions in self.initial_state['obstacles'].values():
            if (x, y) in positions:
                return False
        return True

    def filter_path(self, path, goal):
        filtered_path = []
        last_position = None

        # Check how many positions 'A' occupies
        a_positions = set(self.initial_state['A'])

        for x, y in path:
            if last_position:
                dx = x - last_position[0]
                dy = y - last_position[1]

                if dx == 1:
                    direction = "RIGHT"
                elif dx == -1:
                    direction = "LEFT"
                elif dy == 1:
                    direction = "DOWN"
                elif dy == -1:
                    direction = "UP"
                else:
                    direction = None

                if direction and last_position not in a_positions:
                    filtered_path.append((direction, last_position))

            last_position = (x, y)

        # Add the goal position as the final step
        filtered_path.append((direction, goal))  # Use None as placeholder for direction

        return filtered_path