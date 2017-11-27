select City.name from Country, Capital, City
where Country.Name like 'Malaysia' and Country.Code = City.CountryCode
                                    and Capital.CityId = City.Id;