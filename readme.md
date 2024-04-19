# Model ewolucyjny w oparciu o Geometryczny Model Fishera (GMF)

## Opis projektu

W tym projekcie, staraliśmy się przedstawić sukcesywną adaptację organizmów do nieustannie zachodzących w środowisku zmian. Opisujemy tutaj ewolucję populacji P, składającej się z osobników o genotypie składającym się z n cech w zadanym środowisku. 

Do wizualizacji aplikacji użyliśmy frameworku Streamlit, który pozwala na wybór parametróe i wizualizację zachodzących procesów. 

Rozważamy populację rozmnażającą się bezpłciowo, z osobnikami żyjącym tylko w jednym pokoleniu - na każde kolejne pokolenie składają się dzieci osobników z poprzedniego pokolenia. W populacji występuje optymalny genotyp, do którego dążą osobniki, a miarą ich dopasowania jest fitness, czyli odległość euklidesowa cech genotypu.
W modelu wprowadziliśmy także trzy tryby, które pozwalają na wybór ilości zasobów środowiska i będą wpływać na elastyczność dopasowania, a co za tym idzie także na liczebność populacji:
-'Limited resources'
-'Standard':
-'Many resources'
Liczba potomstwa opisana jest rozkładem Poissona oraz aby ograniczyć zbytni przyrost populacji ograniczyliśmy ją do 8.
Wprowadzone zostało także zjawisko meteoryt, czyli drastyczną zmianę optymalnego genotypu zgodnie z kierunkiem globalnego ocieplenia, która powoduje gwałtowną śmierć wielu osobników.

Jeśli genotyp składa się z więcej niż 2 cech, przeprowadzone zostaje PCA, by zredukować liczbę wymiarów i umożliwić wizualizację. Jednakże na wykresach można odnieść wrażenie, iż genotypy osobników "nie podążają" za optymalnym genotypem, dlatego zachęcamy do weryfikacji.

## Requirements
Aby zainstalować niezbędne biblioteki skorzystaj z komendy: pip install -r requirements.txt
