"""
Curated baseline of known global seed companies. This guarantees the directory is
useful on day one, before any scraping runs. Extend freely.

Sources: public company websites, industry association member lists, wikipedia.
"""

SEED_COMPANIES = [
    # --- United States ---
    {"name": "Bayer Crop Science (Vegetable Seeds)", "country": "United States", "website": "https://www.vegetables.bayer.com", "crops": "tomato,pepper,cucumber,melon,lettuce,broccoli", "description": "Global vegetable seed arm of Bayer (includes Seminis, De Ruiter brands).", "source": "curated"},
    {"name": "Seminis", "country": "United States", "website": "https://www.seminis.com", "crops": "tomato,pepper,cucumber,melon,bean,lettuce", "description": "Global vegetable seed brand, part of Bayer.", "source": "curated"},
    {"name": "De Ruiter", "country": "Netherlands", "website": "https://www.deruiterseeds.com", "crops": "tomato,pepper,cucumber,eggplant,rootstock", "description": "Protected-culture vegetable seeds, part of Bayer.", "source": "curated"},
    {"name": "Harris Moran Seed Company", "country": "United States", "website": "https://www.harrismoran.com", "crops": "tomato,pepper,melon,onion,broccoli", "description": "Vegetable seed breeder, part of HM.Clause / Limagrain.", "source": "curated"},
    {"name": "Johnny's Selected Seeds", "country": "United States", "website": "https://www.johnnyseeds.com", "crops": "tomato,pepper,lettuce,herbs,flowers", "description": "Employee-owned breeder/supplier based in Maine.", "source": "curated"},
    {"name": "Burpee Seeds", "country": "United States", "website": "https://www.burpee.com", "crops": "tomato,pepper,bean,flowers", "description": "Historic American home-garden seed company, est. 1876.", "source": "curated"},
    {"name": "Territorial Seed Company", "country": "United States", "website": "https://www.territorialseed.com", "crops": "tomato,pepper,lettuce,herbs", "description": "Oregon-based seed company focused on PNW-adapted varieties.", "source": "curated"},
    {"name": "Baker Creek Heirloom Seeds", "country": "United States", "website": "https://www.rareseeds.com", "crops": "tomato,pepper,melon,bean", "description": "Heirloom seed specialist, Missouri.", "source": "curated"},
    {"name": "High Mowing Organic Seeds", "country": "United States", "website": "https://www.highmowingseeds.com", "crops": "tomato,pepper,lettuce,herbs", "description": "100% certified organic seed company, Vermont.", "source": "curated"},
    {"name": "Stokes Seeds", "country": "United States", "website": "https://www.stokeseeds.com", "crops": "tomato,pepper,onion,flowers", "description": "Vegetable and flower seeds, US and Canada.", "source": "curated"},
    {"name": "Siegers Seed Company", "country": "United States", "website": "https://www.siegers.com", "crops": "tomato,pepper,melon,pumpkin", "description": "Commercial vegetable seed distributor, Michigan.", "source": "curated"},
    {"name": "Sakata Seed America", "country": "United States", "website": "https://www.sakata.com", "crops": "tomato,broccoli,lettuce,sunflower", "description": "US arm of Japanese breeder Sakata.", "source": "curated"},
    {"name": "PanAmerican Seed", "country": "United States", "website": "https://www.panamseed.com", "crops": "flowers,tomato", "description": "Ornamentals and some vegetables, part of Ball Horticultural.", "source": "curated"},
    {"name": "Ball Horticultural", "country": "United States", "website": "https://www.ballhort.com", "crops": "flowers,vegetables", "description": "Global breeder and distributor of flowers and vegetables.", "source": "curated"},

    # --- Netherlands ---
    {"name": "Rijk Zwaan", "country": "Netherlands", "website": "https://www.rijkzwaan.com", "crops": "tomato,pepper,cucumber,lettuce,melon,onion", "description": "Global vegetable breeder, family-owned, HQ De Lier.", "source": "curated"},
    {"name": "Enza Zaden", "country": "Netherlands", "website": "https://www.enzazaden.com", "crops": "tomato,pepper,cucumber,lettuce,melon,spinach", "description": "Global vegetable breeder, Enkhuizen.", "source": "curated"},
    {"name": "Bejo Zaden", "country": "Netherlands", "website": "https://www.bejo.com", "crops": "onion,carrot,cabbage,beetroot", "description": "Open-field vegetable specialist.", "source": "curated"},
    {"name": "Nunhems (BASF)", "country": "Netherlands", "website": "https://www.nunhems.com", "crops": "tomato,cucumber,melon,onion,carrot,pepper", "description": "Vegetable seeds, part of BASF.", "source": "curated"},
    {"name": "Syngenta Vegetable Seeds", "country": "Netherlands", "website": "https://www.syngentavegetables.com", "crops": "tomato,pepper,cucumber,melon,sweet corn", "description": "Vegetable seed division of Syngenta; Rogers and S&G brands.", "source": "curated"},
    {"name": "Hazera", "country": "Netherlands", "website": "https://www.hazera.com", "crops": "tomato,pepper,cucumber,onion,melon", "description": "Joint venture between Limagrain and Sumitomo, Israeli roots.", "source": "curated"},
    {"name": "Pop Vriend Seeds", "country": "Netherlands", "website": "https://www.popvriendseeds.com", "crops": "bean,spinach,beetroot", "description": "Open-field vegetable breeder, part of KWS.", "source": "curated"},

    # --- France / Europe ---
    {"name": "Limagrain / HM.Clause", "country": "France", "website": "https://www.hmclause.com", "crops": "tomato,pepper,carrot,melon,onion", "description": "Global vegetable seed arm of farmer-owned Limagrain.", "source": "curated"},
    {"name": "Vilmorin-Mikado", "country": "France", "website": "https://www.vilmorinmikado.com", "crops": "tomato,carrot,lettuce,melon,leek", "description": "Part of Limagrain, fresh-market vegetables.", "source": "curated"},
    {"name": "Gautier Semences", "country": "France", "website": "https://www.gautiersemences.com", "crops": "tomato,lettuce,melon,strawberry", "description": "Family-owned vegetable seed breeder in Provence.", "source": "curated"},
    {"name": "Clause Vegetable Seeds", "country": "France", "website": "https://www.hmclause.com", "crops": "tomato,pepper,carrot,melon", "description": "Part of HM.Clause / Limagrain.", "source": "curated"},
    {"name": "Sativa Rheinau", "country": "Switzerland", "website": "https://www.sativa-rheinau.ch", "crops": "tomato,lettuce,cereals", "description": "Organic and biodynamic seed breeder.", "source": "curated"},
    {"name": "Graines Voltz", "country": "France", "website": "https://www.grainesvoltz.com", "crops": "vegetables,flowers", "description": "Major European seed distributor.", "source": "curated"},

    # --- Germany ---
    {"name": "KWS Saat", "country": "Germany", "website": "https://www.kws.com", "crops": "sugar beet,corn,cereals,vegetables", "description": "Major field crop breeder, also vegetables via Pop Vriend.", "source": "curated"},
    {"name": "Bingenheimer Saatgut", "country": "Germany", "website": "https://www.bingenheimersaatgut.de", "crops": "tomato,lettuce,cabbage,herbs", "description": "Organic/biodynamic seed cooperative.", "source": "curated"},

    # --- Italy / Spain ---
    {"name": "Esasem", "country": "Italy", "website": "https://www.esasem.com", "crops": "tomato,pepper,melon,cucumber", "description": "Italian vegetable seed breeder.", "source": "curated"},
    {"name": "Isi Sementi", "country": "Italy", "website": "https://www.isisementi.com", "crops": "tomato,pepper,melon,watermelon", "description": "Italian vegetable seed breeder.", "source": "curated"},
    {"name": "Blumen Group", "country": "Italy", "website": "https://www.blumengroup.it", "crops": "vegetables,flowers,lawn", "description": "Italian seed distributor.", "source": "curated"},
    {"name": "Semillas Fitó", "country": "Spain", "website": "https://www.semillasfito.com", "crops": "tomato,pepper,melon,watermelon,cucumber", "description": "Spanish family-owned vegetable and field crop breeder.", "source": "curated"},
    {"name": "Ramiro Arnedo", "country": "Spain", "website": "https://www.ramiroarnedo.com", "crops": "tomato,pepper,melon,onion", "description": "Spanish vegetable seed breeder.", "source": "curated"},
    {"name": "Zeraim Iberica", "country": "Spain", "website": "https://www.zeraim.com", "crops": "tomato,pepper,cucumber,melon", "description": "Iberian arm of Zeraim (Syngenta).", "source": "curated"},

    # --- Israel ---
    {"name": "Zeraim Gedera", "country": "Israel", "website": "https://www.zeraim.com", "crops": "tomato,pepper,cucumber,melon,watermelon", "description": "Vegetable breeder, part of Syngenta.", "source": "curated"},
    {"name": "Origene Seeds", "country": "Israel", "website": "https://www.origeneseeds.com", "crops": "tomato,pepper,melon,watermelon", "description": "Vegetable seeds for warm climates.", "source": "curated"},
    {"name": "Hishtil", "country": "Israel", "website": "https://www.hishtil.com", "crops": "tomato,pepper,herbs,strawberry", "description": "Grafted plants and seeds, global propagation network.", "source": "curated"},
    {"name": "TomaTech", "country": "Israel", "website": "https://www.tomatech.co.il", "crops": "tomato", "description": "Tomato-specialist breeder.", "source": "curated"},
    {"name": "Philoseed", "country": "Israel", "website": "https://www.philoseed.com", "crops": "tomato,pepper,watermelon", "description": "Vegetable breeder.", "source": "curated"},

    # --- Japan ---
    {"name": "Sakata Seed Corporation", "country": "Japan", "website": "https://www.sakataseed.co.jp", "crops": "tomato,broccoli,lettuce,sunflower,lisianthus", "description": "Global breeder of vegetables and ornamentals, Yokohama.", "source": "curated"},
    {"name": "Takii & Co.", "country": "Japan", "website": "https://www.takii.com", "crops": "tomato,cabbage,onion,lettuce,flowers", "description": "Global vegetable and flower breeder, Kyoto.", "source": "curated"},
    {"name": "Tokita Seed", "country": "Japan", "website": "https://www.tokitaseed.co.jp", "crops": "tomato,pepper,cucumber", "description": "Japanese vegetable breeder.", "source": "curated"},
    {"name": "Mikado Kyowa Seed", "country": "Japan", "website": "https://www.mikadokyowa.com", "crops": "tomato,pepper,melon,cabbage", "description": "Japanese vegetable breeder, ties to Vilmorin-Mikado.", "source": "curated"},

    # --- China ---
    {"name": "Syngenta China", "country": "China", "website": "https://www.syngenta.com.cn", "crops": "corn,vegetables,tomato", "description": "China arm of Syngenta Group (ChemChina).", "source": "curated"},
    {"name": "Beijing Shounong Seed Industry", "country": "China", "website": "", "crops": "vegetables,tomato", "description": "Major state-linked vegetable seed company.", "source": "curated"},
    {"name": "Asia Seed", "country": "China", "website": "https://www.asiaseed.com", "crops": "tomato,pepper,watermelon,cabbage", "description": "Vegetable seed breeder with operations in China and SE Asia.", "source": "curated"},
    {"name": "Beijing Gold Agriculture Seed", "country": "China", "website": "", "crops": "tomato,pepper,cabbage", "description": "Chinese vegetable seed breeder.", "source": "curated"},
    {"name": "Denghai Seeds", "country": "China", "website": "http://www.denghai.com", "crops": "corn,vegetables", "description": "Shandong-based major seed company.", "source": "curated"},
    {"name": "Longping High-Tech", "country": "China", "website": "https://www.lpht.com.cn", "crops": "rice,corn,vegetables", "description": "Major Chinese seed company, rice/corn focus.", "source": "curated"},
    {"name": "Origin Agritech", "country": "China", "website": "https://www.originagritech.com", "crops": "corn,rice,canola,cotton", "description": "Chinese crop biotech and seed company.", "source": "curated"},
    {"name": "Blue River Seeds", "country": "China", "website": "", "crops": "tomato,vegetables", "description": "Chinese vegetable seed company.", "source": "curated"},
    {"name": "Horticulture Seeds (HortiSeeds)", "country": "China", "website": "", "crops": "tomato,pepper,cucumber", "description": "Chinese vegetable seed supplier.", "source": "curated"},
    {"name": "Nongwoobio (China)", "country": "China", "website": "https://www.nongwoobio.com.cn", "crops": "tomato,pepper,cabbage", "description": "Chinese arm of Korean breeder Nongwoo.", "source": "curated"},

    # --- South Korea ---
    {"name": "Nongwoo Bio", "country": "South Korea", "website": "https://www.nongwoobio.co.kr", "crops": "tomato,pepper,radish,cabbage", "description": "Major Korean vegetable breeder.", "source": "curated"},
    {"name": "Asia Seed Korea", "country": "South Korea", "website": "https://www.asiaseed.co.kr", "crops": "tomato,pepper,radish,cabbage", "description": "Korean vegetable breeder.", "source": "curated"},
    {"name": "Koregon Seed", "country": "South Korea", "website": "", "crops": "tomato,pepper,melon", "description": "Korean vegetable seed breeder.", "source": "curated"},
    {"name": "Farm Hannong", "country": "South Korea", "website": "https://www.farmhannong.com", "crops": "rice,vegetables,crop protection", "description": "Korean agriculture / seed / agrochem company.", "source": "curated"},

    # --- India ---
    {"name": "Mahyco", "country": "India", "website": "https://www.mahyco.com", "crops": "cotton,tomato,pepper,okra,rice", "description": "Maharashtra Hybrid Seeds Company; major Indian breeder.", "source": "curated"},
    {"name": "Namdhari Seeds", "country": "India", "website": "https://www.namdhariseeds.com", "crops": "tomato,pepper,cucumber,watermelon,okra", "description": "Indian vegetable seed breeder, global exports.", "source": "curated"},
    {"name": "East-West Seed (India)", "country": "India", "website": "https://www.eastwestseed.com", "crops": "tomato,pepper,okra,gourd,watermelon", "description": "India operations of East-West Seed Group.", "source": "curated"},
    {"name": "Syngenta India", "country": "India", "website": "https://www.syngenta.co.in", "crops": "corn,vegetables,tomato", "description": "Indian arm of Syngenta Group.", "source": "curated"},
    {"name": "Kaveri Seed Company", "country": "India", "website": "https://www.kaveriseeds.in", "crops": "cotton,corn,rice,vegetables", "description": "Major Indian seed company.", "source": "curated"},
    {"name": "Nuziveedu Seeds", "country": "India", "website": "https://www.nuziveeduseeds.com", "crops": "cotton,corn,rice,vegetables", "description": "Major Indian seed company.", "source": "curated"},
    {"name": "Rasi Seeds", "country": "India", "website": "https://www.rasiseeds.com", "crops": "cotton,corn,tomato", "description": "Major Indian cotton and vegetable seed breeder.", "source": "curated"},
    {"name": "VNR Seeds", "country": "India", "website": "https://www.vnrseeds.com", "crops": "tomato,okra,watermelon,gourd", "description": "Indian vegetable seed breeder.", "source": "curated"},
    {"name": "Acsen HyVeg", "country": "India", "website": "https://www.acsenhyveg.com", "crops": "tomato,pepper,okra,watermelon", "description": "Indian vegetable seed breeder.", "source": "curated"},
    {"name": "Sakata Seed India", "country": "India", "website": "https://www.sakataseedindia.com", "crops": "tomato,watermelon,cauliflower", "description": "Indian arm of Sakata.", "source": "curated"},

    # --- Southeast Asia ---
    {"name": "East-West Seed Group", "country": "Thailand", "website": "https://www.eastwestseed.com", "crops": "tomato,pepper,watermelon,bitter gourd,okra", "description": "Tropical-vegetable specialist; HQ Thailand; major smallholder supplier.", "source": "curated"},
    {"name": "Chia Tai", "country": "Thailand", "website": "https://www.chiataigroup.com", "crops": "tomato,watermelon,pepper,corn", "description": "CP Group agri arm; vegetable seeds.", "source": "curated"},
    {"name": "Known-You Seed", "country": "Taiwan", "website": "https://www.knownyou.com", "crops": "tomato,watermelon,papaya,melon", "description": "Major tropical vegetable breeder.", "source": "curated"},

    # --- Turkey ---
    {"name": "May Agro", "country": "Turkey", "website": "https://www.mayagro.com", "crops": "tomato,pepper,cucumber,watermelon", "description": "Turkish vegetable seed breeder.", "source": "curated"},
    {"name": "Yuksel Seed", "country": "Turkey", "website": "https://www.yukseltohum.com", "crops": "tomato,pepper,cucumber,watermelon", "description": "Turkish vegetable seed breeder.", "source": "curated"},
    {"name": "Multi Tohum", "country": "Turkey", "website": "https://www.multitohum.com.tr", "crops": "tomato,pepper,cucumber", "description": "Turkish vegetable seed company.", "source": "curated"},

    # --- Poland / Eastern Europe ---
    {"name": "PlantiCo", "country": "Poland", "website": "https://www.plantico.pl", "crops": "tomato,cabbage,carrot,onion", "description": "Polish vegetable seed breeder.", "source": "curated"},
    {"name": "Spójnia Nochowo", "country": "Poland", "website": "https://www.spojnia.com.pl", "crops": "cabbage,carrot,radish,beetroot", "description": "Polish vegetable seed breeder.", "source": "curated"},
    {"name": "Torseed", "country": "Poland", "website": "https://www.torseed.pl", "crops": "vegetables,flowers,herbs", "description": "Polish seed distributor.", "source": "curated"},
    {"name": "PNOS Ożarów", "country": "Poland", "website": "https://www.pnos.pl", "crops": "vegetables,flowers", "description": "Polish seed distributor.", "source": "curated"},
    {"name": "Moravoseed", "country": "Czech Republic", "website": "https://www.moravoseed.com", "crops": "tomato,pepper,cabbage,carrot", "description": "Czech vegetable seed breeder.", "source": "curated"},
    {"name": "SEMO", "country": "Czech Republic", "website": "https://www.semo.cz", "crops": "tomato,pepper,cucumber,carrot", "description": "Czech vegetable seed breeder.", "source": "curated"},
    {"name": "ZKI Vegetable Crops Research", "country": "Hungary", "website": "https://www.zki.hu", "crops": "tomato,pepper,melon", "description": "Hungarian vegetable breeding institute / company.", "source": "curated"},

    # --- Russia / CIS ---
    {"name": "Gavrish", "country": "Russia", "website": "https://www.gavrish.ru", "crops": "tomato,cucumber,pepper", "description": "Russian vegetable seed breeder.", "source": "curated"},
    {"name": "Poisk Agro", "country": "Russia", "website": "https://www.semenasad.ru", "crops": "tomato,cabbage,carrot", "description": "Russian vegetable seed company.", "source": "curated"},
    {"name": "SeDeK", "country": "Russia", "website": "https://www.sedek.ru", "crops": "tomato,cucumber,pepper", "description": "Russian vegetable seed company.", "source": "curated"},

    # --- Australia / NZ ---
    {"name": "South Pacific Seeds", "country": "Australia", "website": "https://www.spsaust.com.au", "crops": "tomato,pepper,melon,cucumber", "description": "Australian/NZ vegetable seed breeder.", "source": "curated"},
    {"name": "Terranova Seeds", "country": "Australia", "website": "https://www.terranovaseeds.com.au", "crops": "vegetables", "description": "Australian vegetable seed supplier.", "source": "curated"},

    # --- Latin America ---
    {"name": "Sakata Seed Sudamerica", "country": "Brazil", "website": "https://www.sakata.com.br", "crops": "tomato,onion,broccoli,watermelon", "description": "Brazilian arm of Sakata.", "source": "curated"},
    {"name": "ISLA Sementes", "country": "Brazil", "website": "https://www.isla.com.br", "crops": "vegetables,herbs", "description": "Brazilian vegetable seed company.", "source": "curated"},
    {"name": "Agristar (Topseed)", "country": "Brazil", "website": "https://www.agristar.com.br", "crops": "tomato,pepper,lettuce,watermelon", "description": "Brazilian vegetable breeder.", "source": "curated"},
    {"name": "Hortec Mexico", "country": "Mexico", "website": "https://www.hortec.com.mx", "crops": "tomato,pepper,cucumber", "description": "Mexican vegetable seed distributor.", "source": "curated"},

    # --- Africa ---
    {"name": "East African Seed", "country": "Kenya", "website": "https://www.easeed.com", "crops": "tomato,onion,cabbage,kale", "description": "East African regional vegetable seed supplier.", "source": "curated"},
    {"name": "Starke Ayres", "country": "South Africa", "website": "https://www.starkeayres.com", "crops": "tomato,onion,cabbage,pepper", "description": "African regional seed company.", "source": "curated"},
    {"name": "Sakata Seed Southern Africa", "country": "South Africa", "website": "https://www.sakata.co.za", "crops": "tomato,onion,broccoli", "description": "Africa arm of Sakata.", "source": "curated"},

    # --- Canada ---
    {"name": "West Coast Seeds", "country": "Canada", "website": "https://www.westcoastseeds.com", "crops": "tomato,pepper,lettuce,herbs", "description": "BC-based organic seed supplier.", "source": "curated"},
    {"name": "Veseys Seeds", "country": "Canada", "website": "https://www.veseys.com", "crops": "tomato,pepper,flowers", "description": "PEI-based Canadian seed company.", "source": "curated"},
    {"name": "William Dam Seeds", "country": "Canada", "website": "https://www.damseeds.com", "crops": "tomato,pepper,lettuce", "description": "Ontario-based Canadian vegetable seed supplier.", "source": "curated"},
    {"name": "OSC Seeds", "country": "Canada", "website": "https://www.oscseeds.com", "crops": "tomato,pepper,flowers", "description": "Ontario Seed Company.", "source": "curated"},

    # --- UK ---
    {"name": "Thompson & Morgan", "country": "United Kingdom", "website": "https://www.thompson-morgan.com", "crops": "tomato,flowers,vegetables", "description": "UK-based seed and plant company, est. 1855.", "source": "curated"},
    {"name": "Mr Fothergill's", "country": "United Kingdom", "website": "https://www.mr-fothergills.co.uk", "crops": "tomato,flowers,vegetables", "description": "UK home-garden seed company.", "source": "curated"},
    {"name": "Kings Seeds", "country": "United Kingdom", "website": "https://www.kingsseeds.com", "crops": "tomato,pepper,vegetables", "description": "UK-based vegetable and flower seed supplier.", "source": "curated"},
    {"name": "Tozer Seeds", "country": "United Kingdom", "website": "https://www.tozerseeds.com", "crops": "celery,leek,parsnip,carrot", "description": "UK vegetable breeder, specialist in umbelliferous crops.", "source": "curated"},

    # --- More tomato-relevant specialists ---
    {"name": "Axia Vegetable Seeds", "country": "Netherlands", "website": "https://www.axiaseeds.com", "crops": "tomato,cucumber,pepper", "description": "Protected-cropping vegetable breeder.", "source": "curated"},
    {"name": "Vitalis Organic Seeds", "country": "Netherlands", "website": "https://www.vitalisorganic.com", "crops": "tomato,pepper,lettuce,cucumber", "description": "Organic arm of Enza Zaden.", "source": "curated"},
    {"name": "Clause Home Garden", "country": "France", "website": "https://www.clause-homegarden.com", "crops": "tomato,pepper,flowers", "description": "Home-garden division of HM.Clause.", "source": "curated"},
]
