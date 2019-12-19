import json

NAT_PROJECTS = json.loads('''
    [
        {
            "id": "2059",
            "code": "A",
            "meta_id": "2059",
            "start_date": "2019-06-04 01:23:52.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Культура\\"",
            "title_short": "Культура",
            "curator": "Голодец Ольга Юрьевна  - Заместитель Председателя Правительства Российской Федерации",
            "responsible": "МЕДИНСКИЙ ВЛАДИМИР РОСТИСЛАВОВИЧ - Министр культуры Российской Федерации",
            "admin": "Ярилова Ольга Сергеевна - Заместитель Министра культуры Российской Федерации",
            "project_start_date": "2019-01-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2060",
            "code": "D",
            "meta_id": "2060",
            "start_date": "2019-06-27 02:55:16.0",
            "end_date": "",
            "title_full": "Национальная программа \\"Цифровая экономика\\"",
            "title_short": "Цифровая экономика",
            "curator": "Акимов Максим Алексеевич - Заместитель Председателя Правительства",
            "responsible": "Носков Константин Юрьевич - Министр цифрового развития, связи и массовых коммуникаций",
            "admin": "Кисляков Евгений Юрьевич - Заместитель Министра цифрового развития, связи и массовых коммуникаций",
            "project_start_date": "2018-10-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2061",
            "code": "E",
            "meta_id": "2061",
            "start_date": "2019-06-04 01:23:54.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Образование\\"",
            "title_short": "Образование",
            "curator": "Голикова Татьяна Алексеевна - Заместитель Председателя Правительства",
            "responsible": "Васильева Ольга Юрьевна - Министр просвещения",
            "admin": "Ракова Марина Николаевна - Заместитель Министра просвещения",
            "project_start_date": "2018-11-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2062",
            "code": "F",
            "meta_id": "2062",
            "start_date": "2019-06-04 01:23:48.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Жилье и городская среда\\"",
            "title_short": "Жилье и городская среда",
            "curator": "Мутко Виталий  Леонтьевич  - Заместитель Председателя Правительства",
            "responsible": "Якушев Владимир Владимирович - Министр строительства и жилищно-коммунального хозяйства",
            "admin": "Костарева Татьяна Юрьевна - Статс-секретарь – заместитель Министра строительства и жилищно-коммунального хозяйства",
            "project_start_date": "2018-10-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2063",
            "code": "G",
            "meta_id": "2063",
            "start_date": "2019-06-13 08:08:20.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Экология\\"",
            "title_short": "Экология",
            "curator": "Гордеев Алексей  Васильевич - Заместитель Председателя Правительства",
            "responsible": "Кобылкин Дмитрий Николаевич - Министр природных ресурсов и экологии",
            "admin": "Храмов Денис Геннадьевич - Первый заместитель Министра",
            "project_start_date": "2018-10-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2064",
            "code": "I",
            "meta_id": "2064",
            "start_date": "2019-06-04 01:24:02.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Малое и среднее предпринимательство и поддержка индивидуальной предпринимательской инициативы\\"",
            "title_short": "Малое и среднее предпринимательство и поддержка индивидуальной предпринимательской инициативы",
            "curator": "Силуанов Антон Германович - Первый заместитель Председателя Правительства - Министр финансов",
            "responsible": "Орешкин Максим Станиславович - Министр экономического развития",
            "admin": "Живулин Вадим Александрович - Заместитель Министра экономического развития",
            "project_start_date": "2018-10-15 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2065",
            "code": "L",
            "meta_id": "2065",
            "start_date": "2019-06-04 01:23:42.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Производительность труда и поддержка занятости\\"",
            "title_short": "Производительность труда и поддержка занятости",
            "curator": "Силуанов Антон Германович - Первый заместитель Председателя Правительства - Министр финансов",
            "responsible": "Орешкин Максим Станиславович - Министр экономического развития",
            "admin": "Засельский Петр Владимирович - Заместитель Министра",
            "project_start_date": "2018-10-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2066",
            "code": "N",
            "meta_id": "2066",
            "start_date": "2019-06-04 01:24:05.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Здравоохранение\\"",
            "title_short": "Здравоохранение",
            "curator": "Голикова Татьяна Алексеевна - Заместитель Председателя Правительства",
            "responsible": "Скворцова Вероника Игоревна - Министр здравоохранения",
            "admin": "Хорова Наталья Александровна - Заместитель Министра",
            "project_start_date": "2018-10-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2067",
            "code": "P",
            "meta_id": "2067",
            "start_date": "2019-06-04 01:23:46.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Демография\\"",
            "title_short": "Демография",
            "curator": "Голикова Татьяна Алексеевна - Заместитель Председателя Правительства",
            "responsible": "Топилин Максим Анатольевич - Министр труда и социальной защиты",
            "admin": "Вовченко Алексей Витальевич - Первый заместитель Министра труда и социальной защиты",
            "project_start_date": "2019-01-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2068",
            "code": "R",
            "meta_id": "2068",
            "start_date": "2019-06-04 01:24:12.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Безопасные и качественные автомобильные дороги\\"",
            "title_short": "БКАД",
            "curator": "Акимов Максим Алексеевич - Заместитель Председателя Правительства",
            "responsible": "Дитрих Евгений Иванович - Министр транспорта ",
            "admin": "Алафинов Иннокентий Сергеевич - Первый заместитель Министра",
            "project_start_date": "2018-12-03 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2070",
            "code": "T",
            "meta_id": "2070",
            "start_date": "2019-06-04 01:24:09.0",
            "end_date": "",
            "title_full": "Национальный проект \\"Международная кооперация и экспорт\\"",
            "title_short": "Международная кооперация и экспорт",
            "curator": "Силуанов Антон Германович - Первый заместитель Председателя Правительства - Министр финансов",
            "responsible": "Мантуров Денис Валентинович - Министр промышленности и торговли",
            "admin": "Осьмаков Василий Сергеевич - Заместитель Министра",
            "project_start_date": "2018-10-01 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }, {
            "id": "2071",
            "code": "V",
            "meta_id": "2071",
            "start_date": "2019-10-15 22:40:21.0",
            "end_date": "",
            "title_full": "Транспортная часть комплексного плана модернизации и расширения магистральной инфраструктуры на период до 2024 года",
            "title_short": "Комплексный план модернизации и расширения магистральной инфраструктуры",
            "curator": "Акимов Максим Алексеевич - Заместитель Председателя Правительства",
            "responsible": "Дитрих Евгений Иванович - Министр транспорта ",
            "admin": "Алафинов Иннокентий Сергеевич - Первый заместитель Министра",
            "project_start_date": "2018-07-30 00:00:00.0",
            "project_end_date": "2024-12-31 00:00:00.0",
            "updated_outer": "2019-12-13 10:44:44.0"
        }
    ]
''')
