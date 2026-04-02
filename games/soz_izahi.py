import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from games.base_game import BaseGame

# BÜTÜN SÖZ BAZASI (KODUN İÇİNDƏ)
INITIAL_DATA = [
    # QARIŞIQ (150+)
    {"word": "alma", "cat": "qarisiq"}, {"word": "şir", "cat": "qarisiq"}, {"word": "masa", "cat": "qarisiq"}, {"word": "kitab", "cat": "qarisiq"}, {"word": "qələm", "cat": "qarisiq"},
    {"word": "telefon", "cat": "qarisiq"}, {"word": "pəncərə", "cat": "qarisiq"}, {"word": "qapı", "cat": "qarisiq"}, {"word": "eynək", "cat": "qarisiq"}, {"word": "saat", "cat": "qarisiq"},
    {"word": "dəftər", "cat": "qarisiq"}, {"word": "çanta", "cat": "qarisiq"}, {"word": "maşın", "cat": "qarisiq"}, {"word": "təyyarə", "cat": "qarisiq"}, {"word": "gəmi", "cat": "qarisiq"},
    {"word": "velosiped", "cat": "qarisiq"}, {"word": "günəş", "cat": "qarisiq"}, {"word": "bulud", "cat": "qarisiq"}, {"word": "yağış", "cat": "qarisiq"}, {"word": "qar", "cat": "qarisiq"},
    {"word": "küçə", "cat": "qarisiq"}, {"word": "park", "cat": "qarisiq"}, {"word": "məktəb", "cat": "qarisiq"}, {"word": "universitet", "cat": "qarisiq"}, {"word": "çörək", "cat": "qarisiq"},
    {"word": "su", "cat": "qarisiq"}, {"word": "çay", "cat": "qarisiq"}, {"word": "kofe", "cat": "qarisiq"}, {"word": "şəkər", "cat": "qarisiq"}, {"word": "duz", "cat": "qarisiq"},
    {"word": "yumurta", "cat": "qarisiq"}, {"word": "pendir", "cat": "qarisiq"}, {"word": "balıq", "cat": "qarisiq"}, {"word": "toyuq", "cat": "qarisiq"}, {"word": "kartof", "cat": "qarisiq"},
    {"word": "soğan", "cat": "qarisiq"}, {"word": "pomidor", "cat": "qarisiq"}, {"word": "xiyar", "cat": "qarisiq"}, {"word": "üzüm", "cat": "qarisiq"}, {"word": "heyva", "cat": "qarisiq"},
    {"word": "armud", "cat": "qarisiq"}, {"word": "banan", "cat": "qarisiq"}, {"word": "portağal", "cat": "qarisiq"}, {"word": "limon", "cat": "qarisiq"}, {"word": "çiyələk", "cat": "qarisiq"},
    {"word": "qoz", "cat": "qarisiq"}, {"word": "fındıq", "cat": "qarisiq"}, {"word": "badam", "cat": "qarisiq"}, {"word": "şokolad", "cat": "qarisiq"}, {"word": "dondurma", "cat": "qarisiq"},
    {"word": "paltar", "cat": "qarisiq"}, {"word": "ayaqqabı", "cat": "qarisiq"}, {"word": "papaq", "cat": "qarisiq"}, {"word": "əlcək", "cat": "qarisiq"}, {"word": "şarf", "cat": "qarisiq"},
    {"word": "köynək", "cat": "qarisiq"}, {"word": "şalvar", "cat": "qarisiq"}, {"word": "pencək", "cat": "qarisiq"}, {"word": "corab", "cat": "qarisiq"}, {"word": "yataq", "cat": "qarisiq"},
    {"word": "divan", "cat": "qarisiq"}, {"word": "stul", "cat": "qarisiq"}, {"word": "televizor", "cat": "qarisiq"}, {"word": "kompüter", "cat": "qarisiq"}, {"word": "siçan", "cat": "qarisiq"},
    {"word": "klaviatura", "cat": "qarisiq"}, {"word": "soyuducu", "cat": "qarisiq"}, {"word": "soba", "cat": "qarisiq"}, {"word": "ütü", "cat": "qarisiq"}, {"word": "güzgü", "cat": "qarisiq"},
    {"word": "daraq", "cat": "qarisiq"}, {"word": "sabun", "cat": "qarisiq"}, {"word": "dəsmal", "cat": "qarisiq"}, {"word": "diş fırçası", "cat": "qarisiq"}, {"word": "xalça", "cat": "qarisiq"},
    {"word": "oyuncaq", "cat": "qarisiq"}, {"word": "top", "cat": "qarisiq"}, {"word": "kukla", "cat": "qarisiq"}, {"word": "şar", "cat": "qarisiq"}, {"word": "hədiyyə", "cat": "qarisiq"},
    {"word": "bayram", "cat": "qarisiq"}, {"word": "ad günü", "cat": "qarisiq"}, {"word": "toy", "cat": "qarisiq"}, {"word": "musiqi", "cat": "qarisiq"}, {"word": "mahnı", "cat": "qarisiq"},
    {"word": "rəqs", "cat": "qarisiq"}, {"word": "film", "cat": "qarisiq"}, {"word": "teatr", "cat": "qarisiq"}, {"word": "muzey", "cat": "qarisiq"}, {"word": "şəkil", "cat": "qarisiq"},
    {"word": "boya", "cat": "qarisiq"}, {"word": "fırça", "cat": "qarisiq"}, {"word": "kağız", "cat": "qarisiq"}, {"word": "qayçı", "cat": "qarisiq"}, {"word": "yapışqan", "cat": "qarisiq"},
    {"word": "çəkic", "cat": "qarisiq"}, {"word": "mismarı", "cat": "qarisiq"}, {"word": "balta", "cat": "qarisiq"}, {"word": "ip", "cat": "qarisiq"}, {"word": "iynə", "cat": "qarisiq"},
    {"word": "sap", "cat": "qarisiq"}, {"word": "düymə", "cat": "qarisiq"}, {"word": "pul", "cat": "qarisiq"}, {"word": "cüzdan", "cat": "qarisiq"}, {"word": "kart", "cat": "qarisiq"},
    {"word": "bank", "cat": "qarisiq"}, {"word": "apteka", "cat": "qarisiq"}, {"word": "xəstəxana", "cat": "qarisiq"}, {"word": "həkim", "cat": "qarisiq"}, {"word": "dərman", "cat": "qarisiq"},
    {"word": "polis", "cat": "qarisiq"}, {"word": "əsgər", "cat": "qarisiq"}, {"word": "yanğınsöndürən", "cat": "qarisiq"}, {"word": "bağban", "cat": "qarisiq"}, {"word": "aşpaz", "cat": "qarisiq"},
    {"word": "sürücü", "cat": "qarisiq"}, {"word": "pilot", "cat": "qarisiq"}, {"word": "kosmonavt", "cat": "qarisiq"}, {"word": "mühəndis", "cat": "qarisiq"}, {"word": "alim", "cat": "qarisiq"},
    {"word": "it", "cat": "qarisiq"}, {"word": "pişik", "cat": "qarisiq"}, {"word": "at", "cat": "qarisiq"}, {"word": "inək", "cat": "qarisiq"}, {"word": "qoyun", "cat": "qarisiq"},
    {"word": "keçi", "cat": "qarisiq"}, {"word": "dovşan", "cat": "qarisiq"}, {"word": "tülkü", "cat": "qarisiq"}, {"word": "canavar", "cat": "qarisiq"}, {"word": "ayı", "cat": "qarisiq"},
    {"word": "meymun", "cat": "qarisiq"}, {"word": "fil", "cat": "qarisiq"}, {"word": "zürafə", "cat": "qarisiq"}, {"word": "ilan", "cat": "qarisiq"}, {"word": "tısbağa", "cat": "qarisiq"},
    {"word": "qartal", "cat": "qarisiq"}, {"word": "tutuquşu", "cat": "qarisiq"}, {"word": "göyərçin", "cat": "qarisiq"}, {"word": "arı", "cat": "qarisiq"}, {"word": "kəpənək", "cat": "qarisiq"},
    {"word": "hörümçək", "cat": "qarisiq"}, {"word": "qarışqa", "cat": "qarisiq"}, {"word": "milçək", "cat": "qarisiq"}, {"word": "ağac", "cat": "qarisiq"}, {"word": "çiçək", "cat": "qarisiq"},
    {"word": "ot", "cat": "qarisiq"}, {"word": "meşə", "cat": "qarisiq"}, {"word": "dağ", "cat": "qarisiq"}, {"word": "dəniz", "cat": "qarisiq"}, {"word": "göl", "cat": "qarisiq"},
    {"word": "çay", "cat": "qarisiq"}, {"word": "okean", "cat": "qarisiq"}, {"word": "qum", "cat": "qarisiq"}, {"word": "daş", "cat": "qarisiq"}, {"word": "torpaq", "cat": "qarisiq"},

    # TARİX (150+)
    {"word": "şah ismayıl", "cat": "tarix"}, {"word": "atabəylər", "cat": "tarix"}, {"word": "babək", "cat": "tarix"}, {"word": "cavanşir", "cat": "tarix"}, {"word": "tomris", "cat": "tarix"},
    {"word": "nadir şah", "cat": "tarix"}, {"word": "uzun həsən", "cat": "tarix"}, {"word": "fətəli xan", "cat": "tarix"}, {"word": "məmməd əmin rəsulzadə", "cat": "tarix"}, {"word": "heydər əliyev", "cat": "tarix"},
    {"word": "nizami gəncəvi", "cat": "tarix"}, {"word": "nəsimi", "cat": "tarix"}, {"word": "füzuli", "cat": "tarix"}, {"word": "vaqif", "cat": "tarix"}, {"word": "axundov", "cat": "tarix"},
    {"word": "zərdabi", "cat": "tarix"}, {"word": "hacı zeynalabdin tağıyev", "cat": "tarix"}, {"word": "murtuza muxtarov", "cat": "tarix"}, {"word": "əziz bəyov", "cat": "tarix"}, {"word": "nərimanov", "cat": "tarix"},
    {"word": "atropatena", "cat": "tarix"}, {"word": "albaniya", "cat": "tarix"}, {"word": "manat", "cat": "tarix"}, {"word": "midiya", "cat": "tarix"}, {"word": "sümer", "cat": "tarix"},
    {"word": "mısır", "cat": "tarix"}, {"word": "roma", "cat": "tarix"}, {"word": "yunanıstan", "cat": "tarix"}, {"word": "çin səddi", "cat": "tarix"}, {"word": "piramida", "cat": "tarix"},
    {"word": "firon", "cat": "tarix"}, {"word": "sezar", "cat": "tarix"}, {"word": "isgəndər", "cat": "tarix"}, {"word": "atilla", "cat": "tarix"}, {"word": "çingiz xan", "cat": "tarix"},
    {"word": "əmir teymur", "cat": "tarix"}, {"word": "sultan süleyman", "cat": "tarix"}, {"word": "fatih sultan mehmed", "cat": "tarix"}, {"word": "ataturk", "cat": "tarix"}, {"word": "napoleon", "cat": "tarix"},
    {"word": "hitler", "cat": "tarix"}, {"word": "stalin", "cat": "tarix"}, {"word": "çörçill", "cat": "tarix"}, {"word": "linkoln", "cat": "tarix"}, {"word": "vaşinqton", "cat": "tarix"},
    {"word": "kolumb", "cat": "tarix"}, {"word": "maqellan", "cat": "tarix"}, {"word": "vasko da qama", "cat": "tarix"}, {"word": "marko polo", "cat": "tarix"}, {"word": "ibn sina", "cat": "tarix"},
    {"word": "biruni", "cat": "tarix"}, {"word": "nəsirəddin tusi", "cat": "tarix"}, {"word": "da vinçi", "cat": "tarix"}, {"word": "mikelyancelo", "cat": "tarix"}, {"word": "betxoven", "cat": "tarix"},
    {"word": "motsart", "cat": "tarix"}, {"word": "nyuton", "cat": "tarix"}, {"word": "eynşteyn", "cat": "tarix"}, {"word": "tesla", "cat": "tarix"}, {"word": "edison", "cat": "tarix"},
    {"word": "darvin", "cat": "tarix"}, {"word": "qaliley", "cat": "tarix"}, {"word": "kopernik", "cat": "tarix"}, {"word": "sokrat", "cat": "tarix"}, {"word": "platon", "cat": "tarix"},
    {"word": "aristotel", "cat": "tarix"}, {"word": "herodot", "cat": "tarix"}, {"word": "homer", "cat": "tarix"}, {"word": "şekspir", "cat": "tarix"}, {"word": "tolstoy", "cat": "tarix"},
    {"word": "dostoyevski", "cat": "tarix"}, {"word": "puşkin", "cat": "tarix"}, {"word": "vüqar həşimov", "cat": "tarix"}, {"word": "lütfi zadə", "cat": "tarix"}, {"word": "koroğlu", "cat": "tarix"},
    {"word": "qaçaq nəbi", "cat": "tarix"}, {"word": "mübariz ibrahimov", "cat": "tarix"}, {"word": "polad həşimov", "cat": "tarix"}, {"word": "çaldıran", "cat": "tarix"}, {"word": "gülüstan", "cat": "tarix"},
    {"word": "türkmənçay", "cat": "tarix"}, {"word": "mudros", "cat": "tarix"}, {"word": "lozan", "cat": "tarix"}, {"word": "versal", "cat": "tarix"}, {"word": "yalta", "cat": "tarix"},
    {"word": "qanlı yanvar", "cat": "tarix"}, {"word": "xocalı", "cat": "tarix"}, {"word": "şuşa", "cat": "tarix"}, {"word": "zəfər günü", "cat": "tarix"}, {"word": "istiqlal", "cat": "tarix"},
    {"word": "revolyusiya", "cat": "tarix"}, {"word": "monarxiya", "cat": "tarix"}, {"word": "demokratiya", "cat": "tarix"}, {"word": "imperiya", "cat": "tarix"}, {"word": "koloniya", "cat": "tarix"},
    {"word": "səfəvilər", "cat": "tarix"}, {"word": "osmanlı", "cat": "tarix"}, {"word": "səlcuqlu", "cat": "tarix"}, {"word": "qarabağ xanlığı", "cat": "tarix"}, {"word": "irəvan xanlığı", "cat": "tarix"},
    {"word": "şəki xanlığı", "cat": "tarix"}, {"word": "quba xanlığı", "cat": "tarix"}, {"word": "bakı xanlığı", "cat": "tarix"}, {"word": "qacar", "cat": "tarix"}, {"word": "pəhləvi", "cat": "tarix"},
    {"word": "qızıl ordu", "cat": "tarix"}, {"word": "nasizm", "cat": "tarix"}, {"word": "faşizm", "cat": "tarix"}, {"word": "kommunizm", "cat": "tarix"}, {"word": "kapitalizm", "cat": "tarix"},
    {"word": "soyuq müharibə", "cat": "tarix"}, {"word": "səlib yürüşü", "cat": "tarix"}, {"word": "renessans", "cat": "tarix"}, {"word": "islahat", "cat": "tarix"}, {"word": "məşrutə", "cat": "tarix"},
    {"word": "aksiz", "cat": "tarix"}, {"word": "vassal", "cat": "tarix"}, {"word": "feodal", "cat": "tarix"}, {"word": "burjuaziya", "cat": "tarix"}, {"word": "proletariat", "cat": "tarix"},
    {"word": "vikinglər", "cat": "tarix"}, {"word": "samuray", "cat": "tarix"}, {"word": "qladiator", "cat": "tarix"}, {"word": "şahzadə", "cat": "tarix"}, {"word": "vəzir", "cat": "tarix"},
    {"word": "elçi", "cat": "tarix"}, {"word": "fərman", "cat": "tarix"}, {"word": "müqavilə", "cat": "tarix"}, {"word": "ittifaq", "cat": "tarix"}, {"word": "blokada", "cat": "tarix"},
    {"word": "mühasirə", "cat": "tarix"}, {"word": "hücum", "cat": "tarix"}, {"word": "müdafiə", "cat": "tarix"}, {"word": "qələbə", "cat": "tarix"}, {"word": "məğlubiyyət", "cat": "tarix"},
    {"word": "sülh", "cat": "tarix"}, {"word": "atəşkəs", "cat": "tarix"}, {"word": "soyqırım", "cat": "tarix"}, {"word": "terror", "cat": "tarix"}, {"word": "işğal", "cat": "tarix"},
    {"word": "azadlıq", "cat": "tarix"}, {"word": "bayraq", "cat": "tarix"}, {"word": "gerb", "cat": "tarix"}, {"word": "himn", "cat": "tarix"}, {"word": "ordu", "cat": "tarix"},

    # COĞRAFİYA (150+)
    {"word": "everest", "cat": "cografiya"}, {"word": "xəzər", "cat": "cografiya"}, {"word": "amazon", "cat": "cografiya"}, {"word": "nil", "cat": "cografiya"}, {"word": "kür", "cat": "cografiya"},
    {"word": "araz", "cat": "cografiya"}, {"word": "böyük səhra", "cat": "cografiya"}, {"word": "alplar", "cat": "cografiya"}, {"word": "qafqaz", "cat": "cografiya"}, {"word": "ural", "cat": "cografiya"},
    {"word": "himalay", "cat": "cografiya"}, {"word": "and dağları", "cat": "cografiya"}, {"word": "vulkan", "cat": "cografiya"}, {"word": "zəlzələ", "cat": "cografiya"}, {"word": "sunami", "cat": "cografiya"},
    {"word": "ekvator", "cat": "cografiya"}, {"word": "meridian", "cat": "cografiya"}, {"word": "paralel", "cat": "cografiya"}, {"word": "qütb", "cat": "cografiya"}, {"word": "antarktida", "cat": "cografiya"},
    {"word": "avstraliya", "cat": "cografiya"}, {"word": "avropa", "cat": "cografiya"}, {"word": "asya", "cat": "cografiya"}, {"word": "afrika", "cat": "cografiya"}, {"word": "amerika", "cat": "cografiya"},
    {"word": "okeaniya", "cat": "cografiya"}, {"word": "sakit okean", "cat": "cografiya"}, {"word": "atlantik okean", "cat": "cografiya"}, {"word": "hind okeanı", "cat": "cografiya"}, {"word": "şimal buzlu okean", "cat": "cografiya"},
    {"word": "qara dəniz", "cat": "cografiya"}, {"word": "aralıq dənizi", "cat": "cografiya"}, {"word": "qırmızı dəniz", "cat": "cografiya"}, {"word": "mərmərə dənizi", "cat": "cografiya"}, {"word": "baykal gölü", "cat": "cografiya"},
    {"word": "viktoriya gölü", "cat": "cografiya"}, {"word": "göy göl", "cat": "cografiya"}, {"word": "maral göl", "cat": "cografiya"}, {"word": "şahdağ", "cat": "cografiya"}, {"word": "tufandağ", "cat": "cografiya"},
    {"word": "bazardüzü", "cat": "cografiya"}, {"word": "yanardağ", "cat": "cografiya"}, {"word": "qobustan", "cat": "cografiya"}, {"word": "palçıq vulkanı", "cat": "cografiya"}, {"word": "neft daşları", "cat": "cografiya"},
    {"word": "bakı", "cat": "cografiya"}, {"word": "gence", "cat": "cografiya"}, {"word": "sumqayit", "cat": "cografiya"}, {"word": "naxçıvan", "cat": "cografiya"}, {"word": "lənkəran", "cat": "cografiya"},
    {"word": "şəki", "cat": "cografiya"}, {"word": "qəbələ", "cat": "cografiya"}, {"word": "quba", "cat": "cografiya"}, {"word": "şuşa", "cat": "cografiya"}, {"word": "ankara", "cat": "cografiya"},
    {"word": "istanbul", "cat": "cografiya"}, {"word": "moskva", "cat": "cografiya"}, {"word": "london", "cat": "cografiya"}, {"word": "parij", "cat": "cografiya"}, {"word": "berlin", "cat": "cografiya"},
    {"word": "roma", "cat": "cografiya"}, {"word": "vaşinqton", "cat": "cografiya"}, {"word": "tokio", "cat": "cografiya"}, {"word": "pekin", "cat": "cografiya"}, {"word": "qahirə", "cat": "cografiya"},
    {"word": "braziliya", "cat": "cografiya"}, {"word": "kanada", "cat": "cografiya"}, {"word": "mexiko", "cat": "cografiya"}, {"word": "madrıd", "cat": "cografiya"}, {"word": "viana", "cat": "cografiya"},
    {"word": "oslo", "cat": "cografiya"}, {"word": "stokholm", "cat": "cografiya"}, {"word": "helsinki", "cat": "cografiya"}, {"word": "kopenhagen", "cat": "cografiya"}, {"word": "praqa", "cat": "cografiya"},
    {"word": "varşava", "cat": "cografiya"}, {"word": "budapeşt", "cat": "cografiya"}, {"word": "afina", "cat": "cografiya"}, {"word": "lissabon", "cat": "cografiya"}, {"word": "dublin", "cat": "cografiya"},
    {"word": "tbilisi", "cat": "cografiya"}, {"word": "irevan", "cat": "cografiya"}, {"word": "tehran", "cat": "cografiya"}, {"word": "bağdad", "cat": "cografiya"}, {"word": "riyad", "cat": "cografiya"},
    {"word": "islamabad", "cat": "cografiya"}, {"word": "yeni dehli", "cat": "cografiya"}, {"word": "astana", "cat": "cografiya"}, {"word": "daşkənd", "cat": "cografiya"}, {"word": "bişkək", "cat": "cografiya"},
    {"word": "eşqabad", "cat": "cografiya"}, {"word": "düşənbə", "cat": "cografiya"}, {"word": "kabil", "cat": "cografiya"}, {"word": "seul", "cat": "cografiya"}, {"word": "banqkok", "cat": "cografiya"},
    {"word": "sinqapur", "cat": "cografiya"}, {"word": "sidney", "cat": "cografiya"}, {"word": "ottava", "cat": "cografiya"}, {"word": "buenos ayres", "cat": "cografiya"}, {"word": "santiago", "cat": "cografiya"},
    {"word": "ada", "cat": "cografiya"}, {"word": "yarımada", "cat": "cografiya"}, {"word": "körfəz", "cat": "cografiya"}, {"word": "boğaz", "cat": "cografiya"}, {"word": "dərə", "cat": "cografiya"},
    {"word": "təpə", "cat": "cografiya"}, {"word": "düzənlik", "cat": "cografiya"}, {"word": "vadi", "cat": "cografiya"}, {"word": "şəlalə", "cat": "cografiya"}, {"word": "geyser", "cat": "cografiya"},
    {"word": "buzlaq", "cat": "cografiya"}, {"word": "cəngəllik", "cat": "cografiya"}, {"word": "savanna", "cat": "cografiya"}, {"word": "tundra", "cat": "cografiya"}, {"word": "tayqa", "cat": "cografiya"},
    {"word": "iqlim", "cat": "cografiya"}, {"word": "atmosfer", "cat": "cografiya"}, {"word": "stratosfer", "cat": "cografiya"}, {"word": "ozon təbəqəsi", "cat": "cografiya"}, {"word": "külək", "cat": "cografiya"},
    {"word": "siklon", "cat": "cografiya"}, {"word": "tayfun", "cat": "cografiya"}, {"word": "tornado", "cat": "cografiya"}, {"word": "rütubət", "cat": "cografiya"}, {"word": "təzyiq", "cat": "cografiya"},
    {"word": "kompas", "cat": "cografiya"}, {"word": "xəritə", "cat": "cografiya"}, {"word": "atlas", "cat": "cografiya"}, {"word": "miqyas", "cat": "cografiya"}, {"word": "qlobus", "cat": "cografiya"},
    {"word": "azimut", "cat": "cografiya"}, {"word": "relyef", "cat": "cografiya"}, {"word": "faydalı qazıntı", "cat": "cografiya"}, {"word": "neft", "cat": "cografiya"}, {"word": "qaz", "cat": "cografiya"},
    {"word": "qızıl", "cat": "cografiya"}, {"word": "dəmir", "cat": "cografiya"}, {"word": "mis", "cat": "cografiya"}, {"word": "almaz", "cat": "cografiya"}, {"word": "kömür", "cat": "cografiya"},
    {"word": "əhali", "cat": "cografiya"}, {"word": "miqrasiya", "cat": "cografiya"}, {"word": "urbanizasiya", "cat": "cografiya"}, {"word": "iqtisadiyyat", "cat": "cografiya"}, {"word": "sənaye", "cat": "cografiya"},
    {"word": "kənd təsərrüfatı", "cat": "cografiya"}, {"word": "nəqliyyat", "cat": "cografiya"}, {"word": "turizm", "cat": "cografiya"}, {"word": "ekologiya", "cat": "cografiya"}, {"word": "təbiət", "cat": "cografiya"},

    # İNSAN ADLARI (150+)
    {"word": "vaqif", "cat": "insan"}, {"word": "leyla", "cat": "insan"}, {"word": "əli", "cat": "insan"}, {"word": "vəli", "cat": "insan"}, {"word": "həsən", "cat": "insan"},
    {"word": "hüseyn", "cat": "insan"}, {"word": "məmməd", "cat": "insan"}, {"word": "əhməd", "cat": "insan"}, {"word": "mustafa", "cat": "insan"}, {"word": "fatima", "cat": "insan"},
    {"word": "zəhra", "cat": "insan"}, {"word": "nərmin", "cat": "insan"}, {"word": "aygün", "cat": "insan"}, {"word": "günel", "cat": "insan"}, {"word": "vüsal", "cat": "insan"},
    {"word": "vüqar", "cat": "insan"}, {"word": "rəşad", "cat": "insan"}, {"word": "elvin", "cat": "insan"}, {"word": "tural", "cat": "insan"}, {"word": "anar", "cat": "insan"},
    {"word": "elnur", "cat": "insan"}, {"word": "samir", "cat": "insan"}, {"word": "ramil", "cat": "insan"}, {"word": "orxan", "cat": "insan"}, {"word": "fərid", "cat": "insan"},
    {"word": "nicat", "cat": "insan"}, {"word": "şahin", "cat": "insan"}, {"word": "rovşən", "cat": "insan"}, {"word": "ilqar", "cat": "insan"}, {"word": "namiq", "cat": "insan"},
    {"word": "pərviz", "cat": "insan"}, {"word": "eyvaz", "cat": "insan"}, {"word": "ümüd", "cat": "insan"}, {"word": "murad", "cat": "insan"}, {"word": "fuad", "cat": "insan"},
    {"word": "emil", "cat": "insan"}, {"word": "ruslan", "cat": "insan"}, {"word": "zamin", "cat": "insan"}, {"word": "taleh", "cat": "insan"}, {"word": "pənah", "cat": "insan"},
    {"word": "ismayıl", "cat": "insan"}, {"word": "ibrahim", "cat": "insan"}, {"word": "yusif", "cat": "insan"}, {"word": "yunis", "cat": "insan"}, {"word": "yaqub", "cat": "insan"},
    {"word": "isa", "cat": "insan"}, {"word": "musa", "cat": "insan"}, {"word": "davud", "cat": "insan"}, {"word": "süleyman", "cat": "insan"}, {"word": "nuh", "cat": "insan"},
    {"word": "məryəm", "cat": "insan"}, {"word": "ayşə", "cat": "insan"}, {"word": "xədicə", "cat": "insan"}, {"word": "zeynəb", "cat": "insan"}, {"word": "gülnar", "cat": "insan"},
    {"word": "sevinc", "cat": "insan"}, {"word": "sevil", "cat": "insan"}, {"word": "könül", "cat": "insan"}, {"word": "lalə", "cat": "insan"}, {"word": "nərgiz", "cat": "insan"},
    {"word": "bənövşə", "cat": "insan"}, {"word": "reyhan", "cat": "insan"}, {"word": "fidan", "cat": "insan"}, {"word": "çiçək", "cat": "insan"}, {"word": "ulduz", "cat": "insan"},
    {"word": "aytac", "cat": "insan"}, {"word": "aynur", "cat": "insan"}, {"word": "aydan", "cat": "insan"}, {"word": "aysel", "cat": "insan"}, {"word": "günay", "cat": "insan"},
    {"word": "vəfa", "cat": "insan"}, {"word": "sədaqət", "cat": "insan"}, {"word": "arzu", "cat": "insan"}, {"word": "arzuman", "cat": "insan"}, {"word": "dəniz", "cat": "insan"},
    {"word": "yağmur", "cat": "insan"}, {"word": "günəş", "cat": "insan"}, {"word": "ay", "cat": "insan"}, {"word": "parlaq", "cat": "insan"}, {"word": "aydın", "cat": "insan"},
    {"word": "rauf", "cat": "insan"}, {"word": "nail", "cat": "insan"}, {"word": "naidə", "cat": "insan"}, {"word": "nazlı", "cat": "insan"}, {"word": "məhin", "cat": "insan"},
    {"word": "mətanət", "cat": "insan"}, {"word": "mənzər", "cat": "insan"}, {"word": "mehriban", "cat": "insan"}, {"word": "məlahət", "cat": "insan"}, {"word": "səbinə", "cat": "insan"},
    {"word": "fidan", "cat": "insan"}, {"word": "fəridə", "cat": "insan"}, {"word": "lamiyə", "cat": "insan"}, {"word": "təranə", "cat": "insan"}, {"word": "pərvanə", "cat": "insan"},
    {"word": "rəna", "cat": "insan"}, {"word": "röya", "cat": "insan"}, {"word": "xəyal", "cat": "insan"}, {"word": "vüsalə", "cat": "insan"}, {"word": "məleykə", "cat": "insan"},
    {"word": "nuray", "cat": "insan"}, {"word": "nigar", "cat": "insan"}, {"word": "banu", "cat": "insan"}, {"word": "aylin", "cat": "insan"}, {"word": "məsumə", "cat": "insan"},
    {"word": "sidqi", "cat": "insan"}, {"word": "samirə", "cat": "insan"}, {"word": "kamran", "cat": "insan"}, {"word": "kamil", "cat": "insan"}, {"word": "kənan", "cat": "insan"},
    {"word": "ümid", "cat": "insan"}, {"word": "elmir", "cat": "insan"}, {"word": "elsəvər", "cat": "insan"}, {"word": "elmar", "cat": "insan"},
    {"word": "şaiq", "cat": "insan"}, {"word": "sabir", "cat": "insan"}, {"word": "mikayıl", "cat": "insan"}, {"word": "abdulla", "cat": "insan"}, {"word": "vahid", "cat": "insan"},
    {"word": "bəxtiyar", "cat": "insan"}, {"word": "mübariz", "cat": "insan"}, {"word": "polad", "cat": "insan"}, {"word": "ilham", "cat": "insan"}, {"word": "naməlum", "cat": "insan"},
    {"word": "şövkət", "cat": "insan"}, {"word": "rəşid", "cat": "insan"}, {"word": "müslüm", "cat": "insan"}, {"word": "zeynab", "cat": "insan"}, {"word": "flora", "cat": "insan"},
    {"word": "akif", "cat": "insan"}, {"word": "asif", "cat": "insan"}, {"word": "vasif", "cat": "insan"}, {"word": "aqil", "cat": "insan"}, {"word": "adil", "cat": "insan"},
    {"word": "faiq", "cat": "insan"}, {"word": "tariyel", "cat": "insan"}, {"word": "mədəd", "cat": "insan"}, {"word": "qədir", "cat": "insan"},
    {"word": "alxan", "cat": "insan"}, {"word": "eldar", "cat": "insan"}, {"word": "müzəffər", "cat": "insan"}, {"word": "şükür", "cat": "insan"}, {"word": "şərif", "cat": "insan"},
    {"word": "lətif", "cat": "insan"}, {"word": "məcid", "cat": "insan"}, {"word": "qurban", "cat": "insan"}, {"word": "ramazan", "cat": "insan"}, {"word": "novruz", "cat": "insan"}
]

class SozIzahi(BaseGame):
    def __init__(self):
        super().__init__("cro", "HT-Cro")
        self.temp_scores = {}

    def handles_callback(self, data, context, user_id):
        return data.startswith("cro__")

    async def start_game(self, update_or_query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        
        text = "🎮 *HT-Cro* modunu seçin:"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌀 Qarışıq Sözlər", callback_data="cro__mod_qarisiq")],
            [InlineKeyboardButton("📜 Tarix", callback_data="cro__mod_tarix"), 
             InlineKeyboardButton("🌍 Coğrafiya", callback_data="cro__mod_cografiya")],
            [InlineKeyboardButton("👥 İnsan Adları", callback_data="cro__mod_insan")],
            [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
        ])
        
        if isinstance(update_or_query, Update):
            await update_or_query.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await update_or_query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st = context.chat_data.get("game_state", {})
        user = query.from_user

        # MOD SEÇİMİ
        if data.startswith("cro__mod_"):
            mod = data.split("_")[-1]
            all_words = [i['word'] for i in INITIAL_DATA if i['cat'] == mod]
            if not all_words:
                await query.answer("Bu kateqoriyada söz yoxdur!", show_alert=True)
                return
            
            chosen = random.choice(all_words)
            context.chat_data["game_state"] = {
                "soz": chosen,
                "mod": mod,
                "aparici_id": None,
                "aparici_ad": None
            }
            
            text = f"✅ *{mod.capitalize()}* modu seçildi!\n\n👇 Kim izah etmək istəyir? Butona basın."
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎤 Sözü İzah Et", callback_data="cro__aparici_ol")],
                [InlineKeyboardButton("🔙 Modu Dəyiş", callback_data="cro__back_to_mods")],
                [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
            ])
            await query.answer() # Buton donmasın deyə
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

        elif data == "cro__back_to_mods":
            await query.answer()
            await self.start_game(query, context)

        elif data == "cro__aparici_ol":
            if st.get("aparici_id") is not None and st["aparici_id"] != user.id:
                await query.answer(f"Artıq aparıcı var: {st['aparici_ad']}", show_alert=True)
                return

            st["aparici_id"] = user.id
            st["aparici_ad"] = user.first_name
            
            await query.answer(f"Sözün: {st['soz'].upper()}", show_alert=True)
            
            text = (
                f"👤 *Aparıcı:* {user.mention_markdown()}\n"
                f"📂 *Mod:* {st['mod'].capitalize()}\n"
                f"📢 Sözü izah edir... Tapın görək!"
            )
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔍 Sözə Baxmaq", callback_data="cro__soze_bax")],
                [InlineKeyboardButton("❌ Fikrimi Dəyişdim", callback_data="cro__imtina")],
                [InlineKeyboardButton("♻️ Növbəti Söz", callback_data="cro__novbeti")]
            ])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

        elif data == "cro__soze_bax":
            # game_state-i yenidən oxuduğunuzdan əmin olun
            st = context.chat_data.get("game_state", {})
            if user.id == st.get("aparici_id"):
                await query.answer(f"Sənin sözün: {st['soz'].upper()}", show_alert=True)
            else:
                await query.answer("Sən aparıcı deyilsən!", show_alert=True)

        elif data == "cro__novbeti":
            st = context.chat_data.get("game_state", {})
            if user.id == st.get("aparici_id"):
                mod = st.get('mod', 'qarisiq')
                all_words = [i['word'] for i in INITIAL_DATA if i['cat'] == mod]
                new_word = random.choice(all_words)
                
                # MƏLUMATI YENİLƏYİN
                st['soz'] = new_word
                context.chat_data["game_state"] = st # VACİB HİSSƏ
                
                await query.answer(f"Yeni sözün: {new_word.upper()}", show_alert=True)
            else:
                await query.answer("Yalnız aparıcı sözü dəyişə bilər!", show_alert=True)
                
        elif data == "cro__imtina":
            if st.get("aparici_id") == user.id:
                st["aparici_id"] = None
                st["aparici_ad"] = None
                await query.answer("Aparıcılıqdan imtina edildi")
                
                text = f"❌ {user.mention_markdown()} aparıcılıqdan imtina etdi.\n\n👇 Kim izah etmək istəyir? Butona basın."
                kb = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎤 Aparıcı Olmaq İstəyirəm", callback_data="cro__aparici_ol")],
                    [InlineKeyboardButton("🔙 Modu Dəyiş", callback_data="cro__back_to_mods")],
                    [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
                ])
                await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
            else:
                await query.answer("Sən aparıcı deyilsən!", show_alert=True)

        elif data == "cro__bitir":
            await query.answer("Oyun bitirilir...")
            self.clear_active(context)
            await query.edit_message_text("**🏁 HT-Cro dayandırıldı.**")
            
    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st = context.chat_data.get("game_state", {})
        if not st or st.get("aparici_id") is None: return

        user = update.effective_user
        cavab = update.message.text.strip().lower()
        dogru_soz = st["soz"].lower()

        if user.id == st["aparici_id"]:
            if cavab == dogru_soz:
                await update.message.reply_text("🚫 Aparıcı cavabı özü yazmaz!")
            return

        if cavab == dogru_soz:
            self.temp_scores[user.id] = self.temp_scores.get(user.id, 0) + 10
            
            await update.message.reply_text(
                f"🥳 *{user.first_name}* düzgün tapdı! \n"
                f"✅ Söz: *{dogru_soz.upper()}* \n"
                f"🏆 +10 xal qazandın! Yeni raund başlayır..."
            , parse_mode="Markdown")
            
            mod = st['mod']
            all_words = [i['word'] for i in INITIAL_DATA if i['cat'] == mod]
            st['soz'] = random.choice(all_words)
            st['aparici_id'] = None
            st['aparici_ad'] = None
            context.chat_data["game_state"] = st
            
            await self.start_game(update, context)
