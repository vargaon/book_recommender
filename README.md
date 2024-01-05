# Book Recommender

Projekt pro doporučování knížek na základě textového popisu (obsah, krátký úryvek) a historie hodnocení.

## Quick Start

Build and run docker containers:
```bash
$ make up
```
Database initialization:
```
$ docker exec -it br-backend bash
$ poetry run init-db
```

## Funkce

- vyhledání knížek za základě textové query
- vytvoření číselného hodnocení [1, 5] knížky uživatelem
- doporučení knížek pro uživatele
- doporučení podobných knížek

## Datová sada

Záznamy hodnocení knížek ze zdroje: https://github.com/zygmuntz/goodbooks-10k

Vlastnosti knížek včetně textových popisů ze zdroje: https://doi.org/10.5281/zenodo.4265096

## Metody doporučování

Content-based doporučení pomocí předtrénováného modelu BERT pro sémantickou analýzu textu. https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v2

Metoda využívá hodnocení uživatele jako reprezentaci užiatelského profilu, na základě kterého doporučuje nejpodobnější knížky, které uživatel již kladně hodnotil. Míra podobnosti knížek je vypočítána pomocí Cosinové podobnosti a řazení výsledného doporučení využívá Borda Count metody.

Uložení zakódovaných reprezentací knížek ve vektorové databázi pro rychlejší vyhledávání.

## Řešení

Client-Server architektura. 

Server ukládá data o hodnocení a knížkách do mongo databáze a umožňuje komunikaci s frontendovou částí pomocí REST-API. Hlavní funkcionalitou je doporučování knížek podle jejich textového popisu.

Client je implementován jako webové rozhraní pomocí REACT. Získává data z REST-API a umožňuje uživatelům snadněji interagovat s doporučovacím systémem. Uživatel může knížky vyhledávat pomocí atributů nebo textové query, vytvářet hodnocení a nechat si doporučit knížky podle již vytvořeného hodnocení.
