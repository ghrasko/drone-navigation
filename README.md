Hraskó Gábor (2025.04.09., frissítve 2025.04.16.)

# GNSS nélküli vizuális navigáció szimulációja OSM alapon - Projekt terv

Ez a dokumentum összefoglalja a GNSS (műholdas navigáció) nélküli
drónnavigáció kihívásait és lehetséges megoldási módszereit. Ezt
követően bemutat egy konkrét, tanulási célú projekttervet, amely egy
egyszerűsített vizuális navigációs rendszer szimulációjára és
fejlesztésére összpontosít OpenStreetMap adatok alapján.

Ez a projekt lehetőséget nyújt a GNSS nélküli vizuális navigáció
alapelveinek gyakorlati megismerésére egy kontrollált, egyszerűsített
környezetben, fókuszálva a generalizációs képességre és a
**hasonlóság-tanuló architektúrákra**. A fokozatosan növekvő
komplexitású feladatok révén mélyebb megértés szerezhető az
adatfeldolgozás, modelltanítás, kiértékelés és a kapcsolódó algoritmusok
működéséről és kihívásairól.

**Tartalomjegyzék**

- Kihívások és módszerek
- A projekt célja és megközelítése
- Projekt terv
- Hol állunk?
- Módosítási utasítás

## Kihívások és módszerek

A modern drónok és autonóm rendszerek tájékozódása nagymértékben
támaszkodik a Globális Navigációs Műholdrendszerekre (GNSS, pl. GPS,
Galileo). Azonban számos helyzetben -- különösen katonai, de akár ipari
vagy városi környezetben is -- a GNSS jelek nem megbízhatóak vagy nem
elérhetőek zavarás (jamming), megtévesztés (spoofing), vagy egyszerűen a
fizikai környezet (pl. épületek, alagutak) árnyékoló hatása miatt. Ezért
kulcsfontosságú alternatív, autonóm navigációs módszerek fejlesztése.

A főbb GNSS-független navigációs technikák közé tartoznak:

-   **Inerciális Navigáció (INS/IMU):** Gyorsulásmérők és giroszkópok
    adataiból számítja a relatív elmozdulást, de a hibák idővel
    halmozódnak (drift).

-   **Vizuális Odometria (VO):** Kameraképek elemzésével becsüli a
    *relatív* elmozdulást és elfordulást képkockáról képkockára,
    jellegzetes pontok követésével. Nem használ globális térképet, ezért
    a hibája (drift) idővel halmozódik.

-   **SLAM (Simultaneous Localization and Mapping):** A mozgásbecslés
    mellett *egyidejűleg térképet is épít* a környezetről (jellemzően a
    követett pontok alapján). A lokalizáció során ehhez a saját maga
    által épített térképhez viszonyít, és képes a driftet csökkenteni
    hurokzárással (ismert hely felismerése).

-   **Terepegyeztetés (TRN/TERCOM):** A drón magasságmérőjének adatait
    (terep profilját) hasonlítja össze előre tárolt digitális domborzati
    modellekkel (DEM) a pozíció meghatározásához. Pontos referencia
    adatbázist igényel. Pontossága erősen függ a terep
    változatosságától; sík területek felett kevésbé hatékony.

-   **Jelenetegyeztetés (DSMAC):** A drón kamerája által látott képet
    hasonlítja össze előre tárolt referencia képekkel (pl. műholdképek,
    légifotók) a helyzetének azonosítására. Pontos referencia adatbázist
    igényel. Koncepciójában hasonlít az AI-alapú vizuális illesztésre,
    de klasszikus képkorrelációs technikákat használ a modern, tanult
    jellemzők helyett.

-   **Mesterséges Intelligencia (MI) Alkalmazása:** Az MI (különösen a
    **mélytanulás**) javíthatja a fenti módszerek robusztusságát,
    pontosságát (pl. jobb jellemzőfelismerés, intelligens szenzorfúzió).
    Képes általánosabb vizuális mintázatokat megtanulni.

-   **Szenzorfúzió:** Több különböző szenzor adatainak intelligens
    kombinálása a lehető legpontosabb és legmegbízhatóbb állapotbecslés
    érdekében. Két fő megközelítés létezik:

    -   **Klasszikus/Külső Fúzió:** Pl. Kalman-szűrők kombinálják a
        különböző (akár MI által előfeldolgozott) szenzorbecsléseket.

    -   **Integrált/MI-alapú Fúzió:** Multi-modális neurális hálózatok
        tanulják meg közvetlenül a szenzoradatok egyesítését.

## A projekt célja és megközelítése

Ez a projekt **nem** egy bevetésre kész, valós idejű drónnavigációs
rendszer létrehozását célozza. A fő cél a **tanulás és a koncepciók
megértése** egy egyszerűsített, kontrollált környezetben. A projekt
során egy specifikus megközelítést vizsgálunk:

-   **Vizuális helymeghatározás absztrakt térképek alapján:**
    OpenStreetMap (OSM) adatokból generálunk felülnézeti, sematikus
    térképeket. \*(Az OSM adatok használata valós műholdképek helyett
    több okból célszerű ebben a tanulási projektben:

    -   egyszerűbb az adatok programozott elérése és feldolgozása;

    -   a licencelés egyértelműbb;

    -   teljes kontrollunk van a megjelenítés (renderelés) felett;

    -   az absztraktabb, kontrolláltabb adatok miatt vélhetően
        egyszerűbb neurális hálózati modellek is elegendőek lehetnek,
        ami kisebb számítási (IT) erőforrásigényt jelent a tanítás és
        feldolgozás során;

    -   és mindez lehetővé teszi, hogy a hangsúlyt a navigációs
        algoritmusok és a gépi tanulási folyamatok megértésére
        helyezzük, nem pedig a valós képek feldolgozásának és
        adatbeszerzésének komplexitására.)\*

-   **Szimulált \"drónkép\":** A drón \"által látott\" képet szintén
    ebből az OSM világból generáljuk, kezdetben tökéletes egyezéssel,
    majd fokozatosan torzításokat (forgatás, méretezés) bevezetve.

-   **MI Modell:** Egy olyan neurális hálózatot (**jellemzően Sziámi
    hálózati architektúrát** vagy hasonló, párosításra optimalizált
    modellt) tanítunk, amely képes megtanulni a \"drónkép\" és a
    referencia térképrészletek közötti vizuális hasonlóságot. A cél,
    hogy a modell általános vizuális jellemzőket tanuljon meg.

-   **Generalizációs Képesség:** Kulcsfontosságú elvárás, hogy a
    rendszer képes legyen a lokalizációra olyan **referencia térképek
    alapján is, amelyeket a tanítás során nem látott**, pusztán a
    megtanult általános vizuális jellemzők és az inferencia során
    biztosított (új) térkép összevetésével.

-   **Fókusz:** Az adatfeldolgozási lánc (OSM -\> kép -\> modell
    bemenet), a **hasonlóság-tanuló** modell tanításának és
    kiértékelésének folyamata, valamint az alapvető vizuális
    lokalizációs algoritmusok megértése ebben a kontextusban.

Ezzel a megközelítéssel jól körüljárhatók a vizuális navigáció alapvető
kihívásai (pl. nézőpont-változás kezelése, jellemzők kinyerése,
párosítás) egy olyan rendszer keretében, amely képes új környezetekhez
adaptálódni.

## Projekt terv

A fent vázolt célok eléréséhez és a koncepciók gyakorlati kipróbálásához
a következő lépéseket javasoljuk:

### 0. Fázis: Előkészítés és eszközök megismerése

-   **0.1. Python környezet beállítása:** Szükséges könyvtárak
    telepítése (pl. osmnx, geopandas, shapely, rasterio, Pillow,
    matplotlib, tensorflow vagy pytorch, numpy). Virtuális környezet
    létrehozása javasolt.

-   **0.2. OSM adatlekérdezés kipróbálása:** Ismerkedés az osmnx
    könyvtárral. Próbálj meg letölteni úthálózatot, vízrajzot,
    épületeket egy kisebb, ismert területről.

-   **0.3. Képi megjelenítés kipróbálása:** Próbáld ki a letöltött OSM
    adatok egyszerű képpé alakítását matplotlib vagy Pillow
    segítségével. Kísérletezz színekkel, vonalvastagságokkal.

### 1. Fázis: Adat előkészítés és reprezentáció

-   **1.1. Célterületek kijelölése:** Válassz ki földrajzilag
    **elkülönülő** területeket az OSM-en belül:

    -   Tanító régió (pl. Magyarország egy része, kb. 10x10 km)

    -   Validációs régió (hasonló méretű, elkülönülő)

    -   Teszt régió (hasonló méretű, elkülönülő)

-   **1.2. OSM adatletöltő funkció:** Írj egy függvényt, ami adott
    terület határai alapján letölti a szükséges OSM elemeket.

-   **1.3. Térkép megjelenítési séma véglegesítése:** Döntsd el
    pontosan, milyen színekkel, vonalvastagságokkal, felbontással és
    léptékkel akarod a térképeket képpé alakítani. Legyen konzisztens!

-   **1.4. Térkép renderelő funkció:** Írj egy függvényt, ami a
    letöltött OSM vektoros adatokból és a séma alapján elkészíti a
    raszteres térképképet.

-   **1.5. Adatgeneráló pipeline:** Hozz létre egy folyamatot, ami a
    renderelt térképekből előállítja a tanításhoz szükséges adatokat:

    -   **1.5.1. Referencia térképek:** Generáld le a teljes
        térképképeket a tanító, validációs és teszt régiókra.

    -   **1.5.2. \"Tökéletes kamera\" nézetek:** Írj egy funkciót, ami a
        *tanító* és *validációs* referencia térképekből adott (x, y,
        orientáció) alapján kivágja a megfelelő kis méretű (pl.
        100x100 - 250x250 méteres területet lefedő) \"drón által
        látott\" képet (snippet). Alkalmazz jelentős átfedést (pl.
        50-75%).

    -   **1.5.3. Adathalmaz struktúra (párosításhoz):** Hozd létre a
        tanító és validációs adathalmazokat (több tízezer vagy százezer
        elem). A struktúra **párosításra** alkalmas legyen, pl.
        (snippet_1, snippet_2, címke_hasonlo_e) párok vagy
        (anchor_snippet, positive_snippet, negative_snippet) tripletek.
        Mentsd el ezeket feldolgozható formában.

### 2. Fázis: Vizuális lokalizációs modell (tökéletes kamera)

-   **2.1. Gépi tanulási keretrendszer kiválasztása:** Döntés
    TensorFlow/Keras vagy PyTorch mellett.

-   **2.2. Kezdeti modell architektúra tervezése:** Válassz egy
    **párosításra** alkalmas architektúrát, elsősorban **Sziámi
    hálózatot** (két párhuzamos, súlymegosztott CNN ág) a hasonlóság
    mérésére. Alternatívaként megfontolható egy CNN alapú
    jellemzőkinyerő és egy külső távolságmetrika.

-   **2.3. Adatbetöltő implementálása:** Írj kódot, ami betölti és
    előkészíti az 1.5.3. pontban generált párokat/tripleteket a modell
    számára.

-   **2.4. Tanítási ciklus implementálása:** Hozd létre a tanítási
    logikát: **loss function (pl. Contrastive Loss vagy Triplet Loss**
    sziámi hálózatokhoz), optimizer (pl. Adam), metrikák (pl. loss
    alakulása, esetleg pontosság a validációs párokon).

-   **2.5. Kezdeti modell tanítása:** Futtasd a tanítást a \"tökéletes
    kamera\" adatokon (átfedéssel, de még forgatás nélkül). Figyeld a
    tanulási görbéket, végezz validációt.

-   2.6. Alap lokalizációs funkció (illesztés): Írj egy függvényt, ami:

    1.  Vesz egy bemeneti \"drónképet\" (a *teszt* régióból).

    2.  Kinyeri annak jellemzővektorát a betanított modell (egyik ága)
        segítségével.

    3.  Végigpásztázza a *teszt referencia térképet*, minden pozícióból
        kinyerve a jellemzővektort.

    4.  Megkeresi azt a pozíciót a teszt térképen, ahol a jellemzővektor
        a leginkább hasonlít (legkisebb távolságú) a drónkép vektorához.
        Ez lesz a becsült hely.

-   **2.7. Kiértékelés (tökéletes kamera):** Futtasd a lokalizációs
    funkciót a *teszt* adathalmazon generált \"tökéletes kamera\"
    nézetekkel.

    -   **Számszerűsítés:** Mérd a lokalizációs hibát (pl. átlagos
        euklideszi távolság MAE/RMSE). Készíts statisztikát.

    -   **Vizuális ellenőrzés:** Rajzold fel a teszt referencia térképre
        a valódi és a becsült pozíciókat.

### 3. Fázis: Realizmus növelése (torzított kamera)

-   **3.1. \"Torzított kamera\" funkció implementálása:** Bővítsd az
    1.5.2. (és a tesztkép generáló) funkciót úgy, hogy véletlenszerű
    **forgatást** (0-360 fok) és esetleg kis **méretezési/zoom**
    változást is alkalmazzon a snippettek generálásakor.

-   **3.2. Adat augmentáció / újratanítás:** Használd a torzított
    képeket adat augmentációként a tanítás során (ajánlott), vagy
    tanítsd újra/finomhangold a modellt a torzított adatokkal generált
    párokon/tripleteken.

-   **3.3. Kiértékelés (torzított kamera):** Futtasd a lokalizációt a
    teszt adathalmazon a *torzított* \"drónképekkel\".

    -   **Számszerűsítés:** Végezd el ugyanazokat a hibaszámításokat,
        mint a 2.7. pontban. Hasonlítsd össze az eredményeket.

    -   **Vizuális ellenőrzés:** Ismét rajzold fel a valódi és becsült
        pozíciókat.

### 4. Fázis: Szimuláció és alkalmazás

-   **4.1. Random lokalizációs szimuláció (\"Hol vagyok?\"):**
    Implementáld az 1. szimulációs forgatókönyvet: véletlen pontra
    helyezd a drónt a *teszt térképen*, generáld a (torzított) nézetet,
    futtasd a lokalizációt (a teszt térképen keresve), mérd a hibát.
    Ismételd sokszor.

-   **4.2. Útvonalkövetési szimuláció (\"Merre mozgok?\"):**
    Implementáld az 2. szimulációs forgatókönyvet: szimulálj egy mozgó
    drónt a *teszt térképen*. Minden időlépésben generáld a (torzított)
    nézetet a valós pozícióból, futtasd a lokalizációt (a teszt térképen
    keresve), rögzítsd a valódi és becsült útvonalat.

-   **4.3. Eredmények vizualizálása:** Jelenítsd meg grafikusan a
    lokalizációs hibákat (pl. hisztogram) és a szimulált útvonalakat
    (valós vs. becsült a teszt térképen).

### 5. Fázis: Lehetséges további lépések (jövőkép)

-   *(Opcionális)* További torzítások bevezetése a \"kamerába\".

-   *(Opcionális)* Szimulált IMU adatok hozzáadása.

-   *(Opcionális)* Szenzorfúzió implementálása:

    -   **Egyszerűbb/Külső:** Pl. Kalman-szűrő használata a vizuális
        lokalizáció és az IMU predikció kombinálására.

    -   **Haladóbb/Integrált:** Multi-modális (pl. kép+IMU bemenetű)
        Sziámi-szerű hálózat tervezése.

-   *(Opcionális)* Valós műholdképek használatának vizsgálata.

-   *(Opcionális)* Off-nadir nézetek vizsgálata.

## Hol állunk?

2024.04.16-án a projekt 0. fázisának 0.3 lépésénél tartunk. Megtett lépések:

- Lépés 0.1: Felállítottam a környezetet. Végül Anaconda lett, mert az osmnx abban telepíthető biztonságosan.

- Lépés 0.2: Sikeresen lekérdeztem az útvonal, vízfelület és épület adatokat osmnx rutinokkal. Elmentettük képként egyenként és kombinálva. Elmentettük az adatokat egyedi OSM és GeoJSON fájlokba is.A teszt kódjaim az udemy_17.py és az osm_test.py.

- Lépés 0.3: A teszt kódok már egyszerű megjelenítést is alkalmaznak, de itt még komolyabb megjelenítéseket is próbálni kellhet. Túlzásokba azért ne essünk!

Következő lépések ezek lehetnek:

- Az utak és épületek megkülönböztetésére különböző színeket használhatunk. A vizek kékek, az rendben van. Néhány kép kör is van, azt nem tudom, hogy mi lehet. Az utakat nagyságuk alapján (van ilyen attribútum?) lehetne megkülönböztetni.

- Egy kicsit lehene a megjelenítést "szépíteni". Az openstreetmap.org alapnézete lehet példa. Az épületeket korrektebbül jeleníti meg, mint mi. Mi szerintem az épület körvonalát rajzoljuk ki (beleértve a belső udvarokat) vastag vonallal, az épületek belső része nem kitöltött. Inkább vékony vonal kellene és kitölteni az épület belsejét (megtartva az udvarokat). Ezt lehetne még próbálni (linewidth, facecolor, edgecolor stb.). Lehet, hogy ehhez speciális csomagok kellhetnek (contextily, folium, kepler.gl, plotly stb.)

- Letöltöttem Magyarország teljes térképét a geofabrik.de oldalról, de végül nem ezt a lokális hungary-latest.osm.pbf fájlt használjuk (bár a tesztprogram kiírásai erre utalnak), mert ahhoz pyosmium vagy osmium-tool kellene, vagy más PBF parser. Kipróbálhatnánk, mert minek töltsük le mindig ugyanazokat a területeket.

## Módosítási utasítás

- Lehetőleg csak a **Hogy állunk?** fejezetben végezzünk módosításokat: a projekt státuszt és a következő lépések terveit. Visszafele lehetőleg ne módosítsuk a dokumentumot, kivéve ha valami komoly hibát találunk.