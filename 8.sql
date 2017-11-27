select Country.Name, Country.Population, Country.SurfaceArea
from Country inner join City on Country.Code = City.CountryCode 
               inner join Capital on Country.Code = Capital.CountryCode
group by Country.Name
having (City.Population = max(City.Population)) and (City.Id <> Capital.CityId)
order by 1.0 * Country.Population / Country.SurfaceArea desc, Country.Name asc;