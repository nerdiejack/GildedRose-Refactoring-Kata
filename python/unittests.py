from item_creator import ItemCreator
from gilded_rose import GildedRose
from unittest import TestCase

item_creator = ItemCreator()


class UnitTests(TestCase):
    def setUp(self) -> None:
        self.items = []

    def test_normal_decrease(self):
        # Regular items degrade by one (quality + sell_in)
        self.items.append(item_creator.create("5 Dexterity Vest", 10, 20))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 9, 'quality': 19},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_conjured_decrease(self):
        # "Conjured" items degrade in Quality twice as fast as normal items
        self.items.append(item_creator.create("Conjured Health Potion", 10, 10))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 9, 'quality': 8},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_increase_brie(self):
        # "Aged Brie" actually increases in Quality the older it gets
        self.items.append(item_creator.create("Aged Brie", 20, 30))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 19, 'quality': 31},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_increase_pass_by_three(self):
        # Quality increases by 3 when there are 5 days or less
        self.items.append(item_creator.create("Backstage passes to a TAFKAL80ETC concert", 5, 15))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 4, 'quality': 18},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_increase_pass_by_two(self):
        # Quality increases by 2 when there are 10 days or less
        self.items.append(item_creator.create("Backstage passes to a TAFKAL80ETC concert", 8, 30))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 7, 'quality': 32},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_increase_pass_overdue(self):
        # Quality drops to 0 after the concert
        self.items.append(item_creator.create("Backstage passes to a TAFKAL80ETC concert", 0, 35))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': -1, 'quality': 0},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_decrease_double_overdue(self):
        # Once the sell by date has passed, Quality degrades twice as fast
        self.items.append(item_creator.create("+5 Dexterity Vest", 0, 20))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': -1, 'quality': 18},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_max_quality(self):
        # The Quality of an item is never more than 50
        self.items.append(item_creator.create("Aged Brie", 10, 50))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': 9, 'quality': 50},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])

    def test_immutable_sulfuras(self):
        # "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
        self.items.append(item_creator.create("Sulfuras, Hand of Ragnaros", -1, 80))
        self.test_shop = GildedRose(self.items)
        self.test_shop.update_quality()
        results = [
            {'sell_in': -1, 'quality': 80},
        ]
        for num, result in enumerate(results):
            item = self.items[num]
            self.assertEqual(item.quality, result['quality'])
            self.assertEqual(item.sell_in, result['sell_in'])


if __name__ == "__main__":
    UnitTests()
