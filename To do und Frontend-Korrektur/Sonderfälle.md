

Es gibt 1764 zwei Fälle, die sich nicht in das XML-Schema nach Stücken/Beiträgen etc. einfügen lassen:
- Das eine betrifft die Ankündigung der KGPZ (»Nachricht«), eine Art Flugblatt, das einige Tage vor dem erscheinen des ersten Stücks ausgegeben wurde, und einige wichtige programmatische und sonstige Gesichtspunkte enthält und wohl wohl Hamann und Kanter geschrieben wurde. Man könnte es Stück 1 zuordnen, das wäre aber sehr falsch. Am besten einen Reiter vor Stück 1 basteln. Das XML sieht etwa so aus:
	- <beitrag>

        <stueck when="1764" />

        <kategorie ref="ineigenersache" />

        <datum when="1764-01-28" />

        <titel>Nachricht.</titel>

        <akteur ref="hamann" />

        <akteur ref="kanter" />

        <anmerkung>Anzeige und Beschreibung des Zeitungsprojekts, sechs Tage vor dem ersten Stück,

            am 28. Januar 1764 in Königsberg ausgegeben.</anmerkung>

    </beitrag>

- Das zweite ist eine Beilage, die hinten im Jg. 1764 eingebunden war; man wusste offenbar nicht, welchem Stück die Proklamation zuzuordnen ist; wahrscheinlich Ende August in GKPZ erschienen (auf 17. August datiert). Die Proklamation ist als Stück Propaganda der russischen Kaiserin in einem königlich-preußisch privilegierten Königsberger Blatt schon interessant. Aber auch nicht so sehr, dass man da viel basteln müsste; man könnte es auch einfach dem Stück vom 20. August zuordnen und in der Anmerkung halt etwas dazu schreiben.

    <beitrag>

        <stueck when="1764" />

        <kategorie ref="proklamation" />

        <titel>Wir Catharina die Zweyte, von Gottes Gnaden Kayserin und Selbstherrscherin aller

            Reußen thun hiemit jedermänniglich kund und zu wißen…</titel>

        <akteur ref="katharina-ii" />

        <anmerkung>Übersetzung eines Berichts über den versuchten Aufstand zur Befreiung Iwans VI

            und dessen Ermordung, gedruckt in St. Petersburg, 17. August 1764.</anmerkung>

        <!-- unsicher, welchem Stück das beilag -->

    </beitrag>