select * from `Flight` where DepartureTime >= '2023-11-07';
select * from `Flight` where Status = 'Delayed';
select DISTINCT c.FirstName, c.LastName from `Purchase` as p, `Customer` as c where c.email = p.email;
select * from `Airplane` where AirlineName = 'Jet Blue';