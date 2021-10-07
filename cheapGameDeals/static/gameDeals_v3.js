function filterByConsole(){
  var PS_Check, Xbox_Check, Switch_Deal, game_deal_cards;
  PS_Check = document.getElementById("Playstation_Check")
  Xbox_Check = document.getElementById("Xbox_Check")
  Switch_Deal = document.getElementById("Switch_Check")

  game_deal_cards = document.getElementsByClassName("GameDeals")


  var game_deal_card
  var x
  //console.log(game_deal_cards)
  //console.log(game_deal_cards[0])

  for (x in game_deal_cards) {
    game_deal_card = game_deal_cards[x]
    //console.log(game_deal_card)
    //console.log(game_deal_card.getElementsByClassName("Playstation_Deal"))


    var PS_Deal_Exists = game_deal_card.getElementsByClassName("Playstation_Deal")
    //console.log(PS_Deal_Exists)

    var Xbox_Deal_Exists = game_deal_card.getElementsByClassName("Xbox_Deal")
    var Switch_Deal_Exists = game_deal_card.getElementsByClassName("Switch_Deal")


   //Just Playstation
    if (PS_Check.checked == true){
        if (PS_Deal_Exists.length == 0){
            game_deal_card.style.display = 'none'
        }
        else {
            game_deal_card.style.display = 'flex'
        }
    }



    //Just Xbox
    if (Xbox_Check.checked == true){
        if (Xbox_Deal_Exists.length == 0){
            game_deal_card.style.display = 'none'
        } else {
            game_deal_card.style.display = 'flex'
        }
    }


    if (Switch_Deal.checked == true){
        if (Switch_Deal_Exists.length == 0){
            game_deal_card.style.display = 'none'
        } else {
            game_deal_card.style.display = 'flex'
        }
    }

    //PS & Xbox
    if (PS_Check.checked == true && Xbox_Check.checked == true){
        if (PS_Deal_Exists.length == 0 && Xbox_Deal_Exists.length == 0){
            game_deal_card.style.display = 'none'
        }
        else {
            game_deal_card.style.display = 'flex'
        }
    }

    //PS & Switch
    if (PS_Check.checked == true && Switch_Deal.checked == true){
        if (PS_Deal_Exists.length == 0 && Switch_Deal_Exists.length == 0){
            game_deal_card.style.display = 'none'
        }
        else {
            game_deal_card.style.display = 'flex'
        }
    }

    //Xbox & Switch
    if (Switch_Deal.checked == true && Xbox_Check.checked == true){
        if (Switch_Deal_Exists.length == 0 && Xbox_Deal_Exists.length == 0){
            game_deal_card.style.display = 'none'
        }
        else {
            game_deal_card.style.display = 'flex'
        }
    }

    //All Checked
    if (PS_Check.checked == true && Switch_Deal.checked == true && Xbox_Check.checked == true){

        game_deal_card.style.display = 'flex'

    }

    //All Unchecked
    if (PS_Check.checked == false && Switch_Deal.checked == false && Xbox_Check.checked == false){

        game_deal_card.style.display = 'flex'

    }

  }

}

function filterTitleFunction() {

    var game_deal_cards;
    game_deal_cards = document.getElementsByClassName("GameDeals")

    var input, filter
    input = document.getElementById("titleSearch");
    filter = input.value.toUpperCase();

    var game_deal_card
    var x

    if (input.value.length > 0) {
        for (x in game_deal_cards) {

            game_deal_card = game_deal_cards[x]
            txtValue = game_deal_card.textContent || game_deal_card.innerText;

            if (txtValue.toUpperCase().indexOf(filter) > -1 && (input.value.length > 0)) {

                game_deal_card.style.display = "flex";

            } else {

                game_deal_card.style.display = "none";

            }

        }
    } else {
        for (x in game_deal_cards) {
            game_deal_card = game_deal_cards[x]
            game_deal_card.style.display = "flex";
        }
    }

}

function showAllDeals() {

    var topDeals, allDeals, button
    topDeals = document.getElementById("topDeals");
    button = document.getElementById("revealButton");
    allDeals = document.getElementById("homeGameDeals");

    topDeals.style.display = "none";
    button.style.display = "none"
    allDeals.style.display = "flex";

}

