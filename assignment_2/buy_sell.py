class Solution:
    def get_max_profit(self, prices: list[int]) -> int:
        """
        The method returns best difference between sell and buy
        prices from a given list of prices
        :type prices: List[int] a list of prices
        :rtype: int best difference between sell and buy prices
        """
        max_difference = 0
        buy_index = 0
        sell_index = 1
        while buy_index < len(prices) and sell_index < len(prices):
            if prices[sell_index] > prices[buy_index]:
                max_difference = max(max_difference,
                                     prices[sell_index] - prices[buy_index]
                                     )
            else:
                buy_index = sell_index
            sell_index += 1
        return max_difference


if __name__ == '__main__':
    assistant = Solution()
    assert assistant.get_max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert assistant.get_max_profit([7, 6, 4, 3, 1]) == 0
    assert assistant.get_max_profit([1, 2, 4, 2, 5, 7, 2, 4, 9, 0, 9]) == 9
