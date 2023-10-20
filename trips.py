class Trip:
    def __init__(self, price_tag, origin_t, destiny_t):
        self.price_tag = price_tag.split("€")[0] + " Euros"
        self.origin = origin_t
        self.destiny = destiny_t
        self.price = float(price_tag.replace(',', '.').split('€')[0])


class AllTrips:
    def __init__(self, list):
        self.list = list

    def get_chepper(self, list=None):
        if list is None:
            list = self.list
        minimum = 20
        for i in list:
            if i.price < minimum:
                minimum = i.price
        cheeper = []
        for item in list:
            if item.price == minimum:
                cheeper.append(item)
        return cheeper

    def get_itens_dt(self, start, end):
        list = []
        for item in self.list:
            if item.origin > start and item.destiny < end:
                list.append(item)
        return list

    def get_chepper_dt(self, start, end):
        list = self.get_itens_dt(start, end)
        return self.get_chepper(list)


if __name__ == '__main__':
    d = Trip("14.50€", "caldas da rainha", "porto")
    print(d.price, d.price_tag)
