Model ewolucyjny w oparciu o Geometryczny Model Fishera (GMF)

W tym projekcie, staraliśmy się przedstawić sukcesywną adaptację organizmów do nieustannie zachodzących w środowisku zmian. Opisujemy tutaj ewolucję populacji P, składającej się z osobników o genotypie składającym się z n cech w zadanym środowisku. 

Rozważamy populację rozmnażającą się bezpłciowo, z osobnikami żyjącym tylko w jednym pokoleniu - na każde kolejne pokolenie składają się dzieci osobników z poprzedniego pokolenia. W populacji występuje optymalny genotyp, do którego dążą osobniki, a miarą ich dopasowania jest fitness, czyli odległość euklidesowa cech genotypu.
W modelu wprowadziliśmy także trzy tryby, które pozwalają na wybór ilości zasobów środowiska i będą wpływać na elastyczność dopasowania, a co za tym idzie także na liczebność populacji:
-'Limited resources'
-'Standard':
-'Many resources'
Liczba potomstwa opisana jest rozkładem Poissona oraz aby ograniczyć zbytni przyrost populacji ograniczyliśmy ją do 8.
Wprowadzone zostało także zjawisko meteoryt, czyli drastyczną zmianę optymalnego genotypu zgodnie z kierunkiem globalnego ocieplenia, która powoduje gwałtowną śmierć wielu osobników.

Niestety, problematycznym narzędziem okazało się być PCA, które nie wizualizuje poprawnej odległości między genotypami osobników a optymalnym genotypem. Dlatego też, wizualizacje przedstawimy, na przykładzie dwóch cech genotypu. 


Parametry:
\\N0 - populacja startowa
\\n - liczba cech
\\time - długość trwania populacji - liczba pokoleń
\\opt_genotype_sd - odchylenie standardowe z jakim mutuje optymalny genotyp
\\speed - szybkość zmian
\\pop_genotype_sd - odchylenie standardowe z jakim mutują osobniki w populacji
\\resources - tryb zasobów środowiska
\\meteor_chance - szansa katastrofy naturalnej
\\strength - 
\\mi - 