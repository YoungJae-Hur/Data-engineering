-- INSERT
insert into mytable (name, debut) values ('geunee', '2021-03-29');

-- UPDATE
update mytable
    set debut='1994-05-15'
where
    name = 'jaehur' and id = 1;

-- REPLACE
replace into mytable
(id, name, debut) values
(1, 'yoojin', '1992-02-03');

-- INSERT OR IGNORE
insert or ignore
into mytable (id, name, debut) values (1, 'geunee', '2021-03-29');