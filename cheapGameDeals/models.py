from cheapGameDeals import gameDB

class GameDeals(gameDB.Model):
    __tablename__ = 'deals'

    id = gameDB.Column(gameDB.Integer, primary_key = True)
    title = gameDB.Column(gameDB.String(128))

    PS_normal_price = gameDB.Column(gameDB.Float)
    PS_deal_price = gameDB.Column(gameDB.Float)
    PS_link = gameDB.Column(gameDB.String(128))

    Xbox_normal_price = gameDB.Column(gameDB.Float)
    Xbox_deal_price = gameDB.Column(gameDB.Float)
    Xbox_link = gameDB.Column(gameDB.String(128))

    Switch_normal_price = gameDB.Column(gameDB.Float)
    Switch_deal_price = gameDB.Column(gameDB.Float)
    Switch_link = gameDB.Column(gameDB.String(128))

    metacriticURL = gameDB.Column(gameDB.String(128))
    imageURL = gameDB.Column(gameDB.String(128))