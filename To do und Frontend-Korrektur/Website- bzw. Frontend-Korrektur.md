- In der Personen-Anzeige sind die Beiträge grad noch ziemlich ungeordnet. Eine chronologische Anzeige wäre hier am besten. Also etwa in <[https://dev.koenigsberger-zeitungen.de/akteure/lauson](https://dev.koenigsberger-zeitungen.de/akteure/lauson)> die Rezension der »Anmuthigen und Satyrischen Briefe« an den Anfang, danach »Gedicht mit Kommentar« etc. – Und eben die hängenden Einzüge so wie in der Werke-Liste
- Die Reihenfolge der Scans in der Anzeige vieler Beilagen ist häufig ungeordnet; die sekundär überlieferten Jahrgänge sehen auch größtenteils sehr unfertig aus
- bei Theaterkritik fehlt immer ein Spatium zwischen Autor und »Theaterkritik zu etc.«, sieht man etwa hier, ist aber überall so: <[https://dev.koenigsberger-zeitungen.de/1767/90/364#page-363](https://dev.koenigsberger-zeitungen.de/1767/90/364#page-363)> – ähnlich bei Aufsatz: dort ist aber ein Spatium zu viel vorm Doppelpunkt (etwa hier: <[https://dev.koenigsberger-zeitungen.de/akteure/hamann](https://dev.koenigsberger-zeitungen.de/akteure/hamann)>, aber auch sonst überall)
- habe die Kategorien jetzt immer in Singular gemacht, damit die automatische Einfügung der Textart für die Zitation funktioniert (außer bei Kategorien mit »Nachrichten«, da geht nur Plural, aber es sollte auch nie einen Beiträger geben)
- Ein Problem gibt’s mit Titeln (rezensierten Werken), die keinen Autor haben und wo man auch keinen rekonstruieren konnte; da unsere Werke-Liste nach Autoren organisiert ist und in diesem Fall kein Autor zugeordnet ist, laufen solche Titel ins Leere, sind nicht anklickbar und der Scan bzw. ausführliche Titel nirgendwo einsehbar. Beispiel: Die Staats-Verwaltung des Herrn William Pitt in <[https://dev.koenigsberger-zeitungen.de/1764/5](https://dev.koenigsberger-zeitungen.de/1764/5)>. In der Werke-Datei gibt’s 185 solcher Fälle, das lässt sich also nicht über einen Einzelfall lösen. – Vorschlag: entweder ganz unten in der Werke-Liste oder irgendwo anders einen Sammeleintrag für »Anonym« anlegen und dort eben diese 185 Werke alphabetisch nach dem ersten Titelwort geordnet anzeigen (oder unter »nur Beiträger anzeigen«?)
- Die Nachweise für Autorschaftszuweisungen müssen noch angezeigt werden
- die Anzeige von <beitrag id="1764-6-hamann-gedicht"> funktioniert in mehrfacher Hinsicht nicht: <[https://dev.koenigsberger-zeitungen.de/1764/6](https://dev.koenigsberger-zeitungen.de/1764/6)> und

<beitrag id="1764-6-hamann-gedicht">

        <stueck when="1764" nr="6" von="21" bis="22"/>

        <kategorie ref="gedicht"/>

        <werk ref="ramler-hymen" kat="auszug"/>

        <werk ref="ramler-hymen" kat="kommentar"/>

        <akteur ref="hamann">ZH II, 239</akteur>

        <ort ref="kgsb"/>

    </beitrag>  
Eigentlich war das so angedacht: ein von Hamann kommentierter Ramler-Auszug; und Hamann ist für den ganzen Beitrag verantwortlich. Ich schätze aber, es ist sinnvoller, den Ramler-Auszug als eigenen Beitrag zu machen und den Kommentar (mit akteur Hamann) auch als eigenen Beitrag und zwar als Rezension (oder Kurzkommentar? der Übergang ist fließend und so differenziert brauch eigentlich nicht). Die Anzeige und Zitation »Johann Georg Hamann, Gedicht mit Kommentar« ist jedenfalls falsch. Desgleichen in St. 9, <[https://dev.koenigsberger-zeitungen.de/1764/9](https://dev.koenigsberger-zeitungen.de/1764/9)> und 11 <[https://dev.koenigsberger-zeitungen.de/1764/12](https://dev.koenigsberger-zeitungen.de/1764/12)>

- Mehrfachakteure machen Probleme, siehe <[https://dev.koenigsberger-zeitungen.de/1764/10](https://dev.koenigsberger-zeitungen.de/1764/10)>, <[https://dev.koenigsberger-zeitungen.de/akteure/meinhard-jn](https://dev.koenigsberger-zeitungen.de/akteure/meinhard-jn)> und <[https://dev.koenigsberger-zeitungen.de/akteure/home](https://dev.koenigsberger-zeitungen.de/akteure/home)>. – Das muss man in der Stückeanzeige/Zitation anders organisieren: Autor (Home), Werktitel. Übers. von etc (oder Übersetzer ganz weg). Im Home-Werkeintrag: nicht »mit Johann Nicolaus Meinhard (Übers.)«, sondern zwischen Werkeintrag und »Rezensiert«: Übersetzt von: Johann Nicolaus Meinhard. – Im Meinhard-Werkeintrag: nicht »mit Henry Home Kames: (Übers.)«, sondern: »(Übers.) Henry Home Kames: Grundsätze der Kritik etc.«
- <[https://dev.koenigsberger-zeitungen.de/1764/10](https://dev.koenigsberger-zeitungen.de/1764/10)> »Nachrichten zur Lotterie« wird als Beitrag ohne Titel angezeigt; das wird wohl noch gefixt? Desgleichen in St. 12 und wohl sukzessive
- ich weiß nicht so recht, was ich von der automatisierten Anzeige der „Berufe“ unter den Lebensdaten von Personen halten soll, bei <[https://dev.koenigsberger-zeitungen.de/akteure/karsch](https://dev.koenigsberger-zeitungen.de/akteure/karsch)> ist das zB korrupt, auch sonst zumeist nicht sehr zuverlässig; solang man das nicht individuell bearbeiten/korrigieren kann, gefällt mir das eigentlich gar nicht.
- NB später noch einmal schauen, ob er bei der Nahanzeige von S. 22–24 weiterhin Probleme macht ([https://dev.koenigsberger-zeitungen.de/1764/6](https://dev.koenigsberger-zeitungen.de/1764/6)); liegt schätzungsweise daran, dass die Graphiken aus dem GStA zu groß sind
- Die Anzeige von Kommentaren ist noch problematisch, etwa von Lausons Kommentar zu dem Klopstock-Gedicht <[https://dev.koenigsberger-zeitungen.de/1764/37/145](https://dev.koenigsberger-zeitungen.de/1764/37/145)> (<beitrag id="1764-37-lauson-klopstock-done-kommentar">). Wenn das zu kompliziert ist, muss man das allerdings auch nicht erfassen (hier ist eben erst Abdruck eines Klopstock-Gedichts, dann ein Kommentar des Redakteurs Lauson dazu; man kanns aber von der Erfassung her auch beim Klopstock-Gedicht belassen