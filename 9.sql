select Tab1.Year, Tab2.Year, Country.Name, 
                 1.0 * (Tab2.Rate - Tab1.Rate) / (Tab2.Year - Tab1.Year)
from Country, LiteracyRate Tab1, LiteracyRate Tab2 
     on Country.Code = Tab1.CountryCode and Country.Code = Tab2.CountryCode 
                                         and Tab1.Year < Tab2.Year
group by Country.Name, Tab1.Year
having Tab2.Year = min(Tab2.Year)
order by 1.0 * (Tab2.Rate - Tab1.Rate) / (Tab2.Year - Tab1.Year) desc;