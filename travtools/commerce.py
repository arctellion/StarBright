import numpy as np
import travtools.converters as cnv
import travtools.system as sy
import travtools.dice as dd

## speculative cargo price
def spec_price(n, t):
    """
    Generate base cost of speculative cargo for a given set of trade codes n, with tech level t.
    """
    cost = 3000
    cost += cnv.ext_dec(t) * 100
    
    for i in range(len(n)):
        if n[i] == 'Ag':
            cost -= 1000
        if n[i] == 'As':
            cost -= 1000
        if n[i] == 'Ba':
            cost += 1000
        if n[i] == 'De':
            cost += 1000
        if n[i] == 'Fl':
            cost += 1000
        if n[i] == 'Hi':
            cost -= 1000
        if n[i] == 'Ic':
            cost += 0
        if n[i] == 'In':
            cost -= 1000
        if n[i] == 'Lo':
            cost += 1000
        if n[i] == 'Na':
            cost += 0
        if n[i] == 'Ni':
            cost += 1000
        if n[i] == 'Po':
            cost -= 1000
        if n[i] == 'Ri':
            cost += 1000
        if n[i] == 'Va':
            cost += 1000

    return cost

def trade_goods(n):
    """
    Generate a random Trade good type given a list of trade codes n.
    """
    goods = ""
    l = len(n) 
    if l > 1:
        z = np.random.randint(0, (l-1))
    else: 
        z = 0
    i = dd.die_roll()-1
    j = dd.die_roll()-1
    #print('tg:{};l:{};z{};i{};j{}'.format(n,l,z,i,j))
    if n[z] == 'Ag':
        goods = ag_ga[i][j]
    if n[z] == 'As':
        goods = ast[i][j]
    if n[z] == 'Ba':
        goods = na[i][j]
    if n[z] == 'De':
        goods = de[i][j]
    if n[z] == 'Fl':
        goods = fl[i][j]
    if n[z] == 'Hi':
        goods = na[i][j]
    if n[z] == 'Ic':
        goods = ic[i][j]
    if n[z] == 'In':
        goods = ind[i][j]
    if n[z] == 'Lo':
        goods = na[i][j]
    if n[z] == 'Na':
        goods = na[i][j]
    if n[z] == 'Ni':
        goods = na[i][j]
    if n[z] == 'Po':
        goods = po[i][j]
    if n[z] == 'Ri':
        goods = ri[i][j]
    if n[z] == 'Va':
        goods = va[i][j]
    return goods

def sell_price(n, d, b = 0, t = 0):
    """
    takes arguments of a Cargo Code (n) in the format: E - Hi In Na Va Cr3,400, Brokers Skill default is 0, no broker (b), Any Trader Roll default to 0, no trader (t) and Destination UWP (d) in the format A430311-B, it returns the sell price of the goods, taking brokering into account.
    """
    price = 5000
    if b > 0:
        if b > 8:
            b = 8
        b = int(round(b/2))
    if t > 0:
        if t > 6:
            t = 6
    dtech = cnv.ext_dec(d[8])
    dtrade = sy.fun_trade(d).split()
    stech = cnv.ext_dec(n[0])
    strade = n[3:n.find("Cr")].split()
    #print("DestTech: {}; DestTrade: {}; SourceTech: {}; SourceTrade: {}; Broker: {}; TradeRoll: {}".format(dtech,dtrade,stech,strade,b,t))
    ptech = (stech - dtech)*0.1
    pr = 0
    for i in range(len(strade)):
        if strade[i] == 'Ag':
            for x in range(len(dtrade)):
                if dtrade[x] == 'Ag':
                    pr += 1000
                if dtrade[x] == 'As':
                    pr += 1000
                if dtrade[x] == 'De':
                    pr += 1000
                if dtrade[x] == 'Hi':
                    pr += 1000
                if dtrade[x] == 'In':
                    pr += 1000
                if dtrade[x] == 'Ri':
                    pr += 1000
                if dtrade[x] == 'Va':
                    pr += 1000
        if strade[i] == 'As':
            for x in range(len(dtrade)):
                if dtrade[x] == 'As':
                    pr += 1000
                if dtrade[x] == 'In':
                    pr += 1000
                if dtrade[x] == 'Ri':
                    pr += 1000
                if dtrade[x] == 'Va':
                    pr += 1000
        if strade[i] == 'Ba':
            for x in range(len(dtrade)):
                if dtrade[x] == 'In':
                    pr += 1000
        if strade[i] == 'De':
            for x in range(len(dtrade)):
                if dtrade[x] == 'De':
                    pr += 1000
        if strade[i] == 'Fl':
            for x in range(len(dtrade)):
                if dtrade[x] == 'Fl':
                    pr += 1000
                if dtrade[x] == 'In':
                    pr += 1000
        if strade[i] == 'Hi':
            for x in range(len(dtrade)):
                if dtrade[x] == 'Hi':
                    pr += 1000
        if strade[i] == 'Ic':
            pr += 0
        if strade[i] == 'In':
            for x in range(len(dtrade)):
                if dtrade[x] == 'Ag':
                    pr += 1000
                if dtrade[x] == 'As':
                    pr += 1000
                if dtrade[x] == 'De':
                    pr += 1000
                if dtrade[x] == 'Fl':
                    pr += 1000
                if dtrade[x] == 'Hi':
                    pr += 1000
                if dtrade[x] == 'In':
                    pr += 1000
                if dtrade[x] == 'Ri':
                    pr += 1000
                if dtrade[x] == 'Va':
                    pr += 1000
        if strade[i] == 'Lo':
            pr += 0
        if strade[i] == 'Na':
            for x in range(len(dtrade)):
                if dtrade[x] == 'As':
                    pr += 1000
                if dtrade[x] == 'De':
                    pr += 1000
                if dtrade[x] == 'Va':
                    pr += 1000
        if strade[i] == 'Ni':
            pr += 0
        if strade[i] == 'Po':
            for x in range(len(dtrade)):
                if dtrade[x] == 'Ag':
                    pr -= 1000
                if dtrade[x] == 'Hi':
                    pr -= 1000
                if dtrade[x] == 'In':
                    pr -= 1000
                if dtrade[x] == 'Ri':
                    pr -= 1000
        if strade[i] == 'Ri':
            for x in range(len(dtrade)):
                if dtrade[x] == 'Ag':
                    pr += 1000
                if dtrade[x] == 'De':
                    pr += 1000
                if dtrade[x] == 'Hi':
                    pr += 1000
                if dtrade[x] == 'In':
                    pr += 1000
                if dtrade[x] == 'Ri':
                    pr += 1000
        if strade[i] == 'Va':
            for x in range(len(dtrade)):
                if dtrade[x] == 'As':
                    pr += 1000
                if dtrade[x] == 'In':
                    pr += 1000
                if dtrade[x] == 'Va':
                    pr += 1000
    br = {-5: 0.4, -4: 0.5, -3: 0.7, -2: 0.8, -1: 0.9, 0: 1.0, 1: 1.1, 2: 1.2, 3: 1.3, 4: 1.5, 5: 1.7, 6: 2.0, 7: 3.0, 8: 4.0}
    if b > 0:
        if t > 0:
            broker = t - dd.die_roll() + b
            if broker > 8:
                broker = 8
            if broker < -5:
                broker = -5
            pbrk = br[broker]
        else:
            broker = dd.flux() + b 
            if broker > 8:
                broker = 8
            if broker < -5:
                broker = -5
            pbrk = br[broker]
    else:
        broker = dd.flux()
        if broker > 8:
            broker = 8
        if broker < -5:
            broker = -5
        pbrk = br[broker]
    price = price + pr
    tpr = int(price * ptech)
    #print('price: {}; tech effect: {}; {}; broker: {}'.format(price,ptech,tpr, pbrk))
    price += tpr
    #print('Base Price: {}\n'.format(price))
    if price < 0:
        price = 0
    price = int(price * pbrk)
    return price

#Trade Goods Data
ag_ga = [['Bulk Protein','Bulk Carbs','Bulk Fats','Bulk Pharma','Livestock', 'Seedstock'], #Raws
['Flavoured Waters','Wines','Juices','Nectars','Decoctions','Drinkable Lymphs'], #Consumables
['Health Foods','Nutraceuticals','Fast Drug','Painkillers','Antiseptic','Antibiotics'], #Pharma
['Incenses','Iridescents','Photonics','Pigments','Noisemakers','Soundmakers'], #Novelties
['Fine Furs','Meat Delicacies','Fruit Delicacies','Candies','Textiles','Exotic Sauces'], #Rares
['As*','De*','Fl*','Ic*','Na*','In*']] #Imbalances
ag_fa = [['Bulk Woods','Bulk Pelts','Bulk Herbs','Bulk Spices','Bulk Nitrates','Foodstuffs'], #Raws
['Flowers','Aromatics','Pheromones','Secretions,''Adhesives','Novel Flavorings'], #Consumables
['Antifungals','Antivirals','Panacea','Pseudomones','Anagathics','Slow Drug'], #Pharma
['Strange Seeds','Motile Plants','Reactive Plants','Reactive Woods','IR Emitters','Lek Emitters'], #Novelties
['Spices','Organic Gems','Flavorings','Aged Meats','Fermented Fluids','Fine Aromatics'], #Rares
['Po*','Ri*','Va*','Ic*','Na*','In*']] #Imbalances
ast = [['Bulk Nitrates','Bulk Carbon','Bulk Iron','Bulk Copper','Radioactive Ores','Bulk Ices'], #Raws
['Ores','Ices','Carbons','Metals','Uranium','Chelates'], #Samples
['Platinum','Gold','Gallium','Silver','Thorium','Radium'], #Valuta
['Unusual Rocks','Fused Metals','Strange Crystals','Fine Dusts','Magnetics','Light-Sensitives'], #Novelties
['Gemstones','Alloys','Iridium Sponge','Lanthanum','Isotopes','Anti-Matter'], #Rares
['Ag*','De*','Na*','Po*','Ri*','Ic*']] #Imbalances
de = [['Bulk Nitrates','Bulk Minerals','Bulk Abrasives','Bulk Particulates','Exotic Fauna','Exotic Flora'], #Raws
['Archeologicals','Fauna','Flora','Minerals','Ephemerals','Polymers'], #Samples
['Stimulants','Bulk Herbs','Palliatives','Pheromones','Antibiotics','Combat Drug'], #Pharma
['Envirosuits','Reclamation Suits','Navigators','Dupe Masterpieces','ShimmerCloth','ANIFX Blocker'], #Novelties
['Excretions','Flavorings','Nectars','Pelts','ANIFX Dyes','Seedstock'], #Rares
['Pheromones','Artifacts','Sparx','Repulsant','Dominants','Fossils']] #Uniques
fl = [['Bulk Carbon','Bulk Petros','Bulk Precipitates','Exotic Fluids','Organic Polymers','Bulk Synthetics'], #Raws
['Archeologicals','Fauna','Flora','Germanes','Flill','Chelates'], #Samples
['Antifungals','Antivirals','Palliatives','Counter-prions','Antibiotics','Cold Sleep Pills'], #Pharma
['Silanes','Lek Emitters','Aware Blockers','Soothants','Self-Solving Puzzles','Fluidic Timepieces'], #Novelties
['Flavorings','Unusual Fluids','Encapsulants','Insidiants','Corrosives','Exotic Aromatics'], #Rares
['In*','Ri*','Ic*','Na*','Ag*','Po*']] #Imbalances
ic = [['Bulk Ices','Bulk Precipitates','Bulk Ephemerals','Exotic Flora','Bulk Gases','Bulk Oxygen'], #Raws
['Archeologicals','Fauna','Flora','Minerals','Luminescents','Polymers'], #Samples
['Antifungals','Antivirals','Palliatives','Restoratives','Antibiotics','Antiseptics'], #Pharma
['Heat Pumps','Mag Emitters','Percept Blockers','Silanes','Cold Light Blocks','VHDUS Blocker'], #Novelties
['Unusual Ices','Cryo Alloys','Rare Minerals','Unusual Fluids','Cryogems','VHDUS Dyes'], #Rares
['Fossils','Cryogems','Vision Suppressant','Fission Suppressant','Wafers','Cold Sleep Pills']] #Uniques
na = [['Bulk Abrasives','Bulk Gases','Bulk Minerals','Bulk Precipitates','Exotic Fauna','Exotic Flora'], #Raws
['Archeologicals','Fauna','Flora','Minerals','Ephemerals','Polymers'], #Samples
['Branded Tools','Drinkable Lymphs','Strange Seeds','Pattern Creators','Pigments','Warm Leather'], #Novelties
['Hummingsand','Masterpieces','Fine Carpets','Isotopes','Pelts','Seedstock'], #Rares
['Masterpieces','Unusual Rocks','Artifacts','Non-Fossil Carca','Replicating Clays','ANIFX Emitter'], #Uniqies
['Ag*','Ri*','In*','Ic*','De*','Fl*']] #Imbalances
ind = [['Electronics','Photonics','Magnetics','Fluidics','Polymers','Gravitics'], #Manufactureds
['Obsoletes','Used Goods','Reparables','Radioactives','Metals','Sludges'], #Scrap/Waste
['Biologics','Mechanicals','Textiles','Weapons','Armor','Robots'], #Manufactureds
['Nostrums','Restoratives','Palliatives','Chelates','Antidotes','Antitoxins'], #Pharma
['Software','Databases','Expert Systems','Upgrades','Backups','Raw Sensings'], #Data
['Disposables','Respirators','Filter Masks','Combination','Parts ','Improvements']] #Consumables
po = [['Bulk Nutrients','Bulk Fibers','Bulk Organics','Bulk Minerals','Bulk Textiles','Exotic Flora'], #Raws
['Art','Recordings','Writings','Tactiles','Osmancies','Wafers'], #Entertainments
['Strange Crystals','Strange Seeds','Pigments','Emotion Lighting','Silanes','Flora'], #Novelties
['Gemstones','Antiques','Collectibles','Allotropes','Spices','Seedstock'], #Rares
['Masterpieces','Exotic Flora','Antiques','Incomprehensibles','Fossils','VHDUS Emitter'], #Uniques
['In*','Ri*','Fl*','Ic*','Ag*','Va*']] #Imbalances
ri = [['Bulk Foodstuffs','Bulk Protein','Bulk Carbs','Bulk Fats','Exotic Flora','Exotic Fauna'],
['Echostones','Self-Defenders','Attractants','Sophont Cuisine','Sophont Hats','Variable Tattoos'],
['Branded Foods','Branded Drinks','Branded Clothes','Flavored Drinks','Flowers','Music'],
['Delicacies','Spices','Tisanes','Nectars','Pelts','Variable Tattoos'],
['Antique Art','Masterpieces','Artifacts','Fine Art','Meson Barriers','Famous Wafers'],
['Edutainments','Recordings','Writings','Tactiles','Osmancies','Wafers']]
va = [['Bulk Dusts','Bulk Minerals','Bulk Metals','Radioactive Ores','Bulk Particulates','Ephemerals'], #Raws
['Branded Vacc Suits','Awareness Pinger','Strange Seeds','Pigments','Unusual Minerals','Exotic Crystals'], #Novelties
['Branded Oxygen','Vacc Suit Scents','Vacc Suit Patches','Branded Tools','Holo-Companions','Flavored Air'], #Consumables
['Vacc Gems','Unusual Dusts','Insulants','Crafted Devices','Rare Minerals','Catalysts'], #Rares
['Archeologicals','Fauna','Flora','Minerals','Ephemerals','Polymers'], #Samples
['Obsoletes','Used Goods','Reparables','Plutonium','Metals','Sludges']] #Scrap/Waste

##trade Generation
def trade_gds(n, skill = {'Steward':0, 'Admin':0, 'Streetwise':0, 'Liaison':0}, days = 7):
    """
    Generate trade goods for a given UWP. Using skills, skill, where skill is {Steward, Admin, Streetwise, Liaison} defaults = 0, for a given number of days default = 7.
    """
    
    pop = cnv.ext_dec(n[4])
    tech = n[8]
    trade = sy.fun_trade(n)
    trades = trade.split()

    admin = skill['Admin']
    street = skill['Streetwise']
    steward = skill['Steward']
    liaise = skill['Liaison']

    high = dd.flux() + pop + steward
    mid = dd.flux() + pop + admin
    low = dd.flux() + pop + street
    if high < 0: 
        high = 0
    if mid < 0:
        mid = 0
    if low < 0:
        low = 0

    i = 0
    freight = ['None']*days
    cargo = ['None']*days
    frttot = 0
    while i < days:
        amount = dd.flux() + pop
        if amount < 0:
            amount = 0
        frttot += amount
        frtprc = amount * 1000
        freight[i] = '{}dt of {} at Cr{:,}'.format(amount,trade_goods(trades),frtprc)
        cargo[i] = '100dt of ' + trade_goods(trades)
        i += 1
    frt = "\n|=> ".join(freight)
    cgo = "\n|=> ".join(cargo)
    trd = "During the last {} days you find:\n".format(days)
    trd = trd + "* High Passengers: {} at Cr10,000 +/- Cr1,000 depending on demand\n".format(high)
    trd = trd + "* Middle Passengers: {} at Cr8,000 +/- Cr1,000 depending on demand\n".format(mid)
    trd = trd + "* Low Passengers: {} at Cr1,000 +/- Cr100 depending on demand\n---\n".format(low)
    trd = trd + "* Freight totalling {}dt in lots:\n|=> {}\n".format(frttot, frt)
    trd = trd + "* Spec Cargo available:\n|=> {}\n".format(cgo)
    tc = " ".join(map(str, trades))
    cost = spec_price(trades, tech)
    crgo = "{} - {} Cr{:,}".format(tech, tc, cost)
    trd = trd + "|===> Spec Cargo Cost: {} per dt.".format(crgo)

    return trd