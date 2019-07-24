#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pywikibot
import ex_wd_021 as wd_utils
import sys
import time

Test = True

# Waiting time between write operations on commons.
# If you don't have a bot status, keep a WaitTime of 7 seconds between writing operations. If you are using an account with a bot status, WaitTime can be reduced to 0 or 1 second
WaitTime = 7

wdsite = pywikibot.Site("wikidata", "wikidata")
wdrepo = wdsite.data_repository()
targetsite = pywikibot.Site('commons', 'commons')
verzameltext = ''

CLAIM_COMMONS_LINK_AFBEELDING_GEBOUW_INSTELLING = u'P18'
CLAIM_COMMONS_LINK_LOGO_INSTELLING = u'P154'   # (backup voor afbeelding gebouw?)
CLAIM_NAAM_CATEGORY_INSTELLING = u'P373'
CLAIM_SOORT_INSTELLING = u'P31'
CLAIM_URL_HOMEPAGE_INSTELLING = u'P856'

def verwerkcategorie(naamcategorie):
    verzameltext = ''
    localnaamcategorie = naamcategorie.replace("<NAAM INSTELLING>", naam_instelling)
    localnaamcategorie = localnaamcategorie.replace(' ', '_') 
    naaminputbestand = 'Category_'+localnaamcategorie+'.txt'
    if Test:
        naamoutputpagina = 'Category:RonnieV'+localnaamcategorie
    else:
        naamoutputpagina = 'Category:'+localnaamcategorie
    naamoutputpagina = naamoutputpagina.replace("NAAM_INSTELLING", naam_instelling).replace('_', ' ')
    naam_instelling_with_underlines = naam_instelling.replace(' ', '_')
    aanduiding_soort_instelling = ''
    if 'bibliotheek' in soort_instelling:
        aanduiding_soort_instelling = ' by library'
    if 'museum' in soort_instelling:
        aanduiding_soort_instelling = ' by museum'
    print(f'----- {naaminputbestand} ----')
    verzameltext += '----- '+naaminputbestand+' ----\n' 
    print(f'----- {naamoutputpagina} ----')
    verzameltext += f'----- '+naamoutputpagina+' ----\n' 
    with open(naaminputbestand, 'rt', encoding='utf-8') as f:
        text = ''
        for x in f:
#            x = x.replace("<NAAM INSTELLING LOKAAL>", localnaaminstelling)
            x = x.replace("<NAAM INSTELLING WITH UNDERLINES>", naam_instelling_with_underlines)
            x = x.replace("<NAAM INSTELLING>", naam_instelling)
            x = x.replace("<NAAM CATEGORY INSTELLING>", naam_category_instelling)
            x = x.replace("<NAAM AFBEELDING>", naam_afbeelding)
            x = x.replace("<SOORT INSTELLING>", aanduiding_soort_instelling)
            x = x.replace("<URL INSTELLING>", url_homepage)
            text += x     
    f.close()  
    verzameltext += f'{text}\n' 
    page = pywikibot.Page(targetsite, naamoutputpagina )
    if page.text != text:
        nieuw = (page.text == u'')
        page.text = text
        if nieuw:
            print ('---- pagina wordt aangemaakt -----')
            page.save(u"Categorie aangemaakt voor "+ naam_instelling)
        else:
            page.save(u"Categorie bijgewerkt op basis van basissjabloon of data")
        time.sleep(WaitTime)
    print('---------------------------------------')
    verzameltext += '---------------------------------------\n'
    return( verzameltext ) 

def verwerksjabloon(naamsjabloon, subpage = '', nonlatin = False):
    verzamelregel = ''
    verzameltext  = ''
    if Test:
        naamoutputpagina = 'Template:RonnieV'+naam_instelling
    else:
        naamoutputpagina = 'Template:'+naam_instelling
    if subpage == '':
        naaminputbestand = 'Template_'+naamsjabloon
        localnaaminstelling = naam_instelling
    else:
        localnaaminstelling = 'XXXXXXXXX'
        naaminputbestand = 'Template_'+naamsjabloon+'_'+subpage
        naamoutputpagina += '/'+subpage
        print (subpage, localnaaminstelling, naam_instelling)
        if len(subpage) == 2:
            verzamelregel = f'-->[{{{{fullurl:Template:<NAAM INSTELLING>/{subpage}}}}} {{{{ucfirst:{{{{#language:{subpage}}}}}}}}}]&nbsp;| <!--'
        try:
            localnaaminstelling = item.labels[subpage]
        except:
            if nonlatin:
                print(f'----- Geen vertaling beschikbaar voor {subpage} ----')
                return ('')
            localnaaminstelling = naam_instelling
        print (subpage, nonlatin, localnaaminstelling, naam_instelling)
    naaminputbestand += '.txt'         
    
    print(f'----- {naaminputbestand} ----')
    verzameltext += '----- '+naaminputbestand+' ----\n' 
    print(f'----- {naamoutputpagina} ----')
    verzameltext += '----- '+naamoutputpagina+' ----\n' 
    with open(naaminputbestand, 'rt', encoding='utf-8') as f:
        text = ''
        for x in f:
            x = x.replace("<NAAM INSTELLING LOKAAL>", localnaaminstelling)
            x = x.replace("<NAAM INSTELLING>", naam_instelling)
            x = x.replace("<NAAM CATEGORY INSTELLING>", naam_category_instelling)
            x = x.replace("<NAAM AFBEELDING>", naam_afbeelding)
            x = x.replace("<URL INSTELLING>", url_homepage)
            text += x     
    f.close()  
    verzameltext += f'{text}\n' 
    page = pywikibot.Page(targetsite, naamoutputpagina )
    if page.text != text:
        nieuw = (page.text == u'')
        page.text = text 
        if nieuw:
            print ('---- pagina wordt aangemaakt -----')
            page.save(u"Sjabloon aangemaakt voor "+ naam_instelling)
        else:
            page.save(u"Sjabloon bijgewerkt op basis van basissjabloon of aangepaste data")
        time.sleep(WaitTime)
    print('---------------------------------------')
    verzameltext += f'---------------------------------------\n'
    return (verzameltext, verzamelregel) 

if len(sys.argv) > 1:
    if sys.argv[1][0:1] == 'Q':
        qcode = sys.argv[1]
    else: 
        qcode = 'Q'+sys.argv[1]
else:
    print ('Geef het itemnummer in Wikidata voor de instelling mee, bijvoorbeeld')
    print ('py template_creator.py 1526131')
    exit()        
    
def GetValue(item, claimid):    
    try:
        result = item.claims.get(claimid)[0].getTarget()
    except:
        result = u''
    return result
    
item = pywikibot.ItemPage(wdrepo, qcode)
item.get(get_redirect=True)
try:
    naam_instelling = item.labels['nl']
except:
    try:
        naam_instelling = item.labels['en'] 
    except:
        naam_instelling = u''
naam_category_instelling = GetValue(item, CLAIM_NAAM_CATEGORY_INSTELLING)
link_afbeelding = GetValue(item, CLAIM_COMMONS_LINK_AFBEELDING_GEBOUW_INSTELLING)
if link_afbeelding == u'': 
    link_afbeelding = GetValue(item, CLAIM_COMMONS_LINK_LOGO_INSTELLING) 
naam_afbeelding = str(link_afbeelding)[10:-2]           
url_homepage = GetValue(item, CLAIM_URL_HOMEPAGE_INSTELLING)
soort_instelling = wd_utils.get_text_for_claim(item, CLAIM_SOORT_INSTELLING)
                      
verzameltext += f'Naam instelling:  {naam_instelling}\n'                      
verzameltext += f'Naam categorie:   {naam_category_instelling}\n'                      
verzameltext += f'Link afbeelding:  {link_afbeelding}\n'                      
verzameltext += f'Naam afbeelding:  {naam_afbeelding}\n'                      
verzameltext += f'Url instelling :  {url_homepage}\n'                      
verzameltext += f'Soort instelling: {soort_instelling}\n'                      
print ('Naam instelling:  ', naam_instelling)
print ('Naam categorie:   ', naam_category_instelling, "in", CLAIM_NAAM_CATEGORY_INSTELLING)
print ('Link afbeelding:  ', link_afbeelding, "in", CLAIM_COMMONS_LINK_AFBEELDING_GEBOUW_INSTELLING)
print ('Naam afbeelding:  ', naam_afbeelding)
print ('Url instelling:   ', url_homepage, "in", CLAIM_URL_HOMEPAGE_INSTELLING)
print ('Soort instelling: ', soort_instelling, "in", CLAIM_SOORT_INSTELLING)
print (verzameltext)

if naam_instelling == '' or naam_category_instelling == '' or naam_afbeelding == '' or url_homepage == '':
    print('Niet alle benodigde gegevens zijn beschikbaar. Zie het lijstje hierboven voor de ontbrekende waarden in Wikidata')
    exit()
    
verzameltext += verwerksjabloon("NAAM_INSTELLING")
verzameltext += verwerksjabloon("NAAM_INSTELLING","doc")
verzameltext += verwerksjabloon("NAAM_INSTELLING","layout")
verzameltext += verwerksjabloon("NAAM_INSTELLING","lang")
verzameltext += verwerksjabloon("NAAM INSTELLING","de")
verzameltext += verwerksjabloon("NAAM INSTELLING","en")
verzameltext += verwerksjabloon("NAAM INSTELLING","fr")
#verzameltext += verwerksjabloon("NAAM INSTELLING","mk", nonlatin = True)
verzameltext += verwerksjabloon("NAAM INSTELLING","nl")

verzameltext += verwerkcategorie("Collections_from_NAAM_INSTELLING")
verzameltext += verwerkcategorie("Media_contributed_by_NAAM_INSTELLING")

file1 = open(qcode+" "+naam_instelling+".txt","w", encoding='utf8')
file1.write(verzameltext) 
file1.close() 