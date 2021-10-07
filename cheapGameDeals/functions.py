from cheapGameDeals.models import GameDeals

def allGameDealsToDisplay():
    gameDeals = GameDeals.query.all()

    returningGameDeals = []
    for deal in gameDeals:
        if (deal.PS_deal_price is None) and (deal.Xbox_deal_price is None) and (deal.Switch_deal_price is None):
            pass
        else:
            returningGameDeals.append(deal)

    sortedGameDeals = sorted(returningGameDeals, key=mostMoneySaved,
                                              reverse=True)

    return sortedGameDeals

def alphabetically(element):
    return element.title.lower()

def highestSavingPercentage(element):
    savingsPercentage = []

    try:
        PS_SavingPercentage = element.PS_deal_price / element.PS_normal_price
        savingsPercentage.append(PS_SavingPercentage)
    except:
        pass
    try:
        Xbox_SavingPercentage = element.Xbox_deal_price / element.Xbox_normal_price
        savingsPercentage.append(Xbox_SavingPercentage)
    except:
        pass
    try:
        Switch_SavingPercentage = element.Switch_deal_price / element.Switch_normal_price
        savingsPercentage.append(Switch_SavingPercentage)
    except:
        pass

    return min(savingsPercentage)


def homePageTopSix():
    gameDeals = GameDeals.query.all()

    returningGameDeals = []
    for deal in gameDeals:
        if (deal.PS_deal_price is None) and (deal.Xbox_deal_price is None) and (deal.Switch_deal_price is None):
            pass
        else:
            returningGameDeals.append(deal)

    homePageGames = sorted(returningGameDeals, key=mostMoneySaved,
                                                          reverse=True)[0:6]
    return homePageGames

def mostMoneySaved(element):

    savings = []

    try:
        PS_Savings = element.PS_normal_price - element.PS_deal_price
        savings.append(PS_Savings)
    except:
        pass
    try:
        Xbox_Saving = element.Xbox_normal_price - element.Xbox_deal_price
        savings.append(Xbox_Saving)
    except:
        pass
    try:
        Switch_Saving = element.Switch_normal_price - element.Switch_deal_price
        savings.append(Switch_Saving)
    except:
        pass

    return max(savings)
