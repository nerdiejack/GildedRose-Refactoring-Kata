from gilded_rose import *
from unittest import TestCase


class UnitTests(TestCase):

    def setUp(self) -> None:
        self.items = []

    def test_decrease(self):
        # Regular items degrade by one
        # "Conjured" items degrade in Quality twice as fast as normal items
        self.items.append(Item("5 Dexterity Vest", 10, 20))
        self.items.append(Item("Conjured Health Potion", 10, 10))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 9, 'quality': 19},
            {'sell_in': 9, 'quality': 8},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_increase_special(self):
        self.items.append(Item("Aged Brie", 20, 30))
        self.items.append(Item("Backstage passes to a TAFKAL80ETC concert", 20, 30))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 19, 'quality': 31},
            {'sell_in': 19, 'quality': 31},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_increase_by_three_special(self):
        # Quality increases by 3 when there are 5 days or less
        self.items.append(Item("Aged Brie", 4, 11))
        self.items.append(Item("Backstage passes to a TAFKAL80ETC concert", 5, 15))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 3, 'quality': 14},
            {'sell_in': 4, 'quality': 18},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_increase_by_two_special(self):
        # Quality increases by 2 when there are 10 days or less
        self.items.append(Item("Aged Brie", 10, 34))
        self.items.append(Item("Backstage passes to a TAFKAL80ETC concert", 8, 30))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 9, 'quality': 36},
            {'sell_in': 7, 'quality': 32},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_decrease_double_overdue(self):
        # Once the sell by date has passed, Quality degrades twice as fast
        # "Conjured" items degrade in Quality twice as fast as normal items
        self.items.append(Item("+5 Dexterity Vest", 0, 20))
        self.items.append(Item("Conjured Health Potion", 0, 10))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': -1, 'quality': 18},
            {'sell_in': -1, 'quality': 7},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_pass_plus_brie_zero(self):
        # "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches
        # Quality drops to 0 after the concert
        self.items.append(Item("Aged Brie", 0, 20))
        self.items.append(Item("Backstage passes to a TAFKAL80ETC concert", 0, 20))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': -1, 'quality': 0},
            {'sell_in': -1, 'quality': 0},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_immutable_sulfuras(self):
        # "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
        self.items.append(Item("Sulfuras, Hand of Ragnaros", -1, 80))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': -1, 'quality': 80},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_no_increase_above_50(self):
        self.items.append(Item("Aged Brie", 10, 100))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 9, 'quality': 50},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])


if __name__ == "__main__":
    UnitTests()
