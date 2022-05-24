# Проект: “Инструментарий для измерения временных задержек до серверов криптобирж”

Руководитель проекта: Казаков Евгений Александрович, Software Engineer, Facebook. НИУ ВШЭ, ФКН ПМИ, 2022

---

## О проекте

Сейчас одним из самых популярных направлений инвестиций является криптовалюта. Торговля этим инструментом осуществляется на специальных криптобиржах. Основными агентами на них выступают частные инвесторы и инвестиционные фонды, которые занимаются высокочастотной торговлей. При работе с огромными объемами криптовалюты основным узким местом становится время, за которое сделки осуществляются на криптобирже.

Трейдеры в фондах и заинтересованные частные инвесторы хотят иметь данные о временных задержках от клика пользователя до появления сделки на сервере криптобиржи. Иными словами, во время совершения сделок с криптовалютой важно смотреть на такой показатель, как **пинг**.

Таким образом, мы решили написать удобную утилиту, которая будет измерять временные задержки и визуализировать их в разрезе сегментов, которые недоступны в базовых функциях, измеряющих пинг. 

## Описание кода программы

В репозитории нашего проекта на Github есть увидеть четыре основных директории: docker, src, .github/workflows и configs.
- docker содержит файлы для запуска Docker;
- src содержит основной код программного обеспечения;
- .github/workflows содержит файлы для настройки CI (проверка линтера и т.д.);
- configs содержит два шаблонных файла конфигурации: первый файл конфигурации предназначен для коннектора, второй – для описания формата работы утилиты в целом.

## Примеры работы

### Пример Lineplot

<img width="787" alt="Screenshot 2022-05-24 at 12 48 27" src="https://user-images.githubusercontent.com/49996697/170003277-49b769f8-9a7d-4ba0-9426-8e2130586032.png">

### Пример Heatmap

<img width="803" alt="Screenshot 2022-05-24 at 12 48 46" src="https://user-images.githubusercontent.com/49996697/170003348-55a68643-323e-43ab-9137-e1e60e05c1de.png">

## Project setup

<code>python3 main.py main_config.json</code>

<code>localhost:8080/data</code>

## Future scope

Проект обладает высоким потенциалом и может быть полезен при работе с криптобиржами как для частных инвесторов, так и для команд в фондах, специализирующихся на высокочастотной торговле.

## Credits to

Telegram: @phyzzmat @Angela3214 @ninachely
