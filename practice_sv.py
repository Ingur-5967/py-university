class TreeNode:  # 1 task
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_max(root):
    if not root:
        return float('-inf')
    left_max = find_max(root.left)
    right_max = find_max(root.right)
    return max(root.val, left_max, right_max)


root = TreeNode(1,
                TreeNode(3, TreeNode(8, TreeNode(14), TreeNode(15)), TreeNode(10, right=TreeNode(3))),
                TreeNode(5, TreeNode(2), TreeNode(6, TreeNode(0), TreeNode(1)))
                )

print(find_max(root))


class Order:
    def __init__(self, day: int, cost: int):
        self.cost = cost
        self.day = day

    def get_day(self):
        return self.day

    def get_cost(self):
        return self.cost

    def calc_coupons(self):
        return self.cost // 500


def init_purchases(days): # task 2
    orders = []
    for day in range(days):
        orders.append(Order(day, int(input(f"Введите сумму покупки на {day} день: "))))

    cost = 0
    answer = dict()
    for index, order in enumerate(orders):
        coupons = order.calc_coupons()
        if coupons > 0 and len(orders[index + 1:]) > 0:
            while coupons > 0:
                cost += order.get_cost()
                maximum_cost_at_after_days = max(list(map(lambda order: order.get_cost(), orders[index + 1:])))
                answer[(len(orders) - 1) - order.day] = maximum_cost_at_after_days
                cost -= maximum_cost_at_after_days
                coupons -= 1
        else:
            cost += order.get_cost()

    return cost, answer


print(init_purchases(int(input("Введите количество дней: "))))

def sort_nums(array):  # 3
    left, right = [], []

    for num in array:
        if num >= 0:
            right.append(num)
        else:
            left.append(num)

    return left + right


print(sort_nums(list(map(int, input("Введите числа через пробел ").split()))))


def find_squares(n): # task 4
    used = [False] * 10
    used[n] = True
    square = [0] * 9
    square[0] = n
    result = []

    def backtrack(pos):
        if pos == 9:
            rows = [square[i:i+3] for i in [0, 3, 6]]
            cols = [[square[i], square[i+3], square[i+6]] for i in [0, 1, 2]]
            if sum(list(map(lambda point: point[0], rows))) != 15: return
            if sum(list(map(lambda point: point[0], cols))) != 15: return
            if square[0] + square[4] + square[8] != 15: return
            if square[2] + square[4] + square[6] != 15: return
            result.append(square.copy())
            return

        for num in range(1, 10):
            if not used[num]:
                used[num] = True
                square[pos] = num
                valid = True

                if pos in [2, 5, 8]:
                    row_start = (pos // 3) * 3
                    if sum(square[row_start:row_start + 3]) != 15:
                        valid = False

                if pos >= 6:
                    col = pos - 6
                    if sum([square[col], square[col + 3], square[col + 6]]) != 15: valid = False

                if pos == 8 and (square[0] + square[4] + square[8]) != 15: valid = False
                if pos == 6 and (square[2] + square[4] + square[6]) != 15: valid = False

                if valid: backtrack(pos + 1)
                square[pos] = 0
                used[num] = False

    backtrack(1)
    return result

n = int(input())
squares = find_squares(n)
if not squares:
    print(-1)
else:
    for row in [squares[0][:3], squares[0][3:6], squares[0][6:9]]:
        print(' '.join(map(str, row)))