from flask import render_template, url_for, request, current_app, make_response
from cheapGameDeals import application
from cheapGameDeals.functions import allGameDealsToDisplay, homePageTopSix
from datetime import datetime, timedelta



@application.route("/gamedeals", methods=['GET'])
def deals():

    gameDealsToDisplay = allGameDealsToDisplay()

    return render_template('deals.html', gameDeals=gameDealsToDisplay)

@application.route("/about")
def about():

    return render_template('about.html')

@application.route("/home", methods=['GET'])
@application.route("/", methods=['GET'])
def home():
    gameDealsToDisplay = allGameDealsToDisplay()

    topSixGames = homePageTopSix()

    return render_template('home.html', homePageDeals=topSixGames, gameDeals=gameDealsToDisplay)

@application.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []
    ten_days_ago = datetime.now() - timedelta(days=10)

    for rule in current_app.url_map.iter_rules():
        if 'GET' in rule.methods and len(rule.arguments) == 0 and not rule.rule.startswith('/admin'):
            pages.append([url_for('home', _external=True) + rule.rule, ten_days_ago])


    sitemap_template = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_template)
    response.headers["Content-Type"] = "application/xml"

    return response
