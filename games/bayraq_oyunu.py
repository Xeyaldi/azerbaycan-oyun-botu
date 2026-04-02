import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

BAYRAQLАР = [
    {"olke":"Azərbaycan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Flag_of_Azerbaijan.svg/1280px-Flag_of_Azerbaijan.svg.png", "ipucu":"A","herf":10},
    {"olke":"Türkiyə", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Turkey.svg/1280px-Flag_of_Turkey.svg.png", "ipucu":"T","herf":8},
    {"olke":"Rusiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Russia.svg/1280px-Flag_of_Russia.svg.png", "ipucu":"R","herf":6},
    {"olke":"Almaniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Flag_of_Germany.svg/1280px-Flag_of_Germany.svg.png", "ipucu":"A","herf":8},
    {"olke":"Fransa", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Flag_of_France.svg/1280px-Flag_of_France.svg.png", "ipucu":"F","herf":6},
    {"olke":"İtaliya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Flag_of_Italy.svg/1280px-Flag_of_Italy.svg.png", "ipucu":"İ","herf":7},
    {"olke":"İspaniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Spain.svg/1280px-Flag_of_Spain.svg.png", "ipucu":"İ","herf":8},
    {"olke":"Britaniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Flag_of_the_United_Kingdom.svg/1280px-Flag_of_the_United_Kingdom.svg.png","ipucu":"B","herf":9},
    {"olke":"ABŞ", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/1280px-Flag_of_the_United_States.svg.png","ipucu":"A","herf":3},
    {"olke":"Yaponiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Flag_of_Japan.svg/1280px-Flag_of_Japan.svg.png", "ipucu":"Y","herf":8},
    {"olke":"Çin", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/1280px-Flag_of_the_People%27s_Republic_of_China.svg.png","ipucu":"Ç","herf":3},
    {"olke":"Braziliya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1280px-Flag_of_Brazil.svg.png", "ipucu":"B","herf":9},
    {"olke":"Hindistan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/1280px-Flag_of_India.svg.png", "ipucu":"H","herf":8},
    {"olke":"Kanada", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Canada_%28Pantone%29.svg/1280px-Flag_of_Canada_%28Pantone%29.svg.png","ipucu":"K","herf":6},
    {"olke":"Avstraliya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Flag_of_Australia_%28converted%29.svg/1280px-Flag_of_Australia_%28converted%29.svg.png","ipucu":"A","herf":9},
    {"olke":"Gürcüstan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Flag_of_Georgia.svg/1280px-Flag_of_Georgia.svg.png", "ipucu":"G","herf":8},
    {"olke":"Ukrayna", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Ukraine.svg/1280px-Flag_of_Ukraine.svg.png", "ipucu":"U","herf":7},
    {"olke":"Qazaxıstan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Flag_of_Kazakhstan.svg/1280px-Flag_of_Kazakhstan.svg.png", "ipucu":"Q","herf":10},
    {"olke":"İsveç", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Flag_of_Sweden.svg/1280px-Flag_of_Sweden.svg.png", "ipucu":"İ","herf":5},
    {"olke":"Norveç", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Norway.svg/1280px-Flag_of_Norway.svg.png", "ipucu":"N","herf":6},
    {"olke":"Polşa", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Flag_of_Poland.svg/1280px-Flag_of_Poland.svg.png", "ipucu":"P","herf":5},
    {"olke":"Niderland", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/1280px-Flag_of_the_Netherlands.svg.png","ipucu":"N","herf":9},
    {"olke":"Portuqaliya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Portugal.svg/1280px-Flag_of_Portugal.svg.png", "ipucu":"P","herf":11},
    {"olke":"Meksika", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Flag_of_Mexico.svg/1280px-Flag_of_Mexico.svg.png", "ipucu":"M","herf":7},
    {"olke":"Argentina", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Argentina.svg/1280px-Flag_of_Argentina.svg.png", "ipucu":"A","herf":9},
    {"olke":"Misir", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Flag_of_Egypt.svg/1280px-Flag_of_Egypt.svg.png", "ipucu":"M","herf":5},
    {"olke":"Özbəkistan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Flag_of_Uzbekistan.svg/1280px-Flag_of_Uzbekistan.svg.png", "ipucu":"Ö","herf":10},
    {"olke":"Türkmənistan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Flag_of_Turkmenistan.svg/1280px-Flag_of_Turkmenistan.svg.png", "ipucu":"T","herf":12},
    {"olke":"Tacikistan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Flag_of_Tajikistan.svg/1280px-Flag_of_Tajikistan.svg.png", "ipucu":"T","herf":10},
    {"olke":"Qırğızıstan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Flag_of_Kyrgyzstan.svg/1280px-Flag_of_Kyrgyzstan.svg.png", "ipucu":"Q","herf":10},
    {"olke":"Macarıstan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Flag_of_Hungary.svg/1280px-Flag_of_Hungary.svg.png", "ipucu":"M","herf":9},
    {"olke":"Finlandiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Flag_of_Finland.svg/1280px-Flag_of_Finland.svg.png", "ipucu":"F","herf":9},
    {"olke":"Danimarka", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Flag_of_Denmark.svg/1280px-Flag_of_Denmark.svg.png", "ipucu":"D","herf":8},
    {"olke":"İslandiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Flag_of_Iceland.svg/1280px-Flag_of_Iceland.svg.png", "ipucu":"İ","herf":8},
    {"olke":"Bolqarıstan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Bulgaria.svg/1280px-Flag_of_Bulgaria.svg.png", "ipucu":"B","herf":10},
    {"olke":"Rumıniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flag_of_Romania.svg/1280px-Flag_of_Romania.svg.png", "ipucu":"R","herf":8},
    {"olke":"Xorvatiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Flag_of_Croatia.svg/1280px-Flag_of_Croatia.svg.png", "ipucu":"X","herf":9},
    {"olke":"Sloveniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Flag_of_Slovenia.svg/1280px-Flag_of_Slovenia.svg.png", "ipucu":"S","herf":9},
    {"olke":"Slovakiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Flag_of_Slovakia.svg/1280px-Flag_of_Slovakia.svg.png", "ipucu":"S","herf":9},
    {"olke":"Çexiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/1280px-Flag_of_the_Czech_Republic.svg.png", "ipucu":"Ç","herf":6},
    {"olke":"Estoniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flag_of_Estonia.svg/1280px-Flag_of_Estonia.svg.png", "ipucu":"E","herf":8},
    {"olke":"Latviya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Flag_of_Latvia.svg/1280px-Flag_of_Latvia.svg.png", "ipucu":"L","herf":7},
    {"olke":"Litva", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Flag_of_Lithuania.svg/1280px-Flag_of_Lithuania.svg.png", "ipucu":"L","herf":5},
    {"olke":"Moldova", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Flag_of_Moldova.svg/1280px-Flag_of_Moldova.svg.png", "ipucu":"M","herf":7},
    {"olke":"Albaniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Flag_of_Albania.svg/1280px-Flag_of_Albania.svg.png", "ipucu":"A","herf":8},
    {"olke":"Serbiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Flag_of_Serbia.svg/1280px-Flag_of_Serbia.svg.png", "ipucu":"S","herf":7},
    {"olke":"Bosniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Flag_of_Bosnia_and_Herzegovina.svg/1280px-Flag_of_Bosnia_and_Herzegovina.svg.png", "ipucu":"B","herf":7},
    {"olke":"Malta", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flag_of_Malta.svg/1280px-Flag_of_Malta.svg.png", "ipucu":"M","herf":5},
    {"olke":"Kipr", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Flag_of_Cyprus.svg/1280px-Flag_of_Cyprus.svg.png", "ipucu":"K","herf":4},
    {"olke":"İndoneziya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Flag_of_Indonesia.svg/1280px-Flag_of_Indonesia.svg.png", "ipucu":"İ","herf":9},
    {"olke":"Malayziya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Flag_of_Malaysia.svg/1280px-Flag_of_Malaysia.svg.png", "ipucu":"M","herf":9},
    {"olke":"Filippin", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Flag_of_the_Philippines.svg/1280px-Flag_of_the_Philippines.svg.png", "ipucu":"F","herf":8},
    {"olke":"Sinqapur", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Flag_of_Singapore.svg/1280px-Flag_of_Singapore.svg.png", "ipucu":"S","herf":8},
    {"olke":"Monqolustan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Flag_of_Mongolia.svg/1280px-Flag_of_Mongolia.svg.png", "ipucu":"M","herf":10},
    {"olke":"İraq", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Flag_of_Iraq.svg/1280px-Flag_of_Iraq.svg.png", "ipucu":"İ","herf":4},
    {"olke":"Suriya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Flag_of_Syria.svg/1280px-Flag_of_Syria.svg.png", "ipucu":"S","herf":5},
    {"olke":"Livan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Flag_of_Lebanon.svg/1280px-Flag_of_Lebanon.svg.png", "ipucu":"L","herf":5},
    {"olke":"İordaniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Flag_of_Jordan.svg/1280px-Flag_of_Jordan.svg.png", "ipucu":"İ","herf":8},
    {"olke":"Küveyt", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Flag_of_Kuwait.svg/1280px-Flag_of_Kuwait.svg.png", "ipucu":"K","herf":6},
    {"olke":"Qətər", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Flag_of_Qatar.svg/1280px-Flag_of_Qatar.svg.png", "ipucu":"Q","herf":5},
    {"olke":"Bəhreyn", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Flag_of_Bahrain.svg/1280px-Flag_of_Bahrain.svg.png", "ipucu":"B","herf":7},
    {"olke":"Oman", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Flag_of_Oman.svg/1280px-Flag_of_Oman.svg.png", "ipucu":"O","herf":4},
    {"olke":"Yəmən", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Flag_of_Yemen.svg/1280px-Flag_of_Yemen.svg.png", "ipucu":"Y","herf":5},
    {"olke":"İsrail", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Flag_of_Israel.svg/1280px-Flag_of_Israel.svg.png", "ipucu":"İ","herf":6},
    {"olke":"Fələstin", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Flag_of_Palestine.svg/1280px-Flag_of_Palestine.svg.png", "ipucu":"F","herf":8},
    {"olke":"Əfqanıstan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_the_Taliban.svg/1280px-Flag_of_the_Taliban.svg.png", "ipucu":"Ə","herf":9},
    {"olke":"Mərakeş", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Flag_of_Morocco.svg/1280px-Flag_of_Morocco.svg.png", "ipucu":"M","herf":7},
    {"olke":"Əlcəzair", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Flag_of_Algeria.svg/1280px-Flag_of_Algeria.svg.png", "ipucu":"Ə","herf":8},
    {"olke":"Tunis", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Flag_of_Tunisia.svg/1280px-Flag_of_Tunisia.svg.png", "ipucu":"T","herf":5},
    {"olke":"Liviya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Libya.svg/1280px-Flag_of_Libya.svg.png", "ipucu":"L","herf":5},
    {"olke":"Sudan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Flag_of_Sudan.svg/1280px-Flag_of_Sudan.svg.png", "ipucu":"S","herf":5},
    {"olke":"Efiopiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Flag_of_Ethiopia.svg/1280px-Flag_of_Ethiopia.svg.png", "ipucu":"E","herf":8},
    {"olke":"Somali", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Flag_of_Somalia.svg/1280px-Flag_of_Somalia.svg.png", "ipucu":"S","herf":6},
    {"olke":"Keniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/1280px-Flag_of_Kenya.svg.png", "ipucu":"K","herf":5},
    {"olke":"Uqanda", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Flag_of_Uganda.svg/1280px-Flag_of_Uganda.svg.png", "ipucu":"U","herf":6},
    {"olke":"Tanzaniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Flag_of_Tanzania.svg/1280px-Flag_of_Tanzania.svg.png", "ipucu":"T","herf":8},
    {"olke":"Nigeriya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Flag_of_Nigeria.svg/1280px-Flag_of_Nigeria.svg.png", "ipucu":"N","herf":7},
    {"olke":"Qana", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Flag_of_Ghana.svg/1280px-Flag_of_Ghana.svg.png", "ipucu":"Q","herf":4},
    {"olke":"Kamerun", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Flag_of_Cameroon.svg/1280px-Flag_of_Cameroon.svg.png", "ipucu":"K","herf":7},
    {"olke":"Anqola", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Flag_of_Angola.svg/1280px-Flag_of_Angola.svg.png", "ipucu":"A","herf":6},
    {"olke":"Zimbabve", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Flag_of_Zimbabwe.svg/1280px-Flag_of_Zimbabwe.svg.png", "ipucu":"Z","herf":8},
    {"olke":"Botsvana", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_Botswana.svg/1280px-Flag_of_Botswana.svg.png", "ipucu":"B","herf":8},
    {"olke":"Namibiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Flag_of_Namibia.svg/1280px-Flag_of_Namibia.svg.png", "ipucu":"N","herf":8},
    {"olke":"Seneqal", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Flag_of_Senegal.svg/1280px-Flag_of_Senegal.svg.png", "ipucu":"S","herf":7},
    {"olke":"Mali", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Flag_of_Mali.svg/1280px-Flag_of_Mali.svg.png", "ipucu":"M","herf":4},
    {"olke":"Madaqaskar", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Flag_of_Madagascar.svg/1280px-Flag_of_Madagascar.svg.png", "ipucu":"M","herf":10},
    {"olke":"Kolumbiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/1280px-Flag_of_Colombia.svg.png", "ipucu":"K","herf":9},
    {"olke":"Venesuela", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Flag_of_Venezuela.svg/1280px-Flag_of_Venezuela.svg.png", "ipucu":"V","herf":9},
    {"olke":"Ekvador", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Flag_of_Ecuador.svg/1280px-Flag_of_Ecuador.svg.png", "ipucu":"E","herf":7},
    {"olke":"Peru", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Flag_of_Peru.svg/1280px-Flag_of_Peru.svg.png", "ipucu":"P","herf":4},
    {"olke":"Boliviya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Flag_of_Bolivia.svg/1280px-Flag_of_Bolivia.svg.png", "ipucu":"B","herf":8},
    {"olke":"Çili", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/85/Flag_of_Chile.svg/1280px-Flag_of_Chile.svg.png", "ipucu":"Ç","herf":4},
    {"olke":"Paraqvay", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Flag_of_Paraguay.svg/1280px-Flag_of_Paraguay.svg.png", "ipucu":"P","herf":8},
    {"olke":"Uruqvay", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Flag_of_Uruguay.svg/1280px-Flag_of_Uruguay.svg.png", "ipucu":"U","herf":7},
    {"olke":"Kuba", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Flag_of_Cuba.svg/1280px-Flag_of_Cuba.svg.png", "ipucu":"K","herf":4},
    {"olke":"Yamayka", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Flag_of_Jamaica.svg/1280px-Flag_of_Jamaica.svg.png", "ipucu":"Y","herf":7},
    {"olke":"Haiti", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Flag_of_Haiti.svg/1280px-Flag_of_Haiti.svg.png", "ipucu":"H","herf":5},
    {"olke":"Panama", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Flag_of_Panama.svg/1280px-Flag_of_Panama.svg.png", "ipucu":"P","herf":6},
    {"olke":"Kosta-Rika", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Flag_of_Costa_Rica.svg/1280px-Flag_of_Costa_Rica.svg.png", "ipucu":"K","herf":10},
    {"olke":"Qvatemala", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Flag_of_Guatemala.svg/1280px-Flag_of_Guatemala.svg.png", "ipucu":"Q","herf":9},
    {"olke":"Honduras", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Flag_of_Honduras.svg/1280px-Flag_of_Honduras.svg.png", "ipucu":"H","herf":8},
    {"olke":"Nikaraqua", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Flag_of_Nicaragua.svg/1280px-Flag_of_Nicaragua.svg.png", "ipucu":"N","herf":9},
    {"olke":"Yeni Zelandiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Flag_of_New_Zealand.svg/1280px-Flag_of_New_Zealand.svg.png", "ipucu":"Y","herf":14},
    {"olke":"Fici", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Flag_of_Fiji.svg/1280px-Flag_of_Fiji.svg.png", "ipucu":"F","herf":4},
    {"olke":"Papua-Yeni Qvineya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Flag_of_Papua_New_Guinea.svg/1280px-Flag_of_Papua_New_Guinea.svg.png", "ipucu":"P","herf":17},
    {"olke":"Ermənistan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Flag_of_Armenia.svg/1280px-Flag_of_Armenia.svg.png", "ipucu":"E","herf":9},
    {"olke":"Lüksemburq", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Flag_of_Luxembourg.svg/1280px-Flag_of_Luxembourg.svg.png", "ipucu":"L","herf":10},
    {"olke":"Monako", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Flag_of_Monaco.svg/1280px-Flag_of_Monaco.svg.png", "ipucu":"M","herf":6},
    {"olke":"Andorra", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Flag_of_Andorra.svg/1280px-Flag_of_Andorra.svg.png", "ipucu":"A","herf":7},
    {"olke":"San-Marino", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Flag_of_San_Marino.svg/1280px-San_Marino.svg.png", "ipucu":"S","herf":10},
    {"olke":"Lixtenşteyn", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Flag_of_Liechtenstein.svg/1280px-Flag_of_Liechtenstein.svg.png", "ipucu":"L","herf":11},
    {"olke":"Vatikan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Flag_of_the_Vatican_City.svg/1280px-Flag_of_the_Vatican_City.svg.png", "ipucu":"V","herf":7},
    {"olke":"Nepal", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Flag_of_Nepal.svg/800px-Flag_of_Nepal.svg.png", "ipucu":"N","herf":5},
    {"olke":"Butan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Flag_of_Bhutan.svg/1280px-Flag_of_Bhutan.svg.png", "ipucu":"B","herf":5},
    {"olke":"Şri-Lanka", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Flag_of_Sri_Lanka.svg/1280px-Flag_of_Sri_Lanka.svg.png", "ipucu":"Ş","herf":9},
    {"olke":"Maldiv", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Flag_of_Maldives.svg/1280px-Flag_of_Maldives.svg.png", "ipucu":"M","herf":6},
    {"olke":"Kamboca", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Flag_of_Cambodia.svg/1280px-Flag_of_Cambodia.svg.png", "ipucu":"K","herf":7},
    {"olke":"Laos", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Flag_of_Laos.svg/1280px-Flag_of_Laos.svg.png", "ipucu":"L","herf":4},
    {"olke":"Myanmar", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Flag_of_Myanmar.svg/1280px-Flag_of_Myanmar.svg.png", "ipucu":"M","herf":7},
    {"olke":"Bruney", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Flag_of_Brunei.svg/1280px-Flag_of_Brunei.svg.png", "ipucu":"B","herf":6},
    {"olke":"Tayvan", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Flag_of_the_Republic_of_China.svg/1280px-Flag_of_the_Republic_of_China.svg.png", "ipucu":"T","herf":6},
    {"olke":"Surinam", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Flag_of_Suriname.svg/1280px-Flag_of_Suriname.svg.png", "ipucu":"S","herf":7},
    {"olke":"Qayana", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Flag_of_Guyana.svg/1280px-Flag_of_Guyana.svg.png", "ipucu":"Q","herf":6},
    {"olke":"Baham", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Flag_of_the_Bahamas.svg/1280px-Flag_of_the_Bahamas.svg.png", "ipucu":"B","herf":5},
    {"olke":"Salvador", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Flag_of_El_Salvador.svg/1280px-Flag_of_El_Salvador.svg.png", "ipucu":"S","herf":8},
    {"olke":"Qabon", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Flag_of_Gabon.svg/1280px-Flag_of_Gabon.svg.png", "ipucu":"Q","herf":5},
    {"olke":"Eritreya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Flag_of_Eritrea.svg/1280px-Flag_of_Eritrea.svg.png", "ipucu":"E","herf":8},
    {"olke":"Cibuti", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Flag_of_Djibouti.svg/1280px-Flag_of_Djibouti.svg.png", "ipucu":"C","herf":6},
    {"olke":"Ruanda", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Flag_of_Rwanda.svg/1280px-Flag_of_Rwanda.svg.png", "ipucu":"R","herf":6},
    {"olke":"Burundi", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Flag_of_Burundi.svg/1280px-Flag_of_Burundi.svg.png", "ipucu":"B","herf":7},
    {"olke":"Zambiya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Flag_of_Zambia.svg/1280px-Flag_of_Zambia.svg.png", "ipucu":"Z","herf":7},
    {"olke":"Malavi", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Flag_of_Malawi.svg/1280px-Flag_of_Malawi.svg.png", "ipucu":"M","herf":6},
    {"olke":"Mavritaniya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Flag_of_Mauritania.svg/1280px-Flag_of_Mauritania.svg.png", "ipucu":"M","herf":11},
    {"olke":"Qvineya", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Flag_of_Guinea.svg/1280px-Flag_of_Guinea.svg.png", "ipucu":"Q","herf":7},
    {"olke":"Madaqaskar", "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Flag_of_Madagascar.svg/1280px-Flag_of_Madagascar.svg.png", "ipucu":"M","herf":10}
]
# ── Oyun Parametrləri ────────────────────────────────────────────────────────
TURLAR        = 45   
PAS_HAKKI     = 10   # Tur sayı çox olduğu üçün pası da artırdım
XAL_IPUCUSUZ  = 15   
XAL_IPUCULU   = 8    

def dashes(n):
    return "＿ " * n

class BayraqOyunu(BaseGame):
    def __init__(self):
        # Komandaların menyuda görunməsi üçün adları təyin edirik
        super().__init__("bayraq", "Bayraq Oyunu")

    def handles_callback(self, data, context, user_id):
        return data.startswith("bayraq__")

    # ── Oyunu başlat (/baslabayraq üçün) ──────────────────────────────────────
    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        # Siyahıdan 45 təsadüfi bayraq seçirik
        pool = random.sample(BAYRAQLАР, min(TURLAR, len(BAYRAQLАР)))
        context.user_data["game_state"] = {
            "pool": pool, "tur": 0, "xal": 0,
            "pas": PAS_HAKKI, "ipucu_gosterildi": False,
        }
        try:
            await query.message.delete()
        except Exception:
            pass
        await self._foto_gonder(query.message.chat_id, context)

    # ── Bayraq fotosunu göndər ────────────────────────────────────────────────
    async def _foto_gonder(self, chat_id, context):
        st  = context.user_data["game_state"]
        idx = st["tur"]
        s   = st["pool"][idx]

        ipucu_line = (
            f"💡 İlk hərf: *{s['ipucu']}*\n"
            f"🔤 {dashes(s['herf'])}"
            if st["ipucu_gosterildi"]
            else f"🔤 {dashes(s['herf'])}"
        )
        caption = (
            f"🚩 *Bayraq Oyunu* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"❓ Bu bayraq hansı ölkəyə aiddir?\n\n"
            f"{ipucu_line}\n\n"
            "✍️ Ölkə adını yazın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",  callback_data="bayraq__ipucu"),
             InlineKeyboardButton("⏭ Pas",     callback_data="bayraq__pas")],
            [InlineKeyboardButton("🔴 Bitir",  callback_data="bayraq__bitir")],
        ])
        msg = await context.bot.send_photo(
            chat_id=chat_id,
            photo=s["url"],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=kb,
        )
        context.user_data["game_state"]["last_msg_id"] = msg.message_id

    # ── Callback (İpucu, Pas, Bitir) ──────────────────────────────────────────
    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "bayraq__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("💡 İpucu artıq göstərilib!")
                return
            st["ipucu_gosterildi"] = True
            s, idx = st["pool"][st["tur"]], st["tur"]
            caption = (
                f"🚩 *Bayraq Oyunu* | Tur {idx+1}/{TURLAR}\n"
                f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
                f"❓ Bu bayraq hansı ölkəyə aiddir?\n\n"
                f"💡 İlk hərf: *{s['ipucu']}*\n"
                f"🔤 {dashes(s['herf'])}\n\n"
                "✍️ Ölkə adını yazın:"
            )
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("💡 İpucu (✅)", callback_data="bayraq__noop"),
                 InlineKeyboardButton("⏭ Pas",     callback_data="bayraq__pas")],
                [InlineKeyboardButton("🔴 Bitir",  callback_data="bayraq__bitir")],
            ])
            try:
                await query.edit_message_caption(caption=caption, parse_mode="Markdown", reply_markup=kb)
            except: pass

        elif data == "bayraq__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("⚠️ Pas hakkınız qalmayıb!", show_alert=True)
                return
            dogru = st["pool"][st["tur"]]["olke"]
            st["pas"] -= 1
            st["tur"] += 1
            st["ipucu_gosterildi"] = False
            await query.answer(f"⏭ Pas keçildi! Cavab: {dogru}")
            
            if st["tur"] >= TURLAR:
                await self._bitir_mesaj(query.message.chat_id, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._foto_gonder(query.message.chat_id, context)

        elif data == "bayraq__bitir":
            await self._bitir_mesaj(query.message.chat_id, context, st, user)

    # ── Mesaj (Cavabı yoxla) ──────────────────────────────────────────────────
    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st = context.user_data.get("game_state", {})
        if not st: return
        
        user  = update.effective_user
        # Hərf böyüklüyünə baxmırıq (strip() və lower() ilə)
        cavab = update.message.text.strip().lower()
        s     = st["pool"][st["tur"]]
        dogru = s["olke"].lower()

        if cavab == dogru:
            xal = XAL_IPUCUSUZ if not st["ipucu_gosterildi"] else XAL_IPUCULU
            st["xal"] += xal
            await update.message.reply_text(
                f"✅ *Düzgün!* 🎉\n🚩 Bu *{s['olke']}* bayrağı idi!\n⭐ +{xal} xal!",
                parse_mode="Markdown"
            )
            # Düz tapanda növbəti tur
            st["tur"] += 1
            st["ipucu_gosterildi"] = False
            
            if st["tur"] >= TURLAR:
                context.user_data["game_state"] = st
                await self._bitir_mesaj(update.effective_chat.id, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._foto_gonder(update.effective_chat.id, context)
        else:
            # Səhv cavabda bot növbəti tura keçmir, şəkil dəyişmir
            await update.message.reply_text("❌ Səhvdir, yenidən yoxlayın və ya 'Pas' verin.")

    # ── Top Oyunçular (/topbayraq üçün) ───────────────────────────────────────
    async def show_top(self, update, context):
        scores = context.bot_data.get("scores", {})
        if not scores:
            await update.message.reply_text("📊 Hələ ki xal qazanan yoxdur.")
            return
        
        # Xalları azalan sıra ilə düzürük
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        text = "🏆 *Bayraq Oyunu - Top 10 Oyunçu*\n\n"
        for i, (name, score) in enumerate(sorted_scores, 1):
            text += f"{i}. {name} — *{score} xal*\n"
        
        await update.message.reply_text(text, parse_mode="Markdown")

    # ── Oyun bitdi ────────────────────────────────────────────────────────────
    async def _bitir_mesaj(self, chat_id, context, st, user):
        self.add_score(context, user.full_name, st["xal"])
        self.clear_active(context)
        umumi = context.bot_data.get("scores", {}).get(user.full_name, 0)
        text = (
            f"🏁 *Bayraq Oyunu Bitdi!*\n\n"
            f"👤 Oyunçu: *{user.first_name}*\n"
            f"⭐ Topladığınız xal: *{st['xal']}*\n"
            f"🏆 Ümumi xalınız: *{umumi}*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən Oyna",  callback_data="oyun_bayraq")],
            [InlineKeyboardButton("🔙 Oyun Menyusu",  callback_data="ana_menu")],
        ])
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown", reply_markup=kb)
