"""

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import os, re, sys, string, json, random, base64

try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser

convert_special_characters = HTMLParser()
dlg = xbmcgui.Dialog()

from resources.lib.modules.common import *

art = 'special://home/addons/script.j1.artwork/lib/resources/art/'

#==========================================================================================================

channellist=[
        ("[B]Campeonato de Peso Completo Perros del Mal: LPE, Edinburg, TX (12/19/20)[/B]", "GRTYSYyNjpk", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: THE BEST FIGHTS OF 2019[/B]", "Yu45anVWp1I", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: AUTO LUCHAS AAA: Episode 6 (11/29/2020)[/B]", "IJIn9Hr6mLs", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: AUTO LUCHAS AAA: Episode 5 (11/22/2020)[/B]", "cCBD7KDFQgw", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: AUTO LUCHAS AAA: Episode 4 (11/15/2020)[/B]", "qFwPrNPt4fw", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter LIVE EPISODIO 4 (5/9/2020)[/B]", "25PVP1ndAvM", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter LIVE EPISODIO 3 (5/2/2020)[/B]", "IBBNfskn3bU", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter LIVE EPISODIO 2 (4/25/2020)[/B]", "dmStZtQJ9Ow", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter LIVE EPISODIO 1 (4/18/2020)[/B]", "f61BZMsrSJ0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Cabelleras vs Cabelleras: Shotas vs Oficiales (11/15/2020)[/B]", "33QveFfesJg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: AUTO LUCHAS AAA: Episode 3 (11/8/2020)[/B]", "pwkxUrrY6dc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: AUTO LUCHAS AAA: Episode 2 (10/31/2020)[/B]", "sdaYcdR6lKY", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: AUTO LUCHAS AAA: THE RETURN OF AAA 10/25/2020[/B]", "myAaqtweHJE", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Los MOMENTOS MAS ESPECTACULARES de LUCHA FIGHTER: Programa 1[/B]", "aD6AyKM_mdM", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Los MOMENTOS MAS ESPECTACULARES de LUCHA FIGHTER: Programa 2[/B]", "4WUQmJ1neq8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Los MOMENTOS MAS ESPECTACULARES de LUCHA FIGHTER: Programa 3[/B]", "uA0u2ktoA80", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: GRAN FINAL de LUCHA FIGHTER - Los MEJORES MOMENTOS[/B]", "VcDFfU8ENPs", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: TRIPLEMANIA XXVII FIGHT NIGHT 8/3/2019[/B]", "kUaE9eI_8s8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre Live: Noche De Leyendas - Brooklyn NY 10/6/2017[/B]", "QPvdaqIDUzw", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: STAR BATTLE JAPAN, Lucha Libre AAA in TOKIO 10/3/2020[/B]", "CIQ4bGTcIQc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha iAqui esta la Lucha (Septiembre 4, 2020)[/B]", "_VeCe1lT9eQ", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: MASCARA VS CABELLERA FIGHT: PSYCHO CLOWN vs PAGANO 2016[/B]", "9ryJVHl5KV0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]CMLL Homenaje a Dos Leyendas la Rivalidad de los Dinamita y los Perros 8/14/20[/B]", "CllSKSJ_ojE", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: COPA TRIPLEMANIA XXIV 8/17/2020[/B]", "S9tk_oWLDoU", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: REINA DE REINAS 2020[/B]", "n0bU1SO35pg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Las Luchas Mas Espectaculares[/B]", "schuvcjfdTk", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]CABELLERA VS CABELLERA: LADY MARAVILLA Vs BIG MAMI[/B]", "6sH8sWikKPc", 801, "LUCHA, WOMEN", art+'dvd.jpg', fanart),
        ("[B]Canek vs L.A. Park vs Dr. Wagner Jr, Campeonato Mundial IWL [/B]", "ExlWxCYQe6I", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Faccion INGOBERNABLE Vs LUCHA BROTHERS y PSYCHO CLOWN 2020[/B]", "Ke4kDHRkCv0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Penta Zero M y Daga vs L.A. Park y Rey Escorpion, AULL 2017[/B]", "XrWO_Cv3KAc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA N AEW: Kenny Omega y The Young Bucks Vs Lucha Brothers y Laredo Kid 2019[/B]", "El43Ch1ybc0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: ALBERTO EL PATRON VS BRIAN CAGE 2015[/B]", "R44Tsk3NZ-A", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha AAA vs Elite 7/18/2020[/B]", "gEzyH9oIUIY", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lady Shani, Hiedra y Mamba vs Keira, Estrella Divina y Lady Maravilla 2019[/B]", "kASaxdIP8XE", 801, "LUCHA, WOMEN", art+'dvd.jpg', fanart),
        ("[B]International Wrestling League #9 (7/14/20)[/B]", "HbD6XMJ1dL8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]International Wrestling League #8 (7/12/20)[/B]", "W7cGqTrTVmg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]International Wrestling League #7 (7/11/20)[/B]", "OKyoGK40p4c", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]International Wrestling League #6 (7/9/20)[/B]", "Z-lIM5oN9e0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]International Wrestling League #5 (7/9/20)[/B]", "YAS5Nz9ouCs", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA Las MEJORES LUCHAS gira de CONQUISTA 7/11/20[/B]", "Dq5EE5765x4", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]LA PARKA vs L.A. PARK: LUCHA POR EL NOMBRE (7/8/20)[/B]", "CQbIMGapMoc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Sharlie Rockstar vs Chuck Palumbo, Copa Mundial (7/8/20)[/B]", "Yhzz0RK0Qvs", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]El Angel vs Eterno, Campeonato Intercontinantal Medio IWRG (7/6/20)[/B]", "hgr7XczH97U", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]International Wrestling League #4 (7/5/20)[/B]", "2fX1xiys7Ng", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]International Wrestling League #3 (7/3/20)[/B]", "200QB8m3i9c", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Cien Caras Jr. vs Psycho Clown, Campeonato Completo IWRG (7/3/20)[/B]", "t-WmCrxIJGM", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]CMLL 82 Aniversario MASCARA vs MASCARA, : ATLANTIS VS LA SOMBRA[/B]", "hbK65SDkxLI", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA TRIPLEMANIA XXV 6/27/20[/B]", "nL2IMdr8QUg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]CMLL 81 Aniversario MASCARA vs MASCARA, ATLANTIS vs ULTIMO GUERRERO[/B]", "Ql7bPQWs0Jc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]ROW: Lucha Libre in Texas City[/B]", "DzUQ39ljoPc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]DTU - Rancho de Mexico[/B]", "7RcA-5WHjPg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA en Nueva York 6/20/20[/B]", "78aS558B-a4", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Conquista Total En Cancun[/B]", "T4ObH1qCmWo", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Vanguardia, Tierra de Oportunidades 6/20/20[/B]", "FAU7gFpydjs", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]CHATO: Lucha Memes y TWE 6/17/20[/B]", "fY5n5uYEZj8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]CMLL 80 Aniversario 4 Mascaras En Juego[/B]", "-i81PiJwjCI", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #23, iFaby Apache vs Taya![/B]", "6eKQdlL0rbw", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #22, iOctagon vs Pentagon Jr.[/B]", "HQYks9dP8Ek", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #21, Sexy Lady vs Lolita[/B]", "RPmR0PKKXzI", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #20, La Parka, Fenix y Electro vs Pentagon Jr, Parka Negra y Chessman[/B]", "7ywoEXqy-2c", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #19, Revancha Perros del Mal vs Mexican Powers[/B]", "MZXVtLrsg7Y", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #18, Gran Final por el Campeonato Fusion[/B]", "0zdENYXi-Vs", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #17, Mexican Powers vs Perros del Mal[/B]", "NOQ4wO7_GG0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #16, Psycho Circus vs Inferno Rockers[/B]", "t06xJPMD6f0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #15, El debut de Pentagon Jr.[/B]", "ueGjFosGgq8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #14, Lucha de bellezas[/B]", "S8dRpZ4L7rs", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #13, Gran Final Reina de Reinas 2012[/B]", "4OINo61-aVo", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #12, Reina de Reinas 2012 en Japon[/B]", "KTLpP7zRJbA", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #11, Guerra de Titanes[/B]", "ox3Lxv0hs1M", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #10, Los Perros del Mal vs El Consejo[/B]", "NXXNlFwaMm8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #9, Funcion dedicada a Hector Garza[/B]", "k9jJ-NM-e3k", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #8, El Hijo del Perro y Cibernetico frente a frente[/B]", "GSmgwpsl4t8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #7, El Mesias y El Texano Jr. frente a frente[/B]", "itixIXN4Al4", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #6, Inicia el camino por el Campeonato Fusion[/B]", "hIw01Z5nEc4", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #5, iRevancha! L.A. Park y Dr. Wagner Jr. vs El Consejo[/B]", "ibiJUBgSQ3I", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #4, Los Mexitosos vs Los Perros del Mal[/B]", "2_1hFkR3kmk", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #3, El Vampiro quiere acabar con Chessman[/B]", "2Vf1DKblC8c", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #2, L.A. Park y Dr. Wagner Jr. vs El Consejo[/B]", "pEI5cN9yFEg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]AAA Fusion #1, Perros del Mal vs Cibernetico, Mesias y Cuervo[/B]", "73F6TB5b6bk", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Triplemania Regia 2019[/B]", "thicOEd11n8", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Rey De Reyes 2019 Parte 1[/B]", "ZPN4BgzL5cM", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Rey De Reyes 2019 Parte 2[/B]", "QzzceTQm9_c", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: VERANO DE ESCANDALO 2019 Parte 1[/B]", "Af_UHv4luW4", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: VERANO DE ESCANDALO 2019 Parte 2[/B]", "x0NdLGp3ZDk", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: TRIPLEMANIA XXVII Parte 1[/B]", "GDYbpbi3Frc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: TRIPLEMANIA XXVII Parte 2[/B]", "lrFO6KEHd8I", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Heroes Inmortales XIII Parte 1[/B]", "VwoNog47P1g", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Heroes Inmortales XIII Parte 2[/B]", "CVj5JZDJNC4", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Heroes Inmortales XII Parte 1[/B]", "c1ykh0U5R4Q", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Heroes Inmortales XII Parte 2[/B]", "zYEPvie813A", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: GUERRA DE TITANES 2019 Parte 1[/B]", "wFYnN3O9--g", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: GUERRA DE TITANES 2019 Parte 2[/B]", "cbhIM97jBCY", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: GUERRA DE TITANES 2018 Parte 1[/B]", "YL8zHaKay-o", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: GUERRA DE TITANES 2018 Parte 2[/B]", "aWEIUszhDCw", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter EPISODIO 1: 4/18/2020[/B]", "f61BZMsrSJ0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter EPISODIO 2: 4/25/2020[/B]", "dmStZtQJ9Ow", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter EPISODIO 3: 5/02/2020[/B]", "IBBNfskn3bU", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Libre AAA: Lucha Fighter EPISODIO 4: 5/09/2020[/B]", "25PVP1ndAvM", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Las Mejores Luchas en Rey De Reyes 2018-2019[/B]", "w0BixgDtLnI", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: 10 Way Match 12/17/14[/B]", "HtJsFSI7RoQ", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Triple Threat Ladder Match 12/10/14[/B]", "pgNannte8js", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Puma vs Big Ryck Boyle Heights Street Fight 11/26/14[/B]", "t6xJ0MG3WJg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Johnny Mundo vs. Prince Puma 10/29/14[/B]", "FihfGAXEf5g", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Prince Puma vs Cage 1/28/15[/B]", "wLuB6R5_yyg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Prince Puma vs. Fenix 1/14/15[/B]", "lhfq-IfhX2g", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Alberto El Patron vs. Texano 3/4/15[/B]", "9ErWZPSLV8g", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: King Cuerno vs. Johnny Mundo 3/11/15[/B]", "_TJAqqqUuuY", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Grave Consequences 3/18/15[/B]", "Icvizxc3UB0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Prince Puma vs Cage - Boyle Heights Street Fight 3/25/15[/B]", "2Vyt50AMB-4", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Sexy Star, Super Fly, Pentagon Jr VS Big Ryck, Killshot, The Mack[/B]", "5KSwM0QlgHU", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Prince Puma vs King Cuerno 4/8/15[/B]", "NGagZ4hjJEA", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Prince Puma vs Drago (TITLE vs CAREER) 4/29/15[/B]", "F_A7Y9GnQTE", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Alberto El Patron vs Johnny Mundo 5/6/15[/B]", "6VlQq6CBFfE", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Trios Championship Ladder Match 5/20/15[/B]", "3_G1INQGhHE", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Sexy Star vs Pentagon Dark Submission Match 6/3/15[/B]", "2llO7foYodc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: 4-Way #1 Contender Match 6/10/15[/B]", "Wqz_2aRJOPg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Ultima Lucha: Vampiro vs Pentagon Jr CERO MIEDO MATCH[/B]", "rDR6tOXzt6Q", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Ultima Lucha: Prince Puma vs Mil Muertes 2015[/B]", "_5srvkegnIg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Ultima Lucha Dos: Prince Puma vs. Rey Mysterio Jr[/B]", "KpOPHiSn5yI", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Sexy Star/Mariposa vs. Ivelisse/Taya 6/22/16[/B]", "ojPGdPGp2Xc", 801, "WOMEN", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Matanza vs Mil Muertes - GRAVER CONSEQUENCES 5/11/16[/B]", "veKO3mbdXM0", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Sexy Star vs Mariposa NO MAS MATCH 5/4/16[/B]", "V9MLmHnmIr0", 801, "WOMEN", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Cage vs Johnny Mundo STEEL CAGE MATCH 4/27/16[/B]", "cubGnGtx7Ms", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Fenix vs Mil Muertes - LUCHA UNDERGROUND CHAMPIONSHIP 3/16/16[/B]", "KAKuplo_a3Q", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Prince Puma vs Pentagon Jr. vs Mil Muertes 3-WAY TITLE MATCH 3/9/16[/B]", "CcEhvlbTC_c", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Fenix vs King Cuerno - Gift Of the Gods LADDER MATCH 3/2/16[/B]", "xxqPJyleRtE", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: PJ Black vs Cage vs Jeremiah Crane vs The Mack[/B]", "uUgH3TQUNRg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Rey Mysterio Jr vs Chavo Guerrero Jr LOSER LEAVES LUCHA 11/2/16[/B]", "5FjtcmGlfxc", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Johnny Mundo vs. Sexy Star GIFT OF THE GODS CHAMPIONSHIP 10/26/16[/B]", "oz7aUDag1xg", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: Pentagon Dark vs Rey Mysterio Jr vs Chavo Guerrero Jr 10/12/16[/B]", "JBFB-AdKSVk", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: TRIOS CHAMPIONSHIP MATCH 9/21/16[/B]", "-BPUCaR6iMQ", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: WEAPONS OF MASS DESTRUCTION MATCH 9/14/16[/B]", "G528k2-bPOY", 801, "LUCHA", art+'dvd.jpg', fanart),
        ("[B]Lucha Underground: TRIPLE THREAT LADDER MATCH 12/10/14[/B]", "pgNannte8js", 801, "LUCHA", art+'dvd.jpg', fanart),
]

#=====================================

class luchaListing:

    @staticmethod
    def Genres(type):
		
        #errorMsg="%s" % (type)
        #xbmcgui.Dialog().ok("type", errorMsg)

        for name, url, zmode, genre, icon, fanart in channellist:

            addIt=False
            if type is "All":
                icon=art+"lucha.jpg"
                addIt=True

            elif type is "lucha" and 'LUCHA' in genre:
                icon=art+"lucha.jpg"
                addIt=True

            elif type is "misc" and 'MISC' in genre:
                icon=art+"misc.jpg"
                addIt=True

            elif type is "women" and 'WOMEN' in genre:
                icon=art+"wow.jpg"
                addIt=True
		
            if addIt==True:
	            addLink(name,url,zmode,icon,fanart)

#=====================================

